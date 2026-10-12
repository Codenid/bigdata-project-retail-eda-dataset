# Comercio electrónico: informe ejecutivo

Tres EDAs independientes describen entrega y satisfacción, concentración comercial y calidad de datos operativos. Sus empresas, periodos y poblaciones difieren; los importes no se suman ni permiten comparar desempeño directamente.

## 1. Olist: entrega y satisfacción

Sobre **99.441 pedidos**, la entrega mediana es **10,22 días**. De 96.470 entregados con fechas completas, **8,11%** llegó después de la estimación registrada.

La reseña media es **4,29/5 a tiempo** y **2,57/5 tarde**, entre pedidos con reseña. La demora se asocia con menor puntuación, sin demostrar causalidad. Los meses parciales, faltantes y selección de entregados limitan la comparación. Los importes son BRL nominales.

[Informe Olist](edas/olist/reports/informe_eda.md). Fuente: Olist, Kaggle versión 2; CC BY-NC-SA 4.0.

## 2. Online Retail: concentración comercial

Las **19.960 facturas de ventas positivas** suman **GBP 10.666.684,54**. Reino Unido reúne **84,61%** de ese importe. El 10% superior de los 4.338 clientes identificados concentra **61,38%** de las ventas identificadas.

Falta cliente en **24,93%** de las líneas. Las cancelaciones y ajustes se distinguen de ventas positivas; no se emparejaron devoluciones con compras. La concentración es un hallazgo; no confirma margen ni estabilidad futura.

[Informe Online Retail](edas/online_retail/reports/informe_eda.md). Fuente: Daqing Chen, UCI (2015); CC BY 4.0.

## 3. The Look: estructura íntegra y fechas por aclarar

Las exportaciones de BigQuery reúnen **125.303 pedidos**, **181.458 líneas** y **2.426.096 eventos**. Las claves son únicas y los nueve enlaces comprobados cubren todas las referencias no nulas. Las líneas suman **10.795.147,15**, pero solo **2.685.055,36** corresponde al estado Complete; la moneda y el reconocimiento de ingresos no están documentados.

**29,96%** de las líneas con creación y envío tiene el envío anterior a su creación. Además, todas las líneas enlazan unidades sin sold_at, aunque el inventario cuenta 181.458 unidades con esa fecha. Se requiere aclarar estas diferencias antes de interpretar stock o tiempos. El **46,41%** de eventos no tiene usuario; no se atribuye conversión a pedidos.

[Informe The Look](edas/the_look/reports/informe_eda.md). Fuente: CSV agregados aportados tras ejecutar BigQuery; origen exacto y licencia pendientes de confirmar.

Los tres análisis conservan extremos y faltantes, explicitan denominadores y distinguen hallazgos de hipótesis. [Organización y metodología](docs/metodologia.md).
