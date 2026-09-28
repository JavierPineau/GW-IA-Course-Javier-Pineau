"""Chequeo ESTRUCTURAL del registro. Uso: python3 provenance/validate_provenance.py (desde la raíz).

Comprueba: (1) numbers.json: los seis campos en cada entrada; (2) claims.yaml: cada claim con statement y evidencia; cada `numbers` existe;
(3) las referencias Python apuntan a archivos del repositorio con una función de módulo definida;
(4) cada figura tiene sus campos, su archivo existe, `produced_by` resuelve y `supports` referencia claims existentes.
`produced_by` exige ruta relativa .py::función; evidence admite además citas textuales, que no se verifican.
No importa ni ejecuta productores, no certifica la verdad de los claims ni la cobertura del HTML/PDF.
Devuelve errores estructurales; una lista vacía solo significa que estos chequeos pasan."""
import ast
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ("value", "statement", "produced_by", "from_scratch", "from_library", "choices")
FIG_FIELDS = ("file", "produced_by", "shows", "from_scratch", "from_library", "choices", "supports")


def _func_ok(ref):
    """True solo para una referencia local válida; nunca devuelve None ni ejecuta código."""
    if not isinstance(ref, str):
        return False
    m = re.fullmatch(r"([\w./-]+\.py)::([^\W\d]\w*)", ref)
    if not m:
        return False
    path = Path(m.group(1))
    if path.is_absolute() or any(part in ("", ".", "..") for part in m.group(1).split("/")):
        return False
    try:
        p = (ROOT / path).resolve()
        if not p.is_relative_to(ROOT.resolve()) or not p.is_file():
            return False
        module = ast.parse(p.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, SyntaxError, ValueError, RuntimeError):
        return False
    return any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == m.group(2)
               for node in module.body)


def _evidence_ok(ref):
    # Las citas libres son admisibles, pero una referencia Python mal formada no es una cita.
    if not isinstance(ref, str) or not ref.strip():
        return False
    return _func_ok(ref) if "::" in ref or ".py" in ref else True


def validate():
    errs = []
    nums = json.loads((ROOT / "provenance" / "numbers.json").read_text())
    for k, e in nums.items():
        for f in FIELDS:
            if f not in e:
                errs.append(f"numbers.json[{k}]: falta {f}")
        if isinstance(e.get("choices"), list) is False:
            errs.append(f"numbers.json[{k}]: choices debe ser lista")
        if _func_ok(e.get("produced_by")) is not True:
            errs.append(f"numbers.json[{k}]: produced_by no resuelve: {e.get('produced_by')!r}")
    doc = yaml.safe_load((ROOT / "provenance" / "claims.yaml").read_text())
    ids = {c["id"] for c in doc["claims"]}
    for c in doc["claims"]:
        if not c.get("statement") or not c.get("evidence"):
            errs.append(f"claim {c.get('id')}: falta statement o evidence")
        for ev in c.get("evidence", []):
            if _evidence_ok(ev) is not True:
                errs.append(f"claim {c['id']}: evidencia no resuelve: {ev}")
        for s in c.get("numbers", []):
            if s not in nums:
                errs.append(f"claim {c['id']}: número inexistente: {s}")
    for fg in doc["figures"]:
        for f in FIG_FIELDS:
            if f not in fg:
                errs.append(f"figura {fg.get('file')}: falta {f}")
        if not (ROOT / fg["file"]).exists():
            errs.append(f"figura {fg['file']}: el archivo no existe")
        if _func_ok(fg.get("produced_by")) is not True:
            errs.append(f"figura {fg['file']}: produced_by no resuelve: {fg.get('produced_by')!r}")
        for s in fg.get("supports", []):
            if s not in ids:
                errs.append(f"figura {fg['file']}: supports inexistente: {s}")
    return errs


if __name__ == "__main__":
    e = validate()
    print("\n".join(e) if e else "provenance: chequeo estructural OK (no ejecuta productores ni certifica claims/cobertura)")
    sys.exit(1 if e else 0)
