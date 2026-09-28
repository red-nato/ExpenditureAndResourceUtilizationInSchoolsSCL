# Resumen breve · Recursos escolares en La Cisterna (2022–2025)

> **Versión anterior.** La pregunta y el EDA fueron revisados el 28-09-2026. Consultar el [notebook único vigente](notebooks/EDA_gasto_educativo.ipynb) o su [HTML](informes/EDA_gasto_educativo.html). Este resumen documenta el planteamiento previo.

> La [guía unificada vigente](GUIA_UNIFICADA_LA_CISTERNA.md) reúne definiciones, KPI y guion de exposición. Este archivo queda como resumen de una página.

**Avance preparado el 27-09-2026 para el martes 29-09.** Una sola pregunta ordena el estudio: **¿qué se puede comprobar sobre el uso de los recursos públicos destinados a los colegios de La Cisterna?** Para responderla hay que seguir la secuencia *recurso → compra o gasto rendido → revisión oficial → entrega y uso*. Hoy solo tenemos partes de esa secuencia. **Todavía no hay una cifra de malgasto.**

## Qué abarca este avance

La investigación completa considera colegios públicos y particulares subvencionados. **La recolección nueva de este avance se limita a los ocho públicos**: los administró la Municipalidad hasta 2024 y el SLEP Santa Rosa en 2025. Los particulares subvencionados permanecen en el censo para dar contexto; sus compras no se incorporaron a la nueva base de órdenes públicas. El censo cambia de **60 establecimientos en 2022 y 2023 a 59 en 2024 y 2025**. Por eso cada comparación usa el universo de su año.

| Pieza de información | Qué sabemos ahora | Qué falta para concluir |
|---|---|---|
| Compras públicas | Se seleccionaron **1.034 órdenes de compra** relacionadas con la educación municipal (2022–2024) o con un colegio público de La Cisterna (2025). **637** se vinculan de forma inequívoca a un RBD (identificador de colegio). | Factura, pago, recepción y beneficiario. La orden expresa una intención o compromiso de compra; **no demuestra gasto pagado**. La cobertura de 2022 y 2025 es parcial. |
| Fiscalización | Hay **110 PAS** (procesos administrativos sancionatorios) publicados para el censo. | La base no informa la materia de los cargos. Se necesitan actas y resoluciones para saber cuáles tratan de rendición o uso de subvenciones. |
| Planificación y resultados | El PME (Plan de Mejoramiento Educativo) describe acciones y montos estimados; SIMCE e IDPS aportan contexto educativo. | Comprobantes de ejecución y comparaciones pertinentes por grado. Ni un monto PME ni un puntaje prueban buen o mal uso de recursos. |
| Sostenedores particulares subvencionados | Figuran en el censo y rinden subvenciones a la Superintendencia. | El detalle transaccional comparable no se verificó en una descarga pública por RBD; se preparó una solicitud documental, aún sin enviar. |

La Ficha Comprador describe al **municipio o SLEP completo** en ventanas recientes; no mide a cada escuela. La revisión del índice del Observatorio ChileCompra tampoco produjo un caso textual para esos compradores. Ambos controles sirven como contexto y se explican en el informe, sin convertirlos en conclusiones de irregularidad.

La cobertura de compras es desigual: el archivo de 2022 no incluye Compra Ágil del segundo semestre; en 2025 solo seis órdenes del SLEP se pudieron atribuir con certeza a dos colegios de la comuna.

## Qué entregamos y qué sigue

**Avance listo para el martes:** un mapa reproducible de compras públicas y de vacíos documentales para los ocho colegios, integrado a un panel por RBD y año. El trato directo se marca para revisar sus antecedentes; por sí solo no señala una compra indebida. Las **26 órdenes candidatas** con atribución dudosa están separadas y no se suman a las cifras principales.

**Siguiente paso:** obtener las rendiciones por colegio, año y subvención; pedir la materia y las resoluciones de los PAS; después seleccionar operaciones concretas y cotejar orden, factura, pago, recepción y uso. Una afirmación de malgasto requiere avanzar de *señal → observación documentada → resultado administrativo → efecto material*. Un dato ausente queda «sin antecedente», no «cero».

## Dónde está cada cosa

1. **Esta guía** es la explicación breve y el orden de lectura.
2. El [análisis principal](informes/Analisis_La_Cisterna_2022_2025.md) contiene las cifras, filtros, fuentes y límites completos. Sus anexos temáticos son el [plan](informes/Plan_investigacion_La_Cisterna.md), el [marco de evidencia](informes/Marco_evaluacion_gasto.md), el [censo 2025](informes/Universo_2025.md) y la [cobertura de resultados educativos](informes/Cobertura_Agencia_2023_2025.md).
3. El [panel RBD–año](datos/procesados/la_cisterna/panel_rbd_anual.csv) reúne los cruces; el [diccionario](datos/DICCIONARIO.md) explica sus campos y el [cuaderno](notebooks/EDA_gasto_educativo.ipynb) reproduce los cálculos. Los archivos originales y las tablas intermedias en `datos/` son respaldo, no informes adicionales.
4. Las [solicitudes documentales](informes/Solicitudes_documentales_La_Cisterna.md) son borradores para cerrar los vacíos; **no se han enviado**.
5. El [paquete W1](workshop/GROUP_03_W1/README.md) conserva la entrega previa de cinco fuentes. Sirve como antecedente fechado; el análisis principal contiene el avance vigente con ChileCompra.
