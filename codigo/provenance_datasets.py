"""Conserva series completas de figuras para provenance, sin modificar figuras/manifiestos (AC-12)."""
import gzip
import hashlib
import json
import tempfile
from pathlib import Path
import numpy as np
from provenance_tables import ROOT
OUT=ROOT/'provenance/datasets'


def serialize_figure(fig):
    axes=[]
    for ax in fig.axes:
        axes.append(dict(title=ax.get_title(),xlabel=ax.get_xlabel(),ylabel=ax.get_ylabel(),
            lines=[dict(label=l.get_label(),xy=np.asarray(l.get_xydata()).tolist()) for l in ax.lines],
            collections=[dict(label=c.get_label(),offsets=np.asarray(c.get_offsets()).tolist(),paths=[p.vertices.tolist() for p in c.get_paths()]) for c in ax.collections],
            texts=[dict(text=t.get_text(),position=list(t.get_position())) for t in ax.texts]))
    return dict(axes=axes,texts=[t.get_text() for t in fig.texts])


def collect_datasets():
    import matplotlib.pyplot as plt
    import make_figures as A
    import make_report_figures as B
    import make_figures_potenciales as C
    import make_figures_leon as D
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        dest=Path(td);B.FIG=C.FIG=D.FIG=dest
        A.apply_style();data=A.load_outputs();context=B.context()
        jobs=[(A,f,(data,dest)) for f in (A.fig_pt_comparison,A.fig_convergence,A.fig_standard_limit)]
        jobs += [(B,f,context) for f in (B.fig_fondo,B.fig_modo)]
        jobs += [(C,f,()) for f in (C.fig_fondo_starobinsky,C.fig_igual_k,C.fig_igual_Nstar)]
        jobs += [(D,f,()) for f in (D.fig_fondo,D.fig_PT_As)]
        for mod,fn,args in jobs:
            result=fn(*args);fig,stem=result[:2]
            payload=serialize_figure(fig)
            payload['produced_by']=f'codigo/{mod.__name__}.py::{fn.__name__}'
            payload['inputs']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'codigo/resultados').rglob('*')) if p.suffix in ('.json','.csv','.npz')}
            payload['dependencies']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'codigo').glob('*.py')) if not p.name.startswith(('test_','provenance_'))}
            (OUT/(stem.name+'.json.gz')).write_bytes(gzip.compress(json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
            plt.close(fig)


def build_dataset_entries():
    out={}
    for path in sorted(OUT.glob('*.json.gz')):
        data=json.loads(gzip.decompress(path.read_bytes()));key='dataset_'+path.name.split('.')[0]
        out[key]=dict(value=dict(path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),axes=len(data['axes']),
                                points=sum(len(l['xy']) for a in data['axes'] for l in a['lines'])),
            statement='Dataset completo de las series dibujadas, coordenadas, rótulos y anotaciones; sin certificar integridad del manifiesto de la figura.',
            produced_by=data['produced_by'],from_scratch='Serialización de todas las series sin diezmar',from_library='matplotlib/numpy',choices=[],
            coverage_block='AC-04(g)',inputs=data['inputs'],dependencies=data['dependencies'],check=dict(method='leer gzip JSON y comparar SHA256; regenerar con collect_datasets'))
    if len(out)!=10:raise ValueError('Se requieren datasets de las diez figuras')
    return out


if __name__=='__main__':collect_datasets()
