# The Look: informe EDA

## Alcance

Se revisaron tres CSV agregados de BigQuery: **125.303 pedidos**, **181.458 líneas**, **100.000 usuarios**, 29.120 productos, 489.869 registros de inventario, 2.426.096 eventos y 10 centros. Los pedidos abarcan del 2019-01-09 al 2026-10-12. El origen exacto, la licencia y los trabajos de consulta no están confirmados en las exportaciones.

## Ventas y demanda observada

Las líneas suman **10.795.147,15**, incluyendo todos los estados; la moneda no está documentada. Solo el estado **Complete** reúne 31.327 pedidos y 2.685.055,36 de importe de líneas. Ninguno de estos importes confirma cobros o beneficio.

| Estado del pedido | Pedidos | % del total |
| --- | ---: | ---: |
| Shipped | 37.650 | 30,05% |
| Complete | 31.327 | 25,00% |
| Processing | 25.166 | 20,08% |
| Cancelled | 18.810 | 15,01% |
| Returned | 12.350 | 9,86% |

Hay **1,45 líneas por pedido** y 80.035 usuarios con pedidos. Intimates lidera en líneas (13.713); Outerwear & Coats lidera en importe (1.327.471,86). Son registros de demanda en todos los estados, no ventas netas. China reúne 33,77% de los pedidos según el país del usuario, sin confirmar destino de entrega.

![Estados de pedidos](figures/estados_pedidos.png)

## Inventario y logística

**308.411 unidades carecen de sold_at** y 181.458 tienen esa fecha. Sin embargo, las **181.458 líneas vinculadas a unidades únicas apuntan a registros sin sold_at**. La igualdad entre el total de líneas y unidades con fecha no demuestra que sean las mismas unidades. Esta diferencia debe contrastarse en el origen antes de interpretar disponibilidad o ventas de inventario.

**35.231 de 117.596 líneas con ambas fechas (29,96%) tienen envío anterior a su creación**. En pedidos, la exportación no señala esa inversión. La duración media envío–entrega es 60,13 horas para 43.677 pedidos con ambas fechas; no incluye preparación ni mide cumplimiento de una promesa.

También hay fechas posteriores al inicio de las consultas. No se eliminan: las fechas de líneas y pedidos requieren aclaración antes de comparar tiempos o meses parciales.

## Eventos y relaciones

Se registran **681.458 sesiones**. El 46,41% de los eventos no tiene user_id. Los tipos product, cart y purchase describen actividad, pero no permiten calcular conversión atribuida a pedidos: no hay un enlace directo de sesión a pedido en el esquema.

Las siete claves candidatas no presentan nulos ni repeticiones. Los nueve enlaces revisados tienen **100% de cobertura entre claves no nulas**, sin padres duplicados. num_of_item coincide con el conteo de líneas de los 125.303 pedidos comparables; tampoco aparecen diferencias de usuario o producto en las comparaciones exportadas. Un pedido tiene entre una y cuatro líneas: para analizar pedidos hay que agregar esas líneas antes de unir, aunque las claves padre sean únicas.

## Lectura final

La estructura permite relacionar pedidos, usuarios y productos. Los importes dependen del estado y las fechas presentan diferencias relevantes entre pedidos y líneas. **No hay base para afirmar stock disponible, ingresos netos o conversión comercial.** El análisis usa agregados exportados; valida sus balances, sin volver a consultar BigQuery ni auditar sus registros individuales.

Evidencia: [métricas](metricas.json), [relaciones](tables/relaciones.csv), [alertas temporales](tables/alertas_temporales.csv), [categorías](tables/categorias.csv), [países](tables/paises.csv) y [huellas de los CSV](fuentes.json). Gráficos: [categorías](figures/categorias.png), [países](figures/paises.png), [eventos](figures/eventos.png) y [pedidos mensuales](figures/pedidos_mensuales.png).
