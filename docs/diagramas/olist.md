# Olist: diagrama ER

El **pedido** es el centro del modelo. Una fila de order_items es una línea de pedido; pagos y reseñas tienen sus propios registros.

```mermaid
erDiagram
    CUSTOMERS ||--|| ORDERS : "customer_id"
    ORDERS ||--o{ ORDER_ITEMS : "order_id"
    ORDERS ||--o{ ORDER_PAYMENTS : "order_id"
    ORDERS ||--o{ ORDER_REVIEWS : "order_id"
    PRODUCTS ||--o{ ORDER_ITEMS : "product_id"
    SELLERS ||--o{ ORDER_ITEMS : "seller_id"
    CATEGORY_TRANSLATION |o--o{ PRODUCTS : "product_category_name"
    CUSTOMERS }o..o{ GEOLOCATION : "prefijo postal, enlace logico"
    SELLERS }o..o{ GEOLOCATION : "prefijo postal, enlace logico"

    CUSTOMERS {
        string customer_id PK
        string customer_unique_id "identidad recurrente"
        string customer_zip_code_prefix "prefijo postal"
    }
    ORDERS {
        string order_id PK
        string customer_id FK
        string order_status
        datetime order_purchase_timestamp
        datetime order_delivered_customer_date
    }
    ORDER_ITEMS {
        string order_id PK, FK "clave compuesta"
        string order_item_id PK "clave compuesta"
        string product_id FK
        string seller_id FK
        decimal price "BRL"
        decimal freight_value "BRL"
    }
    ORDER_PAYMENTS {
        string order_id PK, FK "clave compuesta"
        int payment_sequential PK "clave compuesta"
        decimal payment_value "BRL"
    }
    ORDER_REVIEWS {
        string review_id "no unico"
        string order_id FK
        int review_score
    }
    PRODUCTS {
        string product_id PK
        string product_category_name "puede faltar o no tener traduccion"
    }
    SELLERS {
        string seller_id PK
        string seller_zip_code_prefix "prefijo postal"
    }
    CATEGORY_TRANSLATION {
        string product_category_name PK
        string product_category_name_english
    }
    GEOLOCATION {
        string geolocation_zip_code_prefix "no unico"
        decimal geolocation_lat
        decimal geolocation_lng
    }
```

## Relaciones principales

| Relación | Lectura |
| --- | --- |
| customers → orders | 1:1 por customer_id en el archivo observado |
| orders → líneas, pagos y reseñas | 1:N; algunos pedidos no tienen registros asociados |
| products y sellers → order_items | Cada línea identifica un producto y un vendedor |
| traducción → products | Una categoría agrupa productos; puede faltar la traducción |
| clientes/vendedores ↔ geolocation | Un prefijo puede repetirse en ambos lados; enlace postal N:M |

`customer_id` corresponde al registro del cliente del pedido. Para reconocer recurrencia se usa `customer_unique_id`, que puede repetirse. `CATEGORY_TRANSLATION` representa la tabla original product_category_name_translation.

## Precauciones de unión

**Agregar antes de unir:** sumar price y freight_value por pedido, sumar pagos y promediar reseñas. Después unir a orders y comprobar que se conservan sus 99.441 pedidos. Unir los detalles directamente puede multiplicar filas e importes.

`review_id` no es único: hay 814 repeticiones adicionales. Geolocation tampoco tiene una clave única por prefijo; debe prepararse una fila por prefijo antes de usarla como dimensión. Hay 610 productos sin categoría y 13 sin traducción; conservar esos faltantes.

[Informe EDA](../../edas/olist/reports/informe_eda.md) · [Claves](../../edas/olist/reports/tables/claves.csv) · [Referencias](../../edas/olist/reports/tables/integridad_referencial.csv) · [Mermaid editable](olist.mmd)
