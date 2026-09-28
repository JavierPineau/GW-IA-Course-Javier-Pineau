> Estado vigente: ver [REPRODUCCION.md](../REPRODUCCION.md) y [auditoría](../AUDITORIA_CONSOLIDADA.md). Este documento conserva hitos históricos; los recuentos y pendientes de cada fecha no describen necesariamente la entrega actual. Las mutaciones simbólicas narradas no se conservan como pruebas reproducibles.

# PROVENANCE — Etapa de literatura

Proyecto: espectro de potencia tensorial primordial en gravedad unimodular (UG) vs. RG.
> **[HISTÓRICO, 2026-09-19; el estado vigente está en las secs. 15–16 y en `ESTADO.md`]** Etapa: **solo literatura** (no hay derivación ni código de física todavía).
Fecha de la búsqueda y verificación: 2026-09-20.

## 0. Cómo leer este archivo

**Niveles de verificación** (última columna de cada tabla):

| Marca | Significa |
|---|---|
| **T** | Texto leído desde el PDF (`pdftotext`); la ecuación/afirmación citada fue contrastada con el texto impreso. La numeración de ecuaciones es la del PDF de la versión arXiv indicada, que puede diferir de la versión publicada. |
| **T-parcial** | Solo se leyeron las secciones/ecuaciones indicadas (búsqueda por palabras clave + lectura del contexto), no el paper completo. |
| **A** | Solo se verificaron abstract y metadatos (arXiv API / Crossref). El contenido específico NO fue leído; lo que dice la columna "qué se toma" es lo que el abstract afirma y debe releerse antes de usarlo. |
| **X** | No se accedió al texto (paywall o no descargado). Se lista por su rol; su contenido no está verificado. |

**Metadatos editoriales** (revista, volumen, DOI): verificados contra la API de Crossref (`literatura_tools/cr.py`) y/o la API de arXiv (`literatura_tools/arxq.py`, `arxabs.py`). Las búsquedas web se usaron **solo para descubrir** candidatos, nunca como evidencia de contenido.

**Fuentes de los PDFs leídos:**
- Carpeta compartida por el director (G. León): `/home/javier-pineau/Doctorado/archivos_unimodular_compartidos-20260919T164029Z-1-001/archivos_unimodular_compartidos/` (versiones: León v2, Piccirilli-León v1, Bengochea et al. v2).
- Resto: descargados de `arxiv.org/pdf/<id>` el 2026-09-20 (última versión disponible ese día salvo que se indique).

**Convención:** `Eq. (n)` = número impreso en el PDF leído. `[M]` = afirmación que viene de mi conocimiento previo y **no** fue contrastada con el texto (hay que verificarla antes de usarla).

---

## 1. Papers de la carpeta del director (fuente primaria del trabajo)

| # | Cita completa | Qué se toma (ecuación / resultado específico) | Link / DOI | Verif. |
|---|---|---|---|---|
| A1 | G. León, "Inflation and the cosmological (not-so) constant in unimodular gravity", *Class. Quantum Grav.* **39**, 075008 (2022). arXiv:2202.04029v2. | (i) Hipótesis (i) contenido = radiación pura, `T=0=δT`, y (ii) `Q` homogéneo, `δQ=δR=0`; `R = 4Q/M_P²` Eq. (40). (ii) Ecs. perturbadas UG = las de RG, Ec. (41). (iii) Eq. (57): `ℋ²−ℋ' = a²(ρ₀+p₀)/(2M_P²)`, "independent of Q explicitly". (iv) Ecs. (58)–(60): ecuación de Mukhanov-Sasaki para `R` / `M=zR` con velocidad del sonido² = 1/3; `z` definida en Eq. (59). (v) **Eq. (66): `P_R = 3^{3/2} H² / (8π² M_P² ε₁)`**; texto: "this result is independent of the particular function Q… The diffusion term Q only affects the dynamics of the background". (vi) Reconstrucción de `Q(N)` desde `ε₁(N)` (Sec. III). **No contiene sector tensorial**: búsqueda de texto por "tensor", "graviton", "gravitational wave", "ratio" solo devuelve "energy-momentum tensor"; `r` no aparece. | https://arxiv.org/abs/2202.04029 · DOI 10.1088/1361-6382/ac52bc | **T-parcial** (Sec. de perturbaciones y ecs. citadas) |
| A2 | M. P. Piccirilli, G. León, "Reconstruction of inflationary scenarios in non-conservative unimodular gravity", *Mon. Not. R. Astron. Soc.* **524**, 4024 (2023). arXiv:2307.06329v1. | Eq. (38): continuidad de radiación `ρ̇_r + 3H(ρ_r+P_r) = −Q̇₀`. Ecs. (40)–(41): `P_s = A_s (k/k⋄)^{n_s−1}`, **`A_s = H⋄²/(8π² ε₁⋄ M_P²)` (sin el factor 3^{3/2})**, `n_s = 1−2ε₁⋄−ε₂⋄`. **Eq. (42): `r = 16 ε₁⋄`**, dada sin derivación; el texto la respalda con "In Ref. [45] it was shown in detail that the theoretical predictions… are exactly the same as in standard (single field slow-roll) inflation", y `[45]` = A1, que no contiene sector tensorial. Ec. (44): `ε₁(N)=(1+N_f−N)^{−γ}` (escenario 1). Los escenarios 2–3 y el contraste con Planck no fueron verificados por mí. | https://arxiv.org/abs/2307.06329 · DOI 10.1093/mnras/stad2095 | **T-parcial** (Sec. II–III, Eqs. 38–45) |
| A3 | G. R. Bengochea, G. León, A. Perez, D. Sudarsky, "A clarification on prevailing misconceptions in unimodular gravity", *JCAP* **11** (2023) 011. arXiv:2308.07360v2. | Sec. 3.1: "if one assumes ∇ₐTᵃᵇ = 0, then, in practice UG is equivalent to GR"; Λ es constante de integración. Eq. (2.14): no-conservación permitida (UG con `Q`). Eq. (5.10): a primer orden la perturbación tensorial es invariante de gauge, `χH_ij = γH_ij` (los escalares y vectores no lo son). Conclusiones: `√−g = 1` es una elección de coordenadas, no la restricción genuina. Su lista de referencias apunta a Fabris et al. (C4) como trabajo sobre GW en UG no conservativa. | https://arxiv.org/abs/2308.07360 · DOI 10.1088/1475-7516/2023/11/011 | **T-parcial** (Sec. 3.1, 5, conclusiones, refs.) |

---

## 2. Fundacionales: formulaciones de UG y equivalencia clásica con RG

| # | Cita completa | Qué se toma | Link / DOI | Verif. |
|---|---|---|---|---|
| B1 | M. Henneaux, C. Teitelboim, "The cosmological constant and general covariance", *Phys. Lett. B* **222**, 195–199 (1989). | Formulación con densidad vectorial `τ^μ`: `S_HT = ∫d⁴x [ √−g R/(16πG) − λ(√−g − ∂_μ τ^μ) ]`; Λ aparece como constante de integración y la teoría es completamente covariante. **Forma de la acción verificada vía Padilla–Saltas Eq. (3) (B5)**, no en el original. Abstract: la constante cosmológica es constante de integración; un grado de libertad global extra. | DOI 10.1016/0370-2693(89)91251-3 · ADS 1989PhLB..222..195H | **X** (original no accedido; acción vía B5 = T) |
| B2 | W. G. Unruh, "Unimodular theory of canonical quantum gravity", *Phys. Rev. D* **40**, 1048–1052 (1989). | Referencia canónica de la formulación Hamiltoniana/cuántica de UG. Ecuación específica: **pendiente de leer**. | DOI 10.1103/PhysRevD.40.1048 | **X** |
| B3 | S. Weinberg, "The cosmological constant problem", *Rev. Mod. Phys.* **61**, 1–23 (1989). | Contexto: por qué UG suele motivarse desde el problema de Λ (citado como [1] en C4 y por B5). Sección específica sobre UG: **pendiente de leer**. | DOI 10.1103/RevModPhys.61.1 | **X** |
| B4 | J. L. Anderson, D. Finkelstein, "Cosmological constant and fundamental length", *Am. J. Phys.* **39**, 901–904 (1971); Y. J. Ng, H. van Dam, "Unimodular theory of gravity and the cosmological constant", *J. Math. Phys.* **32**, 1337–1340 (1991). | Antecedentes históricos de la formulación con `√−g` fijo. No leídos. | DOI 10.1119/1.1986321 · DOI 10.1063/1.529283 | **X** |
| B5 | A. Padilla, I. D. Saltas, "A note on classical and quantum unimodular gravity", *Eur. Phys. J. C* **75**, 561 (2015). arXiv:1409.3573. | Eq. (1): `S = ∫d⁴x [√−g R/(16πG) − λ(x)(√−g − ε₀)] + S_m`; ecs.: Einstein con un término `∝ λ(x) g_μν` (la normalización exacta no pude confirmarla en el texto extraído, que sale desordenado) y `√−g = ε₀`; traza ⇒ `λ = ½(R + 8πG T)`; si `S_m` es Diff-invariante hay conservación de `T` ⇒ `∂_μλ = 0`, `λ = λ₀` y la dinámica es la de RG con Λ = λ₀/2. Eq. (3): acción de HT (B1). Conclusión (abstract): "classically, unimodular gravity is simply a gauge fixed version of GR… identical dynamics and physical predictions". Alcance: **caso conservativo**; el trabajo no trata perturbaciones tensoriales ni difusión. | https://arxiv.org/abs/1409.3573 · DOI 10.1140/epjc/s10052-015-3767-0 | **T-parcial** (Sec. 2, Eqs. 1 y 3, abstract) |
| B6 | G. F. R. Ellis, H. van Elst, J. Murugan, J.-P. Uzan, "On the trace-free Einstein equations as a viable alternative to general relativity", *Class. Quantum Grav.* **28**, 225007 (2011). arXiv:1008.1196. | Ecuaciones de Einstein sin traza + conservación de `T` impuesta como hipótesis independiente ⇒ equivale a RG con Λ como constante de integración; discute que no resuelve el valor de Λ. Una búsqueda de texto en el PDF no encontró tratamiento de ondas gravitacionales, modos tensoriales ni perturbaciones (no es la fuente para el sector TT). | https://arxiv.org/abs/1008.1196 · DOI 10.1088/0264-9381/28/22/225007 | **A** (+ búsqueda de texto negativa) |
| B7 | G. F. R. Ellis, "The trace-free Einstein equations and inflation", *Gen. Relativ. Gravit.* **46**, 1619 (2014). arXiv:1306.3021. | Con ecuaciones sin traza, la inflación con inflatón procede como en RG (el potencial efectivo se desplaza por Λ constante); las ecuaciones slow-roll se reproducen. No trata espectro tensorial (búsqueda de texto: sin "tensor modes"/"gravitational waves"). | https://arxiv.org/abs/1306.3021 · DOI 10.1007/s10714-013-1619-5 | **A** (+ búsqueda de texto negativa) |
| B8 | R. Carballo-Rubio, L. J. Garay, G. García-Moreno, "Unimodular gravity vs general relativity: a status report", *Class. Quantum Grav.* **39**, 243001 (2022). arXiv:2207.08499v2. | Revisión. Sec. II.A: teoría lineal `Fierz-Pauli` (`ξ₁=ξ₂=ξ₃=0`) = RG linealizada; `WTDiff` (`ξ₁=0, ξ₂=−1/2, ξ₃=−5/8`) = UG linealizada; Sec. II.B: no-linealidades. Conclusión (abstract): "Apart from the completely different treatment they provide for the cosmological constant, our results uncover no further differences between them." | https://arxiv.org/abs/2207.08499 · DOI 10.1088/1361-6382/aca386 | **T-parcial** (abstract, Sec. II.A–B) |
| B9 | J. J. Lopez-Villarejo, "TransverseDiff gravity is to scalar-tensor as unimodular gravity is to General Relativity", *JCAP* **11** (2011) 002. arXiv:1009.1023. | Correspondencia TDiff ↔ escalar-tensor análoga a UG ↔ RG. Contexto para "qué cambia cuando se rompe Diff". | https://arxiv.org/abs/1009.1023 · DOI 10.1088/1475-7516/2011/11/002 | **A** |

---

## 3. Perturbaciones cosmológicas y sector tensorial en UG (núcleo de la pregunta)

| # | Cita completa | Qué se toma | Link / DOI | Verif. |
|---|---|---|---|---|
| C1 | A. Basak, O. Fabre, S. Shankaranarayanan, "Cosmological perturbations of unimodular gravity and general relativity are identical", *Gen. Relativ. Gravit.* **48**, 123 (2016). arXiv:1511.01805v1. | **Afirmación clave para (b)**, Conclusiones: "Because of the divergence-less and trace-less conditions, the vector and tensor modes are not affected by the unimodular constraint. Hence, the evolution of vector and tensor modes are also identical in UG and GR." Además: ecuaciones de fondo de UG y RG idénticas (abstract); Sachs–Wolfe y ecuación de Mukhanov–Sasaki de primer orden idénticas; "the only difference comes from the gauge choices". Alcance: materia conservada. | https://arxiv.org/abs/1511.01805 · DOI 10.1007/s10714-016-2116-4 | **T-parcial** (abstract, conclusiones) |
| C2 | C. Gao, R. H. Brandenberger, Y. Cai, P. Chen, "Cosmological perturbations in unimodular gravity", *JCAP* **09** (2014) 021. arXiv:1405.1644. | Sec. de perturbaciones: descomposición SVT, "which at linear order evolve independently"; solo analizan el sector escalar. Resultado (abstract): el vínculo `det g` restringe el gauge; la variable *shift* no puede ponerse a cero; afecta Sachs–Wolfe en escalas grandes. **Disputado por C1**, que lo atribuye a la elección de gauge. No trata tensores. | https://arxiv.org/abs/1405.1644 · DOI 10.1088/1475-7516/2014/09/021 | **T-parcial** (Sec. 3, abstract) |
| C3 | I. Cho, N. K. Singh, "Unimodular theory of gravity and inflation", *Class. Quantum Grav.* **32**, 135020 (2015). arXiv:1412.6205v2. | Eq. (11): acción generalizada `S_uni = ∫d⁴x √−ḡ [A² R̄ − ξ ∂A∂A]/(16πG)`; `ξ=6` ⇒ RG (Eq. 10). Sec. 5: "The action corresponding to the tensor perturbation is independent of the parameter ξ. Due to the traceless property of the tensor perturbation, √−g is fixed up to the linear order, and thus it does not affect the equation of the tensor perturbation". **Eq. (62): `P_T` idéntico al estándar** (`≈ 64πG (H/2π)²`). Eq. (63): `r = P_T/P_R ≈ 16 ε₁` modificado respecto de RG solo a través del fondo (`ε₁(δ)`, `δ=ξ−6`); con `r ≤ 0.09` obtienen `ξ ≲ 5.57`. **Ojo**: es una UG *modificada* (`ξ≠6`), no la UG estándar. | https://arxiv.org/abs/1412.6205 · DOI 10.1088/0264-9381/32/13/135020 | **T-parcial** (Sec. 2, 5, 6) |
| C4 | J. C. Fabris, M. H. Alvarenga, M. Hamani Daouda, H. Velten, "Nonconservative unimodular gravity: gravitational waves", *Symmetry* **14**, 87 (2022). arXiv:2112.06663v1. | **Único paper encontrado que estudia GW en UG no conservativa.** Sec. "Gravitational waves": `g = g^B + h`; síncrono `h_{μ0}=0`; la perturbación de la condición unimodular da `h^k_k = 0` (Eq. 34), "already encoded in the condition to have pure tensorial modes". **Eq. (37): `ḧ_ij − H ḣ_ij − 2(Ḣ+H²) h_ij + (k²/a²) h_ij = 0`**, "exactly the equation for gravitational waves in GR with a perfect fluid". Diferencias solo por el fondo: "the expressions for the background functions H and Ḣ are not the same". El fondo UG solo ve `ρ+p`. Limitaciones que declaran: análisis "fundamentally qualitative"; el modelo requiere una condición adicional (ansatz) para cerrar las ecuaciones. Comprobación manual mía: con `h_ij = δg_ij = a² h^{std}_ij`, la Ec. (37) equivale a `ḧ^{std}+3Hḣ^{std}+(k²/a²)h^{std}=0` (ver Punto abierto O3). | https://arxiv.org/abs/2112.06663 · DOI 10.3390/sym14010087 | **T-parcial** (Sec. GW, conclusiones) |
| C5 | I. Chakraborty, S. Jana, S. Mohanty, "Gravitational radiation from binary systems in unimodular gravity", *JCAP* **02** (2025) 027. arXiv:2409.02909v3. | Eq. (19): suma de polarizaciones de gravitones spin-2 sin masa = la de RG; texto: la acción de Fierz–Pauli se deduce sin usar conservación de `T`, "Hence… the Fierz-Pauli action is restored". Eqs. (21)–(23): con difusión, la condición sobre la fuente pasa a `k^μ(T_μν − g_μν Q) = 0`; el abstract habla de "dispersion relation is modified" (ver O4). Cota `|ζ| ≤ 5×10⁻⁴` con púlsares binarios. Contexto: emisión sobre fondo plano, no espectro primordial. | https://arxiv.org/abs/2409.02909 · DOI 10.1088/1475-7516/2025/02/027 | **T-parcial** (Sec. 2–3, Eqs. 18–23) |
| C6 | M. H. Alvarenga, J. C. Fabris, H. Velten, "Using cosmological perturbation theory to distinguish between General Relativity and Unimodular Gravity", *Symmetry* **15**, 1392 (2023). arXiv:2301.12464. | Solo abstract: análisis de perturbaciones escalares clásicas; "the equivalence is not verified completely at perturbative level". **Disenso con C1** (sector escalar). No trata tensores. | https://arxiv.org/abs/2301.12464 · DOI 10.3390/sym15071392 | **A** |
| C7 | F. X. Linares Cedeño, U. Nucamendi, "Gauge fixing in cosmological perturbations of Unimodular Gravity", *JCAP* **10** (2023) 036. arXiv:2307.04873. | Solo abstract: gauges newtoniano y síncrono en UG; el vínculo unimodular restringe los escalares métricos a un solo grado de libertad; ninguno recupera la dinámica de RG para materia y métrica. Sector escalar. | https://arxiv.org/abs/2307.04873 · DOI 10.1088/1475-7516/2023/10/036 | **A** |
| C8 | M. de Cesare, E. Wilson-Ewing, "Interacting dark sector from the trace-free Einstein equations: cosmological perturbations with no instability", *Phys. Rev. D* **106**, 023527 (2022). arXiv:2112.12701. | Solo abstract: ecuaciones de perturbaciones lineales de TFE con transferencia de energía, "focusing on the scalar sector". No trata tensores. | https://arxiv.org/abs/2112.12701 · DOI 10.1103/PhysRevD.106.023527 | **A** |
| C9 | J. C. Fabris, A. Yu. Kamenshchik, "Generalized unimodular gravity and cosmological perturbations", arXiv:2606.16378 (jun 2026), sin publicar. | Solo abstract: UG generalizada; análisis de fondo y perturbativo "recovering the corresponding results obtained through the general relativity theory but with a different interpretation". Es el más reciente sobre perturbaciones; **leer completo**. | https://arxiv.org/abs/2606.16378 · DOI 10.48550/arXiv.2606.16378 | **A** |

---

## 4. Inflación en UG (variantes)

| # | Cita completa | Qué se toma | Link / DOI | Verif. |
|---|---|---|---|---|
| D1 | A. O. Barvinsky, N. Kolganov, "Inflation in generalized unimodular gravity", *Phys. Rev. D* **100**, 123510 (2019). arXiv:1908.05697v1. | UG **generalizada** (GUMG: agrega un gravitón escalar, 3 dof). Eq. (4.8): `S_t = (M_P²/8)∫dη d³x √σ a² [(t'_ij)² − (∇_k t_ij)² − 2k t_ij²]`: "the action of two graviton oscillators on the nonstatic Friedmann background", es decir, el sector tensorial tiene la forma de RG. Ecs. (5.18)–(5.20): espectro tensorial, `n_t`, y `r` que cambia respecto de RG **solo por el sector escalar** (depende de `c_s` y `1+w` del fluido efectivo); para `c_s=1` coincide con el modelo con inflatón. **No es UG estándar.** | https://arxiv.org/abs/1908.05697 · DOI 10.1103/PhysRevD.100.123510 | **T-parcial** (Sec. 4, 5) |
| D2 | A. O. Barvinsky, N. Kolganov, A. Vikman, "Generalized unimodular gravity as a form of k-essence", *Phys. Rev. D* **103**, 064035 (2021). arXiv:2011.06521. | Solo abstract: GUMG covariantizada es equivalente a k-esencia; UMG (estándar) como caso particular. | https://arxiv.org/abs/2011.06521 · DOI 10.1103/PhysRevD.103.064035 | **A** |

---

## 5. UG no conservativa (difusión `Q`): motivación y fondo

| # | Cita completa | Qué se toma | Link / DOI | Verif. |
|---|---|---|---|---|
| E1 | D. Josset, A. Perez, D. Sudarsky, "Dark energy from violation of energy conservation", *Phys. Rev. Lett.* **118**, 021102 (2017). arXiv:1604.04183. | Abstract: en UG la no-conservación de `T` (modificaciones no unitarias de la MC o modelos de discretización del espacio-tiempo) genera un Λ efectivo. Origen del "término de difusión". PDF descargado, no leído. | https://arxiv.org/abs/1604.04183 · DOI 10.1103/PhysRevLett.118.021102 | **A** |
| E2 | A. Perez, D. Sudarsky, "Dark energy from quantum gravity discreteness", *Phys. Rev. Lett.* **122**, 221302 (2019). arXiv:1711.05183v4. | Metadatos verificados; contenido no leído. Motivación microfísica de `Q`. | https://arxiv.org/abs/1711.05183 · DOI 10.1103/PhysRevLett.122.221302 | **A** (solo metadatos) |
| E3 | S. J. Landau, M. Benetti, A. Perez, D. Sudarsky, "Cosmological constraints on unimodular gravity models with diffusion", *Phys. Rev. D* **108**, 043524 (2023). arXiv:2211.07424. Comentario crítico: M. Cataldo, arXiv:2604.17523 (2026). | Abstract: fondo cosmológico con difusión contrastado con datos. Cataldo: la segunda ley exige `Q̇ < 0` (leído solo el abstract). | https://arxiv.org/abs/2211.07424 · DOI 10.1103/PhysRevD.108.043524 · https://arxiv.org/abs/2604.17523 | **A** |
| E4 | J. C. Fabris, M. H. Alvarenga, M. Hamani-Daouda, H. Velten, "Nonconservative unimodular gravity: a viable cosmological scenario?", *Eur. Phys. J. C* **82**, 522 (2022). arXiv:2112.06644. | Metadatos verificados; contexto de fondo (C4 usa este modelo). No leído. | https://arxiv.org/abs/2112.06644 · DOI 10.1140/epjc/s10052-022-10470-2 | **A** (solo metadatos) |
| E5 | Y. Bonder, J. E. Herrera, A. M. Rubiol, *Phys. Rev. D* **107**, 084032 (2023), arXiv:2211.06532; C. Corral, N. Cruz, E. González, *Phys. Rev. D* **102**, 023508 (2020), arXiv:2005.06052; M. Daouda et al., *Int. J. Mod. Phys. D* **28**, 1950175 (2019), arXiv:1802.01413; P. Pellecchia, A. Perez, S. Ribisi, arXiv:2607.03272 (jul 2026). | Fondo/fenomenología de difusión. Solo metadatos y abstracts (Pellecchia et al.: modelo disipativo primordial). No leídos. | (arXiv IDs listados) | **A** |
| E6 | Otros (no relevantes para TT, listados para completitud): M. Malekpour, K. Nozari, arXiv:2404.12099 (*PTEP* 2024); Malekpour et al., arXiv:2608.20095 (*Phys. Dark Univ.* **43**, 101405); K. Bamba, S. D. Odintsov, E. N. Saridakis, arXiv:1605.02461 (*Mod. Phys. Lett. A* **32**, 1750114); K. Nozari, S. Shafizadeh, arXiv:1712.09522 (*IJMPD* **26**, 1750107); S. Gielen, R. B. Neves, arXiv:2607.27344; M. De Angelis, J. Rubio, arXiv:2607.16405; D. Blas, M. Shaposhnikov, D. Zenhäusern, arXiv:1104.1392. | Inflación con campo escalar dentro de UG o en variantes. **No verifiqué qué dicen de tensores.** Nota: los metadatos de 2608.20095 son inconsistentes (arXiv agosto 2026, revista 2024). | (arXiv IDs listados) | **A** (solo metadatos/abstract) |
| E7 | TDiff (rompen Diff en el sector de materia, no en gravedad): A. L. Maroto, *JCAP* **04** (2024) 037, arXiv:2301.05713; D. Jaramillo-Garrido, A. L. Maroto, P. Martín-Moruno, *JHEP* **03** (2024) 084, arXiv:2307.14861; A. L. Maroto, P. Martín-Moruno, D. Tessainer, arXiv:2605.18424 (2026). | Abstract 2605.18424: perturbaciones cosmológicas de campos TDiff, con presión no adiabática y velocidad del sonido efectiva. Contexto sobre qué cambia al romper Diff (sector escalar). No verifiqué tratamiento de tensores. | DOI 10.1088/1475-7516/2024/04/037 · DOI 10.1007/JHEP03(2024)084 | **A** |
| E8 | A. Álvarez, D. Blas, J. Garriga, E. Verdaguer, "Transverse Fierz–Pauli symmetry", *Nucl. Phys. B* **756**, 148–170 (2006). | Teoría lineal invariante bajo TDiff. Contexto para B8. No leído. | DOI 10.1016/j.nuclphysb.2006.08.003 | **X** |

---

## 6. Referencias de RG estándar (objetivo de la comparación; se usan en la etapa de derivación)

| # | Cita completa | Qué se tomará | Link / DOI | Verif. |
|---|---|---|---|---|
| F1 | V. F. Mukhanov, H. A. Feldman, R. H. Brandenberger, "Theory of cosmological perturbations", *Phys. Rep.* **215**, 203–333 (1992). (PDF en la carpeta del director: `mukhanov_physics_reports.pdf`.) | Ecuación de propagación de los modos TT en FLRW y espectro tensorial estándar. **Ecuaciones específicas: pendiente de localizar y numerar.** | DOI 10.1016/0370-1573(92)90044-Z | **X** (título verificado, no leído) |
| F2 | D. Baumann, "TASI lectures on inflation", arXiv:0907.5424. D. Baumann, *Cosmology* (Cambridge Univ. Press, 2022) (PDF en la carpeta). | Cálculo completo de espectros escalar y tensorial (abstract: "in full detail the famous calculation for the primordial spectra of scalar and tensor fluctuations"). Ecuaciones: pendiente. | https://arxiv.org/abs/0907.5424 | **A** |
| F3 | J. Garriga, V. F. Mukhanov, "Perturbations in k-inflation", *Phys. Lett. B* **458**, 219–225 (1999). hep-th/9904176. | Teoría de perturbaciones para `P(X)` y fluidos hidrodinámicos: sirve para chequear cómo entra la velocidad del sonido en `P_R` (ver O5). | https://arxiv.org/abs/hep-th/9904176 · DOI 10.1016/S0370-2693(99)00602-4 | **A** |
| F4 | Planck Collaboration, "Planck 2018 results. X. Constraints on inflation", *Astron. Astrophys.* **641**, A10 (2020). arXiv:1807.06211 (PDF v1 en la carpeta). | `r₀.₀₀₂ < 0.10` (Planck solo) y `r₀.₀₀₂ < 0.064` (Planck + BK14), ambos 95% CL — texto del abstract verificado en el PDF. | https://arxiv.org/abs/1807.06211 | **T-parcial** (abstract) |
| F5 | BICEP/Keck Collaboration, "BICEP/Keck XIII: Improved constraints on primordial gravitational waves using Planck, WMAP, and BICEP/Keck observations through the 2018 observing season", *Phys. Rev. Lett.* **127**, 151301 (2021). arXiv:2110.00483. | `r₀.₀₅ < 0.036` (95% CL): cota más fuerte que la de F4; usar para la comparación. | https://arxiv.org/abs/2110.00483 · DOI 10.1103/PhysRevLett.127.151301 | **A** (abstract) |
| F6 | C. Caprini, D. G. Figueroa, "Cosmological backgrounds of gravitational waves", *Class. Quantum Grav.* **35**, 163001 (2018). arXiv:1801.04268 (PDF en la carpeta). | Paso de `P_t` a `Ω_GW` (fondo estocástico). Ecuaciones: pendiente. | https://arxiv.org/abs/1801.04268 · DOI 10.1088/1361-6382/aac608 | **X** (título verificado, no leído) |
| F7 | Otros PDFs de la carpeta del director, identificados pero no leídos: K. Malik, D. Wands, "Cosmological perturbations" (arXiv:0809.4944); K. Malik, D. Matravers, "A concise introduction to perturbation theory in cosmology" (arXiv:0804.3276); J. Martin, C. Ringeval, V. Vennin, "Encyclopædia Inflationaris" (arXiv:1303.3787v3); V. Mukhanov, *Physical Foundations of Cosmology* (2005); E. Poisson, *An Advanced Course in GR*. | Fondo. | | **X** |

---

## 7. Puntos abiertos detectados durante la lectura (para verificar en la etapa de derivación)

Ninguno está resuelto. Están anotados porque un resultado sin su check no cuenta.

| ID | Observación | Evidencia | Qué habría que hacer |
|---|---|---|---|
| **O1** | El factor `3^{3/2}` aparece en `P_R` de León (A1, Eq. 66) y no aparece en `A_s` de Piccirilli–León (A2, Eq. 41), cuyo texto dice basarse en A1. | Ambas ecuaciones leídas en el PDF. | Rederivar `P_R` con `c_s²=1/3` y decidir cuál es correcta (o si dependen de la definición de `z`, Eq. 59 de A1). |
| **O2** | `r = 16 ε₁` (A2, Eq. 42) se adopta sin derivar; A1, la referencia que la respalda, no contiene sector tensorial. Si además `P_t` fuera el de RG (`2H²/(π²M_P²)`), aritméticamente A1 Eq. 66 daría `r = P_t/P_R = 16 ε₁/3^{3/2} ≈ 3.1 ε₁`, no `16 ε₁`. **Es una hipótesis por aritmética sobre ecuaciones publicadas, no un resultado verificado.** | Búsqueda de texto en A1 (sin "tensor"/"graviton"/"ratio"); A2 Eq. 42 y su cita a [45]. | Derivar `P_t` en UG con difusión desde la acción de segundo orden y calcular `r` de forma consistente. **Es el corazón del proyecto.** |
| **O3** | Fabris et al. Eq. (37) parece distinta de `ḧ+3Hḣ+k²/a² h=0`. Chequeo a mano: con `h_ij ≡ δg_ij = a² h^{std}_ij` reproduce exactamente la forma estándar; no hay discrepancia, pero **está hecho a mano, no simbólicamente**. | Ec. (37) leída; álgebra manual: `ḧ^{std}=[ḧ−4Hḣ−2Ḣh+4H²h]/a²`. | Reproducir con SymPy y guardar el script como evidencia. |
| **O4** | Chakraborty et al. dicen "dispersion relation is modified", pero su suma de polarizaciones (Eq. 19) es la de RG. Mi lectura: lo que cambia es la condición de transversalidad de la *fuente* (`k^μ(T_μν − g_μν Q) = 0`, Eq. 21), no la propagación libre de TT. **Interpretación mía, sin confirmar.** | Eqs. 19, 21–23 leídas. | Confirmar con el texto completo (Sec. 2) antes de citar. |
| **O5** | Hipótesis sobre O1: para un fluido con velocidad del sonido `c_s`, el resultado estándar es `P_R = H²/(8π² M_P² ε c_s)` `[M]` (Garriga–Mukhanov, F3), que para `c_s²=1/3` daría `3^{1/2}` y no `3^{3/2}`. **No verificado contra el texto de F3.** | — | Verificar en F3 y contrastar con la definición de `z` en A1 Eq. (59) (¿falta un `1/c_s`?). |
| **O6** | Hay disenso publicado en el **sector escalar** (C2, C6, C7 vs. C1). Ningún paper que leí encuentra diferencias en el sector TT. | Abstracts y C1/C3/C4/D1. | Registrar en el trabajo que el disenso es escalar y no afecta a (b). |
| **O7** | Alcance de la búsqueda: buscador web (solo EE. UU.) + API de arXiv por palabras clave + bibliografía de A1–A3 y C4. Puede haber omisiones, sobre todo en revistas sin arXiv. | — | Repetir con INSPIRE/ADS al empezar la derivación. |
| **O8** | El apunte previo en esta carpeta (`gravedad_unimodular_inflacion.tex/.pdf`, 19-sep) cita A1–A3 y **no** tiene registro de provenance. Contrastado en esta etapa: Eq. 41, 42 y 66 (y el factor `3^{3/2}`) coinciden con los PDFs; falta el dato de revista de A3 (JCAP 11 (2023) 011) y no cubre la literatura de tensores. **No lo modifiqué.** Las demás afirmaciones del apunte (escenarios 2–3, `α`, `N_f`, tabla de Piccirilli–León) no fueron contrastadas aquí. | — | Decidir si se reutiliza; si sí, verificarlo línea por línea. |

---

## 8. Registro de cómo se obtuvo cada cosa

| Qué | Cómo | Dónde |
|---|---|---|
| Descubrimiento de candidatos | `WebSearch` + consultas a la API de arXiv | `literatura_tools/arxq.py` |
| Abstracts y metadatos arXiv | API de arXiv por id | `literatura_tools/arxabs.py` |
| Revista/volumen/DOI | API de Crossref, `query.bibliographic` | `literatura_tools/cr.py` |
| Texto de los PDFs | `pdftotext` (con y sin `-layout`) + `grep`/lectura de contexto | (temporales en la sesión; reproducibles con las URLs de las tablas) |
| Ecuaciones citadas | Lectura directa del texto extraído (ver columna Verif.) | — |

Limitación conocida de `pdftotext`: las ecuaciones salen desordenadas; las que cito arriba las reconstruí leyendo el contexto y no son copia literal, salvo las entrecomilladas.

---

## 9. Etapa numérica (código): qué función implementa qué ecuación de `derivation.md`

Fecha: 2026-09-20. Carpeta: `codigo/`. **Estado: corre y tiene checks (sec. 10, 10/10 pasan).** *[Histórico: estos números quedaron registrados después en `numbers.json`/`claims.yaml`, sec. 15.]*

**Entorno:** Python 3.12.3 (anaconda), numpy 1.26.4, scipy 1.13.1, matplotlib 3.9.2. Correr: `cd codigo && python3 run_spectrum.py` (~2 s). Salidas en `codigo/resultados/` (`PT_k.npz`, `PT_k.csv`, `PT_k.png`, `fondo.png`). Sin semillas aleatorias: el cálculo es determinista.

### 9.1 Decisiones (con su origen)

| Decisión | Valor | Origen |
|---|---|---|
| Acoplamiento de `Q` | solo al inflatón, ec. (2.9) (opción (a)). Con un solo campo es el único consistente con (2.7)–(2.8) | Usuario, 2026-09-20 |
| Forma de `Q` | `Q(N) = Q_i·exp(−γN)`, `N = ln(a/a_i)`, `Q_i/V(φ_i) = 0.1`, `γ = 0.1` | Usuario (recomendada) |
| Potencial y masa | `V = ½m²φ²`, `m = 6×10⁻⁶ M_P`. **Valor de m: verificado en C1.3** (reproduce `A_s` de Planck dentro de +3.2 % a `N_*=60` con la fórmula slow-roll escalar estándar; el sector escalar no está derivado). Solo escala la amplitud | Usuario (recomendada) |
| Definición de `P_T` | varianza de `h_ij h_ij`: `P_T = (k³/2π²)·2·Σ_λ|h_λ|²`, `e·e = 2`, `v = aM_P h/√2`, Bunch–Davies | Usuario (recomendada) |
| Condiciones iniciales | mismo `φ_i`, `φ̇_i`, `H_i` en RG y UG; `Λ₀` por (2.11) (sale `Λ₀ = −Q_i`) | Usuario (recomendada) |
| Duración de la inflación | **`N_f = 100` e-folds en UG**; `φ_i` se obtiene por raíz (`background.py::phi_i_for_ug_duration`) → `φ_i = 25.386 M_P`. RG usa el mismo `φ_i` y por eso dura más (161.8) | Usuario: «el más usual en UG». Valor tomado de A2 y A1 (ver abajo) |
| Mismas condiciones iniciales en RG y UG | `φ_i`, `φ̇_i`, `H_i` idénticos (confirmado por el usuario 2026-09-20). Consecuencia: `ε₁` de UG hace un salto inicial porque `φ̇_i` de RG no está en el atractor de UG; se deja así | Usuario |
| `φ̇_i` | slow-roll de RG: `−V'/√(3V)` (2.14 con Q=0, Λ=0), igual en ambos modelos | **Mío, por defecto** |
| `k/(aH)` inicial = 100 y final = 10⁻³ | modo dentro/fuera del horizonte | **Mío, por defecto** |
| 40 modos, equiespaciados en ln k, mismo `k` comóvil en RG y UG (`a_i = 1`) | rango: de `k/aH = 100` a `N=0` hasta `k/aH = 10⁻³` al fin de la inflación del modelo más corto | **Mío, por defecto** |
| Tolerancias | fondo `rtol=1e-12, atol=1e-14`; modos `rtol=1e-10, atol=1e-12`; DOP853 | **Mío, por defecto** |
| Unidades | `M_P = 1` (κ=1) y `m = 1`; `m_phys` multiplica `P_T` al final (`P_T ∝ H²/M_P²`). Exacto por homogeneidad de (2.7), (2.9), (3.9), (4.8) bajo `t→t/m` | Mío (argumento en `config.py`) |

**Fuente de `N_f = 100`** (textos leídos con `pdftotext` de las copias de la carpeta del director; lectura parcial, solo las frases citadas y su contexto):
- A2 (Piccirilli–León, arXiv:2307.06329v1), Sec. III, tras Eq. (44): «where `N_f ≥ 65`, as usual». Escenario 1: «The total number of e-folds of inflation here is taken to be `N_f = 100`»; el escenario 3 usa `N_f ≃ 370`.
- A1 (León, arXiv:2202.04029v2), Sec. III, tras Eq. (34): «Fig. 1-left we have used `N_f = 70`. Recall that a minimum of `N_f ∼ 60-70` is required for solving the horizon and flatness problems», y otra figura con `N_f = 300`. Antes, en el texto de la condición (19): «at least for a minimum of `N_min ≃ 102` e-folds».
- Criterio mío: 100 es el único valor que aparece en los dos papers (A2 escenario 1; `N_min ≃ 102` en A1) y cumple el mínimo `≥ 65`. Alternativas defendibles: 70 (ilustración de A1) o ≥ 65 sin más. Es fácil de cambiar (`Params.N_f_ug`).

### 9.2 Función → ecuación

`derivation.md` es la referencia; "Etiqueta" es la de esa ecuación allí.

| Archivo::función | Implementa | Etiqueta | Propio / librería |
|---|---|---|---|
| `background.py::V`, `dV` | potencial `V=½φ²` (m=1) | SUPUESTO (usuario) | propio |
| `background.py::rho_and_p` | (2.5) | ESTÁNDAR | propio |
| `background.py::Q_of_N`, `Qdot` | `Q(N)`; `Q̇ = (dQ/dN)·H` para el `Q̇` de (2.9) | SUPUESTO (usuario) | propio |
| `background.py::hubble_rg` | (2.10), 1.ª ecuación | ESTÁNDAR | propio |
| `background.py::hubble_ug` | (2.7) | PROPIA | propio |
| `background.py::lambda0_from_initial` | (2.11) | PROPIA (= A1 Eq. 12) | propio |
| `background.py::tensor_mass_term` | (4.6): `X = −3H²−2Ḣ−κp+λ̄` | PROPIA | propio |
| `background.py::quantities_rg` | (2.10) 3.ª ecuación (KG) y derivada temporal de (2.10) | ESTÁNDAR | propio |
| `background.py::quantities_ug` | (2.9) y derivada temporal de (2.7) | PROPIA | propio |
| `background.py::initial_state` | (2.11); `φ̇_i` de slow-roll (2.14) | PROPIA + SUPUESTO | propio |
| `background.py::_solve` | integra `(φ̇, φ̈, Ṅ=H)`; evento `ε₁=1` con `ε₁` de la Sec. 2.7 | PROPIA (definición 2.7) | `scipy.integrate.solve_ivp` (DOP853, eventos, `dense_output`) |
| `background.py::solve_background_rg` / `_ug` | fondo de RG (2.10) / de UG (2.7)+(2.9) | — | propio |
| `background.py::phi_i_for_ug_duration` | ajusta `φ_i` para que `N_end(UG) = N_f` (no hay ecuación nueva) | SUPUESTO (usuario) | propio; `scipy.optimize.brentq` |
| `modes.py::mode_rhs` | (3.11) con el término de masa de (4.6), escrita en `N` (ver 9.3, n1–n2) | PROPIA | propio |
| `modes.py::bunch_davies_ic` | condición inicial de Bunch–Davies para (4.8) (ver 9.3, n5) | ESTÁNDAR / SUPUESTO | propio |
| `modes.py::tensor_power` | (4.6) + definición de `P_T` de P2 corregida (ver 9.3, n4) | ESTÁNDAR | propio |
| `modes.py::_horizon_crossing_N` | cruce `k/(aH) = cte` | — | `scipy.optimize.brentq`, `scipy.interpolate.CubicSpline` |
| `modes.py::run_mode` / `run_all_modes` | integra un modo / todos (paralelo) | — | `solve_ivp` (DOP853, complejo), `ProcessPoolExecutor` |
| `run_spectrum.py::k_grid`, `main` | malla de `k` común; orquestación; figuras | — | numpy, matplotlib |

**Diseño respecto de "no asumas el resultado":** RG y UG tienen fondo separado (`quantities_rg` vs `quantities_ug`); ninguna usa (2.8), `Ḣ` sale de derivar la ecuación de Friedmann de cada modelo. El término de masa `X` se calcula con el `λ̄` de cada modelo (`Λ` en RG, `Λ₀+Q(t)` en UG) y **entra** en la ecuación de modos. La rutina de integración de modos es una sola y no conoce `Q`.

### 9.3 Pasos que el código usa y que `derivation.md` NO tiene escritos (pendientes de incorporar si el usuario los aprueba)  *[Histórico: los pasos n1–n5 se usan tal cual en el código y se registran en la sec. 9; su incorporación a `derivation.md` sigue sin hacerse.]*

| ID | Paso | Cómo se obtiene | Estado |
|---|---|---|---|
| n1 | Ecuación de modos **con** el término de masa: `ḧ_k + 3Hḣ_k + (k²/a² − 2X)h_k = 0` | Variar `L = (1/8κ)[a³ḣ² − a(∂h)² + 2a³X h²]`, que es (4.7) más el término de (4.6). Con `X=0` da (3.9) | PROPIA, a mano, no está en `derivation.md` |
| n2 | Forma en `N`: `w_N + (1−ε₁)w + [k²/(aH)² − (2−ε₁) − 2X/H²]v = 0`, `w = dv/dN`, usando `a''/a = a²H²(2−ε₁)` | de (3.11) con masa, `dN = aH dη`, `d(aH)/dN = aH(1−ε₁)`; `a''/a = ℋ'+ℋ²` (H6) | PROPIA, a mano |
| n3 | `6HḢ = φ̇(φ̈+V') + Q̇` | derivada temporal de (2.7) (mismo paso que "Continuidad" de la Sec. 2.4) | PROPIA |
| n4 | `P_T = 2k²|ṽ|²/(π²a²)` con `ṽ = √(2k) v` (M_P=1) | de `P_T = (k³/2π²)·2·Σ_λ|h_λ|²`, `h_λ = √2 v/a`, dos polarizaciones iguales | ESTÁNDAR; en de Sitter da `2H²/(π²M_P²)` (**sin verificar**) |
| n5 | Bunch–Davies adiabático: `v = e^{−i∫ω dη}/√(2ω)`, `ω² = k² − a''/a − 2Xa²`, `v' = −iωv` | WKB de orden cero (se desprecia `ω'`, error ~`(aH/k)³ ~ 10⁻⁶` con ratio 100) | **ESTÁNDAR/SUPUESTO; es el punto P2 que `derivation.md` deja pendiente** |

Corrección hecha en `derivation.md`/`.tex`/`.pdf` (fila P2 de la Sec. 8): la fórmula de `P_t` omitía el factor `e·e = 2` y daba la mitad del valor estándar `2H²/(π²M_P²)`. No cambia ninguna ecuación numerada (comparadas las 43 con la versión previa).

### 9.4 Corrida de humo (2026-09-20, con `N_f(UG) = 100`) y límites

- Corre completa en ~3 s (ajuste de `φ_i` + fondo RG y UG + 40 modos × 2) y es determinista. Resultados en `codigo/resultados/`. **Verificado en la sec. 10** (con los límites de 10.6).
- Observación cruda, sin interpretar: `φ_i = 25.386 M_P`; `N_end` = 161.8 (RG) y 100.000 (UG); `Λ₀ = −Q_i = −32.2` (unidades m=M_P=1); rango de `k` de 86 e-folds (limitado por UG); `P_T^UG/P_T^RG` va de ~0.94 a ~0.42 en ese rango; `ε₁` de UG salta en el primer e-fold (ver 9.1).
- La corrida anterior con `φ_i = 17` (UG 45.6 e-folds) se descartó por dar menos e-folds que los usuales en UG.
- Los diagnósticos que imprime `run_spectrum.py` (`max|X/H²|`, `max|Ḣ + φ̇²/2|`, ~10⁻¹⁵) **no son checks** (los checks reales de (2.8) están en C3.2, sobre la solución integrada): con `Ḣ` construido como derivada de (2.7) y `φ̈` de (2.9), ambos se anulan algebraicamente para cualquier `Q(N)`; miden el redondeo, no la corrección del código.
- Por lo mismo, la ecuación de modos de UG y de RG resultan numéricamente idénticas como funciones de `(H, ε₁)`: toda la diferencia de `P_T` viene del fondo. Es lo que predice la derivación, pero este cálculo no la contrasta de forma independiente (ver 10.6).


### 9.5 Notebook (`codigo/explorador_PT.ipynb`)

Notebook autocontenido para que el usuario corra y grafique. El código de `config.py`, `background.py`, `modes.py`, `checks.py` y `run_spectrum.py` va **verbatim** en celdas `%%writefile`; los `.py` siguen siendo la fuente de verdad citada en 9.2 y en la sec. 10. `codigo/make_notebook.py` lo genera y `codigo/test_notebook_sync.py` (5 tests) comprueba que el código embebido sea idéntico al de los `.py`. Las secciones 3–7 del notebook muestran lo que está verificado en la sec. 10; la sección 8 (barrido de `γ` y `Q_i/V_i`) es exploración **no verificada** y no se registra como resultado. Todo el notebook se ejecutó sin errores el 2026-09-20 (9 figuras, ~50 s).

---

## 10. Checks (etapa de verificación del cálculo numérico)

Fecha: 2026-09-20. **Resultado: 10/10 checks pasan.** Cada check es una función reproducible, no una verificación manual:

- Código: `codigo/checks.py` (funciones `check_*`, tolerancias y justificaciones en el docstring de cada una) y `codigo/test_checks.py` (pytest).
- Evidencia legible por máquina: `codigo/resultados/checks.json` (valores medidos, tolerancias, veredicto). Es determinista: dos corridas dan el mismo archivo salvo los tiempos.
- Reproducir: `cd codigo && python3 checks.py` (~1 min) o `python3 -m pytest -q test_checks.py` (~30 s). Entorno: Python 3.12.3, numpy 1.26.4, scipy 1.13.1.
- Parámetros de la corrida verificada: los de `config.py` con `φ_i = 25.386364 M_P` (UG dura `N_f = 100`; RG dura 161.8).

### 10.1 Política de tolerancias y cambios posteriores a la primera corrida

Las tolerancias se fijaron en el docstring de cada check **antes** de la primera corrida y **no se modificó ninguna después de ver resultados**. Lo que sí cambió tras la primera corrida (todo visible en el código):

1. **C3.3 falló la primera vez** (discrepancia ~10⁵⁸ en los modos de `k` grande). Causa: bug de escala en mi integrador independiente, no de física: `h ∼ 1/(a√ω)` llega a ~10⁻⁴⁰, muy por debajo de `atol=1e-12`, y el control de error dejaba de funcionar (`modes.py` lo evita con `ṽ=√(2k)v`). Arreglo: integrar `h/|h₀|`. La tolerancia (10⁻⁵) no se tocó. El modo de menor `k`, donde el bug no aparecía, ya coincidía a 1.4×10⁻⁷.
2. Al barrido de `n_grid_bg` se le agregaron valores gruesos (101, 201, 501): con solo {2001, 5001, 20001} el error era 4×10⁻¹³ en todos y el barrido no mostraba sensibilidad. No cambia el criterio (se juzga el valor por defecto).
3. Se agregó C0 (mutaciones). Su mutación M3 se suavizó dos veces (100 % y 1 % de `Q_i` impedían que la inflación terminara y el código lanzaba una excepción; se dejó 0.01 %).

### 10.2 Resumen

| ID | Función (`checks.py::`) | Qué prueba | Referencia | Tolerancia (a priori) | Peor caso medido | Estado |
|---|---|---|---|---|---|---|
| C0 | `check_mutations_are_detected` | Si se rompe el código a propósito, el check correspondiente falla (4 mutaciones) | — | 4/4 detectadas | 4/4 | PASA |
| C1.1 | `check_de_sitter_exact` | de Sitter exacto: `P_T = 2H²/(π²M_P²)(1+(k/aH)²)` | Baumann 8.127; solución exacta | 1e-5 | 8.71e-7 | PASA |
| C1.2 | `check_slow_roll_rg` | RG con `V=½m²φ²` vs. slow-roll a LO/NLO/NNLO | Martin et al. Eqs. 2.19, 2.23 | `30ε₁³+2e-5` (NNLO) | ver 10.3 | PASA |
| C1.3 | `check_planck_phi2` | `r`, `A_s`, `n_T` de `φ²` | Martin 2.19, 2.24; Baumann 8.128; Planck 2018 X | ver 10.3 | ver 10.3 | PASA |
| C2 | `check_convergence` | Convergencia en tolerancias, resolución del fondo, arranque dentro del horizonte y punto de medida | — | por parámetro (10.4) | ver 10.4 | PASA |
| C3.1 | `check_conservative_limit` | UG con `γ=0` (`Q` cte) ≡ RG | derivation.md 1.5, 2.14 | 1e-8 | 4.34e-13 | PASA |
| C3.2 | `check_background_28` | (2.8) `Ḣ=−φ̇²/2` sobre la solución integrada (no se usó para construirla) | derivation.md (2.8) | 1e-6 abs | RG 7.92e-12; UG 3.03e-7 | PASA |
| C3.3 | `check_independent_cosmic_time` | Integrador independiente (`h`, `t` cósmico) vs. `modes.py` | derivation.md (3.9), (4.6) | 1e-5 | 4.43e-10 | PASA |
| C3.4 | `check_ug_vs_rg_difference` | Magnitud de `P_T^UG/P_T^RG`, ruido numérico y atribución al fondo | derivation.md (3.9), (4.7) | ver 10.5 | ver 10.5 | PASA |
| C3.5 | `check_negative_control` | El código detecta una diferencia real en la ecuación de modos | derivation.md (4.6) | ver 10.5 | ver 10.5 | PASA |

### 10.3 Pedido 1: límite estándar (C1.1–C1.3)

**C1.1** En de Sitter exacto el error relativo es -8.71e-7 para `k = 10³, 10⁵, 10⁸` (constante en `k`, como debe ser por invariancia de escala). Lo atribuyo al error de la condición inicial adiabática con `ratio_start = 100`: coincide en magnitud con el que da el barrido de C2 para ese parámetro (9.0×10⁻⁷) y ese barrido cae como `(aH/k)³`. Este check prueba a la vez el integrador, la normalización de `P_T` (`⟨h_ij h_ij⟩`, `e·e=2`) y la forma en `N` de la ecuación de modos.

**C1.2** Residuo de `P_T/(2H²/π²·a₀)−1` con `H, ε₁, ε₂` en `k=aH` (RG):

| `N_exit` | `ε₁` | LO | NLO | NNLO | tol. NNLO |
|---|---|---|---|---|---|
| 20 | 0.0035 | -1.92e-03 | -1.15e-05 | +4.94e-07 | 2.1e-05 |
| 60 | 0.0049 | -2.69e-03 | -2.28e-05 | +5.03e-07 | 2.4e-05 |
| 100 | 0.0081 | -4.45e-03 | -6.38e-05 | -2.87e-07 | 3.6e-05 |
| 140 | 0.0230 | -1.30e-02 | -5.51e-04 | -4.05e-05 | 3.8e-04 |

La desviación LO coincide con `−2(C+1)ε₁` (`C=γ_E+ln2−2`), y cada orden reduce el residuo. A NNLO queda ≲ 5×10⁻⁷ en `N=20..100` (por debajo del piso de la condición inicial, ~9×10⁻⁷) y −4×10⁻⁵ en `N=140` (`ε₁=0.023`, `∼3ε₁³`). La tolerancia (`30ε₁³+2e-5`) es holgada respecto de lo medido; se dejó como estaba.

**C1.3** (`φ²`, RG, con `m = 6×10⁻⁶ M_P`; `N_*` = e-folds antes del fin de la inflación de RG):

| `N_*` | `ε₁` | `r = P_T/P_ζ0` | `16ε₁` | `r/16ε₁` | `n_T` código | `n_T` Martin 2.24 | `−2ε₁` |
|---|---|---|---|---|---|---|---|
| 50 | 0.01004 | 0.1597 | 0.1606 | 0.9945 | -0.020393 | -0.020389 | -0.020075 |
| 60 | 0.00836 | 0.1332 | 0.1338 | 0.9954 | -0.016947 | -0.016945 | -0.016727 |

`A_s` (LO escalar, `H²/8π²ε₁` con el `H` y `ε₁` del código) a `N_*=60`: 2.167e-09 vs. Planck 2018 2.099e-09 (`ln 10¹⁰A_s = 3.044`), diferencia +3.2 %. **Esto cierra la duda sobre `m = 6×10⁻⁶ M_P`** que 9.1 marcaba como [ESTÁNDAR, sin verificar]: reproduce `A_s` dentro de 3.2 % a `N_*=60`. `r` está en 0.13–0.16 para `N_*=60..50`, consistente con lo que Planck dice de un potencial cuadrático («roughly 0.15», en tensión con los datos): este último es un test débil (ventana [0.12, 0.17]).

### 10.4 Pedido 2: convergencia (C2)

Se varía un parámetro por vez y se compara con un valor «verdad» más fino, en 4 modos (`N_exit` = 12, 40, 70, 85) y en RG y UG. Máximo `|P/P_verdad − 1|`:

| Parámetro | Verdad | Valores → error | Defecto | Tol. | Pasa |
|---|---|---|---|---|---|
| `rtol_mode` | 1e-13 | 1e-06 → 2.19e-6; 1e-08 → 2.36e-9; 1e-10 → 1.08e-10; 1e-12 → 2.13e-12 | 1e-10 | 1e-07 | sí |
| `rtol_bg` | 1e-13 | 1e-08 → 4.49e-9; 1e-10 → 2.23e-11; 1e-12 → 3.86e-13 | 1e-12 | 1e-07 | sí |
| `n_grid_bg` | 80001 | 101 → 6.66e-7; 201 → 5.68e-9; 501 → 9.04e-11; 2001 → 4.06e-13; 20001 → 3.53e-13 | 20001 | 1e-06 | sí |
| `ratio_start` | 1000 | 30.0 → 3.59e-5; 100.0 → 9.04e-7; 300.0 → 3.76e-8 | 100 | 1e-05 | sí |
| `ratio_stop` | 0.0001 | 0.01 → 1.00e-4; 0.001 → 9.97e-7 | 0.001 | 1e-05 | sí |

Lectura: la condición inicial (`ratio_start`) es la fuente dominante y cae como `(aH/k)³` (30 → 100 → 300: 3.6×10⁻⁵, 9.0×10⁻⁷, 3.8×10⁻⁸); el punto de medida (`ratio_stop`) da el `(k/aH)²` esperado (10⁻⁴ → 10⁻⁶). Con los valores por defecto el resultado es estable a ~10⁻⁶.

### 10.5 Pedido 3: diferencia UG–RG (C3.1–C3.5)

**Sí hay diferencia, y se cuantifica.** `P_T^UG/P_T^RG` en 9 modos (`N_exit` de RG = 10, 20, …, 90): 0.888, 0.825, 0.782, 0.742, 0.698, 0.644, 0.574, 0.477, 0.327. Es decir, UG suprime `P_T` entre 11 % (`N=10`) y 67 % (`N=90`) con `Q_i/V_i=0.1`, `γ=0.1`. (Lo medido en 40 modos está en `resultados/PT_k.csv`.)

**No es ruido numérico:**
- C3.4: variando `rtol_mode` (10⁻⁸, 10⁻¹²), `rtol_bg` (10⁻¹³), `ratio_start` (300) y `ratio_stop` (10⁻⁴) el cociente cambia como máximo 8.50e-7 (dominado por `ratio_start`), contra una señal mínima de 0.112: señal/ruido = 1.3e+05 (criterio ≥ 100).
- C3.5: con `λ̄` equivocado (se omite `Q`) `P_T` de UG cambia 60 % (`N=12`), 7.6 % (40), 0.7 % (70), 0.3 % (85): el código **es sensible** a un término de masa real (decae porque `Q ∝ e^(−γN)`). Con el `X` que se calcula vs. `X=0`, el cambio es ≤ 4.86e-14: el término de masa calculado es despreciable.

**Se explica por el fondo:** con la fórmula slow-roll NNLO de RG evaluada con el `H`, `ε₁`, `ε₂` **propios de UG** en su cruce `k=aH`, el cociente predicho coincide con el numérico así (`N_exit`: desviación relativa):
10: -1.3e-06; 20: -1.0e-06; 30: -7.3e-07; 40: -7.2e-07; 50: -1.2e-06; 60: -2.6e-06; 70: -7.3e-06; 80: -2.8e-05; 90: -2.7e-04 (no juzgado a priori, ε₂=0.10).

Los 8 modos juzgados quedan a ≲ 3×10⁻⁵ (la mayoría a ~10⁻⁶); el de `N=90` no entra al criterio fijado a priori (`ε₂` de UG = 0.096 > 0.05) y aun así queda en 2.7×10⁻⁴.

**C3.1** `γ=0` ⇒ UG ≡ RG a 4.34e-13 en `P_T` y 8.53e-14 en `N_end`: prueba el camino de UG (`quantities_ug`, `hubble_ug`, (2.9), Λ₀ de (2.11)) contra el de RG, que son código distinto.

**C3.2** `−dlnH/dN = φ_N²/2` en la solución integrada: error máx. RG 7.92e-12, UG 3.03e-7 (en `N=0`, donde `ε₁` de UG salta y el spline resuelve peor; margen 3× sobre la tolerancia de 10⁻⁶).

**C3.3** El integrador independiente (`h`, tiempo cósmico, sin `N`, sin `v`, sin splines, sin `ε₁`) coincide con `modes.py` a 4.43e-10 en RG y UG: valida los pasos n1–n2 (forma en `N` de la ecuación de modos) de la sec. 9.3.

**C0** (mutaciones): duplicar la normalización de `P_T` hace fallar C1.1; cambiar el signo de `ε₁` en la ecuación de modos hace fallar C3.3 y C1.2; un `Λ₀` errado en 0.01 % de `Q_i` hace fallar C3.1. Los checks no son vacuos.

### 10.6 Qué estos checks NO muestran (límites)

- **Solo RG tiene referencia externa.** No conozco literatura con `P_T` de UG con difusión; UG se apoya en C3.1 (límite `Q` cte), C3.2, C3.3 y C3.4, que son consistencia interna y contra RG.
- **C3.4 (atribución) valida la numérica, no la derivación:** que UG siga la fórmula estándar con su propio `H(t)` es exactamente lo que el código implementa (ecuación de modos con `X≈0`). Lo que muestra es que la diferencia UG–RG no es un artefacto y que no hay otra fuente escondida. Que la ecuación de modos de UG sea la de RG es el resultado de `derivation.md`, que no se contrasta acá de forma independiente; C3.5 solo prueba que, de ser distinta, el código lo vería.
- **El sector escalar no está verificado ni derivado:** `A_s` y `r` en C1.3 usan la fórmula slow-roll estándar de RG (Martin 2.19). No dicen nada de `P_R` en UG; **O1, O2 y O5 siguen abiertos**.
- **C3.3 comparte con `modes.py`** la condición de Bunch–Davies adiabática y la definición de `P_T`; esas dos se validan aparte (C1.1 analítico, C2 por `ratio_start`), no por el integrador independiente.
- **Un solo conjunto de parámetros** (`V=½m²φ²`, `Q_i/V_i=0.1`, `γ=0.1`, `φ_i=25.386`), 4 modos en C2/C3.1/C3.3 y 9 en C3.4. Fuera de `γ=0` no se barrió `Q_i` ni `γ`; el pico de C3.2 en `N=0` (salto de `ε₁` en UG) indica que ahí la resolución del fondo es lo más justo.
- **C1.2 usa coeficientes que transcribí del texto extraído por `pdftotext`** (Martin 2.20–2.25); el acuerdo a NNLO (~5×10⁻⁷) es evidencia de que la transcripción es correcta, no una verificación contra el PDF renderizado.
- **`N_*` y recalentamiento:** en C1.3 `N_*` se toma tal cual (50 y 60), sin modelar el recalentamiento.

### 10.7 Fuentes externas usadas (nivel de lectura)

| Fuente | Qué se toma | Dónde | Nivel |
|---|---|---|---|
| J. Martin, C. Ringeval, V. Vennin, «Encyclopaedia Inflationaris», arXiv:1303.3787v3 (copia de la carpeta del director) | Eq. (2.17) `P_h`; Eq. (2.19) `P_h0`, `P_ζ0`; Eqs. (2.20)–(2.25) coeficientes `a_i^(T)`, `C=γ_E+ln2−2≈−0.7296`, `f=5` para `k_*=aH`; `M_Pl²=(8πG)⁻¹` | `pdftotext`, líneas ~1090–1200 | T-parcial (esas ecuaciones y su contexto) |
| D. Baumann, *Cosmology* (CUP 2022) | Eqs. (8.127)–(8.128): `A_t=2V/(3π²M_Pl⁴)`, `n_t=−2ε_V` | `pdftotext`, línea ~20561 | T-parcial |
| Planck 2018 X (arXiv:1807.06211) | «purely quadratic potential always predict a large tensor-to-scalar ratio (of roughly 0.15)»; `ln(10¹⁰A_s)=3.044±0.014` (TT,TE,EE+lowE+lensing) | `pdftotext`, Sec. de modelos y Tabla de parámetros | T-parcial |

---

## 11. Figuras

Fecha: 2026-09-20. **Script:** `codigo/make_figures.py`. **Regenerar:** `cd codigo && python3 make_figures.py` (~3 s). **No recalcula nada**: lee solo los outputs ya guardados en `codigo/resultados/` (`PT_k.npz`, `checks.json`) y no importa `background`, `modes`, `checks` ni `run_spectrum` (lo comprueba `test_figures.py`). Salidas en `codigo/figuras/`: cada figura en `.png` (200 dpi) y `.pdf` (vectorial), una **tabla gemela** `.csv` con exactamente los datos dibujados, y `manifest.json` (sha256 de las entradas, del script y de cada salida). Los números que aparecen escritos en las figuras (0.94, 0.30, errores «defecto», parámetros del modelo) se leen de los datos, no están tipeados a mano.

Las figuras rápidas `resultados/PT_k.png` y `resultados/fondo.png` (de `run_spectrum.py::main`) son solo de inspección; las figuras de reporte son las de esta sección.

### 11.1 Paleta y validación

Guía de estilo: la skill de visualización de datos disponible en el entorno (paleta categórica validada, líneas de 2 px, leyenda siempre presente para ≥ 2 series, texto en tinta neutra, grilla hairline sólida, un solo eje de valores, tabla gemela). Colores: azul `#2a78d6` (RG), naranja `#eb6834` (UG), aguamarina `#1baf7a` (tercera serie, solo en la fig. 3A); tinta `#0b0b0b`/`#52514e` sobre superficie `#fcfcfb`. Solo modo claro (figuras para papel/PDF).

Validador de la skill (`validate_palette.py`, modo claro, superficie `#fcfcfb`):

| Paleta | Resultado |
|---|---|
| `#2a78d6,#eb6834` (adyacentes) | PASA todo: separación CVD ΔE 24.7 (protan), 32.7 (tritan); visión normal 33.6; contraste ≥ 3:1 |
| `#2a78d6,#eb6834,#1baf7a` (`--pairs all`) | PASA con **una advertencia**: la aguamarina tiene contraste 2.74:1 (< 3:1). Obliga a «alivio»: etiquetas directas visibles y tabla gemela. Ambos están (etiquetas LO/NLO/NNLO junto a cada serie, marcadores de forma distinta, `fig3a_C1_2_slow_roll.csv`) |

### 11.2 Entradas por figura

**Fig. 1 — `fig1_PT_k_RG_vs_UG.{png,pdf,csv}`**
- **produced_by:** `make_figures.py::fig_pt_comparison`.
- **datos:** `resultados/PT_k.npz` (← `run_spectrum.py::main`, que integra 40 modos con `modes.py::run_all_modes` sobre los fondos de `background.py`; parámetros en el propio archivo) y, para los 9 marcadores huecos, `resultados/checks.json::C3.4.details.attribution` (← `checks.py::check_ug_vs_rg_difference`).
- **shows:** arriba, `P_T(k)` de RG y UG con la diferencia sombreada; abajo, el cociente `P_T^UG/P_T^RG` (40 modos: de 0.938 en `k = 1.0×10³` a 0.298 en `k = 3.5×10⁴⁰`, en unidades de `m` con `a_i = 1`) y los 9 valores de la fórmula slow-roll NNLO de RG evaluada con el `H`, `ε₁`, `ε₂` de UG. Eje superior: los mismos `k` en e-folds hasta el cruce del horizonte en RG.
- **from_scratch:** todo el código de la figura. **from_library:** `matplotlib` 3.9.2, `numpy` 1.26.4.
- **choices:** (i) mismo `k` comóvil en ambos modelos (`a_i = 1`, mismas condiciones iniciales; PROVENANCE 9.1); consecuencia: RG y UG tienen distinta duración (161.8 vs 100.0 e-folds) y **la correspondencia `k` ↔ «N e-folds antes del fin» no es la misma en los dos**. (ii) eje superior `N_exit`(RG) por interpolación lineal de `ln k` frente a `N_exit` sobre los 40 modos; (iii) los marcadores de C3.4 no traen su `k` en `checks.json`, se ubican por esa misma interpolación (error de posición ≪ el tamaño del marcador); (iv) banda gris = modos con `ε₁ > 0.02` de UG en el cruce (desde el modo 36 de 40): **es una elección de presentación**, distinta del criterio a priori de C3.4 (`ε₂ ≤ 0.05`); (v) `P_T` en unidades físicas con `m = 6×10⁻⁶ M_P`.
- **supports:** (a) para estos parámetros (`Q_i/V_i = 0.1`, `γ = 0.1`, `V = ½m²φ²`), UG suprime `P_T` frente a RG a igual `k`, entre 6 % y 70 % según `k` (PROVENANCE 10.5); (b) esa diferencia coincide con la que da la fórmula estándar con el fondo de UG, a ≲ 3×10⁻⁵ en los modos juzgados (C3.4).
- **no soporta:** que la supresión sea general (un solo conjunto de parámetros, 10.6); nada sobre el sector escalar ni sobre `r` (O1/O2/O5 abiertos); que la ecuación de modos de UG sea la de RG más allá de lo que implementa el código (10.6).

**Fig. 2 — `fig2_convergencia.{png,pdf,csv}`**
- **produced_by:** `make_figures.py::fig_convergence`. **datos:** `resultados/checks.json::C2` (← `checks.py::check_convergence`).
- **shows:** error máximo `|P_T/P_T,verdad − 1|` (4 modos, RG y UG) al variar un parámetro numérico por vez: tolerancia del integrador de modos y del fondo, resolución de la malla de splines, `k/(aH)` inicial y final. Línea = tolerancia fijada a priori; círculo = valor por defecto.
- **choices:** el eje x de las dos tolerancias va invertido (más fino a la derecha); el título («…en los cinco parámetros») se calcula de los datos y cambia si algún valor por defecto no está dentro de la tolerancia.
- **supports:** convergencia numérica del resultado a ~10⁻⁶ (PROVENANCE 10.4). **no soporta:** convergencia en otros parámetros físicos (`Q_i`, `γ`, `φ_i`).

**Fig. 3 — `fig3_limite_estandar.{png,pdf}`, `fig3a_C1_2_slow_roll.csv`, `fig3b_C3_4_atribucion.csv`**
- **produced_by:** `make_figures.py::fig_standard_limit`. **datos:** `resultados/checks.json::C1.2` (← `checks.py::check_slow_roll_rg`) y `::C3.4` (← `checks.py::check_ug_vs_rg_difference`).
- **shows:** (A) RG con `φ²`: residuo de `P_T` frente a `2H²/π²·a₀` en LO, NLO y NNLO (Martin et al. Eqs. 2.19, 2.23) en 4 modos, con la tolerancia NNLO y las guías `ε₁^p`; (B) desviación relativa entre el cociente UG/RG numérico y el de la fórmula slow-roll con el fondo de UG, con la tolerancia a priori; el modo de `N_exit = 90` (`ε₂` de UG = 0.10) se marca aparte porque no entra en el criterio.
- **choices:** el título de A («cada orden reduce el residuo») se activa solo si se cumple `|NNLO| < |NLO| < |LO|` en todos los modos; el de B dice «coincide» solo en sentido numérico (ver límite de C3.4 en 10.6).
- **supports:** límite estándar de RG (10.3) y consistencia numérica de la diferencia UG–RG con el fondo (10.5). **no soporta:** que la derivación de `derivation.md` sea correcta (C3.4 valida la numérica, no la derivación).

### 11.3 Límites de esta sección

- Las figuras son una representación de datos ya guardados, no un resultado independiente de los checks: si `PT_k.npz` o `checks.json` cambian, hay que regenerarlas. `test_figures.py` lo detecta comparando los hashes de `figuras/manifest.json` con los archivos actuales, y comprueba que el script no importa código de cálculo y que sus CSV son deterministas.
- El PNG/PDF puede variar de byte entre versiones de `matplotlib`; lo que se compara en el test es el CSV.
- *[Histórico: al escribirse esto] la carpeta de trabajo no era un repositorio git; ahora es un repositorio git local (sec. 15)*: el script vive junto al resto del código (`codigo/`) y queda versionado cuando se cree el repo de entrega.

### 11.4 Figuras de apoyo del informe (fig. 4 y fig. 5)

Generadas por `codigo/make_report_figures.py`. **A diferencia de `make_figures.py`, este script sí calcula** (~3 s): resuelve los fondos de RG y UG con `background.py` (`solve_background_rg/ug`, con `phi_i` ajustado por `phi_i_for_ug_duration` para `N_f(UG) = 100`) e integra un modo con `modes.py::mode_rhs`, porque esas trayectorias no se guardan en `resultados/`. Comparte parámetros (`config.Params` por defecto) y estilo (`make_figures.py`) con el resto. Salidas en `codigo/figuras/`: `fig4_fondo.{png,pdf,csv}`, `fig5_modo.{png,pdf,csv}` y `manifest_informe.json` (hashes). **No tiene prueba automática** (solo el manifest); es un hueco menor respecto de las figuras 1–3.

- **Fig. 4 — `fig4_fondo`** · produced_by: `make_report_figures.py::fig_fondo` · shows: `H(N)`, `ε₁(N)`, `φ(N)` en RG y UG con las mismas condiciones iniciales, y el presupuesto de energía de UG, `3H² = ρ_φ + Q(N) − Q_i`. · choices: panel (d) sin color por serie (todas son de UG): tinta, naranja para `3H²` y guiones para `Q`. · supports: (a) `N_end` = 161.83 (RG) y 100.00 (UG); (b) el salto inicial de `ε₁` de UG (0.0031 → 0.0104 en `N ≈ 1.04`); (c) **el final de la inflación en UG ocurre con `φ = 8.44 M_P`, `ρ_φ = 37.35` y `3H² = 5.13`, porque `Λ₀ = −Q_i = −32.2` le resta a `H²` una energía comparable a `ρ_φ`**. Este último punto **no se había señalado antes** de graficar y condiciona la lectura de la magnitud de la diferencia UG–RG (informe, sec. 9.1 y 10.2). · no soporta: nada sobre otros valores de `Λ₀`, `Q_i` o `γ`.
- **Fig. 5 — `fig5_modo`** · produced_by: `make_report_figures.py::fig_modo` (con `_mode_history`) · shows: un modo `k = 2.12×10¹⁸ m` (sale del horizonte en `N = 40.000` en RG y `40.149` en UG) antes y después del cruce; `P_T` final 5.888×10⁻¹⁰ (RG) y 4.368×10⁻¹⁰ (UG). · supports: el congelamiento de `P_T` fuera del horizonte y que el cociente 0.742 se anticipa con `(H_UG/H_RG)² = 0.744` en `N = 40`.

---

## 12. Informe (`informe/`)

Fecha: 2026-09-20. `informe/informe_UG.pdf` (45 págs.), compilado con `xelatex` desde `informe/informe_UG.tex` y sus secciones (`s01`–`s10`, apéndices `apA`–`apD`, `bibliografia.tex`); figuras de `codigo/figuras/`. Compilar: `cd informe && xelatex informe_UG.tex` (tres veces para índice y referencias). Es un texto de lectura en formato paper que reúne, desde lo elemental, todo lo hecho en el proyecto; **no agrega resultados nuevos** salvo las figuras 4–5 (11.4) y las lecturas señaladas abajo.

Cosas que el informe dice y que **no estaban explícitas en el resto del registro** (para revisar):
- La magnitud de la supresión de `P_T` en UG es en buena medida consecuencia de `Λ₀ = −Q_i` (mismo `H_i` en ambos modelos); con `Λ₀ = 0` cabe esperar el signo opuesto en parte del rango, **sin haberlo calculado** (informe 10.2).
- La hipótesis sobre la materia (informe 10.3): un `Q` variable no se deduce de una acción covariante estándar; el resultado tensorial supone que `δT^i_j|_TT = 0` y que la acción de la materia a segundo orden es la estándar. Ya estaba como SUPUESTO en `derivation.md` pero sin esta discusión.
- Alternativa no comprobada: perturbar el lapse a segundo orden (`N = 1 + ¼h²`) en lugar de dejar que el multiplicador absorba la violación del volumen; se espera la misma acción en capa, sin desarrollarlo.
- Errores míos corregidos durante la escritura: una estimación de e-folds restantes en RG (era ~17, no ~60), la dirección de la frecuencia de oscilación en `N`, y el conteo de mutaciones/tests.
- Datos de la publicación de Martin et al. omitidos de la bibliografía porque no se habían verificado (solo arXiv). Las citas textuales son traducciones libres.

## 13. Potencial de Starobinsky y comparación a igual N* (2026-09-21)

**Qué se agregó.** Un segundo potencial y un segundo criterio de comparación, sin tocar los resultados del cuadrático (`resultados/checks.json`, `PT_k.npz` y figuras siguen siendo los de la sec. 10–11; la regresión pasa: 17 tests previos + 8 nuevos = 25).

| Elemento | Dónde | Etiqueta | Origen / decisión |
|---|---|---|---|
| `V = (3/4) M² (1 − e^{−√(2/3) φ})²` | `background.py::V, dV` (`potential="starobinsky"`) | SUPUESTO (usuario, 2026-09-21); forma ESTÁNDAR | Marco de Einstein de `R + R²/(6M²)` en RG. Metadatos verificados (Crossref/arXiv): Starobinsky, *Phys. Lett. B* **91**, 99 (1980), DOI 10.1016/0370-2693(80)90670-X; De Felice–Tsujikawa, *Living Rev. Relativ.* **13**, 3 (2010), DOI 10.12942/lrr-2010-3, arXiv:1002.4928; Planck 2018 X, arXiv:1807.06211. **No leí sus textos**: la fórmula está tomada de memoria; se contrasta indirectamente con `r ≈ 12/N²` y `n_s ≈ 1−2/N` (C1.3-S). **Solo se usa la forma del potencial; no se afirma que el origen `R²` valga en UG.** |
| Escala `M = 1.14×10⁻⁵ M_P` | `config.py::M_STAROBINSKY` | CALIBRACIÓN | Se fijó para que RG reproduzca `A_s` de Planck a `N_*=60` con `P_ζ0 = H²/(8π²ε₁)` (M necesario 1.143×10⁻⁵). Mi valor inicial de memoria (1.3×10⁻⁵, N_* ≈ 52) se descartó antes de correr checks. **El check de `A_s` en C1.3-S no es una validación independiente.** |
| `phi_bracket`, `t_max` por potencial | `config.py::params_for` | DEFECTO | Starobinsky: `φ_i ∈ (5,9)` → `φ_i = 7.6604 M_P` (UG dura 100 e-folds); `t_max = 10⁴` porque RG dura 386.7 e-folds. |
| Modos sin desbordes para N grande | `modes.py::bunch_davies_ic, tensor_power, mode_rhs` | Mío | Reescritura algebraicamente equivalente en variables adimensionales `q = k/(aH)` (con `a` y `k²` sueltos se desborda para N ≳ 350). Regresión: los 10 checks del cuadrático siguen pasando, incluido el control de mutaciones. |
| Comparación a igual N* | `compare_potentials.py` → `resultados/comparacion_N_star.csv/.json` | Mío; criterio: usuario («opción recomendada») | Cada modelo se mide en el modo que sale del horizonte `N_* = 50, 60` e-folds antes del final de **su** inflación. Resto de decisiones sin cambios (mismo `φ_i, φ̇_i, H_i`; `Λ₀ = −Q_i`; `Q_i/V_i = 0.1`; `γ = 0.1`; `N_f(UG) = 100`). |

**Checks de Starobinsky** (`python3 checks.py starobinsky`, `resultados/starobinsky/checks.json`): C1.2, C1.3-S, C2, C3.1–C3.5, 8/8 pasan. Cambios hechos **después de ver fallos**, con su justificación (deben leerse como tales):
1. *C1.2, cota NLO*: la cota original `20ε₁²` falló porque en Starobinsky `ε₂ ≫ ε₁` y el residuo NLO es `−0.25 ε₁ε₂` según [MAR] (2.23) (medido 1.5×10⁻⁶ con ε₁ = 1.9×10⁻⁴, ε₂ = 0.032; predicho −0.25·ε₁ε₂ = 1.6×10⁻⁶). Se generalizó a `20 ε₁ max(ε₁, |ε₂|/2)`; en el cuadrático es idéntica. El criterio principal (NNLO) no cambió y pasaba con margen ~100×.
2. *C3.2 ((2.8) sobre la solución)*: falló solo en `N < 0.05` de UG (error 1.6×10⁻⁵ > 10⁻⁶): `φ̇_i` (slow-roll de `V` sola) queda ~30× por debajo del atractor de UG y `ε₁` salta de 5×10⁻⁶ a 1.3×10⁻³ en ΔN = 0.05, donde la interpolación por splines no resuelve. El error converge al refinar la malla (1.6×10⁻⁵, 3.3×10⁻⁶, 1.0×10⁻⁶ para `n_grid_bg` = 2×10⁴, 8×10⁴, 2×10⁵) y para `N ≥ 1` es < 2×10⁻¹⁰. Para Starobinsky se juzga desde `N = 1`; el primer e-fold se guarda sin juzgar.

**Resultados (M fija en cada potencial; ver `comparacion_N_star.csv`).** `P_T` y `n_T` son resultados; `r_std`, `n_s_std`, `A_s_std` **no**: aplican la fórmula escalar de RG con el fondo de UG (el sector escalar de UG con difusión no está derivado; O1/O2/O5).

| Potencial | N* | `P_T^UG/P_T^RG` | `n_T` RG / UG | `r_std` RG / UG | `n_s_std` RG / UG |
|---|---|---|---|---|---|
| cuadrático | 50 | 1.575 | −2.04e−2 / −1.59e−2 | 0.160 / 0.125 | 0.960 / 0.968 |
| cuadrático | 60 | 1.516 | −1.70e−2 / −1.38e−2 | 0.133 / 0.109 | 0.967 / 0.975 |
| Starobinsky | 50 | 0.902 | −5.5e−4 / −6.7e−4 | 4.4e−3 / 5.4e−3 | 0.961 / 0.986 |
| Starobinsky | 60 | 0.904 | −3.9e−4 / −7.0e−4 | 3.1e−3 / 5.6e−3 | 0.967 / 1.022 |

Comparación a igual `k` para Starobinsky (`resultados/starobinsky/PT_k.csv`): `P_T^UG/P_T^RG` de 0.96 a 0.77 (los valores guardados son `staro_ratio_equal_k_first/last` en `numbers.json`; una versión anterior de esta línea decía 0.83, era una errata detectada al revisar, sec. 16).

**Hallazgos que cambian la lectura del informe (histórico: ya reflejados en `informe/` desde la sec. 10.3–10.4, ver sec. 15 y 16):**
- Para el **cuadrático**, el signo de la diferencia depende del criterio: a igual `k` (informe) UG *suprime* `P_T` (0.94 → 0.30); a igual N* UG lo *aumenta* (×1.5). La razón es que a igual `k` se comparan épocas distintas (RG dura 162 e-folds y UG 100 con el mismo `φ_i`). La afirmación de que «UG suprime `P_T`» no es robusta.
- Para **Starobinsky** la diferencia en `P_T` es ~10 % con ambos criterios (`Λ₀ = −Q_i` es ~10 % de la altura del plateau, `H_UG/H_RG ≈ 0.94`), y la inflación termina porque el campo rueda (`3H² = 0.20`, `V = 0.23` al final), no por `Λ₀`: el hallazgo del informe (sec. 10.2) es propio del cuadrático. Además `V_eff = V − Q_i` deja un mínimo negativo (universo tipo AdS tras la inflación).
- En UG-Starobinsky los primeros ~30 e-folds están dominados por el término `Q` (`|Q′|/|V′|` = 500 en N = 0, 9 en N = 10, 1.2 en N = 30, < 0.1 pasado N = 50); el pivote `N_* = 60` cae en N = 40, donde `|Q′|/|V′| ≈ 0.4`.
- Las diferencias de `n_T` son ≲ 3×10⁻⁴ en Starobinsky (inobservables). Los `n_s_std` de UG (0.986 y 1.022) valdrían solo si el sector escalar fuese el estándar; no hay derivación.
- Sin cambiar: el fondo de UG resuelve (2.7)–(2.9) y `X ≈ 0` a 10⁻¹⁵ en ambos potenciales.

### 13.1 Comprobaciones simbólicas (`codigo/symbolic_checks.py`, `test_symbolic.py`)

Cuatro comprobaciones exactas con SymPy 1.14. No se conservan pruebas reproducibles de mutaciones simbólicas; las mutaciones disponibles son las numéricas de C0.

| Id | Qué comprueba | Etiqueta | Alcance / límite |
|---|---|---|---|
| S1 | `G^x_x − G^y_y = +ε(ḧ + 3Hḣ − ∂_z²h/a²)` para `g = diag(−1, a²(1+εh), a²(1−εh), a²)`; componentes espaciales no diagonales nulas | PROPIA (derivation.md Sec. 3) | Solo primer orden. **La acción a segundo orden y la cancelación del vínculo siguen verificadas solo a mano.** El signo esperado lo había supuesto opuesto; lo fijó el cálculo. |
| S2 | `∇ₐTᵃᵇ = (□φ − V′)∇ᵇφ` a primer orden, ansatz escalar sin E (lapse A, shift B, curvatura ψ, dependientes de (t,x)), V cuadrático y de Starobinsky | ESTÁNDAR | Solo dependencia en una coordenada espacial. |
| S3 | Con (2.7) y (2.9): `Ḣ = −φ̇²/2`; con `Q = Q(φ)` la KG de UG es la de RG con `V_eff = V + Q + Λ₀` | PROPIA | Es bookkeeping algebraico; Friedmann coincide por definición de `V_eff`. |
| S4 | Componente espacial de `∇ₐTᵃᵇ = ∇ᵇQ`: `∂ₓδQ = E₀∂ₓδφ` (`E₀ = □φ − V′`, de fondo); temporal de fondo: `Q̇ = E₀φ̇`; `δQ = 0 ⇒ E₀ = 0 ⇒ Q̇ = 0` | PROPIA | Un solo escalar. Para un fluido perfecto no hay esa obstrucción, pero **eso no se comprobó simbólicamente**. |

**Lo que NO está verificado simbólicamente:** la equivalencia UG ≡ RG con `V_eff` a nivel de las perturbaciones escalares completas (argumentada a mano en informe sec. 11.2), el gauge restringido de UG y el segundo orden del sector tensorial.

### 13.2 Figuras nuevas (`codigo/make_figures_potenciales.py`, `figuras/manifest_potenciales.json`)

fig6 (fondo Starobinsky; **calcula** con `background.py`), fig7 (P_T a igual k, ambos potenciales; lee `resultados/PT_k.csv` y `resultados/starobinsky/PT_k.csv`), fig8 (cociente P_T, n_T y r_std a igual N*; lee `resultados/comparacion_N_star.csv`). Estilo de `make_figures.py`; csv gemelo por figura; `test_figures.py::test_potenciales_manifest_is_current` verifica hashes.

### 13.3 Informe (`informe/`, 53 págs.)

Nuevas: sec. 10 «Un segundo potencial y la comparación a igual N*» (`s10_potenciales.tex`) y sec. 11 «El acoplamiento de Q a la materia y el caso δQ = 0» (`s11_acoplamiento.tex`); la discusión pasó a sec. 12. Actualizados: resumen, sec. 1, tabla de decisiones (sec. 8), aviso en sec. 9.3, discusión, apéndice D, bibliografía (Starobinsky 1980 y De Felice–Tsujikawa: solo metadatos). Sec. 9 (resultados a igual k del cuadrático) se conserva como estaba, con la salvedad añadida. Tests: 30 (17 previos + 8 Starobinsky + 4 simbólicos + 1 manifest de figuras).

**Pendiente de decisión del usuario/director:** el marco (inflatón con `Q = Q(φ)` frente a radiación con `δQ = 0` de León). Con radiación, el fondo es `3H² = ρ_r + Q + Λ₀`, `ρ̇_r + 4Hρ_r = −Q̇`; el código de modos se reutiliza tal cual, hay que escribir el fondo y sus controles.

## 14. Modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329): radiación pura + Q, δQ = 0 (2026-09-21)

**Decisión del usuario:** usar el fondo de A1/A2 (radiación, sin inflatón, `δQ = 0`). **Desvío respecto de lo propuesto:** recomendé el escenario 2 de A1 (Eq. 34) con `N_f = 100` y `α` calibrado con `A_s`; no es viable: con esa `ε₁`, `ε₁(N_f−60) = (4/3)e^{−120α}` no depende de `N_f`, y para `H⋄ ~ 10⁻⁵ M_P` hace falta `α ≈ 0.022`, con `ε₁ ≈ 0.09` (sin slow-roll); A2 encuentra `α ≈ 0.0229` con `N_f ≃ 370`. Se usó el escenario 1 de A2 (`N_f = 100`, `ρ_end = 10⁻¹¹ M_P⁴`, `γ = 2.02`) y el 3 (mapeo de potenciales slow-roll). Escenario 2: implementado, **no analizado**.

| Elemento | Dónde | Etiqueta | Origen |
|---|---|---|---|
| Fondo `3H² = ρ + Q`, `ρ_N + Q_N + 4ρ = 0`, `Λ* = 0`, `ε₁ = 2/(1+Q/ρ)` | `background_leon.py::reconstruct` | CITADO | A1 Eqs. 9, 16, 18, 32–33 (PDF leído) |
| `H = H_ref exp(−∫ε₁)`, `ρ = (3/2)ε₁H²`, `Q = (3/2)(2−ε₁)H²` | idem | PROPIA (combinación de las anteriores) | verificado en CL1–CL2 |
| Escenarios 1, 2, 3 y `ρ_end = 10⁻¹¹`, `N_f = 100`, `γ = 2.02` | `eps1_power`, `eps1_tanh`, `eps1_slowroll_map` | CITADO | A2 Eqs. 44, 49; Sec. III.C; Sec. IV.A, IV.C |
| Camino independiente (continuidad integrada) | `integrate_continuity` | PROPIA | hacia adelante en N (hacia atrás amplifica el error `e^{4N}`) |
| Inflatón de RG con `V` reconstruido | `rg_inflaton_with_same_H` | ESTÁNDAR | `φ̇² = 2ε₁H²`, `V = (3−ε₁)H²` |
| Modos, `P_T` | `modes.py` (sin cambios) | — | solo cambia el `Background` |
| `r` con tres variantes de `P_R` | `run_leon.py` | CONDICIONAL | A2 `H²/8π²ε₁`; A1 Eq. 66 literal (×3^{3/2}); hipótesis O5 (`/c_s`, **no verificada**) |

**Controles** (`checks_leon.py`, 7/7, `resultados/leon/checks.json`): CL1 continuidad 1.7e−8; CL2 formas cerradas de A2 Eqs. 46–48 3e−11; CL3 `|X|/H² ≤ 2.5e−10` (`N ≤ N_end−0.5`; en el último punto de la malla el spline tiene error de borde 1e−6); CL4 RG con inflatón reconstruido: `|ΔlnH| = 8e−7`, `P_T` a 1e−10 (N*=50,60), ≤1.1e−6 en los 28 modos que alcanzan q=10^-3; dos evaluados al final se rotulan aparte; CL5 slow-roll [MAR] NNLO; CL6 `A_s` en el punto de A2 (γ=2.02, N=43 desde el inicio ⇒ N*=57) = 2.12e−9 vs Planck 2.099e−9 (+1.0816 %), sin ajustar nada; CL7 forma del mapeo vs RG numérico ≤0.3 %.
**Cambios hechos después de ver resultados:** (i) CL1 se restringió a los escenarios 1 y 3: en el 2, `ρ` llega a ~1e−140 y la integración en doble precisión falla (`ρ` sale de restar O(1), condicionamiento `e^{4N}`; produjo error 6e5 y NaN); (ii) CL7 se planteó a priori como `|P_RG/P_map − 1| ≤ 10 %` y **falló** (+23 % a +29 %); diagnóstico: `ln(H_map/H_RG)` es plano en el interior (variación ≤0.013 entre 20 y 80 e-folds antes del final) y se acumula 0.10–0.13 en las últimas ~10 e-folds (mapeo con `ε_V = 1` como final y `ε_V < ε_H` en 5–20 %); se reemplazó por un criterio sobre la forma (3 %) y el desfasaje absoluto pasó a ser resultado.

**Resultados** (`resultados/leon/comparacion.csv`): γ = 2.02, N* = 57: `P_T = 9.30e−12`, `n_T = −5.5e−4`, `A_s^{A2} = 2.12e−9` (`A_s^{A1} = 1.10e−8`, `A_s^{cs} = 3.67e−9`), `r_A2 = 4.4e−3` (A1: 8.4e−4; cs: 2.5e−3), `n_s,std = 0.9646`. γ = 1.5, N* = 60: `A_s^{A2} = 1.32e−9`. Mapeo Starobinsky/cuadrático (N* = 60): `P_T^{RG}/P_T^{mapa} = 1.23 / 1.29`; `A_s^{A2} = 1.55e−9 / 1.24e−9`.

**Límites:** (1) sector escalar no derivado: `A_s` y `r` condicionales; la consistencia de A2 con Planck es circular (sus parámetros se eligieron con su fórmula); no dice cuál factor (`1`, `3^{3/2}`, `1/c_s`) es correcto (O1/O5 abiertos). (2) Escenario 2 no analizado. (3) Solo 2 valores de `γ` y sin barrido. (4) Los contornos de Planck + BK15 de A2 no se reprodujeron.

**Figuras y informe:** `make_figures_leon.py` (fig9 fondo, fig10 `P_T` y `A_s`; `figuras/manifest_leon.json`, test de vigencia). Informe: sec. 12 nueva (`s12_leon.tex`), sec. 11.3 actualizada, resumen, intro, discusión (ahora sec. 13), apéndice D; 57 págs. Tests: 38 (30 + 7 CL + 1 manifest).

## 15. Repositorio, paper y registro (2026-09-21, noche)

- **Repo:** la carpeta de trabajo (`entrega final/`) es el repo; reestructurada (`derivation/`, `provenance/`, `literatura/`, `paper/`, `docs/`); `.gitignore` excluye el apunte previo (`gravedad_unimodular_inflacion.*`), `versiones_previas/`, `codigo/_nb_src/`, `__pycache__`, PDFs de papers. **Sin remoto ni push** (publicación a cargo del autor).
- **Registro de procedencia (formato del curso, día 5):** `provenance/numbers.json` (30 números; los VALORES se leen de `codigo/resultados/` con `codigo/make_provenance_numbers.py`, no se tipean), `provenance/claims.yaml` (9 afirmaciones con evidencia `archivo::función` o cita, y 10 figuras), `provenance/validate_provenance.py` y `codigo/test_provenance.py` (chequeo estructural de campos, archivos/funciones y claves enlazadas; el test de regeneración comprueba sincronía con resultados guardados). El validador no importa ni ejecuta productores, no verifica las citas textuales, no certifica la verdad de las afirmaciones y no comprueba cobertura del HTML/PDF.
- **Paper corto:** `paper/paper_UG.tex/.pdf` (7 págs.), resumen del informe con derivación, resultados, comparaciones y figuras 1, 6, 8, 9, 10; bibliografía tomada de `informe/bibliografia.tex` (12 entradas). Las cifras se copiaron a mano del informe/`resultados/`: **si cambian los resultados hay que revisarlas** (no se generan automáticamente).
- **Página:** `docs/index.html` + `docs/build_docs.py` (copia figuras y PDF a `docs/`).
- **Tests:** 40 (17 previos + 8 Starobinsky + 4 simbólicos + 7 León + 2 manifests de figuras + 2 de procedencia).

## 16. Correcciones posteriores a la primera versión (2026-09-23)

Tras cerrar la primera versión se hizo una revisión crítica externa; su devolución no forma parte de este repositorio. Cada punto se verificó contra el texto y el código antes de aceptarlo o rechazarlo. Los tests pasaron antes y después (40 → 41); ningún número cambió. Esta sección registra los cambios; los límites que resultaron están incorporados en el paper, el informe (secs. 6.5, 9, 11), el README y `claims.yaml`.

| Punto | Verificación propia | Decisión / cambio |
|---|---|---|
| δQ = 0 ⇒ E₀ = 0 no es general | Correcto: `E₀ ∂ₓδφ = 0` también con `∂ₓδφ = 0`; δQ depende del gauge (`δQ̃ = δQ − Q̇ ξ⁰`, ley estándar de escalares; no se citó el enlace de Hu, no verificado) | Acotado en informe sec. 11.3, paper sec. 5, HTML, README, `claims.yaml`. `symbolic_checks.py::check_dQ_constraint` ahora declara `∂ₓδφ ≠ 0` y comprueba que la rama `∂ₓδφ = 0` deja E₀ libre |
| Λ₀ dimensionalmente mal en el paper | Verificado en `paper_UG.tex`; informe y `background.py::lambda0_from_initial` correctos | Corregido (`Λ₀ = 3H² − (ρ+Q)/M_P²`); `P_T` con `M_P²`; convención M_P declarada |
| Vínculo `√−g = 1` con `g₀₀ = −1` | Verificado en el paper; el informe ya usaba `f = a³` | Corregido en el paper; informe s06: `f` general |
| Acción cuadrática y normalización | Aceptado | Se declara como hipótesis de la realización efectiva (informe sec. 6.5, s07) |
| Equivalencia con V_eff | Aceptado | Acotado a escalar canónico con `Q(φ)` como ley local; `Q(N)` reconstruido solo sobre la rama; se retira «el sector escalar no queda abierto» |
| Fin de la inflación ≠ `V_eff = 0` | Verificado: `ε₁ = 3K/(K+U) = 1 ⇔ U = 2K` | Corregido en informe secs. 9 y 11; el criterio numérico no cambia |
| Igual N* / escala observacional; «no hay escala libre»; «señal/ruido»; «inobservable» | Aceptados | Redacción corregida (paper, informe, HTML, `claims.yaml`) |
| Starobinsky a igual k: «0.96–0.83» | **Discrepancia**: `numbers.json` (`staro_ratio_equal_k_last = 0.7699`) y el informe dicen 0.77; el 0.83 estaba mal en la sec. 13 de este archivo (errata mía) | Corregida esta sec. 13; ambos intervalos en HTML y paper |
| Reproducibilidad | Aceptado | `make all`; `test_numbers_regenerate_identically` regenera en directorio temporal; `manifest_informe.json` con `deps` y test; los `script` de los manifests de potenciales y León se validan; el test del notebook se declara de fuentes; `entorno_probado.txt` |
| Estado histórico vs. vigente | Aceptado | Marcas «histórico» en las secs. 1, 9, 9.3, 11 y 13 |

Decisiones **no** tomadas: no se exige SymPy a 2.º orden; no se resuelve el factor 3^{3/2}, el escenario 2 ni el recalentamiento. Pendientes antes de publicar: prueba desde un clon limpio, licencia, URL real del repositorio, autoría confirmada (se agregó «Javier Pineau» inferido del entorno) y quitar «borrador».

**AC-09 — alcance vigente:** las mutaciones reproducibles son las numéricas de C0. S1–S4 tienen pruebas de sus identidades, pero no mutantes simbólicos conservados; las menciones históricas a mutaciones simbólicas no constituyen evidencia reproducible.

**AC-13 — lectura vigente de CL7:** solo se conserva la comparación de la razón P_T(60)/P_T(50). Los comentarios históricos sobre toda la forma y la causa de los offsets son conjeturas; no resultados comprobados. El cambio de criterio del 10% absoluto al 3% de la razón es posterior y exploratorio.


## Cierre del 27 de septiembre de 2026

La reproducción vigente está en `../REPRODUCCION.md`. AC-25 añade ocho extremos y ocho índices a N*=50,60 con criterios exploratorios conservados de la sesión anterior (1e-5 relativo y 2e-5 absoluto); no se extienden a toda la tabla de radiación con Q. La malla reserva margen para arranque q=1000 y parada q=1e-4. Los extremos actuales UG/RG son 0.91446–0.34413 (cuadrático) y 0.94704–0.79629 (Starobinsky); las cifras anteriores de este registro son históricas.

AC-28: C1.1 usa el modo a tiempo finito de Baumann, [TASI Lectures, arXiv:0907.5424v2](https://arxiv.org/abs/0907.5424v2), ecs. 196 y 198, con la normalización tensorial del trabajo. Las ecs. 2.19, 2.23 y 2.24 de Martin–Ringeval–Vennin se verificaron en la copia conservada de arXiv:1303.3787v3 (encabezado: 3 Sep 2013). Se adopta fenomenológicamente el potencial de Starobinsky; no se presenta el origen conforme como verificado textualmente.
