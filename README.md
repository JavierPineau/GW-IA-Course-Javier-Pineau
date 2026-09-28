# Espectro tensorial primordial en gravedad unimodular con difusión (UG) vs RG

Trabajo final del curso GW IA. **Pregunta:** ¿cambia el espectro de potencia tensorial primordial `P_T(k)` cuando, en gravedad unimodular, el tensor energía-impulso no se conserva (`∇ₐTᵃᵇ = ∇ᵇQ`)?

**Respuesta corta.** (1) Sobre un fondo FLRW plano la ecuación de los modos tensoriales es la de RG y `Q` entra solo por `H(t)` (bajo la hipótesis de materia sin parte TT; derivada a mano, verificada con SymPy a primer orden; el segundo orden solo a mano, y la acción tensorial estándar se adopta como hipótesis de la realización efectiva, de la que depende la normalización). (2) Con un inflatón y `Q(N)` prescripta, el signo de la diferencia UG–RG en el cuadrático depende del criterio (igual `k`: UG suprime `P_T`; igual N*: lo aumenta ×1.5); con Starobinsky es ~10 % (0.90 a igual N*; 0.947–0.796 a igual `k`). (3) Para un escalar canónico con `Q` especificada como ley local `Q(φ)`, las ecuaciones de UG son las de RG con `V_eff` (fondo verificado simbólicamente; perturbaciones argumentadas a mano; con `Q(N)` reconstruida solo sobre la rama considerada); si se impone `δQ = 0` en el marco especificado y la perturbación del inflatón es inhomogénea, resulta `Q̇ = 0` (no se analizaron otros gauges ni perturbaciones uniformes). (4) Con el modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329) (radiación + `Q`, sin inflatón) `P_T` es el de RG con el mismo `H(N)`; `A_s` en el punto de referencia de Piccirilli–León sale +1.1 % sobre Planck con su fórmula escalar (×5.2 con la de arXiv:2202.04029): **el sector escalar no está derivado**, así que `A_s` y `r` son condicionales.

## Para presentar (gente)
- Página: [`docs/index.html`](docs/index.html) (abrir en el navegador; `make docs` la actualiza)
- **PDF en formato paper: [`paper_UG.pdf`](paper_UG.pdf)**
- Informe largo (desde lo elemental): [`informe/informe_UG.pdf`](informe/informe_UG.pdf)
- Derivación analítica (apunte ampliado): [`derivation/derivation.pdf`](derivation/derivation.pdf)

## Para máquinas: reproducir
El procedimiento único y vigente está en [REPRODUCCION.md](REPRODUCCION.md): creación del entorno, reproducción completa y ejecución del notebook. Desde el entorno activado, `make all PY=python` regenera resultados, ejecuta **47 pruebas**, compila los PDF y actualiza `docs/`.

Los comandos individuales que escriben `codigo/resultados/` pueden invalidar los hashes hasta regenerar las figuras y la procedencia. El entorno histórico está en `entorno_probado.txt`; la validación de esta continuación, en `validacion/CIERRE_20260927.md`.

## Estructura
| Carpeta | Contenido |
|---|---|
| `codigo/` | Python: fondos (`background.py`, `background_leon.py`), modos (`modes.py`), controles (`checks*.py`, `symbolic_checks.py`), scripts de resultados y figuras, tests, notebook `explorador_PT.ipynb`, `resultados/`, `figuras/` (ver `codigo/README.md`) |
| `provenance/` | `PROVENANCE.md` (procedencia de todo: literatura, decisiones, checks y sus límites, puntos abiertos O1–O8), `numbers.json` (valores, entradas, referencias y datasets), `claims.yaml` (afirmaciones y 10 figuras, con evidencia `archivo::función`), `validate_provenance.py` |
| `derivation/` | Derivación analítica: `.md` (compacta), `.tex/.pdf` (apunte ampliado) |
| `informe/` | Informe largo (`s01…s12`, apéndices) |
| `paper/` | Fuentes LaTeX del paper (el PDF compilado está en la raíz: `paper_UG.pdf`) |
| `literatura/` | `RESUMEN_CONSENSO.md` y `literatura_tools/` (scripts que verifican metadatos con Crossref/arXiv). Los PDF de papers descargados **no** se incluyen (derechos) |
| `docs/` | Página HTML para presentar |
| `REPRODUCCION.md` | Procedimiento vigente y alcance de las validaciones |
| `entorno_probado.txt` | Versiones con las que se corrió todo |

## Cómo está registrada la procedencia
`validate_provenance.py` realiza un **chequeo estructural**: campos requeridos, claves enlazadas y existencia de archivos/funciones citadas. No importa ni ejecuta los productores, no certifica la verdad de los claims y no comprueba la cobertura del HTML/PDF. Las citas textuales se conservan sin verificarlas. `test_numbers_regenerate_identically` comprueba sincronía del registro con resultados guardados; no reproduce por sí solo los cálculos numéricos. La ampliación de cobertura se documenta en AC-04 de `AUDITORIA_CONSOLIDADA.md`.

Cada resultado lleva su etiqueta (**PROPIA / CITADO / ESTÁNDAR / SUPUESTO**) y su control; las tolerancias y sus cambios posteriores están documentados. Los cambios de criterio hechos *después* de ver un fallo están declarados (`provenance/PROVENANCE.md` secs. 13–14; informe secs. 10.5 y 12.5). `make_provenance_numbers.py` registra salidas conservadas, entradas de configuración y referencias externas, distinguiendo su procedencia.

## Límites (léase antes de citar)
- Sector escalar de UG con difusión **no derivado**; factor `3^{3/2}` entre arXiv:2202.04029 y arXiv:2307.06329 sin resolver (O1/O5). `A_s`, `r` con UG son condicionales.
- La acción a segundo orden del sector tensorial y la equivalencia perturbativa UG = RG con `V_eff` no están verificadas simbólicamente; la acción tensorial estándar es una hipótesis de la realización efectiva (la ecuación de propagación no fija la normalización cuántica).
- La conclusión sobre `δQ = 0` (`Q̇ = 0`) vale para perturbaciones inhomogéneas del inflatón en el marco especificado; `δQ` depende del gauge y no se examinó la compatibilidad con las transformaciones permitidas de UG.
- Comparar a igual `N*` es una convención ilustrativa: no equivale a la misma escala observacional (falta el recalentamiento).
- `Q(N) = Q_i e^{-γN}` (modelo con inflatón) es una prescripción fenomenológica; el modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329) es el de la literatura del grupo. No se modela el recalentamiento.
- Starobinsky: solo la forma del potencial; `M` calibrada con `A_s` (no es validación); referencias verificadas solo en metadatos.
- Escenario 2 de arXiv:2307.06329 (`N_f ≈ 370`) no analizado.

## Licencia y datos
Los espectros se generan con el código; los valores de referencia externos (Planck y BICEP/Keck) están identificados en el registro. Licencia: pendiente de decisión del autor.

## Publicación
El contenido de esta carpeta está preparado para subir a la raíz del repositorio. Ver [PUBLICACION.md](PUBLICACION.md) para el alcance de los archivos incluidos.
