"""Figuras de apoyo del informe (fig. 4: fondo; fig. 5: un modo a través del horizonte).

A diferencia de make_figures.py, ESTE script sí calcula (~3 s): resuelve los fondos de RG y UG con background.py y
integra un modo con modes.py, porque esas trayectorias no se guardan en resultados/. Usa los mismos parámetros que
run_spectrum.py (config.Params por defecto, con phi_i ajustado para que UG dure N_f = 100 e-folds) y el mismo estilo que
make_figures.py. Salidas en figuras/: fig4_fondo.{png,pdf,csv}, fig5_modo.{png,pdf,csv}, manifest_informe.json.
Uso:   python3 make_report_figures.py
"""
import hashlib
import json
import platform
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import background as B
import make_figures as MF
import modes as M
from config import Params

HERE = Path(__file__).parent
FIG = HERE / "figuras"
DEPS = ("config.py", "background.py", "modes.py", "make_figures.py")   # código que produce los datos de las figuras 4 y 5 (se recalculan aquí)
N_EXIT_DEMO = 40.0     # modo de la fig. 5: sale del horizonte 40 e-folds después del inicio (en RG)


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def context():
    P = Params()
    P = replace(P, phi_i=B.phi_i_for_ug_duration(P))
    return P, B.solve_background_rg(P), B.solve_background_ug(P)


def fig_fondo(P, rg, ug):
    """Fig. 4: H(N), eps1(N), phi(N) en RG y UG, y presupuesto de energía de UG (3H^2 = rho_phi + Q - Q_i)."""
    Q_i = ug.diag["Q_i"]
    Nr, Nu = np.linspace(0, rg.N_end, 3000), np.linspace(0, ug.N_end, 3000)
    Hr, Hu = np.exp(rg.lnH(Nr)), np.exp(ug.lnH(Nu))
    phid_u = Hu * ug.phi.derivative()(Nu)
    rho_u = 0.5 * phid_u**2 + B.V(ug.phi(Nu))
    Qu = B.Q_of_N(Nu, Q_i, P.gamma)

    fig, ax = plt.subplots(2, 2, figsize=(11.2, 8.0), constrained_layout=True)
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97))
    a = ax[0, 0]
    a.plot(Nr, Hr, color=MF.C_RG, lw=MF.LW, label="RG"); a.plot(Nu, Hu, color=MF.C_UG, lw=MF.LW, label="UG con Q(N)")
    MF._dot(a, Nr[-1], Hr[-1], MF.C_RG); MF._dot(a, Nu[-1], Hu[-1], MF.C_UG)
    a.set(xlabel="N = ln(a/a_i)", ylabel="H   [m]", title="(a) Parámetro de Hubble"); a.legend(loc="upper right")
    a = ax[0, 1]
    a.set_yscale("log")
    a.plot(Nr, rg.eps1(Nr), color=MF.C_RG, lw=MF.LW, label="RG"); a.plot(Nu, ug.eps1(Nu), color=MF.C_UG, lw=MF.LW, label="UG con Q(N)")
    a.axhline(1.0, color=MF.INK, lw=1.0); a.text(2, 1.15, "ε₁ = 1: fin de la inflación", fontsize=8.5, color=MF.INK2, va="bottom")
    MF._dot(a, Nr[-1], 1.0, MF.C_RG); MF._dot(a, Nu[-1], float(ug.eps1(Nu[-1])), MF.C_UG)
    a.set_ylim(2e-3, 3.0)
    a.set(xlabel="N", ylabel=r"$\epsilon_1=-\dot H/H^2$", title="(b) Primer parámetro de flujo"); a.legend(loc="lower right")
    a = ax[1, 0]
    a.plot(Nr, rg.phi(Nr), color=MF.C_RG, lw=MF.LW, label="RG"); a.plot(Nu, ug.phi(Nu), color=MF.C_UG, lw=MF.LW, label="UG con Q(N)")
    MF._dot(a, Nr[-1], float(rg.phi(Nr[-1])), MF.C_RG); MF._dot(a, Nu[-1], float(ug.phi(Nu[-1])), MF.C_UG)
    a.set(xlabel="N", ylabel=r"$\phi$   [$M_P$]", title="(c) Campo inflatón"); a.legend(loc="upper right")
    a = ax[1, 1]
    a.set_yscale("log")
    a.plot(Nu, rho_u, color=MF.INK, lw=MF.LW, label=r"$\rho_\phi$")
    a.plot(Nu, 3 * Hu**2, color=MF.C_UG, lw=MF.LW, label=r"$3H^2$ (lo que ve la expansión)")
    a.plot(Nu, Qu, color=MF.INK2, lw=MF.LW, ls=(0, (5, 3)), label=r"$Q(N)$")
    a.axhline(Q_i, color=MF.MUTED, lw=1.0); a.text(2, Q_i * 1.12, r"$|\Lambda_0| = Q_i$", fontsize=9, color=MF.INK2, va="bottom")
    a.set_ylim(1e-3, 6e2)
    a.set(xlabel="N", ylabel="densidad de energía   [$m^2M_P^2$]", title=r"(d) UG: $3H^2=\rho_\phi+Q(N)-Q_i$")
    a.legend(loc="lower left")
    fig.suptitle("Fondo cosmológico: mismas condiciones iniciales, distinta evolución", x=0.005, ha="left", fontsize=11.5, fontweight="bold")
    fig.text(0.006, 0.006, f"Datos: background.py::solve_background_rg/ug con config.Params por defecto (φ_i = {P.phi_i:.3f} M_P; Q_i/V_i = {P.Q_over_V_i:g}; γ = {P.gamma:g}). "
             "Tabla gemela: fig4_fondo.csv", fontsize=7.5, color=MF.INK2)
    rows = list(zip(Nu, Hu, ug.eps1(Nu), ug.phi(Nu), rho_u, 3 * Hu**2, Qu, Nr, Hr, rg.eps1(Nr), rg.phi(Nr)))
    MF._write_csv(FIG / "fig4_fondo.csv", ["N_UG", "H_UG", "eps1_UG", "phi_UG", "rho_phi_UG", "3H2_UG", "Q_UG", "N_RG", "H_RG", "eps1_RG", "phi_RG"], rows)
    return fig, FIG / "fig4_fondo"


def _mode_history(k, bg, P, n=6000):
    N_s = M._horizon_crossing_N(k / P.ratio_start, bg)
    N_f = M._horizon_crossing_N(k / P.ratio_stop, bg) or bg.N_end
    sol = solve_ivp(M.mode_rhs, (N_s, N_f), M.bunch_davies_ic(k, N_s, bg), method="DOP853", args=(k, bg),
                    rtol=P.rtol_mode, atol=P.atol_mode, dense_output=True)
    N = np.linspace(N_s, N_f, n)
    vt = sol.sol(N)[0]
    PT_t = 2 * k**2 * np.abs(vt) ** 2 / (np.pi**2 * np.exp(2 * N))      # P_T instantáneo (unidades m = 1)
    return N, vt, PT_t


def fig_modo(P, rg, ug):
    """Fig. 5: evolución de un modo a través del cruce del horizonte en RG y UG."""
    k = float(np.exp(N_EXIT_DEMO + rg.lnH(N_EXIT_DEMO)))
    fig, ax = plt.subplots(1, 2, figsize=(11.2, 4.4), constrained_layout=True)
    rows = []
    for bg, col, lab in ((rg, MF.C_RG, "RG"), (ug, MF.C_UG, "UG con Q(N)")):
        N, vt, PT_t = _mode_history(k, bg, P)
        Nx = M._horizon_crossing_N(k, bg)
        ax[0].semilogy(N, PT_t * P.m_phys**2, color=col, lw=MF.LW, label=lab)
        MF._dot(ax[0], N[-1], PT_t[-1] * P.m_phys**2, col)
        ax[0].axvline(Nx, color=MF.MUTED, lw=1.0)
        inside = N <= Nx + 0.5
        ax[1].plot(N[inside], vt.real[inside], color=col, lw=1.3, label=lab)
        ax[1].axvline(Nx, color=MF.MUTED, lw=1.0)
        rows += [[lab, n, p * P.m_phys**2, v.real] for n, p, v in zip(N, PT_t, vt)]
        print(f"  {lab}: cruce en N = {Nx:.3f}; P_T final = {PT_t[-1] * P.m_phys**2:.6e}")
    ax[0].text(0.98, 0.62, "líneas grises: cruce del horizonte\n(k = aH) en RG y en UG", transform=ax[0].transAxes, fontsize=8.5, color=MF.INK2, ha="right", va="top")
    ax[0].set(xlabel="N = ln(a/a_i)", ylabel=r"$P_T$ instantáneo del modo", title="(a) Se congela al salir del horizonte"); ax[0].legend(loc="upper right")
    ax[1].set(xlabel="N", ylabel=r"Re $\tilde v_k$", title="(b) Antes del cruce: oscilación de Bunch–Davies"); ax[1].legend(loc="lower right")
    fig.suptitle(f"Un modo con k = {k:.2e} m (sale del horizonte en N ≈ {N_EXIT_DEMO:g} en RG)", x=0.005, ha="left", fontsize=11.5, fontweight="bold")
    MF._write_csv(FIG / "fig5_modo.csv", ["modelo", "N", "P_T_instantaneo", "Re_vt"], rows)
    return fig, FIG / "fig5_modo"


def main():
    MF.apply_style()
    FIG.mkdir(exist_ok=True)
    P, rg, ug = context()
    manifest = dict(script=_sha(__file__), deps={f: _sha(HERE / f) for f in DEPS}, versions=dict(python=platform.python_version(), numpy=np.__version__, matplotlib=matplotlib_version()),
                    params=dict(phi_i=P.phi_i, Q_over_V_i=P.Q_over_V_i, gamma=P.gamma, N_f_ug=P.N_f_ug), figures={})
    for fn in (fig_fondo, fig_modo):
        fig, stem = fn(P, rg, ug)
        files = []
        for ext in ("png", "pdf"):
            p = Path(f"{stem}.{ext}")
            fig.savefig(p, dpi=200 if ext == "png" else None)
            files.append(p)
        plt.close(fig)
        files.append(Path(f"{stem}.csv"))
        manifest["figures"][fn.__name__] = {p.name: _sha(p) for p in files}
        print(f"{fn.__name__}: " + ", ".join(p.name for p in files))
    (FIG / "manifest_informe.json").write_text(json.dumps(manifest, indent=1))


def matplotlib_version():
    import matplotlib
    return matplotlib.__version__


if __name__ == "__main__":
    main()
