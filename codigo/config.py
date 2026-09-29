"""Parámetros del cálculo numérico de P_T(k) en RG y en UG con difusión Q.

Unidades: M_P (reducida) = 1, es decir kappa = 8*pi*G = 1, igual que en derivation.md.
Además se integra con m = 1 (tiempo en unidades de 1/m). Es exacto por homogeneidad: las
ecuaciones (2.7), (2.9), (3.9), (4.8) de derivation.md no cambian de forma bajo
t -> t/m, H -> m H, V -> m^2 V, Q -> m^2 Q, k -> m k. La masa física m_phys solo entra al
final, multiplicando P_T por m_phys^2 (porque P_T ~ H^2/M_P^2).

Decisiones del usuario (sesión 2026-09-20) marcadas con [USUARIO]; el resto son valores por
defecto míos, marcados [DEFECTO], que se documentan en PROVENANCE.md sec. 9 y se pueden cambiar.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Params:
    # --- modelo ---------------------------------------------------------------------------
    potential: str = "quadratic" # [USUARIO] "quadratic": V = m^2 phi^2/2 ; "starobinsky": V = (3/4) M^2 (1 - e^{-sqrt(2/3) phi})^2
    m_phys: float = 6e-6         # [USUARIO] escala de masa de V (m en el cuadrático, M en Starobinsky), en M_P. Solo escala P_T.
                                 # Con potential="starobinsky" usar params_for("starobinsky"), que fija M.
    phi_bracket: tuple = (17.0, 40.0)  # [DEFECTO] intervalo donde se busca phi_i (UG dura N_f_ug); depende del potencial
    phi_i: float | None = None   # campo inicial en M_P. None -> se ajusta para que UG dure N_f_ug e-folds
    N_f_ug: float = 100.0        # [USUARIO: 'el más usual en UG'] duración total de la inflación en UG.
                                 # Fuente: A2 Sec. III (N_f >= 65 'as usual'; N_f = 100 en el 1.er escenario)
                                 # y A1 Sec. III (N_min ~ 102 e-folds; ilustra con N_f = 70). Ver PROVENANCE sec. 9.1
    # --- difusión Q(N) = Q_i * exp(-gamma * N), N = ln(a/a_i) ------------------------------
    Q_over_V_i: float = 0.1      # [USUARIO] Q_i / V(phi_i)
    gamma: float = 0.1           # [USUARIO]
    # --- modos ----------------------------------------------------------------------------
    ratio_start: float = 100.0   # [DEFECTO] se arranca cuando k/(aH) = ratio_start (dentro del horizonte)
    ratio_stop: float = 1e-3     # [DEFECTO] se mide P_T cuando k/(aH) = ratio_stop (fuera, congelado)
    n_k: int = 40                # [DEFECTO] modos, equiespaciados en ln k
    # --- integradores ---------------------------------------------------------------------
    rtol_bg: float = 1e-12
    atol_bg: float = 1e-14
    rtol_mode: float = 1e-10
    atol_mode: float = 1e-12
    n_grid_bg: int = 20001       # puntos uniformes en t; se transforman a N para los splines
    t_max: float = 1e3           # tope de tiempo (1/m) para el fondo; el evento eps1=1 corta antes
    workers: int = 8


# [USUARIO 2026-09-21] potencial de Starobinsky. M es una CALIBRACIÓN (no una validación): se fija para que RG reproduzca
# A_s de Planck a N_* = 60 con la fórmula slow-roll escalar de orden cero (M_necesario = 1.143e-5, calculado en
# PROVENANCE sec. 13). Mi valor inicial de memoria (1.3e-5) correspondía a N_* ~ 52 y se descartó antes de correr checks.
M_STAROBINSKY = 1.14e-5
_STARO = dict(potential="starobinsky", m_phys=M_STAROBINSKY, phi_bracket=(5.0, 9.0), t_max=1e4)
# t_max = 1e4 porque con el mismo phi_i RG dura ~390 e-folds (H ~ 0.5 m) y con 1e3 no alcanza eps1 = 1


def params_for(potential: str = "quadratic", **overrides) -> Params:
    """Params con los valores por defecto propios de cada potencial. `overrides` pisa cualquier campo."""
    if potential == "quadratic":
        return Params(**overrides)
    if potential == "starobinsky":
        return Params(**{**_STARO, **overrides})
    raise ValueError(f"potencial desconocido: {potential!r}")
