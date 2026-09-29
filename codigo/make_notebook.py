"""Genera explorador_PT.ipynb a partir de los .py de esta carpeta.

El notebook es autocontenido: cada módulo va, verbatim, en una celda `%%writefile _nb_src/<archivo>.py`, que se puede
leer, editar y volver a correr. Los .py de esta carpeta siguen siendo la fuente de verdad (PROVENANCE.md los cita);
test_notebook_sync.py comprueba que el código embebido sea idéntico. Si cambiás un .py, regenerá con:

    python3 make_notebook.py

Para ejecutarlo y guardar las salidas:
    jupyter nbconvert --to notebook --execute --inplace explorador_PT.ipynb
"""
from pathlib import Path

import nbformat as nbf

HERE = Path(__file__).parent
MODULES = ["config.py", "background.py", "modes.py", "checks.py", "run_spectrum.py"]  # orden de dependencias

cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s.strip("\n")))
code = lambda s: cells.append(nbf.v4.new_code_cell(s.strip("\n")))

# ------------------------------------------------------------------------------------------------- 0
md(r"""
# Explorador de P_T(k): RG vs. gravedad unimodular con difusión Q

Notebook autocontenido para **correr, graficar y chequear** el cálculo del espectro tensorial primordial
(`derivation.md` → `PROVENANCE.md` sec. 9 y 10). Potencial `V = ½m²φ²`, un solo campo, `Q(N) = Q_i e^(−γN)` acoplado al inflatón (2.9).

**Cómo se usa**
1. Corré la sección 1 (escribe el código en `_nb_src/` y lo importa). El código está en las celdas: podés leerlo y editarlo; si editás una celda, volvela a correr y corré la celda de *recarga*.
2. Las secciones 2 a 6 se corren en orden. Los parámetros se cambian en la sección 2 (`P = Params(...)`).
3. La sección 7 corre los checks (~1 min) y los grafica. La sección 8 es exploración libre.

**Unidades:** `M_P = 1` (reducida, κ=1) y `m = 1` (tiempo en 1/m); `k` en unidades de `m` con `a_i = 1`. La masa física `m_phys = 6e-6 M_P` solo multiplica `P_T` por `m²` al final (exacto por homogeneidad, ver `config.py`).

**Fuente de verdad:** los archivos `.py` de la carpeta `codigo/`. Este notebook los genera `make_notebook.py` y `test_notebook_sync.py` comprueba que coincidan.

**Sobre lo que sale acá:** los resultados de las secciones 3 a 7 son los que están verificados en `PROVENANCE.md` sec. 10 (con los límites de 10.6). La sección 8 es exploración **no verificada**.
""")

# ------------------------------------------------------------------------------------------------- 1
md(r"""
## 1. Código

Mapa función → ecuación de `derivation.md` (detalle completo en `PROVENANCE.md` 9.2):

| Módulo | Función | Implementa |
|---|---|---|
| `background.py` | `rho_and_p` | (2.5) |
| | `hubble_rg` / `hubble_ug` | (2.10) / (2.7) |
| | `quantities_rg` / `quantities_ug` | (2.10) KG / (2.9); `Ḣ` como derivada de Friedmann (no usa (2.8)) |
| | `lambda0_from_initial` | (2.11) |
| | `tensor_mass_term` | (4.6): `X = −3H²−2Ḣ−κp+λ̄` |
| `modes.py` | `mode_rhs` | (3.11) con el término de masa de (4.6), en la variable `N` |
| | `bunch_davies_ic` | Bunch–Davies adiabático para (4.8) |
| | `tensor_power` | `P_T = ⟨h_ij h_ij⟩`, `e·e = 2` |
| `checks.py` | `check_*` | ver `PROVENANCE.md` sec. 10 |

Las cinco celdas siguientes escriben los módulos (verbatim de los `.py`). Después viene la celda de importación.
""")

code("""
import pathlib
pathlib.Path("_nb_src").mkdir(exist_ok=True)
print("carpeta _nb_src lista")
""")
for f in MODULES:
    src = (HERE / f).read_text().rstrip("\n")
    code(f"%%writefile _nb_src/{f}\n{src}")

md("**Importación y recarga** (volvé a correr esta celda después de editar cualquiera de las celdas de arriba, en el mismo orden):")
code("""
import sys, importlib, pathlib
SRC = pathlib.Path("_nb_src").resolve()
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import config, background, modes, checks, run_spectrum
for _m in (config, background, modes, checks, run_spectrum):      # orden de dependencias
    importlib.reload(_m)

%matplotlib inline
import numpy as np, matplotlib.pyplot as plt, pandas as pd
from dataclasses import replace
from scipy.integrate import solve_ivp
plt.rcParams.update({"figure.dpi": 100, "axes.grid": True, "grid.alpha": 0.25})

B, M, C = background, modes, checks
Params = config.Params
print("módulos cargados desde", SRC.relative_to(pathlib.Path.cwd()))
""")

# ------------------------------------------------------------------------------------------------- 2
md(r"""
## 2. Parámetros

Los valores por defecto son los de `config.py`. `phi_i` se ajusta para que **UG dure `N_f = 100` e-folds** (valor usual en A1/A2, `PROVENANCE.md` 9.1); RG usa el mismo `phi_i` y las mismas condiciones iniciales, así que dura más.
Editá acá y volvé a correr de esta celda hacia abajo. Si el paralelismo da problemas en tu sistema, poné `workers=1`.
""")
code("""
P = Params(
    # m_phys=6e-6,         # masa del inflatón en M_P (solo escala la amplitud)
    # Q_over_V_i=0.1,      # Q_i / V(phi_i)
    # gamma=0.1,           # Q(N) = Q_i exp(-gamma N)
    # N_f_ug=100.0,        # e-folds de inflación en UG (fija phi_i)
    # ratio_start=100.0,   # k/(aH) inicial (dentro del horizonte)
    # ratio_stop=1e-3,     # k/(aH) al medir P_T (fuera, congelado)
    # n_k=40, workers=8,
)
P = replace(P, phi_i=B.phi_i_for_ug_duration(P))
print(f"phi_i = {P.phi_i:.6f} M_P  (ajustado para que UG dure {P.N_f_ug:g} e-folds)")
P
""")

# ------------------------------------------------------------------------------------------------- 3
md(r"""
## 3. Fondo: RG vs. UG con Q(N)

`H(N)`, `ε₁(N)`, `φ(N)` y el papel de `Q`. Condiciones iniciales idénticas: al inicio los dos coinciden; después `Q(N)` los separa. Notá el salto de `ε₁` de UG en el primer e-fold: la velocidad inicial de slow-roll de RG no está en el atractor de UG.
""")
code("""
bg_rg = B.solve_background_rg(P)
bg_ug = B.solve_background_ug(P)
for bg in (bg_rg, bg_ug):
    d = bg.diag
    print(f"{bg.model}: H_i={d['H_i']:.5g}  eps1_i={d['eps1_i']:.4g}  N_end={d['N_end']:.3f}")
print(f"UG: Q_i={bg_ug.diag['Q_i']:.5g}  Lambda_0={bg_ug.diag['Lambda0']:.5g}  (Lambda_0 = -Q_i por (2.11))")

N_rg = np.linspace(0, bg_rg.N_end, 2000); N_ug = np.linspace(0, bg_ug.N_end, 2000)
Q_ug = B.Q_of_N(N_ug, bg_ug.diag["Q_i"], P.gamma)
fig, ax = plt.subplots(2, 2, figsize=(11, 7))
ax[0, 0].plot(N_rg, np.exp(bg_rg.lnH(N_rg)), label="RG"); ax[0, 0].plot(N_ug, np.exp(bg_ug.lnH(N_ug)), "--", label="UG")
ax[0, 0].set(xlabel="N = ln(a/a_i)", ylabel="H  [m]", title="Hubble"); ax[0, 0].legend()
ax[0, 1].semilogy(N_rg, bg_rg.eps1(N_rg), label="RG"); ax[0, 1].semilogy(N_ug, bg_ug.eps1(N_ug), "--", label="UG")
ax[0, 1].axhline(1, color="k", lw=0.8); ax[0, 1].set(xlabel="N", ylabel=r"$\\epsilon_1$", title="eps1 (inflación termina en eps1 = 1)"); ax[0, 1].legend()
ax[1, 0].plot(N_rg, bg_rg.phi(N_rg), label="RG"); ax[1, 0].plot(N_ug, bg_ug.phi(N_ug), "--", label="UG")
ax[1, 0].set(xlabel="N", ylabel=r"$\\phi$  [M_P]", title="Campo"); ax[1, 0].legend()
ax[1, 1].semilogy(N_ug, Q_ug, label=r"$Q(N)$"); ax[1, 1].semilogy(N_ug, B.V(bg_ug.phi(N_ug)), label=r"$V(\\phi_{UG})$")
ax[1, 1].semilogy(N_ug, np.abs(Q_ug - bg_ug.diag["Q_i"]), ":", label=r"$|\\bar\\lambda| = |\\Lambda_0 + Q|$")
ax[1, 1].set(xlabel="N", ylabel="densidad de energía [m² M_P²]", title="Q frente al potencial (UG)"); ax[1, 1].legend()
fig.tight_layout(); plt.show()
""")

md(r"""
### 3b. La ecuación (2.8) sobre la solución integrada

`Ḣ = −φ̇²/2` **no** se usó para construir el fondo (`Ḣ` sale de derivar Friedmann). Acá se contrasta: en `N`, `−d ln H/dN = φ_N²/2` (= `ε₁`). Izquierda: las dos cantidades (se superponen). Derecha: la diferencia (check C3.2, tolerancia 1e-6).
""")
code("""
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
for bg, st in ((bg_rg, "-"), (bg_ug, "--")):
    N = np.linspace(0, bg.N_end - 1, 4000)
    lhs = -bg.lnH.derivative()(N); rhs = 0.5 * bg.phi.derivative()(N) ** 2
    ax[0].semilogy(N, lhs, st, label=f"{bg.model}: -dlnH/dN"); ax[0].semilogy(N, rhs, ":", label=f"{bg.model}: phi_N^2/2")
    ax[1].semilogy(N, np.abs(lhs - rhs) + 1e-18, st, label=bg.model)
ax[1].axhline(1e-6, color="r", ls=":", label="tolerancia C3.2")
ax[0].set(xlabel="N", title="eps1 por dos caminos"); ax[1].set(xlabel="N", title="|diferencia|", ylim=(1e-17, 1e-5)); ax[0].legend(fontsize=7); ax[1].legend()
plt.show()
""")

# ------------------------------------------------------------------------------------------------- 4
md(r"""
## 4. Un modo en detalle

Evolución de un modo `k` a través del cruce del horizonte (`k = aH`, línea vertical). Se integra `ṽ = √(2k) v` con `mode_rhs`, arrancando en `k/(aH) = ratio_start` con Bunch–Davies. Se grafica `P_T(N) ≡ 2k³|h|²/π²` instantáneo (unidades m=1): oscila/decae dentro del horizonte y **se congela** afuera. El valor final es el `P_T(k)` que reporta `run_mode`.

Cambiá `N_exit_demo` (e-folds, medidos en RG, a los que el modo sale del horizonte).
""")
code("""
N_exit_demo = 40.0

def mode_history(k, bg, P, n=6000):
    N_s = M._horizon_crossing_N(k / P.ratio_start, bg)
    N_f = M._horizon_crossing_N(k / P.ratio_stop, bg) or bg.N_end
    sol = solve_ivp(M.mode_rhs, (N_s, N_f), M.bunch_davies_ic(k, N_s, bg), method="DOP853", args=(k, bg),
                    rtol=P.rtol_mode, atol=P.atol_mode, dense_output=True)
    N = np.linspace(N_s, N_f, n)
    vt = sol.sol(N)[0]
    h_abs = np.abs(vt) / (np.exp(N) * np.sqrt(k))                # |h| = sqrt(2)|v|/a con v = vt/sqrt(2k)
    return N, vt, 2 * k**3 * h_abs**2 / np.pi**2                 # P_T instantáneo

k_demo = C.k_at_exit(bg_rg, N_exit_demo)
fig, ax = plt.subplots(1, 3, figsize=(14, 3.8))
for bg, st in ((bg_rg, "-"), (bg_ug, "--")):
    N, vt, PT_t = mode_history(k_demo, bg, P)
    Nx = M._horizon_crossing_N(k_demo, bg)
    ax[0].semilogy(N, PT_t * P.m_phys**2, st, label=bg.model); ax[0].axvline(Nx, color="gray", ls=":")
    inside = N <= Nx + 0.5                                       # dentro del horizonte (y un poco después del cruce)
    ax[1].plot(N[inside], vt.real[inside], st, lw=0.9, label=bg.model); ax[1].axvline(Nx, color="gray", ls=":")
    ax[2].semilogy(N, k_demo / (np.exp(N) * np.exp(bg.lnH(N))), st, label=bg.model); ax[2].axvline(Nx, color="gray", ls=":")
    print(f"{bg.model}: sale del horizonte en N = {Nx:.3f};  P_T final = {PT_t[-1] * P.m_phys**2:.6e}")
ax[0].set(xlabel="N", ylabel=r"$P_T$ instantáneo", title=f"congelamiento (k = {k_demo:.2e} m)"); ax[0].legend()
ax[1].set(xlabel="N", ylabel=r"Re $\\tilde v_k$", title="oscilación de Bunch-Davies (dentro del horizonte)"); ax[1].legend()
ax[2].axhline(1, color="k", lw=0.8); ax[2].set(xlabel="N", ylabel="k / (aH)", title="cruce del horizonte"); ax[2].legend()
fig.tight_layout(); plt.show()
""")

# ------------------------------------------------------------------------------------------------- 5
md(r"""
## 5. Espectro P_T(k), RG vs. UG

Malla común de `k` (mismo `a_i`, mismas condiciones iniciales). Se integran todos los modos con `run_all_modes` (paralelo). Salidas: `P_T(k)`, el cociente UG/RG, y la comparación con la fórmula slow-roll de LO, `2H²/π²` en `k = aH` (con `H` en el cruce).
""")
code("""
ks = run_spectrum.k_grid(bg_rg, bg_ug, P)
res = {}
for bg in (bg_rg, bg_ug):
    out = M.run_all_modes(ks, bg, P)
    res[bg.model] = {key: np.array([o[key] for o in out]) for key in out[0]}
m2 = P.m_phys**2
PT_rg, PT_ug = res["RG"]["P_T"] * m2, res["UG"]["P_T"] * m2
print(f"{len(ks)} modos, k de {ks[0]:.3e} a {ks[-1]:.3e} (rango de {np.log(ks[-1]/ks[0]):.1f} e-folds)")
print("modos que no llegaron a k/aH = ratio_stop antes del fin:", int(res['RG']['stopped_early'].sum()), "(RG),", int(res['UG']['stopped_early'].sum()), "(UG)")

fig, ax = plt.subplots(1, 3, figsize=(15, 4))
ax[0].loglog(ks, PT_rg, "o-", ms=3, label="RG"); ax[0].loglog(ks, PT_ug, "s--", ms=3, label="UG con Q(N)")
ax[0].set(xlabel="k  [m, a_i=1]", ylabel=r"$P_T(k)$", title="espectro tensorial"); ax[0].legend()
ax[1].semilogx(ks, PT_ug / PT_rg, "k.-"); ax[1].axhline(1, color="gray", lw=0.8)
ax[1].set(xlabel="k  [m, a_i=1]", ylabel=r"$P_T^{UG}/P_T^{RG}$", title="cociente")
for name, st in (("RG", "o"), ("UG", "s")):
    LO = 2 * res[name]["H_exit"] ** 2 / np.pi**2
    ax[2].semilogy(res[name]["eps1_exit"], np.abs(res[name]["P_T"] / LO - 1), st, ms=4, label=f"{name}: |P_T/LO - 1|")
e = np.linspace(2e-3, 0.06, 100)
ax[2].semilogy(e, 2 * (np.euler_gamma + np.log(2) - 1) * e, "k:", label=r"$2(1+C)\\,\\epsilon_1$ (predicción NLO)")
ax[2].set(xlabel=r"$\\epsilon_1$ en el cruce", title="P_T frente a 2H²/π² (LO)"); ax[2].legend(fontsize=8)
fig.tight_layout(); plt.show()

pd.DataFrame(dict(k=ks, N_exit_RG=res["RG"]["N_exit"], N_exit_UG=res["UG"]["N_exit"], eps1_exit_RG=res["RG"]["eps1_exit"],
                  eps1_exit_UG=res["UG"]["eps1_exit"], PT_RG=PT_rg, PT_UG=PT_ug, UG_sobre_RG=PT_ug / PT_rg)).iloc[::4]
""")

# ------------------------------------------------------------------------------------------------- 6
md(r"""
## 6. Comparación con la literatura para `φ²` (RG)

`r`, `n_T` y `A_s` en `N_* = 50` y `60` e-folds antes del fin de la inflación de RG: check C1.3 (`PROVENANCE.md` 10.3). Referencias: Martin et al. (2.19)–(2.25), Baumann (8.128), Planck 2018 X.
""")
code("""
r13 = C.check_planck_phi2()
print("C1.3 pasa:", r13["passed"], "| peor caso:", r13["worst"], "|", r13["tolerance"])
pd.DataFrame(r13["details"])
""")

# ------------------------------------------------------------------------------------------------- 7
md(r"""
## 7. Checks (`PROVENANCE.md` sec. 10)

Corre los 10 checks (~1 min). Cada uno devuelve `passed`, el peor caso medido y la tolerancia (con revisiones documentadas en el docstring de la función: `C.check_...__doc__`).
Para correr uno solo: `C.check_de_sitter_exact()`, `C.check_slow_roll_rg()`, etc.
""")
code("""
results = C.run_all(verbose=True)
R = {r["id"]: r for r in results}
pd.DataFrame([dict(id=r["id"], pasa=r["passed"], peor_caso=r["worst"], tolerancia=r["tolerance"], check=r["title"]) for r in results])
""")

md("### 7a. C1.2 — RG frente a la expansión slow-roll (LO, NLO, NNLO)\nCada orden reduce el residuo; a NNLO queda por debajo de la tolerancia (línea punteada negra).")
code("""
d = R["C1.2"]["details"]; eps = np.array([r["eps1"] for r in d])
fig, ax = plt.subplots(figsize=(6.5, 4.5))
for key, lab, st in (("resid_LO", "LO", "o-"), ("resid_NLO", "NLO", "s-"), ("resid_NNLO", "NNLO", "^-")):
    ax.loglog(eps, [abs(r[key]) + 1e-12 for r in d], st, label=lab)
ax.loglog(eps, [r["tol_NNLO"] for r in d], "k:", label="tolerancia NNLO")
for p, st in ((1, "--"), (2, "--"), (3, "--")):
    ax.loglog(eps, eps**p, st, color="gray", lw=0.7); ax.annotate(f"eps^{p}", (eps[-1], eps[-1]**p), fontsize=7, color="gray")
ax.set(xlabel=r"$\\epsilon_1$", ylabel="|P_T / (LO·a0) − 1|", title="C1.2: convergencia del desarrollo slow-roll"); ax.legend()
plt.show()
""")

md("### 7b. C2 — convergencia numérica\nError máximo frente a un valor «verdad» más fino, un parámetro por vez. Rojo: tolerancia. Verde: valor por defecto.")
code("""
det = R["C2"]["details"]; names = [k for k in det if not k.startswith("_")]
fig, ax = plt.subplots(1, len(names), figsize=(3.6 * len(names), 3.6))
for a, nme in zip(ax, names):
    v = det[nme]; xs = [float(x) for x in v["max_rel_err_by_value"]]; ys = np.array(list(v["max_rel_err_by_value"].values())) + 1e-16
    a.loglog(xs, ys, "o-"); a.axhline(v["tol"], color="r", ls=":"); a.axvline(v["default"], color="g", ls="--"); a.set_title(nme, fontsize=9)
    a.set_xlabel("valor"); a.set_ylabel("max |P/P_verdad − 1|")
fig.tight_layout(); plt.show()
""")

md("### 7c. C3.4 — el cociente UG/RG y su explicación por el fondo\nIzquierda: cociente numérico frente al predicho por la fórmula slow-roll NNLO de RG evaluada con el `H`, `ε₁`, `ε₂` **propios de UG**. Derecha: la diferencia relativa (rojo: tolerancia; los modos con `ε₂ > 0.05` no se juzgan a priori).")
code("""
d34 = R["C3.4"]["details"]; att = d34["attribution"]; Nx = np.array([r["N_exit_RG"] for r in att])
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(Nx, [r["ratio_numeric"] for r in att], "o", label="numérico"); ax[0].plot(Nx, [r["ratio_slowroll_NNLO"] for r in att], "-", label="slow-roll NNLO con H, eps propios")
ax[0].set(xlabel="N_exit (RG)", ylabel="P_T^UG / P_T^RG"); ax[0].legend()
judged = np.array([r["judged"] for r in att])
ax[1].semilogy(Nx[judged], [abs(r["dev"]) for r in att if r["judged"]], "o-", label="juzgados")
ax[1].semilogy(Nx[~judged], [abs(r["dev"]) for r in att if not r["judged"]], "x", color="k", ms=9, label="no juzgados (eps2>0.05)")
ax[1].semilogy(Nx, [r["tol"] for r in att], "r:", label="tolerancia")
ax[1].set(xlabel="N_exit (RG)", ylabel="|numérico/predicho − 1|"); ax[1].legend()
plt.show()
print(f"señal mínima |ratio-1| = {d34['signal_min']:.3f};  ruido numérico = {d34['noise']:.2e};  señal/ruido = {d34['signal_over_noise']:.1e}")
print("variación del cociente por variante numérica:", {k: float(f"{v:.1e}") for k, v in d34["noise_by_variant"].items()})
""")

md("### 7d. C3.5 y C0 — sensibilidad del código y control de mutaciones")
code("""
d35 = R["C3.5"]["details"]; x = np.arange(len(d35["N_exits"]))
fig, ax = plt.subplots(figsize=(6.5, 3.8))
ax.bar(x - 0.2, np.array(d35["rel_change_wrong_lambda"]) + 1e-16, 0.4, label="λ̄ sin Q (ecuación equivocada)")
ax.bar(x + 0.2, np.array(d35["rel_change_X_zero"]) + 1e-16, 0.4, label="X forzado a 0 (lo que dice la derivación)")
ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels([f"N={int(n)}" for n in d35["N_exits"]])
ax.set(ylabel="cambio relativo de P_T (UG)", title="C3.5: el código detecta un término de masa real"); ax.legend(fontsize=8)
plt.show()
pd.DataFrame(dict(detectada=R["C0"]["details"]["mutation_detected"], resultado_del_check_mutado=R["C0"]["details"]["outcome_of_mutated_check"]))
""")

# ------------------------------------------------------------------------------------------------- 8
md(r"""
## 8. Exploración libre (**no verificada**, no forma parte de los checks)

Cómo cambia `P_T^UG/P_T^RG` al variar `γ` o `Q_i/V_i`. Esto **no está barrido ni verificado** en `PROVENANCE.md` sec. 10 (ver 10.6, «un solo conjunto de parámetros»); sirve para tener una idea antes de hacerlo bien. Se mantiene `phi_i` fijo (el ajustado arriba), así que la duración de UG cambia con los parámetros. Si un caso no termina la inflación o el modo no cabe, se devuelve `nan`. **Ojo:** cuando `N_end(UG)` (que se imprime abajo) queda cerca de `N_exit`, ese modo sale casi al final de la inflación de UG y el cociente refleja la zona donde slow-roll deja de valer (ver C3.4, modos con `ε₂ > 0.05`), no solo el efecto de `Q`.
""")
code("""
N_exits_scan = (20.0, 40.0, 60.0)

def scan(name, values):
    out = {}
    for v in values:
        Pv = replace(P, **{name: v})
        try:
            b_r, b_u = B.solve_background_rg(Pv), B.solve_background_ug(Pv)
            rat = []
            for N in N_exits_scan:
                k = C.k_at_exit(b_r, N)
                rat.append(M.run_mode(k, b_u, Pv)["P_T"] / M.run_mode(k, b_r, Pv)["P_T"])
            out[v] = (b_u.N_end, rat)
        except Exception as e:
            out[v] = (np.nan, [np.nan] * len(N_exits_scan))
            print(f"  {name}={v}: {type(e).__name__}: {str(e)[:70]}")
    return out

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for a, (name, vals) in zip(ax, (("gamma", (0.02, 0.05, 0.1, 0.2, 0.5)), ("Q_over_V_i", (0.02, 0.05, 0.1, 0.2, 0.4)))):
    r = scan(name, vals)
    xs = list(r)
    for j, N in enumerate(N_exits_scan):
        a.plot(xs, [r[x][1][j] for x in xs], "o-", label=f"N_exit = {N:g}")
    a.set_xscale("log"); a.set(xlabel=name, ylabel="P_T^UG / P_T^RG", title=f"variando {name} (el resto por defecto)"); a.legend()
    print(name, "→ N_end(UG):", {x: round(r[x][0], 1) for x in xs})
fig.tight_layout(); plt.show()
""")

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
out = HERE / "explorador_PT.ipynb"
_src = lambda n: [(c.cell_type, c.source) for c in n.cells]
if out.exists() and _src(nbf.read(out, as_version=4)) == _src(nb):
    print(f"{out.name}: fuentes sin cambios; se conservan las salidas guardadas ({len(cells)} celdas)")
else:
    nbf.write(nb, out)
    print(f"escrito {out} ({len(cells)} celdas, sin salidas: ejecutarlo con el comando de REPRODUCCION.md)")
