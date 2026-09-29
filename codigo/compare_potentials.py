"""Comparación RG vs UG a igual número de e-folds ANTES DEL FINAL, para los dos potenciales (cuadrático y Starobinsky).

Uso:  python compare_potentials.py        (~1 min)   ->  resultados/comparacion_N_star.csv / .json

Por qué este criterio: con el mismo phi_i RG dura mucho más que UG (cuadrático 162 vs 100 e-folds; Starobinsky 387 vs 100), así
que comparar a igual k mezcla épocas distintas. Acá cada modelo se mide en el modo que sale del horizonte N_* e-folds antes del
final de SU inflación (N_* = 50 y 60). Decisión del usuario (2026-09-21, «opción recomendada»); las demás decisiones (mismo
phi_i, phidot_i, H_i; Lambda_0 = -Q_i; Q_i/V_i = 0.1; gamma = 0.1; N_f(UG) = 100) no cambian.

Qué es resultado y qué no:
  * P_T y n_T: RESULTADO (sector tensorial derivado; ecuación de modos = RG con el H(t) de cada modelo).
  * r_std, n_s_std, A_s_std: NO son resultados de UG. Usan la fórmula escalar ESTÁNDAR de RG (P_zeta0 = H^2/(8 pi^2 eps1),
    n_s = 1 - 2 eps1 - eps2) evaluada con el fondo de UG. El sector escalar de UG con difusión NO está derivado (O1/O2/O5).
    Se reportan solo como referencia condicional (valen si la UG se comporta como RG con un potencial efectivo, o si nada más
    cambia en el sector escalar).
"""
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

import background as B
from config import params_for
from modes import run_mode

OUT = Path(__file__).parent / "resultados"
N_STARS = (50.0, 60.0)
D_LNK = 0.25   # paso de la diferencia finita en ln k para n_T (igual que checks.py C1.3)


def _hubble_flow(bg, N):
    return float(np.exp(bg.lnH(N))), float(bg.eps1(N)), float(bg.eps1.derivative()(N) / bg.eps1(N))


def compare(potential):
    P = params_for(potential)
    P = replace(P, phi_i=B.phi_i_for_ug_duration(P))
    bgs = {"RG": B.solve_background_rg(P), "UG": B.solve_background_ug(P)}
    m2 = P.m_phys**2
    rows = []
    for Ns in N_STARS:
        for name, bg in bgs.items():
            N = bg.N_end - Ns
            k = float(np.exp(N + bg.lnH(N)))
            PT = run_mode(k, bg, P)["P_T"]
            lp = np.log(run_mode(k * np.exp(D_LNK), bg, P)["P_T"]) - np.log(run_mode(k * np.exp(-D_LNK), bg, P)["P_T"])
            H, e1, e2 = _hubble_flow(bg, N)
            Pz0 = H**2 / (8 * np.pi**2 * e1)
            rows.append(dict(potential=potential, model=name, N_star=Ns, N_end=bg.N_end, N_exit=N, H_exit_over_m=H, eps1=e1, eps2=e2,
                             P_T=PT * m2, n_T=lp / (2 * D_LNK), r_std=PT / Pz0, n_s_std=1 - 2 * e1 - e2, A_s_std=Pz0 * m2))
    return P, rows


def main():
    allrows, meta = [], {}
    for pot in ("quadratic", "starobinsky"):
        P, rows = compare(pot)
        allrows += rows
        meta[pot] = dict(phi_i=P.phi_i, m_phys=P.m_phys, Q_over_V_i=P.Q_over_V_i, gamma=P.gamma, N_f_ug=P.N_f_ug)
    # cocientes UG/RG
    for r in allrows:
        if r["model"] == "UG":
            rg = next(x for x in allrows if x["potential"] == r["potential"] and x["model"] == "RG" and x["N_star"] == r["N_star"])
            r["PT_UG_over_RG"], r["dnT_UG_minus_RG"] = r["P_T"] / rg["P_T"], r["n_T"] - rg["n_T"]
    OUT.mkdir(exist_ok=True)
    (OUT / "comparacion_N_star.json").write_text(json.dumps(dict(meta=meta, rows=allrows), indent=1, default=float))
    keys = ["potential", "model", "N_star", "N_end", "N_exit", "H_exit_over_m", "eps1", "eps2", "P_T", "n_T", "r_std", "n_s_std", "A_s_std",
            "PT_UG_over_RG", "dnT_UG_minus_RG"]
    lines = [",".join(keys)] + [",".join("" if r.get(k) is None else (str(r[k]) if isinstance(r[k], str) else f"{r[k]:.6e}") for k in keys)
                                for r in allrows]
    (OUT / "comparacion_N_star.csv").write_text("\n".join(lines) + "\n")
    print(f"{'potencial':11s} {'mod':3s} N*  N_exit   eps1      eps2     P_T        n_T       r_std     n_s_std  A_s_std   PT_UG/RG")
    for r in allrows:
        print(f"{r['potential']:11s} {r['model']:3s} {r['N_star']:3.0f} {r['N_exit']:7.1f} {r['eps1']:.3e} {r['eps2']:+.3e} {r['P_T']:.4e} "
              f"{r['n_T']:+.3e} {r['r_std']:.3e} {r['n_s_std']:.4f} {r['A_s_std']:.3e}  " + (f"{r['PT_UG_over_RG']:.4f}" if 'PT_UG_over_RG' in r else ""))


if __name__ == "__main__":
    main()
