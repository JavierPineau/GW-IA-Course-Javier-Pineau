"""Tests de make_figures.py:
 1. No recalcula: generar las figuras no importa background/modes/checks/run_spectrum (solo lee resultados/).
 2. Reproducibilidad: las tablas gemelas (CSV) que produce coinciden byte a byte con las versionadas en figuras/.
 3. Vigencia: los hashes de entradas del manifest de figuras/ coinciden con los outputs actuales de resultados/
    (si cambian PT_k.npz o checks.json hay que regenerar las figuras: `python3 make_figures.py`).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
FIG = HERE / "figuras"


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def test_make_figures_does_not_recompute(tmp_path):
    # La figura 10 puede existir y regenerarse después: no es salida de fig1.
    unrelated = tmp_path / "fig10_leon_PT_As.csv"
    unrelated.write_text("previous figure 10 data\n")
    code = (f"import sys; sys.path.insert(0, {str(HERE)!r}); import make_figures; make_figures.main({str(tmp_path)!r}); "
            "bad = {'background', 'modes', 'checks', 'run_spectrum', 'scipy'} & set(sys.modules); "
            "assert not bad, f'se importó código de cálculo: {bad}'")
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-800:]
    for name in ("fig1_PT_k_RG_vs_UG", "fig2_convergencia", "fig3_limite_estandar"):
        for ext in ("png", "pdf"):
            assert (tmp_path / f"{name}.{ext}").stat().st_size > 10_000
    assert (tmp_path / "manifest.json").exists()
    man = json.loads((tmp_path / "manifest.json").read_text())
    assert {
        name: {p for p in files if p.endswith(".csv")}
        for name, files in man["figures"].items()
    } == {
        "fig_pt_comparison": {"fig1_PT_k_RG_vs_UG.csv"},
        "fig_convergence": {"fig2_convergencia.csv"},
        "fig_standard_limit": {"fig3a_C1_2_slow_roll.csv", "fig3b_C3_4_atribucion.csv"},
    }
    unrelated.write_text("regenerated figure 10 data\n")
    for files in man["figures"].values():
        for name, digest in files.items():
            assert _sha(tmp_path / name) == digest
    # 2. las tablas gemelas son deterministas y coinciden con las versionadas
    for csv in tmp_path.glob("*.csv"):
        if csv == unrelated:
            continue
        assert _sha(csv) == _sha(FIG / csv.name), f"{csv.name} difiere de figuras/{csv.name}: regenerar y revisar"


def test_figures_are_up_to_date_with_outputs():
    man = json.loads((FIG / "manifest.json").read_text())
    for name, h in man["inputs"].items():
        assert _sha(HERE / "resultados" / name) == h, f"{name} cambió desde que se generaron las figuras: correr make_figures.py"
    assert _sha(HERE / "make_figures.py") == man["script"]["sha256"], "make_figures.py cambió: regenerar las figuras"
    for fn, files in man["figures"].items():
        for fname, h in files.items():
            assert _sha(FIG / fname) == h, f"{fname} no coincide con el manifest"


def test_potenciales_manifest_is_current():
    """Vigencia de las figuras 6-8 (make_figures_potenciales.py): las entradas de resultados/ y las salidas de figuras/
    coinciden con los hashes del manifest. Si cambian resultados/comparacion_N_star.csv o los PT_k.csv, regenerar con
    `python3 make_figures_potenciales.py`."""
    man = json.loads((FIG / "manifest_potenciales.json").read_text())
    assert _sha(HERE / "make_figures_potenciales.py") == man["script"], "make_figures_potenciales.py cambió: regenerar las figuras"
    for dep,digest in man["deps"].items():
        assert _sha(HERE/dep)==digest
    for fname, info in man["figures"].items():
        for rel, h in info["inputs"].items():
            assert _sha(HERE / "resultados" / rel) == h, f"{fname}: la entrada {rel} cambió; regenerar las figuras"
        for name, h in info["outputs"].items():
            assert _sha(FIG / name) == h, f"{fname}: {name} no coincide con el manifest"


def test_leon_manifest_is_current():
    """Vigencia de las figuras 9-10 (make_figures_leon.py): entradas de resultados/leon/ y salidas de figuras/ coinciden con manifest_leon.json."""
    man = json.loads((FIG / "manifest_leon.json").read_text())
    assert _sha(HERE / "make_figures_leon.py") == man["script"], "make_figures_leon.py cambió: regenerar las figuras"
    for dep,digest in man["deps"].items():
        assert _sha(HERE/dep)==digest
    for fname, info in man["figures"].items():
        for rel, h in info["inputs"].items():
            assert _sha(HERE / "resultados" / rel) == h, f"{fname}: la entrada {rel} cambió; regenerar con `python3 make_figures_leon.py`"
        for name, h in info["outputs"].items():
            assert _sha(FIG / name) == h, f"{fname}: {name} no coincide con el manifest"


def test_informe_manifest_is_current():
    """Vigencia de las figuras 4-5 (make_report_figures.py, que RECALCULA fondo y modo): el script, el código de cálculo del que dependen
    (config, background, modes, make_figures) y las salidas de figuras/ coinciden con manifest_informe.json."""
    man = json.loads((FIG / "manifest_informe.json").read_text())
    assert _sha(HERE / "make_report_figures.py") == man["script"], "make_report_figures.py cambió: regenerar con `python3 make_report_figures.py`"
    for f, h in man["deps"].items():
        assert _sha(HERE / f) == h, f"{f} cambió desde que se generaron las figuras 4-5: regenerar con `python3 make_report_figures.py`"
    for fn, files in man["figures"].items():
        for fname, h in files.items():
            assert _sha(FIG / fname) == h, f"{fname} no coincide con manifest_informe.json"


def test_full_recomputed_figure_tables():
    import csv
    def rows(name):
        with open(FIG/name) as f:return list(csv.DictReader(f))
    six=rows('fig6_fondo_starobinsky.csv')
    assert len(six)==8000
    assert {r['model'] for r in six}=={'RG','UG'}
    nine=rows('fig9_fondo_leon.csv')
    assert len(nine)==20001 and float(nine[-1]['N'])==100
    assert {'eps1_g1.5','H_g1.5','Q_g1.5','rho_g1.5'}<=nine[0].keys()
    ten=rows('fig10_leon_scalars.csv')
    assert len(ten)==3 and all(float(r['A_s'])>0 and float(r['r'])>0 for r in ten)
    modes=rows('fig10_leon_PT_As.csv')
    assert sum(r['stopped_early_UGrad']=='True' for r in modes)==2
