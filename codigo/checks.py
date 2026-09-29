"""Checks reproducibles del cálculo de P_T(k) (RG y UG con difusión Q).

Cada `check_*` devuelve un dict {id, title, passed, tolerance, worst, details, source}. Las tolerancias
están fijadas ACÁ, con su justificación, con cambios posteriores documentados para C1.2 y C3.2 (ver PROVENANCE.md
secs. 10 y 13). `run_all()` corre todo y escribe resultados/checks.json; test_checks.py los expone a pytest.

Uso:  python checks.py          (~1-2 min)      |      pytest -q test_checks.py

Referencias externas usadas (textos leídos de las copias de la carpeta del director):
  [MAR]  J. Martin, C. Ringeval, V. Vennin, "Encyclopaedia Inflationaris", arXiv:1303.3787v3:
         Eq. (2.17) P_h = 2k^3|mu_k|^2/(pi^2 a^2); Eq. (2.19) P_h0 = 2H^2/(pi^2 M_Pl^2), P_zeta0 = H^2/(8 pi^2 eps1 M_Pl^2);
         Eqs. (2.20)-(2.25) coeficientes a_i^(T), a_i^(S), C = gamma_E + ln2 - 2 = -0.7296, f = 5 (pivote k* = aH);
         M_Pl^2 = (8 pi G)^(-1) (masa de Planck reducida).
  [TASI] D. Baumann, arXiv:0907.5424v2, Eqs. (196), (198): modo exacto y potencia a tiempo finito.
  [BAU]  D. Baumann, Cosmology (CUP 2022), Eq. (8.127)-(8.128): A_t = 2V/(3 pi^2 M_Pl^4), n_t = -2 eps_V.
  [PLA]  Planck 2018 X (arXiv:1807.06211): "purely quadratic potential always predict a large tensor-to-scalar
         ratio (of roughly 0.15)"; ln(10^10 A_s) = 3.044 +- 0.014 (TT,TE,EE+lowE+lensing).
"""
import json
import os
import platform
import sys
import time
from dataclasses import replace
from functools import lru_cache
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

import background as B
from config import Params, params_for
from modes import run_mode

OUT = Path(__file__).parent / "resultados"

C_SL = np.euler_gamma + np.log(2.0) - 2.0     # [MAR] Eq. (2.20)
F_PIVOT = 5.0                                  # [MAR] Eq. (2.20), pivote k* = aH
A_S_PLANCK = float(np.exp(3.044) * 1e-10)      # [PLA] ln(10^10 A_s) = 3.044
N_EXITS = (12.0, 40.0, 70.0, 85.0)             # N_exit (en RG) de los modos de prueba; cubren el rango de la malla


# ------------------------------------------------------------------------------------------ utilidades
@lru_cache(maxsize=None)
def context(potential="quadratic"):
    """Parámetros por defecto del potencial, con phi_i ajustado (N_f(UG)=100), y los fondos de RG y UG."""
    P = params_for(potential)
    P = replace(P, phi_i=B.phi_i_for_ug_duration(P))
    return P, B.solve_background_rg(P), B.solve_background_ug(P)


def k_at_exit(bg, N):
    """k comóvil que sale del horizonte (k = aH) en N."""
    return float(np.exp(N + bg.lnH(N)))


def eps2_at(bg, N):
    """eps2 = d ln(eps1)/dN (flujo de Hubble). Derivada del spline de eps1."""
    return float(bg.eps1.derivative()(N) / bg.eps1(N))


def a0_tensor(eps1, eps2, order):
    """a0^(T) de [MAR] Eq. (2.23) truncado en `order` (0, 1 o 2)."""
    C, f = C_SL, F_PIVOT
    a = 1.0
    if order >= 1:
        a += -2.0 * (C + 1.0) * eps1
    if order >= 2:
        a += (2 * C**2 + 2 * C + np.pi**2 / 2 - f) * eps1**2 + (-C**2 - 2 * C + np.pi**2 / 12 - 2.0) * eps1 * eps2
    return a


def a1_tensor(eps1, eps2):
    """a1^(T) de [MAR] Eq. (2.24). n_T = a1/a0 en el pivote."""
    C = C_SL
    return -2.0 * eps1 + 2.0 * (2 * C + 1.0) * eps1**2 - 2.0 * (C + 1.0) * eps1 * eps2


def _sr_exits(potential, bg):
    """N_exit (desde el inicio) de los modos de C1.2. Cuadrático: los originales (20, 60, 100, 140). Starobinsky: RG dura ~387
    e-folds y las primeras ~300 son un plateau con eps1 ~ 1e-6 (el check sería trivial); se usan 90, 60, 40, 20 e-folds
    ANTES del final de RG, donde eps1 ~ 1e-4..1e-3."""
    if potential == "quadratic":
        return (20.0, 60.0, 100.0, 140.0)
    return tuple(bg.N_end - n for n in (90.0, 60.0, 40.0, 20.0))


def _result(cid, title, passed, tolerance, worst, details, source):
    return dict(id=cid, title=title, passed=bool(passed), tolerance=tolerance,
                worst=float(worst), details=details, source=source)


def _de_sitter_background(H0=1.0, N_end=40.0):
    """Fondo artificial de de Sitter exacto: H = H0, eps1 = 0, X = 0. Solo para C1.1."""
    N = np.linspace(0.0, N_end, 401)
    cst = lambda c: CubicSpline(N, np.full_like(N, c))
    return B.Background(model="dS", N_end=N_end, t_end=float("nan"), lnH=cst(np.log(H0)), eps1=cst(0.0),
                        X_over_H2=cst(0.0), phi=cst(0.0), diag={})


# ------------------------------------------------------------------------------------------ C1: límite estándar
def check_de_sitter_exact():
    """C1.1  En de Sitter exacto el modo de Bunch-Davies es analítico:
    |v|^2 = (1/2k)(1 + (aH/k)^2)  =>  P_T = (2H^2/pi^2 M_P^2) (1 + (k/aH)^2)  ([TASI] Eqs. 196, 198; normalización tensorial de este trabajo).
    Prueba a la vez: integrador, condición de Bunch-Davies, normalización de P_T (decisión 3: <h_ij h_ij>, e.e = 2)
    y las ecuaciones n1-n2 (forma en N de la ecuación de modos)."""
    tol = 1e-5   # error esperado de la condición inicial adiabática: ~(aH/k)^3 con ratio_start = 100 -> 1e-6
    P = Params()
    bg = _de_sitter_background()
    rows = []
    for k in (1e3, 1e5, 1e8):
        r = run_mode(k, bg, P)
        exact = 2.0 / np.pi**2 * (1.0 + r["ratio_final"] ** 2)  # H0 = 1
        rows.append(dict(k=k, P_num=r["P_T"], P_exact=exact, rel_err=r["P_T"] / exact - 1.0))
    worst = max(abs(x["rel_err"]) for x in rows)
    return _result("C1.1", "de Sitter exacto: P_T = 2H^2/(pi^2 M_P^2)(1+(k/aH)^2)", worst <= tol,
                   f"|rel_err| <= {tol:g}", worst, rows, "[TASI] arXiv:0907.5424v2, Eqs. 196, 198; normalización tensorial de este trabajo")


def check_slow_roll_rg(potential="quadratic"):
    """C1.2  RG con el potencial elegido (por defecto V = m^2 phi^2/2; ver _sr_exits para Starobinsky): P_T de los modos vs la expansión slow-roll de [MAR] Eqs. (2.19),(2.23),
    con H, eps1, eps2 evaluados en k = aH. Se exige que el residuo a segundo orden sea O(eps^3).
    Tolerancia: |P/P_NNLO - 1| <= 30 eps1^3 + 2e-5 (piso numérico: error de la condición inicial ~ 1e-6 y
    del pivote); además |P/P_NLO - 1| <= 20 eps1 max(eps1, |eps2|/2).
    Nota (2026-09-21): la cota NLO original era 20 eps1^2. El residuo de truncar en NLO es O(eps1^2, eps1 eps2) por
    [MAR] (2.23) (coeficiente de eps1 eps2 = -0.25). En el cuadrático eps2 ~ 2 eps1 y ambas cotas coinciden; en Starobinsky
    eps2 >> eps1 y la cota original fallaba por construcción (residuo NLO 1.5e-6 = -0.25 eps1 eps2, como predice (2.23)). Se
    generalizó DESPUÉS de ver ese fallo; el criterio principal (NNLO) no cambió y pasaba con margen ~100x."""
    P, bg, _ = context(potential)
    rows, worst_ratio = [], 0.0
    ok = True
    for N in _sr_exits(potential, bg):
        k = k_at_exit(bg, N)
        r = run_mode(k, bg, P)
        H, e1, e2 = float(np.exp(bg.lnH(N))), float(bg.eps1(N)), eps2_at(bg, N)
        LO = 2.0 * H**2 / np.pi**2
        res = {o: r["P_T"] / (LO * a0_tensor(e1, e2, o)) - 1.0 for o in (0, 1, 2)}
        tol2, tol1 = 30 * e1**3 + 2e-5, 20 * e1 * max(e1, abs(e2) / 2)
        ok &= abs(res[2]) <= tol2 and abs(res[1]) <= tol1
        worst_ratio = max(worst_ratio, abs(res[2]) / tol2)
        rows.append(dict(N_exit=N, eps1=e1, eps2=e2, resid_LO=res[0], resid_NLO=res[1], resid_NNLO=res[2],
                         tol_NLO=tol1, tol_NNLO=tol2, pred_LO_dev=-2 * (C_SL + 1) * e1))
    return _result("C1.2", "RG phi^2 vs slow-roll de Martin et al. (LO, NLO, NNLO)", ok,
                   "|resid_NNLO| <= 30 eps1^3 + 2e-5 y |resid_NLO| <= 20 eps1 max(eps1,|eps2|/2)", worst_ratio, rows,
                   "[MAR] Eqs. (2.19),(2.23); worst = max(|resid_NNLO|/tol)")


def check_planck_phi2(potential="quadratic"):
    """C1.3  Comparación con las predicciones conocidas de V ∝ phi^2 y con Planck.
    a) r = P_T/P_zeta0 = 16 eps1 (1 + O(eps)) con P_zeta0 = H^2/(8 pi^2 eps1) [MAR 2.19], tolerancia 1.5% (las
       correcciones NLO de P_T y P_zeta0 son ~0.5-1.2%).
    b) r(N*=50..60) en [0.12, 0.17]: Planck dice 'roughly 0.15' para un potencial cuadrático [PLA].
    c) A_s(N*=60) = P_zeta0 con H, eps1 del código y m = 6e-6 M_P a menos de 10% de Planck (2.10e-9): valida el valor de m
       (que en PROVENANCE 9.1 estaba marcado como [ESTÁNDAR, sin verificar]).
    d) n_T de los modos (diferencia finita en ln k) = a1/a0 de [MAR] Eq. (2.24) a 5e-5; el LO -2 eps1 [BAU 8.128] se
       reporta solo como referencia."""
    P, bg, _ = context(potential)
    m2 = P.m_phys**2
    rows, ok, worst = [], True, 0.0
    for Nstar in (50.0, 60.0):
        N = bg.N_end - Nstar
        k = k_at_exit(bg, N)
        PT = run_mode(k, bg, P)["P_T"]
        H, e1, e2 = float(np.exp(bg.lnH(N))), float(bg.eps1(N)), eps2_at(bg, N)
        Pz0 = H**2 / (8 * np.pi**2 * e1)
        r_code = PT / Pz0
        d = 0.25
        lp = np.log(run_mode(k * np.exp(d), bg, P)["P_T"]) - np.log(run_mode(k * np.exp(-d), bg, P)["P_T"])
        nT_code = lp / (2 * d)
        nT_mar = a1_tensor(e1, e2) / a0_tensor(e1, e2, 2)
        row = dict(N_star=Nstar, eps1=e1, r_code=r_code, r_16eps1=16 * e1, r_over_16eps1=r_code / (16 * e1),
                   A_s_code=Pz0 * m2, A_s_Planck=A_S_PLANCK, nT_code=nT_code, nT_martin=nT_mar, nT_LO=-2 * e1)
        ok &= abs(r_code / (16 * e1) - 1) <= 0.015
        ok &= 0.12 <= r_code <= 0.17
        ok &= abs(nT_code - nT_mar) <= 5e-5
        worst = max(worst, abs(r_code / (16 * e1) - 1), abs(nT_code - nT_mar))
        if Nstar == 60.0:
            row["A_s_rel_dev"] = Pz0 * m2 / A_S_PLANCK - 1.0
            ok &= abs(row["A_s_rel_dev"]) <= 0.10
        rows.append(row)
    return _result("C1.3", "phi^2: r, A_s, n_T vs slow-roll y Planck", ok,
                   "|r/16eps1-1|<=1.5%; r in [0.12,0.17]; |A_s/A_s,Planck-1|<=10% (N*=60); |n_T-a1/a0|<=5e-5",
                   worst, rows, "[MAR] 2.19,2.23,2.24; [BAU] 8.128; [PLA] texto Sec. 'quadratic', Table 1")


def check_planck_starobinsky(potential="starobinsky"):
    """C1.3-S  Predicciones conocidas de Starobinsky (RG) contra el código, a N* = 50 y 60 e-folds antes del final de RG.
    a) r = P_T/P_zeta0 con P_zeta0 = H^2/(8 pi^2 eps1) [MAR 2.19] (orden cero en el sector escalar) vs 12/N*^2 [ESTÁNDAR,
       límite N* >> 1 de Starobinsky; sin verificar contra texto]: tolerancia 15% (correcciones O(1/N*) ~ 4/N* hasta ~8%).
    b) n_s = 1 - 2 eps1 - eps2 (orden cero) vs 1 - 2/N*: tolerancia absoluta 3e-3 (correcciones O(1/N*^2) ~ 1e-3).
    c) A_s(N*=60) con M = config.M_STAROBINSKY vs Planck a 10%. OJO: M se CALIBRÓ con este mismo dato (config.py), así que
       c) NO es una validación independiente: solo confirma que la calibración está bien aplicada.
    d) n_T de los modos (dif. finita en ln k) = a1/a0 de [MAR] Eq. (2.24) a 5e-5 (igual que C1.3).
    Tolerancias fijadas antes de correr el check."""
    P, bg, _ = context(potential)
    m2 = P.m_phys**2
    rows, ok, worst = [], True, 0.0
    for Nstar in (50.0, 60.0):
        N = bg.N_end - Nstar
        k = k_at_exit(bg, N)
        PT = run_mode(k, bg, P)["P_T"]
        H, e1, e2 = float(np.exp(bg.lnH(N))), float(bg.eps1(N)), eps2_at(bg, N)
        Pz0 = H**2 / (8 * np.pi**2 * e1)
        r_code, r_ref = PT / Pz0, 12.0 / Nstar**2
        ns_code, ns_ref = 1.0 - 2.0 * e1 - e2, 1.0 - 2.0 / Nstar
        d = 0.25
        lp = np.log(run_mode(k * np.exp(d), bg, P)["P_T"]) - np.log(run_mode(k * np.exp(-d), bg, P)["P_T"])
        nT_code = lp / (2 * d)
        nT_mar = a1_tensor(e1, e2) / a0_tensor(e1, e2, 2)
        row = dict(N_star=Nstar, eps1=e1, eps2=e2, r_code=r_code, r_12_over_N2=r_ref, r_rel=r_code / r_ref - 1.0,
                   ns_code=ns_code, ns_1_minus_2_over_N=ns_ref, ns_diff=ns_code - ns_ref,
                   A_s_code=Pz0 * m2, A_s_Planck=A_S_PLANCK, nT_code=nT_code, nT_martin=nT_mar, nT_LO=-2 * e1)
        ok &= abs(r_code / r_ref - 1) <= 0.15 and abs(ns_code - ns_ref) <= 3e-3 and abs(nT_code - nT_mar) <= 5e-5
        worst = max(worst, abs(r_code / r_ref - 1) / 0.15, abs(ns_code - ns_ref) / 3e-3, abs(nT_code - nT_mar) / 5e-5)
        if Nstar == 60.0:
            row["A_s_rel_dev"] = Pz0 * m2 / A_S_PLANCK - 1.0
            ok &= abs(row["A_s_rel_dev"]) <= 0.10
            worst = max(worst, abs(row["A_s_rel_dev"]) / 0.10)
        rows.append(row)
    return _result("C1.3-S", "Starobinsky: r, n_s, n_T vs 12/N^2, 1-2/N y [MAR]; A_s (calibración)", ok,
                   "|r/(12/N^2)-1|<=15%; |n_s-(1-2/N)|<=3e-3; |n_T-a1/a0|<=5e-5; |A_s/A_s,Planck-1|<=10% (N*=60, calibración)",
                   worst, rows, "[MAR] 2.19, 2.24; Starobinsky N* >> 1 [ESTÁNDAR]; [PLA] A_s; worst = max(err/tol)")


# ------------------------------------------------------------------------------------------ C2: convergencia
def _spectra(Pv, bgs, ks):
    return np.array([[run_mode(k, bg, Pv)["P_T"] for k in ks] for bg in bgs])  # (modelo, k)


def check_convergence(potential="quadratic"):
    """C2  Convergencia: se varía UN parámetro por vez y se compara con un valor 'verdad' más fino, en 4 modos (12,
    40, 70, 85 e-folds desde el inicio) y en RG y UG. Mide el máximo |P/P_verdad - 1|.
    Criterio: el valor por defecto debe estar dentro de la tolerancia indicada.
      rtol_mode (verdad 1e-13) : defecto 1e-10 -> 1e-7
      rtol_bg   (verdad 1e-13) : defecto 1e-12 -> 1e-7
      n_grid_bg (verdad 80001) : defecto 20001 -> 1e-6   (interpolación por splines cúbicos)
      ratio_start (verdad 1000): defecto 100   -> 1e-5   (qué tan adentro del horizonte se arranca)
      ratio_stop  (verdad 1e-4): defecto 1e-3  -> 1e-5   (qué tan afuera se mide; error esperado ~(k/aH)^2)"""
    P, bg_rg, bg_ug = context(potential)
    ks = [k_at_exit(bg_rg, N) for N in N_EXITS]
    base = _spectra(P, (bg_rg, bg_ug), ks)
    scans = [  # (parámetro, valores, verdad, defecto, tol, re-resolver fondo)
        ("rtol_mode", (1e-6, 1e-8, 1e-10, 1e-12), 1e-13, 1e-10, 1e-7, False),
        ("rtol_bg", (1e-8, 1e-10, 1e-12), 1e-13, 1e-12, 1e-7, True),
        ("n_grid_bg", (101, 201, 501, 2001, 20001), 80001, 20001, 1e-6, True),
        ("ratio_start", (30.0, 100.0, 300.0), 1000.0, 100.0, 1e-5, False),
        ("ratio_stop", (1e-2, 1e-3), 1e-4, 1e-3, 1e-5, False),
    ]

    def run(pname, val, resolve):
        Pv = replace(P, **{pname: val})
        bgs = (B.solve_background_rg(Pv), B.solve_background_ug(Pv)) if resolve else (bg_rg, bg_ug)
        return _spectra(Pv, bgs, ks)

    details, ok, worst = {}, True, 0.0
    for pname, vals, truth, default, tol, resolve in scans:
        Pt = run(pname, truth, resolve)
        errs = {}
        for v in vals:
            errs[str(v)] = float(np.max(np.abs(run(pname, v, resolve) / Pt - 1.0)))
        e_def = errs[str(default)]
        ok &= e_def <= tol
        worst = max(worst, e_def / tol)
        details[pname] = dict(truth=truth, default=default, tol=tol, max_rel_err_by_value=errs, default_ok=bool(e_def <= tol))
    details["_N_exits"] = list(N_EXITS)
    details["_default_vs_default"] = float(np.max(np.abs(base / base - 1)))
    return _result("C2", "Convergencia numérica (tolerancias, resolución del fondo, condición inicial, punto de medida)",
                   ok, "ver details[*].tol (por parámetro)", worst, details,
                   "worst = max(err_defecto/tol) sobre parámetros")


# ------------------------------------------------------------------------------------------ C3: UG vs RG
def check_conservative_limit(potential="quadratic"):
    """C3.1  Límite conservativo: con gamma = 0, Q = Q_i = cte y Lambda_0 = -Q_i (2.11) la UG DEBE ser RG exacta
    ([derivation.md] Sec. 1.5, 'UG conservativa'; 2.14). El código de UG y el de RG son distintos, así que esto prueba
    el camino de UG (quantities_ug, hubble_ug, (2.9) con Q-punto, Lambda_0) contra el de RG. Tolerancia 1e-8 en P_T
    y 1e-6 en N_end."""
    P, bg_rg, _ = context(potential)
    bg0 = B.solve_background_ug(replace(P, gamma=0.0))
    ks = [k_at_exit(bg_rg, N) for N in N_EXITS]
    a = _spectra(P, (bg_rg,), ks)[0]
    b = _spectra(P, (bg0,), ks)[0]
    rel = np.abs(b / a - 1.0)
    dN = abs(bg0.N_end - bg_rg.N_end)
    ok = rel.max() <= 1e-8 and dN <= 1e-6
    return _result("C3.1", "UG con gamma=0 (Q cte) == RG", ok, "max|P_UG/P_RG-1|<=1e-8 y |dN_end|<=1e-6", rel.max(),
                   dict(rel_diff=rel.tolist(), N_end_RG=bg_rg.N_end, N_end_UG_gamma0=bg0.N_end, dN_end=dN),
                   "derivation.md 1.5, 2.5, 2.14")


def check_background_28(potential="quadratic"):
    """C3.2  La ecuación (2.8), Hdot = -phidot^2/2, NO se usó para construir el fondo. Se contrasta con la solución
    integrada: -dlnH/dN = phi_N^2/2 (derivadas de los splines de H(N) y phi(N)) en RG y UG. Vale solo si la solución
    obedece (2.7) y (2.9) (o (2.10)). Tolerancia absoluta 1e-6 en 0 <= N <= N_end - 1.
    Nota (2026-09-21): para Starobinsky se juzga desde N = 1. En UG-Starobinsky phidot_i (slow-roll de V sola) está ~30x por
    debajo del atractor de UG y eps1 salta de 5e-6 a 1.3e-3 en DN = 0.05; ahí la interpolación por splines falla (error
    1.6e-5 en N < 0.05) y converge al refinar la malla (1.6e-5, 3.3e-6, 1.0e-6 para n_grid_bg = 2e4, 8e4, 2e5), mientras que
    en la muestra de 4000 puntos con N>=1 el máximo conservado RG/UG es 7.43e-9. El error del primer e-fold se guarda en details pero no se juzga. Decidido DESPUÉS de
    ver el fallo; el cuadrático no cambia."""
    P, bg_rg, bg_ug = context(potential)
    tol, rows, worst = 1e-6, {}, 0.0
    N_min = 0.0 if potential == "quadratic" else 1.0   # ver nota abajo
    for bg in (bg_rg, bg_ug):
        N = np.linspace(N_min, bg.N_end - 1.0, 4000)
        lhs = -bg.lnH.derivative()(N)
        rhs = 0.5 * bg.phi.derivative()(N) ** 2
        err = float(np.max(np.abs(lhs - rhs)))
        rows[bg.model] = dict(max_abs_err=err, N_at_max=float(N[np.argmax(np.abs(lhs - rhs))]), max_eps1=float(np.max(rhs)))
        if N_min > 0.0:   # informativo, NO juzgado: el primer e-fold
            N0 = np.linspace(0.0, N_min, 4000)
            rows[bg.model]["first_efold_max_abs_err_not_judged"] = float(np.max(np.abs(-bg.lnH.derivative()(N0) - 0.5 * bg.phi.derivative()(N0) ** 2)))
        worst = max(worst, err)
    return _result("C3.2", "(2.8) sobre la solución integrada (RG y UG)", worst <= tol, f"max abs <= {tol:g}", worst, rows,
                   "derivation.md (2.8)")


def p_t_cosmic_time(k, model, P):
    """Integrador INDEPENDIENTE: ecuación (3.9) con el término de masa, en tiempo cósmico t y para h (no v), integrada
    junto con el fondo. No usa N como variable independiente, ni v, ni splines, ni las fórmulas n1-n2 (forma en N),
    ni eps1. Solo comparte con modes.py las decisiones (condición de Bunch-Davies adiabática y P_T = <h_ij h_ij>)."""
    ini = B.initial_state(P)
    if model == "RG":
        q = lambda y: B.quantities_rg(y, P.potential)
    else:
        Q_i, gamma, Lam0 = ini["Q_i"], P.gamma, ini["Lam0"]
        q = lambda y: B.quantities_ug(y, Q_i, gamma, Lam0, P.potential)

    def rhs_bg(t, y):
        d = q(y)
        return [y[1], d["phidd"], d["H"]]

    def ev(t, y):
        d = q(y)
        return -d["Hdot"] / d["H"] ** 2 - 1.0
    ev.terminal, ev.direction = True, 1
    sol = solve_ivp(rhs_bg, (0.0, P.t_max), ini["y0"], method="DOP853", rtol=P.rtol_bg, atol=P.atol_bg,
                    dense_output=True, events=ev)
    t_end = float(sol.t_events[0][0])
    lnaH = lambda t: sol.sol(t)[2] + np.log(q(sol.sol(t))["H"])
    t_s = brentq(lambda t: lnaH(t) - np.log(k / P.ratio_start), 0.0, t_end, xtol=1e-14)
    tgt = np.log(k / P.ratio_stop)
    t_f = brentq(lambda t: lnaH(t) - tgt, 0.0, t_end, xtol=1e-14) if lnaH(t_end) >= tgt else t_end

    ys = sol.sol(t_s)
    d = q(ys)
    a, H, Hd = np.exp(ys[2]), d["H"], d["Hdot"]
    X = B.tensor_mass_term(H, Hd, d["p"], d["lam_bar"])
    omega = np.sqrt(k**2 - a**2 * (2 * H**2 + Hd) - 2 * X * a**2)      # a''/a = a^2 (2H^2 + Hdot)
    h0 = 1.0 / (a * np.sqrt(omega)) + 0j                                # h = sqrt(2) v / a, v = 1/sqrt(2 omega)
    hd0 = h0 * (-1j * omega / a - H)                                    # hdot = h'/a, h' = h(-i omega - aH)

    def rhs(t, y):
        yb = y[:3].real
        d = q(yb)
        a, H = np.exp(yb[2]), d["H"]
        X = B.tensor_mass_term(H, d["Hdot"], d["p"], d["lam_bar"])
        return [yb[1], d["phidd"], H, y[4], -3.0 * H * y[4] - (k**2 / a**2 - 2.0 * X) * y[3]]

    # h ~ 1/(a sqrt(omega)) llega a ser ~1e-40 para k grandes, muy por debajo de atol: se integra h/|h0| (la ecuación es
    # lineal, es solo un reescalado) y se deshace al final. La 1.ª versión de este check no lo hacía y falló (ver PROVENANCE 10).
    s0 = abs(h0)
    y0 = np.concatenate([ys, [h0 / s0, hd0 / s0]]).astype(complex)
    s2 = solve_ivp(rhs, (t_s, t_f), y0, method="DOP853", rtol=P.rtol_mode, atol=P.atol_mode)
    return 2.0 * k**3 * (abs(s2.y[3, -1]) * s0) ** 2 / np.pi**2          # P_T = (k^3/2pi^2) 2 (2 |h|^2)


def check_independent_cosmic_time(potential="quadratic"):
    """C3.3  P_T con el integrador independiente en tiempo cósmico (p_t_cosmic_time) vs modes.py, en RG y UG, 4 modos.
    Verifica la traducción a N/v (pasos n1-n2 de PROVENANCE 9.3) y el manejo de splines. Tolerancia 1e-5."""
    P, bg_rg, bg_ug = context(potential)
    ks = [k_at_exit(bg_rg, N) for N in N_EXITS]
    tol, rows, worst = 1e-5, [], 0.0
    for name, bg in (("RG", bg_rg), ("UG", bg_ug)):
        for N, k in zip(N_EXITS, ks):
            a = run_mode(k, bg, P)["P_T"]
            b = p_t_cosmic_time(k, name, P)
            rel = b / a - 1.0
            worst = max(worst, abs(rel))
            rows.append(dict(model=name, N_exit_RG=N, P_modes=a, P_cosmic=b, rel_diff=rel))
    return _result("C3.3", "Integrador independiente (h en t cósmico) vs modes.py", worst <= tol, f"|rel| <= {tol:g}",
                   worst, rows, "derivation.md (3.9), (4.6); PROVENANCE 9.3 n1-n2")


def check_ug_vs_rg_difference(potential="quadratic"):
    """C3.4  Cuantificación de P_T^UG/P_T^RG y descarte de que sea ruido numérico.
    1) Ruido: se recalcula el cociente variando rtol_mode (1e-8, 1e-12), rtol_bg (1e-13), ratio_start (300),
       ratio_stop (1e-4). 'noise' = máx. variación del cociente. Pasa si min|ratio-1| >= 100 * noise.
    2) Atribución: el cociente numérico debe coincidir con el cociente de la fórmula slow-roll NNLO ([MAR] 2.19, 2.23)
       evaluada con H, eps1, eps2 propios de cada modelo en su cruce k = aH. Solo se juzgan (a priori) los modos con
       max(eps1, |eps2|) <= 0.05 en ambos modelos; tolerancia 30*max(eps1)^3 + 2e-5. El resto se reporta."""
    P, bg_rg, bg_ug = context(potential)
    Ns = np.arange(10.0, 91.0, 10.0)
    ks = [k_at_exit(bg_rg, N) for N in Ns]
    ratio = lambda Pv, bgs: (lambda s: s[1] / s[0])(_spectra(Pv, bgs, ks))
    r0 = ratio(P, (bg_rg, bg_ug))
    variants = {}
    for name, kw, resolve in (("rtol_mode=1e-8", dict(rtol_mode=1e-8), False), ("rtol_mode=1e-12", dict(rtol_mode=1e-12), False),
                              ("rtol_bg=1e-13", dict(rtol_bg=1e-13), True), ("ratio_start=300", dict(ratio_start=300.0), False),
                              ("ratio_stop=1e-4", dict(ratio_stop=1e-4), False)):
        Pv = replace(P, **kw)
        bgs = (B.solve_background_rg(Pv), B.solve_background_ug(Pv)) if resolve else (bg_rg, bg_ug)
        variants[name] = float(np.max(np.abs(ratio(Pv, bgs) - r0)))
    noise = max(variants.values())
    signal_min, signal_max = float(np.min(np.abs(r0 - 1))), float(np.max(np.abs(r0 - 1)))
    ok_noise = signal_min >= 100 * noise

    rows, ok_attr, worst_attr = [], True, 0.0
    for N_rg, k, r_num in zip(Ns, ks, r0):
        pred, eps = {}, {}
        for bg in (bg_rg, bg_ug):
            Nx = brentq(lambda n: n + bg.lnH(n) - np.log(k), 0.0, bg.N_end, xtol=1e-13)
            H, e1, e2 = float(np.exp(bg.lnH(Nx))), float(bg.eps1(Nx)), eps2_at(bg, Nx)
            pred[bg.model] = 2 * H**2 / np.pi**2 * a0_tensor(e1, e2, 2)
            eps[bg.model] = (e1, e2)
        r_pred = pred["UG"] / pred["RG"]
        dev = r_num / r_pred - 1.0
        judged = all(max(e1, abs(e2)) <= 0.05 for e1, e2 in eps.values())
        tol = 30 * max(eps["RG"][0], eps["UG"][0]) ** 3 + 2e-5
        if judged:
            ok_attr &= abs(dev) <= tol
            worst_attr = max(worst_attr, abs(dev) / tol)
        rows.append(dict(N_exit_RG=N_rg, ratio_numeric=float(r_num), ratio_slowroll_NNLO=float(r_pred), dev=float(dev),
                         eps1_RG=eps["RG"][0], eps1_UG=eps["UG"][0], eps2_UG=eps["UG"][1], judged=judged, tol=tol))
    return _result("C3.4", "P_T^UG/P_T^RG: magnitud, ruido numérico y atribución al fondo", ok_noise and ok_attr,
                   "min|ratio-1| >= 100*noise; |ratio/ratio_SR - 1| <= 30 eps^3 + 2e-5 (modos con eps<=0.05)",
                   max(noise / signal_min * 100, worst_attr),
                   dict(ratio=[float(x) for x in r0], signal_min=signal_min, signal_max=signal_max, noise_by_variant=variants,
                        noise=noise, signal_over_noise=signal_min / noise if noise > 0 else float("inf"), attribution=rows),
                   "derivation.md (3.9), (4.7); [MAR] 2.19, 2.23")


def check_negative_control(potential="quadratic"):
    """C3.5  Control negativo: ¿el código detecta una diferencia REAL en la ecuación de modos?
    a) Con lambda_bar equivocado (se omite Q, o sea lambda_bar = Lambda_0 en vez de Lambda_0 + Q) el término de masa
       -2X deja de anularse y P_T^UG debe cambiar mucho: se exige un cambio >= 1e-2 (relativo) en algún modo.
    b) Con X forzado a 0 (lo que dice la derivación), P_T no debe cambiar respecto del X calculado: <= 1e-9.
    Juntos muestran que (i) la ausencia de diferencia entre las ecuaciones de modos de UG y RG no es insensibilidad
    del código y (ii) el término de masa calculado es despreciable."""
    P, bg_rg, bg_ug = context(potential)
    ks = [k_at_exit(bg_rg, N) for N in N_EXITS]
    N = bg_ug.lnH.x
    Q = B.Q_of_N(N, bg_ug.diag["Q_i"], P.gamma)
    H2 = np.exp(2 * bg_ug.lnH(N))
    X2 = bg_ug.X_over_H2(N)

    def variant(x_over_h2):
        return B.Background(model="UG*", N_end=bg_ug.N_end, t_end=bg_ug.t_end, lnH=bg_ug.lnH, eps1=bg_ug.eps1,
                            X_over_H2=CubicSpline(N, x_over_h2), phi=bg_ug.phi, diag=bg_ug.diag)
    base = np.array([run_mode(k, bg_ug, P)["P_T"] for k in ks])
    wrong = np.array([run_mode(k, variant(X2 - Q / H2), P)["P_T"] for k in ks])   # lambda_bar = Lambda_0 (sin Q)
    zero = np.array([run_mode(k, variant(np.zeros_like(N)), P)["P_T"] for k in ks])
    d_wrong, d_zero = np.abs(wrong / base - 1), np.abs(zero / base - 1)
    ok = d_wrong.max() >= 1e-2 and d_zero.max() <= 1e-9
    return _result("C3.5", "Control negativo: lambda_bar sin Q cambia P_T; X=0 no", ok,
                   "max cambio (sin Q) >= 1e-2 y max cambio (X=0) <= 1e-9", d_wrong.max(),
                   dict(N_exits=list(N_EXITS), rel_change_wrong_lambda=d_wrong.tolist(), rel_change_X_zero=d_zero.tolist()),
                   "derivation.md (4.6), (2.6)")


def check_mutations_are_detected():
    """C0  Los checks no son vacuos: si se rompe el código a propósito, el check correspondiente debe FALLAR.
      M1  normalización de P_T x2            -> C1.1 (de Sitter) debe fallar
      M2  signo de eps1 en la ecuación de modos ((1-eps1) -> (1+eps1)) -> C3.3 (integrador independiente) y C1.2 deben fallar
      M3  Lambda_0 de (2.11) errado en 0.01% de Q_i -> C3.1 (UG con gamma=0 == RG) debe fallar
    Si el código mutado lanza una excepción, cuenta como detectado (el check no puede pasar).
    Usa unittest.mock.patch sobre funciones de modes.py / background.py; no modifica archivos."""
    from unittest import mock
    import modes as M

    def bad_rhs(N, y, k, bg):
        vt, w = y
        H, eps, X2 = np.exp(bg.lnH(N)), bg.eps1(N), bg.X_over_H2(N)
        kk = np.exp(2.0 * (np.log(k) - N - bg.lnH(N)))
        return [w, -(1.0 + eps) * w - (kk - (2.0 - eps) - 2.0 * X2) * vt]

    good_power = M.tensor_power

    def passed_or_none(fn):
        try:
            return fn()["passed"]
        except Exception as e:        # código mutado que revienta = check que no pasa
            return f"excepcion: {type(e).__name__}"

    rows = {}
    with mock.patch.object(M, "tensor_power", lambda k, vt, N: 2.0 * good_power(k, vt, N)):
        rows["M1_P_T_x2 -> C1.1"] = passed_or_none(check_de_sitter_exact)
    with mock.patch.object(M, "mode_rhs", bad_rhs):
        rows["M2_signo_eps1 -> C3.3"] = passed_or_none(check_independent_cosmic_time)
        rows["M2_signo_eps1 -> C1.2"] = passed_or_none(check_slow_roll_rg)
    with mock.patch.object(B, "lambda0_from_initial", lambda H_ini, rho_ini, Q_ini: 3.0 * H_ini**2 - (rho_ini + Q_ini) + 1e-4 * Q_ini):
        rows["M3_Lambda0_+0.01%Q -> C3.1"] = passed_or_none(check_conservative_limit)
    detected = {k: (v is not True) for k, v in rows.items()}
    return _result("C0", "Control de mutaciones: los checks detectan código roto", all(detected.values()),
                   "cada mutación debe hacer fallar su check", sum(not d for d in detected.values()),
                   dict(mutation_detected=detected, outcome_of_mutated_check=rows), "-")


ALL_CHECKS = [check_mutations_are_detected, check_de_sitter_exact, check_slow_roll_rg, check_planck_phi2, check_convergence,
              check_conservative_limit, check_background_28, check_independent_cosmic_time,
              check_ug_vs_rg_difference, check_negative_control]


# Batería completa para Starobinsky (misma que la del cuadrático salvo C0/C1.1, que no dependen del potencial, y C1.3, que es propio)
STARO_CHECKS = [check_slow_roll_rg, check_planck_starobinsky, check_convergence, check_conservative_limit,
                check_background_28, check_independent_cosmic_time, check_ug_vs_rg_difference, check_negative_control]


def run_all(verbose=True, potential="quadratic"):
    P, bg_rg, bg_ug = context(potential)
    results, t0 = [], time.time()
    for fn in (ALL_CHECKS if potential == "quadratic" else STARO_CHECKS):
        t1 = time.time()
        r = fn() if potential == "quadratic" else fn(potential)
        dt = round(time.time() - t1, 1)   # solo se imprime: guardarlo haría cambiar checks.json (y sus hashes) en cada corrida
        results.append(r)
        if verbose:
            print(f"[{'PASS' if r['passed'] else 'FAIL'}] {r['id']:5s} {r['title']}  (worst={r['worst']:.3g}, {dt} s)")
    meta = dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                phi_i=P.phi_i, N_end_RG=bg_rg.N_end, N_end_UG=bg_ug.N_end)
    meta["potential"], meta["m_phys"] = potential, P.m_phys
    out = OUT if potential == "quadratic" else OUT / potential   # el cuadrático conserva resultados/checks.json (lo leen las figuras)
    out.mkdir(parents=True, exist_ok=True)
    (out / "checks.json").write_text(json.dumps(dict(meta=meta, checks=results), indent=1, default=float))
    if verbose:
        print(f"{sum(r['passed'] for r in results)}/{len(results)} checks pasan en {time.time() - t0:.1f} s -> {os.path.relpath(out / 'checks.json')}")
    return results


if __name__ == "__main__":
    pot = sys.argv[1] if len(sys.argv) > 1 else "quadratic"
    sys.exit(0 if all(r["passed"] for r in run_all(potential=pot)) else 1)
