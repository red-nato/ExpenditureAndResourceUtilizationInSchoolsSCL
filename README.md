# Recursos escolares de La Cisterna

**Empieza por el [notebook completo y ejecutado](notebooks/EDA_gasto_educativo.ipynb)** o su [versión de lectura HTML](informes/EDA_gasto_educativo.html). Desde el 28-09-2026 concentran el análisis vigente: fuentes, pregunta, limpieza antes/después, histogramas, densidades, ECDF, faltantes, outliers, correlaciones y decisión documental.

**Pregunta propuesta:** ¿Cómo se distribuye la proporción de acciones PME 2024 con estimación de $0 o sin implementación declarada completa entre los establecimientos y dimensiones de La Cisterna, y qué casos conviene priorizar para solicitar respaldo documental?

Se adopta la línea B (PME/Agencia) para el avance actual. La línea A (rendiciones/PAS) queda como siguiente fase. El KPI es la unión de dos señales, sin duplicar acciones que cumplen ambas; no es una medida de malgasto. Su denominador son las acciones observadas en 2024. La cobertura permanece como control, no como KPI principal.

La investigación completa cubre establecimientos públicos y particulares subvencionados entre 2022 y 2025. **Este avance añade compras públicas solo para los ocho colegios municipales/SLEP.** El censo de los demás colegios sigue como contexto. Las órdenes de compra no son pagos y los datos actuales no cuantifican malgasto.

## Orden de lectura

| Si necesitas… | Abre… |
|---|---|
| Preparar la exposición y entender los KPI | [Diapositivas revisadas](presentacion/EDA_La_Cisterna_C1_revision.pptx) y secciones 5, 11 y 12 del notebook |
| Revisar cifras, filtros y límites | [Notebook completo](notebooks/EDA_gasto_educativo.ipynb) |
| Entender cada fuente descargada | Secciones 1 y 2 del notebook e [inventario individual](datos/procesados/la_cisterna/eda/inventario_archivos.csv) |
| Seguir decisiones, verificaciones y feedback | [PROCESS_LOG.md](PROCESS_LOG.md) |
| Ver qué documentos faltan y cómo pedirlos | [Solicitudes preparadas, aún sin enviar](informes/Solicitudes_documentales_La_Cisterna.md) |
| Repetir el análisis | [Cuaderno del avance](notebooks/EDA_gasto_educativo.ipynb) y [diccionario de datos](datos/DICCIONARIO.md) |

Los originales y extractos permanecen intactos. `datos/procesados/la_cisterna/panel_rbd_anual.csv` es el panel base; `datos/procesados/la_cisterna/eda/panel_rbd_anual_eda.csv` añade KPI y puntajes por grado/indicador. La carpeta `eda/` reúne las tablas reproducidas por el notebook. Los textos anteriores y la presentación del 27-09 son antecedentes; su pregunta y guion quedan reemplazados por esta revisión. El [paquete W1](workshop/GROUP_03_W1/README.md) conserva su fecha. La versión con reflexiones se identifica aparte en `informes/referencias/`.

## Reproducir el avance vigente

Desde la raíz del proyecto, con el entorno científico de `requirements.txt` y `7z`:

```sh
python scripts/crear_cuaderno_la_cisterna.py
```

El comando crea un kernel nuevo, ejecuta todas las celdas y guarda notebook y HTML. También se puede abrir el notebook y usar Restart Kernel and Run All desde la raíz o `notebooks/`. No basta generar un archivo sin ejecutarlo. En este computador se usó el entorno científico existente de la carpeta anterior `Code/BI/Auditoría Colegios - BI/.venv/`, sin instalar paquetes. Las fuentes están incluidas en este proyecto; no se necesita esa carpeta anterior para calcular el EDA, salvo que se desee ampliar el inventario histórico.

Huellas: [extractos](datos/extraidos/la_cisterna/manifiesto_extraccion.json), [ChileCompra](datos/procesados/la_cisterna/manifiesto_chilecompra.json) y [originales recuperados](datos/manifiesto_recuperacion_local.json). Para reproducir W1 se siguen sus instrucciones propias. No se enviaron solicitudes ni se publicó una entrega en Canvas.
