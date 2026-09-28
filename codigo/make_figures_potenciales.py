"""Figuras del segundo potencial (Starobinsky) y de la comparación a igual N* (informe, sec. 10).

  fig6_fondo_starobinsky : fondo de RG y UG para Starobinsky (H, eps1, phi, |Q'|/|V'|). CALCULA (~3 s, background.py).
  fig7_igual_k_potenciales: P_T(k) y cociente UG/RG a igual k, cuadrático y Starobinsky. Lee resultados/PT_k.csv y
                            resultados/starobinsky/PT_k.csv (run_spectrum.py).
  fig8_igual_Nstar       : cociente P_T^UG/P_T^RG, n_T y r_std a igual N*, ambos potenciales. Lee resultados/comparacion_N_star.csv
                            (compare_potentials.py) y el rango a igual k de fig7.
Salidas en figuras/: <nombre>.{png,pdf,csv} y manifest_potenciales.json (hashes de entradas, script y salidas).
Estilo y paleta: los de make_figures.py. Uso:   python3 make_figures_potenciales.py
"""
import csv
import hashlib
import json
import platform
from dataclasses import replace
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import background as B
import make_figures as MF
from config import params_for

HERE = Path(__file__).parent
FIG, RES = HERE / "figuras", HERE / "resultados"


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _read_pt_k(path):
    d = np.genfromtxt(path, delimiter=",", names=True)
    return d


def _read_nstar():
    with open(RES / "comparacion_N_star.csv") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k, v in r.items():
            if k not in ("potential", "model") and v != "":
                r[k] = float(v)
    return rows


# ------------------------------------------------------------------------------------------------ fig 6
def fig_fondo_starobinsky():
    P = params_for("starobinsky")
    P = replace(P, phi_i=B.phi_i_for_ug_duration(P))
    P_long = replace(P)                     # t_max ya viene de params_for
    rg, ug = B.solve_background_rg(P_long), B.solve_background_ug(P_long)
    Q_i, gam = ug.diag["Q_i"], P.gamma
    Nu, Nr = np.linspace(0, ug.N_end, 4000), np.linspace(0, rg.N_end, 4000)
    Hu, Hr = np.exp(ug.lnH(Nu)), np.exp(rg.lnH(Nr))
    dphidN = ug.phi.derivative()(Nu)
    Qp = (-gam * B.Q_of_N(Nu, Q_i, gam)) / dphidN                 # Q'(phi) = (dQ/dN)/(dphi/dN)
    ratio = np.abs(Qp) / np.abs(B.dV(ug.phi(Nu), "starobinsky"))
    N_piv = ug.N_end - 60.0

    fig, ax = plt.subplots(2, 2, figsize=(11.2, 8.0), constrained_layout=True)
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97))
    a = ax[0, 0]
    a.plot(Nr, Hr, color=MF.C_RG, lw=MF.LW, label="RG"); a.plot(Nu, Hu, color=MF.C_UG, lw=MF.LW, label="UG con Q(N)")
    MF._dot(a, Nu[-1], Hu[-1], MF.C_UG)
    a.set_xlim(0, 110); a.set(xlabel="N = ln(a/a_i)", ylabel="H   [M]", title="(a) Parámetro de Hubble"); a.legend(loc="center right")
    a.text(0.02, 0.05, f"RG dura {rg.N_end:.0f} e-folds (fuera del eje)", transform=a.transAxes, fontsize=8.5, color=MF.INK2)
    a = ax[0, 1]
    a.set_yscale("log")
    a.plot(Nr, rg.eps1(Nr), color=MF.C_RG, lw=MF.LW, label="RG"); a.plot(Nu, ug.eps1(Nu), color=MF.C_UG, lw=MF.LW, label="UG con Q(N)")
    a.axhline(1.0, color=MF.INK, lw=1.0)
    a.set_xlim(0, 110); a.set_ylim(1e-6, 3.0)
    a.set(xlabel="N", ylabel=r"$\epsilon_1=-\dot H/H^2$", title="(b) Primer parámetro de flujo"); a.legend(loc="lower right")
    a = ax[1, 0]
    a.plot(Nr, rg.phi(Nr), color=MF.C_RG, lw=MF.LW, label="RG"); a.plot(Nu, ug.phi(Nu), color=MF.C_UG, lw=MF.LW, label="UG con Q(N)")
    a.set_xlim(0, 110); a.set(xlabel="N", ylabel=r"$\phi$   [$M_P$]", title="(c) Campo inflatón"); a.legend(loc="upper right")
    a = ax[1, 1]
    a.set_yscale("log")
    m = Nu > 0.02
    a.plot(Nu[m], ratio[m], color=MF.C_UG, lw=MF.LW)
    a.axhline(1.0, color=MF.INK, lw=1.0); a.text(60, 1.15, r"$|Q'|=|V'|$", fontsize=9, color=MF.INK2)
    a.axvline(N_piv, color=MF.MUTED, lw=1.0)
    a.text(N_piv + 1, 2e-4, "pivote N* = 60\n(en UG)", fontsize=8.5, color=MF.INK2)
    a.set_xlim(0, 110); a.set_ylim(1e-4, 1e3)
    a.set(xlabel="N", ylabel=r"$|Q'(\phi)|\,/\,|V'(\phi)|$", title="(d) UG: cuánto empuja Q respecto del potencial")
    fig.suptitle("Starobinsky: mismas condiciones iniciales, RG dura mucho más que UG", x=0.005, ha="left", fontsize=11.5, fontweight="bold")
    fig.text(0.006, 0.006, f"Datos: background.py con params_for('starobinsky') (φ_i = {P.phi_i:.3f} M_P; Q_i/V_i = {P.Q_over_V_i:g}; γ = {P.gamma:g}). "
             "Tabla gemela: fig6_fondo_starobinsky.csv", fontsize=7.5, color=MF.INK2)
    rows = [[bg.model,n,float(np.exp(bg.lnH(n))),float(bg.eps1(n)),float(bg.phi(n)),float(ratio[i]) if bg.model=="UG" else 0.0]
            for bg,ns in ((ug,Nu),(rg,Nr)) for i,n in enumerate(ns)]
    MF._write_csv(FIG / "fig6_fondo_starobinsky.csv", ["model", "N", "H", "eps1", "phi", "abs_Qprime_over_abs_Vprime"], rows)
    return fig, FIG / "fig6_fondo_starobinsky", []



# ------------------------------------------------------------------------------------------------ fig 7
def fig_igual_k():
    fig, ax = plt.subplots(2, 2, figsize=(11.2, 7.2), constrained_layout=True, sharex="col")
    rows = []
    for j, (name, path) in enumerate((("Cuadrático", RES / "PT_k.csv"), ("Starobinsky", RES / "starobinsky" / "PT_k.csv"))):
        d = _read_pt_k(path)
        k = d["k"]
        ax[0, j].loglog(k, d["PT_RG"], color=MF.C_RG, lw=MF.LW, label="RG"); ax[0, j].loglog(k, d["PT_UG"], color=MF.C_UG, lw=MF.LW, label="UG con Q(N)")
        ax[0, j].set(ylabel=r"$P_T(k)$", title=f"({'ab'[j]}) {name}"); ax[0, j].legend(loc="best")
        ax[1, j].semilogx(k, d["ratio_UG_over_RG"], color=MF.INK, lw=MF.LW)
        ax[1, j].axhline(1.0, color=MF.MUTED, lw=1.0)
        ax[1, j].set(xlabel=r"$k$  [$m$ o $M$, $a_i=1$]", ylabel=r"$P_T^{UG}/P_T^{RG}$")
        rows += [[name, a, b, c, e] for a, b, c, e in zip(k, d["PT_RG"], d["PT_UG"], d["ratio_UG_over_RG"])]
    ax[1, 0].set_ylim(0, 1.1); ax[1, 1].set_ylim(0.75, 1.02)
    fig.suptitle("Comparación a igual k comóvil (mismas condiciones iniciales): mezcla épocas distintas", x=0.005, ha="left", fontsize=11.5, fontweight="bold")
    MF._write_csv(FIG / "fig7_igual_k_potenciales.csv", ["potencial", "k", "PT_RG", "PT_UG", "ratio"], rows)
    return fig, FIG / "fig7_igual_k_potenciales", [RES / "PT_k.csv", RES / "starobinsky" / "PT_k.csv"]


# ------------------------------------------------------------------------------------------------ fig 8
def fig_igual_Nstar():
    R = _read_nstar()
    pots = ("quadratic", "starobinsky")
    lab = {"quadratic": "Cuadrático", "starobinsky": "Starobinsky"}
    rng = {p: (lambda d: (d["ratio_UG_over_RG"].min(), d["ratio_UG_over_RG"].max()))(_read_pt_k(RES / ("PT_k.csv" if p == "quadratic" else "starobinsky/PT_k.csv")))
           for p in pots}
    fig, ax = plt.subplots(1, 3, figsize=(12.6, 4.6), constrained_layout=True)
    xs = {p: i for i, p in enumerate(pots)}
    a = ax[0]
    for p in pots:
        lo, hi = rng[p]
        a.plot([xs[p] - 0.18] * 2, [lo, hi], color=MF.MUTED, lw=6, solid_capstyle="butt", label="a igual k (rango)" if p == pots[0] else None)
        for Ns, mk, dx in ((50.0, "o", 0.06), (60.0, "s", 0.20)):
            r = next(x for x in R if x["potential"] == p and x["model"] == "UG" and x["N_star"] == Ns)
            a.plot([xs[p] + dx], [r["PT_UG_over_RG"]], mk, ms=9, mfc=MF.C_UG, mec=MF.SURFACE, mew=1.5, label=f"a igual N* = {Ns:g}" if p == pots[0] else None)
    a.axhline(1.0, color=MF.INK, lw=1.0)
    a.set_xticks(list(xs.values()), [lab[p] for p in pots]); a.set_xlim(-0.6, 1.6)
    a.set(ylabel=r"$P_T^{UG}/P_T^{RG}$", title="(a) Cociente de $P_T$ (UG/RG)"); a.legend(loc="upper right", fontsize=8)
    a = ax[1]
    for p in pots:
        for Ns, mk in ((50.0, "o"), (60.0, "s")):
            for mod, col in (("RG", MF.C_RG), ("UG", MF.C_UG)):
                r = next(x for x in R if x["potential"] == p and x["model"] == mod and x["N_star"] == Ns)
                a.plot([xs[p] + (0.12 if mod == "UG" else -0.12) + (0.05 if Ns == 60 else -0.05)], [-r["n_T"]], mk, ms=8, mfc=col, mec=MF.SURFACE, mew=1.5)
    a.set_xticks(list(xs.values()), [lab[p] for p in pots]); a.set_xlim(-0.6, 1.6); a.set_yscale("log")
    a.set(ylabel=r"$-n_T$", title="(b) Índice tensorial (azul RG, naranja UG)")
    a = ax[2]
    for p in pots:
        for Ns, mk in ((50.0, "o"), (60.0, "s")):
            for mod, col in (("RG", MF.C_RG), ("UG", MF.C_UG)):
                r = next(x for x in R if x["potential"] == p and x["model"] == mod and x["N_star"] == Ns)
                a.plot([xs[p] + (0.12 if mod == "UG" else -0.12) + (0.05 if Ns == 60 else -0.05)], [r["r_std"]], mk, ms=8,
                       mfc=col if mod == "RG" else "none", mec=col, mew=1.8)
    a.set_yscale("log"); a.set_xticks(list(xs.values()), [lab[p] for p in pots]); a.set_xlim(-0.6, 1.6)
    a.set(ylabel=r"$r_{\rm std}=P_T/P_\mathcal{R}^{\rm LO}$", title="(c) $r$ con $P_\\mathcal{R}$ estándar")
    a.text(0.5, 0.5, "UG (huecos): condicional;\nsector escalar sin derivar", transform=a.transAxes, fontsize=8, color=MF.INK2, ha="center")
    fig.suptitle("Comparación a igual número de e-folds antes del final (N* = 50: círculos; N* = 60: cuadrados)", x=0.005, ha="left", fontsize=11.5, fontweight="bold")
    keys = ["potential", "model", "N_star", "N_exit", "eps1", "eps2", "P_T", "n_T", "r_std", "n_s_std", "PT_UG_over_RG"]
    MF._write_csv(FIG / "fig8_igual_Nstar.csv", keys, [[r.get(k, "") for k in keys] for r in R])
    return fig, FIG / "fig8_igual_Nstar", [RES / "comparacion_N_star.csv", RES / "PT_k.csv", RES / "starobinsky" / "PT_k.csv"]


def main():
    MF.apply_style()
    FIG.mkdir(exist_ok=True)
    manifest = dict(script=_sha(__file__), deps={f:_sha(HERE/f) for f in ("background.py","config.py","make_figures.py")}, versions=dict(python=platform.python_version(), numpy=np.__version__, matplotlib=matplotlib.__version__), figures={})
    for fn in (fig_fondo_starobinsky, fig_igual_k, fig_igual_Nstar):
        fig, stem, inputs = fn()
        files = []
        for ext in ("png", "pdf"):
            p = Path(f"{stem}.{ext}")
            fig.savefig(p, dpi=200 if ext == "png" else None)
            files.append(p)
        plt.close(fig)
        files.append(Path(f"{stem}.csv"))
        manifest["figures"][fn.__name__] = dict(inputs={i.name if i.parent == RES else f"{i.parent.name}/{i.name}": _sha(i) for i in inputs},
                                                outputs={p.name: _sha(p) for p in files})
        print(f"{fn.__name__}: " + ", ".join(p.name for p in files))
    (FIG / "manifest_potenciales.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
