"""Figuras del modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329) (informe, sec. 12).

  fig9_fondo_leon : escenario 1 de Piccirilli–León 2023 (A2) (gamma = 2.02, N_f = 100, rho_end = 1e-11): eps1(N), rho(N) y Q(N), H(N). CALCULA (background_leon.py).
  fig10_leon_PT_As: (a) P_T(k) con radiación + Q y con el inflatón de RG reconstruido (mismo H(N)); (b) A_s y r según la fórmula escalar usada.
                    CALCULA los modos (a) y LEE resultados/leon/comparacion.json (b).
Salidas en figuras/: <nombre>.{png,pdf,csv} y manifest_leon.json. Estilo de make_figures.py. Uso:   python3 make_figures_leon.py
"""
import hashlib
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import background_leon as L
import make_figures as MF
from checks import A_S_PLANCK, k_at_exit
from checks_leon import GAMMA_STAR, N_F, P0
from modes import run_mode

HERE = Path(__file__).parent
FIG, RES = HERE / "figuras", HERE / "resultados" / "leon"


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fig_fondo():
    lb15 = L.reconstruct(L.eps1_power(N_F, 1.5), N_F)
    lb = L.reconstruct(L.eps1_power(N_F, GAMMA_STAR), N_F)
    N = lb.bg.lnH.x
    fig, ax = plt.subplots(1, 3, figsize=(13.0, 4.4), constrained_layout=True)
    a = ax[0]; a.set_yscale("log")
    a.plot(N, lb.bg.eps1(N), color=MF.C_UG, lw=MF.LW, label=r"$\gamma=2.02$"); a.plot(N, lb15.bg.eps1(N), color=MF.C_RG, lw=MF.LW, label=r"$\gamma=1.5$")
    a.axhline(1.0, color=MF.INK, lw=1.0)
    a.set(xlabel="N = ln(a/a_i)", ylabel=r"$\epsilon_1=(1+N_f-N)^{-\gamma}$", title="(a) Primer parámetro de flujo (dato)"); a.legend(loc="lower right")
    a = ax[1]; a.set_yscale("log")
    a.plot(N, lb.Q(N), color=MF.C_UG, lw=MF.LW, label=r"$Q(N)$"); a.plot(N, lb.rho(N), color=MF.INK, lw=MF.LW, label=r"$\rho(N)$ (radiación)")
    a.text(2, 3e-11, r"$Q>\rho$ durante toda la inflación" "\n" r"$\Leftrightarrow\ \epsilon_1<1$", fontsize=8.5, color=MF.INK2)
    a.set(xlabel="N", ylabel=r"densidad   [$M_P^4$]", title=r"(b) $Q$ y $\rho$ reconstruidos ($\gamma=2.02$)"); a.legend(loc="center right")
    a = ax[2]; a.set_yscale("log")
    a.plot(N, np.exp(lb.bg.lnH(N)), color=MF.C_UG, lw=MF.LW, label=r"$\gamma=2.02$"); a.plot(N, np.exp(lb15.bg.lnH(N)), color=MF.C_RG, lw=MF.LW, label=r"$\gamma=1.5$")
    a.set(xlabel="N", ylabel=r"$H$   [$M_P$]", title=r"(c) $H(N)=H_{\rm end}\,e^{\int_N^{N_f}\epsilon_1}$"); a.legend(loc="upper right")
    fig.suptitle("Radiación con difusión Q: escenario 1, N_f = 100, ρ_end = 10⁻¹¹ M_P⁴\nReferencias: arXiv:2202.04029 y arXiv:2307.06329", x=0.005, ha="left", fontsize=11.5, fontweight="bold")
    MF._write_csv(FIG / "fig9_fondo_leon.csv", ["N", "eps1_g2.02", "H_g2.02", "rho_g2.02", "Q_g2.02", "eps1_g1.5", "H_g1.5", "rho_g1.5", "Q_g1.5"],
                  list(zip(N,lb.bg.eps1(N),lb.H(N),lb.rho(N),lb.Q(N),lb15.bg.eps1(N),lb15.H(N),lb15.rho(N),lb15.Q(N))))
    return fig, FIG / "fig9_fondo_leon", []


def fig_PT_As():
    lb = L.reconstruct(L.eps1_power(N_F, GAMMA_STAR), N_F)
    rg = L.rg_inflaton_with_same_H(lb)
    Nx = np.linspace(8.0, lb.N_end - 2.0, 30)
    ks = [k_at_exit(lb.bg, n) for n in Nx]
    ru = [run_mode(k, lb.bg, P0) for k in ks]
    rr_modes = [run_mode(k, rg, P0) for k in ks]
    pu = np.array([r["P_T"] for r in ru])
    pr = np.array([r["P_T"] for r in rr_modes])
    frozen = np.array([not (u["stopped_early"] or r["stopped_early"]) for u,r in zip(ru,rr_modes)])
    R = json.loads((RES / "comparacion.json").read_text())["rows"]
    r57 = next(r for r in R if r["scenario"].startswith("1") and "2.02" in r["scenario"] and r["N_star"] == 57.0)
    fig, ax = plt.subplots(1, 2, figsize=(11.6, 4.5), constrained_layout=True)
    a = ax[0]
    a.plot(Nx[frozen], pu[frozen], color=MF.C_UG, lw=MF.LW, label="radiación + Q")
    a.plot(Nx[frozen], pr[frozen], "o", ms=6, mfc="none", mec=MF.C_RG, mew=1.6, label="inflatón de RG con potencial reconstruido")
    a.plot(Nx[~frozen], pu[~frozen], "x", color=MF.INK2, label="evaluación al final: q > 0.001")
    a.set_yscale("log"); a.legend(loc="lower right")
    a.text(0.03, 0.75, f"máx |P_RG/P_UG − 1| = {np.max(np.abs(pr[frozen] / pu[frozen] - 1)):.1e}", transform=a.transAxes, fontsize=8.5, color=MF.INK2, va="bottom")
    a.set(xlabel="N en que el modo sale del horizonte", ylabel=r"$P_T$", title="(a) Mismo H(N), mismo espectro tensorial")
    a = ax[1]; a.set_yscale("log")
    vals = [("Piccirilli–León (2023):\n$H^2/8\\pi^2\\epsilon_1$", r57["A_s_A2"], r57["r_A2"], MF.C_UG), ("con $1/c_s$, $c_s=1/\\sqrt{3}$:\n$\\sqrt{3}\\,H^2/8\\pi^2\\epsilon_1$", r57["A_s_cs"], r57["r_cs"], MF.C_3),
            ("León (2022):\n$3^{3/2}H^2/8\\pi^2\\epsilon_1$", r57["A_s_A1"], r57["r_A1"], MF.C_RG)]
    for i, (lab, v, rr, col) in enumerate(vals):
        a.plot([i], [v], "o", ms=10, mfc=col, mec=MF.SURFACE, mew=1.5)
        a.text(i, v * 1.25, f"r = {rr:.1e}", ha="center", fontsize=8.5, color=MF.INK2)
    a.axhline(A_S_PLANCK, color=MF.INK, lw=1.0); a.text(2.35, A_S_PLANCK * 1.08, "Planck", fontsize=8.5, color=MF.INK2, ha="right")
    a.set_xticks(range(3), [v[0] for v in vals], fontsize=8.5); a.set_xlim(-0.5, 2.5); a.set_ylim(1e-9, 2e-8)
    a.set(ylabel=r"$A_s$ predicha", title="(b) $A_s$ y $r$ en el punto de referencia de Piccirilli–León\n" r"($\gamma=2.02$, $N_*=57$; condicional)")
    fig.suptitle("Espectros con radiación y difusión Q; sector escalar condicional\nReferencias: arXiv:2202.04029 y arXiv:2307.06329", x=0.005, ha="left", fontsize=11.5, fontweight="bold")
    MF._write_csv(FIG / "fig10_leon_PT_As.csv", ["N_exit", "P_T_UGrad", "P_T_RGrec", "stopped_early_UGrad", "ratio_final_UGrad", "stopped_early_RGrec", "ratio_final_RGrec"],
                  [[n,u["P_T"],r["P_T"],u["stopped_early"],u["ratio_final"],r["stopped_early"],r["ratio_final"]] for n,u,r in zip(Nx,ru,rr_modes)])
    MF._write_csv(FIG / "fig10_leon_scalars.csv", ["formula", "A_s", "r", "A_s_Planck", "N_star", "gamma"],
                  [[label,value,r,A_S_PLANCK,57.0,GAMMA_STAR] for label,value,r,color in vals])
    return fig, FIG / "fig10_leon_PT_As", [RES / "comparacion.json"]


def main():
    MF.apply_style()
    FIG.mkdir(exist_ok=True)
    manifest = dict(script=_sha(__file__), deps={f:_sha(HERE/f) for f in ("background.py","background_leon.py","modes.py","config.py","checks.py","checks_leon.py","make_figures.py")}, versions=dict(python=platform.python_version(), numpy=np.__version__, matplotlib=matplotlib.__version__), figures={})
    for fn in (fig_fondo, fig_PT_As):
        fig, stem, inputs = fn()
        files = []
        for ext in ("png", "pdf"):
            p = Path(f"{stem}.{ext}")
            fig.savefig(p, dpi=200 if ext == "png" else None)
            files.append(p)
        plt.close(fig)
        files.append(Path(f"{stem}.csv"))
        if fn == fig_PT_As: files.append(FIG / "fig10_leon_scalars.csv")
        manifest["figures"][fn.__name__] = dict(inputs={f"leon/{i.name}": _sha(i) for i in inputs}, outputs={p.name: _sha(p) for p in files})
        print(f"{fn.__name__}: " + ", ".join(p.name for p in files))
    (FIG / "manifest_leon.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
