"""Genera el resumen de los tres EDAs independientes."""
from estructura import DESCRIPTIONS, DECISIONS, modelo, estructura
import csv
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def metric(dataset):
    return json.loads((ROOT/f'edas/{dataset}/reports/metricas.json').read_text())
def es(n,d=2):
    return f'{n:,.{d}f}'.replace(',','_').replace('.',',').replace('_','.')
o=metric('olist');u=metric('online_retail');t=metric('the_look')
with (ROOT/'edas/olist/reports/tables/resenas_demora.csv').open() as handle:
    scores={r['late']:float(r['puntuacion_media']) for r in csv.DictReader(handle)}
resumen = f'''# Comercio electrónico: informe ejecutivo

Tres EDAs independientes describen entrega y satisfacción, concentración comercial y calidad de datos operativos. Sus empresas, periodos y poblaciones difieren; los importes no se suman ni permiten comparar desempeño directamente.

## 1. Olist: entrega y satisfacción

Sobre **{es(o['total_orders'],0)} pedidos**, la entrega mediana es **{es(o['delivery_median'])} días**. De {es(o['delivered_complete'],0)} entregados con fechas completas, **{es(o['late_percent'])}%** llegó después de la estimación registrada.

La reseña media es **{es(scores['A tiempo'])}/5 a tiempo** y **{es(scores['Tarde'])}/5 tarde**, entre pedidos con reseña. La demora se asocia con menor puntuación, sin demostrar causalidad. Los meses parciales, faltantes y selección de entregados limitan la comparación. Los importes son BRL nominales.

[Informe Olist](edas/olist/reports/informe_eda.md). Fuente: Olist, Kaggle versión 2; CC BY-NC-SA 4.0.

## 2. Online Retail: concentración comercial

Las **{es(u['facturas_ventas'],0)} facturas de ventas positivas** suman **GBP {es(u['importe_ventas'])}**. Reino Unido reúne **{es(u['uk_porcentaje'])}%** de ese importe. El 10% superior de los {es(u['clientes_ventas'],0)} clientes identificados concentra **{es(u['top10_clientes_porcentaje'])}%** de las ventas identificadas.

Falta cliente en **{es(u['clientes_faltantes']/u['filas']*100)}%** de las líneas. Las cancelaciones y ajustes se distinguen de ventas positivas; no se emparejaron devoluciones con compras. La concentración es un hallazgo; no confirma margen ni estabilidad futura.

[Informe Online Retail](edas/online_retail/reports/informe_eda.md). Fuente: Daqing Chen, UCI (2015); CC BY 4.0.

## 3. The Look: estructura íntegra y fechas por aclarar

Las exportaciones de BigQuery reúnen **{es(t['filas']['orders'],0)} pedidos**, **{es(t['filas']['order_items'],0)} líneas** y **{es(t['filas']['events'],0)} eventos**. Las claves son únicas y los nueve enlaces comprobados cubren todas las referencias no nulas. Las líneas suman **{es(t['importe_lineas'])}**, pero solo **{es(t['importe_complete'])}** corresponde al estado Complete; la moneda y el reconocimiento de ingresos no están documentados.

**{es(t['envio_previo_lineas']/t['envio_comparable_lineas']*100)}%** de las líneas con creación y envío tiene el envío anterior a su creación. Además, todas las líneas enlazan unidades sin sold_at, aunque el inventario cuenta {es(t['inventario_sold_at_presente'],0)} unidades con esa fecha. Se requiere aclarar estas diferencias antes de interpretar stock o tiempos. El **{es(t['eventos_anonimos']/t['filas']['events']*100)}%** de eventos no tiene usuario; no se atribuye conversión a pedidos.

[Informe The Look](edas/the_look/reports/informe_eda.md). Fuente: CSV agregados aportados tras ejecutar BigQuery; origen exacto y licencia pendientes de confirmar.

Los tres análisis conservan extremos y faltantes, explicitan denominadores y distinguen hallazgos de hipótesis. [Organización y metodología](docs/metodologia.md).
'''

# Un documento autosuficiente para evaluar alcance, estructura y viabilidad.
intro = """# Comercio electrónico: informe ejecutivo técnico

El proyecto evalúa tres fuentes independientes para definir qué decisiones y productos analíticos pueden sostener. El resultado es un diagnóstico de estructura, calidad y viabilidad: conocer las tablas y sus unidades de análisis es necesario para calcular indicadores sin duplicar operaciones. Sus poblaciones, periodos y monedas difieren; no se cruzan clientes ni se suman importes.

| Fuente | Qué contiene | Cobertura | Prioridad propuesta |
| --- | --- | --- | --- |
| Olist | Marketplace: pedidos, vendedores, pagos y satisfacción; nueve CSV relacionados | 2016–2018; BRL; archivos individuales locales | Cumplimiento de entrega y satisfacción |
| Online Retail | Una tabla de líneas de facturas de un comercio británico | 2010-12-01 a 2011-12-09; GBP; Excel local | Concentración y recurrencia de clientes conocidos |
| The Look | Siete entidades de comercio, inventario y navegación descritas por tres CSV agregados | Pedidos de 2019-01-09 a 2026-10-12; moneda pendiente | Aclarar semántica antes de medir stock y logística |

Las prioridades siguientes son propuestas derivadas de los hallazgos, no intervenciones evaluadas. El análisis no estima efectos causales, beneficios ni ingresos auditados.
"""
parts = [intro]
for index, dataset in enumerate(('olist', 'online_retail', 'the_look'), 1):
    title, description, _ = DESCRIPTIONS[dataset]
    report = (ROOT/f'edas/{dataset}/reports/informe_eda.md').read_text()
    inventory = report.split('## 2. Tablas, granularidad y relaciones\n\n')[1].split('```mermaid')[0].strip()
    old = resumen.split(f'## {index}. ')[1].split('\n', 1)[1]
    old = old.split('\n## ')[0].strip()
    if index == 3:
        old = old.split('\nLos tres análisis')[0]
    parts.append(f"""## {index}. {title}

{description}

### Estructura y lectura de los datos

{inventory}

{modelo(dataset, compacto=True)}

PK indica clave candidata; FK, campo de enlace. En Online Retail el segundo diagrama es conceptual, todavía no materializado. The Look describe el esquema mediante agregados exportados; no se inspeccionaron sus registros individuales.

### Normalización y reglas para analizar

{estructura(dataset)}

### Resultados y límites decisivos

{old}

### Valor y siguiente decisión

{DECISIONS[dataset]}
""")
parts.append("""## Criterio para avanzar

Olist y Online Retail permiten construir bases analíticas a partir de sus registros locales, manteniendo detalles y agregados separados. The Look permite diseñar el modelo y describir distribuciones; las anomalías temporales y de inventario requieren aclaración antes de indicadores operativos. La integridad de claves no garantiza coherencia de negocio.

Cada informe mantiene la misma estructura: alcance, tablas y relaciones, normalización, hallazgos, calidad, valor y trazabilidad. El detalle de indicadores, gráficos, licencias y huellas permanece en los informes enlazados; la reproducción se documenta en [metodología](docs/metodologia.md).
""")
(ROOT/'README.md').write_text('\n\n'.join(parts), encoding='utf-8')
