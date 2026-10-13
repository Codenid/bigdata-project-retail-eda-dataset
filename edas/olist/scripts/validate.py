"""Comprueba artefactos reales, enlaces del informe y cifras básicas contra CSV."""
import json
from pathlib import Path
import re

import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = ROOT / 'reports/informe_eda.md'
    content = report.read_text(encoding='utf-8')
    links = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', content)
    local = [link for link in links if not link.startswith(('http://', 'https://'))]
    for link in local:
        path = report.parent / link
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f'Enlace inexistente o vacío: {link}')
    figures = list((ROOT / 'reports/figures').glob('*.png'))
    if len(figures) != 8:
        raise ValueError(f'Se esperaban ocho figuras; hay {len(figures)}.')
    for path in figures:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if image.width < 600 or image.height < 400:
                raise ValueError(f'Gráfico demasiado pequeño: {path.name}')
    inventory = pd.read_csv(ROOT / 'reports/tables/dimensiones.csv')
    if len(inventory) != 9:
        raise ValueError('El inventario debe cubrir las nueve tablas.')
    for row in inventory.to_dict('records'):
        filename = ('product_category_name_translation.csv' if row['Tabla'] == 'product_category_name_translation'
                    else f"olist_{row['Tabla']}_dataset.csv")
        source = pd.read_csv(ROOT / 'data/raw' / filename)
        actual = (len(source), len(source.columns), int(source.duplicated().sum()), int(source.isna().sum().sum()))
        expected = tuple(row[c] for c in ['Filas', 'Columnas', 'Duplicados completos', 'Celdas faltantes'])
        if actual != expected:
            raise ValueError(f'Inventario inconsistente: {filename}')
    metrics = json.loads((ROOT / 'reports/metricas.json').read_text())
    orders = pd.read_csv(ROOT / 'data/raw/olist_orders_dataset.csv')
    dates = orders[['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']].apply(pd.to_datetime)
    eligible = orders.order_status.eq('delivered') & dates.notna().all(axis=1)
    late = dates.order_delivered_customer_date > dates.order_estimated_delivery_date
    if metrics['total_orders'] != len(orders) or metrics['delivered_complete'] != int(eligible.sum()) or metrics['late_orders'] != int((eligible & late).sum()):
        raise ValueError('Métricas de pedidos inconsistentes con los CSV originales.')
    structure = json.loads((ROOT / 'reports/estructura.json').read_text())
    count_columns = []
    for name in ('order_items', 'order_payments', 'order_reviews'):
        detail = pd.read_csv(ROOT / f'data/raw/olist_{name}_dataset.csv', dtype={'order_id': 'string'})
        counts = orders[['order_id']].merge(detail.groupby('order_id').size().rename('n'),
                                           on='order_id', how='left', validate='one_to_one').n.fillna(0).astype(int)
        expected = next(row for row in structure['granularidad'] if row['tabla'] == name)
        assert expected['sin_detalle'] == int((counts == 0).sum())
        assert expected['con_varios'] == int((counts > 1).sum())
        assert expected['max_registros'] == int(counts.max())
        count_columns.append(counts.clip(lower=1))
    assert structure['filas_union_detalles'] == int(pd.concat(count_columns, axis=1).prod(axis=1).sum())
    customers = pd.read_csv(ROOT/'data/raw/olist_customers_dataset.csv', dtype='string')
    assert structure['clientes_unicos'] == customers.customer_unique_id.nunique()
    assert structure['identidades_varios_registros'] == int(customers.customer_unique_id.value_counts().gt(1).sum())
    geo = pd.read_csv(ROOT/'data/raw/olist_geolocation_dataset.csv', dtype={'geolocation_zip_code_prefix': 'string'})
    assert structure['prefijos_geo'] == geo.geolocation_zip_code_prefix.nunique()
    assert structure['prefijos_geo_varios'] == int(geo.geolocation_zip_code_prefix.value_counts().gt(1).sum())
    print(f'OK: {len(local)} enlaces locales, 8 PNG decodificables, 9 tablas contrastadas y métricas de pedidos recalculadas.')


if __name__ == '__main__':
    main()
