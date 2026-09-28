# Preparación de archivos para GitHub — 27/09/2026

Se conservaron código, notebook, resultados, figuras, datasets, documentos y evidencia de validación. Se apartaron auxiliares de LaTeX, cachés de Python/pytest, la copia generada por el notebook y una bibliografía duplicada que no se incluye en el paper. El historial Git local se guardó fuera del paquete publicable.

Comprobaciones de esta preparación:
- 15 pruebas de procedencia, figuras y sincronía del notebook aprobadas (sin repetir la integración completa): `preparacion_github_pruebas.txt`.
- Paper compilado en una copia temporal limpia con tres pasadas de XeLaTeX; sin referencias indefinidas ni desbordamientos horizontales: `preparacion_github_compilacion.txt`.
- Enlaces locales del HTML de presentación y de README/PUBLICACION/REPRODUCCION comprobados.
- Las tres copias del paper PDF son idénticas.

Esta comprobación no sustituye la reproducción completa previa ni la futura prueba desde GitHub. El manifiesto `fuentes_cierre_20260927.json` corresponde al cierre anterior; el paper fue revisado editorialmente después. No se alteraron retroactivamente esos hashes históricos. La publicación y la prueba desde un clon remoto siguen pendientes.
