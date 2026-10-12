# The Look: consultas y resultados

El usuario ejecutó las consultas en BigQuery y dejó los tres resultados en `edas/the_look/data/raw/`. El análisis local no volvió a consultar BigQuery.

| Bloque | CSV recibido | Contenido |
| --- | --- | --- |
| Perfil | `thelook_perfil_tablas.csv` | Filas, claves, nulos, fechas y anomalías |
| Distribuciones | `thelook_distribuciones.csv` | Categorías, países, estados, meses y eventos |
| Relaciones | `thelook_relaciones.csv` | Cobertura, multiplicidad y consistencia entre tablas |

[SQL preparado](thelook_perfilado.sql): tres SELECT independientes. Conserva el marcador `__PROYECTO__.__DATASET__`; el origen exacto y los identificadores de trabajos no se recibieron. No usar ese archivo sin sustituir el origen.

[Informe de resultados](../reports/informe_eda.md). Las validaciones locales comprueban balances y huellas de los CSV, no los registros individuales de BigQuery.

Los importes incluyen todos los estados salvo indicación expresa y su moneda no está confirmada. Las fechas ausentes no se imputan. `sold_at` nulo no demuestra stock disponible; eventos sin enlace directo a pedidos no permiten atribuir conversión.

No se exportan datos personales. Los CSV originales permanecen excluidos de Git. `docs/fuentes.md` y `docs/integracion.md` no estaban disponibles; se continuó sin ellos por indicación del usuario.
