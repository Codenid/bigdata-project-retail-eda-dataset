# Diagramas ER: tres fuentes independientes

Cada fuente tiene su propio modelo. No se relacionan sus clientes, pedidos ni productos entre datasets.

| Fuente | Estructura | Diagrama y explicación |
| --- | --- | --- |
| Olist | Nueve tablas relacionadas por pedido, producto y vendedor | [Olist](olist.md) |
| Online Retail | Una tabla de líneas; facturas, clientes y productos son entidades conceptuales | [Online Retail](online_retail.md) |
| The Look | Siete tablas de usuarios, pedidos, líneas, inventario, productos, eventos y centros | [The Look](the_look.md) |

## Cómo leerlos

- **PK:** clave única. Si varias columnas llevan PK, forman una clave compuesta.
- **FK:** columna usada para relacionar tablas; no implica una restricción impuesta por el archivo.
- **1:1:** una fila se relaciona con una fila. **1:N:** una fila se relaciona con varias.
- En Mermaid: `||` = uno; `o|` o `|o` = cero o uno; `|{` = uno o más; `o{` = cero o más. Las llaves al lado izquierdo se leen de forma equivalente.
- Los diagramas muestran claves y campos esenciales, no todas las columnas. Las líneas punteadas de Olist representan enlaces postales que requieren preparación.

Olist y Online Retail se contrastaron con sus archivos locales. The Look se describe a partir del esquema y las exportaciones agregadas de BigQuery; sus cardinalidades corresponden a esos resultados.
