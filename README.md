# GROUP_03_C1 · Respaldo documental del PME 2024 en La Cisterna

**Curso:** Business Intelligence · IIB423T-1 · Universidad del Desarrollo · Instructor: Tomás Fontecilla Correa
**Grupo:** GROUP_03 (el mismo de W1) · **Integrantes:** Javier Alcaíno, Lucas Riquelme y Renato Varela
**Entrega:** C1, versión del 28-09-2026, para el 29-09-2026 antes de las 17:50

**Pregunta:** ¿Cómo se distribuye la proporción de acciones PME 2024 con estimación de $0 o sin implementación declarada completa entre los establecimientos y dimensiones de La Cisterna, y qué casos conviene priorizar para solicitar respaldo documental?

**Resultado central:** 369 de 767 acciones (48,1 %) tienen estimación $0 o no declaran implementación completa; con un umbral de 50 %, 24 de 46 colegios entrarían primero a revisión. El KPI ordena solicitudes de respaldo; **no mide malgasto ni calidad**.

## Orden para abrir los archivos

1. `report/GROUP_03_C1_Report.pdf`: informe autocontenido (problema, siete pasos, calidad y Five Cs, EDA, límites, ML y dashboard, Process record y referencias).
2. `presentation/GROUP_03_C1_Slides.pdf`: diapositivas de la defensa.
3. `analysis/EDA_gasto_educativo.html` o `analysis/EDA_gasto_educativo.ipynb`: análisis ejecutado con todas sus salidas guardadas. El HTML es la misma salida en formato de lectura.
4. `data/procesados/la_cisterna/eda/`: tablas que respaldan cada cifra del informe.
5. `PROCESS_LOG.md`: bitácora de decisiones, retroalimentación y uso de IA.

## Estructura y rol de cada archivo

| Ruta | Rol |
|---|---|
| `analysis/EDA_gasto_educativo.ipynb` | Cuaderno único del análisis, ejecutado de arriba abajo con salidas guardadas |
| `analysis/scripts/eda_notebook_source.py` | Fuente editable del cuaderno (el `.ipynb` se genera desde aquí) |
| `analysis/scripts/crear_cuaderno_la_cisterna.py` | Genera, ejecuta y exporta el cuaderno |
| `analysis/scripts/integrar_chilecompra.py`, `pipeline_la_cisterna.py` | Lectura de las órdenes de compra y construcción del panel base |
| `analysis/figures/` | Gráficos producidos por el cuaderno |
| `data/originales/` | **Insumos originales** descargados (los pequeños; ver «Archivos omitidos») |
| `data/extraidos/la_cisterna/` | **Extractos de entrada sin limpiar** (reducción a La Cisterna) y su manifiesto con huellas SHA-256 |
| `data/procesados/la_cisterna/` | **Salidas procesadas**: panel RBD–año, tablas de OC y cobertura |
| `data/procesados/la_cisterna/eda/` | **Salidas procesadas del EDA**: una tabla CSV por cada resultado, limpieza, cruces y Five Cs |
| `data/fuentes.json`, `data/manifiesto_recuperacion_local.json` | Procedencia: URL, fecha de revisión y huellas |
| `data/referencias/` | Material del curso y W1 usado como referencia |

## Software y versiones

Las salidas guardadas se ejecutaron con Python 3.12.3, pandas 3.0.2, numpy 2.4.4, matplotlib 3.10.8, scipy 1.17.1, openpyxl 3.1.5 y 7-Zip 23.01 (más `nbclient`, `nbformat`, `ipykernel` y `Markdown` para ejecutar y exportar). `analysis/requirements.txt` fija las versiones del entorno original del grupo (Python 3.14, pandas 3.0.6). Al comparar ambas ejecuciones, 72 de 76 tablas salieron idénticas byte a byte; las diferencias fueron el inventario de archivos y tres tablas de correlación con diferencias de 1e-16.

**Instalación:** `pip install -r analysis/requirements.txt` y tener instalado `7z` (por ejemplo `apt install 7zip` o `brew install sevenzip`), porque las órdenes de compra vienen en archivos `.7z`.

## Cómo ejecutar

Desde la carpeta `GROUP_03_C1/`: `python analysis/scripts/crear_cuaderno_la_cisterna.py`. También se puede abrir `analysis/EDA_gasto_educativo.ipynb` y usar *Restart Kernel and Run All*. La raíz del proyecto se detecta buscando `data/extraidos/la_cisterna`, por lo que todas las rutas son relativas. Tarda cerca de 90 segundos. No descarga datos ni envía solicitudes.

## Fuentes: versión, URL y reconstrucción del caso reducido

| Fuente | Página o URL | Versión o fecha | Archivo local | Cómo se obtuvo el caso reducido |
|---|---|---|---|---|
| Directorio de establecimientos, Mineduc | https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/ | Directorios oficiales 2022 a 2025 (matrícula al 30 de abril de cada año; el de 2025 con fecha de archivo 26-09-2025) | `data/originales/directorio_*.csv` | Cuaderno, sección 2.3: comuna 13109, en funcionamiento, matrícula informada, dependencia 2, 3 o 6 y matrícula positiva. Da el censo 60/60/59/59 |
| Implementación PME 2024, Mineduc | https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/ | Base de Implementación 2024 descargada del portal Datos Abiertos; fecha de revisión local 25-09-2026 | `data/originales/pme_implementacion_2024.xlsx` | Cuaderno, sección 2.4: filas cuyo RBD está en el censo 2024, cotejadas una a una contra el XLSX oficial (767 acciones de 46 RBD) |
| PAS, Superintendencia de Educación | https://www.supereduc.cl/pas/ | Archivos anuales 2022 a 2025 (URL en `data/fuentes.json`) | `data/originales/pas_*.xlsx` | Cuaderno, sección 6: se relee el original nacional y se comprueba que la selección no pierde ningún RBD del censo de su año |
| SIMCE e IDPS, Agencia de Calidad | https://informacionestadistica.agenciaeducacion.cl/ | Archivos 2023 a 2025 (URL y huella en `data/fuentes.json`) | `data/extraidos/la_cisterna/simce_*.json`, `idps_*.json` | **Los RAR originales no se incluyen** (94 MB). El extracto contiene solo RBD del censo comunal de cada año, y el cuaderno comprueba que todas sus filas pertenecen a ese censo |
| Órdenes de compra, ChileCompra | https://datos-abiertos.chilecompra.cl/descargas/ordenes-y-licitaciones | 8 archivos semestrales: municipal 2022 a 2024 y SLEP 2025 | `data/originales/chilecompra/*.7z` | Cuaderno, sección 2.5 y `analysis/scripts/integrar_chilecompra.py`: una OC por código; se selecciona la unidad educación municipal o una escuela inequívoca del SLEP |

Las descargas pueden cambiar; se conservan los originales locales y sus huellas.

## Archivos omitidos y problemas sin resolver

- **No incluidos por tamaño:** los RAR de SIMCE e IDPS de la Agencia (94 MB), los ZIP de PAS (duplicados de los XLSX incluidos) y los RAR del Directorio (duplicados de los CSV). El cuaderno no los lee.
- **El script que extrajo SIMCE e IDPS desde los RAR no está en este paquete:** pertenecía a la organización anterior del proyecto. La reducción se documenta arriba y se verifica en el cuaderno, pero no puede repetirse desde este paquete sin descargar esos archivos.
- **Inventario de archivos** (`data/procesados/la_cisterna/eda/inventario_archivos.csv`): describe únicamente lo que contiene este paquete.
- **Pendientes de completar por el grupo** (están marcados en el informe): contribuciones individuales, reflexiones individuales y extractos de prompts y respuestas de IA del propio uso.
- **Diapositivas:** `presentation/GROUP_03_C1_Slides.pdf` debe exportarse desde la presentación en línea (ver `presentation/LEEME.txt`).
