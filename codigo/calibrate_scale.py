"""Receta de calibración RG a N*=60, usando el dato externo Planck a k*=0.05 Mpc^-1.
La identificación observacional N*↔k* se adopta como convención; no se modela recalentamiento.
"""
import json
import math
from provenance_tables import ROOT


def calibration():
    doc=json.loads((ROOT/'codigo/resultados/comparacion_N_star.json').read_text())
    row=next(r for r in doc['rows'] if r['potential']=='starobinsky' and r['model']=='RG' and r['N_star']==60)
    from config import M_STAROBINSKY
    external=json.loads((ROOT/'provenance/external_inputs.json').read_text())
    As=math.exp(external['external_planck_lnAs']['value'])*1e-10
    return dict(M_input=M_STAROBINSKY,M_required=M_STAROBINSKY*math.sqrt(As/row['A_s_std']),
                A_s_target=As,A_s_at_input=row['A_s_std'],relative_residual=row['A_s_std']/As-1)


def build_calibration_entries():
    out={}
    for key,v in calibration().items():
        out['staro_calibration_'+key]=dict(value=v,statement='Calibración RG condicional a N*=60: '+key,
            produced_by='codigo/calibrate_scale.py::calibration',from_scratch='As escala como M²; M_required=M_input sqrt(As_target/As_at_input)',
            from_library='Planck 2018 v2 TT,TE,EE+lowE+lensing, k*=0.05 Mpc^-1',choices=['M_input=1.14e-5 es entrada redondeada, no salida de params_for.',
            'Comprobar el mismo As de calibración no es una predicción independiente.'],inputs=['codigo/resultados/comparacion_N_star.json','provenance/external_inputs.json','codigo/config.py'],
            check=dict(method='repetir selección RG/Starobinsky/N*=60 y transformación por homogeneidad'))
    return out


if __name__=='__main__':print(json.dumps(calibration(),indent=2))
