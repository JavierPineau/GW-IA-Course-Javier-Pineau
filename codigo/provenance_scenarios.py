"""Salidas conservadas de CL5–CL7 y límites explícitos de interpretación."""
import json
from provenance_tables import ROOT, entry


def leaves(value, path=()):
    if isinstance(value, dict):
        for k,v in value.items():
            yield from leaves(v,path+(k,))
    elif isinstance(value,list):
        for i,v in enumerate(value):
            yield from leaves(v,path+(i,))
    else:
        yield path,value


def build_scenario_entries():
    out={};path='codigo/resultados/leon/checks.json'
    doc=json.loads((ROOT/path).read_text())
    funcs={'CL5':'check_slow_roll_formula','CL6':'check_A2_reference_point','CL7':'check_slowroll_map_vs_rg'}
    for i,c in enumerate(doc['checks']):
        if c['id'] not in funcs:continue
        for j,(selector,value) in enumerate(leaves(c['details'])):
            e=entry(value,f"{c['id']}: {'/'.join(map(str,selector))}; salida conservada",'codigo/checks_leon.py::'+funcs[c['id']],path,['checks',i,'details',*selector],'AC-04(e)')
            e.update(origin='saved_result',criterion=c['tolerance'],references=c['source'])
            out[f"scenario_{c['id']}_{j}"]=e
    return out
