"""Contrasta artefactos con agregados exportados, no con filas de BigQuery."""
import hashlib
import json
import math
from pathlib import Path
import re
import pandas as pd
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]

def main():
    raw=ROOT/'data/raw';out=ROOT/'reports'
    p=pd.read_csv(raw/'thelook_perfil_tablas.csv');d=pd.read_csv(raw/'thelook_distribuciones.csv');r=pd.read_csv(raw/'thelook_relaciones.csv')
    m=json.loads((out/'metricas.json').read_text()); sources=json.loads((out/'fuentes.json').read_text())
    for name,digest in sources['sha256'].items():
        assert hashlib.sha256((raw/name).read_bytes()).hexdigest()==digest,name
    rows=p[p.metrica=='filas'].set_index('tabla').valor.astype(int)
    assert rows.to_dict()==m['filas']
    total=float(p.loc[(p.tabla=='order_items')&(p.campo=='sale_price')&(p.metrica=='suma_finitos'),'valor'].iloc[0])
    assert math.isclose(total,m['importe_lineas'])
    for (t,dim),z in d.groupby(['tabla','dimension']):
        assert z.filas.sum()==rows[t],(t,dim)
        if t=='order_items':
            assert math.isclose(z.importe_observado_finito.sum(),total,rel_tol=1e-9),(t,dim)
    q=r[r.relacion.str.contains(' -> ',regex=False)].pivot(index='relacion',columns='metrica',values='valor').astype(float)
    assert len(q)==9
    assert ((q.fk_nulas+q.fk_no_nulas)==q.filas_hijas).all()
    assert ((q.filas_hijas_con_correspondencia+q.filas_hijas_sin_correspondencia)==q.fk_no_nulas).all()
    inventory=p.loc[(p.tabla=='inventory_items')&(p.campo=='sold_at')&(p.metrica=='nulos'),'valor'].astype(int).iloc[0]
    assert m['inventario_sold_at_ausente']==inventory
    issue=r.loc[(r.relacion=='order_items.product_id vs inventory_items.product_id')&(r.metrica=='lineas_con_unidad_unica_sin_sold_at'),'valor'].astype(int).iloc[0]
    assert m['lineas_unidad_sin_sold_at']==issue
    figures=list((out/'figures').glob('*.png'));assert len(figures)==5
    for file in figures:
        with Image.open(file) as im: im.verify()
    report=out/'informe_eda.md'
    for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',report.read_text()):
        if not link.startswith('https://'): assert (report.parent/link).is_file(),link
    print('OK: huellas de fuentes, siete tablas, balances de distribuciones, nueve relaciones, enlaces y cinco PNG. Validación limitada a exportaciones.')

if __name__=='__main__': main()
