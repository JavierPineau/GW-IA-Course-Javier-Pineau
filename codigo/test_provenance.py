"""Estructura del registro y sincronía con resultados guardados, no verdad/cobertura de claims.

validate_provenance no importa ni ejecuta productores. El test de regeneración ejecuta el
generador del registro (incluye sus checks simbólicos), pero no vuelve a integrar fondos/modos
ni verifica cada productor citado. Escribe en un directorio temporal, sin modificar la entrega.
"""
import json
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "provenance"))


def test_provenance_valid():
    import validate_provenance
    assert validate_provenance.validate() == []


def test_numbers_regenerate_identically(tmp_path):
    versioned = ROOT / "provenance" / "numbers.json"
    regenerated = tmp_path / "numbers.json"
    r = subprocess.run([sys.executable, "make_provenance_numbers.py", str(regenerated)], cwd=HERE, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    assert json.loads(regenerated.read_text()) == json.loads(versioned.read_text())


def test_produced_by_requires_a_local_defined_function(tmp_path, monkeypatch):
    import validate_provenance as validator

    (tmp_path / "provenance").mkdir()
    (tmp_path / "producer.py").write_text(
        'raise RuntimeError("el validador no debe importar el productor")\n'
        'def produce():\n    return 1\n'
        'async def async_produce():\n    return 1\n'
        'text = """\ndef fake():\n    pass\n"""\n'
        'class Container:\n    def method(self):\n        pass\n')
    (tmp_path / "figure.png").write_bytes(b"fixture")
    monkeypatch.setattr(validator, "ROOT", tmp_path)
    good = "producer.py::produce"
    number = dict(value=1, statement="fixture", produced_by=good, from_scratch="fixture",
                  from_library="", choices=[])
    doc = dict(claims=[dict(id="fixture", statement="fixture", evidence=[good, "Referencia bibliográfica"],
                           numbers=["fixture"])],
               figures=[dict(file="figure.png", produced_by=good, shows="fixture", from_scratch="fixture",
                             from_library="", choices=[], supports=["fixture"])])

    def save():
        (tmp_path / "provenance/numbers.json").write_text(json.dumps({"fixture": number}))
        (tmp_path / "provenance/claims.yaml").write_text(yaml.safe_dump(doc))

    save()
    assert validator.validate() == []  # la función existe, aun si importar el módulo fallaría
    assert validator._func_ok("producer.py::async_produce") is True
    invalid = [None, False, 123, [], {}, "", "una cita", "producer.py", "producer.py:produce",
               "producer.py::", "producer.py::produce()", "producer.py::produce.extra",
               " producer.py::produce", "producer.py::produce\n", "producer.py::0bad",
               "missing.py::produce", "producer.py::missing", "producer.py::fake", "producer.py::method",
               "../producer.py::produce", "./producer.py::produce", "sub//producer.py::produce",
               str(tmp_path / "producer.py") + "::produce"]
    for ref in invalid:
        assert validator._func_ok(ref) is False, repr(ref)
        number["produced_by"] = doc["figures"][0]["produced_by"] = ref
        save()
        errors = validator.validate()
        assert any("numbers.json[fixture]: produced_by" in e for e in errors), repr(ref)
        assert any("figura figure.png: produced_by" in e for e in errors), repr(ref)
    del number["produced_by"]
    del doc["figures"][0]["produced_by"]
    save()
    assert sum("falta produced_by" in e for e in validator.validate()) == 2
    number["produced_by"] = doc["figures"][0]["produced_by"] = good
    for ref in (None, "producer.py:produce", "producer.py::missing"):
        doc["claims"][0]["evidence"] = [ref]
        save()
        assert any("evidencia no resuelve" in e for e in validator.validate()), repr(ref)
    doc["claims"][0]["evidence"] = ["Referencia bibliográfica"]
    save()
    monkeypatch.setattr(validator, "_func_ok", lambda ref: None)
    assert sum("produced_by no resuelve" in e for e in validator.validate()) == 2


def test_complete_table_coverage_and_datasets():
    import gzip
    import hashlib
    from provenance_tables import build_table_entries
    import provenance_datasets
    entries=build_table_entries()
    for field in ('n_T','r_std','n_s_std'):
        assert sum(k.startswith('equalN_') and k.endswith('_'+field) for k in entries)==8
    source=json.loads((ROOT/'codigo/resultados/leon/comparacion.json').read_text())
    assert sum(k.startswith('leon_table_') for k in entries)==sum(len(r) for r in source['rows'])
    doc=yaml.safe_load((ROOT/'provenance/claims.yaml').read_text())
    nums=json.loads((ROOT/'provenance/numbers.json').read_text())
    for figure in doc['figures']:
        for key in figure['datasets']:
            dataset=nums[key]['value'];path=ROOT/dataset['path']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==dataset['sha256']
            payload=json.loads(gzip.decompress(path.read_bytes()))
            assert payload['axes']
            assert sum(len(l['xy']) for a in payload['axes'] for l in a['lines'])==dataset['points']
