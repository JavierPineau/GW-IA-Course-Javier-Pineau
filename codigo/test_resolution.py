"""Recalcula convergencia en los bordes y el paso de los ocho índices tensoriales."""
from checks_resolution import check_resolution


def test_resolution():
    result = check_resolution()
    assert len(result["edges"]) == 8
    assert len(result["tilts"]) == 8
    assert result["passed"], result
