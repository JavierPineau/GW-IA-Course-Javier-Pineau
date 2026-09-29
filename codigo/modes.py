"""Modos tensoriales: integración numérica de la ecuación de modos y P_T(k).

Implementa derivation.md Secs. 3-4 con la normalización decidida por el usuario
(<h_ij h_ij>, e^lambda_ij e^lambda'_ij = 2 delta, v = a M_P h / sqrt(2), Bunch-Davies).

Variable independiente: N = ln(a/a_i). Se integra v_k (variable canónica de (4.8)) reescalada,
vt = sqrt(2k) v, para que sea O(1) al inicio (los k van de ~1e3 a ~1e26 en unidades de m).

La misma rutina sirve para RG y UG: lo que las distingue son las cantidades de fondo H(N),
eps1(N) y X(N) que entrega cada `Background`. En particular X (término de masa de (4.6)) se
calcula con lambda_bar de cada modelo y ENTRA en la ecuación; el código no supone que se anula.
"""
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from background import Background
from config import Params


def mode_rhs(N, y, k, bg: Background):
    """Ecuación de modos en N, para y = (vt, dvt/dN).

    Parte de v'' + (k^2 - a''/a - 2 X a^2) v = 0, que es (3.11) con el término de masa de (4.6)
    (' = d/d eta). Con dN = aH d eta, a''/a = a^2 H^2 (2 - eps1) y d(aH)/dN = aH (1 - eps1):
        w_N + (1 - eps1) w + [ k^2/(aH)^2 - (2 - eps1) - 2 X/H^2 ] v = 0,   w = dv/dN.
    (3.11) se obtiene de (3.9) con v = a h; la forma con X viene de la acción (4.6)-(4.8)."""
    vt, w = y
    H = np.exp(bg.lnH(N))
    eps = bg.eps1(N)
    X2 = bg.X_over_H2(N)
    kk = np.exp(2.0 * (np.log(k) - N - bg.lnH(N)))   # (k/aH)^2
    return [w, -(1.0 - eps) * w - (kk - (2.0 - eps) - 2.0 * X2) * vt]


def bunch_davies_ic(k, N_s, bg: Background):
    """Condición inicial de Bunch-Davies (adiabática, orden WKB) en N_s. [SUPUESTO / ESTÁNDAR].

    v = e^{-i int omega d eta} / sqrt(2 omega),  omega^2 = k^2 - a''/a - 2 X a^2  (frecuencia de (4.8)).
    Se desprecia omega' (error relativo ~ (aH/k)^3 ~ 1e-6 con ratio_start = 100).
    En vt = sqrt(2k) v:  vt = sqrt(k/omega),  dvt/dN = v'/(aH) = -i omega/(aH) vt."""
    eps = float(bg.eps1(N_s))
    X2 = float(bg.X_over_H2(N_s))
    # Forma adimensional (sin a ni k^2 sueltos, que desbordan para N >~ 350, como en Starobinsky-RG con ~390 e-folds):
    # q = k/(aH);  omega/(aH) = sqrt(q^2 - (2 - eps) - 2 X/H^2);  vt = sqrt(k/omega) = sqrt(q/(omega/aH)).
    q = np.exp(np.log(k) - N_s - float(bg.lnH(N_s)))
    om = np.sqrt(q**2 - (2.0 - eps) - 2.0 * X2)          # omega/(aH)
    vt = np.sqrt(q / om) + 0j
    w = -1j * om * vt
    return np.array([vt, w], dtype=complex)


def tensor_power(k, vt, N):
    """P_T = <h_ij h_ij> por ln k  =  (k^3/2 pi^2) * 2 * sum_lambda |h_lambda|^2   (M_P = 1).

    Con h_lambda = sqrt(2) v_lambda/(a M_P) (4.6), dos polarizaciones idénticas, v = vt/sqrt(2k):
        P_T = 4 k^3 |v|^2 / (pi^2 a^2) = 2 k^2 |vt|^2 / (pi^2 a^2).
    En de Sitter da 2 H^2/(pi^2 M_P^2) [ESTÁNDAR, sin verificar todavía]."""
    return 2.0 * np.abs(vt) ** 2 * np.exp(2.0 * (np.log(k) - N)) / np.pi**2   # (k/a)^2 sin overflow para N grande


def _horizon_crossing_N(k_over, bg: Background):
    """N donde e^N H(N) = k_over, con e^N H creciente durante la inflación. None si no hay raíz."""
    f = lambda N: N + bg.lnH(N) - np.log(k_over)
    lo, hi = 0.0, bg.N_end
    if f(lo) > 0.0 or f(hi) < 0.0:
        return None
    return brentq(f, lo, hi, xtol=1e-13)


def run_mode(k, bg: Background, P: Params):
    """Integra un modo desde k/(aH)=ratio_start hasta k/(aH)=ratio_stop (o hasta el fin de la inflación)."""
    N_s = _horizon_crossing_N(k / P.ratio_start, bg)
    if N_s is None:
        raise ValueError(f"[{bg.model}] k={k:.3e}: k/ratio_start fuera del rango del fondo (modo empieza antes de N=0)")
    N_f = _horizon_crossing_N(k / P.ratio_stop, bg)
    stopped_early = N_f is None
    if stopped_early:
        N_f = bg.N_end
    y0 = bunch_davies_ic(k, N_s, bg)
    sol = solve_ivp(mode_rhs, (N_s, N_f), y0, method="DOP853", args=(k, bg),
                    rtol=P.rtol_mode, atol=P.atol_mode)
    if not sol.success:
        raise RuntimeError(f"[{bg.model}] k={k:.3e}: {sol.message}")
    vt_f = sol.y[0, -1]
    N_x = _horizon_crossing_N(k, bg)  # salida del horizonte, k = aH
    return dict(
        k=k, N_start=N_s, N_stop=N_f, N_exit=np.nan if N_x is None else N_x,
        ratio_final=k / (np.exp(N_f) * np.exp(bg.lnH(N_f))),
        H_exit=np.nan if N_x is None else float(np.exp(bg.lnH(N_x))),
        eps1_exit=np.nan if N_x is None else float(bg.eps1(N_x)),
        P_T=tensor_power(k, vt_f, N_f),   # en unidades m = 1; se multiplica por m_phys^2 al final
        nfev=sol.nfev, stopped_early=stopped_early,
    )


def _run_mode_star(args):
    return run_mode(*args)


def run_all_modes(ks, bg: Background, P: Params):
    """Corre todos los k (en paralelo si P.workers > 1). Devuelve lista de dicts en el orden de ks."""
    jobs = [(float(k), bg, P) for k in ks]
    if P.workers <= 1:
        return [_run_mode_star(j) for j in jobs]
    with ProcessPoolExecutor(max_workers=P.workers) as ex:
        return list(ex.map(_run_mode_star, jobs, chunksize=1))
