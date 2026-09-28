# ¿El vínculo de traza de UG afecta al sector tensorial (TT)? — estado de la literatura

*Resumen de la etapa de literatura, 2026-09-20. Cada afirmación remite a una fila de `PROVENANCE.md` (códigos A1, C1, …). Es lo que encontré, no una derivación propia.*

**Respuesta corta:** no hay ningún paper que haya encontrado que el sector TT se vea afectado por el vínculo unimodular. Lo que sí cambia es el **fondo** cuando se permite difusión `Q`, y por esa vía el espectro. Pero el espectro tensorial completo en UG con difusión **no está derivado en la literatura que leí**: se lo da por supuesto.

**1. Caso conservativo (`∇T=0`): consenso claro.** UG equivale a RG con Λ como constante de integración (B5, B6, A3, B8). Sobre perturbaciones, Basak et al. (C1) afirman que, por ser transversos y sin traza, los modos vectoriales y tensoriales "are not affected by the unimodular constraint". Cho–Singh (C3) llegan a lo mismo: la acción tensorial no depende del vínculo y `P_T` es el estándar. A nivel lineal, UG corresponde a `WTDiff` y RG a Fierz–Pauli, sin diferencias adicionales (B8). Bengochea et al. (A3) muestran además que la perturbación tensorial es invariante de gauge (Eq. 5.10) y que `√−g=1` es solo una elección de coordenadas.

**2. Caso no conservativo (difusión `Q`), tu (a) y (b).**
- *(a) Fondo:* `Q` entra en `H²` (`3M_P²H² = ρ+Q`) pero no en `Ḣ`, que solo ve `ρ+p` (A1 Eq. 57; C4). El fondo cambia porque `Q` modifica `H(t)` y con ello `ε₁`.
- *(b) Propagación TT:* Fabris et al. (C4, Eq. 37) obtienen para los modos tensoriales "exactly the equation for gravitational waves in GR", y la diferencia con ΛCDM viene solo de `H, Ḣ`. Chakraborty et al. (C5) encuentran que la suma de polarizaciones es la de RG. Barvinsky–Kolganov (D1) muestran que en la UG *generalizada* la acción tensorial también tiene la forma de RG; allí `r` cambia por el sector escalar (gravitón escalar extra), no por los tensores.

**3. Disenso, y por qué no toca a TT.** Gao et al. (C2), Alvarenga et al. (C6) y Linares Cedeño–Nucamendi (C7) hallan diferencias con RG, pero **en el sector escalar** (gauge, *shift*, Sachs–Wolfe); Basak et al. (C1) las atribuyen a la elección de gauge. Nadie reporta diferencias en TT.

**4. Lo que NO está hecho (esto define el proyecto).** León (A1) deriva solo el espectro escalar; Piccirilli–León (A2, Eq. 42) **adoptan** `r = 16 ε₁` sin derivarlo, citando a A1, que no tiene sector tensorial. Además `P_R` en A1 (Eq. 66) lleva un factor `3^{3/2}` que falta en A2 (Eq. 41), y si `P_t` fuera el de RG eso daría un `r` distinto de `16 ε₁` (hipótesis aritmética, ver O1–O2 en `PROVENANCE.md`, **sin verificar**). Las derivaciones existentes suponen radiación pura y `δQ=0`.

**Confianza y límites.** De ~10 papers relevantes leí el texto (completo o las secciones clave) y de otros ~20 solo abstract. No accedí a los originales de Henneaux–Teitelboim, Unruh ni Weinberg (paywall). La búsqueda pudo omitir trabajos sin arXiv. Que "nadie encontró diferencias en TT" es evidencia de consenso implícito, no de una verificación explícita de (b) en UG con difusión.
