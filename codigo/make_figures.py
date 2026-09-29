"""Figuras del resultado: P_T(k) en RG y UG, convergencia numérica y límite estándar.

Lee SOLO outputs ya guardados (no recalcula nada, no importa background/modes/checks):
    resultados/PT_k.npz      <- run_spectrum.py::main
    resultados/checks.json   <- checks.py::run_all
Escribe en figuras/:  <nombre>.png, <nombre>.pdf, <nombre>.csv (tabla gemela con los mismos datos) y manifest.json
(hashes sha256 de entradas, script y salidas). Uso:   python3 make_figures.py [--outdir figuras]

Estilo según la guía de dataviz: paleta categórica validada (azul, naranja, aguamarina; ver PROVENANCE.md sec. 11),
líneas de 2 px, leyenda siempre presente para >= 2 series, texto en tinta neutra (nunca del color de la serie),
grilla en hairline sólida, un solo eje de valores (el eje superior de la fig. 1 reetiqueta el MISMO k en e-folds),
etiquetas directas selectivas y tabla gemela. Solo modo claro (figuras para papel/PDF).
"""
import argparse
import ast
import csv
import hashlib
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = Path(__file__).parent
DATA = HERE / "resultados"

# --- tokens de estilo (guía dataviz, modo claro) -------------------------------------------------
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#85837c"
AXIS, GRID = "#d6d5d0", "#e8e7e3"
C_RG, C_UG, C_3 = "#2a78d6", "#eb6834", "#1baf7a"     # categóricos 1-3 (validados; PROVENANCE 11.1)
LW = 1.9                                               # ~2 px a la resolución de trabajo
CAUTION_EPS1 = 0.02                                    # elección de presentación: banda "UG con eps1 > 0.02 en el cruce"


def apply_style():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.labelcolor": INK, "axes.titlecolor": INK,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "grid.linestyle": "-", "axes.axisbelow": True,
        "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
        "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "legend.frameon": False, "legend.fontsize": 9, "pdf.fonttype": 42, "svg.fonttype": "none",
    })


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _dot(ax, x, y, color, ms=8):
    """Marcador de fin de línea (>= 8 px) con anillo del color de la superficie."""
    ax.plot([x], [y], "o", ms=ms, mfc=color, mec=SURFACE, mew=2, zorder=6, clip_on=False)


def _write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def _sci(v):
    """Etiqueta de eje en notación científica con mathtext."""
    e = int(np.floor(np.log10(v) + 1e-12))
    m = v / 10.0**e
    return rf"$10^{{{e}}}$" if abs(m - 1) < 1e-9 else rf"${m:g}\times10^{{{e}}}$"


def _mass_label(m):
    mant, exp = f"{m:.0e}".split("e")
    return rf"{mant}\times10^{{{int(exp)}}}"


# ------------------------------------------------------------------------------------------ entradas
def load_outputs():
    """Carga los outputs guardados y comprueba que provengan de la misma corrida (mismo phi_i)."""
    npz, jsn = DATA / "PT_k.npz", DATA / "checks.json"
    for p in (npz, jsn):
        if not p.exists():
            raise FileNotFoundError(f"falta {p}: correr run_spectrum.py y checks.py (o `python3 checks.py`)")
    d = np.load(npz)
    params = ast.literal_eval(str(d["params"]))
    chk = json.loads(jsn.read_text())
    if abs(params["phi_i"] - chk["meta"]["phi_i"]) > 1e-9 * abs(params["phi_i"]):
        raise ValueError("PT_k.npz y checks.json son de corridas distintas (phi_i difiere); volver a generar ambos")
    R = {c["id"]: c for c in chk["checks"]}
    if not all(c["passed"] for c in chk["checks"]):
        print("AVISO: hay checks que no pasan en checks.json; las figuras se generan igual, pero no están respaldadas")
    return dict(k=d["k"], PT_RG=d["PT_RG"], PT_UG=d["PT_UG"], N_exit_RG=d["RG_N_exit"], N_exit_UG=d["UG_N_exit"],
                eps1_exit_UG=d["UG_eps1_exit"], params=params, meta=chk["meta"], checks=R, inputs=[npz, jsn])


# ------------------------------------------------------------------------------------------ figura 1
def fig_pt_comparison(D, outdir):
    """Fig. 1: P_T(k) en RG y UG (arriba) y cociente UG/RG con la diferencia resaltada (abajo).
    Datos: PT_k.npz (40 modos) y, para los marcadores huecos, checks.json::C3.4 (9 modos)."""
    k, PTr, PTu = D["k"], D["PT_RG"], D["PT_UG"]
    ratio = PTu / PTr
    lnk, N_rg = np.log(k), D["N_exit_RG"]
    P, meta = D["params"], D["meta"]
    att = D["checks"]["C3.4"]["details"]["attribution"]
    k_c = k[np.argmax(D["eps1_exit_UG"] > CAUTION_EPS1)]           # primer k con eps1_UG > 0.02 en el cruce
    xlim = (k[0] / 4, k[-1] * 3e5)

    fig = plt.figure(figsize=(10.8, 8.0), constrained_layout=True)
    fig.get_layout_engine().set(rect=(0, 0.025, 1, 0.975))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 2])
    ax1, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1], sharex=None)

    # ---- panel superior: P_T(k)
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.plot(k, PTr, color=C_RG, lw=LW, label="RG", zorder=4)
    ax1.plot(k, PTu, color=C_UG, lw=LW, label="UG con difusión Q(N)", zorder=4)
    ax1.fill_between(k, PTu, PTr, color=C_UG, alpha=0.10, lw=0, label="diferencia UG − RG")
    ax1.axvspan(k_c, xlim[1], color=GRID, alpha=0.55, lw=0, zorder=0)
    _dot(ax1, k[-1], PTr[-1], C_RG); _dot(ax1, k[-1], PTu[-1], C_UG)
    ax1.text(k[-1] * 4, PTr[-1], "RG", va="center", color=INK, fontsize=10, fontweight="bold")
    ax1.text(k[-1] * 4, PTu[-1], "UG", va="center", color=INK, fontsize=10, fontweight="bold")
    ax1.set_xlim(*xlim); ax1.set_ylim(7e-11, 1.05e-9)
    ax1.set_xticks([10.0 ** e for e in range(5, 41, 5)])
    yt = [1e-10, 2e-10, 3e-10, 5e-10, 7e-10, 1e-9]
    ax1.set_yticks(yt); ax1.set_yticklabels([_sci(v) for v in yt]); ax1.minorticks_off()
    ax1.set_ylabel(r"$P_T(k)$   (varianza de $h_{ij}h_{ij}$ por $\ln k$)")
    ax1.set_title("Espectro tensorial primordial: RG vs. gravedad unimodular con difusión Q", pad=34)
    ax1.legend(loc="upper right", bbox_to_anchor=(0.92, 1.0))
    info = (f"$V=\\frac{{1}}{{2}}m^2\\phi^2$,  $m={_mass_label(P['m_phys'])}\\,M_P$\n"
            f"$Q(N)=Q_i\\,e^{{-\\gamma N}}$,  $Q_i/V_i={P['Q_over_V_i']:g}$,  $\\gamma={P['gamma']:g}$\n"
            f"mismas condiciones iniciales ($\\phi_i={P['phi_i']:.3f}\\,M_P$)\n"
            f"inflación: RG {meta['N_end_RG']:.1f} · UG {meta['N_end_UG']:.1f} e-folds")
    ax1.text(0.015, 0.05, info, transform=ax1.transAxes, fontsize=9, color=INK2, va="bottom")
    # eje superior: el MISMO k, reetiquetado en e-folds desde el inicio hasta el cruce del horizonte (en RG)
    Nt = np.arange(10, int(np.floor(N_rg.max())) + 1, 10)
    axt = ax1.twiny()
    axt.set_xscale("log"); axt.set_xlim(*xlim)
    axt.set_xticks(np.exp(np.interp(Nt, N_rg, lnk))); axt.set_xticklabels([str(n) for n in Nt]); axt.minorticks_off()
    axt.grid(False); axt.tick_params(colors=INK2)
    axt.set_xlabel("N_exit (RG): e-folds desde el inicio hasta que el modo sale del horizonte", color=INK2, fontsize=9)
    for s in axt.spines.values():
        s.set_color(AXIS)

    # ---- panel inferior: cociente
    ax2.set_xscale("log")
    ax2.axhline(1.0, color=MUTED, lw=1.0)
    ax2.plot(k, ratio, color=INK, lw=LW, zorder=4, label="numérico, 40 modos")
    ax2.fill_between(k, ratio, 1.0, color=C_UG, alpha=0.10, lw=0)
    ax2.axvspan(k_c, xlim[1], color=GRID, alpha=0.55, lw=0, zorder=0)
    kk = np.exp(np.interp([r["N_exit_RG"] for r in att], N_rg, lnk))   # N_exit -> k por interpolación en ln k (los 40 modos)
    ax2.plot(kk, [r["ratio_slowroll_NNLO"] for r in att], "D", ms=8, mfc=SURFACE, mec=INK, mew=1.5, ls="none", zorder=5,
             label="fórmula slow-roll NNLO de RG con el $H(t)$, $\\epsilon_i$ de UG\n(9 modos, check C3.4)")
    ax2.text(k[0] * 1.0, ratio[0] - 0.065, f"{ratio[0]:.2f}", va="top", ha="left", fontsize=10, color=INK, fontweight="bold")
    ax2.text(k[-1] * 12, ratio[-1], f"{ratio[-1]:.2f}", va="center", ha="left", fontsize=10, color=INK, fontweight="bold")
    _dot(ax2, k[-1], ratio[-1], INK)
    ax2.text(k[0] * 1.5, 1.025, "= RG", fontsize=8.5, color=INK2, va="bottom")
    ax2.text(k_c * 2, 0.80, f"UG con $\\epsilon_1>{CAUTION_EPS1:g}$\nen el cruce:\nslow-roll\nse degrada", fontsize=8.5, color=INK2, va="top")
    ax2.set_xlim(*xlim); ax2.set_ylim(0.16, 1.08)
    ax2.set_xticks([10.0 ** e for e in range(5, 41, 5)])
    ax2.set_xlabel("k   [en unidades de m, con a_i = 1]   (mismo k comóvil en ambos modelos)")
    ax2.set_ylabel(r"$P_T^{UG}\,/\,P_T^{RG}$")
    ax2.legend(loc="lower left", fontsize=8.5)
    fig.text(0.012, 0.004, "Fuente: resultados/PT_k.npz (run_spectrum.py) y checks.json::C3.4 (checks.py); incertidumbre numérica del cociente ≲ 1e-6 "
             "(C3.4). Tabla gemela: fig1_PT_k_RG_vs_UG.csv", fontsize=7.5, color=INK2)

    stem = outdir / "fig1_PT_k_RG_vs_UG"
    _write_csv(str(stem) + ".csv", ["k", "N_exit_RG", "N_exit_UG", "PT_RG", "PT_UG", "ratio_UG_over_RG", "eps1_exit_UG"],
               zip(k, N_rg, D["N_exit_UG"], PTr, PTu, ratio, D["eps1_exit_UG"]))
    return fig, stem


# ------------------------------------------------------------------------------------------ figura 2
CONV_TITLES = {
    "rtol_mode": "tolerancia relativa\ndel integrador de modos", "rtol_bg": "tolerancia relativa\ndel integrador del fondo",
    "n_grid_bg": "puntos de la malla en N\n(splines del fondo)", "ratio_start": "arranque: k/(aH) inicial\n(dentro del horizonte)",
    "ratio_stop": "medición: k/(aH) final\n(fuera del horizonte)",
}


def fig_convergence(D, outdir):
    """Fig. 2: convergencia numérica (check C2). Un parámetro por vez frente a un valor 'verdad' más fino; 4 modos, RG y UG."""
    det = D["checks"]["C2"]["details"]
    names = [n for n in det if not n.startswith("_")]
    all_ok = all(det[n]["default_ok"] for n in names)
    fig, axes = plt.subplots(1, len(names), figsize=(15.5, 4.1), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(rect=(0, 0.06, 1, 0.94))
    rows = []
    for ax, nme in zip(axes, names):
        v = det[nme]
        xs = np.array([float(x) for x in v["max_rel_err_by_value"]]); ys = np.maximum(np.array(list(v["max_rel_err_by_value"].values())), 1e-15)
        inverted = nme in ("rtol_mode", "rtol_bg")           # tolerancias: más fino hacia la derecha
        vis = np.argsort(xs)[::-1] if inverted else np.argsort(xs)
        xs, ys = xs[vis], ys[vis]                            # de izquierda a derecha en pantalla
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.plot(xs, ys, "-o", color=C_RG, lw=LW, ms=7, mec=SURFACE, mew=1.5, zorder=4)
        ax.axhline(v["tol"], color=INK, lw=1.0, zorder=3)
        if inverted:
            ax.invert_xaxis()
        ys_vis = ys
        left_far = abs(np.log10(ys_vis[0] / v["tol"])) >= abs(np.log10(ys_vis[-1] / v["tol"]))
        edge_y = ys_vis[0] if left_far else ys_vis[-1]
        below = edge_y > v["tol"]                            # la curva pasa por encima de la línea de ese lado -> rotular debajo
        ax.text(0.03 if left_far else 0.97, v["tol"] / 1.3 if below else v["tol"] * 1.3, "tolerancia", transform=ax.get_yaxis_transform(),
                fontsize=8.5, color=INK2, ha="left" if left_far else "right", va="top" if below else "bottom")
        i_def = int(np.argmin(np.abs(np.log(xs / v["default"]))))
        ax.plot([xs[i_def]], [ys[i_def]], "o", ms=13, mfc="none", mec=INK, mew=1.4, zorder=5)
        pos = i_def                                          # posición en pantalla
        dy = 34 if ys[i_def] < 1e-11 else -34
        dx, ha = (32, "left") if pos == 0 else ((-32, "right") if pos == len(xs) - 1 else (0, "center"))
        ax.annotate(f"defecto\n{ys[i_def]:.1e}", (xs[i_def], ys[i_def]), xytext=(dx, dy), textcoords="offset points", ha=ha,
                    va="bottom" if dy > 0 else "top", fontsize=8.5, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
        ax.set_title(CONV_TITLES.get(nme, nme), fontsize=9.5, pad=6)
        ax.set_xlabel(nme, fontsize=8.5, color=INK2)
        ax.set_ylim(1e-13, 3e-4)
        for x, y in zip(xs, ys):
            rows.append([nme, x, y, v["tol"], bool(abs(x - v["default"]) < 1e-12 * abs(v["default"])), v["truth"]])
    axes[0].set_ylabel(r"máx $|P_T/P_{T,\mathrm{verdad}}-1|$   (4 modos, RG y UG)")
    n_ok = sum(det[n]["default_ok"] for n in names)
    fig.suptitle("Convergencia numérica de P_T: el valor por defecto está dentro de la tolerancia en "
                 + ("los cinco parámetros" if all_ok else f"solo {n_ok} de {len(names)} parámetros"),
                 x=0.005, ha="left", fontsize=11.5, fontweight="bold")
    e_start, e_stop = det["ratio_start"]["max_rel_err_by_value"]["100.0"], det["ratio_stop"]["max_rel_err_by_value"]["0.001"]
    fig.text(0.006, 0.012, f"Fuente: resultados/checks.json::C2. El error dominante viene del arranque (≈ (aH/k)³: {e_start:.1e}) y de la medición (≈ (k/aH)²: {e_stop:.1e}). "
             "Tabla gemela: fig2_convergencia.csv", fontsize=7.5, color=INK2)
    stem = outdir / "fig2_convergencia"
    _write_csv(str(stem) + ".csv", ["parametro", "valor", "max_error_relativo", "tolerancia", "es_valor_por_defecto", "valor_verdad"], rows)
    return fig, stem


# ------------------------------------------------------------------------------------------ figura 3
def fig_standard_limit(D, outdir):
    """Fig. 3: (A) RG frente al desarrollo slow-roll estándar (check C1.2); (B) la diferencia UG/RG explicada por el fondo (check C3.4)."""
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.6, 4.9), constrained_layout=True)
    fig.get_layout_engine().set(rect=(0, 0.055, 1, 0.945))
    # ---- A: C1.2
    dA = D["checks"]["C1.2"]["details"]
    eps = np.array([r["eps1"] for r in dA])
    series = (("LO", "resid_LO", C_RG, "o", "-"), ("NLO", "resid_NLO", C_UG, "s", "-"), ("NNLO", "resid_NNLO", C_3, "^", "-"))
    axA.set_xscale("log"); axA.set_yscale("log")
    for lab, key, col, mk, ls in series:
        y = np.maximum(np.abs([r[key] for r in dA]), 1e-9)
        axA.plot(eps, y, ls, color=col, lw=LW, marker=mk, ms=8, mec=SURFACE, mew=1.5, label=lab, zorder=4)
        axA.text(eps[-1] * 1.07, y[-1], lab, fontsize=9, color=INK, va="center")
    axA.plot(eps, [r["tol_NNLO"] for r in dA], color=INK, lw=1.2, ls=(0, (5, 3)), zorder=3)
    axA.text(eps[-1] * 1.07, dA[-1]["tol_NNLO"] * 0.62, "tolerancia\nNNLO", fontsize=8.5, color=INK2, va="top")
    for p in (1, 2, 3):
        axA.plot(eps, eps**p, "-", color=MUTED, lw=0.8, zorder=2)
        axA.text(eps[0] * 0.93, eps[0] ** p, rf"$\epsilon_1^{{{p}}}$", fontsize=8.5, color=INK2, ha="right", va="center")
    axA.set_xlim(eps[0] * 0.7, eps[-1] * 1.9)
    xt = [3e-3, 5e-3, 1e-2, 2e-2]
    axA.set_xticks(xt); axA.set_xticklabels([_sci(v) for v in xt]); axA.minorticks_off()
    axA.set_xlabel(r"$\epsilon_1$ en el cruce del horizonte"); axA.set_ylabel(r"$|P_T\,/\,(2H^2/\pi^2\,a_0)-1|$")
    order_ok = all(abs(r["resid_NNLO"]) < abs(r["resid_NLO"]) < abs(r["resid_LO"]) for r in dA)
    axA.set_title("A. RG con φ²: cada orden slow-roll reduce el residuo" if order_ok else "A. RG con φ² frente al desarrollo slow-roll", fontsize=10.5)
    axA.legend(loc="lower right", title="orden de $a_0^{(T)}$", title_fontsize=8.5)
    # ---- B: C3.4
    dB = D["checks"]["C3.4"]["details"]
    att = dB["attribution"]
    N = np.array([r["N_exit_RG"] for r in att]); dev = np.maximum(np.abs([r["dev"] for r in att]), 1e-9)
    tol = np.array([r["tol"] for r in att]); judged = np.array([r["judged"] for r in att])
    axB.set_yscale("log")
    axB.plot(N[judged], dev[judged], "-o", color=INK, lw=LW, ms=8, mec=SURFACE, mew=1.5, zorder=4, label="modos juzgados (ε₂ ≤ 0.05)")
    axB.plot(N[~judged], dev[~judged], "D", ms=8, mfc=SURFACE, mec=INK, mew=1.5, ls="none", zorder=5, label="no juzgado a priori (ε₂ de UG = %.2f)" % att[-1]["eps2_UG"])
    axB.plot(N, tol, "-", color=MUTED, lw=1.0, zorder=3, label="tolerancia fijada a priori")
    axB.set_xlabel("N_exit (RG): e-folds hasta el cruce del horizonte"); axB.set_ylabel("|cociente UG/RG numérico  /  cociente slow-roll  − 1|")
    axB.set_title("B. UG/RG numérico vs. slow-roll con el fondo de UG", fontsize=10.5)
    axB.legend(loc="upper left", fontsize=8.5)
    fig.text(0.006, 0.012, "Fuente: resultados/checks.json::C1.2 y ::C3.4. Slow-roll: Martin, Ringeval y Vennin (2013), Eqs. (2.19), (2.23). "
             "Tablas gemelas: fig3a_*.csv, fig3b_*.csv", fontsize=7.5, color=INK2)
    stem = outdir / "fig3_limite_estandar"
    _write_csv(str(outdir / "fig3a_C1_2_slow_roll.csv"), ["N_exit", "eps1", "eps2", "resid_LO", "resid_NLO", "resid_NNLO", "tol_NNLO"],
               [[r["N_exit"], r["eps1"], r["eps2"], r["resid_LO"], r["resid_NLO"], r["resid_NNLO"], r["tol_NNLO"]] for r in dA])
    _write_csv(str(outdir / "fig3b_C3_4_atribucion.csv"), ["N_exit_RG", "ratio_numerico", "ratio_slowroll_NNLO", "dev_relativa", "tol", "juzgado", "eps1_RG", "eps1_UG", "eps2_UG"],
               [[r["N_exit_RG"], r["ratio_numeric"], r["ratio_slowroll_NNLO"], r["dev"], r["tol"], r["judged"], r["eps1_RG"], r["eps1_UG"], r["eps2_UG"]] for r in att])
    return fig, stem


FIGURES = [fig_pt_comparison, fig_convergence, fig_standard_limit]
CSV_OUTPUTS = {
    "fig_pt_comparison": ("fig1_PT_k_RG_vs_UG.csv",),
    "fig_convergence": ("fig2_convergencia.csv",),
    "fig_standard_limit": ("fig3a_C1_2_slow_roll.csv", "fig3b_C3_4_atribucion.csv"),
}


def main(outdir=HERE / "figuras"):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    apply_style()
    D = load_outputs()
    manifest = dict(script=dict(path="make_figures.py", sha256=_sha(__file__)), inputs={p.name: _sha(p) for p in D["inputs"]},
                    versions=dict(python=platform.python_version(), numpy=np.__version__, matplotlib=matplotlib.__version__),
                    figures={})
    for fn in FIGURES:
        fig, stem = fn(D, outdir)
        files = []
        for ext in ("png", "pdf"):
            p = Path(f"{stem}.{ext}")
            fig.savefig(p, dpi=200 if ext == "png" else None)
            files.append(p)
        plt.close(fig)
        files += [outdir / name for name in CSV_OUTPUTS[fn.__name__]]
        manifest["figures"][fn.__name__] = {p.name: _sha(p) for p in files}
        print(f"{fn.__name__}: " + ", ".join(p.name for p in files))
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=1))
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--outdir", default=str(HERE / "figuras"))
    main(ap.parse_args().outdir)
