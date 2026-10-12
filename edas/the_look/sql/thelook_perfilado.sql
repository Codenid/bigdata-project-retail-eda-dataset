-- GoogleSQL / BigQuery. Solo lectura: tres SELECT independientes.
-- Sustituir bigquery-public-data.thelook_ecommerce por el origen confirmado. No ejecutado.

-- BLOQUE 1. Exportar thelook_perfil_tablas.csv
WITH
perfil_distribution_centers AS (
  SELECT 'distribution_centers' AS tabla, [
    STRUCT('*' AS campo, 'filas' AS metrica, CAST(COUNT(*) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'valores_distintos_no_nulos' AS metrica, CAST(COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'repeticiones_adicionales_no_nulas' AS metrica, CAST(COUNT(id) - COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador)
  ] AS metricas
  FROM `bigquery-public-data.thelook_ecommerce.distribution_centers`
),
perfil_events AS (
  SELECT 'events' AS tabla, [
    STRUCT('*' AS campo, 'filas' AS metrica, CAST(COUNT(*) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'valores_distintos_no_nulos' AS metrica, CAST(COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'repeticiones_adicionales_no_nulas' AS metrica, CAST(COUNT(id) - COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('user_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(user_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('sequence_number' AS campo, 'nulos' AS metrica, CAST(COUNTIF(sequence_number IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('session_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(session_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(created_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(created_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('state' AS campo, 'nulos' AS metrica, CAST(COUNTIF(state IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('browser' AS campo, 'nulos' AS metrica, CAST(COUNTIF(browser IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('traffic_source' AS campo, 'nulos' AS metrica, CAST(COUNTIF(traffic_source IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('event_type' AS campo, 'nulos' AS metrica, CAST(COUNTIF(event_type IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador)
  ] AS metricas
  FROM `bigquery-public-data.thelook_ecommerce.events`
),
perfil_inventory_items AS (
  SELECT 'inventory_items' AS tabla, [
    STRUCT('*' AS campo, 'filas' AS metrica, CAST(COUNT(*) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'valores_distintos_no_nulos' AS metrica, CAST(COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'repeticiones_adicionales_no_nulas' AS metrica, CAST(COUNT(id) - COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('product_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(product_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(created_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(created_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('sold_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(sold_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('sold_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(sold_at) AS STRING) AS valor, CAST(COUNT(sold_at) AS INT64) AS denominador),
    STRUCT('sold_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(sold_at) AS STRING) AS valor, CAST(COUNT(sold_at) AS INT64) AS denominador),
    STRUCT('sold_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(sold_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(sold_at) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'nulos' AS metrica, CAST(COUNTIF(cost IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'no_finitos' AS metrica, CAST(COUNTIF(IS_NAN(cost) OR IS_INF(cost)) AS STRING) AS valor, CAST(COUNT(cost) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'negativos_finitos' AS metrica, CAST(COUNTIF((cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AND cost < 0) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'ceros_finitos' AS metrica, CAST(COUNTIF((cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AND cost = 0) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'min_finitos' AS metrica, CAST(MIN(IF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost), cost, NULL)) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'max_finitos' AS metrica, CAST(MAX(IF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost), cost, NULL)) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'suma_finitos' AS metrica, CAST(SUM(IF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost), cost, NULL)) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('product_category' AS campo, 'nulos' AS metrica, CAST(COUNTIF(product_category IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('product_brand' AS campo, 'nulos' AS metrica, CAST(COUNTIF(product_brand IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('product_retail_price' AS campo, 'nulos' AS metrica, CAST(COUNTIF(product_retail_price IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('product_retail_price' AS campo, 'no_finitos' AS metrica, CAST(COUNTIF(IS_NAN(product_retail_price) OR IS_INF(product_retail_price)) AS STRING) AS valor, CAST(COUNT(product_retail_price) AS INT64) AS denominador),
    STRUCT('product_retail_price' AS campo, 'negativos_finitos' AS metrica, CAST(COUNTIF((product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price)) AND product_retail_price < 0) AS STRING) AS valor, CAST(COUNTIF(product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price)) AS INT64) AS denominador),
    STRUCT('product_retail_price' AS campo, 'ceros_finitos' AS metrica, CAST(COUNTIF((product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price)) AND product_retail_price = 0) AS STRING) AS valor, CAST(COUNTIF(product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price)) AS INT64) AS denominador),
    STRUCT('product_retail_price' AS campo, 'min_finitos' AS metrica, CAST(MIN(IF(product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price), product_retail_price, NULL)) AS STRING) AS valor, CAST(COUNTIF(product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price)) AS INT64) AS denominador),
    STRUCT('product_retail_price' AS campo, 'max_finitos' AS metrica, CAST(MAX(IF(product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price), product_retail_price, NULL)) AS STRING) AS valor, CAST(COUNTIF(product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price)) AS INT64) AS denominador),
    STRUCT('product_retail_price' AS campo, 'suma_finitos' AS metrica, CAST(SUM(IF(product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price), product_retail_price, NULL)) AS STRING) AS valor, CAST(COUNTIF(product_retail_price IS NOT NULL AND NOT IS_NAN(product_retail_price) AND NOT IS_INF(product_retail_price)) AS INT64) AS denominador),
    STRUCT('product_department' AS campo, 'nulos' AS metrica, CAST(COUNTIF(product_department IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('product_sku' AS campo, 'nulos' AS metrica, CAST(COUNTIF(product_sku IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('product_distribution_center_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(product_distribution_center_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at->sold_at' AS campo, 'venta_anterior_al_registro' AS metrica, CAST(COUNTIF(sold_at < created_at) AS STRING) AS valor, CAST(COUNTIF(sold_at IS NOT NULL AND created_at IS NOT NULL) AS INT64) AS denominador)
  ] AS metricas
  FROM `bigquery-public-data.thelook_ecommerce.inventory_items`
),
perfil_order_items AS (
  SELECT 'order_items' AS tabla, [
    STRUCT('*' AS campo, 'filas' AS metrica, CAST(COUNT(*) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'valores_distintos_no_nulos' AS metrica, CAST(COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'repeticiones_adicionales_no_nulas' AS metrica, CAST(COUNT(id) - COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('order_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(order_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('user_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(user_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('product_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(product_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('inventory_item_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(inventory_item_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('status' AS campo, 'nulos' AS metrica, CAST(COUNTIF(status IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(created_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(created_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('shipped_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(shipped_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('shipped_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(shipped_at) AS STRING) AS valor, CAST(COUNT(shipped_at) AS INT64) AS denominador),
    STRUCT('shipped_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(shipped_at) AS STRING) AS valor, CAST(COUNT(shipped_at) AS INT64) AS denominador),
    STRUCT('shipped_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(shipped_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(shipped_at) AS INT64) AS denominador),
    STRUCT('delivered_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(delivered_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('delivered_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(delivered_at) AS STRING) AS valor, CAST(COUNT(delivered_at) AS INT64) AS denominador),
    STRUCT('delivered_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(delivered_at) AS STRING) AS valor, CAST(COUNT(delivered_at) AS INT64) AS denominador),
    STRUCT('delivered_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(delivered_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(delivered_at) AS INT64) AS denominador),
    STRUCT('returned_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(returned_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('returned_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(returned_at) AS STRING) AS valor, CAST(COUNT(returned_at) AS INT64) AS denominador),
    STRUCT('returned_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(returned_at) AS STRING) AS valor, CAST(COUNT(returned_at) AS INT64) AS denominador),
    STRUCT('returned_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(returned_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(returned_at) AS INT64) AS denominador),
    STRUCT('sale_price' AS campo, 'nulos' AS metrica, CAST(COUNTIF(sale_price IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('sale_price' AS campo, 'no_finitos' AS metrica, CAST(COUNTIF(IS_NAN(sale_price) OR IS_INF(sale_price)) AS STRING) AS valor, CAST(COUNT(sale_price) AS INT64) AS denominador),
    STRUCT('sale_price' AS campo, 'negativos_finitos' AS metrica, CAST(COUNTIF((sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price)) AND sale_price < 0) AS STRING) AS valor, CAST(COUNTIF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price)) AS INT64) AS denominador),
    STRUCT('sale_price' AS campo, 'ceros_finitos' AS metrica, CAST(COUNTIF((sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price)) AND sale_price = 0) AS STRING) AS valor, CAST(COUNTIF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price)) AS INT64) AS denominador),
    STRUCT('sale_price' AS campo, 'min_finitos' AS metrica, CAST(MIN(IF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price), sale_price, NULL)) AS STRING) AS valor, CAST(COUNTIF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price)) AS INT64) AS denominador),
    STRUCT('sale_price' AS campo, 'max_finitos' AS metrica, CAST(MAX(IF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price), sale_price, NULL)) AS STRING) AS valor, CAST(COUNTIF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price)) AS INT64) AS denominador),
    STRUCT('sale_price' AS campo, 'suma_finitos' AS metrica, CAST(SUM(IF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price), sale_price, NULL)) AS STRING) AS valor, CAST(COUNTIF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price)) AS INT64) AS denominador),
    STRUCT('created_at->shipped_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(shipped_at < created_at) AS STRING) AS valor, CAST(COUNTIF(created_at IS NOT NULL AND shipped_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('created_at->delivered_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(delivered_at < created_at) AS STRING) AS valor, CAST(COUNTIF(created_at IS NOT NULL AND delivered_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('shipped_at->delivered_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(delivered_at < shipped_at) AS STRING) AS valor, CAST(COUNTIF(shipped_at IS NOT NULL AND delivered_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('created_at->returned_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(returned_at < created_at) AS STRING) AS valor, CAST(COUNTIF(created_at IS NOT NULL AND returned_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('delivered_at->returned_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(returned_at < delivered_at) AS STRING) AS valor, CAST(COUNTIF(delivered_at IS NOT NULL AND returned_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('shipped_at,delivered_at' AS campo, 'entrega_sin_envio' AS metrica, CAST(COUNTIF(delivered_at IS NOT NULL AND shipped_at IS NULL) AS STRING) AS valor, CAST(COUNTIF(delivered_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('created_at->shipped_at' AS campo, 'duracion_media_horas_con_signo' AS metrica, CAST(AVG(TIMESTAMP_DIFF(shipped_at, created_at, SECOND) / 3600.0) AS STRING) AS valor, CAST(COUNTIF(created_at IS NOT NULL AND shipped_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('shipped_at->delivered_at' AS campo, 'duracion_media_horas_con_signo' AS metrica, CAST(AVG(TIMESTAMP_DIFF(delivered_at, shipped_at, SECOND) / 3600.0) AS STRING) AS valor, CAST(COUNTIF(shipped_at IS NOT NULL AND delivered_at IS NOT NULL) AS INT64) AS denominador)
  ] AS metricas
  FROM `bigquery-public-data.thelook_ecommerce.order_items`
),
perfil_orders AS (
  SELECT 'orders' AS tabla, [
    STRUCT('*' AS campo, 'filas' AS metrica, CAST(COUNT(*) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('order_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(order_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('order_id' AS campo, 'valores_distintos_no_nulos' AS metrica, CAST(COUNT(DISTINCT order_id) AS STRING) AS valor, CAST(COUNT(order_id) AS INT64) AS denominador),
    STRUCT('order_id' AS campo, 'repeticiones_adicionales_no_nulas' AS metrica, CAST(COUNT(order_id) - COUNT(DISTINCT order_id) AS STRING) AS valor, CAST(COUNT(order_id) AS INT64) AS denominador),
    STRUCT('user_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(user_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('status' AS campo, 'nulos' AS metrica, CAST(COUNTIF(status IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(created_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(created_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('returned_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(returned_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('returned_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(returned_at) AS STRING) AS valor, CAST(COUNT(returned_at) AS INT64) AS denominador),
    STRUCT('returned_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(returned_at) AS STRING) AS valor, CAST(COUNT(returned_at) AS INT64) AS denominador),
    STRUCT('returned_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(returned_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(returned_at) AS INT64) AS denominador),
    STRUCT('shipped_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(shipped_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('shipped_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(shipped_at) AS STRING) AS valor, CAST(COUNT(shipped_at) AS INT64) AS denominador),
    STRUCT('shipped_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(shipped_at) AS STRING) AS valor, CAST(COUNT(shipped_at) AS INT64) AS denominador),
    STRUCT('shipped_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(shipped_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(shipped_at) AS INT64) AS denominador),
    STRUCT('delivered_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(delivered_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('delivered_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(delivered_at) AS STRING) AS valor, CAST(COUNT(delivered_at) AS INT64) AS denominador),
    STRUCT('delivered_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(delivered_at) AS STRING) AS valor, CAST(COUNT(delivered_at) AS INT64) AS denominador),
    STRUCT('delivered_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(delivered_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(delivered_at) AS INT64) AS denominador),
    STRUCT('num_of_item' AS campo, 'nulos' AS metrica, CAST(COUNTIF(num_of_item IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('num_of_item' AS campo, 'cero_o_negativo' AS metrica, CAST(COUNTIF(num_of_item <= 0) AS STRING) AS valor, CAST(COUNT(num_of_item) AS INT64) AS denominador),
    STRUCT('num_of_item' AS campo, 'min' AS metrica, CAST(MIN(num_of_item) AS STRING) AS valor, CAST(COUNT(num_of_item) AS INT64) AS denominador),
    STRUCT('num_of_item' AS campo, 'max' AS metrica, CAST(MAX(num_of_item) AS STRING) AS valor, CAST(COUNT(num_of_item) AS INT64) AS denominador),
    STRUCT('created_at->shipped_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(shipped_at < created_at) AS STRING) AS valor, CAST(COUNTIF(created_at IS NOT NULL AND shipped_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('created_at->delivered_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(delivered_at < created_at) AS STRING) AS valor, CAST(COUNTIF(created_at IS NOT NULL AND delivered_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('shipped_at->delivered_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(delivered_at < shipped_at) AS STRING) AS valor, CAST(COUNTIF(shipped_at IS NOT NULL AND delivered_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('created_at->returned_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(returned_at < created_at) AS STRING) AS valor, CAST(COUNTIF(created_at IS NOT NULL AND returned_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('delivered_at->returned_at' AS campo, 'secuencia_invertida' AS metrica, CAST(COUNTIF(returned_at < delivered_at) AS STRING) AS valor, CAST(COUNTIF(delivered_at IS NOT NULL AND returned_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('shipped_at,delivered_at' AS campo, 'entrega_sin_envio' AS metrica, CAST(COUNTIF(delivered_at IS NOT NULL AND shipped_at IS NULL) AS STRING) AS valor, CAST(COUNTIF(delivered_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('created_at->shipped_at' AS campo, 'duracion_media_horas_con_signo' AS metrica, CAST(AVG(TIMESTAMP_DIFF(shipped_at, created_at, SECOND) / 3600.0) AS STRING) AS valor, CAST(COUNTIF(created_at IS NOT NULL AND shipped_at IS NOT NULL) AS INT64) AS denominador),
    STRUCT('shipped_at->delivered_at' AS campo, 'duracion_media_horas_con_signo' AS metrica, CAST(AVG(TIMESTAMP_DIFF(delivered_at, shipped_at, SECOND) / 3600.0) AS STRING) AS valor, CAST(COUNTIF(shipped_at IS NOT NULL AND delivered_at IS NOT NULL) AS INT64) AS denominador)
  ] AS metricas
  FROM `bigquery-public-data.thelook_ecommerce.orders`
),
perfil_products AS (
  SELECT 'products' AS tabla, [
    STRUCT('*' AS campo, 'filas' AS metrica, CAST(COUNT(*) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'valores_distintos_no_nulos' AS metrica, CAST(COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'repeticiones_adicionales_no_nulas' AS metrica, CAST(COUNT(id) - COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'nulos' AS metrica, CAST(COUNTIF(cost IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'no_finitos' AS metrica, CAST(COUNTIF(IS_NAN(cost) OR IS_INF(cost)) AS STRING) AS valor, CAST(COUNT(cost) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'negativos_finitos' AS metrica, CAST(COUNTIF((cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AND cost < 0) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'ceros_finitos' AS metrica, CAST(COUNTIF((cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AND cost = 0) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'min_finitos' AS metrica, CAST(MIN(IF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost), cost, NULL)) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'max_finitos' AS metrica, CAST(MAX(IF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost), cost, NULL)) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('cost' AS campo, 'suma_finitos' AS metrica, CAST(SUM(IF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost), cost, NULL)) AS STRING) AS valor, CAST(COUNTIF(cost IS NOT NULL AND NOT IS_NAN(cost) AND NOT IS_INF(cost)) AS INT64) AS denominador),
    STRUCT('category' AS campo, 'nulos' AS metrica, CAST(COUNTIF(category IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('brand' AS campo, 'nulos' AS metrica, CAST(COUNTIF(brand IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('retail_price' AS campo, 'nulos' AS metrica, CAST(COUNTIF(retail_price IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('retail_price' AS campo, 'no_finitos' AS metrica, CAST(COUNTIF(IS_NAN(retail_price) OR IS_INF(retail_price)) AS STRING) AS valor, CAST(COUNT(retail_price) AS INT64) AS denominador),
    STRUCT('retail_price' AS campo, 'negativos_finitos' AS metrica, CAST(COUNTIF((retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price)) AND retail_price < 0) AS STRING) AS valor, CAST(COUNTIF(retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price)) AS INT64) AS denominador),
    STRUCT('retail_price' AS campo, 'ceros_finitos' AS metrica, CAST(COUNTIF((retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price)) AND retail_price = 0) AS STRING) AS valor, CAST(COUNTIF(retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price)) AS INT64) AS denominador),
    STRUCT('retail_price' AS campo, 'min_finitos' AS metrica, CAST(MIN(IF(retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price), retail_price, NULL)) AS STRING) AS valor, CAST(COUNTIF(retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price)) AS INT64) AS denominador),
    STRUCT('retail_price' AS campo, 'max_finitos' AS metrica, CAST(MAX(IF(retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price), retail_price, NULL)) AS STRING) AS valor, CAST(COUNTIF(retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price)) AS INT64) AS denominador),
    STRUCT('retail_price' AS campo, 'suma_finitos' AS metrica, CAST(SUM(IF(retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price), retail_price, NULL)) AS STRING) AS valor, CAST(COUNTIF(retail_price IS NOT NULL AND NOT IS_NAN(retail_price) AND NOT IS_INF(retail_price)) AS INT64) AS denominador),
    STRUCT('department' AS campo, 'nulos' AS metrica, CAST(COUNTIF(department IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('sku' AS campo, 'nulos' AS metrica, CAST(COUNTIF(sku IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('distribution_center_id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(distribution_center_id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador)
  ] AS metricas
  FROM `bigquery-public-data.thelook_ecommerce.products`
),
perfil_users AS (
  SELECT 'users' AS tabla, [
    STRUCT('*' AS campo, 'filas' AS metrica, CAST(COUNT(*) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'nulos' AS metrica, CAST(COUNTIF(id IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'valores_distintos_no_nulos' AS metrica, CAST(COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('id' AS campo, 'repeticiones_adicionales_no_nulas' AS metrica, CAST(COUNT(id) - COUNT(DISTINCT id) AS STRING) AS valor, CAST(COUNT(id) AS INT64) AS denominador),
    STRUCT('state' AS campo, 'nulos' AS metrica, CAST(COUNTIF(state IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('country' AS campo, 'nulos' AS metrica, CAST(COUNTIF(country IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('traffic_source' AS campo, 'nulos' AS metrica, CAST(COUNTIF(traffic_source IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'nulos' AS metrica, CAST(COUNTIF(created_at IS NULL) AS STRING) AS valor, CAST(COUNT(*) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_min_UTC' AS metrica, CAST(MIN(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'fecha_max_UTC' AS metrica, CAST(MAX(created_at) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador),
    STRUCT('created_at' AS campo, 'posteriores_al_inicio_consulta' AS metrica, CAST(COUNTIF(created_at > CURRENT_TIMESTAMP()) AS STRING) AS valor, CAST(COUNT(created_at) AS INT64) AS denominador)
  ] AS metricas
  FROM `bigquery-public-data.thelook_ecommerce.users`
)
SELECT tabla, m.campo, m.metrica, m.valor, m.denominador
FROM (
  SELECT * FROM perfil_distribution_centers
UNION ALL
  SELECT * FROM perfil_events
UNION ALL
  SELECT * FROM perfil_inventory_items
UNION ALL
  SELECT * FROM perfil_order_items
UNION ALL
  SELECT * FROM perfil_orders
UNION ALL
  SELECT * FROM perfil_products
UNION ALL
  SELECT * FROM perfil_users
), UNNEST(metricas) AS m
ORDER BY tabla, campo, metrica;

-- BLOQUE 2. Exportar thelook_distribuciones.csv
WITH
productos_por_clave AS (
  SELECT id, COUNT(*) AS filas_clave, ANY_VALUE(category) AS categoria
  FROM `bigquery-public-data.thelook_ecommerce.products` WHERE id IS NOT NULL GROUP BY id
),
usuarios_por_clave AS (
  SELECT id, COUNT(*) AS filas_clave, ANY_VALUE(country) AS pais, ANY_VALUE(state) AS estado
  FROM `bigquery-public-data.thelook_ecommerce.users` WHERE id IS NOT NULL GROUP BY id
),
lineas_categoria AS (
  SELECT o.*, CASE WHEN o.product_id IS NULL THEN '[clave nula]'
    WHEN p.id IS NULL THEN '[sin correspondencia]'
    WHEN p.filas_clave > 1 THEN '[clave duplicada en products]'
    ELSE COALESCE(p.categoria, '[categoria nula]') END AS categoria_perfil
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS o LEFT JOIN productos_por_clave AS p ON o.product_id = p.id
),
pedidos_geografia AS (
  SELECT o.*, CASE WHEN o.user_id IS NULL THEN '[clave nula]'
    WHEN u.id IS NULL THEN '[sin correspondencia]'
    WHEN u.filas_clave > 1 THEN '[clave duplicada en users]'
    ELSE COALESCE(u.pais, '[pais nulo]') END AS pais_perfil,
    CASE WHEN o.user_id IS NULL THEN '[clave nula]'
    WHEN u.id IS NULL THEN '[sin correspondencia]'
    WHEN u.filas_clave > 1 THEN '[clave duplicada en users]'
    ELSE TO_JSON_STRING(STRUCT(u.pais AS pais, u.estado AS estado)) END AS estado_perfil
  FROM `bigquery-public-data.thelook_ecommerce.orders` AS o LEFT JOIN usuarios_por_clave AS u ON o.user_id = u.id
),
distribuciones AS (
SELECT 'products' AS tabla, 'category' AS dimension, CAST(COALESCE(category, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.products`
GROUP BY valor
UNION ALL
SELECT 'products' AS tabla, 'department' AS dimension, CAST(COALESCE(department, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.products`
GROUP BY valor
UNION ALL
SELECT 'inventory_items' AS tabla, 'product_category' AS dimension, CAST(COALESCE(product_category, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.inventory_items`
GROUP BY valor
UNION ALL
SELECT 'inventory_items' AS tabla, 'product_department' AS dimension, CAST(COALESCE(product_department, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.inventory_items`
GROUP BY valor
UNION ALL
SELECT 'inventory_items' AS tabla, 'sold_at_presente' AS dimension, CAST(IF(sold_at IS NULL, 'sin sold_at registrado', 'con sold_at registrado') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.inventory_items`
GROUP BY valor
UNION ALL
SELECT 'users' AS tabla, 'country' AS dimension, CAST(COALESCE(country, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.users`
GROUP BY valor
UNION ALL
SELECT 'users' AS tabla, 'country_state' AS dimension, CAST(TO_JSON_STRING(STRUCT(country AS pais, state AS estado)) AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.users`
GROUP BY valor
UNION ALL
SELECT 'orders' AS tabla, 'status' AS dimension, CAST(COALESCE(status, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT order_id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.orders`
GROUP BY valor
UNION ALL
SELECT 'orders' AS tabla, 'pais_perfil' AS dimension, CAST(pais_perfil AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT order_id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM pedidos_geografia
GROUP BY valor
UNION ALL
SELECT 'orders' AS tabla, 'estado_perfil' AS dimension, CAST(estado_perfil AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT order_id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM pedidos_geografia
GROUP BY valor
UNION ALL
SELECT 'order_items' AS tabla, 'status' AS dimension, CAST(COALESCE(status, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT order_id) AS claves_distintas_no_nulas, SUM(IF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price), sale_price, NULL)) AS importe_observado_finito, COUNTIF(sale_price IS NULL OR IS_NAN(sale_price) OR IS_INF(sale_price)) AS importes_no_utilizables
FROM lineas_categoria
GROUP BY valor
UNION ALL
SELECT 'order_items' AS tabla, 'categoria_perfil' AS dimension, CAST(COALESCE(categoria_perfil, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT order_id) AS claves_distintas_no_nulas, SUM(IF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price), sale_price, NULL)) AS importe_observado_finito, COUNTIF(sale_price IS NULL OR IS_NAN(sale_price) OR IS_INF(sale_price)) AS importes_no_utilizables
FROM lineas_categoria
GROUP BY valor
UNION ALL
SELECT 'order_items' AS tabla, 'status_fechas' AS dimension, CAST(TO_JSON_STRING(STRUCT(status AS estado, shipped_at IS NOT NULL AS con_envio, delivered_at IS NOT NULL AS con_entrega, returned_at IS NOT NULL AS con_devolucion)) AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT order_id) AS claves_distintas_no_nulas, SUM(IF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price), sale_price, NULL)) AS importe_observado_finito, COUNTIF(sale_price IS NULL OR IS_NAN(sale_price) OR IS_INF(sale_price)) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY valor
UNION ALL
SELECT 'events' AS tabla, 'event_type' AS dimension, CAST(COALESCE(event_type, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT session_id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.events`
GROUP BY valor
UNION ALL
SELECT 'events' AS tabla, 'traffic_source' AS dimension, CAST(COALESCE(traffic_source, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT session_id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.events`
GROUP BY valor
UNION ALL
SELECT 'events' AS tabla, 'browser' AS dimension, CAST(COALESCE(browser, '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT session_id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.events`
GROUP BY valor
UNION ALL
SELECT 'events' AS tabla, 'usuario_identificado' AS dimension, CAST(IF(user_id IS NULL, 'sin user_id', 'con user_id') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT session_id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.events`
GROUP BY valor
UNION ALL
SELECT 'products' AS tabla, 'distribution_center_id' AS dimension, CAST(COALESCE(CAST(distribution_center_id AS STRING), '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.products`
GROUP BY valor
UNION ALL
SELECT 'inventory_items' AS tabla, 'product_distribution_center_id' AS dimension, CAST(COALESCE(CAST(product_distribution_center_id AS STRING), '[nulo]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.inventory_items`
GROUP BY valor
UNION ALL
SELECT 'orders' AS tabla, 'mes_registro_UTC' AS dimension, CAST(COALESCE(FORMAT_TIMESTAMP('%Y-%m', created_at, 'UTC'), '[fecha nula]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT order_id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.orders`
GROUP BY valor
UNION ALL
SELECT 'order_items' AS tabla, 'mes_registro_UTC' AS dimension, CAST(COALESCE(FORMAT_TIMESTAMP('%Y-%m', created_at, 'UTC'), '[fecha nula]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT order_id) AS claves_distintas_no_nulas, SUM(IF(sale_price IS NOT NULL AND NOT IS_NAN(sale_price) AND NOT IS_INF(sale_price), sale_price, NULL)) AS importe_observado_finito, COUNTIF(sale_price IS NULL OR IS_NAN(sale_price) OR IS_INF(sale_price)) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY valor
UNION ALL
SELECT 'events' AS tabla, 'mes_registro_UTC' AS dimension, CAST(COALESCE(FORMAT_TIMESTAMP('%Y-%m', created_at, 'UTC'), '[fecha nula]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT session_id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.events`
GROUP BY valor
UNION ALL
SELECT 'inventory_items' AS tabla, 'mes_registro_UTC' AS dimension, CAST(COALESCE(FORMAT_TIMESTAMP('%Y-%m', created_at, 'UTC'), '[fecha nula]') AS STRING) AS valor, COUNT(*) AS filas, COUNT(DISTINCT id) AS claves_distintas_no_nulas, CAST(NULL AS FLOAT64) AS importe_observado_finito, CAST(NULL AS INT64) AS importes_no_utilizables
FROM `bigquery-public-data.thelook_ecommerce.inventory_items`
GROUP BY valor
)
SELECT * FROM distribuciones
ORDER BY tabla, dimension, valor;

-- BLOQUE 3. Exportar thelook_relaciones.csv
WITH
p0 AS (SELECT id AS clave, COUNT(*) AS multiplicidad FROM `bigquery-public-data.thelook_ecommerce.users` WHERE id IS NOT NULL GROUP BY id),
h0 AS (SELECT user_id AS clave, COUNT(*) AS filas FROM `bigquery-public-data.thelook_ecommerce.orders` WHERE user_id IS NOT NULL GROUP BY user_id),
r0 AS (SELECT 'orders.user_id -> users.id' AS relacion, [
STRUCT('filas_hijas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('fk_nulas' AS metrica, CAST(COUNTIF(c.user_id IS NULL) AS STRING) AS valor),
STRUCT('fk_no_nulas' AS metrica, CAST(COUNT(c.user_id) AS STRING) AS valor),
STRUCT('filas_hijas_sin_correspondencia' AS metrica, CAST(COUNTIF(c.user_id IS NOT NULL AND p.clave IS NULL) AS STRING) AS valor),
STRUCT('filas_hijas_con_correspondencia' AS metrica, CAST(COUNTIF(p.clave IS NOT NULL) AS STRING) AS valor),
STRUCT('claves_hijas_distintas_no_nulas' AS metrica, CAST(COUNT(DISTINCT c.user_id) AS STRING) AS valor),
STRUCT('filas_hijas_con_padre_duplicado' AS metrica, CAST(COUNTIF(p.multiplicidad > 1) AS STRING) AS valor),
STRUCT('max_multiplicidad_padre_en_match' AS metrica, CAST(COALESCE(MAX(p.multiplicidad), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_inner_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 0)), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_left_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 1)), 0) AS STRING) AS valor),
STRUCT('claves_padre_sin_hijas' AS metrica, CAST((SELECT COUNT(*) FROM p0 AS p LEFT JOIN h0 AS h ON p.clave=h.clave WHERE h.clave IS NULL) AS STRING) AS valor),
STRUCT('claves_padre_distintas' AS metrica, CAST((SELECT COUNT(*) FROM p0) AS STRING) AS valor),
STRUCT('claves_padre_duplicadas' AS metrica, CAST((SELECT COUNTIF(multiplicidad > 1) FROM p0) AS STRING) AS valor),
STRUCT('claves_hijas_con_varias_filas' AS metrica, CAST((SELECT COUNTIF(filas > 1) FROM h0) AS STRING) AS valor),
STRUCT('max_filas_hijas_por_clave' AS metrica, CAST((SELECT COALESCE(MAX(filas),0) FROM h0) AS STRING) AS valor),
STRUCT('importe_lineas_finitos' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('importe_estimado_left_join' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('inflacion_absoluta_potencial' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor)
] AS metricas FROM `bigquery-public-data.thelook_ecommerce.orders` AS c LEFT JOIN p0 AS p ON c.user_id=p.clave),
p1 AS (SELECT order_id AS clave, COUNT(*) AS multiplicidad FROM `bigquery-public-data.thelook_ecommerce.orders` WHERE order_id IS NOT NULL GROUP BY order_id),
h1 AS (SELECT order_id AS clave, COUNT(*) AS filas FROM `bigquery-public-data.thelook_ecommerce.order_items` WHERE order_id IS NOT NULL GROUP BY order_id),
r1 AS (SELECT 'order_items.order_id -> orders.order_id' AS relacion, [
STRUCT('filas_hijas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('fk_nulas' AS metrica, CAST(COUNTIF(c.order_id IS NULL) AS STRING) AS valor),
STRUCT('fk_no_nulas' AS metrica, CAST(COUNT(c.order_id) AS STRING) AS valor),
STRUCT('filas_hijas_sin_correspondencia' AS metrica, CAST(COUNTIF(c.order_id IS NOT NULL AND p.clave IS NULL) AS STRING) AS valor),
STRUCT('filas_hijas_con_correspondencia' AS metrica, CAST(COUNTIF(p.clave IS NOT NULL) AS STRING) AS valor),
STRUCT('claves_hijas_distintas_no_nulas' AS metrica, CAST(COUNT(DISTINCT c.order_id) AS STRING) AS valor),
STRUCT('filas_hijas_con_padre_duplicado' AS metrica, CAST(COUNTIF(p.multiplicidad > 1) AS STRING) AS valor),
STRUCT('max_multiplicidad_padre_en_match' AS metrica, CAST(COALESCE(MAX(p.multiplicidad), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_inner_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 0)), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_left_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 1)), 0) AS STRING) AS valor),
STRUCT('claves_padre_sin_hijas' AS metrica, CAST((SELECT COUNT(*) FROM p1 AS p LEFT JOIN h1 AS h ON p.clave=h.clave WHERE h.clave IS NULL) AS STRING) AS valor),
STRUCT('claves_padre_distintas' AS metrica, CAST((SELECT COUNT(*) FROM p1) AS STRING) AS valor),
STRUCT('claves_padre_duplicadas' AS metrica, CAST((SELECT COUNTIF(multiplicidad > 1) FROM p1) AS STRING) AS valor),
STRUCT('claves_hijas_con_varias_filas' AS metrica, CAST((SELECT COUNTIF(filas > 1) FROM h1) AS STRING) AS valor),
STRUCT('max_filas_hijas_por_clave' AS metrica, CAST((SELECT COALESCE(MAX(filas),0) FROM h1) AS STRING) AS valor),
STRUCT('importe_lineas_finitos' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), c.sale_price, NULL)) AS STRING) AS valor),
STRUCT('importe_estimado_left_join' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), c.sale_price * COALESCE(p.multiplicidad, 1), NULL)) AS STRING) AS valor),
STRUCT('inflacion_absoluta_potencial' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), ABS(c.sale_price) * GREATEST(COALESCE(p.multiplicidad, 1) - 1, 0), NULL)) AS STRING) AS valor)
] AS metricas FROM `bigquery-public-data.thelook_ecommerce.order_items` AS c LEFT JOIN p1 AS p ON c.order_id=p.clave),
h2 AS (SELECT user_id AS clave, COUNT(*) AS filas FROM `bigquery-public-data.thelook_ecommerce.order_items` WHERE user_id IS NOT NULL GROUP BY user_id),
r2 AS (SELECT 'order_items.user_id -> users.id' AS relacion, [
STRUCT('filas_hijas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('fk_nulas' AS metrica, CAST(COUNTIF(c.user_id IS NULL) AS STRING) AS valor),
STRUCT('fk_no_nulas' AS metrica, CAST(COUNT(c.user_id) AS STRING) AS valor),
STRUCT('filas_hijas_sin_correspondencia' AS metrica, CAST(COUNTIF(c.user_id IS NOT NULL AND p.clave IS NULL) AS STRING) AS valor),
STRUCT('filas_hijas_con_correspondencia' AS metrica, CAST(COUNTIF(p.clave IS NOT NULL) AS STRING) AS valor),
STRUCT('claves_hijas_distintas_no_nulas' AS metrica, CAST(COUNT(DISTINCT c.user_id) AS STRING) AS valor),
STRUCT('filas_hijas_con_padre_duplicado' AS metrica, CAST(COUNTIF(p.multiplicidad > 1) AS STRING) AS valor),
STRUCT('max_multiplicidad_padre_en_match' AS metrica, CAST(COALESCE(MAX(p.multiplicidad), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_inner_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 0)), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_left_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 1)), 0) AS STRING) AS valor),
STRUCT('claves_padre_sin_hijas' AS metrica, CAST((SELECT COUNT(*) FROM p0 AS p LEFT JOIN h2 AS h ON p.clave=h.clave WHERE h.clave IS NULL) AS STRING) AS valor),
STRUCT('claves_padre_distintas' AS metrica, CAST((SELECT COUNT(*) FROM p0) AS STRING) AS valor),
STRUCT('claves_padre_duplicadas' AS metrica, CAST((SELECT COUNTIF(multiplicidad > 1) FROM p0) AS STRING) AS valor),
STRUCT('claves_hijas_con_varias_filas' AS metrica, CAST((SELECT COUNTIF(filas > 1) FROM h2) AS STRING) AS valor),
STRUCT('max_filas_hijas_por_clave' AS metrica, CAST((SELECT COALESCE(MAX(filas),0) FROM h2) AS STRING) AS valor),
STRUCT('importe_lineas_finitos' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), c.sale_price, NULL)) AS STRING) AS valor),
STRUCT('importe_estimado_left_join' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), c.sale_price * COALESCE(p.multiplicidad, 1), NULL)) AS STRING) AS valor),
STRUCT('inflacion_absoluta_potencial' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), ABS(c.sale_price) * GREATEST(COALESCE(p.multiplicidad, 1) - 1, 0), NULL)) AS STRING) AS valor)
] AS metricas FROM `bigquery-public-data.thelook_ecommerce.order_items` AS c LEFT JOIN p0 AS p ON c.user_id=p.clave),
p3 AS (SELECT id AS clave, COUNT(*) AS multiplicidad FROM `bigquery-public-data.thelook_ecommerce.products` WHERE id IS NOT NULL GROUP BY id),
h3 AS (SELECT product_id AS clave, COUNT(*) AS filas FROM `bigquery-public-data.thelook_ecommerce.order_items` WHERE product_id IS NOT NULL GROUP BY product_id),
r3 AS (SELECT 'order_items.product_id -> products.id' AS relacion, [
STRUCT('filas_hijas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('fk_nulas' AS metrica, CAST(COUNTIF(c.product_id IS NULL) AS STRING) AS valor),
STRUCT('fk_no_nulas' AS metrica, CAST(COUNT(c.product_id) AS STRING) AS valor),
STRUCT('filas_hijas_sin_correspondencia' AS metrica, CAST(COUNTIF(c.product_id IS NOT NULL AND p.clave IS NULL) AS STRING) AS valor),
STRUCT('filas_hijas_con_correspondencia' AS metrica, CAST(COUNTIF(p.clave IS NOT NULL) AS STRING) AS valor),
STRUCT('claves_hijas_distintas_no_nulas' AS metrica, CAST(COUNT(DISTINCT c.product_id) AS STRING) AS valor),
STRUCT('filas_hijas_con_padre_duplicado' AS metrica, CAST(COUNTIF(p.multiplicidad > 1) AS STRING) AS valor),
STRUCT('max_multiplicidad_padre_en_match' AS metrica, CAST(COALESCE(MAX(p.multiplicidad), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_inner_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 0)), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_left_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 1)), 0) AS STRING) AS valor),
STRUCT('claves_padre_sin_hijas' AS metrica, CAST((SELECT COUNT(*) FROM p3 AS p LEFT JOIN h3 AS h ON p.clave=h.clave WHERE h.clave IS NULL) AS STRING) AS valor),
STRUCT('claves_padre_distintas' AS metrica, CAST((SELECT COUNT(*) FROM p3) AS STRING) AS valor),
STRUCT('claves_padre_duplicadas' AS metrica, CAST((SELECT COUNTIF(multiplicidad > 1) FROM p3) AS STRING) AS valor),
STRUCT('claves_hijas_con_varias_filas' AS metrica, CAST((SELECT COUNTIF(filas > 1) FROM h3) AS STRING) AS valor),
STRUCT('max_filas_hijas_por_clave' AS metrica, CAST((SELECT COALESCE(MAX(filas),0) FROM h3) AS STRING) AS valor),
STRUCT('importe_lineas_finitos' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), c.sale_price, NULL)) AS STRING) AS valor),
STRUCT('importe_estimado_left_join' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), c.sale_price * COALESCE(p.multiplicidad, 1), NULL)) AS STRING) AS valor),
STRUCT('inflacion_absoluta_potencial' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), ABS(c.sale_price) * GREATEST(COALESCE(p.multiplicidad, 1) - 1, 0), NULL)) AS STRING) AS valor)
] AS metricas FROM `bigquery-public-data.thelook_ecommerce.order_items` AS c LEFT JOIN p3 AS p ON c.product_id=p.clave),
p4 AS (SELECT id AS clave, COUNT(*) AS multiplicidad FROM `bigquery-public-data.thelook_ecommerce.inventory_items` WHERE id IS NOT NULL GROUP BY id),
h4 AS (SELECT inventory_item_id AS clave, COUNT(*) AS filas FROM `bigquery-public-data.thelook_ecommerce.order_items` WHERE inventory_item_id IS NOT NULL GROUP BY inventory_item_id),
r4 AS (SELECT 'order_items.inventory_item_id -> inventory_items.id' AS relacion, [
STRUCT('filas_hijas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('fk_nulas' AS metrica, CAST(COUNTIF(c.inventory_item_id IS NULL) AS STRING) AS valor),
STRUCT('fk_no_nulas' AS metrica, CAST(COUNT(c.inventory_item_id) AS STRING) AS valor),
STRUCT('filas_hijas_sin_correspondencia' AS metrica, CAST(COUNTIF(c.inventory_item_id IS NOT NULL AND p.clave IS NULL) AS STRING) AS valor),
STRUCT('filas_hijas_con_correspondencia' AS metrica, CAST(COUNTIF(p.clave IS NOT NULL) AS STRING) AS valor),
STRUCT('claves_hijas_distintas_no_nulas' AS metrica, CAST(COUNT(DISTINCT c.inventory_item_id) AS STRING) AS valor),
STRUCT('filas_hijas_con_padre_duplicado' AS metrica, CAST(COUNTIF(p.multiplicidad > 1) AS STRING) AS valor),
STRUCT('max_multiplicidad_padre_en_match' AS metrica, CAST(COALESCE(MAX(p.multiplicidad), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_inner_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 0)), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_left_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 1)), 0) AS STRING) AS valor),
STRUCT('claves_padre_sin_hijas' AS metrica, CAST((SELECT COUNT(*) FROM p4 AS p LEFT JOIN h4 AS h ON p.clave=h.clave WHERE h.clave IS NULL) AS STRING) AS valor),
STRUCT('claves_padre_distintas' AS metrica, CAST((SELECT COUNT(*) FROM p4) AS STRING) AS valor),
STRUCT('claves_padre_duplicadas' AS metrica, CAST((SELECT COUNTIF(multiplicidad > 1) FROM p4) AS STRING) AS valor),
STRUCT('claves_hijas_con_varias_filas' AS metrica, CAST((SELECT COUNTIF(filas > 1) FROM h4) AS STRING) AS valor),
STRUCT('max_filas_hijas_por_clave' AS metrica, CAST((SELECT COALESCE(MAX(filas),0) FROM h4) AS STRING) AS valor),
STRUCT('importe_lineas_finitos' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), c.sale_price, NULL)) AS STRING) AS valor),
STRUCT('importe_estimado_left_join' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), c.sale_price * COALESCE(p.multiplicidad, 1), NULL)) AS STRING) AS valor),
STRUCT('inflacion_absoluta_potencial' AS metrica, CAST(SUM(IF(c.sale_price IS NOT NULL AND NOT IS_NAN(c.sale_price) AND NOT IS_INF(c.sale_price), ABS(c.sale_price) * GREATEST(COALESCE(p.multiplicidad, 1) - 1, 0), NULL)) AS STRING) AS valor)
] AS metricas FROM `bigquery-public-data.thelook_ecommerce.order_items` AS c LEFT JOIN p4 AS p ON c.inventory_item_id=p.clave),
h5 AS (SELECT product_id AS clave, COUNT(*) AS filas FROM `bigquery-public-data.thelook_ecommerce.inventory_items` WHERE product_id IS NOT NULL GROUP BY product_id),
r5 AS (SELECT 'inventory_items.product_id -> products.id' AS relacion, [
STRUCT('filas_hijas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('fk_nulas' AS metrica, CAST(COUNTIF(c.product_id IS NULL) AS STRING) AS valor),
STRUCT('fk_no_nulas' AS metrica, CAST(COUNT(c.product_id) AS STRING) AS valor),
STRUCT('filas_hijas_sin_correspondencia' AS metrica, CAST(COUNTIF(c.product_id IS NOT NULL AND p.clave IS NULL) AS STRING) AS valor),
STRUCT('filas_hijas_con_correspondencia' AS metrica, CAST(COUNTIF(p.clave IS NOT NULL) AS STRING) AS valor),
STRUCT('claves_hijas_distintas_no_nulas' AS metrica, CAST(COUNT(DISTINCT c.product_id) AS STRING) AS valor),
STRUCT('filas_hijas_con_padre_duplicado' AS metrica, CAST(COUNTIF(p.multiplicidad > 1) AS STRING) AS valor),
STRUCT('max_multiplicidad_padre_en_match' AS metrica, CAST(COALESCE(MAX(p.multiplicidad), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_inner_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 0)), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_left_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 1)), 0) AS STRING) AS valor),
STRUCT('claves_padre_sin_hijas' AS metrica, CAST((SELECT COUNT(*) FROM p3 AS p LEFT JOIN h5 AS h ON p.clave=h.clave WHERE h.clave IS NULL) AS STRING) AS valor),
STRUCT('claves_padre_distintas' AS metrica, CAST((SELECT COUNT(*) FROM p3) AS STRING) AS valor),
STRUCT('claves_padre_duplicadas' AS metrica, CAST((SELECT COUNTIF(multiplicidad > 1) FROM p3) AS STRING) AS valor),
STRUCT('claves_hijas_con_varias_filas' AS metrica, CAST((SELECT COUNTIF(filas > 1) FROM h5) AS STRING) AS valor),
STRUCT('max_filas_hijas_por_clave' AS metrica, CAST((SELECT COALESCE(MAX(filas),0) FROM h5) AS STRING) AS valor),
STRUCT('importe_lineas_finitos' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('importe_estimado_left_join' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('inflacion_absoluta_potencial' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor)
] AS metricas FROM `bigquery-public-data.thelook_ecommerce.inventory_items` AS c LEFT JOIN p3 AS p ON c.product_id=p.clave),
p6 AS (SELECT id AS clave, COUNT(*) AS multiplicidad FROM `bigquery-public-data.thelook_ecommerce.distribution_centers` WHERE id IS NOT NULL GROUP BY id),
h6 AS (SELECT distribution_center_id AS clave, COUNT(*) AS filas FROM `bigquery-public-data.thelook_ecommerce.products` WHERE distribution_center_id IS NOT NULL GROUP BY distribution_center_id),
r6 AS (SELECT 'products.distribution_center_id -> distribution_centers.id' AS relacion, [
STRUCT('filas_hijas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('fk_nulas' AS metrica, CAST(COUNTIF(c.distribution_center_id IS NULL) AS STRING) AS valor),
STRUCT('fk_no_nulas' AS metrica, CAST(COUNT(c.distribution_center_id) AS STRING) AS valor),
STRUCT('filas_hijas_sin_correspondencia' AS metrica, CAST(COUNTIF(c.distribution_center_id IS NOT NULL AND p.clave IS NULL) AS STRING) AS valor),
STRUCT('filas_hijas_con_correspondencia' AS metrica, CAST(COUNTIF(p.clave IS NOT NULL) AS STRING) AS valor),
STRUCT('claves_hijas_distintas_no_nulas' AS metrica, CAST(COUNT(DISTINCT c.distribution_center_id) AS STRING) AS valor),
STRUCT('filas_hijas_con_padre_duplicado' AS metrica, CAST(COUNTIF(p.multiplicidad > 1) AS STRING) AS valor),
STRUCT('max_multiplicidad_padre_en_match' AS metrica, CAST(COALESCE(MAX(p.multiplicidad), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_inner_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 0)), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_left_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 1)), 0) AS STRING) AS valor),
STRUCT('claves_padre_sin_hijas' AS metrica, CAST((SELECT COUNT(*) FROM p6 AS p LEFT JOIN h6 AS h ON p.clave=h.clave WHERE h.clave IS NULL) AS STRING) AS valor),
STRUCT('claves_padre_distintas' AS metrica, CAST((SELECT COUNT(*) FROM p6) AS STRING) AS valor),
STRUCT('claves_padre_duplicadas' AS metrica, CAST((SELECT COUNTIF(multiplicidad > 1) FROM p6) AS STRING) AS valor),
STRUCT('claves_hijas_con_varias_filas' AS metrica, CAST((SELECT COUNTIF(filas > 1) FROM h6) AS STRING) AS valor),
STRUCT('max_filas_hijas_por_clave' AS metrica, CAST((SELECT COALESCE(MAX(filas),0) FROM h6) AS STRING) AS valor),
STRUCT('importe_lineas_finitos' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('importe_estimado_left_join' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('inflacion_absoluta_potencial' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor)
] AS metricas FROM `bigquery-public-data.thelook_ecommerce.products` AS c LEFT JOIN p6 AS p ON c.distribution_center_id=p.clave),
h7 AS (SELECT product_distribution_center_id AS clave, COUNT(*) AS filas FROM `bigquery-public-data.thelook_ecommerce.inventory_items` WHERE product_distribution_center_id IS NOT NULL GROUP BY product_distribution_center_id),
r7 AS (SELECT 'inventory_items.product_distribution_center_id -> distribution_centers.id' AS relacion, [
STRUCT('filas_hijas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('fk_nulas' AS metrica, CAST(COUNTIF(c.product_distribution_center_id IS NULL) AS STRING) AS valor),
STRUCT('fk_no_nulas' AS metrica, CAST(COUNT(c.product_distribution_center_id) AS STRING) AS valor),
STRUCT('filas_hijas_sin_correspondencia' AS metrica, CAST(COUNTIF(c.product_distribution_center_id IS NOT NULL AND p.clave IS NULL) AS STRING) AS valor),
STRUCT('filas_hijas_con_correspondencia' AS metrica, CAST(COUNTIF(p.clave IS NOT NULL) AS STRING) AS valor),
STRUCT('claves_hijas_distintas_no_nulas' AS metrica, CAST(COUNT(DISTINCT c.product_distribution_center_id) AS STRING) AS valor),
STRUCT('filas_hijas_con_padre_duplicado' AS metrica, CAST(COUNTIF(p.multiplicidad > 1) AS STRING) AS valor),
STRUCT('max_multiplicidad_padre_en_match' AS metrica, CAST(COALESCE(MAX(p.multiplicidad), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_inner_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 0)), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_left_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 1)), 0) AS STRING) AS valor),
STRUCT('claves_padre_sin_hijas' AS metrica, CAST((SELECT COUNT(*) FROM p6 AS p LEFT JOIN h7 AS h ON p.clave=h.clave WHERE h.clave IS NULL) AS STRING) AS valor),
STRUCT('claves_padre_distintas' AS metrica, CAST((SELECT COUNT(*) FROM p6) AS STRING) AS valor),
STRUCT('claves_padre_duplicadas' AS metrica, CAST((SELECT COUNTIF(multiplicidad > 1) FROM p6) AS STRING) AS valor),
STRUCT('claves_hijas_con_varias_filas' AS metrica, CAST((SELECT COUNTIF(filas > 1) FROM h7) AS STRING) AS valor),
STRUCT('max_filas_hijas_por_clave' AS metrica, CAST((SELECT COALESCE(MAX(filas),0) FROM h7) AS STRING) AS valor),
STRUCT('importe_lineas_finitos' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('importe_estimado_left_join' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('inflacion_absoluta_potencial' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor)
] AS metricas FROM `bigquery-public-data.thelook_ecommerce.inventory_items` AS c LEFT JOIN p6 AS p ON c.product_distribution_center_id=p.clave),
h8 AS (SELECT user_id AS clave, COUNT(*) AS filas FROM `bigquery-public-data.thelook_ecommerce.events` WHERE user_id IS NOT NULL GROUP BY user_id),
r8 AS (SELECT 'events.user_id -> users.id' AS relacion, [
STRUCT('filas_hijas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('fk_nulas' AS metrica, CAST(COUNTIF(c.user_id IS NULL) AS STRING) AS valor),
STRUCT('fk_no_nulas' AS metrica, CAST(COUNT(c.user_id) AS STRING) AS valor),
STRUCT('filas_hijas_sin_correspondencia' AS metrica, CAST(COUNTIF(c.user_id IS NOT NULL AND p.clave IS NULL) AS STRING) AS valor),
STRUCT('filas_hijas_con_correspondencia' AS metrica, CAST(COUNTIF(p.clave IS NOT NULL) AS STRING) AS valor),
STRUCT('claves_hijas_distintas_no_nulas' AS metrica, CAST(COUNT(DISTINCT c.user_id) AS STRING) AS valor),
STRUCT('filas_hijas_con_padre_duplicado' AS metrica, CAST(COUNTIF(p.multiplicidad > 1) AS STRING) AS valor),
STRUCT('max_multiplicidad_padre_en_match' AS metrica, CAST(COALESCE(MAX(p.multiplicidad), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_inner_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 0)), 0) AS STRING) AS valor),
STRUCT('filas_estimadas_left_join' AS metrica, CAST(COALESCE(SUM(COALESCE(p.multiplicidad, 1)), 0) AS STRING) AS valor),
STRUCT('claves_padre_sin_hijas' AS metrica, CAST((SELECT COUNT(*) FROM p0 AS p LEFT JOIN h8 AS h ON p.clave=h.clave WHERE h.clave IS NULL) AS STRING) AS valor),
STRUCT('claves_padre_distintas' AS metrica, CAST((SELECT COUNT(*) FROM p0) AS STRING) AS valor),
STRUCT('claves_padre_duplicadas' AS metrica, CAST((SELECT COUNTIF(multiplicidad > 1) FROM p0) AS STRING) AS valor),
STRUCT('claves_hijas_con_varias_filas' AS metrica, CAST((SELECT COUNTIF(filas > 1) FROM h8) AS STRING) AS valor),
STRUCT('max_filas_hijas_por_clave' AS metrica, CAST((SELECT COALESCE(MAX(filas),0) FROM h8) AS STRING) AS valor),
STRUCT('importe_lineas_finitos' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('importe_estimado_left_join' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor),
STRUCT('inflacion_absoluta_potencial' AS metrica, CAST(CAST(NULL AS FLOAT64) AS STRING) AS valor)
] AS metricas FROM `bigquery-public-data.thelook_ecommerce.events` AS c LEFT JOIN p0 AS p ON c.user_id=p.clave),
pedido_unico AS (SELECT order_id, COUNT(*) AS n, ANY_VALUE(user_id) AS user_id, ANY_VALUE(num_of_item) AS declarados FROM `bigquery-public-data.thelook_ecommerce.orders` WHERE order_id IS NOT NULL GROUP BY order_id),
lineas_por_pedido AS (SELECT order_id, COUNT(*) AS lineas FROM `bigquery-public-data.thelook_ecommerce.order_items` WHERE order_id IS NOT NULL GROUP BY order_id),
inventario_unico AS (SELECT id, COUNT(*) AS n, ANY_VALUE(product_id) AS product_id, ANY_VALUE(sold_at) AS sold_at FROM `bigquery-public-data.thelook_ecommerce.inventory_items` WHERE id IS NOT NULL GROUP BY id),
sesiones AS (SELECT session_id, COUNT(*) AS eventos, COUNT(DISTINCT user_id) AS usuarios, COUNTIF(user_id IS NULL) AS anonimos, COUNT(sequence_number) - COUNT(DISTINCT sequence_number) AS secuencias_repetidas FROM `bigquery-public-data.thelook_ecommerce.events` WHERE session_id IS NOT NULL GROUP BY session_id),
extra31 AS (SELECT 'orders.num_of_item vs lineas observadas' AS relacion, [STRUCT('pedidos_unicos_con_cantidad_declarada' AS metrica, CAST(COUNTIF(p.n=1 AND p.declarados IS NOT NULL) AS STRING) AS valor),
STRUCT('pedidos_comparables' AS metrica, CAST(COUNTIF(p.n=1 AND p.declarados IS NOT NULL AND h.order_id IS NOT NULL) AS STRING) AS valor),
STRUCT('diferencias_en_comparables' AS metrica, CAST(COUNTIF(p.n=1 AND p.declarados IS NOT NULL AND h.order_id IS NOT NULL AND p.declarados != h.lineas) AS STRING) AS valor),
STRUCT('pedidos_unicos_sin_lineas' AS metrica, CAST(COUNTIF(p.n=1 AND h.order_id IS NULL) AS STRING) AS valor)] AS metricas FROM pedido_unico p LEFT JOIN lineas_por_pedido h ON p.order_id=h.order_id),
extra32 AS (SELECT 'order_items.user_id vs orders.user_id' AS relacion, [STRUCT('lineas_con_pedido_unico_y_usuarios_presentes' AS metrica, CAST(COUNTIF(p.n=1 AND p.user_id IS NOT NULL AND c.user_id IS NOT NULL) AS STRING) AS valor),
STRUCT('usuarios_distintos' AS metrica, CAST(COUNTIF(p.n=1 AND p.user_id IS NOT NULL AND c.user_id IS NOT NULL AND p.user_id != c.user_id) AS STRING) AS valor)] AS metricas FROM `bigquery-public-data.thelook_ecommerce.order_items` c LEFT JOIN pedido_unico p ON c.order_id=p.order_id),
extra33 AS (SELECT 'order_items.product_id vs inventory_items.product_id' AS relacion, [STRUCT('lineas_con_unidad_unica_y_productos_presentes' AS metrica, CAST(COUNTIF(p.n=1 AND p.product_id IS NOT NULL AND c.product_id IS NOT NULL) AS STRING) AS valor),
STRUCT('productos_distintos' AS metrica, CAST(COUNTIF(p.n=1 AND p.product_id IS NOT NULL AND c.product_id IS NOT NULL AND p.product_id != c.product_id) AS STRING) AS valor),
STRUCT('lineas_con_unidad_unica_sin_sold_at' AS metrica, CAST(COUNTIF(p.n=1 AND p.sold_at IS NULL) AS STRING) AS valor),
STRUCT('lineas_con_unidad_unica' AS metrica, CAST(COUNTIF(p.n=1) AS STRING) AS valor)] AS metricas FROM `bigquery-public-data.thelook_ecommerce.order_items` c LEFT JOIN inventario_unico p ON c.inventory_item_id=p.id),
extra34 AS (SELECT 'events.session_id y sequence_number' AS relacion, [STRUCT('sesiones_no_nulas' AS metrica, CAST(COUNT(*) AS STRING) AS valor),
STRUCT('sesiones_con_varios_usuarios' AS metrica, CAST(COUNTIF(usuarios>1) AS STRING) AS valor),
STRUCT('sesiones_mixtas_anonimas_identificadas' AS metrica, CAST(COUNTIF(usuarios>0 AND anonimos>0) AS STRING) AS valor),
STRUCT('sesiones_con_secuencias_repetidas' AS metrica, CAST(COUNTIF(secuencias_repetidas>0) AS STRING) AS valor),
STRUCT('max_eventos_por_sesion' AS metrica, CAST(COALESCE(MAX(eventos),0) AS STRING) AS valor)] AS metricas FROM sesiones)
SELECT relacion, m.metrica, m.valor FROM r0, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM r1, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM r2, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM r3, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM r4, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM r5, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM r6, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM r7, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM r8, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM extra31, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM extra32, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM extra33, UNNEST(metricas) AS m
UNION ALL
SELECT relacion, m.metrica, m.valor FROM extra34, UNNEST(metricas) AS m
ORDER BY relacion, metrica;
