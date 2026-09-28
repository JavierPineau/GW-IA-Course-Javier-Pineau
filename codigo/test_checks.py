"""Expone los checks de checks.py a pytest:  cd codigo && pytest -q test_checks.py"""
import pytest

import checks


@pytest.mark.parametrize("fn", checks.ALL_CHECKS, ids=lambda f: f.__name__)
def test_check(fn):
    r = fn()
    assert r["passed"], f"{r['id']} {r['title']}: worst={r['worst']:.3g}, tol: {r['tolerance']}\n{r['details']}"


@pytest.mark.parametrize("fn", checks.STARO_CHECKS, ids=lambda f: f"starobinsky-{f.__name__}")
def test_check_starobinsky(fn):
    r = fn("starobinsky")
    assert r["passed"], f"{r['id']} {r['title']}: worst={r['worst']:.3g}, tol: {r['tolerance']}\n{r['details']}"
