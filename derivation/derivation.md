> Derivación compacta con historia de decisiones. El desarrollo final del espectro y los modos está en `../informe/s06_tensores.tex`, `s07_espectro.tex` y `s08_numerico.tex`; reproducción vigente en `../REPRODUCCION.md`.

# Derivación analítica: Friedmann y modos tensoriales en gravedad unimodular (UG) vs. RG

Etapa: derivación analítica. **Sin código.** Fecha: 2026-09-20.
Versión para leer con ecuaciones tipografiadas: `derivation.pdf`. Desde 2026-09-20 el PDF es un **apunte ampliado**: mismas ecuaciones y misma numeración que este archivo (comprobado automáticamente: las 43 ecuaciones numeradas son idénticas), más texto explicativo (qué es UG, diagrama del argumento, glosario, recuadros «En palabras» y «Para llevarse»). Este `.md` es la versión compacta y **no** incluye ese texto. Versión anterior del PDF/tex en `versiones_previas/`.

## 0. Cómo leer este documento

**Etiquetas de procedencia** (una por cada paso o ecuación):

| Etiqueta | Significa |
|---|---|
| **[PROPIA]** | Álgebra hecha a mano; los controles manuales se enumeran en la Sec. 7. El informe identifica además los cuatro controles simbólicos a primer orden. |
| **[CITADO X, Eq. n]** | Resultado tomado del paper `X` (ID de `PROVENANCE.md`) con el número de ecuación impreso en el PDF que leí. Lo releí contra el texto. |
| **[ESTÁNDAR]** | Resultado de libro de texto que uso tal cual y que **no** está respaldado por ninguna fuente que haya leído en `../provenance/PROVENANCE.md` (Mukhanov F1 y Baumann F2 figuran como no leídos). Queda pendiente verificarlo contra F1/F2. |
| **[SUPUESTO]** | Elección o hipótesis. |

**Decisiones que me diste** (respuestas a mis preguntas): (i) convención de la perturbación: **ambas en paralelo** (estándar y la de Fabris et al.); (ii) tiempo: **t cósmico**, con nota sobre el tiempo unimodular; (iii) **sí** incluir el segundo orden (acción cuadrática con el multiplicador de Lagrange); (iv) formulación: **multiplicador de Lagrange + volumen fiducial**.

**Convenciones.** Firma $(-,+,+,+)$, $c=\hbar=1$, $\kappa\equiv 8\pi G = 1/M_P^2$. Espacio plano. Índices latinos $i,j,k$ espaciales; $h_{ij}^2\equiv h_{ij}h_{ij}$ (suma sobre índices repetidos). Punto = $d/dt$ (tiempo cósmico); prima = $d/d\eta$ con $dt=a\,d\eta$; $\mathcal H = a'/a$.

**Alcance.** Se deriva: (1) Friedmann con inflatón en UG vs. RG; (2) ecuación de $h_k$ en ambos casos; (3) dónde actúa el vínculo. **No** se deriva el espectro $P_t$, ni el sector escalar, ni la cuantización (ver Sec. 8).

---

## 1. Marco de UG (formulación con multiplicador de Lagrange)

**1.1 Acción.** **[CITADO A3, Eq. (2.1)]** (equivalente a A1 Eq. (1) y B5 Eq. (1)):

$$S=\int\frac{1}{2\kappa}\Big[R\,\epsilon^{(g)}_{abcd}-2\lambda\big(\epsilon^{(g)}_{abcd}-\varepsilon_{abcd}\big)\Big]+S_m[g,\Psi]\tag{1.1}$$

$\varepsilon_{abcd}$ es una 4-forma de volumen **fiducial dada** (no dinámica) y $\lambda(x)$ el multiplicador de Lagrange. En coordenadas: $\epsilon^{(g)}=\sqrt{-g}\,d^4x$, $\varepsilon=f\,d^4x$.

**1.2 Tensor energía-impulso.** **[CITADO A3, Eq. (2.8)]**

$$T_{ab}=-\frac{2}{\sqrt{-g}}\frac{\delta S_m}{\delta g^{ab}}\tag{1.2}$$

**1.3 Ecuaciones de campo.** Variar respecto de $g^{ab}$, $\lambda$ y $\Psi$ da **[CITADO A3, Eqs. (2.5)–(2.7)]**:

$$G_{ab}+\lambda(x)\,g_{ab}=\kappa\,T_{ab}\tag{1.3}$$

$$\epsilon^{(g)}_{abcd}=\varepsilon_{abcd}\quad\Longleftrightarrow\quad \sqrt{-g}=f\tag{1.4}$$

(y $\delta S_m/\delta\Psi=0$ para la materia). Ojo: $\sqrt{-g}=f$ **no** es "$\sqrt{-g}=1$" salvo que se elijan coordenadas con $f=1$ (A3, nota al pie 1 y Sec. 3.2).

**1.4 Traza.** **[PROPIA]**, reproduce **[CITADO A3, Eqs. (2.9)–(2.10)]**. Con $g^{ab}G_{ab}=-R$ y $g^{ab}g_{ab}=4$, la traza de (1.3) es $-R+4\lambda=\kappa T$, luego

$$\lambda=\frac{R+\kappa T}{4}\tag{1.5}$$

y sustituyendo en (1.3):

$$R_{ab}-\tfrac14 g_{ab}R=\kappa\big(T_{ab}-\tfrac14 g_{ab}T\big)\tag{1.6}$$

**Lectura.** En RG con $\Lambda$ fijo, la traza $R=-\kappa T+4\Lambda$ es una ecuación con contenido dinámico. En UG la traza (1.5) **solo define** $\lambda$: se pierde una ecuación (10 → 9).

**1.5 No conservación.** **[PROPIA]** Aplicar $\nabla^a$ a (1.3) y usar la identidad de Bianchi $\nabla^aG_{ab}=0$:

$$\nabla_b\lambda=\kappa\,\nabla^aT_{ab}\tag{1.7}$$

Como $\lambda$ es un gradiente, el vector $J_b\equiv\nabla^aT_{ab}$ es cerrado y localmente $J_b=\nabla_bQ$ (A3 lo obtiene también por invariancia bajo difeos de volumen fijo, Eqs. (2.11)–(2.13), y de forma alternativa en Sec. 2.2). **[CITADO A3, Eqs. (2.13)–(2.15); A1, Eqs. (5)–(6)]**:

$$\nabla_aT^{ab}=\nabla^bQ\tag{1.8}$$

$$\lambda=\Lambda_0+\kappa\,Q(x)\tag{1.9}$$

con $\Lambda_0$ constante de integración. Equivalente: $\nabla_a\big(T^{ab}-g^{ab}Q\big)=0$ (1.10). $Q$ es un **escalar** por construcción.

**Dos casos** (A3 Sec. 3.1; B5; A1 texto tras Eq. (6)):
- **UG conservativa**, $\nabla_aT^{ab}=0$: $Q=$ cte, $\lambda=\Lambda_0$ (o se absorbe en $\Lambda_0$). Las ecuaciones son las de RG con constante cosmológica $\Lambda_0$, que no aparece en la acción sino que es constante de integración.
- **UG no conservativa**: $Q(x)$ variable. Es el caso de A1 y A2.

---

**Alcance variacional.** Una acción de materia canónica covariante, al imponer su ecuación de Euler–Lagrange, conserva T y exige Q constante. El caso Q variable de este trabajo añade una transferencia fenomenológica; no se deriva de esa acción canónica. La acción TT estándar y el estado de Bunch–Davies se adoptan como hipótesis efectivas para normalizar la amplitud.

## 2. Fondo cosmológico: Friedmann en UG vs. RG

**2.1 Métrica y vínculo.** **[PROPIA]** con $ds^2=-N^2dt^2+a^2\,d\mathbf x^2$, el vínculo (1.4) es

$$\sqrt{-g}=N(t)\,a(t)^3=f(t)\tag{2.1}$$

Dada una $f$, el vínculo determina el lapse: $N=f/a^3$. **[CITADO A3, Sec. 3.2, Eqs. (3.10)–(3.12)]**: como (1.3) y (1.4) son covariantes, dada una solución en tiempo cósmico ($N=1$) basta reexpresar el volumen fiducial en esas coordenadas ($f=a^3$); es la **misma solución**, no otra. Con $N=1$:

$$ds^2=-dt^2+a^2\,d\mathbf x^2,\qquad f=a^3\tag{2.2}$$

**[SUPUESTO, decisión (ii)]** Trabajo en $t$ cósmico. La misma solución en coordenada unimodular $T$ (con $dT=a^3dt$, $\sqrt{-g}=1$) es **[CITADO A3, Eq. (3.12)]**:

$$ds^2=-a^{-6}\,dT^2+a^2\,d\mathbf x^2\tag{2.3}$$

**2.2 Geometría.** **[PROPIA]**, resultado **[ESTÁNDAR]**. Para (2.2), $\Gamma^0_{ij}=a\dot a\,\delta_{ij}$ y $\Gamma^i_{0j}=H\delta^i_j$. Entonces $R_{00}=-3(\dot H+H^2)$, $R_{ij}=a^2(\dot H+3H^2)\delta_{ij}$, $R=6(\dot H+2H^2)$, y

$$G^0{}_0=-3H^2,\qquad G^i{}_j=-(2\dot H+3H^2)\,\delta^i_j\tag{2.4}$$

**2.3 Materia: inflatón estándar.** **[ESTÁNDAR]** $S_m=\int\sqrt{-g}\,[-\tfrac12(\partial\phi)^2-V(\phi)]$ da $T_{ab}=\partial_a\phi\,\partial_b\phi-g_{ab}\big[\tfrac12(\partial\phi)^2+V\big]$. En el fondo homogéneo:

$$\rho=\tfrac12\dot\phi^2+V,\quad p=\tfrac12\dot\phi^2-V,\quad \rho+p=\dot\phi^2,\quad T^0{}_0=-\rho,\quad T^i{}_j=p\,\delta^i_j\tag{2.5}$$

**2.4 Friedmann en UG.** **[PROPIA]** Componentes mixtas de (1.3), con $\bar\lambda(t)=\Lambda_0+\kappa Q(t)$ (1.9). Componente $00$: $-3H^2+\bar\lambda=-\kappa\rho$. Componente $ij$: $-(2\dot H+3H^2)+\bar\lambda=\kappa p$. Es decir,

$$3H^2=\kappa\rho+\bar\lambda,\qquad 2\dot H+3H^2=-\kappa p+\bar\lambda\tag{2.6}$$

Con (2.5):

$$\boxed{\,3M_P^2H^2=\tfrac12\dot\phi^2+V+Q+\Lambda_0M_P^2\,}\tag{2.7}$$

$$\boxed{\,\dot H=-\frac{\dot\phi^2}{2M_P^2}\,}\tag{2.8}$$

(2.8) sale de restar las dos ecuaciones (2.6): $2\dot H=-\kappa(\rho+p)$. **[CITADO A1, Eqs. (9)–(10)]** coinciden (con $\Lambda_*\equiv\Lambda_0$). **[CITADO A1, Eq. (57)]** subraya que la relación análoga en tiempo conforme "is independent of $Q$ explicitly".

**Continuidad.** **[PROPIA]** Derivar (2.7) y usar (2.8): $\dot\rho+\dot Q+3H(\rho+p)=0$, es decir $\dot\rho+3H(\rho+p)=-\dot Q$. **[CITADO A1, Eq. (11)]**. Es consistente con (1.8): la componente $b=0$ da $\dot\rho+3H(\rho+p)=-\dot Q$ (uso $\nabla_aT^{a0}=\dot\rho+3H(\rho+p)$ y $\nabla^0Q=-\dot Q$).

**$Q$ como fluido.** **[PROPIA]** De (1.10), $T^{ab}_{\rm ef}=T^{ab}-g^{ab}Q$: $\rho_Q=Q$ y $p_Q=-Q$, o sea $w_Q=-1$ pero con densidad **variable**.

**Ecuación del inflatón.** **[PROPIA]** Como $\dot\rho_\phi+3H(\rho_\phi+p_\phi)=\dot\phi(\ddot\phi+3H\dot\phi+V')$, si **toda** la no conservación se atribuye al inflatón:

$$\ddot\phi+3H\dot\phi+V'(\phi)=-\frac{\dot Q}{\dot\phi}\tag{2.9}$$

Si $Q$ es constante (UG conservativa) se recupera la ecuación de Klein–Gordon estándar. **[SUPUESTO del ejemplo numérico]**: (2.9) supone que $Q$ intercambia energía solo con el inflatón. A2 (Eq. (38)) hace otra cosa: el inflatón se conserva y $Q$ alimenta a un fluido de radiación. **Nada de lo que sigue en las Secs. 3–6 depende de esto**, porque solo entra el total.

**2.5 Friedmann en RG.** **[ESTÁNDAR]**, misma álgebra con $\lambda\to\Lambda$ constante (o $0$):

$$3M_P^2H^2=\tfrac12\dot\phi^2+V\;(+\Lambda M_P^2),\qquad \dot H=-\frac{\dot\phi^2}{2M_P^2},\qquad \ddot\phi+3H\dot\phi+V'=0\tag{2.10}$$

**2.6 Constante de integración.** **[PROPIA]** Evaluar (2.7) en $t_{\rm ini}$:

$$\Lambda_0=3H_{\rm ini}^2-\frac{\rho_{\rm ini}+Q_{\rm ini}}{M_P^2}\tag{2.11}$$

**[CITADO A1, Eq. (12)]**. $\Lambda_0$ lo fijan las condiciones iniciales, no la acción.

**2.7 Primer parámetro de flujo de Hubble.** **[PROPIA]** $\epsilon_1\equiv-\dot H/H^2=\dot\phi^2/(2M_P^2H^2)$. Con (2.7):

$$\epsilon_1^{\rm UG}=\frac{3\dot\phi^2}{\dot\phi^2+2\,(V+Q+\Lambda_0M_P^2)},\qquad \epsilon_1^{\rm RG}=\frac{3\dot\phi^2}{\dot\phi^2+2V}\tag{2.12}$$

La aceleración ($\epsilon_1<1$) equivale a $\dot\phi^2<V+Q+\Lambda_0M_P^2$. **[CITADO A2, texto tras Eq. (38)]** da la condición "$Q+V>2X$" con $X=\dot\phi^2/2$: coincide para $\Lambda_0=0$.

Para un fluido perfecto $p=w\rho$: $\dot H=-(1+w)\rho/(2M_P^2)$ y, con $\Lambda_0=0$ y $\Gamma\equiv Q/\rho$,

$$\epsilon_1=\frac{3(1+w)}{2(1+\Gamma)}\tag{2.13}$$

**[CITADO A1, Eq. (15)]**. Reproduce el caso de A1 (radiación: $\epsilon_1=2/(1+\Gamma)$).

La aproximación (2.14) exige KG conservativa y Q constante para el único escalar receptor. Con ley local fija U=V+Q(phi)+Lambda0 MP², se usan U y Uprime. El código integra la ecuación completa con fuente para Q(N).

**2.8 Slow-roll (aproximación, no exacta).** **[PROPIA]**, **[SUPUESTO]**: $|\ddot\phi|\ll|3H\dot\phi|$ y ecuación de Klein–Gordon estándar. Entonces $\dot\phi\simeq-V'/3H$ y

$$H^2\simeq\frac{V+Q+\Lambda_0M_P^2}{3M_P^2},\qquad \epsilon_1\simeq\frac{M_P^2}{2}\left(\frac{V'}{V+Q+\Lambda_0M_P^2}\right)^2\tag{2.14}$$

Con $Q$ constante, esto es RG con $V\to V+\text{cte}$. Es el resultado cualitativo de **[CITADO B7 (solo abstract)]**: "inflation proceeds as usual" con las ecuaciones sin traza.

**Cuadro comparativo del fondo**

| | RG | UG conservativa ($Q$ cte) | UG no conservativa |
|---|---|---|---|
| $3M_P^2H^2$ | $\rho_\phi\,(+\Lambda M_P^2)$ | $\rho_\phi+\Lambda_0M_P^2$ | $\rho_\phi+Q(t)+\Lambda_0M_P^2$ |
| $\dot H$ | $-\dot\phi^2/2M_P^2$ | igual | **igual** |
| Origen de la constante | parámetro de la acción | integración, (2.11) | integración; $Q(t)$ libre |
| Ecuación del inflatón | KG estándar | KG estándar | (2.9) si $Q$ se acopla al inflatón |
| Equivalencia con RG | — | **exacta**, $\Lambda=\Lambda_0$ | no: $H(t)$ distinto para el mismo $V$ |

---

## 3. Modos tensoriales sobre el fondo

**3.1 Perturbación.** **[SUPUESTO, decisión (i): ambas]** Métrica $g_{00}=-1$, $g_{0i}=0$ y

$$g_{ij}=a^2(\delta_{ij}+h_{ij}),\qquad h_{ii}=0,\ \ \partial_ih_{ij}=0\tag{3.1}$$

Variable de Fabris et al.: $\hat h_{ij}\equiv\delta g_{ij}=a^2h_{ij}$ (3.2) **[CITADO C4, Sec. GW]**.

**3.2 Invariancia de gauge.** **[PROPIA]**, coincide con **[CITADO A3, Eq. (5.10)]** y **[CITADO C4]**. Bajo $x^\mu\to x^\mu+\xi^\mu$, $\delta g_{ij}\to\delta g_{ij}-\mathcal L_\xi\bar g_{ij}$ con $\mathcal L_\xi\bar g_{ij}=2a\dot a\,\xi^0\delta_{ij}+a^2(\partial_i\xi_j+\partial_j\xi_i)$. Descomponiendo $\xi_i=\partial_i\xi+\xi^V_i$ con $\partial_i\xi^V_i=0$, esto contiene solo partes escalares ($\propto\delta_{ij}$, $\partial_i\partial_j\xi$) y vectoriales ($\partial_{(i}\xi^V_{j)}$): **no hay parte TT**. Luego $h_{ij}$ es invariante de gauge a primer orden, y no hay ninguna elección de gauge que hacer para los tensores. En UG los difeos permitidos están además restringidos a $\nabla_a\xi^a=0$ (A3), lo que no afecta a este argumento.

**3.3 Vínculo linealizado.** **[PROPIA]** $\delta\sqrt{-g}=\tfrac12a^3h_{ii}=0$. Para modos TT el vínculo (1.4) se cumple **idénticamente** a primer orden: no restringe $h_{ij}$ ni quita libertad. Coincide con **[CITADO C4, Eq. (34)]** ("already encoded in the condition to have pure tensorial modes"), **[CITADO C1, Conclusiones]** y **[CITADO C3, Sec. 5]**.

**3.4 Geometría a primer orden.** **[PROPIA]** Con (3.1) y $\delta\ln\sqrt{\gamma}=O(h^2)$ (porque ${\rm tr}\,h=0$):

$$\Gamma^0{}_{ij}=a^2\!\Big[H(\delta_{ij}+h_{ij})+\tfrac12\dot h_{ij}\Big],\quad \Gamma^i{}_{0j}=H\delta_{ij}+\tfrac12\dot h_{ij},\quad \Gamma^i{}_{jk}=\tfrac12(\partial_jh_{ik}+\partial_kh_{ij}-\partial_ih_{jk})\tag{3.3}$$

Con $R_{ij}=\partial_\mu\Gamma^\mu_{ij}-\partial_j\Gamma^\mu_{i\mu}+\Gamma^\mu_{\mu\lambda}\Gamma^\lambda_{ij}-\Gamma^\mu_{j\lambda}\Gamma^\lambda_{i\mu}$:

- $\partial_\mu\Gamma^\mu_{ij}=a^2\big[(2H^2+\dot H)(\delta+h)_{ij}+2H\dot h_{ij}+\tfrac12\ddot h_{ij}\big]-\tfrac12\nabla^2h_{ij}$,
- $\Gamma^\mu_{\mu\lambda}\Gamma^\lambda_{ij}=3Ha^2\big[H(\delta+h)_{ij}+\tfrac12\dot h_{ij}\big]$,
- $\Gamma^\mu_{j\lambda}\Gamma^\lambda_{i\mu}=2a^2\big[H^2(\delta+h)_{ij}+H\dot h_{ij}\big]$,
- $\partial_j\Gamma^\mu_{i\mu}=0$.

Sumando:

$$R_{ij}=a^2(\dot H+3H^2)(\delta_{ij}+h_{ij})+\tfrac12a^2\big(\ddot h_{ij}+3H\dot h_{ij}\big)-\tfrac12\nabla^2h_{ij}\tag{3.4}$$

Además $R_{00}$, $R_{0i}$ y $R$ **no** se perturban a primer orden ($R_{0i}=0$ por transversalidad; ${\rm tr}\,h=0$ en el resto). Con $g^{ik}=a^{-2}(\delta-h)_{ik}$, el tensor mixto:

$$G^i{}_j=-(2\dot H+3H^2)\,\delta^i_j+\tfrac12\Big(\ddot h_{ij}+3H\dot h_{ij}-\frac{\nabla^2h_{ij}}{a^2}\Big)\tag{3.5}$$

**3.5 Proyección TT de la ecuación de campo.** **[PROPIA]** Perturbando (1.3) en forma mixta, $G^i{}_j+\lambda\,\delta^i_j=\kappa T^i{}_j$, a primer orden:

$$\delta G^i{}_j+\delta\lambda\,\delta^i_j=\kappa\,\delta T^i{}_j\tag{3.6}$$

$\lambda$ es un escalar (1.9), así que $\delta\lambda\,\delta^i_j$ es **puramente traza** y desaparece al proyectar sobre TT. Para el inflatón, $T^i{}_j=\partial^i\phi\,\partial_j\phi-\delta^i_j[\dots]$: $\partial_i\phi$ es de primer orden (perturbación escalar), luego $\partial^i\phi\,\partial_j\phi$ es de segundo orden, y $g^{00}\dot\phi^2$ no cambia. Por lo tanto (para un fluido perfecto pasa lo mismo, $u^i$ es de primer orden):

$$\delta T^i{}_j\big|_{\rm TT}=0\tag{3.7}$$

En forma mixta los términos de fondo $\propto\delta^i_j$ **se cancelan exactamente** por la ecuación de fondo $(ij)$ de (2.6), cualquiera sea $\bar\lambda(t)$. Queda:

$$\boxed{\;\ddot h_{ij}+3H\dot h_{ij}-\frac{\nabla^2h_{ij}}{a^2}=0\;}\tag{3.8}$$

En Fourier, $h_{ij}=\sum_{\lambda=+,\times}\int\!\frac{d^3k}{(2\pi)^3}\,h_k^\lambda(t)\,e^\lambda_{ij}(\mathbf k)\,e^{i\mathbf k\cdot\mathbf x}$, con $e^\lambda_{ij}$ constantes:

$$\boxed{\;\ddot h_k+3H\dot h_k+\frac{k^2}{a^2}h_k=0\;}\tag{3.9}$$

Tiempo conforme y variable canónica: **[PROPIA]**

$$h_k''+2\mathcal H\,h_k'+k^2h_k=0\tag{3.10}$$

$$v_k\equiv a\,h_k:\qquad v_k''+\Big(k^2-\frac{a''}{a}\Big)v_k=0\tag{3.11}$$

La velocidad de propagación es $c_T=1$ (el coeficiente de $k^2$ en (3.11) es 1).

**3.6 RG.** **[PROPIA]** Con $G^i{}_j+\Lambda\,\delta^i_j=\kappa T^i{}_j$ ($\Lambda$ constante) los pasos son **literalmente los mismos**: se obtiene (3.8)–(3.11). La **única** diferencia entre UG y RG es qué función $H(t)$ entra en (3.9): la que resuelve (2.7)–(2.8) en UG y (2.10) en RG.

**3.7 Traducción a la variable de Fabris et al.** **[PROPIA]** Sustituir $h=\hat h/a^2$ en (3.9), con $\dot h=(\dot{\hat h}-2H\hat h)/a^2$ y $\ddot h=(\ddot{\hat h}-4H\dot{\hat h}-2\dot H\hat h+4H^2\hat h)/a^2$, y multiplicar por $a^2$:

$$\ddot{\hat h}_k-H\dot{\hat h}_k-2(\dot H+H^2)\hat h_k+\frac{k^2}{a^2}\hat h_k=0\tag{3.12}$$

**[CITADO C4, Eq. (37)]**: forma idéntica. Cierra el punto abierto O3 de `PROVENANCE.md` a mano (queda pendiente la verificación simbólica). Que C4 obtenga "exactly the equation for gravitational waves in GR" es exactamente lo que muestra (3.6). Sus diferencias con ΛCDM vienen "only [from] the background functions $H$ and $\dot H$".

**3.8 Nota: tiempo unimodular.** **[PROPIA]** Con $dT=a^3dt$ (métrica (2.3)), $d/dt=a^3\,d/dT$ y $H=a^2a_T$, la ecuación (3.9) se convierte en

$$h_{TT}+6\frac{a_T}{a}h_T+\frac{k^2}{a^8}h=0\tag{3.13}$$

Es la misma física reetiquetada. Por eso el vínculo $\sqrt{-g}=1$ no cambia nada por sí mismo (A3 Sec. 3.2).

**3.9 Consistencia con $\nabla_aT^{ab}=\nabla^bQ$.** **[PROPIA]** La componente $b=j$ a primer orden, para TT: $\nabla_aT^a{}_j=\partial_jp+\Gamma^\mu_{\mu k}T^k{}_j-\Gamma^\lambda_{\mu j}T^\mu{}_\lambda=0$, porque $\Gamma^\mu_{\mu k}=\partial_k\ln\sqrt\gamma=0$, $T^0{}_k=0$ y $\Gamma^k_{kj}p=0$. Igual a $\partial_jQ=0$. La no conservación **no genera ninguna condición sobre TT**.

---

## 4. Acción cuadrática y el vínculo a segundo orden

Objetivo: expansión formal compatible con (3.8), condicionada a la acción efectiva de materia adoptada; no es una demostración independiente para Q variable y control del término del vínculo a segundo orden, que **no** es trivial. Uso $N=1$, $f=a^3$ (2.2).

**4.1 Vínculo a segundo orden.** **[PROPIA]** Con $M=\delta+h$: $\sqrt{\det M}=\exp\big[\tfrac12\,{\rm tr}\ln(1+h)\big]=1-\tfrac14h_{ij}^2+O(h^3)$. Entonces

$$\sqrt\gamma=a^3\big(1-\tfrac14h_{ij}^2\big)\ \Rightarrow\ \sqrt{-g}-f=-\tfrac14a^3h_{ij}^2\neq0\tag{4.1}$$

A segundo orden **el vínculo sí actúa sobre $h$**: (1.4) exige que un escalar de segundo orden compense $-\tfrac14 a^3h^2_{ij}$. El multiplicador no corrige el determinante de una métrica dada: hay que completar la métrica a segundo orden o usar g_ij=a²(exp h)_ij con tr h=0.

**4.2 Parte de Einstein–Hilbert.** **[ESTÁNDAR]** En forma ADM con $N=1$, $S_{EH}=\frac1{2\kappa}\int\sqrt\gamma\,[{}^{(3)}R+K_{ij}K^{ij}-K^2]$ (hasta un término de borde). **[PROPIA]** Con $K^i{}_j=H\delta^i_j+\tfrac12(M^{-1}\dot h)_{ij}$:

$$K=3H-\tfrac14\tfrac{d}{dt}h_{ij}^2,\qquad K^i{}_jK^j{}_i-K^2=-6H^2+H\tfrac{d}{dt}h_{ij}^2+\tfrac14\dot h_{ij}^2\tag{4.2}$$

Multiplicando por $\sqrt\gamma$ e integrando por partes $a^3H\,\frac{d}{dt}h^2_{ij}\to-(3a^3H^2+a^3\dot H)h^2_{ij}$:

$$\sqrt\gamma\,(K_{ij}K^{ij}-K^2)\simeq a^3\Big[-6H^2-\big(\tfrac32H^2+\dot H\big)h_{ij}^2+\tfrac14\dot h_{ij}^2\Big]\tag{4.3}$$

El término gradiente viene de $\sqrt\gamma\,{}^{(3)}R$. **[ESTÁNDAR]** $\int\sqrt\gamma\,{}^{(3)}R\to-\tfrac14a\,(\partial_kh_{ij})^2$ (TT, tras integrar por partes). No lo derivo aquí; su coeficiente queda **fijado por consistencia con (3.8)** (ver 4.5) y es pendiente de verificar en F1/F2.

**4.3 Materia.** **[PROPIA]** Para $\phi$ homogéneo, $L_m=p$ y $\sqrt{-g}\,L_m=a^3(1-\tfrac14h_{ij}^2)\,p$:

$$S_m^{(2)}\supset-\tfrac14a^3\,p\,h_{ij}^2\tag{4.4}$$

**4.4 Término del vínculo.** **[PROPIA]** Con $\lambda=\bar\lambda+\delta\lambda$ y (4.1): $-\frac1\kappa\lambda(\sqrt{-g}-f)$. El término $\delta\lambda\cdot\delta_1\sqrt{-g}$ se anula para TT (Sec. 3.3). Queda:

$$S_\lambda^{(2)}=+\frac{\bar\lambda}{4\kappa}\,a^3h_{ij}^2\tag{4.5}$$

**4.5 Suma de los términos en $h^2_{ij}$ (sin derivadas).** **[PROPIA]** De (4.3)·$\frac1{2\kappa}$, (4.4) y (4.5):

$$\frac{a^3h_{ij}^2}{4\kappa}\Big[-3H^2-2\dot H-\kappa p+\bar\lambda\Big]=0\tag{4.6}$$

**se anula** por la ecuación de fondo $(ij)$ de (2.6), $2\dot H+3H^2=-\kappa p+\bar\lambda$. Aquí $\bar\lambda=\Lambda_0+\kappa Q(t)$ **entra y se cancela**: el término del vínculo a segundo orden (4.5) participa en la cancelación de modo que no queda un "término de masa". En RG con $\Lambda$: idéntico con $\bar\lambda\to\Lambda$.

**Acción cuadrática resultante** (con el término gradiente [ESTÁNDAR]):

$$S^{(2)}_{TT}=\frac{M_P^2}{8}\int dt\,d^3x\;\Big[a^3\dot h_{ij}\dot h_{ij}-a\,(\partial_kh_{ij})^2\Big]\tag{4.7}$$

**Chequeos.** (a) Variar (4.7) da $\ddot h_{ij}+3H\dot h_{ij}-\nabla^2h_{ij}/a^2=0$, que es (3.8), deducida antes por otro camino (ecuaciones de campo). El coeficiente del gradiente es el único que quedó por consistencia; el cinético $\frac14a^3\dot h^2$ y la cancelación de masa sí salen de la álgebra de arriba. (b) **[CITADO D1, Eq. (4.8)]**: $S_t=\frac{M_P^2}{8}\int d\eta\,d^3x\,a^2[(t_{ij}')^2-(\nabla t_{ij})^2]$ (con curvatura nula) en la UG *generalizada*. Pasando (4.7) a tiempo conforme se obtiene exactamente eso.

**4.6 Variable canónica.** **[PROPIA]**, **[SUPUESTO, normalización]** Con $e^\lambda_{ij}e^{\lambda'*}_{ij}=2\delta_{\lambda\lambda'}$: $S^{(2)}=\frac{M_P^2}{4}\sum_\lambda\int d\eta\,\frac{d^3k}{(2\pi)^3}\,a^2\big[|h'_\lambda|^2-k^2|h_\lambda|^2\big]$. Con $v_\lambda=\frac{aM_P}{\sqrt2}h_\lambda$ y una integración por partes:

$$S^{(2)}=\frac12\sum_\lambda\int d\eta\,\frac{d^3k}{(2\pi)^3}\Big[|v_\lambda'|^2-\Big(k^2-\frac{a''}{a}\Big)|v_\lambda|^2\Big]\tag{4.8}$$

Esta normalización se usa en el cálculo de $P_t$ del informe, sección 7, y en `../codigo/modes.py`.

**4.7 Observación.** **[PROPIA]** Con la parametrización exponencial $g_{ij}=a^2(e^h)_{ij}$, $\det e^h=e^{{\rm tr}\,h}=1$, luego $\sqrt{-g}=a^3$ **exactamente**: el vínculo se cumple a todo orden y no aparece el término (4.5). La diferencia con la parametrización $\delta+h$ es un término de segundo orden que multiplica la ecuación de fondo, así que $S^{(2)}$ en capa es la misma. Es un buen ejemplo de una elección que **no** cambia nada.

---

## 5. Dónde el vínculo modifica algo y dónde no

| Punto | ¿Modifica? | Detalle | Ecs. |
|---|---|---|---|
| Estatus de $\lambda$ | **Sí** | Deja de ser parámetro de la acción: $\lambda=\Lambda_0+\kappa Q$, con $\Lambda_0$ de integración | (1.9), (2.11) |
| Ecuación de la traza | **Sí** | Pasa a definir $\lambda$; se pierde una ecuación (10→9) | (1.5) |
| Conservación de $T_{ab}$ | **Sí (permite violarla)** | En RG es un teorema; en UG es hipótesis adicional | (1.8) |
| $H^2$ (Friedmann) | **Sí, si $Q\neq$ cte** | $Q(t)$ suma como fluido $w=-1$ de densidad variable | (2.7) |
| $H^2$ con $Q$ cte | **No** | Equivale a RG con $\Lambda=\Lambda_0$ | (2.7), (2.10) |
| $\dot H$ | **No** | $Q$ no entra | (2.8) |
| $\epsilon_1$ y slow-roll | **Sí, vía $H^2$** | $\epsilon_1$ depende de $V+Q+\Lambda_0M_P^2$ | (2.12), (2.14) |
| Vínculo a 1.er orden para TT | **No** | $\delta\sqrt{-g}=\tfrac12a^3h_{ii}=0$ | Sec. 3.3 |
| Gauge de $h_{ij}$ | **No** | TT invariante de gauge | 3.2 |
| Fuente de TT | **No** | $Q$ escalar; $\delta T^i{}_j|_{TT}=0$ | (3.6)–(3.7) |
| **Ecuación de $h_k$** | **No** | Igual que RG (3.9), con $c_T=1$ | (3.8)–(3.11) |
| Vínculo a 2.º orden para TT | **Sí, pero se cancela** | $-\tfrac14a^3h^2_{ij}$, requiere completar la métrica; no lo absorbe $\bar\lambda$ | (4.1), (4.6) |
| Acción cuadrática | **Hipótesis efectiva** | Se adopta la de RG | (4.7) |
| Conclusión | El vínculo **entra en TT solo a través de $H(t)$** | vía Friedmann | (2.7), (3.9) |

**Respuesta a tu punto 3, en una línea:** el vínculo modifica el fondo cuando hay difusión, **no** modifica la ecuación lineal de los modos TT bajo las hipótesis indicadas; la acción estándar se adopta como hipótesis efectiva para su amplitud, que depende de $Q$ únicamente a través de $H(t)$. Esto coincide con lo que dice la literatura (C1, C3, C4, D1; ver `RESUMEN_CONSENSO.md`), pero aquí queda derivado.

---

## 6. Resultado en una tabla: ecuaciones en ambos casos

| | RG | UG (con inflatón, $Q$ general) |
|---|---|---|
| Friedmann | $3M_P^2H^2=\tfrac12\dot\phi^2+V\,(+\Lambda M_P^2)$ | $3M_P^2H^2=\tfrac12\dot\phi^2+V+Q+\Lambda_0M_P^2$ |
| $\dot H$ | $-\dot\phi^2/2M_P^2$ | $-\dot\phi^2/2M_P^2$ |
| Modos TT | $\ddot h_k+3H\dot h_k+\frac{k^2}{a^2}h_k=0$ | $\ddot h_k+3H\dot h_k+\frac{k^2}{a^2}h_k=0$ |
| Acción TT | $\frac{M_P^2}{8}\int a^3[\dot h^2-(\partial h)^2/a^2]$ | igual |

---

## 7. Chequeos hechos a mano (ninguno con código)

| ID | Chequeo | Resultado |
|---|---|---|
| H1 | (2.6) con $\bar\lambda=\Lambda_0+\kappa Q$ vs. A1 Eqs. (9)–(10) | Coincide |
| H2 | Continuidad derivada de (2.7)–(2.8) vs. (1.8) con signos ($\nabla^0Q=-\dot Q$) y vs. A1 Eq. (11) | Coincide |
| H3 | (2.13) vs. A1 Eq. (15); (2.12) vs. la condición "$Q+V>2X$" de A2 | Coincide |
| H4 | $G^i{}_j$ a primer orden (3.5): reproduce el fondo y el resultado estándar $\ddot h+3H\dot h+k^2h/a^2=0$ | Coincide |
| H5 | (3.9) → (3.12) vs. C4 Eq. (37) | Coincide (con $\hat h=a^2h$) |
| H6 | (3.9) → (3.10) y (3.11): sustitución $h=v/a$ | Coincide con $a''/a=\mathcal H'+\mathcal H^2$ |
| H7 | Cancelación de masa (4.6) usando (2.6) | Se anula |
| H8 | EOM de (4.7) vs. (3.8); (4.7) en $\eta$ vs. D1 Eq. (4.8) | Coincide |

**Lo que estos chequeos NO cubren:** no son verificación simbólica ni numérica; el término gradiente de (4.7) es [ESTÁNDAR] y solo está chequeado por consistencia con (3.8); y F1/F2 (libros) no fueron leídos.

---

## 8. Cuentas adicionales que considero necesarias (pediste que te las aclare)

**Incluidas arriba, aunque no las pediste explícitamente:**

1. **Consistencia con la no conservación** (3.9): que $\nabla_aT^{ab}=\nabla^bQ$ no impone nada sobre TT.
2. **Vínculo a segundo orden** (4.1)–(4.6): el punto donde el vínculo *sí* toca a los tensores, y por qué no tiene efecto físico.
3. **Traducción a la variable de Fabris** (3.12): para conectar con C4 y cerrar O3.
4. **$\epsilon_1$ en términos de $V$, $Q$** (2.12), (2.14): es por donde $Q$ entra en cualquier observable tensorial.
5. **Forma conforme y variable canónica** (3.10)–(3.11), (4.8).

## Estado de las extensiones

La cuantización tensorial y la normalización están implementadas en `../codigo/modes.py` y desarrolladas en `../informe/s07_espectro.tex`; C1.1 contrasta de Sitter a tiempo finito. Se adoptaron transferencia al inflatón, polarizaciones con e·e=2 y P_T definido por la varianza de h_ij; la radiación con Q es un modelo separado.

Las cuatro comprobaciones de `../codigo/symbolic_checks.py` verifican identidades a primer orden. No verifican toda la acción cuadrática ni conservan mutantes simbólicos. Siguen abiertos el sector escalar con difusión, el factor 3^(3/2), la justificación completa de la acción efectiva y el recalentamiento. Son límites científicos, no pasos de reproducción pendientes. Procedimiento vigente: `../REPRODUCCION.md`.
