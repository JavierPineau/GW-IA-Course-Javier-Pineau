"""Genera provenance/numbers.json a partir de los OUTPUTS guardados (resultados/**), sin recalcular el fondo ni los modos.

Cada número lleva los seis campos del formato del curso (día 5): value, statement, produced_by, from_scratch, from_library, choices.
Los valores proceden de salidas conservadas, entradas de configuración y referencias externas identificadas; el resto (declaración, procedencia, decisiones) está en la
tabla SPEC de abajo. Los tres números `symbolic_*` sí ejecutan symbolic_checks.py (~2 s).

Uso:  python3 make_provenance_numbers.py        ->  ../provenance/numbers.json
"""
import csv
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
RES = HERE / "resultados"
OUT = HERE.parent / "provenance" / "numbers.json"

LIB_NUMPY = "numpy 1.26.4, scipy 1.13.1 (solve_ivp DOP853, CubicSpline, brentq)"
STD = "Ecuación de modos y P_T de derivation.md Secs. 3-4; integración por modes.py::run_mode"


def _j(p):
    return json.loads((RES / p).read_text())


def _check(checks, cid):
    return next(c for c in checks["checks"] if c["id"] == cid)


def _pt(path):
    with open(RES / path) as f:
        return list(csv.DictReader(f))


def _row(cmp_, pot, model, ns):
    return next(r for r in cmp_["rows"] if r["potential"] == pot and r["model"] == model and r["N_star"] == ns)


def build():
    q, s, cmp_ = _j("checks.json"), _j("starobinsky/checks.json"), _j("comparacion_N_star.json")
    lc, lcmp = _j("leon/checks.json"), _j("leon/comparacion.json")
    ptq, pts = _pt("PT_k.csv"), _pt("starobinsky/PT_k.csv")
    r57 = next(r for r in lcmp["rows"] if r["scenario"].startswith("1") and "2.02" in r["scenario"] and r["N_star"] == 57.0)
    g15 = next(r for r in lcmp["rows"] if "1.5" in r["scenario"] and r["N_star"] == 60.0)
    map_quad = _check(lc, "CL7")["details"]["quadratic"]
    map_staro = _check(lc, "CL7")["details"]["starobinsky"]
    cl4 = _check(lc, "CL4")["details"]
    from config import M_STAROBINSKY
    import symbolic_checks as SC
    sym = {fn.__name__: fn()["passed"] for fn in SC.ALL_SYMBOLIC}

    def N(value, statement, produced_by, from_scratch, from_library=LIB_NUMPY, choices=()):
        return dict(value=value, statement=statement, produced_by=produced_by, from_scratch=from_scratch, from_library=from_library,
                    choices=list(choices))

    CH_INI = ["Mismas condiciones iniciales en RG y UG (phi_i, phidot_i, H_i), lo que fija Lambda_0 = -Q_i: decisión del usuario; alternativa razonable: Lambda_0 = 0 con H_i distinto.",
              "Q(N) = Q_i exp(-gamma N), Q_i/V_i = 0.1, gamma = 0.1: prescripción fenomenológica que propuse yo y el usuario aceptó sin criterio propio; alternativas: otras formas de Q(N) o Q(phi).",
              "Duración de UG fijada en N_f = 100 e-folds (valor que aparece en A2, escenario 1); RG usa el mismo phi_i y dura más."]
    n = {}
    n["quad_phi_i"] = N(q["meta"]["phi_i"], "phi_i (M_P) del potencial cuadrático tal que UG dura 100 e-folds", "codigo/background.py::phi_i_for_ug_duration",
                        "búsqueda de raíz sobre la duración de UG", choices=CH_INI)
    n["quad_Nend_RG"] = N(q["meta"]["N_end_RG"], "e-folds de inflación en RG (V cuadrático), mismo phi_i que UG", "codigo/background.py::solve_background_rg",
                          "fondo de RG (derivation.md 2.10)", choices=CH_INI[:1])
    n["quad_ratio_equal_k_first"] = N(float(ptq[0]["ratio_UG_over_RG"]), "P_T^UG/P_T^RG a igual k, primer modo (cuadrático)", "codigo/run_spectrum.py::main",
                                      STD, choices=CH_INI + ["Comparación a igual k comóvil con el mismo a_i: mezcla épocas distintas (ver quad_ratio_equal_Nstar_60)."])
    n["quad_ratio_equal_k_last"] = N(float(ptq[-1]["ratio_UG_over_RG"]), "P_T^UG/P_T^RG a igual k, último modo (cuadrático)", "codigo/run_spectrum.py::main",
                                     STD, choices=CH_INI)
    for ns in (50.0, 60.0):
        n[f"quad_ratio_equal_Nstar_{ns:g}"] = N(_row(cmp_, "quadratic", "UG", ns)["PT_UG_over_RG"],
                                                 f"P_T^UG/P_T^RG a igual N* = {ns:g} e-folds antes del final de cada inflación (cuadrático, m = 6e-6 M_P)",
                                                 "codigo/compare_potentials.py::main",
                                                 STD + f"; resultados/comparacion_N_star.json::rows[potential=quadratic, model=UG, N_star={ns:g}].PT_UG_over_RG (división por P_T de RG al mismo N*)",
                                                 choices=CH_INI + ["Criterio a igual N* (decisión del usuario, 2026-09-21); no modela el recalentamiento."])
    n["staro_phi_i"] = N(_j("starobinsky/checks.json")["meta"]["phi_i"], "phi_i (M_P) del potencial de Starobinsky tal que UG dura 100 e-folds",
                         "codigo/background.py::phi_i_for_ug_duration", "búsqueda de raíz", choices=CH_INI)
    n["staro_Nend_RG"] = N(s["meta"]["N_end_RG"], "e-folds de inflación en RG (Starobinsky) con el mismo phi_i que UG", "codigo/background.py::solve_background_rg",
                           "fondo de RG", choices=CH_INI[:1])
    n["staro_M_calibrated"] = N(M_STAROBINSKY, "Entrada redondeada M (M_P) de Starobinsky; receta y residuo de calibración registrados aparte",
                                "codigo/config.py::params_for", "constante config.M_STAROBINSKY; calibración con P_zeta0 = H^2/(8 pi^2 eps1) a N*=60 (M necesario 1.143e-5)",
                                "Planck 2018 X (A_s = exp(3.044)e-10); solo metadatos verificados para Starobinsky 1980 y De Felice-Tsujikawa 2010",
                                ["Es una CALIBRACIÓN, no una validación; un valor de memoria (1.3e-5, N*~52) se descartó antes de correr los controles.",
                                 "Solo se usa la forma del potencial; no se afirma que el origen R^2 valga en UG."])
    for ns in (50.0, 60.0):
        n[f"staro_ratio_equal_Nstar_{ns:g}"] = N(_row(cmp_, "starobinsky", "UG", ns)["PT_UG_over_RG"],
                                                  f"P_T^UG/P_T^RG a igual N* = {ns:g} (Starobinsky, M = 1.14e-5 M_P)", "codigo/compare_potentials.py::main",
                                                  STD + f"; resultados/comparacion_N_star.json::rows[potential=starobinsky, model=UG, N_star={ns:g}].PT_UG_over_RG (división por P_T de RG al mismo N*)",
                                                  choices=CH_INI)
    n["staro_ratio_equal_k_first"] = N(float(pts[0]["ratio_UG_over_RG"]), "P_T^UG/P_T^RG a igual k, primer modo (Starobinsky)", "codigo/run_spectrum.py::main", STD, choices=CH_INI)
    n["staro_ratio_equal_k_last"] = N(float(pts[-1]["ratio_UG_over_RG"]), "P_T^UG/P_T^RG a igual k, último modo (Starobinsky)", "codigo/run_spectrum.py::main", STD, choices=CH_INI)
    n["check_deSitter_worst_rel_err"] = N(_check(q, "C1.1")["worst"], "error relativo máximo de P_T contra la solución exacta de de Sitter",
                                          "codigo/checks.py::check_de_sitter_exact", "solución analítica a tiempo finito: Baumann, arXiv:0907.5424v2, Eqs. 196 y 198; normalización tensorial de este trabajo", choices=["tolerancia 1e-5 fijada a priori"])
    n["check_UG_gamma0_vs_RG"] = N(_check(q, "C3.1")["worst"], "diferencia máxima de P_T entre UG con gamma=0 y RG (deben ser iguales)",
                                   "codigo/checks.py::check_conservative_limit", "camino de UG contra camino de RG del código", choices=["tolerancia 1e-8 fijada a priori"])
    n["check_independent_integrator"] = N(_check(q, "C3.3")["worst"], "diferencia máxima de P_T entre modes.py y un integrador independiente en tiempo cósmico",
                                          "codigo/checks.py::check_independent_cosmic_time", "integrador para h (no v), sin splines, sin N", choices=["tolerancia 1e-5 fijada a priori"])
    n["check_signal_over_noise_quad"] = N(_check(q, "C3.4")["details"]["signal_over_noise"], "cociente señal/ruido numérico de P_T^UG/P_T^RG a igual k (cuadrático)",
                                          "codigo/checks.py::check_ug_vs_rg_difference", "variaciones de rtol, ratio_start/stop", choices=["criterio señal >= 100 x ruido fijado a priori"])
    for k, v in sym.items():
        n[f"symbolic_{k.replace('check_', '')}_passed"] = N(bool(v), f"comprobación simbólica SymPy: {k}", f"codigo/symbolic_checks.py::{k}", "álgebra exacta a primer orden",
                                                            "sympy 1.14.0", ["Solo primer orden; el segundo orden del sector tensorial y la equivalencia perturbativa UG=RG con V_eff no están verificados simbólicamente."])
    CH_L = ["Modelo de arXiv:2202.04029 y arXiv:2307.06329: radiación pura, Lambda_* = 0, dQ = 0, sin inflatón; decisión del usuario (2026-09-21).",
            "Escenario 1 de A2 con N_f = 100, rho_end = 1e-11 M_P^4, gamma = 2.02 (valores de A2); el escenario 2 (N_f ~ 370) no se analiza.",
            "Sector escalar NO derivado: A_s y r usan la fórmula de A2 (H^2/8 pi^2 eps1); las alternativas (A1 con 3^{3/2}; 1/c_s) se reportan aparte."]
    n["leon_A_s_A2_Nstar57"] = N(r57["A_s_A2"], "A_s predicha con el modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329), escenario 1 (gamma=2.02) a N*=57, fórmula escalar de A2", "codigo/run_leon.py::main",
                                 "reconstrucción del fondo desde eps1(N) (background_leon.py::reconstruct)", "A2 Eqs. 41, 44-48; Planck 2018 X (comparación)", CH_L)
    n["leon_A_s_A1_Nstar57"] = N(r57["A_s_A1"], "A_s con la fórmula de A1 (Eq. 66, factor 3^{3/2}) en el mismo punto", "codigo/run_leon.py::main", "P_R^{A1} = 3^{3/2} P_R^{A2} (condicional)",
                                 "A1 Eq. 66", CH_L)
    n["leon_r_A2_Nstar57"] = N(r57["r_A2"], "r = P_T/P_R con la fórmula de A2 en el punto de referencia", "codigo/run_leon.py::main", "P_T numérico de los modos / P_R de A2 (condicional)", "A2 Eqs. 41-42", CH_L)
    n["leon_P_T_Nstar57"] = N(r57["P_T"], "P_T numérico con el modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329) (gamma=2.02, N*=57)", "codigo/run_leon.py::main", STD, choices=CH_L)
    n["leon_nT_Nstar57"] = N(r57["n_T"], "n_T (diferencia finita en ln k) con el modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329) (gamma=2.02, N*=57)", "codigo/run_leon.py::main", "diferencia finita central en ln k, paso 0.25", choices=CH_L)
    n["leon_As_gamma1p5_Nstar60"] = N(g15["A_s_A2"], "A_s de A2 para gamma=1.5 a N*=60 (A2 descarta este valor con los datos)", "codigo/run_leon.py::main", "ídem", "A2 Sec. IV.A", CH_L)
    n["leon_RGrec_max_dlnH"] = N(cl4["max_abs_dlnH"], "máx |ln H| de RG con inflatón reconstruido menos el del fondo radiación+Q", "codigo/checks_leon.py::check_rg_inflaton_equivalence",
                                 "reconstrucción de V(phi) desde eps1 y H (phidot^2 = 2 eps1 H^2, V = (3-eps1) H^2) e integración de Klein-Gordon de RG", choices=["tolerancia 1e-4 fijada a priori"])
    n["leon_mapping_offset_quadratic_Nstar60"] = N(map_quad["offset_rel_N60"], "P_T^RG/P_T^mapa - 1 a N*=60 (escenario 3, cuadrático): desfasaje del mapeo slow-roll normalizado en el final",
                                                    "codigo/checks_leon.py::check_slowroll_map_vs_rg", "mapeo eps1(N)=eps_V(phi(N)); RG numérico con la misma escala en el final",
                                                    "A2 Sec. III.C", ["Criterio original |offset| <= 10% FALLÓ; se reemplazó por criterio de forma (3%) y el offset pasó a ser resultado (ver PROVENANCE sec. 14)."])
    n["leon_mapping_offset_starobinsky_Nstar60"] = N(map_staro["offset_rel_N60"], "ídem para Starobinsky", "codigo/checks_leon.py::check_slowroll_map_vs_rg", "ídem", "A2 Sec. III.C",
                                                     ["Ídem: el criterio original de 10% falló."])
    from provenance_controls import build_control_entries
    n.update(build_control_entries())
    from provenance_tables import build_table_entries
    n.update(build_table_entries())
    from provenance_diagnostics import build_diagnostic_entries
    n.update(build_diagnostic_entries())
    from provenance_external import build_external_entries
    n.update(build_external_entries())
    from provenance_scenarios import build_scenario_entries
    n.update(build_scenario_entries())
    from provenance_datasets import build_dataset_entries
    n.update(build_dataset_entries())
    from calibrate_scale import build_calibration_entries
    n.update(build_calibration_entries())
    resolution = _j("resolution_checks.json")
    for field in ("worst_edge", "worst_tilt", "edge_tolerance", "tilt_absolute_tolerance"):
        n["resolution_" + field] = N(resolution[field], "AC-25: " + field,
            "codigo/checks_resolution.py::check_resolution",
            "resultados/resolution_checks.json::" + field,
            choices=["8 extremos, 8 índices a N*=50,60; no cubre toda la tabla de radiación con Q",
                     "Criterios exploratorios conservados de la sesión anterior: 1e-5 relativo y 2e-5 absoluto"])
    return n


def main(out=None):
    """Escribe numbers.json en `out` (por defecto, provenance/numbers.json versionado)."""
    out = Path(out) if out else OUT
    n = build()
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(n, indent=1, ensure_ascii=False, default=float) + "\n")
    print(f"{len(n)} números -> {out}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)
