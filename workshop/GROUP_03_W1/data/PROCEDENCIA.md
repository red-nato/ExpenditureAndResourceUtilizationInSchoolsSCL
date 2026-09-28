# Procedencia y unidades

| Archivo | Fuente y unidad | Transformación local | Límite |
|---|---|---|---|
| `universo_la_cisterna_2022_2025.json` | Directorio Oficial Mineduc, RBD–año | La Cisterna, funcionamiento con matrícula, dependencia pública o particular subvencionada; 2022–2025 | Censo 60/60/59/59; RBD 9830 solo 2022–2023. RBD 9860 de administración delegada queda fuera. |
| `procesos_supereduc_la_cisterna_2022_2025.json` | Supereduc, PAS, PA_ID | Archivo anual oficial, filtrado a los 59 RBD; conserva fila de origen y campos de estado | Año de archivo no siempre coincide con ingreso/término; PAS no equivale a hallazgo financiero. |
| `pme_la_cisterna_2024.csv` | Mineduc, acción PME 2024 | Filtrado por RBD desde la selección de campos nacional del workshop anterior | Monto estimado y avance declarado, no pago ni gasto aprobado. La falta de acción no implica incumplimiento. |
| `simce_la_cisterna_2023_2025.json` | Agencia de Calidad, RBD–año–grado | Extraído de bases públicas; conserva medidas, versión y archivo | Una fila puede no tener puntaje; no imputar cero ni comparar grados diferentes. Algunas versiones 2024 son preliminares. |
| `idps_la_cisterna_2023_2025.json` | Agencia de Calidad, RBD–año–grado–indicador | Extraído de bases públicas; conserva medida, versión y archivo | Cobertura variable por aplicación; algunos archivos 2024 preliminares. |
| `fuentes.json` y `manifiesto_extraccion.json` | Paquetes oficiales y extractos reducidos | URL, fecha/versión y SHA-256; el segundo manifiesto agrega Directorios 2022–2023 y PME | Permiten auditar selección; los paquetes comprimidos originales no se duplican aquí. |

Fuentes públicas del paquete W1: [Directorio Mineduc](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/), [PAS Supereduc](https://www.supereduc.cl/pas/), [PME Mineduc](https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/), [Agencia de Calidad](https://informacionestadistica.agenciaeducacion.cl/). Las OC agregadas después de W1 tienen [manifiesto propio con URL y SHA-256](../../../datos/procesados/la_cisterna/manifiesto_chilecompra.json).

## Reglas de cruce

- RBD identifica al establecimiento; año identifica el denominador anual. En 2024 los ocho públicos son DAEM y en 2025 SLEP. El rótulo de dependencia en un PAS se conserva como dato del expediente, pero la clasificación del panel se toma del directorio del año.
- Los procesos se cuentan una vez por `pa_id`. La fila del archivo anual y el estado de instancia se conservan para verificar casos.
- PME se cuenta por acción y se agrega a RBD solo como planificación. No sumar estas estimaciones a gastos rendidos.
- SIMCE e IDPS se conservan por año, grado e indicador/área. Los 17 establecimientos de educación especial requieren indicadores acordes a su oferta; un RBD con fila sin puntaje no cuenta como resultado publicado.
- Estas son bases estadísticas públicas, no una colección de reportes individuales por colegio. Incorporar tales reportes es un paso documental pendiente.
- La ventana de rendición propuesta es 2022–2025, máximo cuatro ejercicios, con 2025 condicionado a disponibilidad y cierre. Esa rendición no forma parte del paquete actual.

El [diccionario operativo](DICCIONARIO.md) explicita cada fila, campos y llave propuesta. `analysis/outputs/perfil_fuentes.csv` registra el perfil real; `analysis/outputs/controles_etapas.csv` deja la secuencia de decisiones y comprobaciones.
