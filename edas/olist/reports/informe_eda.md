# Olist: informe EDA

## Alcance

**99,441 pedidos** de 2016–2018, distribuidos en nueve tablas. Fuente: [Olist en Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), versión 2, licencia [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Los importes están en BRL nominales.

## Hallazgos principales

| Indicador | Resultado | Población |
| --- | ---: | --- |
| Mediana de entrega | 10.22 días | 96,470 entregados con fechas completas |
| Percentil 95 de entrega | 29.27 días | Misma población |
| Entregados tarde | 7,826 (8.11%) | Misma población; después de la hora estimada |
| Reseña media a tiempo | 4.29/5 | 88,163 pedidos con reseña |
| Reseña media tarde | 2.57/5 | 7,661 pedidos con reseña |

Las entregas más largas se asocian con puntuaciones menores: Spearman **-0.235**, sobre 95,824 pedidos entregados con fechas y reseña. La asociación no demuestra causalidad; vendedor, categoría y selección de quienes reseñan pueden influir.

![Reseñas según puntualidad](figures/resenas_demora.png)

El precio por artículo tiene mediana **BRL 74.99** y P99 **BRL 890.00**. Los extremos se conservan. Hay **260 discrepancias superiores a BRL 0,05** entre pagos y precio más flete, sobre 98,665 pedidos comparables; no prueban fraude.

## Calidad y límites

Las claves de pedidos, clientes, productos y vendedores son únicas y las referencias principales están completas. Las reseñas repiten identificadores; la geolocalización repite prefijos. Hay 610 productos sin categoría y 13 sin traducción correspondiente. Los faltantes se mantienen, sin imputación.

Artículos y pagos se sumaron por pedido; reseñas se promediaron. Las uniones 1:1 conservan los 99,441 pedidos. La puntualidad excluye cancelaciones y entregas sin fechas completas. El dataset histórico no representa todo Brasil ni permite estimar margen.

## Evidencia

[Métricas](metricas.json), [dimensiones](tables/dimensiones.csv), [calidad](tables/columnas_calidad.csv), [claves](tables/claves.csv), [referencias](tables/integridad_referencial.csv), [estadísticas](tables/estadisticas_numericas.csv) y [denominadores de correlación](tables/n_pares_correlacion.csv). [Entrega](figures/entrega.png), [pedidos mensuales](figures/pedidos_mensuales.png) y [precios](figures/precios.png).

SHA-256 de la fuente: `967e41e04fc306fe604e2a693f488995a8b41e5047418f8a5c8e4abd6deca784`. Datos originales intactos y excluidos de Git.
