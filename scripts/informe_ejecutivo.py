"""Genera el informe ejecutivo desde las métricas de los dos EDAs."""
import json
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
o=json.loads((ROOT/'edas/olist/reports/metricas.json').read_text())
u=json.loads((ROOT/'edas/online_retail/reports/metricas.json').read_text())
with (ROOT/'edas/olist/reports/tables/resenas_demora.csv').open() as handle:
    scores={r['late']:float(r['puntuacion_media']) for r in csv.DictReader(handle)}
def es(value,decimals=2):
    return f'{value:,.{decimals}f}'.replace(',','_').replace('.',',').replace('_','.')
(ROOT/'README.md').write_text(f'''# Informe ejecutivo: dos análisis del comercio electrónico

El análisis de Olist sitúa la entrega como un punto relevante de la experiencia del comprador. Online Retail muestra una actividad concentrada en Reino Unido y en una fracción de sus clientes identificados, con importes de factura muy desiguales. Son dos EDAs independientes: corresponden a empresas, periodos, monedas y unidades de observación diferentes. Sus cifras no se suman ni permiten comparar directamente desempeño comercial.

## 1. Olist: entregas y satisfacción del comprador

El dataset brasileño de Olist reúne **{es(o['total_orders'],0)} pedidos** de 2016–2018 distribuidos en nueve tablas. Entre los **{es(o['delivered_complete'],0)} pedidos entregados con fechas completas**, la mediana de entrega es **{es(o['delivery_median'])} días** y el percentil 95 llega a **{es(o['delivery_p95'])} días**. **{es(o['late_orders'],0)} pedidos ({es(o['late_percent'])}%)** llegaron después de la fecha y hora estimadas.

La experiencia de entrega se asocia con diferencias en reseñas. Entre pedidos entregados con fechas y puntuación disponibles, la puntuación media es **{es(scores['A tiempo'])}/5 cuando llegan a tiempo**, frente a **{es(scores['Tarde'])}/5 cuando llegan tarde**. La correlación de Spearman entre duración y puntuación es **{es(o['spearman_delivery_review'],3)}**. Esta asociación justifica estudiar los pedidos demorados, pero no demuestra que el retraso explique por sí solo la valoración: vendedores, categorías, distancias y selección de quienes reseñan pueden influir.

La calidad estructural permite analizar los pedidos sin multiplicarlos al cruzar tablas: artículos, pagos y reseñas se agregaron previamente por pedido. Hay **{es(o['payment_discrepancies'],0)} discrepancias mayores a BRL 0,05** entre pagos y precio más flete sobre **{es(o['payment_comparable'],0)} pedidos comparables**; requieren contexto contable y no prueban fraude. La repetición de registros geográficos y de claves de reseña exige tratar cada tabla según su granularidad.

La lectura empresarial principal es la presencia de una cola de entregas prolongadas asociada a menor satisfacción. La puntualidad descrita excluye cancelaciones y pedidos sin fechas completas; el dataset histórico no representa todo el comercio brasileño actual. Las cifras monetarias son BRL nominales y no describen margen.

[Informe completo de Olist](edas/olist/reports/informe_eda.md) · [Gráficos](edas/olist/reports/figures/) · [Tablas](edas/olist/reports/tables/)

## 2. Online Retail: concentración comercial y facturas heterogéneas

El archivo de UCI contiene **{es(u['filas'],0)} líneas de factura** de un comercio británico, del 1 de diciembre de 2010 al 9 de diciembre de 2011. Las ventas positivas —cantidades y precios mayores que cero, fecha y factura disponibles y sin prefijo de cancelación C— reúnen **{es(u['facturas_ventas'],0)} facturas** y suman **GBP {es(u['importe_ventas'])}**. Este importe incluye los cargos presentes en esas líneas y no equivale a beneficio ni cobros auditados.

**Reino Unido concentra el {es(u['uk_porcentaje'])}% del importe positivo.** Entre **{es(u['clientes_ventas'],0)} clientes identificados con ventas positivas**, los **{es(u['top10_clientes_n'],0)} clientes de mayor importe**, aproximadamente el 10%, concentran **{es(u['top10_clientes_porcentaje'])}%** de las ventas identificadas. **{es(u['clientes_recurrentes']/u['clientes_ventas']*100)}%** de estos clientes tienen al menos dos facturas en la ventana observada; es recurrencia observada, no una tasa de retención.

La factura positiva mediana suma **GBP {es(u['ticket_mediano'])}**, mientras que el percentil 95 alcanza **GBP {es(u['ticket_p95'])}**. La asimetría es compatible con la presencia de compradores mayoristas descrita por la fuente, pero no identifica qué clientes son mayoristas. Noviembre de 2011 suma **GBP {es(u['noviembre_2011'])}**; diciembre de 2011 termina el día 9, de modo que su descenso no permite concluir una caída de demanda mensual.

Las **{es(u['cancelaciones_facturas'],0)} facturas con prefijo C** registran **GBP {es(u['importe_cancelaciones'])}** de importe firmado. El total firmado de todas las líneas, incluidos otros ajustes, es **GBP {es(u['importe_total_firmado'])}**. Las cancelaciones no se emparejaron con ventas originales, por lo que no se presenta una tasa de devolución. Faltan identificadores de cliente en **{es(u['clientes_faltantes']/u['filas']*100)}% de las líneas** y se conservan **{es(u['duplicados'],0)} duplicados completos adicionales** al no poder confirmar que sean errores.

La lectura empresarial principal es una exposición relevante a pocos clientes identificados y al mercado británico. Conviene investigar la naturaleza de esa concentración y de los ajustes antes de interpretar estabilidad comercial. La ausencia de clientes en parte de las líneas limita la extrapolación; no hay costos ni evidencia causal.

[Informe completo de Online Retail](edas/online_retail/reports/informe_eda.md) · [Gráficos](edas/online_retail/reports/figures/) · [Tablas](edas/online_retail/reports/tables/)

Los dos análisis conservan faltantes y extremos, explicitan sus poblaciones y distinguen hallazgos de hipótesis. Fuente Olist: [Kaggle, versión 2](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Fuente Online Retail: [Daqing Chen, UCI (2015)](https://doi.org/10.24432/C5BW33), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [Metodología y organización técnica](docs/metodologia.md).
''',encoding='utf-8')
