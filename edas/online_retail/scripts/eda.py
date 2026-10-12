"""EDA descriptivo de Online Retail; conserva el Excel y todas sus filas."""
import json
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports'


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
    report=f'''# Informe EDA: Online Retail (UCI)

## Alcance y calidad

Se analizaron {m['filas']:,} líneas y ocho columnas del comercio británico documentado por [UCI](https://archive.ics.uci.edu/dataset/352/online+retail), entre {m['fecha_min']} y {m['fecha_max']}. Fuente: Daqing Chen (2015), DOI [10.24432/C5BW33](https://doi.org/10.24432/C5BW33), licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). El importe es Quantity × UnitPrice, en GBP nominales; no representa beneficio ni cobro confirmado.

Hay {m['facturas']:,} códigos de factura y {m['clientes']:,} identificadores de cliente distintos no nulos. Faltan CustomerID en {m['clientes_faltantes']:,} líneas ({m['clientes_faltantes']/m['filas']*100:.2f}%) y Description en {m['descripciones_faltantes']:,}. Aunque la ficha de UCI declara ausencia de faltantes, el archivo observado sí los contiene. Se encontraron {m['duplicados']:,} duplicados completos adicionales: se mantienen porque no hay identificador de línea que permita determinar si son errores. Fechas inválidas o ausentes tras conversión: {m['fechas_invalidas']}.

![Faltantes](figures/faltantes.png)

## Ventas, cancelaciones y ajustes

La población de ventas positivas exige factura y fecha disponibles, factura sin prefijo C, cantidad > 0 y precio > 0. Contiene {m['lineas_ventas']:,} líneas y {m['facturas_ventas']:,} facturas; conserva duplicados y extremos. Las {m['filas']-m['lineas_ventas']:,} líneas restantes se mantienen en el perfil y en el balance firmado. Los códigos especiales de producto no se excluyen: el importe puede incluir portes y otros cargos.

Las ventas positivas suman GBP {fmt(m['importe_ventas'])}. Las facturas con prefijo C, que UCI identifica como cancelaciones, contienen {m['cancelaciones_lineas']:,} líneas, {m['cancelaciones_facturas']:,} facturas y un importe firmado de GBP {fmt(m['importe_cancelaciones'])}. Este importe no es una tasa de devolución de ventas: no se enlazaron cancelaciones con compras originales y sus ventanas pueden diferir. El total firmado de todas las líneas es GBP {fmt(m['importe_total_firmado'])}; incluye ajustes y no equivale a ingresos netos auditados.

Se observan {m['cantidades_negativas']:,} cantidades negativas, {m['precios_cero']:,} precios cero y {m['precios_negativos']:,} precios negativos. No se consideran errores automáticamente. [Segmentos y balance](tables/segmentos.csv), [calidad](tables/calidad.csv) y [estadísticas y extremos IQR](tables/estadisticas_numericas.csv) documentan las poblaciones.

## Distribución y concentración

La mediana del importe positivo por factura es GBP {fmt(m['ticket_mediano'])}; P95 es GBP {fmt(m['ticket_p95'])}. La diferencia muestra una distribución asimétrica. No se recorta la cola ni se borra ninguna observación por IQR.

![Facturas](figures/facturas.png)

Reino Unido concentra {m['uk_porcentaje']:.2f}% del importe de ventas positivas, con denominador GBP {fmt(m['importe_ventas'])}. Country es el país registrado del cliente; no demuestra el destino de entrega. [Detalle por país](tables/paises.csv).

![Países](figures/paises.png)

Noviembre de 2011 suma GBP {fmt(m['noviembre_2011'])} en ventas positivas. Diciembre de 2011 termina el día 9 y es parcial: no debe compararse como un mes completo. El patrón mensual es compatible con estacionalidad, pero un solo ciclo no demuestra una pauta estable ni su causa. [Serie mensual](tables/ventas_mensuales.csv).

![Ventas mensuales](figures/ventas_mensuales.png)

Entre {m['clientes_ventas']:,} clientes identificados con ventas positivas, {m['clientes_recurrentes']:,} ({m['clientes_recurrentes']/m['clientes_ventas']*100:.2f}%) tienen al menos dos facturas distintas dentro de la ventana observada. No es retención por cohorte. El 10% superior, redondeado hacia arriba a {n_top:,} clientes, concentra {m['top10_clientes_porcentaje']:.2f}% del importe identificado (GBP {fmt(m['importe_ventas_identificadas'])}). Los clientes ausentes se excluyen solo de esta población; no se imputan ni se agrupan como una persona. [Frecuencia agregada](tables/frecuencia_clientes.csv).

![Concentración](figures/concentracion.png)

## Granularidad, relaciones y límites

Se agregan líneas por InvoiceNo antes de calcular tickets; no se unen tablas. {m['facturas_inconsistentes']:,} facturas tienen más de un valor de cliente, país o fecha contando el faltante como categoría. La tabla [consistencia](tables/consistencia_facturas.csv) recoge solo conteos por factura, sin sus identificadores en los artefactos publicados. Spearman entre número de líneas e importe positivo por factura: {m['spearman_lineas_importe']:.3f}; ambos comparten una construcción contable y no se infiere causalidad.

Hallazgos: concentración geográfica y de clientes, cola larga de tickets y presencia material de cancelaciones y ajustes. Hipótesis: la actividad mayorista descrita por UCI podría contribuir a los extremos; no se ha validado el tipo de cada cliente. El archivo corresponde a una empresa histórica y no representa el mercado británico actual. No hay costos, margen, pagos ni emparejamiento de devoluciones. Los faltantes limitan la lectura de recurrencia y concentración.

SHA-256 del ZIP: `f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b`. [Métricas calculadas](metricas.json). Datos originales intactos y excluidos de Git; no se publican listas de clientes ni transacciones individuales.
'''
    # El diagnóstico conserva granularidad por factura, pero publica únicamente sus frecuencias.
    consistency.value_counts().rename('facturas').to_csv(tables/'consistencia_facturas.csv')
    (OUT/'informe_eda.md').write_text(report,encoding='utf-8')
    print(json.dumps(m,indent=2))


if __name__=='__main__':
    main()
