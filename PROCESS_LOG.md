# Process log · La Cisterna

Registro de decisiones, uso de IA, evidencia y respuesta a retroalimentación. Las fechas históricas se reconstruyen desde W1 y los archivos existentes; no se presentan como un historial Git de contribuciones individuales. Última revisión: 28-09-2026.

## Antecedente W1 del 25-09-2026

Fuente: `informes/referencias/W1_con_reflexiones_25-09-2026.pdf`, recuperada con hash en `datos/manifiesto_recuperacion_local.json`. La copia `workshop/GROUP_03_W1/report/GROUP_03_W1_Report.pdf` es una versión distinta, con reflexiones pendientes.

| Decisión registrada | Alternativa y razón | Evidencia conservada |
|---|---|---|
| Delimitar La Cisterna, públicos y particulares subvencionados | No continuar Melipeuco como caso principal: otro territorio | Directorios y censo 60/60/59/59; RBD 9830 solo 2022–2023 |
| Comparar A (rendición/PAS) y B (PME/Agencia), preferencia inicial A | PME no puede tratarse como prueba de malgasto | Informe W1, 767 acciones de 46 RBD; falta de rendiciones |
| Agregar cada fuente antes de unir por RBD–año | Unir directamente acciones con resultados multiplica filas | Llaves y controles del pipeline; 238 RBD–año |
| No imputar montos ni puntajes | Cero fabricaría evidencia de inactividad o bajo desempeño | Marcas de presencia y ausencias conservadas |
| Separar fila de Agencia y puntaje publicado | Tener una fila no garantiza resultado numérico | JSON con medidas y versiones |

W1 registra autorización del tema educativo y aportes informados por el grupo. No se atribuye al docente una evaluación del análisis que no consta en el documento. Las reflexiones individuales se conservan en sus palabras en el PDF; no se escriben nuevas reflexiones en nombre de integrantes.

## Incorporación de compras del 27-09-2026

Se conserva el avance existente: ocho archivos semestrales ChileCompra; unidad EDUCACIÓN municipal 2022–2024 y vínculos inequívocos SLEP en 2025. Se registraron 1.034 OC seleccionadas y 637 con RBD único. Las candidatas fuera de alcance permanecieron aparte. OC no acredita pago. Falta Compra Ágil municipal del segundo semestre 2022 y la cobertura SLEP es parcial. La Ficha Comprador usa ventanas recientes del organismo, no resultados por colegio.

## Revisión del 28-09-2026

### Instrucción y retroalimentación recibida

El usuario pidió reformular la pregunta según los datos, explicar las fuentes descargadas y rehacer el EDA en **un mismo notebook**, con limpieza antes/después, histogramas, densidades, correlaciones, missingness y outliers. La retroalimentación proporcionada señala que W1 mejora framing y documentación, pero no completa el EDA. Recomienda adaptar el KPI de Lucas a un año, explicitar usuarios/decisión A/B, graficar dimensiones, conservar bitácora y relegar siete pasos/Five Cs al respaldo.

No se afirma que esa retroalimentación provenga directamente del profesor: se registra como material entregado por el usuario.

| Sugerencia | Decisión | Razón y evidencia |
|---|---|---|
| Cambiar pregunta | Incorporada | Pregunta descriptiva sobre señales PME 2024 por colegio/dimensión y priorización de respaldo |
| KPI anual de variación | Adaptada a un corte 2024 | No hay serie PME extraída. Se computa unión de estimación cero o no declarada completa |
| Preferencia por A de W1 | Cambiada a B para este avance | La evidencia disponible responde planificación declarada; A requiere rendiciones y expedientes |
| Usar cobertura como KPI principal | Relegada a control de disponibilidad | El KPI principal vincula una señal observada con una solicitud documental |
| Mostrar antes/después | Incorporada | Conteos originales/selección, conversiones, vacíos, ejemplos, deduplicación OC y efecto monetario |
| Borrar extremos para limpiar | Rechazada | Se marcan y conservan; exclusión y winsorización solo en sensibilidad |
| Imputar puntajes/montos | Rechazada | Ausencias estructurales y de registro; falta sustento para sustitución |
| Correlacionar panel | Incorporada como diagnóstico | Corte 2024 por RBD, Pearson/Spearman, n por pareja, segmentación y sensibilidad |
| Inferir materia financiera PAS por actividad/programa | Rechazada | El campo de cargos no está en la fuente |
| Siete pasos y Five Cs | Anexo/respaldo | No sustituyen exploración. Nombres Five Cs permanecen provisionales de W1 |

### Fuentes recuperadas y alcance de la inspección

Se inspeccionaron el proyecto vigente, su carpeta anterior en `Code/BI/`, la calendarización y materiales de clase. Se recuperaron por copia local dos Directorios, XLSX y diccionario PME, W1 con reflexiones, calendarización y PDF de EDA. SHA-256 de origen y copia coinciden. No se modificó la carpeta anterior. `inventario_archivos.csv` documenta individualmente las fuentes y resultados encontrados en las carpetas de datos, incluidos antecedentes de Melipeuco y PME nacional que no entran al censo actual.

No se encontró un archivo independiente llamado pseudo temario. Se aplicaron los requerimientos descritos por el usuario y contrastados con el material de EDA disponible. La carpeta Downloads no permitió lectura; no se afirma que el inventario cubra todos los archivos del computador.

### Uso de IA y verificaciones

Codex apoyó la inspección de fuentes, el código del notebook, la documentación, los gráficos y la reformulación propuesta. Las salidas numéricas se calcularon con los archivos locales; no se generaron datos sintéticos. La decisión final de adoptar la pregunta y la defensa de sus límites corresponden al equipo.

- Se contrastaron los extractos PME con el XLSX oficial, los RBD con los Directorios de cada año y PAS con los XLSX anuales.
- Se añadió auditoría de granularidad OC desde los ocho originales, con conteos y sumas antes/después bajo los mismos filtros.
- Se corrigió en el pipeline una regla que podía producir monto OC cero cuando había órdenes vinculadas pero ninguna elegible en CLP. Ahora ese caso conserva ausencia.
- Se preservaron los extractos originales y sus huellas. Las conversiones inesperadas detienen el notebook.
- El notebook se ejecuta con un kernel nuevo y calcula las salidas; no se ensamblan salidas manuales como sustituto de ejecución.
- El entorno científico ya instalado en la carpeta anterior aporta bibliotecas ausentes del runtime documental. No se instalaron paquetes nuevos.
- Jupyter requirió autorización para su conexión local porque el sandbox bloqueó el enlace entre cliente y kernel.

### Evidencia de cierre

La ejecución guarda `datos/procesados/la_cisterna/eda/validaciones.csv`, `resultados_eda.json`, perfiles, matrices de faltantes, outliers, correlaciones y listados del KPI. El notebook y la copia HTML contienen las salidas completas. La inspección visual y la ejecución final se registran al cerrar esta revisión.

### Pendientes sustantivos

Validar el umbral operativo con capacidad real de revisión; confirmar aplicabilidad PME de los 13 RBD sin fila; recopilar el padrón de aplicación Agencia y reportes individuales; verificar versiones preliminares; obtener rendiciones/pagos/recepción y cargos PAS; contrastar una muestra sin señal para conocer omisiones. No se enviaron solicitudes, no se entrenó un modelo y no se etiquetó a colegios como irregulares.
