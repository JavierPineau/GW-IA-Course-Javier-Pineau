"""Copia las figuras (PNG) y los PDF a docs/ para que docs/index.html se sirva solo desde esa carpeta (p. ej. GitHub Pages)."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
(DOCS / "img").mkdir(exist_ok=True)
for n in ("fig1_PT_k_RG_vs_UG", "fig6_fondo_starobinsky", "fig7_igual_k_potenciales", "fig8_igual_Nstar", "fig9_fondo_leon", "fig10_leon_PT_As"):
    shutil.copy(ROOT / "codigo" / "figuras" / f"{n}.png", DOCS / "img" / f"{n}.png")
shutil.copy(ROOT / "paper" / "paper_UG.pdf", DOCS / "paper_UG.pdf")
shutil.copy(ROOT / "informe" / "informe_UG.pdf", DOCS / "informe_UG.pdf")
shutil.copy(ROOT / "paper" / "paper_UG.pdf", ROOT / "paper_UG.pdf")   # el PDF para presentar, a la vista en la raíz del repositorio
print("docs/ actualizado")
