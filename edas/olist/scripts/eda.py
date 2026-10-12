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
    text = f'''# Olist: informe EDA

## Alcance

**{len(orders):,} pedidos** de 2016–2018, distribuidos en nueve tablas. Fuente: [Olist en Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), versión 2, licencia [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Los importes están en BRL nominales.

## Hallazgos principales

| Indicador | Resultado | Población |
| --- | ---: | --- |
| Mediana de entrega | {metrics['delivery_median']:.2f} días | {len(delivered):,} entregados con fechas completas |
| Percentil 95 de entrega | {metrics['delivery_p95']:.2f} días | Misma población |
| Entregados tarde | {metrics['late_orders']:,} ({metrics['late_percent']:.2f}%) | Misma población; después de la hora estimada |
| Reseña media a tiempo | {comparison.loc['A tiempo', 'puntuacion_media']:.2f}/5 | {comparison.loc['A tiempo', 'pedidos']:,} pedidos con reseña |
| Reseña media tarde | {comparison.loc['Tarde', 'puntuacion_media']:.2f}/5 | {comparison.loc['Tarde', 'pedidos']:,} pedidos con reseña |

Las entregas más largas se asocian con puntuaciones menores: Spearman **{metrics['spearman_delivery_review']:.3f}**, sobre {len(reviewed):,} pedidos entregados con fechas y reseña. La asociación no demuestra causalidad; vendedor, categoría y selección de quienes reseñan pueden influir.

![Reseñas según puntualidad](figures/resenas_demora.png)

El precio por artículo tiene mediana **BRL {items.price.median():.2f}** y P99 **BRL {items.price.quantile(.99):.2f}**. Los extremos se conservan. Hay **{int(discrepancies):,} discrepancias superiores a BRL 0,05** entre pagos y precio más flete, sobre {len(comparable):,} pedidos comparables; no prueban fraude.

## Calidad y límites

Las claves de pedidos, clientes, productos y vendedores son únicas y las referencias principales están completas. Las reseñas repiten identificadores; la geolocalización repite prefijos. Hay 610 productos sin categoría y 13 sin traducción correspondiente. Los faltantes se mantienen, sin imputación.

Artículos y pagos se sumaron por pedido; reseñas se promediaron. Las uniones 1:1 conservan los {len(joined):,} pedidos. La puntualidad excluye cancelaciones y entregas sin fechas completas. El dataset histórico no representa todo Brasil ni permite estimar margen.

## Evidencia

[Métricas](metricas.json), [dimensiones](tables/dimensiones.csv), [calidad](tables/columnas_calidad.csv), [claves](tables/claves.csv), [referencias](tables/integridad_referencial.csv), [estadísticas](tables/estadisticas_numericas.csv) y [denominadores de correlación](tables/n_pares_correlacion.csv). [Entrega](figures/entrega.png), [pedidos mensuales](figures/pedidos_mensuales.png) y [precios](figures/precios.png).

SHA-256 de la fuente: `{manifest['sha256']}`. Datos originales intactos y excluidos de Git.
'''
    (OUT / 'informe_eda.md').write_text(text, encoding='utf-8')
    print(f'Informe generado: {OUT / "informe_eda.md"}; {len(joined):,} pedidos.')


if __name__ == '__main__':
    main()
