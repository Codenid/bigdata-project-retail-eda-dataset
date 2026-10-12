# The Look: diagrama ER

El modelo conecta **pedidos y líneas** con usuarios, productos, unidades de inventario y centros. Los eventos describen actividad del usuario; no tienen una clave directa hacia pedidos.

```mermaid
erDiagram
    USERS ||--o{ ORDERS : "user_id"
    USERS ||--o{ ORDER_ITEMS : "user_id"
    USERS |o--o{ EVENTS : "user_id opcional"
    ORDERS ||--|{ ORDER_ITEMS : "order_id, 1 a 4 lineas"
    PRODUCTS ||--o{ ORDER_ITEMS : "product_id"
    PRODUCTS ||--o{ INVENTORY_ITEMS : "product_id"
    INVENTORY_ITEMS ||--o| ORDER_ITEMS : "inventory_item_id"
    DISTRIBUTION_CENTERS ||--o{ PRODUCTS : "distribution_center_id"
    DISTRIBUTION_CENTERS ||--o{ INVENTORY_ITEMS : "product_distribution_center_id"

    USERS {
        int id PK
        string country
        string state
    }
    ORDERS {
        int order_id PK
        int user_id FK
        string status
        int num_of_item
        timestamp created_at
    }
    ORDER_ITEMS {
        int id PK
        int order_id FK
        int user_id FK
        int product_id FK
        int inventory_item_id FK "no repetido en las lineas exportadas"
        string status
        float sale_price
        timestamp created_at
        timestamp shipped_at
        timestamp delivered_at
        timestamp returned_at
    }
    PRODUCTS {
        int id PK
        int distribution_center_id FK
        string category
        string department
        float retail_price
        float cost
    }
    INVENTORY_ITEMS {
        int id PK
        int product_id FK
        int product_distribution_center_id FK
        timestamp created_at
        timestamp sold_at "no demuestra stock disponible"
        float cost
    }
    EVENTS {
        int id PK
        int user_id FK "puede ser nulo"
        string session_id "agrupa eventos"
        int sequence_number
        string event_type
        timestamp created_at
    }
    DISTRIBUTION_CENTERS {
        int id PK
        string name
    }
```

## Relaciones comprobadas en las exportaciones

| Relación | Lectura |
| --- | --- |
| users → orders | 1:N; hay usuarios sin pedidos |
| orders → order_items | 1:N; cada pedido observado tiene entre 1 y 4 líneas |
| users → order_items | 1:N; el usuario coincide con el del pedido en los casos comparables |
| products → líneas e inventario | 1:N; cada registro referencia un producto existente |
| inventory_items → order_items | 1:0..1; una unidad aparece como máximo en una línea |
| distribution_centers → products e inventory_items | 1:N por los identificadores de centro respectivos |
| users → events | 1:N; el usuario del evento es opcional |

Las siete claves candidatas son únicas y no nulas. Los nueve enlaces tienen 100% de cobertura entre referencias no nulas, sin padres duplicados. Estas conclusiones proceden de agregados exportados, no de una nueva consulta al origen.

## Precauciones de unión e interpretación

**Para analizar pedidos, agregar primero sus líneas.** Una unión desde orders a order_items repite los atributos del pedido; no sumar num_of_item después de esa unión.

El 46,41% de eventos no tiene user_id. session_id agrupa eventos, pero no enlaza con orders. Unir eventos y pedidos solo por usuario produciría combinaciones, sin demostrar que una sesión generó una compra.

Las 181.458 líneas apuntan a unidades sin sold_at, aunque el inventario contiene 181.458 unidades con esa fecha. La coincidencia de conteos no demuestra que sean las mismas unidades. **No interpretar sold_at nulo como stock disponible.**

Las fechas de envío son anteriores a la creación en el 29,96% de líneas comparables. El modelo relacional no valida esa cronología ni permite afirmar ingresos netos; sale_price debe interpretarse por estado y su moneda no está confirmada.

[Informe EDA](../../edas/the_look/reports/informe_eda.md) · [Relaciones](../../edas/the_look/reports/tables/relaciones.csv) · [Alertas temporales](../../edas/the_look/reports/tables/alertas_temporales.csv) · [Mermaid editable](the_look.mmd)
