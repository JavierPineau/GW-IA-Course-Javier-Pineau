"""Modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329) (radiación pura + difusión Q, sin inflatón): A1 (arXiv:2202.04029) y A2 (arXiv:2307.06329).

Marco [CITADO A1 Secs. II-III, A2 Sec. III]: el contenido es un fluido de radiación (p = rho/3, T = 0), la difusión Q es
homogénea (dQ = 0) y la constante de integración es Lambda_* = 0. Las ecuaciones de fondo (M_P = 1) son
    3 H^2 = rho + Q                      (A1 Eq. 9 con Lambda_* = 0)
    2 Hdot + 3 H^2 = -p + Q              (A1 Eq. 10)
    rho_N + Q_N + 4 rho = 0              (A1 Eq. 16; N = ln a)
y con eps1 = -Hdot/H^2 = 2/(1 + Q/rho) (A1 Eq. 18) el fondo entero queda determinado por eps1(N) y una normalización:
    H(N) = H_ref exp(-int_{N_ref}^{N} eps1),   rho = (3/2) eps1 H^2,   Q = (3/2)(2 - eps1) H^2       (A1 Eqs. 32-33)
Sin inflatón: la aceleración la produce Q (Q > rho <=> eps1 < 1, A1 Eq. 19).

Este módulo NO usa background.py salvo por la clase `Background`, para que la ecuación de modos (modes.py) sea la misma que
en RG; lo único que cambia es de dónde salen H(N), eps1(N) y X(N) (el término de masa del vínculo, que se calcula y no se
supone nulo).

Escenarios de eps1(N) (A2 Sec. III):
  1  eps1 = (1 + N_f - N)^(-gamma), normalizado al final: rho_end = 1e-11 M_P^4, N_f = 100 (A2 Eqs. 44, 46-48 y Sec. IV.A).
  2  eps1 = (2/3)(1 + tanh(alpha (N - N_f))) + exp(-4 alpha N), normalizado al inicio: rho_ini = Q_ini = M_P^4 (A1 Eq. 34, 13).
  3  eps1(N) de un potencial slow-roll V(phi) mapeado con  dphi/dDN = V'/V  (DN = N_f - N), rho_end = 1e-11 (A2 Sec. III.C).
"""
from dataclasses import dataclass, replace

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

import background as B
from config import Params

RHO_END_A2 = 1e-11   # [CITADO A2 Sec. IV.A y IV.C] densidad al final de la inflación, en M_P^4


# ------------------------------------------------------------------------------------------------ escenarios
def eps1_power(N_f, gamma):
    """Escenario 1 [CITADO A2 Eq. 44]: eps1 = (1 + N_f - N)^(-gamma)."""
    return lambda N: (1.0 + N_f - np.asarray(N, dtype=float)) ** (-gamma)


def eps1_tanh(N_f, alpha):
    """Escenario 2 [CITADO A1 Eq. 34 = A2 Eq. 49]."""
    return lambda N: (2.0 / 3.0) * (1.0 + np.tanh(alpha * (np.asarray(N, dtype=float) - N_f))) + np.exp(-4.0 * alpha * np.asarray(N, dtype=float))


def eps1_slowroll_map(potential, N_f):
    """Escenario 3 [CITADO A2 Sec. III.C]: eps1(N) = eps_V(phi(N)) con dphi/dDN = V'/V (M_P = 1), DN = N_f - N, phi_end tal que
    eps_V = 1. Devuelve (eps1(N), phi_end). Es la aproximación de slow-roll (la de A2), no la solución exacta de RG."""
    Vf = lambda p: B.V(p, potential)
    dVf = lambda p: B.dV(p, potential)
    epsV = lambda p: 0.5 * (dVf(p) / Vf(p)) ** 2
    p_end = brentq(lambda p: epsV(p) - 1.0, 0.05 if potential == "starobinsky" else 0.2, 3.0, xtol=1e-14)
    sol = solve_ivp(lambda dn, y: [dVf(y[0]) / Vf(y[0])], (0.0, N_f + 5.0), [p_end], method="DOP853", rtol=1e-12, atol=1e-14,
                    dense_output=True)
    return (lambda N: epsV(sol.sol(N_f - np.asarray(N, dtype=float))[0])), p_end


# ------------------------------------------------------------------------------------------------ reconstrucción
@dataclass
class LeonBackground:
    """Fondo reconstruido: `bg` es un background.Background (para modes.py) y `rho`, `Q`, `H`, `eps1` son splines en N."""
    bg: B.Background
    N_f: float
    N_end: float
    rho: CubicSpline
    Q: CubicSpline
    H: CubicSpline
    eps1_fn: object
    meta: dict


def _end_of_inflation(eps1, N_f):
    """N donde eps1 = 1 (por arriba). Para el escenario 1 es exactamente N_f."""
    if abs(float(eps1(N_f)) - 1.0) < 1e-12:
        return float(N_f)
    return brentq(lambda N: float(eps1(N)) - 1.0, 0.5 * N_f, 1.6 * N_f, xtol=1e-13)


def reconstruct(eps1, N_f, norm="end", rho_norm=RHO_END_A2, n_grid=20001, label="UGrad") -> LeonBackground:
    """Construye el fondo de A1/A2 a partir de eps1(N).

    norm="end"  : rho(N_end) = rho_norm  (A2, escenarios 1 y 3);  norm="start": rho(0) = rho_norm  (A1, escenario 2).
    La normalización fija H en el punto de referencia con 3H^2 = rho + Q = 2 rho / eps1 [(2 - eps1) + eps1 = 2].
    Lambda_* = 0 [SUPUESTO de A1, Sec. III]."""
    N_end = _end_of_inflation(eps1, N_f)
    N = np.linspace(0.0, N_end, n_grid)
    e = np.asarray(eps1(N), dtype=float)
    I = CubicSpline(N, e).antiderivative()(N)                     # int_0^N eps1
    N_ref, i_ref = (N_end, -1) if norm == "end" else (0.0, 0)
    H_ref = np.sqrt(2.0 * rho_norm / (3.0 * e[i_ref]))
    lnH = np.log(H_ref) - (I - I[i_ref])                          # dlnH/dN = -eps1
    H = np.exp(lnH)
    rho, Q = 1.5 * e * H**2, 1.5 * (2.0 - e) * H**2
    lnH_s = CubicSpline(N, lnH)
    # X = -3H^2 - 2 Hdot - p + lambda_bar, con Hdot/H^2 = dlnH/dN (derivada NUMÉRICA de la solución), p = rho/3, lambda_bar = Q
    X_over_H2 = -3.0 - 2.0 * lnH_s.derivative()(N) - rho / (3.0 * H**2) + Q / H**2
    phi = np.concatenate([[0.0], np.cumsum(0.5 * (np.sqrt(2 * e[1:]) + np.sqrt(2 * e[:-1])) * np.diff(N))])
    bg = B.Background(model=label, N_end=float(N_end), t_end=float("nan"), lnH=lnH_s, eps1=CubicSpline(N, e),
                      X_over_H2=CubicSpline(N, X_over_H2), phi=CubicSpline(N, -phi),
                      diag=dict(H_i=float(H[0]), eps1_i=float(e[0]), N_end=float(N_end), max_abs_X_over_H2=float(np.max(np.abs(X_over_H2))),
                                rho_norm=rho_norm, norm=norm))
    return LeonBackground(bg=bg, N_f=float(N_f), N_end=float(N_end), rho=CubicSpline(N, rho), Q=CubicSpline(N, Q), H=CubicSpline(N, H),
                          eps1_fn=eps1, meta=dict(norm=norm, rho_norm=rho_norm))


# ------------------------------------------------------------------------------------------------ caminos independientes
def integrate_continuity(lb: LeonBackground, rtol=1e-12):
    """Camino INDEPENDIENTE de la reconstrucción: dado Q(N) (de la reconstrucción), integra la continuidad de radiación
    rho_N = -4 rho - Q_N [A1 Eq. 16] desde N = 0, y calcula H con Friedmann 3H^2 = rho + Q y
    eps1 = 2/(1 + Q/rho) [A1 Eq. 18]. No usa Eqs. 32-33 ni la integral de eps1. Devuelve N, rho, H, eps1."""
    N = lb.bg.lnH.x
    QN = lb.Q.derivative()
    # Siempre HACIA ADELANTE en N: hacia atrás la solución homogénea e^{-4N} crece y amplifica el error ~e^{4 N_f}.
    # Con norm="end" la condición inicial es rho(0) de la reconstrucción y el valor en N_end queda como comprobación de la normalización.
    sol = solve_ivp(lambda n, y: [-4.0 * y[0] - float(QN(n))], (0.0, N[-1]), [float(lb.rho(0.0))], method="DOP853", rtol=rtol,
                    atol=1e-40, t_eval=N)
    rho = sol.y[0]
    Q = lb.Q(N)
    return N, rho, np.sqrt((rho + Q) / 3.0), 2.0 / (1.0 + Q / rho)


def rg_inflaton_with_same_H(lb: LeonBackground, rtol=1e-12):
    """RG con UN inflatón cuyo potencial se RECONSTRUYE para reproducir el mismo H(N): dphi/dN = -sqrt(2 eps1), V = (3 - eps1) H^2
    (M_P = 1) [ESTÁNDAR: phidot^2 = 2 eps1 H^2 y V = (3 - eps1) H^2 de las ecuaciones de RG]. Se integra la ecuación de
    Klein-Gordon de RG con ese V(phi) desde N = 0 con las mismas condiciones iniciales, y se devuelve un Background de RG
    para modes.py. Prueba que el fondo radiación + Q es, para los tensores, el fondo de un inflatón de RG."""
    N = lb.bg.lnH.x
    e = lb.bg.eps1(N)
    H = np.exp(lb.bg.lnH(N))
    phi = lb.bg.phi(N)                                            # decreciente
    V = (3.0 - e) * H**2
    Vs = CubicSpline(phi[::-1], V[::-1])
    dVs = Vs.derivative()

    def rhs(n, y):
        p, chi = y
        eps = 0.5 * chi**2
        H2 = float(Vs(p)) / (3.0 - eps)
        return [chi, eps * chi - 3.0 * chi - float(dVs(p)) / H2]   # chi = dphi/dN

    sol = solve_ivp(rhs, (0.0, N[-1]), [float(phi[0]), -np.sqrt(2.0 * float(e[0]))], method="DOP853", rtol=rtol, atol=1e-30,
                    t_eval=N)
    p, chi = sol.y
    eps = 0.5 * chi**2
    Hn = np.sqrt(Vs(p) / (3.0 - eps))
    lnH = CubicSpline(N, np.log(Hn))
    # X de RG con Lambda = 0: X = -3H^2 - 2 Hdot - p_phi (p_phi = phidot^2/2 - V), Hdot/H^2 numérico
    p_phi = 0.5 * chi**2 * Hn**2 - Vs(p)
    X = -3.0 - 2.0 * lnH.derivative()(N) - p_phi / Hn**2
    return B.Background(model="RGrec", N_end=lb.N_end, t_end=float("nan"), lnH=lnH, eps1=CubicSpline(N, eps),
                        X_over_H2=CubicSpline(N, X), phi=CubicSpline(N, p), diag=dict(H_i=float(Hn[0]), N_end=lb.N_end))


def phi_i_for_rg_duration(P: Params, N_dur, bracket):
    """phi_i tal que RG (background.py) con potencial P.potential y misma escala termina en N_end = N_dur."""
    f = lambda phi: B.solve_background_rg(replace(P, phi_i=phi)).N_end - N_dur
    return brentq(f, *bracket, xtol=1e-11)
