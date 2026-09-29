"""Selección completa de tablas conservadas; no ejecuta sus productores físicos."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


def entry(value, statement, producer, path, selector, block, choices=()):
    return dict(value=value, statement=statement, produced_by=producer,
                from_scratch='Selección literal de la salida conservada', from_library='', choices=list(choices),
                coverage_block=block, inputs=[dict(path=path, selector=selector)],
                check=dict(method='comparación exacta con el campo seleccionado del JSON conservado'))


def build_table_entries():
    entries = {}
    for tag, path, producer in [('equalN', 'codigo/resultados/comparacion_N_star.json', 'codigo/compare_potentials.py::main'),
                                  ('leon_table', 'codigo/resultados/leon/comparacion.json', 'codigo/run_leon.py::main')]:
        doc = json.loads((ROOT/path).read_text())
        for i, row in enumerate(doc['rows']):
            selection = {k: row[k] for k in ('potential', 'model', 'scenario', 'N_star') if k in row}
            for field, value in row.items():
                entries[f'{tag}_row_{i}_{field}'] = entry(value, f'{field}; fila {selection}', producer, path, ['rows', i, field], 'AC-04(b)',
                    ['n_s, A_s y r son estimaciones escalares condicionales; el sector escalar UG no se deriva.',
                     'N* cuenta e-folds antes del final de cada fondo; no identifica por sí solo una escala observada.'])
    return entries
