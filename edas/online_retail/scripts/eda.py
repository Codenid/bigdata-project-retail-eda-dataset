"""EDA descriptivo de Online Retail; conserva el Excel y todas sus filas."""
import json
import sys
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports'
sys.path.insert(0, str(ROOT.parents[1] / 'scripts'))
from estructura import informe, guardar, analizar_olist, analizar_retail


def main():
    tables, figures = OUT / 'tables', OUT / 'figures'
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(ROOT / 'data/raw/Online Retail.xlsx', dtype={c: 'string' for c in ['InvoiceNo', 'StockCode', 'CustomerID']})
    profile = pd.DataFrame([dict(columna=c, tipo=str(df[c].dtype), faltantes=int(df[c].isna().sum()), porcentaje_faltantes=df[c].isna().mean()*100, distintos=df[c].nunique()) for c in df])
    profile.to_csv(tables / 'calidad.csv', index=False)
    df['InvoiceDate'] = pd.to_datetime(df.InvoiceDate, errors='coerce')
    df['importe'] = df.Quantity * df.UnitPrice
    cancel = df.InvoiceNo.str.upper().str.startswith('C', na=False)
    positive = ~cancel & df.Quantity.gt(0) & df.UnitPrice.gt(0) & df.InvoiceDate.notna() & df.InvoiceNo.notna()
    # Una fila es una línea, no una factura ni un cliente. No se deduplican líneas.
    sales = df.loc[positive].copy()
    groups = df.groupby('InvoiceNo', dropna=False)
    consistency = groups[['CustomerID', 'Country', 'InvoiceDate']].nunique(dropna=False)
    invoices = sales.groupby('InvoiceNo').agg(importe=('importe','sum'), lineas=('importe','size'), unidades=('Quantity','sum'))
    invoices.describe(percentiles=[.5,.95,.99]).to_csv(tables / 'distribucion_facturas.csv')
    numeric = df[['Quantity','UnitPrice','importe']].describe(percentiles=[.25,.5,.75,.95,.99]).T
    for c in numeric.index:
        q1, q3 = df[c].quantile([.25,.75]); iqr=q3-q1
        numeric.loc[c,'extremos_iqr'] = ((df[c]<q1-1.5*iqr)|(df[c]>q3+1.5*iqr)).sum()
    numeric.to_csv(tables / 'estadisticas_numericas.csv')
    monthly = sales.groupby(sales.InvoiceDate.dt.to_period('M')).agg(importe=('importe','sum'), lineas=('importe','size'), facturas=('InvoiceNo','nunique'))
    monthly.index=monthly.index.astype(str)
    monthly.to_csv(tables / 'ventas_mensuales.csv')
    countries = sales.groupby('Country').agg(importe=('importe','sum'), lineas=('importe','size'), facturas=('InvoiceNo','nunique')).sort_values('importe',ascending=False)
    countries['porcentaje_importe']=countries.importe / sales.importe.sum()*100
    countries.to_csv(tables / 'paises.csv')
    # Clientes conocidos: se excluyen IDs nulos únicamente de esta población.
    customer = sales.dropna(subset=['CustomerID']).groupby('CustomerID').agg(importe=('importe','sum'), facturas=('InvoiceNo','nunique'))
    customer.sort_values('importe', ascending=False, inplace=True)
    bins=customer.facturas.value_counts().sort_index()
    bins.rename('clientes').to_csv(tables / 'frecuencia_clientes.csv')
    segments=pd.Series('Otros ajustes / no elegibles',index=df.index)
    segments.loc[positive]='Ventas positivas'; segments.loc[cancel]='Cancelaciones C'
    segment=df.groupby(segments).agg(lineas=('importe','size'), importe=('importe','sum'))
    segment.to_csv(tables / 'segmentos.csv')
    n_top=max(1,math.ceil(len(customer)*.1))
    m=dict(filas=len(df),columnas=8,duplicados=int(df.iloc[:,:8].duplicated().sum()),facturas=df.InvoiceNo.nunique(),clientes=df.CustomerID.nunique(),fecha_min=str(df.InvoiceDate.min()),fecha_max=str(df.InvoiceDate.max()),fechas_invalidas=int(df.InvoiceDate.isna().sum()),clientes_faltantes=int(df.CustomerID.isna().sum()),descripciones_faltantes=int(df.Description.isna().sum()),cancelaciones_lineas=int(cancel.sum()),cancelaciones_facturas=df.loc[cancel,'InvoiceNo'].nunique(),cantidades_negativas=int(df.Quantity.lt(0).sum()),precios_cero=int(df.UnitPrice.eq(0).sum()),precios_negativos=int(df.UnitPrice.lt(0).sum()),lineas_ventas=len(sales),facturas_ventas=len(invoices),importe_ventas=float(sales.importe.sum()),importe_cancelaciones=float(df.loc[cancel,'importe'].sum()),importe_total_firmado=float(df.importe.sum()),ticket_mediano=float(invoices.importe.median()),ticket_p95=float(invoices.importe.quantile(.95)),uk_porcentaje=float(countries.loc['United Kingdom','porcentaje_importe']),clientes_ventas=len(customer),clientes_recurrentes=int(customer.facturas.ge(2).sum()),importe_ventas_identificadas=float(customer.importe.sum()),top10_clientes_n=n_top,top10_clientes_porcentaje=float(customer.head(n_top).importe.sum()/customer.importe.sum()*100),facturas_inconsistentes=int(consistency.gt(1).any(axis=1).sum()),noviembre_2011=float(monthly.loc['2011-11','importe']),spearman_lineas_importe=float(invoices[['lineas','importe']].corr(method='spearman').iloc[0,1]))
    (OUT/'metricas.json').write_text(json.dumps(m,indent=2)+'\n')
    def save(name,title,ylabel):
        plt.title(title); plt.ylabel(ylabel); plt.tight_layout(); plt.savefig(figures/name,dpi=150); plt.close()
    monthly.importe.plot.bar(figsize=(10,5)); plt.xlabel('Mes (2011-12: hasta el día 9)'); save('ventas_mensuales.png','Importe de ventas positivas por mes','GBP')
    countries.head(10).importe.sort_values().plot.barh(figsize=(9,5)); plt.xlabel('GBP'); save('paises.png','Diez países con mayor importe positivo','País')
    plt.figure(figsize=(9,5)); plt.hist(invoices.importe,bins=100); plt.yscale('log'); plt.xlabel('GBP por factura'); save('facturas.png','Importes por factura: cola completa','Facturas (escala log)')
    profile.set_index('columna').porcentaje_faltantes.plot.bar(figsize=(9,5)); plt.xlabel('Columna'); save('faltantes.png','Campos faltantes en las 541.909 líneas','Porcentaje de filas')
    plt.figure(figsize=(9,5)); cumulative=customer.importe.cumsum()/customer.importe.sum()*100
    plt.plot(range(1,len(customer)+1),cumulative); plt.xlabel('Clientes ordenados por importe'); save('concentracion.png','Concentración entre clientes identificados','Porcentaje acumulado de importe')
    fmt=lambda x: f'{x:,.2f}'
    report=f'''# Online Retail: informe EDA

## Alcance

**{m['filas']:,} líneas de factura**, del {m['fecha_min'][:10]} al {m['fecha_max'][:10]}, de un comercio británico. Fuente: [Daqing Chen, UCI (2015)](https://doi.org/10.24432/C5BW33), licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Importes nominales en GBP, calculados como Quantity × UnitPrice.

## Hallazgos principales

| Indicador | Resultado |
| --- | ---: |
| Facturas con ventas positivas | {m['facturas_ventas']:,} |
| Importe de ventas positivas | GBP {fmt(m['importe_ventas'])} |
| Factura positiva mediana / P95 | GBP {fmt(m['ticket_mediano'])} / {fmt(m['ticket_p95'])} |
| Participación de Reino Unido en importe positivo | {m['uk_porcentaje']:.2f}% |
| Importe de cancelaciones con prefijo C | GBP {fmt(m['importe_cancelaciones'])} |
| Total firmado, incluidos otros ajustes | GBP {fmt(m['importe_total_firmado'])} |

Las ventas positivas incluyen {m['lineas_ventas']:,} líneas con cantidad y precio > 0, fecha y factura presentes y sin prefijo C. El importe puede incluir portes y otros cargos; no representa beneficio ni cobro auditado.

Entre **{m['clientes_ventas']:,} clientes identificados** con ventas positivas, **{m['clientes_recurrentes']/m['clientes_ventas']*100:.2f}%** tiene al menos dos facturas. Los **{n_top:,} clientes de mayor importe** (10%, redondeado hacia arriba) reúnen **{m['top10_clientes_porcentaje']:.2f}%** de GBP {fmt(m['importe_ventas_identificadas'])} de ventas identificadas. Es recurrencia dentro de la ventana, no retención por cohorte.

![Concentración de clientes identificados](figures/concentracion.png)

Noviembre de 2011 registra GBP {fmt(m['noviembre_2011'])} de ventas positivas. Diciembre termina el día 9; no debe compararse como mes completo.

## Calidad y límites

Falta CustomerID en **{m['clientes_faltantes']/m['filas']*100:.2f}%** de las líneas y descripción en {m['descripciones_faltantes']:,}. Se conservan **{m['duplicados']:,} duplicados completos adicionales** y los extremos: no hay una clave de línea que confirme que sean errores. Hay {m['cantidades_negativas']:,} cantidades negativas, {m['precios_cero']:,} precios cero y {m['precios_negativos']:,} precios negativos.

Las líneas se agregaron por factura; clientes nulos se excluyeron solo del análisis de clientes. No se emparejaron cancelaciones con ventas originales, por lo que no se estima una tasa de devolución. La concentración y la cola larga de facturas son hallazgos; la presencia de mayoristas podría contribuir, pero no se identificó a esos clientes. No hay costos ni margen.

## Evidencia

[Métricas](metricas.json), [calidad](tables/calidad.csv), [segmentos](tables/segmentos.csv), [países](tables/paises.csv), [serie mensual](tables/ventas_mensuales.csv) y [estadísticas](tables/estadisticas_numericas.csv). [Países](figures/paises.png), [facturas](figures/facturas.png) y [ventas mensuales](figures/ventas_mensuales.png).

SHA-256 de la fuente: `f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b`. Datos originales intactos y excluidos de Git.
'''
    # El diagnóstico conserva granularidad por factura, pero publica únicamente sus frecuencias.
    consistency.value_counts().rename('facturas').to_csv(tables/'consistencia_facturas.csv')
    guardar('online_retail', analizar_retail(df))
    (OUT/'informe_eda.md').write_text(informe('online_retail', report),encoding='utf-8')
    print(json.dumps(m,indent=2))


if __name__=='__main__':
    main()
