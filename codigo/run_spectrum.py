"""Calcula P_T(k) en RG y en UG con difusión Q, para el potencial elegido (cuadrático por defecto; o Starobinsky).

Uso:  python run_spectrum.py [quadratic|starobinsky]   (parámetros por defecto de config.py)
Salidas: codigo/resultados/ (cuadrático) o codigo/resultados/starobinsky/: PT_k.npz, PT_k.csv, PT_k.png, fondo.png

No hace verificaciones: solo integra y guarda. Los checks son una etapa posterior.
"""
import time
from dataclasses import asdict, replace
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from background import phi_i_for_ug_duration, solve_background_rg, solve_background_ug
from config import Params, params_for
from modes import run_all_modes

OUT = Path(__file__).parent / "resultados"


def k_grid(bg_rg, bg_ug, P: Params):
    """Malla común de k (comóvil, unidades de m con a_i = 1), equiespaciada en ln k.

    k_min: margen para q inicial hasta 1000 dentro del fondo, incluso al refinar el vacío.
    k_max: margen para q final hasta 1e-4 dentro de ambos fondos, sin saturar la parada.
    [SUPUESTO] Se compara a igual k comóvil (mismo a_i, mismas condiciones iniciales); la relación entre k
    y "N e-folds antes del fin" es distinta en cada modelo (Sec. 9 de PROVENANCE.md)."""
    aH0 = np.exp(bg_rg.lnH(0.0))
    k_min = 1.01 * max(1000.0, P.ratio_start) * aH0
    aH_end = min(np.exp(bg.N_end + bg.lnH(bg.N_end)) for bg in (bg_rg, bg_ug))
    k_max = 0.99 * min(1e-4, P.ratio_stop) * aH_end
    if k_max <= k_min:
        raise ValueError("rango de k vacío: la inflación dura muy poco para ratio_start/ratio_stop")
    return np.geomspace(k_min, k_max, P.n_k)


def main(P: Params = Params()):
    t0 = time.time()
    outdir = OUT if P.potential == "quadratic" else OUT / P.potential   # el cuadrático conserva resultados/ (lo leen las figuras)
    outdir.mkdir(parents=True, exist_ok=True)

    if P.phi_i is None:
        P = replace(P, phi_i=phi_i_for_ug_duration(P))
        print(f"== phi_i = {P.phi_i:.6f} M_P (ajustado para que UG dure N_f = {P.N_f_ug:g} e-folds) ==")
    bg_rg = solve_background_rg(P)
    bg_ug = solve_background_ug(P)
    print("== Fondo (unidades M_P = 1, m = 1) ==")
    for bg in (bg_rg, bg_ug):
        d = bg.diag
        print(f"  {bg.model}: H_i={d['H_i']:.6g}  eps1_i={d['eps1_i']:.4g}  N_end={d['N_end']:.3f}  "
              f"max|X/H^2|={d['max_abs_X_over_H2']:.2e}  max|Hdot+phidot^2/2|={d['max_abs_Hdot_minus_28']:.2e}")
    print(f"  UG: Q_i={bg_ug.diag['Q_i']:.5g}  Lambda_0={bg_ug.diag['Lambda0']:.5g}")
    print("  (los dos últimos números son diagnósticos crudos, NO los checks formales)")

    ks = k_grid(bg_rg, bg_ug, P)
    print(f"== k: {P.n_k} modos, {ks[0]:.3e} .. {ks[-1]:.3e} (m, a_i=1), ln(kmax/kmin)={np.log(ks[-1]/ks[0]):.2f} ==")

    res = {}
    for bg in (bg_rg, bg_ug):
        t1 = time.time()
        out = run_all_modes(ks, bg, P)
        res[bg.model] = {key: np.array([o[key] for o in out]) for key in out[0]}
        print(f"  {bg.model}: {len(ks)} modos en {time.time()-t1:.1f} s "
              f"(nfev medio {np.mean(res[bg.model]['nfev']):.0f}; "
              f"paradas antes de tiempo: {int(np.sum(res[bg.model]['stopped_early']))})")

    m2 = P.m_phys**2  # P_T ~ H^2/M_P^2 -> escala con m^2
    PT_rg = res["RG"]["P_T"] * m2
    PT_ug = res["UG"]["P_T"] * m2

    np.savez(outdir / "PT_k.npz", k=ks, PT_RG=PT_rg, PT_UG=PT_ug,
             **{f"{m}_{key}": v for m, r in res.items() for key, v in r.items() if key not in ("k", "P_T")},
             params=str(asdict(P)))
    header = "k,PT_RG,PT_UG,ratio_UG_over_RG,N_exit_RG,N_exit_UG,H_exit_RG,H_exit_UG,eps1_exit_RG,eps1_exit_UG"
    table = np.column_stack([ks, PT_rg, PT_ug, PT_ug / PT_rg, res["RG"]["N_exit"], res["UG"]["N_exit"],
                             res["RG"]["H_exit"], res["UG"]["H_exit"], res["RG"]["eps1_exit"], res["UG"]["eps1_exit"]])
    np.savetxt(outdir / "PT_k.csv", table, delimiter=",", header=header, comments="")

    print("== P_T(k) (M_P=1, m_phys = %.1e) ==" % P.m_phys)
    print("   k [m, a_i=1]    N_exit_RG  N_exit_UG      P_T_RG        P_T_UG     UG/RG")
    for i in range(0, P.n_k, max(1, P.n_k // 10)):
        print(f"  {ks[i]:12.4e}   {res['RG']['N_exit'][i]:8.3f}  {res['UG']['N_exit'][i]:8.3f}   "
              f"{PT_rg[i]:.6e}  {PT_ug[i]:.6e}  {PT_ug[i]/PT_rg[i]:.6f}")

    # ---- figuras
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].loglog(ks, PT_rg, "o-", ms=3, label="RG")
    ax[0].loglog(ks, PT_ug, "s--", ms=3, label="UG con Q(N)")
    ax[0].set_xlabel(r"$k$  [$m$, $a_i=1$]"); ax[0].set_ylabel(r"$P_T(k)$"); ax[0].legend()
    ax[1].semilogx(ks, PT_ug / PT_rg, "k.-")
    ax[1].set_xlabel(r"$k$  [$m$, $a_i=1$]"); ax[1].set_ylabel(r"$P_T^{UG}/P_T^{RG}$")
    fig.tight_layout(); fig.savefig(outdir / "PT_k.png", dpi=130); plt.close(fig)

    N_grid = np.linspace(0, min(bg_rg.N_end, bg_ug.N_end), 400)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for bg, st in ((bg_rg, "-"), (bg_ug, "--")):
        ax[0].plot(N_grid, np.exp(bg.lnH(N_grid)), st, label=bg.model)
        ax[1].plot(N_grid, bg.eps1(N_grid), st, label=bg.model)
    ax[0].set_xlabel("N = ln(a/a_i)"); ax[0].set_ylabel("H  [m]"); ax[0].legend()
    ax[1].set_xlabel("N = ln(a/a_i)"); ax[1].set_ylabel(r"$\epsilon_1$"); ax[1].set_yscale("log"); ax[1].legend()
    fig.tight_layout(); fig.savefig(outdir / "fondo.png", dpi=130); plt.close(fig)

    print(f"listo en {time.time()-t0:.1f} s -> {outdir}")


if __name__ == "__main__":
    import sys
    main(params_for(sys.argv[1] if len(sys.argv) > 1 else "quadratic"))
