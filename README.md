# Informe ejecutivo: dos análisis del comercio electrónico

El análisis de Olist sitúa la entrega como un punto relevante de la experiencia del comprador. Online Retail muestra una actividad concentrada en Reino Unido y en una fracción de sus clientes identificados, con importes de factura muy desiguales. Son dos EDAs independientes: corresponden a empresas, periodos, monedas y unidades de observación diferentes. Sus cifras no se suman ni permiten comparar directamente desempeño comercial.

## 1. Olist: entregas y satisfacción del comprador

El dataset brasileño de Olist reúne **99.441 pedidos** de 2016–2018 distribuidos en nueve tablas. Entre los **96.470 pedidos entregados con fechas completas**, la mediana de entrega es **10,22 días** y el percentil 95 llega a **29,27 días**. **7.826 pedidos (8,11%)** llegaron después de la fecha y hora estimadas.

La experiencia de entrega se asocia con diferencias en reseñas. Entre pedidos entregados con fechas y puntuación disponibles, la puntuación media es **4,29/5 cuando llegan a tiempo**, frente a **2,57/5 cuando llegan tarde**. La correlación de Spearman entre duración y puntuación es **-0,235**. Esta asociación justifica estudiar los pedidos demorados, pero no demuestra que el retraso explique por sí solo la valoración: vendedores, categorías, distancias y selección de quienes reseñan pueden influir.

La calidad estructural permite analizar los pedidos sin multiplicarlos al cruzar tablas: artículos, pagos y reseñas se agregaron previamente por pedido. Hay **260 discrepancias mayores a BRL 0,05** entre pagos y precio más flete sobre **98.665 pedidos comparables**; requieren contexto contable y no prueban fraude. La repetición de registros geográficos y de claves de reseña exige tratar cada tabla según su granularidad.

La lectura empresarial principal es la presencia de una cola de entregas prolongadas asociada a menor satisfacción. La puntualidad descrita excluye cancelaciones y pedidos sin fechas completas; el dataset histórico no representa todo el comercio brasileño actual. Las cifras monetarias son BRL nominales y no describen margen.

[Informe completo de Olist](edas/olist/reports/informe_eda.md) · [Gráficos](edas/olist/reports/figures/) · [Tablas](edas/olist/reports/tables/)

## 2. Online Retail: concentración comercial y facturas heterogéneas

El archivo de UCI contiene **541.909 líneas de factura** de un comercio británico, del 1 de diciembre de 2010 al 9 de diciembre de 2011. Las ventas positivas —cantidades y precios mayores que cero, fecha y factura disponibles y sin prefijo de cancelación C— reúnen **19.960 facturas** y suman **GBP 10.666.684,54**. Este importe incluye los cargos presentes en esas líneas y no equivale a beneficio ni cobros auditados.

**Reino Unido concentra el 84,61% del importe positivo.** Entre **4.338 clientes identificados con ventas positivas**, los **434 clientes de mayor importe**, aproximadamente el 10%, concentran **61,38%** de las ventas identificadas. **65,58%** de estos clientes tienen al menos dos facturas en la ventana observada; es recurrencia observada, no una tasa de retención.

La factura positiva mediana suma **GBP 303,84**, mientras que el percentil 95 alcanza **GBP 1.585,92**. La asimetría es compatible con la presencia de compradores mayoristas descrita por la fuente, pero no identifica qué clientes son mayoristas. Noviembre de 2011 suma **GBP 1.509.496,33**; diciembre de 2011 termina el día 9, de modo que su descenso no permite concluir una caída de demanda mensual.

Las **3.836 facturas con prefijo C** registran **GBP -896.812,49** de importe firmado. El total firmado de todas las líneas, incluidos otros ajustes, es **GBP 9.747.747,93**. Las cancelaciones no se emparejaron con ventas originales, por lo que no se presenta una tasa de devolución. Faltan identificadores de cliente en **24,93% de las líneas** y se conservan **5.268 duplicados completos adicionales** al no poder confirmar que sean errores.

La lectura empresarial principal es una exposición relevante a pocos clientes identificados y al mercado británico. Conviene investigar la naturaleza de esa concentración y de los ajustes antes de interpretar estabilidad comercial. La ausencia de clientes en parte de las líneas limita la extrapolación; no hay costos ni evidencia causal.

[Informe completo de Online Retail](edas/online_retail/reports/informe_eda.md) · [Gráficos](edas/online_retail/reports/figures/) · [Tablas](edas/online_retail/reports/tables/)

Los dos análisis conservan faltantes y extremos, explicitan sus poblaciones y distinguen hallazgos de hipótesis. Fuente Olist: [Kaggle, versión 2](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Fuente Online Retail: [Daqing Chen, UCI (2015)](https://doi.org/10.24432/C5BW33), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [Metodología y organización técnica](docs/metodologia.md).
