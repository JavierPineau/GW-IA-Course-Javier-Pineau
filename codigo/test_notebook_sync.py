"""Comprueba que el código embebido en explorador_PT.ipynb sea idéntico a los .py de esta carpeta (compara FUENTES; NO ejecuta el notebook).
Si falla: `python3 make_notebook.py` regenera el notebook (y hay que volver a ejecutarlo para guardar las salidas)."""
import json
from pathlib import Path

import pytest

HERE = Path(__file__).parent
FILES = ["config.py", "background.py", "modes.py", "checks.py", "run_spectrum.py"]


def _embedded():
    nb = json.loads((HERE / "explorador_PT.ipynb").read_text())
    out = {}
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            src = "".join(c["source"])
            if src.startswith("%%writefile _nb_src/"):
                first, rest = src.split("\n", 1)
                out[first.split("/")[-1]] = rest
    return out


@pytest.mark.parametrize("fname", FILES)
def test_embedded_source_matches(fname):
    emb = _embedded()
    assert fname in emb, f"{fname} no está embebido en el notebook"
    assert emb[fname].rstrip("\n") == (HERE / fname).read_text().rstrip("\n"), \
        f"{fname} difiere del notebook: correr `python3 make_notebook.py`"
