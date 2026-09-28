"""Los extremos admiten refinar arranque/parada en el mismo fondo."""
import pytest
from checks import context
from modes import _horizon_crossing_N
from run_spectrum import k_grid


@pytest.mark.parametrize('potential',['quadratic','starobinsky'])
def test_endpoints_allow_deeper_start_and_later_stop(potential):
    P,rg,ug=context(potential);ks=k_grid(rg,ug,P)
    for bg in (rg,ug):
        assert _horizon_crossing_N(ks[0]/1000,bg)>0
        assert _horizon_crossing_N(ks[-1]/1e-4,bg)<bg.N_end
