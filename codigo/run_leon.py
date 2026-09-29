"""Espectro tensorial con el modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329) (radiación + Q, sin inflatón) para los escenarios de A2/A1; escribe resultados/leon/.

Uso:  python3 run_leon.py        (~15 s)  ->  resultados/leon/comparacion.csv y comparacion.json

En este marco P_T depende solo de H(N), eps1(N) (como en RG), y la amplitud NO se calibra: la fija rho_end = 1e-11 M_P^4 (escenarios 1 y 3) o
rho_ini = M_P^4 (escenario 2). Por eso A_s es una predicción y se compara con Planck.

P_T, n_T: RESULTADOS del sector tensorial. Lo escalar NO está derivado: se reportan tres variantes de P_R, todas CONDICIONALES:
  A2  : P_R = H^2/(8 pi^2 eps1)               -> r_A2 = P_T/P_R  (A2 Eqs. 41-42; A2 da r = 16 eps1 sin derivarlo)
  A1  : P_R = 3^(3/2) H^2/(8 pi^2 eps1)       -> r_A1 = r_A2/3^(3/2)  (A1 Eq. 66 tal como está impresa; O1)
  cs  : P_R = H^2/(8 pi^2 eps1 c_s), c_s^2 = 1/3 -> r_cs = r_A2/sqrt(3)  (hipótesis O5 de PROVENANCE: NO verificada contra Garriga-Mukhanov)
"""
import csv
import json
from pathlib import Path

import numpy as np

import background_leon as L
from checks import A_S_PLANCK, eps2_at, k_at_exit
from checks_leon import N_F, GAMMA_STAR, P0, _rg_numeric_matched
from modes import run_mode

OUT = Path(__file__).parent / "resultados" / "leon"
D_LNK = 0.25
C3 = 3.0**1.5


def scenarios():
    yield "1: eps1=(1+Nf-N)^-g, g=2.02", L.reconstruct(L.eps1_power(N_F, GAMMA_STAR), N_F, norm="end"), (50.0, 57.0, 60.0), None
    yield "1: eps1=(1+Nf-N)^-g, g=1.5", L.reconstruct(L.eps1_power(N_F, 1.5), N_F, norm="end"), (50.0, 60.0), None
    # Escenario 2 (A1 Eq. 34, N_f = 371, alpha = 0.0229) NO se analiza: con N_f ~ 370 el slow-roll recién vale ~120 e-folds antes del final
    # (eps1 = 0.2-0.3 a 50-60 e-folds), no fijé el pivote de A2 y la integración independiente es imposible en doble precisión (CL1).
    for pot in ("starobinsky", "quadratic"):
        eps_fn, _ = L.eps1_slowroll_map(pot, N_F)
        yield f"3: mapeo slow-roll {pot}", L.reconstruct(eps_fn, N_F, norm="end"), (50.0, 60.0), pot


def main():
    rows = []
    for name, lb, pivots, pot in scenarios():
        bg = lb.bg
        rg_ref = _rg_numeric_matched(pot, lb) if pot else None
        for Ns in pivots:
            N = lb.N_end - Ns
            k = k_at_exit(bg, N)
            PT = run_mode(k, bg, P0)["P_T"]
            lp = np.log(run_mode(k * np.exp(D_LNK), bg, P0)["P_T"]) - np.log(run_mode(k * np.exp(-D_LNK), bg, P0)["P_T"])
            H, e1, e2 = float(np.exp(bg.lnH(N))), float(bg.eps1(N)), eps2_at(bg, N)
            PR_A2 = H**2 / (8 * np.pi**2 * e1)
            row = dict(scenario=name, N_f=lb.N_f, N_star=Ns, N_exit=N, H=H, eps1=e1, eps2=e2, P_T=PT, n_T=lp / (2 * D_LNK),
                       A_s_A2=PR_A2, A_s_A1=C3 * PR_A2, A_s_cs=np.sqrt(3.0) * PR_A2, ns_std=1 - 2 * e1 - e2,
                       r_A2=PT / PR_A2, r_A1=PT / PR_A2 / C3, r_cs=PT / PR_A2 / np.sqrt(3.0), r_16eps1=16 * e1)
            if rg_ref:
                P, rg, m = rg_ref
                row["P_T_RG_numeric"] = run_mode(k_at_exit(rg, rg.N_end - Ns), rg, P0)["P_T"] * m**2
                row["PT_RG_over_map"] = row["P_T_RG_numeric"] / PT
            rows.append(row)
    keys = ["scenario", "N_f", "N_star", "N_exit", "H", "eps1", "eps2", "P_T", "n_T", "A_s_A2", "A_s_A1", "A_s_cs", "ns_std", "r_A2", "r_A1",
            "r_cs", "r_16eps1", "P_T_RG_numeric", "PT_RG_over_map"]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "comparacion.json").write_text(json.dumps(dict(A_s_Planck=A_S_PLANCK, rows=rows), indent=1, default=float))
    with open(OUT / "comparacion.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(keys)
        for r in rows:
            w.writerow([r.get(k, "") if isinstance(r.get(k, ""), str) or r.get(k, "") == "" else f"{r[k]:.6e}" for k in keys])
    print(f"A_s Planck = {A_S_PLANCK:.3e}")
    print(f"{'escenario':36s} N*   eps1      eps2     P_T        n_T       A_s(A2)   A_s(A1)   A_s(cs)   r_A2      r_A1      r_cs    ns_std  PT_RG/map")
    for r in rows:
        print(f"{r['scenario']:36s} {r['N_star']:3.0f} {r['eps1']:.2e} {r['eps2']:+.3f} {r['P_T']:.3e} {r['n_T']:+.2e} {r['A_s_A2']:.2e} {r['A_s_A1']:.2e} "
              f"{r['A_s_cs']:.2e} {r['r_A2']:.2e} {r['r_A1']:.2e} {r['r_cs']:.2e} {r['ns_std']:.4f}  " + (f"{r['PT_RG_over_map']:.3f}" if 'PT_RG_over_map' in r else ""))


if __name__ == "__main__":
    main()
