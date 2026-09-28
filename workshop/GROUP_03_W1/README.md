# GROUP_03_W1 · Workshop 1 de Business Intelligence

**Grupo 03:** Javier Alcaíno, Lucas Riquelme y Renato Varela. **Revisión W1:** 25-09-2026. El grupo informó que el docente autorizó el tema educativo en vez de las bases de salud de la pauta; la autorización no equivale a aprobación de resultados. Este paquete W1 conserva el análisis original de cinco fuentes. La [guía breve actual](<../../Investigación exploratoria — gasto escolar Chile.md>) explica cómo se relaciona con el [avance del 27-09](../../informes/Analisis_La_Cisterna_2022_2025.md#avance-de-compras-públicas-ficha-comprador-y-cruces), que añade ChileCompra solo para los ocho públicos, Ficha Comprador y revisión de límites de la materia PAS, sin modificar las salidas históricas W1.

## Qué cambió

La investigación se concentra en **La Cisterna**. Incluye establecimientos públicos y particulares subvencionados con matrícula: **60 RBD en 2022–2023 y 59 en 2024–2025**. El RBD 9830 solo aparece en los dos primeros años. Los ocho públicos eran DAEM hasta 2024 y SLEP en 2025; en 2025 hay 51 particulares subvencionados. Los 17 de educación especial de ese año integran el censo financiero y se distinguen al interpretar indicadores educativos. No se usa el caso de Melipeuco.

El informe compara dos líneas de W1: **A, rendición y fiscalización de recursos** como pregunta principal; **B, PME y resultados de la Agencia de Calidad** como contexto. Ni los procesos sancionatorios ni las acciones PME demuestran por sí mismos malgasto. El objetivo siguiente es obtener rendiciones y expedientes acotados para verificar observaciones.

## Orden de lectura

1. `report/GROUP_03_W1_Report.pdf`: pregunta, dos líneas, evidencia revisada, límites y decisión provisional.
2. `analysis/W1_analisis_ejecutado.ipynb`: cuaderno con el cálculo reproducible y la salida guardada.
3. `analysis/outputs/`: perfil de cinco fuentes, controles de ocho etapas, panel anual de 238 RBD–año, cobertura por grado y métricas.
4. `data/DICCIONARIO.md` y `data/PROCEDENCIA.md`: unidad, llave propuesta, origen, transformación y límite de cada fuente.

## Reproducir

Desde esta carpeta, con Python 3.10+ y ReportLab para el PDF:

```sh
python analysis/w1_analisis.py
python analysis/crear_cuaderno.py
python analysis/generar_informe.py
```

Los cálculos usan solo la biblioteca estándar; el informe requiere `reportlab`. El cuaderno puede abrirse con Jupyter y ejecutarse de arriba abajo. No se necesita red para reproducir las salidas incluidas. Las fuentes originales y huellas de los extractos se documentan en `data/fuentes.json` y `data/manifiesto_extraccion.json`; el paquete contiene extractos territoriales, no los archivos nacionales completos. El [análisis principal](../../informes/Analisis_La_Cisterna_2022_2025.md) extiende ese núcleo con órdenes de compra; para reproducirlo requiere `7z` y los archivos de `datos/originales/chilecompra/`.

## Estado de la investigación

El censo, PME local, procesos Supereduc y bases públicas SIMCE/IDPS están incorporados. Los reportes individuales de la Agencia para cada colegio todavía deben reunirse; las bases estadísticas actuales permiten un primer cruce. La rendición financiera desagregada y los expedientes aún **no se han obtenido**. Las solicitudes documentales son borradores **no enviados** en el proyecto de investigación. Ninguna cifra del informe estima pérdida o malgasto definitivo. El profesor todavía no ha dado feedback de W1 porque no se ha entregado; la única sección que el grupo completará después es la reflexión individual.
