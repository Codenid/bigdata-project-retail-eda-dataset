# Convenciones de eda-dataset

- Python 3.12, scripts pequeños, pandas y matplotlib; evitar frameworks y notebooks obligatorios.
- Ejecutar desde la raíz; los scripts resuelven rutas respecto de su propio archivo.
- Originales CSV/XLSX en `edas/<dataset>/data/raw/`, nunca modificarlos ni versionarlos. No subir datos, secretos o `.venv`.
- EDAs independientes en `edas/olist/`, `edas/online_retail/` y `edas/the_look/`; no cruzar sus poblaciones.
- Olist versión 2: CC BY-NC-SA 4.0. Online Retail UCI 352: CC BY 4.0. Conservar URL, atribución y SHA-256 de cada fuente.
- Identificadores y prefijos postales como texto. Documentar denominadores y tratamiento de faltantes.
- Antes de unir tablas, explicitar granularidad, agregar por pedido y validar cardinalidad.
- Extremos no equivalen a errores; no borrar observaciones silenciosamente.
- Informe en español con cifras calculadas, rutas relativas y distinción entre hallazgos e hipótesis.
- No inferir causalidad a partir de correlaciones. No afirmar verificaciones no ejecutadas.

## Comandos de validación

```bash
python edas/olist/scripts/download.py
MPLCONFIGDIR=/tmp/eda-matplotlib python edas/olist/scripts/eda.py
python edas/olist/scripts/validate.py
python -m compileall -q edas/olist/scripts edas/online_retail/scripts
python -m pip check
```

Si `.venv` no incluye pip, usar `python3 -m pip --python .venv/bin/python check`.
Al cambiar el análisis, regenerar informe, tablas y gráficos, y ejecutar la validación independiente.

Para Online Retail ejecutar también download.py, eda.py y validate.py de `edas/online_retail/scripts/`. El README principal es un informe ejecutivo; las instrucciones técnicas viven en `docs/metodologia.md`.

- Markdown breve, claro y directo: hallazgos, denominadores y límites necesarios, sin detalle técnico innecesario.
- The Look se analiza desde CSV agregados locales; no afirmar validación de registros individuales ni ejecutar BigQuery sin autorización.
