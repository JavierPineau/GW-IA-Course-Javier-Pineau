"""Expone los checks del modelo de radiación con difusión Q (arXiv:2202.04029; arXiv:2307.06329) a pytest:  cd codigo && pytest -q test_leon.py"""
import pytest

import checks_leon


@pytest.mark.parametrize("fn", checks_leon.ALL_LEON, ids=lambda f: f.__name__)
def test_leon(fn):
    r = fn()
    assert r["passed"], f"{r['id']} {r['title']}: worst={r['worst']:.3g}, tol: {r['tolerance']}\n{r['details']}"
