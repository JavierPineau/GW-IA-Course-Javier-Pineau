# Contenido preparado para GitHub

Esta carpeta contiene los archivos destinados a publicación. Subir su **contenido a la raíz del repositorio**, conservando las subcarpetas e incluyendo `.gitignore`.

- `paper_UG.pdf`: paper para leer y presentar; su fuente canónica es `paper/paper_UG.tex`.
- `codigo/`: implementación, pruebas, notebook, resultados y figuras necesarios para reproducir y verificar el trabajo.
- `derivation/` e `informe/`: desarrollos ampliados y sus PDF.
- `provenance/`, `validacion/` y `AUDITORIA_CONSOLIDADA.md`: procedencia y evidencia de validación, con su alcance histórico declarado.
- `docs/`: página de presentación y sus recursos; las copias de PDF son necesarias para sus enlaces.
- `literatura/`: síntesis y herramientas bibliográficas; no incluye PDF de artículos ajenos.
- `Makefile`, `requirements.txt`, `environment.yml`, `REPRODUCCION.md` y los registros de entorno: instrucciones y dependencias.

Los auxiliares de LaTeX, cachés, copia de trabajo del notebook y bibliografía duplicada se apartaron. La ejecución de las herramientas puede volver a generar auxiliares, que `.gitignore` excluye. La bibliografía utilizada está incorporada en el paper; las menciones del archivo duplicado en los hashes históricos documentan el estado anterior.

El historial Git local se conserva fuera de esta carpeta, junto con el inventario de lo apartado. Esta carpeta se entrega como paquete de archivos para publicación; no contiene `.git`. No se realizó ninguna publicación ni se configuró un remoto. Después de publicar, registrar la URL y el commit o tag en `REPRODUCCION.md` y comprobar la reproducción desde un clon nuevo.
