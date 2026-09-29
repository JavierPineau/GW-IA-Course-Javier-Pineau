"""Diagnósticos conservados AC-04(c), con dominio y parámetros explícitos."""
import ast
import json
from dataclasses import asdict
import numpy as np
from provenance_tables import ROOT, entry
PATH = 'codigo/resultados/provenance_diagnostics.json'


def collect():
    import background as B
    import modes as M
    from config import Params
    rows = []
    for pot, folder in [('quadratic',''), ('starobinsky','starobinsky/')]:
        source = f'codigo/resultados/{folder}PT_k.npz'
        with np.load(ROOT/source) as d:
            params = ast.literal_eval(d['params'].item()); params.setdefault('potential',pot)
            P = Params(**params)
            for field in ['k','PT_RG','PT_UG','N_exit_RG','N_exit_UG']:
                name = field if field in d else field.replace('N_exit_RG','RG_N_exit').replace('N_exit_UG','UG_N_exit')
                if name in d:
                    for which, idx in [('min',np.argmin(d[name])),('max',np.argmax(d[name]))]:
                        rows.append(dict(potential=pot,model='spectrum',field=field,selection=which,value=float(d[name][idx]),index=int(idx),source=source,params=params))
        initial=B.initial_state(P)
        for solve in [B.solve_background_rg,B.solve_background_ug]:
            bg=solve(P);N=np.unique(np.r_[np.linspace(0,bg.N_end,20001),np.linspace(0,1,4001),bg.N_end-50,bg.N_end-60])
            H=np.exp(bg.lnH(N));phi=bg.phi(N);phid=H*bg.phi.derivative()(N)
            Q=B.Q_of_N(N,initial['Q_i'],P.gamma) if bg.model=='UG' else np.zeros_like(N)
            lam=initial['Lam0'] if bg.model=='UG' else 0.
            kinetic=phid**2/2;V=B.V(phi,pot); U=V+Q+lam
            force=-P.gamma*Q/bg.phi.derivative()(N)
            values=dict(H=H,phi=phi,phidot=phid,eps1=bg.eps1(N),K=kinetic,V=V,Q=Q,U=U,rho_phi=kinetic+V,
                        total=kinetic+U,epsV_bare=(B.dV(phi,pot)/V)**2/2,force_Q=force,force_V=B.dV(phi,pot),
                        force_ratio=np.abs(force/B.dV(phi,pot)))
            for field,arr in values.items():
                points={'initial':0,'end':len(N)-1,'Nstar50':int(np.argmin(abs(N-(bg.N_end-50)))), 'Nstar60':int(np.argmin(abs(N-(bg.N_end-60)))),
                        'minimum_sampled':int(np.argmin(arr)), 'maximum_sampled':int(np.argmax(arr)),
                        'first_efold_maximum_sampled':int(np.where(N<=1)[0][np.argmax(arr[N<=1])])}
                for sel,i in points.items():
                    rows.append(dict(potential=pot,model=bg.model,field=field,selection=sel,value=float(arr[i]),N=float(N[i]),
                                     source=source,params=params,domain=[0,bg.N_end],sampling='20001 puntos uniformes en N + 4001 en [0,1] + pivotes',Lambda0=lam))
            rows.append(dict(potential=pot,model=bg.model,field='N_end',selection='event_eps1_1',value=bg.N_end,source=source,params=params))
            if pot=='quadratic':
                rg=B.solve_background_rg(P);k=float(np.exp(40+rg.lnH(40)))
                result=M.run_mode(k,bg,P)
                for field,value in result.items():
                    rows.append(dict(potential=pot,model=bg.model,field=field,selection='demo_mode_NexitRG40',value=value,source=source,params=params))
    return dict(rows=rows)


def build_diagnostic_entries():
    rows=json.loads((ROOT/PATH).read_text())['rows']
    entries={}
    for i,row in enumerate(rows):
        e=entry(row['value'],f"{row['potential']} {row['model']}: {row['field']} ({row['selection']}); extremos sobre malla, no optimización continua",'codigo/provenance_diagnostics.py::collect',PATH,['rows',i,'value'],'AC-04(c)')
        e['scope']={k:v for k,v in row.items() if k!='value'}
        entries[f'diagnostic_{i}']=e
    return entries


if __name__=='__main__':
    (ROOT/PATH).write_text(json.dumps(collect(),indent=1,ensure_ascii=False,default=float)+'\n')
