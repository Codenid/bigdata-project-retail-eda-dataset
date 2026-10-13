"""Diagnóstico estructural e informes comunes; no transforma fuentes originales."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def es(value, decimals=0):
    return f'{value:,.{decimals}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def analizar_olist(frames):
    orders = frames['orders']
    counts = [frames[name].groupby('order_id').size().reindex(orders.order_id, fill_value=0)
              for name in ('order_items', 'order_payments', 'order_reviews')]
    rows = []
    for name, count in zip(('order_items', 'order_payments', 'order_reviews'), counts):
        rows.append(dict(tabla=name, pedidos=len(count), sin_detalle=int(count.eq(0).sum()),
                         con_varios=int(count.gt(1).sum()), max_registros=int(count.max())))
    pd.DataFrame(rows).to_csv(ROOT/'edas/olist/reports/tables/granularidad.csv', index=False)
    # Tamaño exacto de un LEFT JOIN de los tres detalles; no materializa el cruce.
    multiplicity = counts[0].clip(lower=1) * counts[1].clip(lower=1) * counts[2].clip(lower=1)
    customers = frames['customers']
    geo = frames['geolocation']
    return dict(pedidos=len(orders), filas_union_detalles=int(multiplicity.sum()),
                clientes_unicos=customers.customer_unique_id.nunique(),
                identidades_varios_registros=int(customers.groupby('customer_unique_id').size().gt(1).sum()),
                prefijos_geo=geo.geolocation_zip_code_prefix.nunique(),
                prefijos_geo_varios=int(geo.groupby('geolocation_zip_code_prefix').size().gt(1).sum()),
                granularidad=rows)


def analizar_retail(df):
    fields = ['CustomerID', 'Country', 'InvoiceDate']
    grouped = df.groupby('InvoiceNo', dropna=False)[fields].nunique(dropna=False)
    rows = [dict(determinante='InvoiceNo', atributo=field, grupos=len(grouped),
                 grupos_multivalor=int(grouped[field].gt(1).sum())) for field in fields]
    product = df.groupby('StockCode', dropna=False)[['Description', 'UnitPrice']].nunique(dropna=False)
    rows += [dict(determinante='StockCode', atributo=field, grupos=len(product),
                  grupos_multivalor=int(product[field].gt(1).sum())) for field in product]
    pd.DataFrame(rows).to_csv(ROOT/'edas/online_retail/reports/tables/dependencias.csv', index=False)
    return dict(repeticiones_factura_producto=int(df.duplicated(['InvoiceNo', 'StockCode']).sum()),
                dependencias=rows)


def guardar(dataset, values):
    (ROOT/f'edas/{dataset}/reports/estructura.json').write_text(
        json.dumps(values, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


DESCRIPTIONS = {
    'olist': ('Olist', 'Marketplace brasileño: compras, artículos de distintos vendedores, pagos, entrega y reseñas. Permite estudiar el servicio logístico y su asociación con la satisfacción.', [
        ('orders', 'Pedido', 'order_id', 'Estado y ciclo de compra/entrega'),
        ('customers', 'Registro de cliente por pedido', 'customer_id', 'customer_unique_id identifica recurrencia; ubicación'),
        ('order_items', 'Artículo dentro de un pedido', 'order_id + order_item_id', 'Producto, vendedor, precio y flete'),
        ('order_payments', 'Registro de pago', 'order_id + payment_sequential', 'Medio, cuotas e importe'),
        ('order_reviews', 'Registro de reseña', 'review_id no es único', 'Puntuación y comentarios opcionales'),
        ('products', 'Producto', 'product_id', 'Categoría y atributos físicos'),
        ('sellers', 'Vendedor', 'seller_id', 'Ubicación del vendedor'),
        ('geolocation', 'Observación de un prefijo postal', 'Sin clave por prefijo', 'Coordenadas y localidad; múltiples observaciones'),
        ('product_category_name_translation', 'Traducción de categoría', 'product_category_name', 'Correspondencia portugués–inglés')]),
    'online_retail': ('Online Retail', 'Transacciones de un comercio británico: líneas de facturas con productos o cargos, cantidades, precios y cliente cuando está identificado. Permite estudiar concentración y recurrencia comercial.', [
        ('Online Retail', 'Línea del Excel', 'Sin identificador único de línea', 'InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID y Country')]),
    'the_look': ('The Look', 'Modelo de comercio electrónico que conecta usuarios, pedidos, catálogo, unidades de inventario y navegación. En este proyecto solo se dispone de perfiles y distribuciones agregados, no de las siete tablas individuales.', [
        ('users', 'Usuario', 'id', 'Perfil y ubicación'),
        ('orders', 'Pedido', 'order_id', 'Usuario, estado, fechas y número de artículos'),
        ('order_items', 'Línea de pedido', 'id', 'Pedido, usuario, producto, unidad, estado y sale_price'),
        ('products', 'Producto', 'id', 'Categoría, departamento, costo y precio de catálogo'),
        ('inventory_items', 'Unidad de inventario', 'id', 'Producto, centro, costo y fechas'),
        ('events', 'Evento de navegación', 'id', 'Usuario opcional, sesión, secuencia y tipo'),
        ('distribution_centers', 'Centro de distribución', 'id', 'Nombre y ubicación')]),
}


def modelo(dataset, compacto=False):
    path = ROOT/f'docs/diagramas/{dataset}.md'
    content = path.read_text()
    blocks = content.split('```mermaid')[1:]
    diagrams = [block.split('```')[0] for block in blocks]
    if compacto:
        diagrams = [diagram for diagram in diagrams if '--' in diagram or '..' in diagram]
        diagrams = ['\n' + '\n'.join(line for line in diagram.splitlines() if line.strip() == 'erDiagram' or '--' in line or '..' in line) + '\n' for diagram in diagrams]
    return '\n\n'.join('```mermaid'+diagram+'```' for diagram in diagrams)


def estructura(dataset):
    if dataset == 'the_look':
        return '''El esquema separa entidades y hechos, pero conserva redundancias: user_id está en pedido y línea; inventario replica atributos de producto y centro. Pueden representar una instantánea histórica, hipótesis que debe confirmarse antes de reemplazarlos por atributos actuales del catálogo. No se certifica una forma normal solo por tener claves únicas.

Los agregados indican claves únicas y no nulas en siete tablas y cobertura total en nueve enlaces no nulos. También indican concordancia de usuario pedido–línea y producto línea–unidad. No disponemos de filas para reconstruir esos cruces o normalizar físicamente el modelo. Los tres CSV locales son perfiles, distribuciones y relaciones; sus filas son métricas agregadas, no compradores ni pedidos.

Para una futura base analítica: una tabla de pedidos y otra de líneas, dimensiones de usuario/producto/centro y un hecho separado de eventos. Agregar líneas por pedido antes de unir; mantener eventos por sesión. El enlace por usuario entre eventos y pedidos es N:M y no demuestra atribución.'''
    s = json.loads((ROOT/f'edas/{dataset}/reports/estructura.json').read_text())
    if dataset == 'olist':
        rows = '\n'.join(f"| {r['tabla']} | {es(r['sin_detalle'])} | {es(r['con_varios'])} | {es(r['max_registros'])} |" for r in s['granularidad'])
        return f'''Las entidades están separadas en tablas; el detalle comercial, los pagos y las reseñas son hechos distintos. Esta separación reduce repetición, pero no demuestra por sí sola tercera forma normal. customer_id identifica un registro por pedido: hay {es(s['clientes_unicos'])} identidades customer_unique_id y {es(s['identidades_varios_registros'])} aparecen en varios registros. La recurrencia debe usar esa segunda clave.

| Detalle | Pedidos sin registro | Pedidos con varios registros | Máximo por pedido |
| --- | ---: | ---: | ---: |
{rows}

Denominador: {es(s['pedidos'])} pedidos en cada fila. Un LEFT JOIN directo de artículos × pagos × reseñas produciría **{es(s['filas_union_detalles'])} filas**, en vez de {es(s['pedidos'])} pedidos; repetiría medidas. El análisis agrega cada detalle y valida uniones 1:1. Para categorías o vendedores se conserva una tabla de líneas separada y se cuentan pedidos distintos.

Geolocation contiene {es(s['prefijos_geo'])} prefijos; {es(s['prefijos_geo_varios'])} tienen varias observaciones. Antes del enlace postal se necesita una dimensión de una fila por prefijo y una regla explícita de selección de coordenadas. Las reseñas necesitan una clave técnica si se almacenan como registros; review_id no basta. No se ha creado esa normalización física.'''
    deps = {r['atributo']: r for r in s['dependencias']}
    return f'''El Excel es una tabla plana y repite datos de factura y producto. InvoiceNo + StockCode tiene **{es(s['repeticiones_factura_producto'])} repeticiones adicionales**: no es una clave de línea. Conservar una fila_origen técnica permitiría identificar cada registro sin borrar duplicados.

La comprobación de dependencias funcionales cuenta valores distintos, incluidos nulos, dentro de cada grupo. De {es(deps['InvoiceDate']['grupos'])} facturas, {es(deps['CustomerID']['grupos_multivalor'])} tienen varios valores de cliente, {es(deps['Country']['grupos_multivalor'])} varios países y {es(deps['InvoiceDate']['grupos_multivalor'])} varias fechas. De {es(deps['Description']['grupos'])} códigos, {es(deps['Description']['grupos_multivalor'])} tienen varias descripciones y {es(deps['UnitPrice']['grupos_multivalor'])} varios precios.

Se propone separar factura, línea, cliente conocido y producto/cargo, sin presentar esas entidades como tablas existentes. La fecha original, la descripción y el precio se conservan en la línea; no se elige silenciosamente un valor por producto o factura. Importe = Quantity × UnitPrice es una medida derivada. La ausencia de cliente se conserva y las cancelaciones no tienen vínculo verificable con su compra original.'''


DECISIONS = {
    'olist': '''| Decisión que puede apoyar | Base analítica | Condición / límite |
| --- | --- | --- |
| Priorizar revisión del servicio de entrega | Pedido: demora, reseña, flete y ubicación | Segmentar por mes, vendedor y categoría; asociación sin causalidad |
| Detectar diferencias de conciliación | Pedido: pagos frente a precio + flete | Revisar discrepancias antes de clasificarlas como error |
| Estudiar recurrencia | customer_unique_id y pedidos distintos | Ventana histórica; no sustituir por customer_id |

La siguiente propuesta con mayor respaldo es un tablero de cumplimiento y satisfacción con denominadores visibles. Una intervención sobre vendedores o rutas exige comprobar diferencias de composición; este EDA no demuestra su efecto.''',
    'online_retail': '''| Decisión que puede apoyar | Base analítica | Condición / límite |
| --- | --- | --- |
| Priorizar seguimiento comercial | Cliente conocido: frecuencia e importe | Cobertura parcial; no representa a clientes anónimos |
| Planificar revisión del mix y concentración | Línea y factura positiva, por país/mes | Incluye cargos; meses parciales y sin costos |
| Separar venta y ajustes | Línea clasificada por signo y prefijo C | No equivale a devoluciones emparejadas ni cobros |

La siguiente propuesta con mayor respaldo es segmentación descriptiva de clientes conocidos y un tablero de concentración. La concentración permite evaluar dependencia comercial; no justifica campañas ni predice abandono sin evaluación adicional.''',
    'the_look': '''| Decisión que puede apoyar | Base disponible | Condición / límite |
| --- | --- | --- |
| Describir demanda por estado, país y categoría | Distribuciones exportadas | No son ingresos netos ni destino confirmado |
| Diseñar un modelo analítico | Esquema y perfiles de relaciones | Obtener filas autorizadas para materializarlo |
| Priorizar correcciones de semántica | Alertas de fechas y unidad–línea | Confirmar fuente, extracción, moneda y estados |

La siguiente propuesta con mayor respaldo es aclarar el contrato de datos antes de un tablero de stock o logística. Los eventos permiten describir actividad agregada; un embudo de conversión necesita definición de sesión, secuencia y enlace de compra que estas exportaciones no resuelven.''',
}


def informe(dataset, original):
    title, description, entities = DESCRIPTIONS[dataset]
    sections = {}
    for part in original.split('\n## ')[1:]:
        heading, body = part.split('\n', 1)
        sections[heading] = body.strip()
    if dataset == 'the_look':
        findings = '\n\n'.join(sections[h] for h in ('Ventas y demanda observada', 'Inventario y logística', 'Eventos y relaciones'))
        conclusion, evidence = sections['Lectura final'].split('Evidencia:', 1)
        quality = conclusion.strip()
        evidence = 'Evidencia:'+evidence
    else:
        findings, quality, evidence = (sections[h] for h in ('Hallazgos principales', 'Calidad y límites', 'Evidencia'))
    if dataset == 'olist':
        sizes = pd.read_csv(ROOT/'edas/olist/reports/tables/dimensiones.csv').set_index('Tabla').Filas.to_dict()
    elif dataset == 'the_look':
        sizes = json.loads((ROOT/'edas/the_look/reports/metricas.json').read_text())['filas']
    else:
        sizes = {'Online Retail': json.loads((ROOT/'edas/online_retail/reports/metricas.json').read_text())['filas']}
    table = '| Tabla / entidad original | Filas | Una fila representa | Clave | Contenido y uso |\n| --- | ---: | --- | --- | --- |\n'
    table += '\n'.join(f'| {name} | {es(sizes[name])} | {grain} | {key} | {purpose} |' for name, grain, key, purpose in entities)
    if dataset != 'the_look':
        table_file = 'granularidad.csv' if dataset == 'olist' else 'dependencias.csv'
        evidence += f'\n\n[Diagnóstico estructural](estructura.json) · [Comprobaciones de granularidad o dependencias](tables/{table_file}).'
    return f'''# {title}: informe de datos y viabilidad analítica

## 1. Propósito y alcance

{description}

{sections['Alcance']}

## 2. Tablas, granularidad y relaciones

{table}

{modelo(dataset)}

Las conexiones se leen de la entidad padre al detalle: uno a muchos, salvo las excepciones descritas. PK indica clave candidata y FK campo de enlace; los archivos no imponen restricciones de base de datos. Los diagramas muestran campos esenciales. En Online Retail, el segundo modelo es una propuesta; en The Look, el esquema se describe mediante exportaciones agregadas.

## 3. Normalización y construcción analítica

{estructura(dataset)}

## 4. Hallazgos y denominadores

{findings}

## 5. Calidad y límites de interpretación

{quality}

## 6. Valor para el proyecto y siguiente decisión

{DECISIONS[dataset]}

## 7. Evidencia y trazabilidad

{evidence}
'''
