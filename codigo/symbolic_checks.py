"""Comprobaciones simbólicas (SymPy) de los pasos analíticos que hasta ahora estaban hechos a mano.

Uso:  python3 symbolic_checks.py     (~1 min)      |      pytest -q test_symbolic.py

Cada `check_*` devuelve un dict {id, title, passed, details, source}. Se comprueba, con álgebra exacta (sin números):

  S1  Ecuación TT sobre FLRW plano: el Tensor de Einstein de g = diag(-1, a²(1+εh), a²(1-εh), a²), h = h(t,z), cumple
      G^x_x - G^y_y = +ε (h'' + 3H h' - ∂_z² h / a²) + O(ε²)   (h' = dh/dt). En UG (G^a_b + λ̄ δ^a_b = κ T^a_b, λ̄ escalar,
      T^i_j sin parte TT) el término λ̄ δ^a_b se cancela en la diferencia x-y, así que la ecuación de h es la de RG y Q entra
      solo por H(t). Es el paso [PROPIA] de derivation.md Sec. 3 que el informe declaraba «no verificado simbólicamente».
      NO comprueba el segundo orden (acción cuadrática y cancelación del vínculo), que sigue verificado solo a mano.
  S2  Identidad ∇_a T^{ab} = (□φ - V') ∂^b φ para un campo escalar en una ansatz escalar perturbado sin E a primer orden
      (lapse A, shift B, curvatura ψ, todos función de (t,x)), con V cuadrático y de Starobinsky.
  S3  Cierre del fondo de UG con un escalar (derivation.md (2.7), (2.9)): Ḣ = -φ̇²/2; y si Q = Q(φ) las ecuaciones
      son idénticas a las de RG con V_eff = V + Q(φ) + Λ_0.
  S4  Perturbaciones: con ∇_a T^{ab} = ∇^b Q y un único campo escalar, la componente espacial a primer orden da
      ∂_x δQ = E_0 ∂_x δφ, con E_0 = □φ - V' = -(φ̈ + 3Hφ̇ + V') (fondo). Luego δQ = Q'(φ) δφ; y δQ = 0 exige E_0 = 0, es decir Q̇ = 0, SOLO si ∂_x δφ ≠ 0 (perturbación inhomogénea del inflatón) y en el
      marco donde se impone δQ = 0 (δQ cambia bajo t → t + ξ⁰ en Q̇ ξ⁰). No cubre ∂_x δφ = 0 ni otros gauges.
"""
import sympy as sp

t, x, y, z = sp.symbols("t x y z", real=True)
eps = sp.Symbol("epsilon")
COORDS = (t, x, y, z)


def tr(e):
    """Trunca a primer orden en eps (sirve para cualquier función de eps, no solo polinomios)."""
    return e.subs(eps, 0) + eps * sp.diff(e, eps).subs(eps, 0)


def christoffel(g, ginv):
    n = 4
    return [[[tr(sum(ginv[a, d] * (sp.diff(g[d, c], COORDS[b]) + sp.diff(g[d, b], COORDS[c]) - sp.diff(g[b, c], COORDS[d]))
                     for d in range(n)) / 2) for c in range(n)] for b in range(n)] for a in range(n)]


def _result(cid, title, passed, details, source):
    return dict(id=cid, title=title, passed=bool(passed), details=details, source=source)


# ---------------------------------------------------------------------------------------------------- S1
def check_tt_equation():
    a = sp.Function("a")(t)
    h = sp.Function("h")(t, z)
    g = sp.diag(-1, a**2 * (1 + eps * h), a**2 * (1 - eps * h), a**2)
    ginv = sp.diag(-1, 1 / (a**2 * (1 + eps * h)), 1 / (a**2 * (1 - eps * h)), 1 / a**2).applyfunc(tr)
    G = christoffel(g, ginv)
    n = 4

    def ricci(b, c):
        return sum(sp.diff(G[a_][b][c], COORDS[a_]) - sp.diff(G[a_][b][a_], COORDS[c]) +
                   sum(G[a_][a_][d] * G[d][b][c] - G[a_][c][d] * G[d][b][a_] for d in range(n)) for a_ in range(n))
    Ric = sp.Matrix(n, n, lambda b, c: tr(ricci(b, c)))
    Rmixed = (ginv * Ric).applyfunc(tr)          # R^a_b
    diff_xy = sp.simplify(tr(Rmixed[1, 1] - Rmixed[2, 2]))   # G^x_x - G^y_y = R^x_x - R^y_y (la traza se cancela)
    H = sp.diff(a, t) / a
    op = sp.diff(h, t, 2) + 3 * H * sp.diff(h, t) - sp.diff(h, z, 2) / a**2
    resid = sp.simplify(diff_xy - eps * op)
    off = [sp.simplify(Rmixed[i, j]) for i in range(1, 4) for j in range(1, 4) if i != j]
    return _result("S1", "ecuación TT sobre FLRW: G^x_x - G^y_y = +eps (h'' + 3H h' - h_zz/a^2)", resid == 0,
                   dict(G_xx_minus_G_yy=str(diff_xy), residual=str(resid), off_diagonal_spatial_nonzero=[str(o) for o in off if o != 0]),
                   "derivation.md Sec. 3 (3.9), (3.6)-(3.7); Einstein tensor de la métrica con h_xx = -h_yy = a^2 h")


# ---------------------------------------------------------------------------------------------------- S2
def _scalar_setup(Vexpr, phsym):
    """Ansatz escalar perturbado sin E a 1.er orden, campo phi = phi0(t) + eps dphi(t,x) y su divergencia."""
    a = sp.Function("a")(t)
    A, B, psi, dphi = (sp.Function(n)(t, x) for n in ("A", "B", "psi", "dphi"))
    phi0 = sp.Function("phi0")(t)
    g = sp.zeros(4, 4)
    g[0, 0] = -(1 + 2 * eps * A)
    g[0, 1] = g[1, 0] = eps * a * sp.diff(B, x)
    for i in (1, 2, 3):
        g[i, i] = a**2 * (1 - 2 * eps * psi)
    g0inv = sp.diag(-1, 1 / a**2, 1 / a**2, 1 / a**2)
    g1 = g.applyfunc(lambda e: sp.diff(e, eps).subs(eps, 0))
    ginv = (g0inv - eps * g0inv * g1 * g0inv).applyfunc(tr)
    Gam = christoffel(g, ginv)
    phi = phi0 + eps * dphi
    V = Vexpr.subs(phsym, phi)
    dV = sp.diff(Vexpr, phsym).subs(phsym, phi)
    dphi_l = [sp.diff(phi, c) for c in COORDS]                       # ∂_a φ (índice abajo)
    dphi_u = [tr(sum(ginv[i, j] * dphi_l[j] for j in range(4))) for i in range(4)]
    kin = tr(sum(ginv[i, j] * dphi_l[i] * dphi_l[j] for i in range(4) for j in range(4)))
    T = sp.Matrix(4, 4, lambda i, j: tr(dphi_u[i] * dphi_u[j] - ginv[i, j] * (kin / 2 + V)))
    sqrtg = a**3 * (1 + eps * (A - 3 * psi))                          # sqrt(-g) a 1.er orden (B no entra a este orden)
    box = tr(sum(sp.diff(sqrtg * dphi_u[i], COORDS[i]) for i in range(4)) / sqrtg)
    E = tr(box - dV)
    div = [tr(sum(sp.diff(T[i, b], COORDS[i]) for i in range(4)) +
              sum(Gam[i][i][c] * T[c, b] for i in range(4) for c in range(4)) +
              sum(Gam[b][i][c] * T[i, c] for i in range(4) for c in range(4))) for b in range(4)]
    return dict(a=a, A=A, B=B, psi=psi, dphi=dphi, phi0=phi0, g=g, ginv=ginv, E=E, div=div, dphi_u=dphi_u, dphi_l=dphi_l)


def check_divergence_identity():
    ph = sp.Symbol("ph")
    c, m = sp.symbols("c m", positive=True)
    pots = {"cuadratico": m**2 * ph**2 / 2, "starobinsky": sp.Rational(3, 4) * m**2 * (1 - sp.exp(-c * ph))**2}
    rows, ok = {}, True
    for name, Vexpr in pots.items():
        s = _scalar_setup(Vexpr, ph)
        res = []
        for b in range(4):
            rhs = tr(s["E"] * s["dphi_u"][b])
            res.append(sp.simplify(s["div"][b] - rhs))
        rows[name] = [str(r) for r in res]
        ok &= all(r == 0 for r in res)
    return _result("S2", "∇_a T^{ab} = (□φ - V') ∂^b φ a 1.er orden, ansatz escalar sin E, V cuadrático y de Starobinsky", ok,
                   dict(residuals_by_component=rows), "identidad estándar; derivation.md (1.8), (2.9)")


# ---------------------------------------------------------------------------------------------------- S3
def check_background_closure():
    Hs, ph, phid, phidd, Q, Qd, L0 = sp.symbols("H phi phid phidd Q Qd Lambda0")
    V = sp.Function("V")
    Vp = sp.Function("Vp")            # V'(phi), independiente: la comprobación no depende de la forma de V
    # UG: (2.7) 3H^2 = phid^2/2 + V + Q + L0 ; (2.9) phidd + 3 H phid + V' + Qd/phid = 0
    # d/dt (2.7):  6 H Hd = phid phidd + V' phid + Qd
    phidd_ug = -3 * Hs * phid - Vp(ph) - Qd / phid
    Hd = (phid * phidd_ug + Vp(ph) * phid + Qd) / (6 * Hs)
    hd_expr = sp.simplify(Hd)
    ok_28 = sp.simplify(hd_expr + phid**2 / 2) == 0       # Hdot = -phid^2 / 2 con (2.9)
    # Q = Q(phi): Qd = Qp(phi) phid  =>  ecuaciones = RG con V_eff = V + Q(phi) + L0
    Qp = sp.Symbol("Qp")
    phidd_ug_Q = phidd_ug.subs(Qd, Qp * phid)
    phidd_rg_eff = -3 * Hs * phid - (Vp(ph) + Qp)          # KG de RG con V_eff' = V' + Q'
    ok_eq = sp.simplify(phidd_ug_Q - phidd_rg_eff) == 0
    # Friedmann: (2.7) 3H^2 = phid^2/2 + V + Q(phi) + L0 es, por definición de V_eff, la de RG: no hay nada que comprobar.
    return _result("S3", "fondo UG con un escalar: Hdot = -phidot^2/2; Q = Q(phi) ⇒ RG con V_eff = V + Q + Lambda_0",
                   ok_28 and ok_eq, dict(Hdot_UG=str(hd_expr), Hdot_eq_minus_half_phid2=bool(ok_28),
                                                 KG_equal_RG_Veff=bool(ok_eq)),
                   "derivation.md (2.7)-(2.9), (2.14)")


# ---------------------------------------------------------------------------------------------------- S4
def check_dQ_constraint():
    ph = sp.Symbol("ph")
    m = sp.Symbol("m", positive=True)
    s = _scalar_setup(m**2 * ph**2 / 2, ph)
    a, phi0, dphi, g = s["a"], s["phi0"], s["dphi"], s["g"]
    E0 = -(sp.diff(phi0, t, 2) + 3 * (sp.diff(a, t) / a) * sp.diff(phi0, t) + m**2 * phi0)   # E = □φ - V' de fondo (signatura -+++)
    # componente espacial (índice abajo) de ∇_a T^{ab}: g_{xb} div^b, a orden eps
    low_x = tr(sum(g[1, b] * s["div"][b] for b in range(4)))
    first_order_x = sp.simplify(sp.diff(low_x, eps).subs(eps, 0))
    expected = sp.simplify(E0 * sp.diff(dphi, x))                                       # E_0 ∂_x δφ
    ok_x = sp.simplify(first_order_x - expected) == 0
    # b = t a orden 0: ∇_a T^{at} = E_0 ∂^t φ = -E_0 phi0_dot  y  ∇^t Q = -Qdot  =>  Qdot = E_0 phi0_dot  (equivale a (2.9): phiddot + 3H phidot + V' = -Qdot/phidot)
    zeroth_t = sp.simplify(s["div"][0].subs(eps, 0) + E0 * sp.diff(phi0, t))
    ok_t = zeroth_t == 0
    # Consecuencia lógica de ∂_x δQ = E_0 ∂_x δφ con δQ = 0 (en el marco/gauge donde se impone δQ = 0). Es un producto: se anula si E_0 = 0 O si ∂_x δφ = 0.
    # Rama genérica (∂_x δφ ≠ 0, perturbación inhomogénea del inflatón): E_0 = 0 y entonces Qdot = E_0 phi0_dot = 0.
    dphx = sp.Symbol("dphx", nonzero=True)
    E0s = sp.Symbol("E0s")
    ok_generic = sp.solve(sp.Eq(0, E0s * dphx), E0s) == [0]
    # Rama excluida: con ∂_x δφ = 0 (campo espacialmente uniforme) la relación se cumple para todo E_0, es decir, NO fuerza E_0 = 0.
    ok_branch = sp.Eq(0, E0s * 0) == sp.true
    ok_logic = bool(ok_generic and ok_branch)
    return _result("S4", "∇_a T^{ab} = ∇^b Q con un escalar: ∂_x δQ = E_0 ∂_x δφ; con δQ = 0 y ∂_x δφ ≠ 0: E_0 = 0 ⇒ Qdot = 0 (no cubre ∂_x δφ = 0 ni otros gauges)",
                   ok_x and ok_t and ok_logic,
                   dict(spatial_first_order_equals_E0_dx_dphi=bool(ok_x), time_background_Qdot_equals_E0_phidot=bool(ok_t),
                        dQ_zero_implies_E0_zero_if_dphi_nonzero=bool(ok_generic), branch_dphi_zero_leaves_E0_free=bool(ok_branch)),
                   "derivation.md (1.8); informe sec. de acoplamiento de Q")


ALL_SYMBOLIC = [check_tt_equation, check_divergence_identity, check_background_closure, check_dQ_constraint]

if __name__ == "__main__":
    import sys
    import time
    allok = True
    for fn in ALL_SYMBOLIC:
        t0 = time.time()
        r = fn()
        allok &= r["passed"]
        print(f"[{'PASS' if r['passed'] else 'FAIL'}] {r['id']} {r['title']}  ({time.time() - t0:.1f} s)")
        if not r["passed"]:
            print("   ", r["details"])
    sys.exit(0 if allok else 1)
