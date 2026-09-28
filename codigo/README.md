# codigo/ — espectro tensorial primordial P_T(k), RG vs UG con difusión Q

Estado: suite de **47 pruebas**; evidencia en `../validacion/CIERRE_20260927.md`. Procedencia en `../provenance/PROVENANCE.md` (sec. 9 decisiones y mapa función→ecuación; sec. 10 checks; sec. 13 Starobinsky y SymPy; sec. 14 modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329)) y en `../provenance/numbers.json`, `claims.yaml`.

```
cd codigo
python3 run_spectrum.py     # ~3 s; escribe resultados/PT_k.{npz,csv,png} y fondo.png
python3 checks.py           # ~1 min; corre los checks y escribe resultados/checks.json
python3 -m pytest -q test_checks.py   # lo mismo, como tests
python3 make_figures.py             # ~3 s; figuras a partir de resultados/ (no recalcula)
jupyter lab explorador_PT.ipynb       # notebook para correr y graficar todo (ver abajo)
```

Requiere numpy, scipy, matplotlib (probado con numpy 1.26.4, scipy 1.13.1, matplotlib 3.9.2, Python 3.12.3).

| Archivo | Contenido |
|---|---|
| `config.py` | Parámetros (`Params`), unidades y qué decidió el usuario vs. qué es defecto |
| `background.py` | Fondo con un inflatón: RG (`derivation.md` 2.10) y UG con Q (2.7, 2.9, 2.11); término de masa (4.6) |
| `modes.py` | Ecuación de modos (3.11)+(4.6) en N, condición de Bunch–Davies, `P_T` |
| `run_spectrum.py` | Malla de k, corre RG y UG, guarda tablas y figuras |
| `checks.py`, `test_checks.py` | Checks reproducibles (límite estándar, convergencia, UG vs RG, mutaciones) |
| `explorador_PT.ipynb` | Notebook autocontenido: código en celdas + fondo, modo individual, espectro, checks y sus gráficos, exploración libre |
| `make_notebook.py`, `test_notebook_sync.py` | Generan el notebook a partir de los `.py` y comprueban que el código embebido sea idéntico |
| `make_figures.py`, `test_figures.py` | Figuras de reporte (fig. 1 `P_T(k)` RG vs UG, fig. 2 convergencia, fig. 3 límite estándar) a partir de `resultados/` **sin recalcular**; escribe `figuras/` (png, pdf, csv gemelo, `manifest.json`) |
| `make_report_figures.py` | Figuras de apoyo del informe (fig. 4 fondo, fig. 5 modo); **sí calcula** (~3 s) |
| `figuras/` | Salida de `make_figures.py` y `make_report_figures.py` |
| `resultados/` | Salidas de la última corrida |

Duración: UG dura `N_f = 100` e-folds (valor que aparece en A2, escenario 1; en A1/A2 va de 70 a 370); `φ_i` sale de un ajuste (25.386 `M_P`) y RG usa el mismo `φ_i` y las mismas condiciones iniciales.

Unidades: `M_P = 1`, `m = 1` (exacto por homogeneidad); la masa física `6e-6 M_P` multiplica `P_T` por `m²` al final. `k` está en unidades de `m` con `a_i = 1`.

**Notebook.** `explorador_PT.ipynb` trae el código de los cinco módulos en celdas `%%writefile _nb_src/...` (se pueden leer y editar; después se corre la celda de recarga) y lo ejecuta paso a paso con gráficos. Los `.py` de esta carpeta son la fuente de verdad: si cambiás uno, `python3 make_notebook.py` regenera el notebook y `pytest test_notebook_sync.py` verifica que coincidan. Al correrlo crea `_nb_src/` (copia de trabajo; se puede borrar).

Con el entorno de `requirements.txt` o `environment.yml` activado, pandas y JupyterLab están incluidos. Para ejecutar todas las celdas con el Python de ese entorno, desde `codigo/`:

```bash
python -m ipykernel install --sys-prefix --name ug-tensor --display-name 'UG tensor'
python -m nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=ug-tensor \
  --ExecutePreprocessor.timeout=300 \
  --output /tmp/explorador_PT_ejecutado.ipynb explorador_PT.ipynb
```

La salida ejecutada queda en `/tmp/explorador_PT_ejecutado.ipynb`. En JupyterLab, seleccionar el kernel **UG tensor**. `test_notebook_sync.py` comprueba las fuentes embebidas; la ejecución anterior comprueba las celdas, sus imports y sus cálculos.

## Módulos adicionales

| Archivo | Contenido |
|---|---|
| `config.py::params_for`, `background.py` (`potential="starobinsky"`) | Segundo potencial (Starobinsky); `python3 run_spectrum.py starobinsky`, `python3 checks.py starobinsky` (resultados en `resultados/starobinsky/`) |
| `compare_potentials.py` | Comparación a igual N* (e-folds antes del final de cada inflación), ambos potenciales |
| `symbolic_checks.py`, `test_symbolic.py` | 4 comprobaciones SymPy (TT sobre FLRW, ∇T = (□φ−V′)∇φ, cierre del fondo, restricción sobre δQ) |
| `background_leon.py`, `checks_leon.py`, `run_leon.py`, `test_leon.py` | Modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329) (radiación + Q, δQ = 0, sin inflatón): reconstrucción desde ε₁(N), 7 controles CL1–CL7, tabla (`resultados/leon/`) |
| `make_figures_potenciales.py`, `make_figures_leon.py` | Figuras 6–8 y 9–10 (con `manifest_*.json` y test de vigencia en `test_figures.py`) |
| `make_provenance_numbers.py`, `test_provenance.py` | Genera `../provenance/numbers.json` desde `resultados/` (valores no tipeados a mano) y comprueba estructura y sincronía del registro; no certifica claims ni cobertura |

**Aviso:** `checks.py`, `run_spectrum.py`, `compare_potentials.py` y `run_leon.py` reescriben `resultados/`; después hay que regenerar las figuras y `numbers.json` (`make reproduce` en la raíz lo hace en orden). Si no, `test_figures.py` y `test_provenance.py` fallan por hashes desactualizados (es a propósito).
