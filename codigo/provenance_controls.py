"""AC-04(a): selección de residuos guardados y conservación del diagnóstico X.

La extracción no ejecuta los checks. collect_mass_residuals sí reintegra los cuatro
fondos con los parámetros conservados en PT_k.npz, sin recalcular modos/figuras.
"""
import ast
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MASS_FILE = "codigo/resultados/provenance_mass_residuals.json"
FUNCTIONS = {
    "C1.1": "check_de_sitter_exact", "C1.2": "check_slow_roll_rg",
    "C1.3": "check_planck_phi2", "C1.3-S": "check_planck_starobinsky",
    "C2": "check_convergence", "C3.1": "check_conservative_limit",
    "C3.2": "check_background_28", "C3.3": "check_independent_cosmic_time",
    "C3.4": "check_ug_vs_rg_difference", "C3.5": "check_negative_control",
    "CL1": "check_continuity_path", "CL2": "check_closed_forms_A2",
    "CL3": "check_mass_term", "CL4": "check_rg_inflaton_equivalence",
}
ALIASES = {
    ("quad", "C1.1", "worst"): "check_deSitter_worst_rel_err",
    ("quad", "C3.1", "worst"): "check_UG_gamma0_vs_RG",
    ("quad", "C3.3", "worst"): "check_independent_integrator",
    ("quad", "C3.4", "signal_over_noise"): "check_signal_over_noise_quad",
    ("leon", "CL4", "max_abs_dlnH"): "leon_RGrec_max_dlnH",
}
NORMALIZED = {"C1.2", "C1.3-S", "C2", "C3.4", "CL4"}


def select(document, path):
    """Selección mecánica de claves/índices de una salida JSON conservada."""
    for key in path:
        document = document[key]
    return document


def reduce_values(values, operation):
    """Reducciones explícitas de campos de salida; no ejecuta productores físicos."""
    if operation == "identity":
        if len(values) != 1:
            raise ValueError("identity exige un solo campo")
        return values[0]
    if operation == "max_abs":
        return max(abs(v) for v in values)
    if operation == "minus_one":
        return values[0] - 1.0
    if operation == "difference":
        return values[0] - values[1]
    if operation == "max_abs_difference":
        return max(abs(a - b) for a, b in zip(values[::2], values[1::2], strict=True))
    if operation == "max_abs_minus_one":
        return max(abs(v - 1.0) for v in values)
    raise ValueError(operation)


def collect_mass_residuals(root=ROOT):
    """Conserva diag.max_abs_X_over_H2 de RG/UG para ambos potenciales."""
    import background as B
    from config import Params

    rows = []
    for potential, folder in (("quadratic", ""), ("starobinsky", "starobinsky/")):
        source = f"codigo/resultados/{folder}PT_k.npz"
        with np.load(root / source, allow_pickle=False) as data:
            saved = ast.literal_eval(data["params"].item())
        saved.setdefault("potential", potential)  # formato histórico del NPZ cuadrático
        if saved["potential"] != potential:
            raise ValueError(f"potencial inesperado en {source}")
        P = Params(**saved)
        for solve in (B.solve_background_rg, B.solve_background_ug):
            bg = solve(P)
            rows.append(dict(potential=potential, model=bg.model, params=asdict(P),
                             params_source=source, produced_by=f"codigo/background.py::{solve.__name__}",
                             N_min=0.0, N_max=bg.N_end, n_grid=P.n_grid_bg,
                             grid="malla uniforme en t del integrador, transformada a N",
                             max_abs_X_over_H2=bg.diag["max_abs_X_over_H2"]))
    return dict(rows=rows)


def build_control_entries(root=ROOT, mass_file=None):
    """Construye entradas con productor, selecciones de inputs y chequeo reproducible."""
    entries = {}

    def add(tag, c, source, index, suffix, paths, operation="identity", kind="raw", scope=None, tolerance=None):
        full_paths = [["checks", index] + p for p in paths]
        document = documents[source]
        key = ALIASES.get((tag, c["id"], suffix),
                          f"control_{tag}_{c['id'].replace('.', '_').replace('-', '_')}_{suffix}")
        module = "checks_leon.py" if tag == "leon" else "checks.py"
        producer = f"codigo/{module}::{FUNCTIONS[c['id']]}"
        inputs = dict(path=source, selectors=full_paths, check_id=c["id"],
                      parameters_source=("codigo/checks_leon.py::scenario1; codigo/background_leon.py::reconstruct"
                                         if tag == "leon" else f"codigo/checks.py::context; potential={dict(quad='quadratic', staro='starobinsky')[tag]}; checks.json::meta"),
                      saved_meta=document.get("meta", {}))
        entries[key] = dict(
            value=reduce_values([select(document, p) for p in full_paths], operation),
            statement=f"{tag}, {c['id']}: {suffix} (selección y reducción explícitas en inputs/check)",
            produced_by=producer, from_scratch="Extracción de campos guardados; operación " + operation,
            from_library=c["source"], choices=[], coverage_block="AC-04(a)",
            inputs=[inputs], metric_kind=kind, scope=scope or {},
            check=dict(method="comparar con la selección de la salida guardada y la reducción indicada",
                       operation=operation, implementation="codigo/provenance_controls.py::reduce_values",
                       producer=producer, saved_criterion=c["tolerance"],
                       local_tolerance=tolerance, saved_control_passed=c["passed"]))

    documents = {}
    for tag, folder in (("quad", ""), ("staro", "starobinsky/"), ("leon", "leon/")):
        source = f"codigo/resultados/{folder}checks.json"
        documents[source] = json.loads((root / source).read_text())
        for index, c in enumerate(documents[source]["checks"]):
            cid, d = c["id"], c["details"]
            if cid not in FUNCTIONS:
                continue

            def metric(suffix, paths, operation="identity", **kwargs):
                add(tag, c, source, index, suffix, paths, operation, **kwargs)

            metric("worst", [["worst"]], kind="normalized" if cid in NORMALIZED else "raw",
                   scope={"field": "worst", "definition_source": f"codigo/{'checks_leon.py' if tag == 'leon' else 'checks.py'}::{FUNCTIONS[cid]}"})
            if cid == "C1.1":
                for i, row in enumerate(d):
                    metric(f"rel_err_k_{row['k']:g}", [["details", i, "rel_err"]], scope={"k": row["k"]})
            elif cid == "C1.2":
                for order in ("LO", "NLO", "NNLO"):
                    metric(f"max_abs_resid_{order}", [["details", i, f"resid_{order}"] for i in range(len(d))], "max_abs",
                           scope={"N_exit": [r["N_exit"] for r in d]})
                    for i, row in enumerate(d):
                        metric(f"resid_{order}_row_{i}", [["details", i, f"resid_{order}"]],
                               scope={"N_exit": row["N_exit"]}, tolerance=row.get(f"tol_{order}"))
            elif cid in ("C1.3", "C1.3-S"):
                rfield = "r_over_16eps1" if cid == "C1.3" else "r_rel"
                rop = "minus_one" if cid == "C1.3" else "identity"
                metric("max_abs_r_resid", [["details", i, rfield] for i in range(len(d))],
                       "max_abs_minus_one" if cid == "C1.3" else "max_abs")
                metric("max_abs_nT_resid", [["details", i, f] for i in range(len(d)) for f in ("nT_code", "nT_martin")], "max_abs_difference")
                if cid == "C1.3-S":
                    metric("max_abs_ns_resid", [["details", i, "ns_diff"] for i in range(len(d))], "max_abs")
                for i, row in enumerate(d):
                    scope = {"N_star": row["N_star"], "model": "RG"}
                    metric(f"r_resid_Nstar_{row['N_star']:g}", [["details", i, rfield]], rop, scope=scope)
                    metric(f"nT_resid_Nstar_{row['N_star']:g}", [["details", i, f] for f in ("nT_code", "nT_martin")], "difference", scope=scope)
                    for field in ("ns_diff", "A_s_rel_dev"):
                        if field in row:
                            metric(f"{field}_Nstar_{row['N_star']:g}", [["details", i, field]], scope=scope)
            elif cid == "C2":
                for parameter, scan in d.items():
                    if parameter.startswith("_"):
                        continue
                    for value in scan["max_rel_err_by_value"]:
                        metric(f"{parameter}_{value}", [["details", parameter, "max_rel_err_by_value", value]],
                               scope={"parameter": parameter, "value": value, "truth": scan["truth"], "default": scan["default"],
                                      "judged": float(value) == scan["default"], "models": ["RG", "UG"], "N_exit_RG": d["_N_exits"]},
                               tolerance=scan["tol"])
            elif cid == "C3.1":
                metric("dN_end", [["details", "dN_end"]], tolerance=1e-6)
                for i in range(len(d["rel_diff"])):
                    metric(f"rel_diff_mode_{i}", [["details", "rel_diff", i]],
                           scope={"mode_index": i, "N_exit_RG": [12, 40, 70, 85][i]}, tolerance=1e-8)
            elif cid == "C3.2":
                for model, row in d.items():
                    for field in ("max_abs_err", "first_efold_max_abs_err_not_judged"):
                        if field in row:
                            metric(f"{model}_{field}", [["details", model, field]],
                                   scope={"model": model, "judged": field == "max_abs_err",
                                          "N_min": 0 if tag == "quad" or field != "max_abs_err" else 1,
                                          "N_max": documents[source]["meta"][f"N_end_{model}"] - 1 if field == "max_abs_err" else 1,
                                          "n_samples": 4000}, tolerance=1e-6 if field == "max_abs_err" else None)
            elif cid == "C3.3":
                for i, row in enumerate(d):
                    metric(f"{row['model']}_Nexit_{row['N_exit_RG']:g}", [["details", i, "rel_diff"]],
                           scope={"model": row["model"], "N_exit_RG": row["N_exit_RG"]}, tolerance=1e-5)
            elif cid == "C3.4":
                for field in ("signal_min", "signal_max", "noise", "signal_over_noise"):
                    metric(field, [["details", field]], scope={"N_exit_RG": [r["N_exit_RG"] for r in d["attribution"]]})
                for variant in d["noise_by_variant"]:
                    metric("noise_" + variant, [["details", "noise_by_variant", variant]], scope={"variant": variant})
                for i, row in enumerate(d["attribution"]):
                    metric(f"attribution_Nexit_{row['N_exit_RG']:g}", [["details", "attribution", i, "dev"]],
                           scope={"N_exit_RG": row["N_exit_RG"], "judged": row["judged"]}, tolerance=row["tol"])
                for subset in ("all", "judged"):
                    selected = [i for i, r in enumerate(d["attribution"]) if subset == "all" or r["judged"]]
                    metric(f"max_abs_attribution_{subset}", [["details", "attribution", i, "dev"] for i in selected], "max_abs",
                           scope={"subset": subset, "N_exit_RG": [d["attribution"][i]["N_exit_RG"] for i in selected]})
            elif cid == "C3.5":
                for field in ("rel_change_wrong_lambda", "rel_change_X_zero"):
                    metric("max_" + field, [["details", field, i] for i in range(len(d[field]))], "max_abs",
                           scope={"N_exit_RG": d["N_exits"]})
                    for i in range(len(d[field])):
                        metric(f"{field}_mode_{i}", [["details", field, i]], scope={"N_exit_RG": d["N_exits"][i]})
            elif cid == "CL1":
                for i, (scenario, fields) in enumerate(d.items()):
                    for field in fields:
                        metric(f"scenario_{i}_{field}", [["details", scenario, field]],
                               scope={"scenario": scenario, "N_min": 0, "N_max": 100, "n_samples": 20001,
                                      "error_type": "absolute" if field == "eps1" else "relative"}, tolerance=1e-6)
            elif cid == "CL2":
                for field in d:
                    metric(field, [["details", field]], scope={"scenario": 1, "gamma": 2.02, "N_min": 0, "N_max": 100, "n_samples": 500}, tolerance=1e-9)
            elif cid == "CL3":
                for i, (scenario, fields) in enumerate(d.items()):
                    for field in fields:
                        judged = field == "max_abs_X_over_H2"
                        metric(f"scenario_{i}_{field}", [["details", scenario, field]],
                               scope={"scenario": scenario, "judged": judged, "N_min": 0 if judged else 100, "N_max": 99.5 if judged else 100},
                               tolerance=1e-8 if judged else None)
            elif cid == "CL4":
                for field in d:
                    metric(field, [["details", field]],
                           scope={"N_min": 1, "N_max": 99, "n_samples": 4000} if field == "max_abs_dlnH" else {"N_star": float(field.split("=")[-1])},
                           tolerance=1e-4 if field == "max_abs_dlnH" else 1e-6)
                metric("max_PT_rel_diff", [["details", field] for field in d if field.startswith("PT_rel_diff")], "max_abs", scope={"N_star": [50, 60]}, tolerance=1e-6)

    mass = json.loads(Path(mass_file or root / MASS_FILE).read_text())
    for i, row in enumerate(mass["rows"]):
        key = f"mass_{row['potential']}_{row['model']}_max_abs_X_over_H2"
        entries[key] = dict(value=row["max_abs_X_over_H2"], statement=f"{row['potential']}, {row['model']}: diag.max_abs_X_over_H2",
                            produced_by=row["produced_by"], from_scratch="background._solve: max(abs(X/H**2)) sobre su malla de fondo",
                            from_library="numpy; scipy.integrate.solve_ivp (DOP853)", choices=[], coverage_block="AC-04(a)",
                            metric_kind="raw", scope={k: row[k] for k in ("potential", "model", "N_min", "N_max", "n_grid", "grid")},
                            inputs=[dict(path=MASS_FILE, selectors=[["rows", i, "max_abs_X_over_H2"]], parameters=row["params"],
                                         parameters_source=row["params_source"])],
                            check=dict(method="selección del diagnóstico conservado; reproducir con collect_mass_residuals usando params del NPZ",
                                       operation="identity", implementation="codigo/provenance_controls.py::collect_mass_residuals",
                                       local_tolerance=None, saved_control_passed=None))
    return entries


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mass-output", type=Path, default=ROOT / MASS_FILE)
    parser.add_argument("--entries-output", type=Path)
    args = parser.parse_args()
    args.mass_output.parent.mkdir(parents=True, exist_ok=True)
    args.mass_output.write_text(json.dumps(collect_mass_residuals(), ensure_ascii=False, indent=1) + "\n")
    if args.entries_output:
        result = build_control_entries(mass_file=args.mass_output)
        args.entries_output.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n")
        print(f"{len(result)} entradas mecánicas -> {args.entries_output}")
