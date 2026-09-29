# Reproducción desde una copia limpia — 28/09/2026

**Qué se hizo.** Se copió el contenido del repositorio a un directorio nuevo, se creó un entorno pip nuevo con `requirements.txt` y se ejecutó el flujo completo:

```bash
python3 -m venv <venv>
<venv>/bin/python -m pip install -r requirements.txt
make all PY=<venv>/bin/python
```

Se hizo dos veces el mismo día: primero sobre la versión anterior a las correcciones editoriales del 28/09, y después sobre la versión final (la de este repositorio). Lo que sigue describe la segunda corrida. En la primera, el resultado numérico fue el mismo.

**Entorno.** Python 3.12.3, Linux x86_64, XeTeX de TeX Live 2023 (Debian). `pip check`: sin conflictos. Versiones exactas: `../entorno_probado.txt`.

**Resultado.**

- `make all`: salida 0 en 4 min 25 s. Log completo, con las rutas locales reemplazadas por `<clon>` y `<venv>`: `reproduccion_20260928_make_all.txt`.
- Controles: 10/10 (cuadrático), 8/8 (Starobinsky), 7/7 (radiación con difusión Q) y control de resolución aprobado (peor extremo 1.03e-6 < 1e-5; peor índice 6.74e-7 < 2e-5).
- `make test`: **47 passed** en 103.9 s (14 avisos de deprecación de dependencias, ningún fallo).
- `make pdf`: los tres documentos compilaron con `-halt-on-error`, sin referencias ni citas indefinidas.
- Notebook: se ejecutó con `nbconvert` y el kernel del entorno (comando de `../REPRODUCCION.md`): 19 celdas de código ejecutadas, ninguna salida de error. Esas salidas son las que están guardadas en `codigo/explorador_PT.ipynb`.

**Comparación con lo guardado.** Con `git status` después de `make all`, solo difieren:

- los PDF de las figuras y de los tres documentos, por la fecha de compilación embebida;
- los cuatro manifiestos de `codigo/figuras/`, que guardan los hashes de esos PDF.

Todo lo demás queda idéntico byte a byte: `codigo/resultados/`, las figuras PNG y CSV, `provenance/numbers.json` (1028 entradas), los datasets de `provenance/datasets/` y el notebook.

**Qué no cubre.** No se probó la vía conda ni otro sistema operativo, ni un clon desde GitHub. Esta reproducción la hizo una sesión que conocía el trabajo, así que no reemplaza la prueba con un agente sin historia que propone la consigna del curso.
