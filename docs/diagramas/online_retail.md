# Online Retail: diagrama ER

## Archivo original

Online Retail.xlsx contiene **una sola tabla**, con 541.909 líneas. InvoiceNo agrupa las líneas de una factura; no identifica una fila.

```mermaid
erDiagram
    ONLINE_RETAIL {
        string InvoiceNo "factura; C indica cancelacion"
        string StockCode "codigo de producto o cargo"
        string Description "descripcion, puede faltar"
        int Quantity "unidades con signo"
        datetime InvoiceDate "fecha y hora de la linea"
        decimal UnitPrice "precio unitario en GBP"
        string CustomerID "cliente, puede faltar"
        string Country "pais registrado del cliente"
    }
```

## Modelo conceptual

Este segundo diagrama explica las entidades que podrían separarse. **No son tablas existentes ni una transformación realizada.** Sus claves son propuestas.

```mermaid
erDiagram
    CLIENTE |o--o{ FACTURA : "asociacion opcional por CustomerID"
    FACTURA ||--|{ LINEA_FACTURA : "agrupa InvoiceNo"
    PRODUCTO_O_CARGO ||--|{ LINEA_FACTURA : "agrupa StockCode"

    CLIENTE {
        string CustomerID PK "clave propuesta; excluir nulos"
    }
    FACTURA {
        string InvoiceNo PK "clave propuesta de agrupacion"
        string CustomerID FK "opcional"
        string Country "valor observado por factura"
        boolean es_cancelacion "derivado del prefijo C"
    }
    LINEA_FACTURA {
        int fila_origen PK "clave tecnica propuesta, no existe en Excel"
        string InvoiceNo FK
        string StockCode FK
        string Description "se conserva en la linea"
        int Quantity
        datetime InvoiceDate "se conserva por variacion intrafactura"
        decimal UnitPrice "se conserva en la linea"
        decimal importe "derivado Quantity por UnitPrice"
    }
    PRODUCTO_O_CARGO {
        string StockCode PK "clave propuesta de agrupacion"
    }
```

| Relación | Lectura |
| --- | --- |
| cliente → facturas | 1:N; una factura puede no tener cliente conocido |
| factura → líneas | 1:N por InvoiceNo |
| producto o cargo → líneas | 1:N por StockCode |

## Precauciones de interpretación

**InvoiceNo + StockCode no es una clave única:** tiene 10.684 repeticiones adicionales. fila_origen es una clave técnica propuesta para distinguir líneas, incluidos duplicados.

Falta CustomerID en el 24,93% de las líneas. Description y UnitPrice pertenecen a la línea: no se presume descripción ni precio único por producto. La fecha también se conserva allí, porque 43 facturas tienen dos valores de InvoiceDate.

El importe es Quantity × UnitPrice, en GBP. El prefijo C identifica cancelaciones, pero no hay una clave que las enlace con la venta original. No se calcula una tasa de devolución a partir de esa relación inexistente.

[Informe EDA](../../edas/online_retail/reports/informe_eda.md) · [Calidad](../../edas/online_retail/reports/tables/calidad.csv) · [Mermaid original](online_retail_original.mmd) · [Mermaid conceptual](online_retail_conceptual.mmd)
