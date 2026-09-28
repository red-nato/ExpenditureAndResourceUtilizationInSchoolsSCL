# Cobertura de resultados de la Agencia de Calidad en La Cisterna

**Anexo de resultados educativos.** La [guía unificada](../GUIA_UNIFICADA_LA_CISTERNA.md) explica cómo se usa esta fuente dentro del estudio; el [análisis principal](Analisis_La_Cisterna_2022_2025.md) reúne los cruces actuales.

Se descargaron las bases públicas por establecimiento de [SIMCE e IDPS](https://informacionestadistica.agenciaeducacion.cl/) correspondientes a 2023, 2024 y 2025. El cruce por RBD conserva los puntajes, diferencias, marcas de significancia, código de grupo socioeconómico, versión y fecha de cada base en [SIMCE](../datos/procesados/simce_la_cisterna_2023_2025.json) e [IDPS](../datos/procesados/idps_la_cisterna_2023_2025.json). Las bases originales comprimidas siguen en `datos/originales/`. El denominador anual del Directorio es **60 RBD en 2023 y 59 en 2024–2025**; cada grado tiene un universo elegible distinto, aún por verificar. El [control reproducible por grado](../datos/procesados/la_cisterna/cobertura_agencia_por_grado.csv) separa fila, puntaje numérico, promedio IDPS y versión.

| Año | Grado evaluado | RBD en archivo SIMCE | RBD con puntaje de Lectura y Matemática | Públicos con puntaje | Particulares subvencionados con puntaje | RBD con IDPS |
|---:|---|---:|---:|---:|---:|---:|
| 2023 | 4.º básico | 33 | 32 | 7 | 25 | 32 |
| 2023 | II medio | 24 | 23 | 3 | 20 | 24 |
| 2024 | 4.º básico | 33 | 32 | 7 | 25 | 33 |
| 2024 | 6.º básico | 33 | 32 | 7 | 25 | 33 |
| 2024 | II medio | 24 | 24 | 3 | 21 | 24 |
| 2025 | 4.º básico | 33 | 32 | 7 | 25 | 32 |
| 2025 | 8.º básico | 32 | 32 | 7 | 25 | 32 |
| 2025 | II medio | 24 | 24 | 3 | 21 | 24 |

Los 42 RBD de básica/media regular aparecen al menos una vez en los archivos de la Agencia. El RBD **9499**, clasificado como educación especial en el directorio, aparece en algunas bases SIMCE con **0 estudiantes evaluados y puntajes vacíos**: no se incluye en la columna «con puntaje». El RBD **26384** aparece en SIMCE de II medio 2023 sin puntaje publicado. Que un RBD no tenga puntaje en un grado o año no significa bajo desempeño; puede no impartir ese grado o tener un resultado no publicable.

**Versiones:** SIMCE 2023 se rotula final. Los tres archivos SIMCE 2024 descargados se rotulan `preliminar20240422v1`; IDPS 2024 de II medio y 6.º básico también figura como preliminar, mientras 4.º básico se rotula final. Los archivos 2025 tienen códigos `v1` o `v2` y fechas de abril o junio de 2026. Se conservaron esas etiquetas literales; antes de publicar tendencias se comprobará si existe una versión posterior. En IDPS 2025 los códigos numéricos 1–4 se homologaron con los cuatro indicadores que el glosario del paquete denomina autoestima académica y motivación escolar, clima de convivencia escolar, participación y formación ciudadana y hábitos de vida saludable. Los códigos originales permanecen en el archivo filtrado.

La cobertura no permite atribuir una diferencia de puntaje al gasto del mismo año. Los grados cambian entre 2024 y 2025, los estudiantes no son necesariamente la misma cohorte y las diferencias de resultados tienen marcas de significancia publicadas por la Agencia. Toda comparación posterior debe conservar grado, área, contexto y versión de base. Las bases estadísticas no sustituyen los reportes individuales por establecimiento del [portal de resultados](https://resultadossimce.agenciaeducacion.cl/), cuya recopilación y cotejo continúa pendiente.
