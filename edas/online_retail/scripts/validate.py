"""Contrasta métricas y agregados publicados contra el Excel original."""
import json
import math
from pathlib import Path
import re
import pandas as pd
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def main():
    df=pd.read_excel(ROOT/'data/raw/Online Retail.xlsx',dtype={c:'string' for c in ['InvoiceNo','StockCode','CustomerID']})
    m=json.loads((ROOT/'reports/metricas.json').read_text())
    cancel=df.InvoiceNo.str.upper().str.startswith('C',na=False)
    mask=(~cancel)&(df.Quantity>0)&(df.UnitPrice>0)&df.InvoiceDate.notna()&df.InvoiceNo.notna()
    sales=df.loc[mask].copy(); sales['amount']=sales.Quantity*sales.UnitPrice
    amount=df.Quantity*df.UnitPrice
    checks=dict(filas=len(df),columnas=df.shape[1],duplicados=int(df.duplicated().sum()),facturas=df.InvoiceNo.nunique(),clientes=df.CustomerID.nunique(),clientes_faltantes=int(df.CustomerID.isna().sum()),descripciones_faltantes=int(df.Description.isna().sum()),cancelaciones_lineas=int(cancel.sum()),cancelaciones_facturas=df.loc[cancel,'InvoiceNo'].nunique(),cantidades_negativas=int((df.Quantity<0).sum()),precios_cero=int((df.UnitPrice==0).sum()),precios_negativos=int((df.UnitPrice<0).sum()),lineas_ventas=len(sales),facturas_ventas=sales.InvoiceNo.nunique(),importe_ventas=float(sales.amount.sum()),importe_cancelaciones=float(amount[cancel].sum()),importe_total_firmado=float(amount.sum()))
    ticket=sales.groupby('InvoiceNo').amount.sum()
    known=sales.dropna(subset=['CustomerID']); clients=known.groupby('CustomerID').amount.sum().sort_values(ascending=False)
    freq=known.groupby('CustomerID').InvoiceNo.nunique()
    top=math.ceil(len(clients)*.1)
    checks.update(ticket_mediano=float(ticket.median()),ticket_p95=float(ticket.quantile(.95)),clientes_ventas=len(clients),clientes_recurrentes=int((freq>=2).sum()),importe_ventas_identificadas=float(clients.sum()),top10_clientes_n=top,top10_clientes_porcentaje=float(clients.head(top).sum()/clients.sum()*100),uk_porcentaje=float(sales.loc[sales.Country=='United Kingdom','amount'].sum()/sales.amount.sum()*100),noviembre_2011=float(sales.loc[sales.InvoiceDate.dt.to_period('M')=='2011-11','amount'].sum()))
    for key,value in checks.items():
        if not math.isclose(m[key],value,rel_tol=1e-10,abs_tol=1e-6):
            raise ValueError(f'Métrica inconsistente: {key}')
    structure=json.loads((ROOT/'reports/estructura.json').read_text())
    assert structure['repeticiones_factura_producto'] == len(df)-len(df.drop_duplicates(['InvoiceNo','StockCode']))
    dependencies=pd.read_csv(ROOT/'reports/tables/dependencias.csv')
    for row in dependencies.to_dict('records'):
        values=df[[row['determinante'], row['atributo']]].drop_duplicates()
        counts=values.groupby(row['determinante'], dropna=False).size()
        assert row['grupos']==len(counts)
        assert row['grupos_multivalor']==int((counts>1).sum())
    assert dependencies.to_dict('records') == structure['dependencias']
    quality=pd.read_csv(ROOT/'reports/tables/calidad.csv').set_index('columna')
    for c in df:
        assert quality.loc[c,'faltantes']==df[c].isna().sum(), c
    monthly=pd.read_csv(ROOT/'reports/tables/ventas_mensuales.csv')
    countries=pd.read_csv(ROOT/'reports/tables/paises.csv')
    segment=pd.read_csv(ROOT/'reports/tables/segmentos.csv')
    assert math.isclose(monthly.importe.sum(),sales.amount.sum())
    assert math.isclose(countries.importe.sum(),sales.amount.sum())
    assert segment.lineas.sum()==len(df)
    assert math.isclose(segment.importe.sum(),amount.sum())
    content=(ROOT/'reports/informe_eda.md').read_text()
    for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',content):
        if not link.startswith('https://'):
            assert (ROOT/'reports'/link).is_file(), link
    figures=list((ROOT/'reports/figures').glob('*.png'))
    assert len(figures)==5
    for path in figures:
        with Image.open(path) as image:
            image.verify()
    print(f'OK: {len(checks)} métricas contra Excel, faltantes, balances, enlaces y cinco PNG.')


if __name__=='__main__':
    main()
