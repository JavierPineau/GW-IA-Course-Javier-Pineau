"""Fondo cosmológico con un inflatón: RG (derivation.md Sec. 2.5) y UG con difusión Q (Secs. 2.4-2.6).

Tiempo cósmico t (decisión ii de derivation.md). Estado y = (phi, phidot, N) con N = ln(a/a_i).
Unidades M_P = 1, m = 1 (ver config.py).

Diseño: RG y UG tienen funciones separadas (`quantities_rg`, `quantities_ug`); ninguna usa la
relación Hdot = -phidot^2/2 de (2.8). Hdot se obtiene derivando en el tiempo la ecuación de
Friedmann de cada modelo ((2.10) o (2.7)) y usando la ecuación del inflatón ((2.10) o (2.9)).
Así (2.8) queda como una consecuencia que se puede contrastar, no como una entrada.
"""
from dataclasses import dataclass, replace

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

from config import Params

LAMBDA_RG = 0.0  # [SUPUESTO] RG sin constante cosmológica: Lambda = 0 en (2.10)
C_STARO = np.sqrt(2.0 / 3.0)  # exponente del potencial de Starobinsky, V ~ (1 - exp(-sqrt(2/3) phi/M_P))^2
POTENTIALS = ("quadratic", "starobinsky")


# ----------------------------------------------------------------------------- potencial
def V(phi, potential="quadratic"):
    """Potencial del inflatón en unidades donde la escala de masa vale 1 (m para el cuadrático, M para Starobinsky).

    quadratic  : V = phi^2/2.                                   [SUPUESTO, decisión del usuario: potencial cuadrático]
    starobinsky: V = (3/4)(1 - exp(-sqrt(2/3) phi))^2.          [SUPUESTO, decisión del usuario 2026-09-21; forma
                 ESTÁNDAR del marco de Einstein de R + R^2/(6M^2) en RG, ver PROVENANCE sec. 13]. Aquí solo se usa la
                 forma del potencial; no se afirma que el origen R^2 valga en UG."""
    if potential == "quadratic":
        return 0.5 * phi**2
    if potential == "starobinsky":
        return 0.75 * (1.0 - np.exp(-C_STARO * phi)) ** 2
    raise ValueError(f"potencial desconocido: {potential!r} (usar {POTENTIALS})")


def dV(phi, potential="quadratic"):
    """V'(phi) del potencial elegido (misma normalización que V)."""
    if potential == "quadratic":
        return phi
    if potential == "starobinsky":
        e = np.exp(-C_STARO * phi)
        return 1.5 * C_STARO * (1.0 - e) * e
    raise ValueError(f"potencial desconocido: {potential!r} (usar {POTENTIALS})")


# ----------------------------------------------------------------------------- materia
def rho_and_p(phi, phid, potential="quadratic"):
    """Densidad y presión del inflatón homogéneo. Implementa derivation.md (2.5) [ESTÁNDAR]."""
    kin = 0.5 * phid**2
    pot = V(phi, potential)
    return kin + pot, kin - pot


# ----------------------------------------------------------------------------- difusión Q
def Q_of_N(N, Q_i, gamma):
    """Q(N) = Q_i exp(-gamma N). [SUPUESTO, decisión del usuario]. Entra en (1.9) y (2.7)."""
    return Q_i * np.exp(-gamma * N)


def Qdot(N, H, Q_i, gamma):
    """dQ/dt = (dQ/dN)(dN/dt) = -gamma Q H, con dN/dt = H. Es el Q-punto de (2.9)."""
    return -gamma * Q_of_N(N, Q_i, gamma) * H


# ----------------------------------------------------------------------------- Hubble
def hubble_rg(rho, Lam=LAMBDA_RG):
    """3 M_P^2 H^2 = rho (+ Lambda M_P^2). Implementa derivation.md (2.10), primera ecuación."""
    return np.sqrt((rho + Lam) / 3.0)


def hubble_ug(rho, Q, Lam0):
    """3 M_P^2 H^2 = rho + Q + Lambda_0 M_P^2. Implementa derivation.md (2.7)."""
    return np.sqrt((rho + Q + Lam0) / 3.0)


def lambda0_from_initial(H_ini, rho_ini, Q_ini):
    """Lambda_0 = 3 H_ini^2 - (rho_ini + Q_ini)/M_P^2. Implementa derivation.md (2.11)."""
    return 3.0 * H_ini**2 - (rho_ini + Q_ini)


# ----------------------------------------------------------------------------- término de masa
def tensor_mass_term(H, Hdot, p, lam_bar):
    """X = -3H^2 - 2 Hdot - kappa p + lambda_bar (kappa = 1).  Implementa derivation.md (4.6).

    Es el coeficiente que multiplica a (a^3 h_ij^2)/(4 kappa) en la acción cuadrática. En la
    ecuación de h entra como  hddot + 3H hdot + (k^2/a^2 - 2X) h = 0.  La derivación dice que
    X = 0 por ecuaciones de fondo relacionadas: es un control interno algebraico, no una prueba independiente de la teoría. Se calcula con las
    cantidades de fondo de cada modelo y lo pasa a la ecuación de modos.
    lam_bar = Lambda (RG) o Lambda_0 + kappa Q(t) (UG)."""
    return -3.0 * H**2 - 2.0 * Hdot - p + lam_bar


# ----------------------------------------------------------------------------- modelos
def quantities_rg(y, potential="quadratic"):
    """Cantidades de fondo en RG a partir de y = (phi, phidot, N).

    phidd: Klein-Gordon estándar, (2.10) tercera ecuación.
    Hdot : derivada temporal de (2.10) primera ecuación, 6 H Hdot = phidot (phiddot + V')."""
    phi, phid, N = y
    rho, p = rho_and_p(phi, phid, potential)
    H = hubble_rg(rho)
    phidd = -3.0 * H * phid - dV(phi, potential)
    Hdot = phid * (phidd + dV(phi, potential)) / (6.0 * H)
    return dict(H=H, phidd=phidd, Hdot=Hdot, p=p, lam_bar=LAMBDA_RG + 0.0 * H)


def quantities_ug(y, Q_i, gamma, Lam0, potential="quadratic"):
    """Cantidades de fondo en UG con difusión a partir de y = (phi, phidot, N).

    phidd: (2.9), Q se acopla solo al inflatón [decisión (a) del usuario].
    Hdot : derivada temporal de (2.7), 6 H Hdot = phidot (phiddot + V') + Qdot."""
    phi, phid, N = y
    rho, p = rho_and_p(phi, phid, potential)
    Q = Q_of_N(N, Q_i, gamma)
    H = hubble_ug(rho, Q, Lam0)
    Qd = Qdot(N, H, Q_i, gamma)
    phidd = -3.0 * H * phid - dV(phi, potential) - Qd / phid
    Hdot = (phid * (phidd + dV(phi, potential)) + Qd) / (6.0 * H)
    return dict(H=H, phidd=phidd, Hdot=Hdot, p=p, lam_bar=Lam0 + Q)


# ----------------------------------------------------------------------------- condiciones iniciales
def initial_state(P: Params):
    """(phi_i, phidot_i, N=0) y datos iniciales comunes a RG y UG.

    [SUPUESTO] phidot_i = -V'/(3 H_SR) con H_SR^2 = V/3 (slow-roll de (2.14) con Q=0, Lambda=0).
    Decisión del usuario: mismo phi_i, phidot_i y mismo H_i en ambos modelos; H_i es el de RG (2.10)."""
    if P.phi_i is None:
        raise ValueError("P.phi_i es None: usar phi_i_for_ug_duration() para fijarlo")
    phi_i = P.phi_i
    phid_i = -dV(phi_i, P.potential) / np.sqrt(3.0 * V(phi_i, P.potential))
    rho_i, _ = rho_and_p(phi_i, phid_i, P.potential)
    H_i = hubble_rg(rho_i)
    Q_i = P.Q_over_V_i * V(phi_i, P.potential)
    Lam0 = lambda0_from_initial(H_i, rho_i, Q_i)  # (2.11): con este H_i sale Lambda_0 = -Q_i
    return dict(y0=np.array([phi_i, phid_i, 0.0]), H_i=H_i, rho_i=rho_i, Q_i=Q_i, Lam0=Lam0)


# ----------------------------------------------------------------------------- integración
@dataclass
class Background:
    """Fondo como funciones de N = ln(a/a_i), listo para integrar los modos."""
    model: str
    N_end: float
    t_end: float
    lnH: CubicSpline
    eps1: CubicSpline
    X_over_H2: CubicSpline
    phi: CubicSpline
    diag: dict


def _solve(model, quantities, y0, P: Params):
    def rhs(t, y):
        q = quantities(y)
        return [y[1], q["phidd"], q["H"]]

    def end_of_inflation(t, y):
        q = quantities(y)
        return -q["Hdot"] / q["H"] ** 2 - 1.0  # eps1 - 1

    end_of_inflation.terminal = True
    end_of_inflation.direction = 1

    sol = solve_ivp(rhs, (0.0, P.t_max), y0, method="DOP853", rtol=P.rtol_bg, atol=P.atol_bg,
                    dense_output=True, events=end_of_inflation)
    if sol.t_events[0].size == 0:
        raise RuntimeError(f"[{model}] no se alcanzó eps1=1 antes de t_max={P.t_max}")
    t_end = float(sol.t_events[0][0])

    # Malla uniforme en t; N(t) no es uniforme y es la abscisa de los splines.
    t = np.linspace(0.0, t_end, P.n_grid_bg)
    Y = sol.sol(t)
    q = quantities(Y)
    X = tensor_mass_term(q["H"], q["Hdot"], q["p"], q["lam_bar"])
    N = Y[2]
    eps1 = -q["Hdot"] / q["H"] ** 2
    if not np.all(np.diff(N) > 0):
        raise RuntimeError(f"[{model}] N(t) no es monótono")
    diag = dict(
        H_i=float(q["H"][0]), eps1_i=float(eps1[0]), N_end=float(N[-1]),
        max_abs_X_over_H2=float(np.max(np.abs(X / q["H"] ** 2))),
        # cantidad que NO se usa en el código y sirve para contrastar (2.8) más adelante:
        max_abs_Hdot_minus_28=float(np.max(np.abs(q["Hdot"] + 0.5 * Y[1] ** 2))),
    )
    return Background(
        model=model, N_end=float(N[-1]), t_end=t_end,
        lnH=CubicSpline(N, np.log(q["H"])),
        eps1=CubicSpline(N, eps1),
        X_over_H2=CubicSpline(N, X / q["H"] ** 2),
        phi=CubicSpline(N, Y[0]),
        diag=diag,
    )


def solve_background_rg(P: Params):
    """Fondo de RG: integra (2.10)."""
    ini = initial_state(P)
    return _solve("RG", lambda y: quantities_rg(y, P.potential), ini["y0"], P)


def solve_background_ug(P: Params):
    """Fondo de UG con difusión: integra (2.9) con H de (2.7) y Q(N) dada."""
    ini = initial_state(P)
    Q_i, gamma, Lam0 = ini["Q_i"], P.gamma, ini["Lam0"]
    bg = _solve("UG", lambda y: quantities_ug(y, Q_i, gamma, Lam0, P.potential), ini["y0"], P)
    bg.diag.update(Q_i=Q_i, Lambda0=Lam0)
    return bg


def phi_i_for_ug_duration(P: Params, bracket=None):
    """phi_i tal que la inflación de UG (eps1 = 1) ocurre en N_end = P.N_f_ug e-folds.

    [SUPUESTO, decisión del usuario] Se fija la duración en UG (valor usual en la literatura de UG, ver config.py);
    RG usa el mismo phi_i y las mismas condiciones iniciales, por lo que dura más. Solo busca una raíz
    sobre solve_background_ug; no interviene ninguna ecuación nueva."""
    bracket = P.phi_bracket if bracket is None else bracket
    f = lambda phi: solve_background_ug(replace(P, phi_i=phi)).N_end - P.N_f_ug
    lo, hi = bracket
    if f(lo) * f(hi) > 0:
        raise ValueError(f"N_end(UG) - {P.N_f_ug} no cambia de signo en phi_i in {bracket}")
    return brentq(f, lo, hi, xtol=1e-10)
