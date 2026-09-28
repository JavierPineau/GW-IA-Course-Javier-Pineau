# Reproducción vigente — 27 de septiembre de 2026

Ejecutar desde la raíz del repositorio. La fuente del paper es `paper/paper_UG.tex`; `paper_UG.pdf` y las copias de `docs/` se actualizan con `make docs`.

## Entorno

Vía pip, con Python 3.12:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make all PY=python
```

Alternativa con conda:

```bash
conda env create -f environment.yml
conda activate ug-tensor
make all PY=python
```

También se necesita XeLaTeX y los paquetes TeX usados por los documentos (fontspec, babel español, tcolorbox, entre otros). La vía conda se ofrece como alternativa; no se certifica aquí una creación nueva de ese entorno. Las dependencias directas de Python están fijadas, incluidas nbconvert 7.16.4, ipykernel 6.30.1 y Pillow 10.4.0. `requirements.txt` no es un lock de todas las dependencias transitivas ni del sistema operativo. `entorno_probado.txt` es un registro histórico, no ese lock.

## Flujo y resultados

`make all` ejecuta en orden `reproduce`, `test`, `pdf` y `docs`, también si se invoca con `-j`. `make reproduce` vuelve a integrar los fondos y modos, los controles, las tablas y figuras; conserva los datasets completos, regenera el registro de procedencia y sincroniza las fuentes del notebook. `make test` recalcula los controles y comprueba figuras y procedencia: **47 pruebas**. `make pdf` se detiene si una compilación falla.

El control `codigo/checks_resolution.py` ensaya ocho extremos del espectro y ocho índices tensoriales a N*=50,60. Exige alcanzar efectivamente la parada refinada; no considera convergencia volver a evaluar al mismo final de inflación. No cubre toda la tabla de radiación con difusión Q de [la referencia de 2023](https://arxiv.org/abs/2307.06329).

La ejecución del notebook es una comprobación separada del test de sincronía de fuentes:

```bash
python -m ipykernel install --sys-prefix --name ug-tensor --display-name 'UG tensor'
cd codigo
python -m nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=ug-tensor \
  --ExecutePreprocessor.timeout=300 \
  --output /tmp/explorador_PT_ejecutado.ipynb explorador_PT.ipynb
```

Las cifras de los documentos son transcripciones redondeadas de las salidas conservadas: no todas se generan automáticamente. Se cotejaron los extremos tras recortar la malla para admitir q inicial=1000 y q final=1e-4. Los resultados de la malla anterior que aparezcan en registros históricos no son los extremos de la entrega vigente.

El validador de procedencia comprueba estructura, archivos, funciones y enlaces. No ejecuta los productores ni certifica la verdad científica. El test de regeneración del registro verifica sincronía con salidas guardadas; `make reproduce` sí ejecuta los cálculos.

## Evidencia y límites de reproducción

La validación de esta continuación se registra en `validacion/CIERRE_20260927.md`. Los logs anteriores AC-01/AC-02 documentan una reproducción en clon y entorno pip nuevos y una ejecución completa del notebook; no certifican por sí solos esta versión. Las auditorías independientes del 24 y 26 de septiembre están consolidadas en `AUDITORIA_CONSOLIDADA.md`.

Los tiempos, metadatos PDF y últimos dígitos de residuos numéricos pueden variar entre corridas. Regenerar solo una parte puede invalidar hashes: ejecutar el flujo completo antes de interpretar un fallo de vigencia de figuras o procedencia.

## Publicación a cargo del autor

No se publica ni configura un remoto en esta sesión. Después de subir el repositorio, registrar aquí la URL y el commit o tag entregado, clonar desde esa URL en un directorio nuevo y ejecutar los pasos anteriores. La prueba local no certifica acceso ni reproducción desde GitHub (AC-15). La consigna propone además una reproducción con un agente sin historia; esta continuación no se presenta como esa prueba independiente.
