# eda-dataset

Proyecto reproducible para descargar y explorar el Brazilian E-Commerce Public Dataset by Olist. Analiza las nueve tablas sin alterar los CSV originales y produce un informe en español con cifras, calidad de datos y ocho gráficos.

## Dataset y acceso

Fuente y documentación: [Olist en Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Nueve CSV relacionados: clientes, geolocalización, artículos, pagos, reseñas, pedidos, productos, vendedores y traducción de categorías. La documentación publica 126,19 MB sin comprimir, con pedidos de 2016–2018. La descarga de la versión 2 se comprobó sin cuenta, API key ni autenticación. El ZIP real y los CSV se miden en el informe; reservar al menos 600 MB de espacio libre para entorno, datos, caché y archivos temporales.

Licencia de los datos: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Atribuir a Olist, respetar uso no comercial y compartir adaptaciones bajo la misma licencia. Los datos no se incluyen en el repositorio. Los resultados derivados mantienen estas condiciones; el proyecto no implica respaldo de Olist.

La URL entregada apunta a la versión vigente; `edas/olist/scripts/download.py` fija `datasetVersionNumber=2` y un SHA-256 conocido. Descarga mediante `curl -fL` con reintentos, valida hash, miembros y CRC, y extrae solo los nueve CSV. Reutiliza el ZIP verificado; `--force` vuelve a descargar. Si el endpoint cambia, exige login, devuelve HTML o cambia bytes, falla: no acepta silenciosamente un dataset diferente. No se necesitan credenciales para la ejecución comprobada.

## Reproducción

Requisitos: Python 3.12, `venv`, `pip`, `curl`, acceso a Kaggle y al índice de paquetes. Comandos desde esta carpeta, Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt
python edas/olist/scripts/download.py
MPLCONFIGDIR=/tmp/eda-matplotlib python edas/olist/scripts/eda.py
python edas/olist/scripts/validate.py
python -m compileall -q scripts
python -m pip check
```

`requirements.txt` fija las dos dependencias directas; `requirements.lock.txt` fija también todas las dependencias transitivas de la ejecución de referencia en Python 3.12/Linux. No garantiza compatibilidad con otras versiones de Python o reproducción binaria de PNG entre sistemas.

Si Python carece de `ensurepip` pero existe pip del sistema (como en el entorno de referencia), la alternativa ejecutada fue:

```bash
python3 -m venv --without-pip .venv
python3 -m pip --python .venv/bin/python install -r requirements.lock.txt
.venv/bin/python edas/olist/scripts/download.py
MPLCONFIGDIR=/tmp/eda-matplotlib .venv/bin/python edas/olist/scripts/eda.py
.venv/bin/python edas/olist/scripts/validate.py
.venv/bin/python -m compileall -q scripts
python3 -m pip --python .venv/bin/python check
```

Si tampoco existe pip del sistema, instalar los componentes `python3-venv` y `python3-pip` con el gestor del sistema antes de continuar. El análisis no requiere internet una vez descargados los datos y las dependencias. Los scripts funcionan también al invocarlos desde otro directorio.

## Estructura y resultados

```text
eda-dataset/
├── AGENTS.md
├── README.md
├── requirements.txt
├── requirements.lock.txt
├── edas/olist/scripts/
│   ├── download.py
│   ├── eda.py
│   └── validate.py
├── data/                  # ZIP, manifest.json y raw/; excluidos de Git
└── reports/
    ├── informe_eda.md
    ├── metricas.json
    ├── figures/           # 8 PNG
    └── tables/            # inventarios, estadísticas e integridad
```

Leer [el informe](reports/informe_eda.md). Incluye dimensiones, columnas y tipos, faltantes, duplicados, claves candidatas, referencias, parseo de fechas, importes inválidos, extremos IQR, distribuciones y relaciones a nivel de pedido. Los artículos y pagos se suman y las reseñas se promedian por pedido antes de cruzar, con validación uno a uno. Las correlaciones usan casos completos por par y exportan sus denominadores. No se imputan faltantes ni se eliminan extremos.

## Validación de referencia

Ejecución completada el 11 de octubre de 2026 con Python 3.12.3/Linux:

- Descarga pública inicial y `edas/olist/scripts/download.py --force`: ambas completadas; nueve CSV con SHA-256 y CRC correctos. ZIP: 44.717.580 bytes; CSV extraídos: 126.186.995 bytes.
- `edas/olist/scripts/eda.py`: informe, nueve tablas CSV, métricas JSON y ocho PNG generados; 99.441 pedidos conservados tras los cruces.
- `edas/olist/scripts/validate.py`: 14 enlaces locales válidos, ocho PNG decodificables, dimensiones/faltantes/duplicados de las nueve tablas contrastados con los CSV originales y métricas de pedidos recalculadas.
- `compileall`: sin errores; `pip check`: sin dependencias incompatibles.
- Inspección visual de los gráficos de faltantes y correlaciones: etiquetas y contenido legibles.

Hallazgos de referencia: 96.470 pedidos entregados con fechas completas, 8,11% posteriores a la estimación, mediana de entrega de 10,22 días. La relación entre entrega y reseñas es una asociación descriptiva, no una conclusión causal.
