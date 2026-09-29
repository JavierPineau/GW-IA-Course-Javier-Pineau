# Reproducción

Todos los comandos se ejecutan desde la raíz del repositorio.

## Requisitos

- **Python 3.12.** Las versiones fijadas (numpy 1.26.4, scipy 1.13.1) no tienen ruedas para Python 3.13.
- **make.**
- **XeLaTeX** (TeX Live), solo para `make pdf`. Está verificado con `texlive-full` en Ubuntu 24.04. El conjunto mínimo probable en Debian/Ubuntu, deducido de los paquetes que cargan los `.tex` pero **no verificado**, es: `texlive-xetex texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-pictures texlive-lang-spanish fonts-lmodern`.

## Entorno

Con pip (vía verificada):

```bash
python3.12 -m venv .venv
.venv/bin/python --version          # debe dar Python 3.12.x
.venv/bin/python -m pip install -r requirements.txt -c entorno_probado.txt
```

`-c entorno_probado.txt` fija también las dependencias transitivas a las versiones exactas con las que se verificó la reproducción (106 paquetes). Sin esa opción, `requirements.txt` fija solo las directas y pip elige libremente el resto. Si en el `PATH` hay otro Python (por ejemplo, el de Anaconda), `python3.12` puede resolver a ese; funciona igual, siempre que sea 3.12.

Con conda (alternativa, no verificada desde cero):

```bash
conda env create -f environment.yml
conda activate ug-tensor
```

Con conda, activar el entorno y usar `PY=python` en los comandos de abajo.

## Reproducción completa

```bash
make all PY="$PWD/.venv/bin/python"
```

La ruta tiene que ser absoluta porque el Makefile entra en `codigo/`. Así no hace falta activar el entorno. Si se lo activa (`. .venv/bin/activate`), también sirve `make all PY=python`, pero en la misma terminal en la que se activó.

`make all` ejecuta en orden (también con `-j`) los cuatro objetivos siguientes; el flujo completo tarda unos 4–5 minutos, de los cuales unos 100 s son las pruebas.

| Objetivo | Qué hace |
|---|---|
| `make reproduce` | Integra fondos y modos (RG y UG; potenciales cuadrático y de Starobinsky; radiación con difusión Q), corre los controles, regenera tablas, figuras, datasets y el registro `provenance/numbers.json`, valida su estructura y regenera las fuentes del notebook |
| `make test` | 47 pruebas: controles numéricos y simbólicos, figuras, sincronía del notebook y del registro de procedencia |
| `make pdf` | Compila `derivation/`, `informe/` y `paper/` (tres pasadas de XeLaTeX; se detiene si falla) |
| `make docs` | Copia figuras y PDF a `docs/` y el paper a `paper_UG.pdf` en la raíz |

Después de `make all`, `git status` muestra cambios solo en los PDF (llevan la fecha de compilación) y en los cuatro manifiestos de `codigo/figuras/`, que guardan sus hashes. Resultados, figuras PNG y CSV, `numbers.json` y datasets quedan idénticos. Los tiempos de ejecución se imprimen pero no se guardan, y `make reproduce` conserva las salidas del notebook mientras sus fuentes no cambien. Además quedan archivos no versionados que `.gitignore` excluye: `.venv/`, las cachés `__pycache__/`, `codigo/_nb_src/` (lo crea el notebook) y los auxiliares de LaTeX (`*.aux`, `*.log`, `*.out`, `*.toc`, `build.log`).

Regenerar solo una parte (por ejemplo, correr `python checks.py` suelto) puede dejar desactualizados los hashes de figuras y procedencia; en ese caso, correr el flujo completo antes de interpretar un fallo de las pruebas.

## Notebook

La ejecución del notebook es una comprobación aparte de `make test` (que solo verifica la sincronía de sus fuentes):

```bash
PY="$PWD/.venv/bin/python"
$PY -m ipykernel install --sys-prefix --name ug-tensor --display-name 'UG tensor'
cd codigo
$PY -m nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=ug-tensor \
  --ExecutePreprocessor.timeout=300 \
  --output /tmp/explorador_PT_ejecutado.ipynb explorador_PT.ipynb
```

## Alcance de las comprobaciones

- `provenance/validate_provenance.py` comprueba estructura, archivos, funciones y enlaces del registro. No ejecuta los productores ni certifica la verdad científica de las afirmaciones.
- El test de regeneración del registro comprueba la sincronía con las salidas guardadas; `make reproduce` es el que vuelve a calcular.
- `codigo/checks_resolution.py` ensaya ocho extremos del espectro y ocho índices tensoriales a N* = 50, 60. No cubre toda la tabla de radiación con difusión Q de [arXiv:2307.06329](https://arxiv.org/abs/2307.06329).
- Cada entrada de `provenance/numbers.json` dice dónde está guardado su valor: en `inputs` (selectores sobre los archivos de salida) o en `output` (`archivo::selector`).
- Las cifras del paper, del informe y de la página HTML son transcripciones redondeadas de las salidas conservadas; la fuente es `provenance/numbers.json`.

## Última verificación

28/09/2026, en una copia limpia del repositorio, siguiendo al pie de la letra los comandos de este archivo (Python 3.12.3, Linux x86_64, TeX Live 2023): el `pip freeze` del entorno resultó idéntico a `entorno_probado.txt`; `make all` terminó con salida 0 en 4 min 15 s, con **47 pruebas aprobadas** y los tres PDF compilados; el notebook se ejecutó completo sin errores, y `.gitignore` cubrió todos los archivos no versionados. Todo lo generado coincide byte a byte con lo guardado, salvo los PDF y los manifiestos de sus hashes. Registro: `validacion/reproduccion_20260928.md`.

El mismo día, un agente sin historia clonó el repositorio de GitHub y lo reprodujo siguiendo solo estas instrucciones: todos los pasos funcionaron, aprobaron las 47 pruebas y los valores de la tabla 1 y de las secciones 4 y 6 del paper salieron idénticos bit a bit a los registrados. Sus sugerencias (fijar las dependencias transitivas, no depender de activar el entorno, listar los paquetes de TeX, mencionar los archivos no versionados y ubicar cada valor en su archivo de salida) están incorporadas en esta versión. Informe: `validacion/prueba_agente_nuevo.md`.

No se verificó la vía conda ni otro sistema operativo. Las verificaciones anteriores y las dos auditorías independientes están en `validacion/` y `AUDITORIA_CONSOLIDADA.md`.
