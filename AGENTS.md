# Convenciones de eda-dataset

- Python 3.12, scripts pequeños, pandas y matplotlib; evitar frameworks y notebooks obligatorios.
- Ejecutar desde la raíz; los scripts resuelven rutas respecto de su propio archivo.
- CSV originales en `data/raw/`, nunca modificarlos ni versionarlos. No subir datos, secretos o `.venv`.
- Dataset Olist versión 2; conservar URL, SHA-256 y condiciones CC BY-NC-SA 4.0.
- Identificadores y prefijos postales como texto. Documentar denominadores y tratamiento de faltantes.
- Antes de unir tablas, explicitar granularidad, agregar por pedido y validar cardinalidad.
- Extremos no equivalen a errores; no borrar observaciones silenciosamente.
- Informe en español con cifras calculadas, rutas relativas y distinción entre hallazgos e hipótesis.
- No inferir causalidad a partir de correlaciones. No afirmar verificaciones no ejecutadas.

## Comandos de validación

```bash
python scripts/download.py
MPLCONFIGDIR=/tmp/eda-matplotlib python scripts/eda.py
python scripts/validate.py
python -m compileall -q scripts
python -m pip check
```

Si `.venv` no incluye pip, usar `python3 -m pip --python .venv/bin/python check`.
Al cambiar el análisis, regenerar informe, tablas y gráficos, y ejecutar la validación independiente.
