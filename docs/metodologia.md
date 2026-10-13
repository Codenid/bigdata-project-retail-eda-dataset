# Organización y metodología

Los tres análisis son independientes. `edas/olist/` contiene sus nueve tablas originales locales, scripts, informe, tablas y gráficos; `edas/online_retail/` contiene el Excel original local y sus propios artefactos. No se mezclan registros, monedas ni poblaciones. El README raíz presenta resultados ejecutivos; cada informe detalla definiciones, denominadores y limitaciones.

## Ejecución desde la raíz

Python 3.12. Las rutas de los scripts se resuelven respecto de su propio archivo.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt
python edas/olist/scripts/download.py
MPLCONFIGDIR=/tmp/eda-matplotlib python edas/olist/scripts/eda.py
python edas/olist/scripts/validate.py
python edas/online_retail/scripts/download.py
MPLCONFIGDIR=/tmp/eda-matplotlib python edas/online_retail/scripts/eda.py
python edas/online_retail/scripts/validate.py
python scripts/informe_ejecutivo.py
python -m compileall -q scripts edas/olist/scripts edas/online_retail/scripts
python -m pip check
```

Si el entorno virtual no incluye pip, usar `/usr/bin/python3 -m pip --python .venv/bin/python check`. La descarga verifica SHA-256, miembros y CRC. Los datos, ZIP, manifiestos locales, credenciales y entorno virtual se excluyen de Git.

Olist conserva su versión 2 y licencia CC BY-NC-SA 4.0. Online Retail, de Daqing Chen (2015), UCI 352, DOI 10.24432/C5BW33, usa CC BY 4.0. Las licencias de datos y resultados son independientes; no atribuir la licencia de UCI a Olist.

Online Retail conserva todas las filas, incluidos 5.268 duplicados adicionales. Sus ventas positivas requieren cantidad y precio positivos, fecha y factura disponibles y ausencia de prefijo C. Cancelaciones y ajustes se contabilizan por separado. Para clientes se usan solo IDs conocidos; la recurrencia cuenta facturas distintas en la ventana, sin interpretar retención. Los precios están en GBP nominales, sin redondear líneas antes de agregarlas. Se publican estadísticas agregadas, sin listas de IDs de clientes ni transacciones.

## The Look

Analiza los tres CSV agregados de BigQuery en `edas/the_look/data/raw/`, sin consultar el servicio. Ejecutar `MPLCONFIGDIR=/tmp/eda-matplotlib python edas/the_look/scripts/eda.py` y `python edas/the_look/scripts/validate.py`; luego regenerar el README con `python scripts/informe_ejecutivo.py`. La validación comprueba las exportaciones, no los registros individuales del origen.

## Lectura estructural y viabilidad

Los informes usan siete secciones comunes. El README integra inventario, diagramas, reglas de unión, hallazgos y decisiones para permitir una lectura ejecutiva técnica sin abrir los tres informes. `scripts/estructura.py` genera esta presentación común a partir de resultados calculados; cada `eda.py` la aplica y `scripts/informe_ejecutivo.py` consolida el resumen.

Olist publica `tables/granularidad.csv` y `estructura.json`: pedidos sin detalle, con varios registros y máximo por pedido; identidades recurrentes; multiplicidad postal; tamaño esperado de un LEFT JOIN de los tres detalles. Ese tamaño se calcula multiplicando los conteos por pedido, con mínimo uno por detalle; no se materializa ni se usa ese cruce para métricas comerciales.

Online Retail publica `tables/dependencias.csv` y `estructura.json`: repeticiones de factura–producto y grupos con más de un valor de cliente, país, fecha, descripción o precio. Los nulos cuentan como un valor en esta prueba. Se comprueban dependencias observadas, sin certificar formas normales ni efectuar una migración. Ambos validadores recalculan los diagnósticos desde las fuentes originales.

La normalización propuesta distingue registros originales de entidades conceptuales. Una futura capa analítica conserva hechos a su granularidad: pedido, línea, pago, reseña o evento; cada medida debe indicar población, estado, período y unidad monetaria. No se suman atributos de cabecera repetidos por un enlace de detalle. The Look mantiene el alcance de validación sobre exportaciones agregadas.
