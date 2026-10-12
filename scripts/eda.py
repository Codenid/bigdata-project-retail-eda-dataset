"""EDA completo de las nueve tablas de Olist; no modifica datos originales."""
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports'
TABLES = OUT / 'tables'
FIGURES = OUT / 'figures'


def markdown(frame):
    """Tabla Markdown sin dependencia adicional tabulate."""
    def clean(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    return '\n'.join(['| ' + ' | '.join(map(clean, frame.columns)) + ' |',
                      '| ' + ' | '.join(['---'] * len(frame.columns)) + ' |'] +
                     ['| ' + ' | '.join(map(clean, row)) + ' |'
                      for row in frame.itertuples(index=False, name=None)])


def save(name, title, xlabel, ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(FIGURES / name, dpi=150)
    plt.close()


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    frames = {}
    profiles, summary, numeric = [], [], []
    for path in sorted((ROOT / 'data/raw').glob('*.csv')):
        name = path.stem.replace('olist_', '').replace('_dataset', '')
        header = pd.read_csv(path, nrows=0).columns
        # IDs y prefijos postales son etiquetas, no magnitudes numéricas.
        labels = {c: 'string' for c in header if c.endswith('_id') or 'zip_code_prefix' in c}
        df = pd.read_csv(path, dtype=labels)
        frames[name] = df
        summary.append([name, len(df), len(df.columns), int(df.duplicated().sum()),
                        int(df.isna().sum().sum())])
        for column in df:
            series = df[column]
            profiles.append([name, column, str(series.dtype), int(series.isna().sum()),
                             round(series.isna().mean() * 100, 3), series.nunique()])
        for column in df.select_dtypes('number'):
            s = df[column].dropna()
            q1, q3 = s.quantile([.25, .75])
            iqr = q3 - q1
            extremes = (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)
            numeric.append([name, column, s.size, s.min(), q1, s.median(), s.mean(),
                            q3, s.quantile(.95), s.quantile(.99), s.max(), s.std(),
                            int(extremes.sum())])
    if len(frames) != 9:
        raise ValueError('Se requieren los nueve CSV: ejecuta scripts/download.py primero.')
    overview = pd.DataFrame(summary, columns=['Tabla', 'Filas', 'Columnas', 'Duplicados completos', 'Celdas faltantes'])
    profile = pd.DataFrame(profiles, columns=['Tabla', 'Columna', 'Tipo', 'Faltantes', 'Faltantes (%)', 'Valores distintos'])
    stats = pd.DataFrame(numeric, columns=['Tabla', 'Columna', 'N', 'Mínimo', 'Q1', 'Mediana', 'Media', 'Q3', 'P95', 'P99', 'Máximo', 'DE', 'Extremos IQR'])
    overview.to_csv(TABLES / 'dimensiones.csv', index=False)
    profile.to_csv(TABLES / 'columnas_calidad.csv', index=False)
    stats.to_csv(TABLES / 'estadisticas_numericas.csv', index=False)

    keys = {'orders': ['order_id'], 'customers': ['customer_id'], 'products': ['product_id'],
            'sellers': ['seller_id'], 'order_items': ['order_id', 'order_item_id'],
            'order_payments': ['order_id', 'payment_sequential'],
            'order_reviews': ['review_id'],
            'product_category_name_translation': ['product_category_name']}
    key_rows = []
    for name, columns in keys.items():
        df = frames[name]
        key_rows.append([name, ', '.join(columns), int(df.duplicated(columns).sum()),
                         int(df[columns].isna().any(axis=1).sum())])
    key_table = pd.DataFrame(key_rows, columns=['Tabla', 'Clave candidata', 'Repeticiones adicionales', 'Filas con clave nula'])
    key_table.to_csv(TABLES / 'claves.csv', index=False)
    relations = [('orders', 'customer_id', 'customers', 'customer_id'),
                 ('order_items', 'order_id', 'orders', 'order_id'),
                 ('order_items', 'product_id', 'products', 'product_id'),
                 ('order_items', 'seller_id', 'sellers', 'seller_id'),
                 ('order_payments', 'order_id', 'orders', 'order_id'),
                 ('order_reviews', 'order_id', 'orders', 'order_id'),
                 ('products', 'product_category_name', 'product_category_name_translation', 'product_category_name')]
    integrity = []
    for child, ck, parent, pk in relations:
        s = frames[child][ck]
        integrity.append([child, ck, parent, int((s.notna() & ~s.isin(frames[parent][pk])).sum()), int(s.isna().sum())])
    integrity = pd.DataFrame(integrity, columns=['Tabla', 'Columna', 'Referencia', 'Filas sin referencia', 'Claves nulas'])
    integrity.to_csv(TABLES / 'integridad_referencial.csv', index=False)

    orders = frames['orders'].copy()
    invalid_dates = []
    for name, df in frames.items():
        for col in df:
            if 'timestamp' in col or col.endswith(('_date', '_at')):
                parsed = pd.to_datetime(df[col], errors='coerce')
                invalid_dates.append([name, col, int((df[col].notna() & parsed.isna()).sum())])
                if name == 'orders':
                    orders[col] = parsed
    date_table = pd.DataFrame(invalid_dates, columns=['Tabla', 'Columna', 'Fechas no interpretables'])
    date_table.to_csv(TABLES / 'fechas.csv', index=False)
    items, payments, reviews = (frames[n] for n in ['order_items', 'order_payments', 'order_reviews'])
    amounts = items.groupby('order_id').agg(price=('price', 'sum'), freight_value=('freight_value', 'sum'), items=('order_item_id', 'size'))
    paid = payments.groupby('order_id').agg(payment_value=('payment_value', 'sum'))
    ratings = reviews.groupby('order_id').agg(review_score=('review_score', 'mean'), reviews=('review_score', 'size'))
    joined = orders.merge(amounts, on='order_id', how='left', validate='one_to_one').merge(
        paid, on='order_id', how='left', validate='one_to_one').merge(
        ratings, on='order_id', how='left', validate='one_to_one')
    assert len(joined) == len(orders), 'El cruce debe conservar exactamente un registro por pedido.'
    joined['delivery_days'] = (joined.order_delivered_customer_date - joined.order_purchase_timestamp).dt.total_seconds() / 86400
    joined['late_days'] = (joined.order_delivered_customer_date - joined.order_estimated_delivery_date).dt.total_seconds() / 86400
    delivered = joined[joined.order_status.eq('delivered') & joined.delivery_days.notna() & joined.late_days.notna()].copy()
    delivered['late'] = delivered.late_days > 0
    reviewed = delivered.dropna(subset=['review_score'])
    comparison = reviewed.groupby('late').agg(pedidos=('order_id', 'size'), puntuacion_media=('review_score', 'mean'), puntuacion_mediana=('review_score', 'median'))
    comparison.index = comparison.index.map({False: 'A tiempo', True: 'Tarde'})
    comparison.reset_index().to_csv(TABLES / 'resenas_demora.csv', index=False)
    corr = joined[['price', 'freight_value', 'items', 'payment_value', 'review_score', 'delivery_days', 'late_days']].corr(method='spearman')
    corr.to_csv(TABLES / 'correlaciones_spearman.csv')
    counts = joined[corr.columns].notna().astype(int)
    (counts.T @ counts).to_csv(TABLES / 'n_pares_correlacion.csv')

    plt.figure(figsize=(9, 5))
    missing = profile.nlargest(15, 'Faltantes (%)').copy()
    missing.index = missing['Tabla'] + '.' + missing['Columna']
    missing['Faltantes (%)'].sort_values().plot.barh()
    save('faltantes.png', '15 columnas con mayor proporción de faltantes', 'Faltantes (%)', '')
    plt.figure(figsize=(9, 4))
    orders.groupby(orders.order_purchase_timestamp.dt.to_period('M')).size().plot(marker='o')
    save('pedidos_mensuales.png', 'Pedidos por mes de compra (todos los estados)', 'Mes', 'Pedidos')
    plt.figure(figsize=(9, 4))
    orders.order_status.value_counts().plot.bar()
    save('estados_pedido.png', 'Estados de los pedidos', 'Estado', 'Pedidos')
    plt.figure(figsize=(9, 4))
    plt.hist(items.price, bins=80)
    plt.yscale('log')
    save('precios.png', 'Precio por artículo: rango completo; conteos logarítmicos', 'Precio (BRL)', 'Artículos (escala log)')
    plt.figure(figsize=(9, 4))
    plt.hist(delivered.delivery_days, bins=70)
    save('entrega.png', 'Tiempo hasta entrega: pedidos entregados con fechas completas', 'Días desde compra', 'Pedidos')
    plt.figure(figsize=(7, 4))
    reviews.review_score.value_counts().sort_index().plot.bar()
    save('resenas.png', 'Puntuaciones: una observación por registro de reseña', 'Puntuación', 'Reseñas')
    plt.figure(figsize=(7, 4))
    comparison.puntuacion_media.plot.bar()
    plt.ylim(0, 5)
    save('resenas_demora.png', 'Reseña media por puntualidad (agregada por pedido)', 'Entrega', 'Puntuación media')
    plt.figure(figsize=(8, 7))
    plt.imshow(corr, vmin=-1, vmax=1, cmap='coolwarm')
    plt.xticks(range(len(corr)), corr.columns, rotation=45, ha='right')
    plt.yticks(range(len(corr)), corr.index)
    for i in range(len(corr)):
        for j in range(len(corr)):
            plt.text(j, i, f'{corr.iloc[i, j]:.2f}', ha='center', va='center', fontsize=8)
    plt.colorbar(label='Spearman')
    save('correlaciones.png', 'Asociaciones por pedido; casos completos por par', '', '')

    geo = frames['geolocation']
    suspicious_geo = (~geo.geolocation_lat.between(-90, 90) | ~geo.geolocation_lng.between(-180, 180)).sum()
    negative_money = sum(int((df[c] < 0).sum()) for df, cols in [(items, ['price', 'freight_value']), (payments, ['payment_value'])] for c in cols)
    comparable = joined.dropna(subset=['price', 'freight_value', 'payment_value'])
    discrepancies = ((comparable.payment_value - comparable.price - comparable.freight_value).abs() > .05).sum()
    manifest = json.loads((ROOT / 'data/manifest.json').read_text())
    metrics = dict(total_orders=len(orders), delivered_complete=len(delivered), reviewed_delivered=len(reviewed),
                   late_orders=int(delivered.late.sum()), late_percent=float(delivered.late.mean() * 100),
                   delivery_median=float(delivered.delivery_days.median()), delivery_p95=float(delivered.delivery_days.quantile(.95)),
                   spearman_delivery_review=float(corr.loc['delivery_days', 'review_score']),
                   negative_delivery_days=int((joined.delivery_days < 0).sum()),
                   payment_discrepancies=int(discrepancies), payment_comparable=len(comparable))
    (OUT / 'metricas.json').write_text(json.dumps(metrics, indent=2) + '\n')
    text = f'''# Informe EDA: Brazilian E-Commerce Public Dataset by Olist

## Fuente, acceso y reproducción

Fuente: [Olist en Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), versión 2, nueve CSV. La documentación describe pedidos de 2016–2018 de distintos marketplaces. Descarga pública comprobada sin cuenta ni token. Licencia del dataset: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/): atribución, uso no comercial y compartir adaptaciones bajo la misma licencia. Olist es la fuente; este análisis no está afiliado a Olist.

ZIP observado: {manifest['compressed_bytes']:,} bytes ({manifest['compressed_bytes']/1e6:.2f} MB); CSV: {manifest['uncompressed_bytes']:,} bytes ({manifest['uncompressed_bytes']/1e6:.2f} MB). SHA-256: `{manifest['sha256']}`. URL exacta y lista de archivos en `data/manifest.json` (generado localmente). Python {platform.python_version()}, pandas {pd.__version__}, matplotlib {matplotlib.__version__}. Los scripts calculan todas las cifras; no hay muestreo aleatorio.

## Dimensiones, tipos y calidad

{markdown(overview)}

Total: {sum(len(df) for df in frames.values()):,} filas distribuidas en tablas de distinta granularidad, no observaciones independientes sumables para inferencia. Inventario completo de columnas, tipos, faltantes y cardinalidad: [columnas_calidad.csv](tables/columnas_calidad.csv). Los identificadores y prefijos postales se leen como texto para preservar ceros iniciales. Las fechas originales se perfilan como texto y luego se convierten explícitamente para el análisis temporal; fallos de conversión: {date_table['Fechas no interpretables'].sum():,}.

![Faltantes](figures/faltantes.png)

Los campos opcionales de título y comentario de reseña concentran faltantes; su ausencia no implica automáticamente un error. Las fechas de entrega dependen del estado del pedido. No se imputan faltantes ni se eliminan duplicados en los CSV originales.

{markdown(key_table)}

Una clave repetida no equivale a una fila completamente duplicada. Las reseñas pueden repetirse por identificador o por pedido: {reviews.order_id.duplicated().sum():,} filas adicionales comparten pedido. Se agregan las puntuaciones mediante su media por pedido. Geolocalización tiene {geo.geolocation_zip_code_prefix.nunique():,} prefijos para {len(geo):,} registros; no debe cruzarse por prefijo sin agregación previa. Coordenadas fuera de los límites físicos latitud/longitud: {suspicious_geo:,}; esta prueba no valida fronteras de Brasil ni exactitud geográfica.

{markdown(integrity)}

Las referencias se comprueban por fila, excluyendo claves nulas del conteo de referencias inexistentes. Detalles en [integridad_referencial.csv](tables/integridad_referencial.csv). Importes negativos de precio, flete o pago: {negative_money:,}; puntuaciones fuera de 1–5: {int((~reviews.review_score.between(1,5)).sum()):,}; duraciones de entrega negativas: {metrics['negative_delivery_days']:,}. Pagos con diferencia absoluta superior a BRL 0,05 respecto a precio más flete: {discrepancies:,} de {len(comparable):,} pedidos comparables. Es una discrepancia contable descriptiva, no prueba de fraude.

## Distribuciones y valores extremos

Compras observadas desde {orders.order_purchase_timestamp.min()} hasta {orders.order_purchase_timestamp.max()}. Los extremos temporales pueden contener meses parciales; los conteos no miden crecimiento comparable ni demanda de todo Brasil.

![Pedidos mensuales](figures/pedidos_mensuales.png)
![Estados](figures/estados_pedido.png)

Estadísticas de todas las columnas numéricas (N, media, desviación estándar, mediana, cuartiles, P95, P99 y extremos): [estadisticas_numericas.csv](tables/estadisticas_numericas.csv). Se señalan extremos fuera de Q1 − 1,5×IQR y Q3 + 1,5×IQR; no se borran ni se consideran errores por definición. En variables discretas o con IQR cero esta regla requiere cautela.

Precio por artículo: mediana BRL {items.price.median():.2f}, media BRL {items.price.mean():.2f}, P99 BRL {items.price.quantile(.99):.2f}, máximo BRL {items.price.max():.2f}. Flete mediano BRL {items.freight_value.median():.2f}. La escala de conteos logarítmica permite mostrar la cola completa sin recortar precios.

![Precios](figures/precios.png)

Entre {len(delivered):,} pedidos entregados con fechas de compra, entrega y estimación disponibles, la mediana de entrega es {metrics['delivery_median']:.2f} días y P95 {metrics['delivery_p95']:.2f} días. {metrics['late_orders']:,} ({metrics['late_percent']:.2f}%) se entregaron después de la fecha estimada. Se compara la hora exacta con la estimación registrada (a menudo medianoche); no se presupone una tolerancia adicional.

![Entrega](figures/entrega.png)
![Reseñas](figures/resenas.png)

## Relaciones entre variables

Artículos y pagos se suman por pedido; reseñas se promedian por pedido. Cruces validados uno a uno conservan {len(joined):,} pedidos. Los pedidos sin artículos, pagos o reseñas conservan faltantes, no ceros. Precio representa suma de precios de líneas; flete suma por línea; pagos son registros de pago, no beneficio ni ingresos netos.

{markdown(comparison.reset_index())}

![Reseñas y demora](figures/resenas_demora.png)
![Correlaciones](figures/correlaciones.png)

Hallazgo: correlación de Spearman entre duración de entrega y puntuación media del pedido = {metrics['spearman_delivery_review']:.3f}. Correlaciones calculadas con casos completos por par, sin asumir igualdad de muestras; tamaños en [n_pares_correlacion.csv](tables/n_pares_correlacion.csv), coeficientes en [correlaciones_spearman.csv](tables/correlaciones_spearman.csv). Las relaciones entre importe de artículos y pagos tienen un componente contable esperado.

Hipótesis: la experiencia de entrega podría estar relacionada con satisfacción. No se demuestra causalidad: categoría, vendedor, distancia, época y selección de quienes reseñan pueden influir en ambas variables. No se han estimado efectos causales, intervalos de confianza ni modelos predictivos.

## Limitaciones y decisiones

- Dataset histórico de una plataforma; no representa todo el comercio electrónico brasileño ni la situación actual.
- Un cliente por pedido (`customer_id`) no equivale a una persona distinta; `customer_unique_id` permite reconocer recurrencia, sin garantizar identidad real.
- Los faltantes de fechas y reseñas generan selección. Comparar puntualidad solo entre entregados con fechas completas excluye cancelaciones y pedidos en proceso.
- Múltiples reseñas se promedian sin escoger arbitrariamente una. La geolocalización se perfila, pero no se utiliza para estimar distancias o deducir domicilios.
- Las magnitudes monetarias se interpretan en BRL nominales; no se ajustan por inflación ni incluyen costos, impuestos o márgenes.
- Los extremos se conservan; su legitimidad requiere contexto externo. Los prefijos postales no son coordenadas únicas.
- El EDA describe asociaciones; no prueba significancia, representatividad ni causalidad.

## Artefactos y comprobaciones

Generados por `python scripts/eda.py`: ocho gráficos PNG, siete tablas de calidad/estadística más correlaciones y tamaños de pares, y [metricas.json](metricas.json). La descarga comprueba SHA-256, lista exacta de miembros y CRC del ZIP. Los cruces comprueban cardinalidad y conservación de pedidos. La comprobación independiente de archivos se ejecuta con `python scripts/validate.py`; sus resultados de la ejecución de referencia se registran en README.
'''
    (OUT / 'informe_eda.md').write_text(text, encoding='utf-8')
    print(f'Informe generado: {OUT / "informe_eda.md"}; {len(joined):,} pedidos.')


if __name__ == '__main__':
    main()
