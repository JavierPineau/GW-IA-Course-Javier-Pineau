# AC-04, parte 1 — validador y alcance

Se corrigieron exclusivamente los subpuntos 1 y 2. La lista consolidada conserva sus 33 hallazgos; AC-04 continúa abierto hasta completar a–g.

`_func_ok` devuelve un booleano, exige una ruta relativa local `.py::función` y comprueba una definición de función de módulo con AST. Los consumidores de `produced_by` rechazan cualquier resultado distinto de `True`, incluidos valores ausentes o `None`. Las citas textuales de `evidence` se admiten sin atribuirles verificación; las referencias Python mal formadas se rechazan.

La descripción del validador en código, README, registro de reproducción, paper, HTML e informe dice expresamente **chequeo estructural**. No importa ni ejecuta productores, no comprueba la verdad de los claims ni garantiza cobertura del HTML/PDF. La prueba de regeneración comprueba sincronía con resultados guardados y ejecuta los controles simbólicos incorporados en el generador; no reintegra los modelos numéricos.

Validación:

- `/tmp/fixes_gw_20260926/venv/bin/python -m pytest -q codigo/test_provenance.py`: **3 passed en 1.81 s**.
- `/tmp/fixes_gw_20260926/venv/bin/python provenance/validate_provenance.py`: **chequeo estructural OK**.
- La regresión cubre números y figuras con tipos/sintaxis inválidos, ausencia del campo, archivos/funciones inexistentes, rutas ajenas, falsas definiciones dentro de strings, métodos de clase y un `_func_ok` simulado que devuelve `None`. Un módulo que fallaría al importarse permite verificar que el validador no lo ejecuta.

Las cifras y los enunciados científicos de los resultados no se modificaron. Las letras a–g siguen pendientes al terminar esta parte.
