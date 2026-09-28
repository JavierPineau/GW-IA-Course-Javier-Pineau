"""Importa referencias observacionales explícitas; no produce datos de Planck/CMB."""
import json
import math
from provenance_tables import ROOT, entry
PATH='provenance/external_inputs.json'


def build_external_entries():
    doc=json.loads((ROOT/PATH).read_text());out={}
    for key,row in doc.items():
        e=entry(row['value'],row['description'],'codigo/provenance_external.py::build_external_entries',PATH,[key,'value'],'AC-04(d)')
        e.update(origin='external_observation',source=row,produced_by_role='importador local; el resultado observacional pertenece a la fuente citada')
        e['check']['method']='cotejo documental manual con versión, selección y pivote citados; el validador estructural no lo realiza'
        out[key]=e
    out['external_planck_As']=dict(out['external_planck_lnAs'], value=math.exp(doc['external_planck_lnAs']['value'])*1e-10,
        statement='Conversión exp(ln(10^10 A_s))*10^-10 del dato externo',origin='derived_from_external_observation',check=dict(method='exp(valor externo)*1e-10'))
    return out
