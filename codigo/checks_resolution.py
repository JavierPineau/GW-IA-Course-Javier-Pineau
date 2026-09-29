"""AC-25: refinamiento en extremos y paso de ocho índices a igual N*.
No extiende esta verificación de tilt a toda la tabla de radiación con Q.
"""
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
from checks import context, k_at_exit, p_t_cosmic_time
from modes import run_mode
from run_spectrum import k_grid


def check_resolution():
    rows=[];tilts=[]
    for potential in ('quadratic','starobinsky'):
        P,rg,ug=context(potential)
        fine=replace(P,rtol_bg=1e-13,atol_bg=1e-15,n_grid_bg=80001,rtol_mode=1e-12,atol_mode=1e-14)
        import background as B
        for bg,refined in [(rg,B.solve_background_rg(fine)),(ug,B.solve_background_ug(fine))]:
            for edge,k in zip(('first','last'),k_grid(rg,ug,P)[[0,-1]]):
                base=run_mode(k,bg,P);variants={}
                assert not base['stopped_early'], 'El modo base debe alcanzar la parada'
                for tag,bg_v,p_v in [('refinement',refined,fine),('start300',bg,replace(P,ratio_start=300)),
                                     ('start1000',bg,replace(P,ratio_start=1000)),('stop1e4',bg,replace(P,ratio_stop=1e-4))]:
                    r=run_mode(k,bg_v,p_v)
                    if r['stopped_early'] or r['ratio_final']>p_v.ratio_stop*(1+1e-7):
                        raise AssertionError('La parada no alcanzó el objetivo; no es evidencia de convergencia')
                    variants[tag]=dict(relative_change=r['P_T']/base['P_T']-1,ratio_final=r['ratio_final'],N_start=r['N_start'],N_stop=r['N_stop'])
                    if tag == 'stop1e4':
                        assert r['N_stop'] > base['N_stop'], 'La parada refinada debe avanzar en el fondo'
                cosmic=p_t_cosmic_time(k,bg.model,P)
                # p_t_cosmic_time devuelve P_T para el mismo k y modelo.
                variants['independent_cosmic_time']=dict(relative_change=cosmic/base['P_T']-1)
                rows.append(dict(potential=potential,model=bg.model,edge=edge,k=float(k),
                                 baseline=dict(P_T=base['P_T'],ratio_final=base['ratio_final'],N_start=base['N_start'],N_stop=base['N_stop']),
                                 variants=variants))
            for Ns in (50.,60.):
                k=k_at_exit(bg,bg.N_end-Ns);values={}
                for step in (0.5,0.25,0.125):
                    plus=run_mode(k*np.exp(step),bg,P);minus=run_mode(k*np.exp(-step),bg,P)
                    assert not plus['stopped_early'] and not minus['stopped_early']
                    values[str(step)]=float(np.log(plus['P_T']/minus['P_T'])/(2*step))
                tilts.append(dict(potential=potential,model=bg.model,N_star=Ns,tilts=values,
                                  max_abs_change=max(abs(v-values['0.125']) for v in values.values())))
    worst_edge=max(abs(v['relative_change']) for row in rows for v in row['variants'].values())
    worst_tilt=max(r['max_abs_change'] for r in tilts)
    return dict(passed=bool(worst_edge<1e-5 and worst_tilt<2e-5),edge_tolerance=1e-5,tilt_absolute_tolerance=2e-5,
                worst_edge=worst_edge,worst_tilt=worst_tilt,edges=rows,tilts=tilts,
                scope='8 extremos (2 potenciales x 2 modelos x 2 bordes); 8 índices a N*=50,60; no tabla completa de radiación con Q (arXiv:2307.06329)')


if __name__=='__main__':
    result=check_resolution()
    path=Path(__file__).parent/'resultados/resolution_checks.json'
    path.write_text(json.dumps(result,indent=1)+'\n')
    print({k:v for k,v in result.items() if k not in ('edges','tilts')})
    raise SystemExit(0 if result['passed'] else 1)
