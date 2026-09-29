# Hallazgos consolidados — auditorías del 24 y 26 de septiembre de 2026

Base común: `4c7ab4e41c791fa416ec6807f4431a2d6f8fa400` (commit del repositorio local de trabajo; ese historial no se publica). Los informes originales de las auditorías no se incluyen en el repositorio; este archivo registra cada hallazgo y cómo se resolvió. Este archivo consolida las dos auditorías existentes; no es una auditoría nueva. Se creó antes de modificar código.

Fuentes leídas completas:

- **A24:** `auditoria_gw_20260924_evidencia/crear_informe.py` (fuera de este repositorio), contenido íntegro del informe del 24/09 conservado en su generador, incluidas las tablas de `comparacion_30_numeros.json` y `chequeos_independientes.json`. No se ejecutó el generador. El destino que declara coincide con el TeX ocupado ahora por A26; por eso se consultó esta fuente conservada.
- **A26:** `auditoria_independiente_GW_IA.tex` (fuera de este repositorio), informe del 26/09.

Las rutas de implementación siguientes son relativas a este repositorio. Las líneas de las auditorías corresponden al commit base. Los documentos de correcciones del **23/09 no forman parte** de esta consolidación.

Criterio: una entrada por problema corregible, fusionando repeticiones entre informes. Cuando un H original reúne problemas distintos, se desdobla y se conserva su correspondencia. Se adopta la mayor severidad asignada por las dos auditorías, indicando las discrepancias. «Solo» significa que la objeción específica no figura en la otra auditoría; no significa que esa auditoría la haya descartado. Ninguna asigna hallazgos críticos al resultado central condicional.

## Importantes — orden de trabajo

### AC-01. Colisión de CSV de figuras que rompe `make all`
- **Origen:** ambos; A24 H03 ↔ A26 H01. **Severidad:** Importante en ambos.
- **Archivo/función:** `codigo/make_figures.py::main`, selección de salidas; `codigo/test_figures.py`; `Makefile`.
- **Qué cambiar:** enumerar las salidas propias de cada figura: `fig1*.csv` captura indebidamente `fig10_leon_PT_As.csv`. Conservar los dos CSV de fig3; regenerar el manifiesto y verificar el flujo completo en clon limpio, sin reordenamientos que escondan la dependencia falsa.
- **Estado:** resuelto. Salidas CSV explícitas y regresión que introduce/modifica un CSV de fig10 sin invalidar fig1; se conservan ambos CSV de fig3. `make all` en clon y venv nuevos: salida 0, **41 passed**, PDF/docs completados. Figuras/manifiestos dependientes y PDF/docs de la entrega regenerados. Log: `validacion/AC-01_make_all.txt`.

### AC-02. Notebook no ejecutable con las dependencias documentadas
- **Origen:** **solo A24 H04**; A26 no ejecuta/documenta ese fallo. **Severidad:** Importante.
- **Archivo/función:** `requirements.txt`, `environment.yml`, `codigo/explorador_PT.ipynb` (import de pandas), `codigo/README.md` (`jupyter lab`).
- **Qué cambiar:** declarar pandas y JupyterLab si se conserva el comando ofrecido; ejecutar el notebook completo con el entorno documentado y conservar el log. La prueba de sincronía de fuentes no sustituye su ejecución.
- **Estado:** resuelto. pandas 2.2.3 y JupyterLab 4.2.5 declarados en pip/conda; instrucciones de kernel del entorno añadidas. En un venv nuevo instalado desde requirements, nbconvert terminó con salida 0: **19 celdas de código ejecutadas y ninguna salida de error**; JupyterLab informó 4.2.5 y `pip check` pasó. Se verificó la vía pip, no se recreó el entorno con conda. Evidencia: `validacion/AC-02.md` y `validacion/AC-02_notebook.txt`.

### AC-03. Cuatro cocientes atribuidos a una función que no los calcula
- **Origen:** ambos; parte de A24 H12 ↔ A26 H03. **Severidad:** Importante (A24: Menor).
- **Archivo/función:** `codigo/make_provenance_numbers.py`, `provenance/numbers.json` (`*ratio_equal_Nstar*`), `provenance/claims.yaml` (`sign-depends-on-criterion`); `codigo/compare_potentials.py::compare/main`.
- **Qué cambiar:** identificar `main`, donde se divide UG/RG, o extraer un productor explícito; conservar potencial, N* y selección de salida. Cambiar el generador y regenerar el registro, no solo editar JSON.
- **Estado:** resuelto. Generador y registro apuntan a `main` y especifican dataset, potencial, modelo, N* y campo `PT_UG_over_RG`; evidencia del claim actualizada. Los **30 valores permanecen idénticos** y solo cambian los metadatos de las cuatro entradas afectadas. Validador y dos tests de provenance aprobados; suite final: **41 passed**. Evidencia: `validacion/AC-03.md`.

### AC-04. Cobertura incompleta del registro y alcance excesivo de su validador
- **Origen:** ambos; A24 H02 ↔ A26 H02 e inventarios de §1. **Severidad:** Importante.
- **Archivo/función:** `provenance/validate_provenance.py::_func_ok`, `codigo/test_provenance.py`, `provenance/{claims.yaml,numbers.json}`, `codigo/make_provenance_numbers.py`, `paper/paper_UG.tex:149`, HTML e informe.
- **Qué cambiar:** rechazar referencias mal formadas que hoy devuelven `None`; describir el chequeo como estructural, sin afirmar que ejecuta productores o prueba la verdad de claims. Registrar datasets completos con claves de fila/columna, productores, entradas, métricas, dominios y fuentes externas. Generar o cotejar las cifras humanas. Cobertura pendiente consolidada:
  - Residuos CL1–CL4, masa X, máximos C1–C3 y señal/ruido por separado.
  - Tablas completas de nT, r y ns a igual N*, y tabla completa de radiación con Q (arXiv:2307.06329) para todas sus filas/columnas.
  - Diagnósticos de fondos: condiciones iniciales, transitorios/extremos, final de inflación, energías, fuerzas, H y campos en pivotes; ejemplo del modo y extremos del espectro.
  - Valores externos Planck/CMB con selección y pivote; estimaciones estándar distinguidas de salidas; configuración y tolerancias como entradas.
  - Offsets/diagnósticos de CL7, alternativas escalares y escenarios excluidos, distinguiendo resultados conservados de historia/conjetura.
  - Bloques teóricos auxiliares (sistema de fondo, acción/normalización/estado, identidades y predicciones estándar) con hipótesis y referencias, sin convertir cada coeficiente algebraico en una entrada numérica.
  - Datos completos de las figuras mediante datasets, no miles de entradas aisladas; su integridad específica se corrige en AC-12.
- **Estado:** resuelto (1, 2 y 3a–3g). Registro ampliado y generación integrada en `make reproduce`; chequeo estructural y pruebas de sincronía aprobados.
  - **1 resuelto:** `produced_by` exige una referencia local `.py::función` válida y definida; se rechazan `None`, tipos/formato inválidos, referencias ausentes y cualquier retorno distinto de `True`. Se comprueba la definición mediante AST sin importar el productor.
  - **2 resuelto:** docstrings, salida del validador, README, reproducción, paper, HTML e informe distinguen chequeo estructural de ejecución de productores, verdad de claims y cobertura. Las citas textuales no se verifican; la regeneración del registro comprueba sincronía con salidas guardadas.
  - **Validación de 1–2:** tres tests de provenance aprobados, incluida regresión de formatos inválidos en números/figuras y retorno `None`; el registro actual pasa el chequeo estructural. Registro detallado en `validacion/AC-04_parte1.md`.
  - **3a resuelto:** 218 entradas de controles con productor, selectors de inputs, dominio, reducción y criterio; incluye CL1–CL4, masa X de los cuatro fondos, máximos C1–C3 y señal/ruido. Salida de masa X conservada y extracción conectada al generador. Claims enlazados. Regeneración y chequeo estructural comprobados. **3b resuelto:** tablas completas (8 filas de igual N*, 9 de radiación con Q), todas las columnas enlazadas con selección literal y productor; regeneración verificada. Las letras siguientes se detallan abajo.
  - **Autorización actualizada:** el autor autorizó completar AC-04–AC-33 y resolver textos sustentados en las fuentes sin confirmación individual.
  - **Continuación:** los puntos 1–2 ya constan en el commit `749b7c1`, con el mensaje solicitado. Se repitieron los tres tests de `codigo/test_provenance.py` (3 passed) y el chequeo estructural (OK) usando `python`; el entorno temporal citado en la validación anterior ya no existe.
  - **3c resuelto:** Diagnósticos conservados con parámetros, dominio, malla y selección; se incluyen condiciones iniciales, transitorios, energías, fuerzas, pivotes, final, modo de ejemplo y extremos del espectro. Regeneración verificada.
  - **3d resuelto:** Entradas externas diferenciadas de salidas propias; lnAs, As, ns y límites r con selección, versión y pivote, incluyendo BK14 histórico y BK15/BK18. Regeneración verificada.
  - **3e resuelto:** Registrados todos los campos conservados CL5–CL7, incluyendo offsets y potencias; alternativas escalares completas en 3b. Historia y conjeturas separadas en claims de límites. Regeneración verificada.

  - **3f resuelto:** bloques de sistema de fondo, acción/estado/normalización, identidad escalar y predicciones estándar con hipótesis y referencias; sin atomizar coeficientes algebraicos. Chequeo estructural aprobado.
  - **3g resuelto:** Diez datasets gzip JSON completos enlazados desde números y figuras, con productor, inputs, dependencias y método de cotejo; AC-12 sigue separado.

### AC-05. Difusión atribuida a la variación de una acción canónica conservativa
- **Origen:** ambos; A24 H01 ↔ A26 H04. **Severidad:** Importante.
- **Archivo/función:** `derivation/derivation.md` §§1,2,4 y conclusiones; `informe/s06_tensores.tex:154,184`, `informe/s10_discusion.tex`; contraste con `paper/paper_UG.tex:69`.
- **Qué cambiar:** separar ecuaciones fenomenológicas con fuente de la variación canónica que da conservación. Unificar la hipótesis efectiva/condicional de acción TT y vacío para la amplitud. Incorporar el cuidado del vínculo unimodular a segundo orden (corrección de segundo orden o parametrización exponencial); el multiplicador no absorbe una violación del vínculo. No hace falta cambiar la ecuación TT correcta para retirar la deducción excesiva.
- **Estado:** resuelto. Se separó la transferencia fenomenológica de la acción canónica conservativa; acción TT y vacío quedan como hipótesis efectivas. Se corrigió el papel del multiplicador y la necesidad de completar la métrica a segundo orden en derivación e informe. Compilación documental se registra al cierre.

### AC-06. El residuo X se presenta como prueba independiente de la teoría
- **Origen:** ambos; A24 H07 ↔ A26 H05. **Severidad:** Importante.
- **Archivo/función:** `informe/s08_numerico.tex:4,26,36`; `codigo/background.py::tensor_mass_term/quantities_ug`; registro y discusión asociados.
- **Qué cambiar:** describir su anulación algebraica como control interno de implementación. Distinguirla de S1/proyección TT y de C3.2, que contrasta derivación numérica del spline. Propagar la salvedad ya presente en el paper.
- **Estado:** resuelto. X queda como control interno algebraico, distinguido de C3.2 y S1 en código e informe.

### AC-07. Euler omite la proyección de transferencia de momento
- **Origen:** **solo A26 H06**. **Severidad:** Importante.
- **Archivo/función:** `informe/s11_acoplamiento.tex:59`.
- **Qué cambiar:** incorporar `(rho+p)a_b + D_b p = D_b Q`; especificar marco de transferencia y velocidad. Con Q homogéneo en coordenadas puede existir `D_i Q = u_i dot(Q)` a primer orden. Retirar la afirmación general de Euler usual sin efecto de la transferencia.
- **Estado:** resuelto. Se incorporó la proyección de Euler con D_b Q, definición del marco y término de velocidad perturbada.

### AC-08. Radiación presentada como consecuencia necesaria de delta Q = 0
- **Origen:** ambos; A24 H06 ↔ A26 H07. **Severidad:** Importante.
- **Archivo/función:** `informe/s11_acoplamiento.tex:65`, en conflicto con líneas 51–59 y `paper/paper_UG.tex:122`.
- **Qué cambiar:** presentar el modelo de radiación de León como elección. Conservar las salvedades sobre campo uniforme, perturbaciones inhomogéneas y gauge; S4 no excluye todas las ramas.
- **Estado:** resuelto. Radiación es una elección de modelo; se conservan los límites de campo uniforme, gauge y perturbaciones inhomogéneas.

### AC-09. Mutaciones simbólicas anunciadas sin pruebas reproducibles
- **Origen:** ambos; A24 H08 ↔ parte de A26 H20. **Severidad:** Importante (A26: Menor).
- **Archivo/función:** `codigo/test_symbolic.py`, `codigo/symbolic_checks.py`, `docs/index.html:44`, `paper/paper_UG.tex:149`, `informe/apD_codigo.tex:43`, `provenance/PROVENANCE.md:435`.
- **Qué cambiar:** conservar mutantes y criterios de fallo de S1–S4, o restringir la afirmación a las pruebas disponibles. Separar las mutaciones numéricas existentes de las simbólicas narradas.
- **Estado:** resuelto. Se restringió la afirmación a cuatro comprobaciones simbólicas sin mutantes conservados; las mutaciones reproducibles son las numéricas de C0.

### AC-10. Dos modos de León publicados sin alcanzar congelamiento
- **Origen:** ambos; A24 H05 ↔ A26 H08. **Severidad:** Importante.
- **Archivo/función:** `codigo/make_figures_leon.py::fig_PT_As`, `codigo/modes.py::run_mode`, figura 10 y textos asociados en paper/informe/HTML.
- **Qué cambiar:** conservar `stopped_early` y `ratio_final`, filtrar o rotular evaluaciones a tiempo finito. Los cruces N≈94.8966 y 98 terminan con q≈0.01387 y 0.262, no 0.001. Revisar el alcance de «30 modos congelados» sin inventar evolución posinflacionaria.
- **Estado:** resuelto. Fig10 conserva stopped_early y ratio_final de ambos modelos; 28 modos alcanzan q=0.001 y dos evaluaciones al final se rotulan por separado. El máximo comparado usa solo los primeros. Figura y CSV regenerados.

### AC-11. Extremo inferior sin convergencia del arranque del vacío
- **Origen:** **solo A26 H09 como diagnóstico específico**; A24 H19 identifica falta general de pruebas de extremos, pero no ensaya este arranque más profundo. **Severidad:** Importante.
- **Archivo/función:** `codigo/run_spectrum.py::k_grid`, `codigo/checks.py::check_convergence`.
- **Qué cambiar:** extender el fondo o recortar k mínimo para comparar el mismo modo con arranques más profundos. El primer k no admite q inicial=300 dentro del fondo actual; variar a 30 no certifica la convergencia restante a 100.
- **Estado:** resuelto. Malla recortada para admitir el mismo primer modo con q inicial=300 y 1000; también reserva margen de parada q=1e-4 para AC-25. Dos pruebas comprueban ambos extremos en RG/UG y ambos potenciales. Espectros regenerados y cotejados con los extremos refinables; flujo completo aprobado.

### AC-12. CSV gemelos y manifiestos incompletos de figuras
- **Origen:** ambos; A24 H18 ↔ A26 H10. **Severidad:** Importante (A24: Menor).
- **Archivo/función:** `codigo/make_figures_potenciales.py::fig_fondo_starobinsky/main`, `codigo/make_figures_leon.py::fig_fondo/fig_PT_As/main`, `codigo/test_figures.py`.
- **Qué cambiar:** fig6 debe incluir RG y dependencias del recálculo (`background.py`, `config.py`), no atribuir el fondo al CSV de espectros. Fig9 debe guardar ambas gammas y toda la malla dibujada; fig10, también As/r. Registrar dependencias reales de fondo/modos/configuración o dibujar exclusivamente datasets conservados. **Detalle exclusivo A24:** fig6; **detalle explícito A26:** diezmado de fig9. Mantener esta tarea separada de la colisión AC-01.
- **Estado:** resuelto. CSV completos: fig6 RG/UG (8000 filas), fig9 ambas gammas y malla completa (20001 filas), fig10 incluye tabla As/r y flags de parada. Fig4/5 también conservan series completas. Manifiestos registran dependencias reales y tests verifican hashes y cobertura de tablas; seis tests de figuras aprobados.

### AC-13. CL7 prueba dos puntos, no toda la forma ni la causa del offset
- **Origen:** ambos; A24 H09 ↔ A26 H11. **Severidad:** Importante.
- **Archivo/función:** `codigo/checks_leon.py::check_slowroll_map_vs_rg`, `provenance/claims.yaml:83–90`, `paper/paper_UG.tex:135`, `informe/s12_leon.tex:75`, `provenance/PROVENANCE.md` §14.
- **Qué cambiar:** limitar el claim a la razón N*=50/60 o conservar barrido de forma, epsilonH−epsilonV, integral de ln H y contraste normalizado/con epsilonH exacto. Mantener visible el fallo del criterio absoluto del 10% y justificar el nuevo criterio del 3% como exploratorio.
- **Estado:** resuelto. CL7 se limita a la razón entre dos pivotes, conserva offsets e historia del criterio sin atribución causal.

### AC-14. Causa exclusiva del final de Starobinsky sin control que la aísle
- **Origen:** ambos; A24 H14 y evaluación del claim 5 ↔ A26 H12. **Severidad:** Importante (A24: Menor).
- **Archivo/función:** `provenance/claims.yaml:42–47`, `informe/s10_potenciales.tex:38,110`, discusión correspondiente.
- **Qué cambiar:** restringir la interpretación al presupuesto energético del ejemplo o realizar comparación controlada que aísle Lambda0. El control RG de Planck no prueba la causa del final UG. El tamaño del efecto se trata en AC-21.
- **Estado:** resuelto. La interpretación del final se restringe al presupuesto energético; no se afirma una causa exclusiva.

### AC-15. Falta URL/remoto para reproducir la entrega desde GitHub
- **Origen:** ambos; A24 H20 ↔ A26 H22. **Severidad:** Importante.
- **Archivo/función:** `README.md`, `REPRODUCCION.md`, `provenance/PROVENANCE.md:481`, `informe/apD_codigo.tex:47`, presentación HTML.
- **Qué cambiar:** publicar cuando el autor lo decida, documentar URL y commit/tag y verificar clon remoto con las instrucciones. Un clon local no certifica esa parte de la consigna. **Pendiente de destino y autorización de publicación:** la orden actual de fixes/commits locales no indica cuenta ni repositorio remoto.
- **Estado:** pendiente de publicación por decisión del autor. El autor subirá el trabajo a GitHub al finalizar; no se configura remoto ni se publica en esta sesión. Después: registrar URL y commit/tag, clonar desde esa URL en un directorio nuevo y ejecutar las instrucciones de REPRODUCCION.md. No se presenta el clon local como prueba de reproducción remota.

## Menores

### AC-16. Fórmula slow-roll conservativa aplicada en explicación de difusión
- **Origen:** ambos; A24 H10 ↔ parte de A26 H21 y revisión de §2.8. **Severidad:** Menor.
- **Archivo/función:** `derivation/derivation.md:139–143`, `informe/s05_fondo.tex:56–62`.
- **Qué cambiar:** conservar la condición KG estándar (Q constante para el único escalar que recibe la transferencia), o formular la aproximación para una ley local fija con U y U'. Aclarar que el código integra la ecuación completa con fuente.
- **Estado:** resuelto. Se explicitó Q constante para la aproximación KG estándar y el uso de U/Uprime para una ley local fija.

### AC-17. Slow-roll del potencial desnudo confundido con el fondo al final
- **Origen:** **solo A26 H21 como objeción explícita**; A24 describe el evento correcto pero no formula este hallazgo. **Severidad:** Menor.
- **Archivo/función:** `informe/s09_resultados.tex:22`, `informe/s10_discusion.tex:17`.
- **Qué cambiar:** al evento epsilonH=1 no afirmar que el modelo sigue en slow-roll porque epsilonV(V)≈0.03. Limitar esa observación al potencial V aislado.
- **Estado:** resuelto. Se distingue epsilonV del potencial desnudo de epsilonH=1 al final del fondo.

### AC-18. Final RG cuadrático aproximado presentado como resultado integrado
- **Origen:** ambos; A24 H11 ↔ parte de A26 H16. **Severidad:** Menor.
- **Archivo/función:** `paper/paper_UG.tex:84`, `informe/s10_potenciales.tex:83`.
- **Qué cambiar:** usar phi final RG≈1.00934 MP para epsilonH=1; identificar sqrt(2)≈1.4 como aproximación epsilonV=1, como ya hace `s09_resultados.tex`.
- **Estado:** resuelto. Se usa phi final RG=1.00934 MP para epsilonH=1 y se identifica sqrt(2) como aproximación de potencial.

### AC-19. Escala M registrada como salida de una calibración que no se ejecuta
- **Origen:** ambos; parte de A24 H12 ↔ A26 H17. **Severidad:** Menor.
- **Archivo/función:** `codigo/config.py::params_for`, `codigo/make_provenance_numbers.py`, `provenance/numbers.json::staro_M_calibrated`, README.
- **Qué cambiar:** registrar M=1.14e−5 como entrada redondeada; agregar receta ejecutable de calibración, dato/pivote y residuo por separado. Corregir «todos los números leídos de outputs». No presentar la comprobación del mismo As usado para calibrar como predicción independiente.
- **Estado:** resuelto. M se identifica como entrada redondeada; calibrate_scale.py conserva receta ejecutable por homogeneidad, referencia/pivote, M requerido y residuo separados. Tests de provenance aprobados.

### AC-20. Desvío de As no está dentro del 1%
- **Origen:** ambos; A24 H13 ↔ A26 H14. **Severidad:** Menor.
- **Archivo/función:** `provenance/claims.yaml:73–82`, `codigo/checks_leon.py::check_reference_point_A2`, paper e informe de León.
- **Qué cambiar:** usar +1.0816% (≈1.1%), registrar el dato externo y residuo; hacer coherentes el enunciado y la tolerancia, dejando claro que CL6 actualmente admite 10%.
- **Estado:** resuelto. Desvío As corregido a +1.0816% (aproximadamente 1.1%); CL6 conserva tolerancia 10%. Dato externo y residuo están registrados.

### AC-21. Resumen de Starobinsky como 10% con ambos criterios
- **Origen:** ambos; parte de A24 H14 ↔ A26 H15. **Severidad:** Menor.
- **Archivo/función:** `provenance/claims.yaml:42`, `docs/index.html:25`, `informe/s10_potenciales.tex:85,110`, `informe/s10_discusion.tex:10–11`.
- **Qué cambiar:** distinguir ≈9.6–9.8% a igual N* de ≈3.9–23.0% a igual k; no inferir ley universal de una sola elección de difusión.
- **Estado:** resuelto. Se distinguen las reducciones a igual N* y a igual k; no se infiere universalidad de una sola difusión. Con la malla refinable de AC-11 la reducción a igual k es 5.3–20.4%; cifras actualizadas en paper, informe y HTML.

### AC-22. Igual k confundido con igual N de cruce
- **Origen:** ambos; A24 H15 ↔ parte de A26 H16. **Severidad:** Menor.
- **Archivo/función:** `informe/s10_potenciales.tex:52`; ejemplo correcto en `informe/s09_resultados.tex:26`.
- **Qué cambiar:** definir cruces resolviendo k=aH en cada fondo; no afirmar tiempos iguales si H difiere. Conservar la salvedad de escala observada/recalentamiento.
- **Estado:** resuelto. Cruces definidos por k=aH en cada fondo; se conserva la salvedad de escala observada y recalentamiento.

### AC-23. Precisión slow-roll anunciada superior al peor modo aprobado
- **Origen:** ambos; A24 H16 ↔ A26 H13. **Severidad:** Menor.
- **Archivo/función:** `paper/paper_UG.tex:76`, `informe/s10_discusion.tex:10–11`, `codigo/checks.py::check_ug_vs_rg_difference`.
- **Qué cambiar:** indicar máximo ≈2.80e−5 entre los modos juzgados del cuadrático y el dominio/muestra; distinguir precisión típica de máxima y puntos excluidos.
- **Estado:** resuelto. Se publica el máximo 2.80e-5 de los modos juzgados de C3.4, separado de precisión típica y puntos excluidos.

### AC-24. Cota C3.2 posterior al transitorio desactualizada
- **Origen:** **solo A24 H17 como discrepancia comprobada**; A26 inventaría la cifra 2e−10, pero no la contrasta con el máximo. **Severidad:** Menor.
- **Archivo/función:** `informe/s10_potenciales.tex:94`, `codigo/checks.py::check_background_28`, `codigo/resultados/starobinsky/checks.json`.
- **Qué cambiar:** reemplazar <2e−10 por el máximo del dominio y malla juzgados (≈7.43e−9 en la auditoría), preferentemente generado desde datos. No cambiar la tolerancia para acomodar el texto.
- **Estado:** resuelto. Cota descriptiva actualizada al máximo RG/UG de 7.43e-9 en dominio y malla juzgados; tolerancia intacta.

### AC-25. Barridos de extremos/paso de nT ausentes de la suite
- **Origen:** ambos; A24 H19 ↔ discusión de convergencia de A26 §3. **Severidad:** Menor (clasificación A24; A26 sin H independiente).
- **Archivo/función:** `codigo/checks.py::check_convergence`, `codigo/compare_potentials.py`, `codigo/run_leon.py` (paso de tilt).
- **Qué cambiar:** incorporar controles de refinamiento/integrador en extremos y barrido del paso de nT; identificar alcance de las pruebas (los ocho índices ensayados, no toda tabla de radiación con Q (arXiv:2307.06329)). **Detalle solo A24:** k máximo UG satura al final: pedir q final=1e−4 devuelve el mismo tiempo y potencia; no contar esa igualdad como convergencia. Recortar el extremo o especificar evolución posterior para poder variar la parada. El arranque inferior específico queda en AC-11.
- **Estado:** resuelto. checks_resolution.py integrado en make reproduce y test_resolution.py: ocho extremos con refinamiento, integrador independiente, arranques q=300/1000 y parada q=1e-4 efectivamente alcanzada; ocho índices a N*=50,60 con pasos 0.5/0.25/0.125. Máximos 1.032e-6 relativo y 6.742e-7 absoluto. Criterios exploratorios conservados: 1e-5 y 2e-5; no cubre toda la tabla de radiación con Q. Registro enlazado en numbers/claims. Evidencia: `validacion/CIERRE_20260927.md`.

### AC-26. Notación temporal incorrecta en la ecuación TT
- **Origen:** ambos; A24 H21 ↔ tabla de claims de A26 §1.1. **Severidad:** Menor.
- **Archivo/función:** `provenance/claims.yaml:7`, `derivation/derivation.md:19`.
- **Qué cambiar:** puntos para tiempo cósmico y 3H, o primas para tiempo conforme y 2H conforme; explicitar la convención.
- **Estado:** resuelto. El claim usa derivadas explícitas respecto de t cósmico con 3H; derivation.md ya define puntos cósmicos y primas conformes. Convenciones cotejadas. Evidencia: `validacion/CIERRE_20260927.md`.

### AC-27. Extrapolaciones más allá del fondo/formulación ensayados
- **Origen:** A24 H22; A26 también limita la imposibilidad de doble precisión en su tabla de afirmaciones, **pero no recoge la objeción específica a la extrapolación anti-de Sitter**. **Severidad:** Menor.
- **Archivo/función:** `informe/s10_potenciales.tex:38`, `informe/s12_leon.tex:22,82`, discusión.
- **Qué cambiar:** condicionar el futuro mínimo negativo/anti-de Sitter a una extensión del modelo Q(N). Limitar la dificultad del escenario 2 a la formulación ensayada; no descartar reformulaciones reescaladas/logarítmicas sin probarlas.
- **Estado:** resuelto. El futuro de energía efectiva negativa se condiciona a extender Q(N) y la solución posinflacionaria; la dificultad del escenario 2 se limita a la formulación directa ensayada. No se descartan reformulaciones reescaladas/logarítmicas. Evidencia: `validacion/CIERRE_20260927.md`.

### AC-28. Referencias incompletas para fórmulas y controles concretos
- **Origen:** ambos; A24 H23 ↔ A26 H19 y tablas de fuentes/claims. **Severidad:** Menor.
- **Archivo/función:** `provenance/claims.yaml:17–22`, `provenance/numbers.json::check_deSitter_worst_rel_err` y su generador, bibliografía, `informe/s10_potenciales.tex:16`.
- **Qué cambiar:** enlazar `check_planck_phi2` en el claim correspondiente; citar solución de de Sitter a tiempo finito y no solo amplitud slow-roll; verificar fuente textual de la forma/origen conforme de Starobinsky o declarar adopción fenomenológica. **Detalle solo A26:** fijar Martin arXiv:1303.3787v3 para ecs. 2.19/2.23/2.24, cuya numeración cambia en v5.
- **Estado:** resuelto. Claim de límite RG enlazado con check_planck_phi2; de Sitter a tiempo finito referenciado a Baumann, arXiv:0907.5424v2, ecs. 196/198 (texto consultado), más normalización tensorial propia. Martin fijado a arXiv:1303.3787v3 y contrastado con la copia conservada. Starobinsky se adopta fenomenológicamente, sin presentar el origen conforme como verificado. Evidencia: `validacion/CIERRE_20260927.md`.

### AC-29. Estado vigente mezclado con historia y pendientes obsoletos
- **Origen:** ambos; A24 H24 ↔ A26 H18. **Severidad:** Menor.
- **Archivo/función:** `derivation/derivation.md`, `paper/paper_UG.tex:30,149`, `codigo/README.md`, `informe/apD_codigo.tex`, `REPRODUCCION.md`, `provenance/PROVENANCE.md`.
- **Qué cambiar:** actualizar recuento real de tests (41 en el commit auditado), rutas ausentes y pasos ya implementados; enlazar la derivación final de espectro/modos. Separar hitos históricos de estado actual, incluidos cambios posteriores de tolerancias: no afirmar sin excepciones que todas se fijaron antes. Conservar un procedimiento vigente único. Sincronización/cobertura numérica: AC-04.
- **Estado:** resuelto. Reproducción vigente única en REPRODUCCION.md, recuento de 47 pruebas, 1028 entradas y 24 claims; historia distinguida en PROVENANCE.md. Derivación enlazada al desarrollo final del espectro; retirados pendientes obsoletos y afirmaciones de mutaciones simbólicas sin evidencia. Revisiones posteriores de criterios declaradas. Las correcciones ya marcadas resueltas se propagaron al informe y al HTML. Evidencia: `validacion/CIERRE_20260927.md`.

### AC-30. Convención dimensional de masa de Planck errónea
- **Origen:** **solo A26 H19**. **Severidad:** Menor.
- **Archivo/función:** `codigo/checks.py:13`, `provenance/PROVENANCE.md:327`.
- **Qué cambiar:** escribir MP²=(8πG)^−1, no MP=8πG.
- **Estado:** resuelto. Convención corregida a M_P²=(8πG)^−1 en checks.py y PROVENANCE.md; notebook sincronizado. Evidencia: `validacion/CIERRE_20260927.md`.

### AC-31. Alcance del ansatz escalar y descripción de gauge excesivos
- **Origen:** **solo A26 H20 como errores específicos**; A24 reconoce en general límites del ansatz. **Severidad:** Menor.
- **Archivo/función:** `codigo/symbolic_checks.py::_scalar_setup`, `paper/paper_UG.tex:115`, `informe/s11_acoplamiento.tex:34,56`.
- **Qué cambiar:** no llamar general a la métrica escalar ensayada, que no incluye E. Para volumen fiducial variable describir conservación de f d⁴x, ∂a(f ξa)=0, no jacobiano unidad en coordenadas arbitrarias. Mutaciones: AC-09.
- **Estado:** resuelto. El ansatz simbólico se describe sin E y con dependencia en una coordenada espacial; no se llama general. El informe expresa conservación de f d⁴x y ∂a(f ξa)=0, sin imponer jacobiano unidad en coordenadas arbitrarias. Evidencia: `validacion/CIERRE_20260927.md`.

### AC-32. Dependencias auxiliares sin versión para reconstrucción duradera
- **Origen:** **solo A26 H23**. **Severidad:** Menor.
- **Archivo/función:** `requirements.txt` (nbconvert, ipykernel, pillow), documentación del entorno.
- **Qué cambiar:** fijar versiones compatibles/probadas y distinguir registro del entorno histórico de un lock reproducible. La ausencia de pandas/JupyterLab que impide ejecutar comandos está separada en AC-02.
- **Estado:** resuelto. nbconvert 7.16.4, ipykernel 6.30.1 y Pillow 10.4.0 fijados en pip/conda. Venv nuevo instalado desde requirements.txt, pip check aprobado, flujo completo y notebook ejecutados. Registro de transitivas en validacion/entorno_cierre_20260927.txt; se distingue de un lock multiplataforma. No se recreó conda. Evidencia: `validacion/CIERRE_20260927.md`.

### AC-33. Comentario de malla uniforme en la variable incorrecta
- **Origen:** **solo A26 H23**. **Severidad:** Menor.
- **Archivo/función:** `codigo/config.py:38`, `codigo/background.py:175`.
- **Qué cambiar:** documentar que se muestrea uniformemente en t y luego se transforma a N para construir splines.
- **Estado:** resuelto. config.py y background.py documentan muestreo uniforme en t y transformación a N para construir splines. Notebook regenerado y ejecutado. Evidencia: `validacion/CIERRE_20260927.md`.

## Seguimiento

33 hallazgos consolidados: **15 Importantes y 18 Menores; ninguno Crítico**. Los H compuestos se desdoblaron para permitir un commit por problema resuelto. Todas las entradas H01–H24 de A24 y H01–H23 de A26 tienen correspondencia arriba; también se conservaron precisiones accionables de sus tablas y desarrollo.

Primero se versiona esta lista. Después, cada fix registra aquí su estado y su validación en el mismo commit; no se marca resuelto un hallazgo por corregir solo una parte. La compilación y los tests de los fixes son validaciones de implementación, no una nueva auditoría científica. Esta continuación deja los cambios en el árbol local, sin publicar; el esquema de commits anterior es histórico.

**Estado al cierre del 27/09/2026: 32 de 33 hallazgos resueltos.** Solo AC-15 queda pendiente de la publicación que hará el autor y de verificar el clon remoto. La reproducción con un agente sin historia sugerida por la consigna no se atribuye a esta continuación. Validación: `make all` con entorno pip nuevo, 47 pruebas aprobadas, tres PDF compilados, 19 celdas del notebook ejecutadas sin errores. Evidencia en `validacion/CIERRE_20260927.md`.
