"""Expone los checks simbólicos de symbolic_checks.py a pytest:  cd codigo && pytest -q test_symbolic.py"""
import pytest

import symbolic_checks


@pytest.mark.parametrize("fn", symbolic_checks.ALL_SYMBOLIC, ids=lambda f: f.__name__)
def test_symbolic(fn):
    r = fn()
    assert r["passed"], f"{r['id']} {r['title']}: {r['details']}"
