# Procedencia y alcance de los datos de W1

Corte del paquete: 25-09-2026, Santiago. Las URL, fechas de recuperación y SHA-256 de los originales están en `fuentes_proyecto.json`. Los archivos CSV del paquete conservan filas y llaves de origen; no representan un censo de pagos.

| Archivo | Rol y unidad | Procedencia y transformación |
|---|---|---|
| `cgr_melipeuco_43_2024.pdf` | Documento primario, 91 páginas | Informe final CGR 43/2024, 10-06-2024; copia alojada por CIPER. Compras 2020-2022; visita 2023. |
| `cgr_tablas_extraidas.json` | Extracción sin normalizar de anexos 1, 2, 4 y 5 | `pdfplumber`; cada tabla retiene página PDF y celdas. Página 63 contiene dos anexos, separados al extraer. No incluye el anexo 3 con microdatos de estudiantes. |
| `cgr_compras_lotes.csv` | 29 partidas destino-documento-modelo | Tablas de anexo 1: se conservan texto original, página/fila y cantidades; se convierten importes CLP y fechas. Una factura puede tener varias filas. |
| `cgr_no_habidos.csv` | 628 registros de bienes observados | Anexo 4 (625) y tablas 3 (2) y 4 (1) del informe. 10.b significa identificación insuficiente, no desaparición individual probada. |
| `cgr_con_comodato.csv` | 600 registros con certificado | Anexo 5, no equivalen a bienes localizados. El cruce se hace por factura + serie normalizada sin fuzzy matching. |
| `pme_acciones_campos_seleccionados_2024.csv` | 129.726 acciones de 8.240 RBD | Selección de columnas cuantitativas de Implementación PME 2024, extracción Mineduc 16-01-2025; `fila_excel` preserva referencia original. `ESTIM_TOTAL` es estimación declarada, no pago. El RAR original se omite (aprox. 40 MB). |
| `directorio_campos_seleccionados_2024.csv` | 16.694 RBD | Selección del Directorio Oficial EE 2024, corte de matrícula 30-04-2024. `MAT_TOTAL` es conteo; no usar bandera `MATRICULA` como alumnos. |
| `pme_cisterna_extracto_2024.csv` y `directorio_cisterna_extracto_2024.csv` | 134 acciones y 8 RBD del piloto | Filtro `RBD IN (9693,9699,9700,9701,9703,9706,9722,9730)` sobre los dos archivos precedentes. |
| `fuentes_proyecto.json` | Manifiesto | URLs, versión, fecha de recuperación y hash de originales. |

**Reconstrucción de la selección reducida:** descargar los RAR de PME/directorio desde las URL del manifiesto y cotejar SHA-256. El proyecto original contiene `scripts/extraer_fuentes.py` y `scripts/analizar.py`; se copiaron a `analysis/antecedentes/` para examinar la extracción completa. Esos scripts requieren los originales grandes y la estructura del proyecto madre. Este paquete se ejecuta directamente con sus CSV reducidos, sin red. Para el CGR se incluye el PDF original y la extracción inicial de tablas, lo que permite cotejar cada fila por `pagina_pdf` y `fila_tabla`.

**Productos del workshop:** `analysis/w1_analisis.py` lee los CSV incluidos, comprueba conteos, llaves y uniones y genera las tablas y figuras en `analysis/outputs/`. Los datos de alumnos del anexo 3 del informe CGR no se incorporan.
