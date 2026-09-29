# Prueba de reproducción con un agente sin historia — 28/09/2026

**Quién.** Una sesión de Claude Code (Opus 5.5) que trabajó sobre un clon recién hecho de `GW-IA-Course-Javier-Pineau`. No tenía contexto previo y usó solo lo que está en el repositorio. No editó ningún archivo versionado; los cambios que aparecen en `git status` son los que genera `make all`. No se hizo commit.

**Resultado en una línea.** Todos los pasos funcionaron tal como están escritos. `make all` terminó con salida 0 en 4 min 25 s y aprobó **47 pruebas**. Los ocho valores pedidos coinciden con el paper y son idénticos bit a bit a `provenance/numbers.json` y a lo guardado en `HEAD`. El notebook se ejecutó completo sin errores.

## Entorno

| | |
|---|---|
| Sistema operativo | Ubuntu 24.04.4 LTS, kernel 7.0.0-34-generic, x86_64 (32 núcleos, 29 GB de RAM) |
| Python | 3.12.3. `python3.12` resolvió a `~/anaconda3/bin/python3.12`, el primero del PATH; también existe `/usr/bin/python3.12` 3.12.3. Dentro del venv, pip 24.0 |
| TeX | XeTeX 3.141592653-2.6-0.999995 (TeX Live 2023/Debian) en `/usr/bin/xelatex`, con el paquete `texlive-full` ya instalado |
| make | GNU Make 4.3 |
| Paquetes | El `pip freeze` del venv es idéntico a `entorno_probado.txt` (106 paquetes). `pip check` no encontró conflictos |

## Pasos: qué funcionó tal como está escrito

| Paso (REPRODUCCION.md) | Resultado |
|---|---|
| `python3.12 -m venv .venv`, `. .venv/bin/activate`, `python -m pip install -r requirements.txt` | OK |
| `make all PY=python` | OK, salida 0. `reproduce`: 10/10 controles (cuadrático), 8/8 (Starobinsky), 7/7 (radiación con Q) y control de resolución aprobado (peor extremo 1.03e-6, peor índice 6.74e-7). `test`: **47 passed**, 14 warnings. `pdf`: los tres documentos compilaron sin referencias indefinidas. `docs`: OK |
| `git status` después de `make all` | Entre los archivos versionados cambiaron exactamente los que anuncia REPRODUCCION.md: 10 PDF de figuras, los 3 PDF de documentos, las copias en `docs/` y en la raíz, y los 4 manifiestos, que solo cambian en los hashes de esos PDF. Resultados, PNG, CSV, `numbers.json`, datasets y notebook quedaron idénticos. El texto del paper, del informe y de la derivación recompilados (`pdftotext`) es idéntico al de `HEAD` |
| Notebook: `ipykernel install ...` y `nbconvert --execute ...` (comando literal) | OK. Se ejecutaron las 19 celdas de código, sin errores y sin salida por stderr. 18 de 19 celdas dan una salida idéntica a la guardada; en la otra (la de los controles) solo cambian los tiempos impresos |

No falló ningún paso.

## Qué tuve que adivinar o resolver por mi cuenta

1. **Cuál `python3.12` usar.** Usé el primero del PATH, que es el de Anaconda. Funcionó, pero el venv queda construido sobre Anaconda y las instrucciones no dicen nada al respecto. Además, `validacion/reproduccion_20260928.md` registra `python3 -m venv`, mientras que REPRODUCCION.md indica `python3.12 -m venv`.
2. **Activación del entorno.** `make all PY=python` y los comandos del notebook suponen el venv activo en la misma shell. Como mis comandos corren cada uno en una shell nueva, tuve que anteponer `. .venv/bin/activate` a cada uno. Sin eso, `python` sería el Python base de Anaconda (no probé qué pasa en ese caso).
3. **Paquetes de TeX.** Ya estaban instalados (`texlive-full`), así que no pude comprobar cuál es el mínimo necesario. Según los `.sty` que cargan los `.tex`, los paquetes Debian que los proveen son `texlive-xetex`, `texlive-latex-base`, `texlive-latex-recommended`, `texlive-latex-extra` (tcolorbox, needspace, titlesec…), `texlive-pictures` (tikz), `texlive-lang-spanish` (babel en español) y `fonts-lmodern` (Latin Modern OTF, la fuente por defecto de fontspec). Que ese conjunto alcance **no está verificado**. Un detalle más: Anaconda pone primero en el PATH su propio `kpsewhich`, `latexmk` y un `tlmgr` roto. `make pdf` no los usa, pero confunden si hay que diagnosticar un problema de TeX.
4. **En qué archivo está cada valor.** `numbers.json` da el valor y el productor (`produced_by`), pero en los puntos b) y c) no nombra el archivo de salida. Lo encontré en el pie de la fig. 1 del paper (`resultados/PT_k.npz (run_spectrum.py)`) y en el docstring de `run_leon.py` (`resultados/leon/comparacion.json`). En a) sí lo nombra el campo `from_scratch`.
5. **Tiempos por etapa.** `make all` no imprime marcas de tiempo por objetivo. Reconstruí la duración de `reproduce` a partir de las fechas de modificación de sus salidas y medí `pdf` y `docs` con una corrida aparte, que vuelve a tocar solo los mismos PDF.
6. **Kernel del notebook ejecutado.** Los metadatos del notebook ejecutado siguen diciendo `python3 / Python 3`, aunque corrió con `ug-tensor` (su `kernel.json` apunta a `.venv/bin/python`). El nombre lo fija `make_notebook.py`. No causa problemas, pero confunde si alguien lo revisa.

## Resultados: paper frente a lo obtenido

"Coincide" quiere decir dos cosas: el valor obtenido, redondeado a la precisión del paper, da el valor del paper, y además es idéntico bit a bit al de `provenance/numbers.json` y al guardado en `HEAD`.

| Punto | Magnitud | Paper | Obtenido | ¿Coincide? |
|---|---|---|---|---|
| a) Tabla 1 | P_T^UG/P_T^RG, cuadrático, N* = 50 | 1.575 | 1.574618822351915 | sí |
| a) Tabla 1 | P_T^UG/P_T^RG, cuadrático, N* = 60 | 1.516 | 1.5163624877754753 | sí |
| a) Tabla 1 | P_T^UG/P_T^RG, Starobinsky, N* = 50 | 0.902 | 0.9016953421734708 | sí |
| a) Tabla 1 | P_T^UG/P_T^RG, Starobinsky, N* = 60 | 0.904 | 0.9035027627546985 | sí |
| b) Sec. 4 | igual k, cuadrático, primer modo | 0.914 | 0.9144634012803122 | sí |
| b) Sec. 4 | igual k, cuadrático, último modo | 0.344 | 0.3441298152448522 | sí (40 modos, decrece de forma monótona) |
| c) Sec. 6 | A_s (γ = 2.02, N* = 57, fórmula de A2) | 2.12 × 10⁻⁹ | 2.121604922109299 × 10⁻⁹ | sí (+1.08 % sobre Planck 2.0989 × 10⁻⁹; el paper dice 1.1 %) |
| c) Sec. 6 | r (mismo punto) | 4.4 × 10⁻³ | 4.384600586610843 × 10⁻³ | sí |

**Procedencia de cada valor**, según `provenance/numbers.json` (`produced_by`) y `provenance/claims.yaml` (`evidence`):

- **a) Tabla 1.**
  - Archivo: `codigo/resultados/comparacion_N_star.json`, filas con `model = UG`, campo `PT_UG_over_RG` (también en el `.csv`).
  - Claves: `quad_ratio_equal_Nstar_50`, `quad_ratio_equal_Nstar_60`, `staro_ratio_equal_Nstar_50` y `staro_ratio_equal_Nstar_60`.
  - Productor: `codigo/compare_potentials.py::main`, que divide P_T de UG por el de RG a igual N*. P_T se obtiene integrando fondos y modos en `compare(potential)`.
  - Claims: `sign-depends-on-criterion` (`compare_potentials.py::main`, `run_spectrum.py::main`) y `starobinsky-effect-small` (`compare_potentials.py::compare`).
- **b) Igual k.**
  - Archivo: `codigo/resultados/PT_k.csv`, columna `ratio_UG_over_RG`, primera y última fila (también en `PT_k.npz`).
  - Claves: `quad_ratio_equal_k_first` y `quad_ratio_equal_k_last`.
  - Productor: `codigo/run_spectrum.py::main`.
  - Claims: `ug-rg-difference-from-background` (`checks.py::check_ug_vs_rg_difference`, `checks.py::check_negative_control`) y `sign-depends-on-criterion`.
- **c) A_s y r.**
  - Archivo: `codigo/resultados/leon/comparacion.json`, fila `scenario = "1: eps1=(1+Nf-N)^-g, g=2.02"` con `N_star = 57`, campos `A_s_A2` y `r_A2` (también en el `.csv`).
  - Claves: `leon_A_s_A2_Nstar57` y `leon_r_A2_Nstar57`.
  - Productor: `codigo/run_leon.py::main`.
  - Claim: `leon-reference-point-As` (`checks_leon.py::check_A2_reference_point`, `run_leon.py::main`).

## Tiempos

| Etapa | Tiempo |
|---|---|
| Crear el venv e instalar `requirements.txt` | 22 s |
| `make reproduce` | ≈ 157 s (reconstruido a partir de las fechas de sus salidas) |
| `make test` | 100.75 s (según pytest) |
| `make pdf` | ≈ 8 s (7.79 s en la corrida aparte) |
| `make docs` | < 0.1 s |
| **`make all` completo** | **265 s (4 min 25 s)**, igual a lo documentado |
| `ipykernel install` | 0.1 s |
| Ejecución del notebook (`nbconvert`) | 47 s |

## Qué cambiaría en las instrucciones

1. **Fijar también las dependencias transitivas.** `requirements.txt` fija solo las directas. Esta vez pip resolvió lo mismo que `entorno_probado.txt`, pero nada lo garantiza. Ya hay una señal: pyparsing 3.3.3, que no está fijado, produce los 14 avisos de obsolescencia que aparecen en los tests con matplotlib 3.9.2; una versión futura que quite esos nombres podría romper matplotlib. Propuesta: `python -m pip install -r requirements.txt -c entorno_probado.txt`. Lo comprobé con `pip install --dry-run --ignore-installed` y resuelve exactamente los 106 paquetes probados.
2. **Aclarar que el venv tiene que estar activo en la misma shell** en la que se corren `make all` y el notebook, o dar una alternativa sin activarlo: `make all PY="$PWD/.venv/bin/python"`. Hace falta la ruta absoluta porque el Makefile hace `cd codigo`. Esta alternativa **no la probé**, pero las pruebas lanzan subprocesos con `sys.executable`, así que debería funcionar. Conviene agregar además una línea de control después de activar, como `python --version`, que debe dar 3.12.x.
3. **Listar los paquetes de TeX del sistema** (por ejemplo, para apt la lista del punto 3 de la sección anterior) o decir explícitamente que con `texlive-full` funciona.
4. **Mencionar los archivos no versionados** que quedan después de `make all` y del notebook: `.venv/`, `codigo/__pycache__/`, `provenance/__pycache__/`, `codigo/_nb_src/`, y los `build.log`, `.aux`, `.log`, `.out` y `.toc` de LaTeX (17 entradas `??` en `git status`). También se podría agregar un `.gitignore`. La frase "`git status` muestra cambios solo en los PDF y en los cuatro manifiestos" vale solo para los archivos versionados.
5. **Nombrar en `numbers.json` el archivo de salida y el campo** de cada valor (por ejemplo, `codigo/resultados/PT_k.csv::ratio_UG_over_RG[0]`). Hoy falta en b) y en c).
6. Opcional: que `make all` imprima el tiempo de cada objetivo, para que la etapa "cuánto tarda" no dependa de reconstrucciones.

## Cómo se incorporaron las sugerencias (28/09/2026)

Las propuestas 1 a 5 se incorporaron en `REPRODUCCION.md`: instalación con `-c entorno_probado.txt`, `make all PY="$PWD/.venv/bin/python"` sin depender de activar el entorno, control `python --version`, lista de paquetes de TeX (marcada como no verificada), mención de los archivos no versionados, y un campo `output` (`archivo::selector`) en las entradas de `provenance/numbers.json` que no tenían ubicación. El `.gitignore` existía en la carpeta de trabajo, pero no había llegado al repositorio de GitHub; se agregó. La propuesta 6 (tiempos por objetivo) y la observación 6 (metadatos del kernel del notebook) no se aplicaron.
