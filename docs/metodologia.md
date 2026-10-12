# Organización y metodología

Los dos análisis son independientes. `edas/olist/` contiene sus nueve tablas originales locales, scripts, informe, tablas y gráficos; `edas/online_retail/` contiene el Excel original local y sus propios artefactos. No se mezclan registros, monedas ni poblaciones. El README raíz presenta resultados ejecutivos; cada informe detalla definiciones, denominadores y limitaciones.

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
