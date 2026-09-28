# Análisis principal: recursos escolares en La Cisterna, 2022–2025

> **Antecedente del 27-09-2026.** Para la nueva pregunta, KPI PME de un año, limpieza antes/después y EDA completo, consultar el [notebook vigente](../notebooks/EDA_gasto_educativo.ipynb) o su [HTML](EDA_gasto_educativo.html). Este informe conserva las verificaciones y el enfoque documental anterior; ya no es la exposición principal.

**Lugar en el proyecto:** la [guía unificada](../GUIA_UNIFICADA_LA_CISTERNA.md) explica la idea y el orden de lectura; este documento reúne la evidencia y el método completos. Los demás textos de `informes/` son anexos o accesos breves a este análisis.

**Avance actualizado: 27 de septiembre de 2026; entrega prevista para el martes 29.** La pregunta rectora es: **¿qué se puede comprobar sobre el uso de los recursos públicos destinados a los colegios de La Cisterna?** Para responderla se distingue qué se planificó, compró, rindió, observó y entregó. En este avance, la recolección nueva se concentra en los **ocho establecimientos públicos**: municipales/DAEM en 2022–2024 y SLEP Santa Rosa en 2025. El censo y las fuentes ya reunidas conservan a los particulares subvencionados como contexto descriptivo; su nueva recolección queda para la solicitud documental.

## Avance de compras públicas, Ficha Comprador y cruces

Se descargaron los ocho archivos semestrales de órdenes de compra de [ChileCompra, Descargas por organismo](https://datos-abiertos.chilecompra.cl/descargas/ordenes-y-licitaciones): municipio, código 100488, en 2022–2024; SLEP Santa Rosa, código 1890640, en 2025. Los CSV repiten cada OC por ítem e incluso por combinación ítem–cotización, por lo que se deduplicó por `codigoOC` antes de sumar. Para el municipio se seleccionó la unidad de compra `EDUCACIÓN`; las demás unidades municipales permanecen fuera de la cifra principal aunque algunas glosas mencionen escuelas. Para el SLEP solo se seleccionaron OC con identificación inequívoca de uno de los ocho RBD; una OC que también menciona Lo Espejo quedó sin atribución. Las **26 OC candidatas** de otras unidades o alcance territorial mixto están [separadas para revisión](../datos/procesados/la_cisterna/oc_candidatas_revision.csv), sin sumarlas al panel. La tabla [OC seleccionadas](../datos/procesados/la_cisterna/oc_escuelas_publicas.csv), el [resumen anual](../datos/procesados/la_cisterna/oc_cobertura_anual.csv) y el [manifiesto con URL y SHA-256](../datos/procesados/la_cisterna/manifiesto_chilecompra.json) permiten auditar el filtro.

| Año | Comprador y filtro | OC seleccionadas | Con RBD único | Trato directo | Valor de OC aceptadas/recepción conforme, CLP* |
|---|---|---:|---:|---:|---:|
| 2022 | Municipalidad, unidad EDUCACIÓN | 155 | 83 | 70 | $208.526.777,41 |
| 2023 | Municipalidad, unidad EDUCACIÓN | 426 | 265 | 68 | $545.234.235,65 |
| 2024 | Municipalidad, unidad EDUCACIÓN | 447 | 283 | 9 | $509.439.233,85 |
| 2025 | SLEP, glosa de RBD único | 6 | 6 | 2 | $42.653.931,60 |

\* Valor nominal de las OC en CLP con estado `Aceptada` o `Recepcion Conforme`, una vez por código. No incluye OC en otras monedas (3, 2 y 8 en 2022–2024), canceladas o aún enviadas. **Una OC, incluso con recepción conforme, no prueba pago**, y una orden plurianual no representa necesariamente desembolso de su año de envío. El archivo municipal del segundo semestre de 2022 no trae el CSV de Compra Ágil: la serie 2022 es incompleta para ese mecanismo. El SLEP compra para cinco comunas: las seis OC inequívocas se refieren solo a dos RBD (9693 y 9701), por lo que esta es cobertura mínima identificada, no el total de compras de los ocho colegios. Las 72/161/164 OC municipales sin RBD único permanecen en el agregado de la unidad EDUCACIÓN y fuera de los montos escolares individuales. El panel RBD–año incluye únicamente las **637 OC con RBD único**; un cero allí significa cero vínculos confirmados, no ausencia de compras.

La variable `trato_directo` se deriva de `ProcedenciaOC = Trato Directo` y sirve para priorizar lectura de causal, resolución y recepción. [ChileCompra explica las causales legales de contratación directa](https://www.chilecompra.cl/trato-directo-proveedor/). El indicador no acredita irregularidad. Estas OC describen adquisiciones de bienes, servicios y eventualmente inversión; **no son el universo PME** ni se suman a las estimaciones de acciones PME. Para hablar de gasto operativo efectivamente **pagado**, se requieren factura, pago y, cuando corresponda, recepción acreditada.

La [Ficha Comprador de la Municipalidad](https://comprador.mercadopublico.cl/ficha/informacion-general/69.072.000-0) muestra **170 reclamos** entre septiembre de 2025 y agosto de 2026 y **sin información** de días promedio de pago porque no usa SIGFE en ese indicador. Su [pestaña del Tribunal](https://comprador.mercadopublico.cl/ficha/demandas-judiciales/69.072.000-0) muestra **1 demanda** entre octubre de 2025 y septiembre de 2026 (rol 96-2026). La [Ficha del SLEP](https://comprador.mercadopublico.cl/ficha/informacion-general/61.981.070-8) muestra **14 días promedio de pago** y **37 reclamos** entre septiembre de 2025 y agosto de 2026; su [pestaña del Tribunal](https://comprador.mercadopublico.cl/ficha/demandas-judiciales/61.981.070-8) informa **ninguna demanda en los últimos 12 meses**. Los valores y ventanas están [anotados en una tabla fechada](../datos/procesados/la_cisterna/ficha_comprador_2026-09-27.csv). Son indicadores **del organismo completo y ventanas recientes**, no métricas de sus ocho colegios ni de cada ejercicio 2022–2025; consulta: 27-09-2026.

Se revisaron los **110 PAS** extraídos y los encabezados de los cuatro XLSX oficiales. La base **no trae materia de cargos ni motivo específico**: `actividad`, `programa` y sanción no permiten identificar cuáles RBD tienen “rendición de cuentas” o “uso de subvención”. La [tabla de revisión](../datos/procesados/la_cisterna/pas_revision_materia.csv) conserva los 110 `PA_ID` con `sin_antecedente_en_base_pas`; **no se contabiliza cero casos financieros**. La materia debe comprobarse en actas o resoluciones antes de clasificarlos. En el [índice de casos del Observatorio ChileCompra](https://www.chilecompra.cl/casos/) no se encontraron referencias textuales a Municipalidad de La Cisterna ni SLEP Santa Rosa al 27-09-2026; esto describe el índice consultado, no demuestra que nunca hayan sido investigados. Un caso publicado o un trato directo sería una señal documental que exige leer resultado y alcance; no acreditaría por sí solo malversación.

**Asimetría de acceso como hallazgo metodológico.** Los sostenedores particulares subvencionados rinden recursos públicos a la Superintendencia, pero sus compras propias no dejan, como regla, un registro equivalente de OC y Ficha Comprador en Mercado Público. En este avance tampoco se verificó un buscador público de estados de resultados transaccionales por RBD. La [rendición SEP de Ayuda Mineduc](https://ayudamineduc.cl/ficha/rendicion-de-cuentas-sep) confirma que ambos tipos de sostenedor rinden; la vía para obtener aquí la desagregación faltante es la [solicitud documental preparada](Solicitudes_documentales_La_Cisterna.md), aún sin enviar. Los PAS y PME disponibles no sustituyen ese registro. Esta diferencia de trazabilidad justifica el siguiente paso y limita cualquier comparación de gasto entre dependencias.

## Resumen de lo comprobado

El censo anual del Directorio Oficial comprende **60 establecimientos en 2022 y 2023, y 59 en 2024 y 2025**. Los ocho públicos figuran como municipales DAEM hasta 2024 y como SLEP en 2025. Hay 52 particulares subvencionados en 2022–2023 y 51 en 2024–2025: el RBD **9830** solo aparece en los dos primeros años. Este cambio impide usar los 59 colegios de 2025 como denominador automático de todo el período. El RBD 9860 de administración delegada queda fuera porque corresponde a otra dependencia.

Las fuentes integradas registran **110 procesos PAS** de la Superintendencia publicados en archivos 2022–2025, **767 acciones PME 2024** de 46 RBD, **236 filas SIMCE** y **936 filas IDPS** de 2023–2025. Los PAS se asocian a 39 establecimientos y muestran 47 multas y 0 reintegros en primera instancia en este extracto. La suma de montos **estimados** PME es $9.009.408.718. Ninguno de estos números representa por sí mismo recursos malgastados, pagos efectuados o efectos sobre el aprendizaje.

Dentro del PME, **469 de 767 acciones** se declaran completas y **149** tienen estimación total cero. Por dimensión, [la tabla reproducible](../datos/procesados/la_cisterna/pme_dimensiones.csv) muestra acciones, RBD, declaraciones completas y estimaciones cero; Gestión de Recursos tiene la mayor mediana estimada por acción ($11.775.000). Estos patrones orientan preguntas de verificación, sin acreditar ejecución o eficacia.

La relevancia de estudiar uso y rendición está respaldada por la [evaluación de la Subvención Escolar Preferencial de DIPRES, marzo de 2023](https://www.dipres.gob.cl/597/articles-308400_informe_final.pdf), que analiza uso de recursos y procesos operativos de rendición. La [Ley 20.248, texto vigente](https://www.bcn.cl/leychile/navegar?idNorma=269001), vincula la SEP con el Plan de Mejoramiento Educativo y la rendición de su uso. Esta política aplica a sostenedores públicos y particulares subvencionados que participan en el régimen correspondiente; la presencia de un colegio en el Directorio no demuestra por sí sola que una subvención específica le corresponda.

## Siete pasos para formular la pregunta

| Paso de Clase 03 | Decisión en este estudio | Vacío visible |
|---|---|---|
| 1. Decisión | Elegir casos para revisión documental y precisar qué se puede publicar. | Sin rendición detallada no puede estimarse gasto objetado. |
| 2. Criterio de éxito | Cobertura anual explícita y hallazgos con monto, período, resolución, descargos y evidencia de uso. | Faltan expedientes y soporte transaccional. |
| 3. Preguntas de negocio | ¿Qué se recibió, declaró, aceptó/rechazó y entregó/empleó? | Los archivos actuales solo cubren parte de la cadena. |
| 4. Proceso de negocio | Transferencia → planificación → rendición → fiscalización → resolución → recepción/uso. | No hay llave automática compra–acción–RBD. |
| 5. Entidades, eventos y estados | RBD, sostenedor, subvención, cuenta, acción, PAS, compra, beneficiario, recurso y estado de apelación. | Una multa y un reintegro son entidades/medidas distintas. |
| 6. Representación | Panel RBD–año y tablas separadas de acciones, indicadores, procesos y cuentas. | Una compra compartida necesita tabla puente respaldada. |
| 7. Medición | Cobertura de fuentes, montos aceptados/rechazados firmes, saldos y servicios acreditados. | No mezclar estimación PME, multa y pérdida. |

Estos siete pasos describen el problema. Las **ocho etapas de preparación de datos** siguientes son otro marco, aplicado al material ya reunido.

## Ocho etapas reproducibles: Load → Profile → Explore → Clean → Impute → Transform → Validate → Explore again

El programa [analizar_la_cisterna.py](../scripts/analizar_la_cisterna.py) ejecuta el núcleo de cálculo del workshop y añade el módulo [integrar_chilecompra.py](../scripts/integrar_chilecompra.py). Sus cinco entradas reducidas están en `datos/extraidos/la_cisterna/`; las OC originales comprimidas se conservan en `datos/originales/chilecompra/`. Produce `datos/procesados/la_cisterna/`. Requiere `7z` para leer los `.7z` oficiales. Las tablas no se corrigen a mano.

| Etapa | Operación concreta | Evidencia generada o criterio |
|---|---|---|
| **Load** | Lee cinco extractos base y la selección OC deduplicada por código. | 238 filas Directorio, 110 PAS, 767 PME, 236 SIMCE, 936 IDPS y 1.034 OC seleccionadas. |
| **Profile** | Declara unidad y llave propuesta antes de unir; cuenta duplicados y nulos críticos. | [`perfil_fuentes.csv`](../datos/procesados/la_cisterna/perfil_fuentes.csv). Las seis llaves propuestas tienen cero duplicados; RBD nulo en OC se conserva explícito. |
| **Explore** | Cuenta establecimientos por año y PAS por año de archivo en fuentes separadas. | 60/60/59/59 RBD; PAS 21/39/31/19. `archivo_anio` no equivale siempre a ingreso o término. |
| **Clean** | Convierte RBD/año a enteros, montos a decimal, grado a código uniforme. Conserva originales. | No descarta filas. Para SIMCE/IDPS conserva versiones y medidas originales. |
| **Impute** | Decide explícitamente qué ausencia permite sustitución. | **No** imputa rendición, pago, puntaje ni materia PAS. Cero OC vinculadas significa cero coincidencias inequívocas en este extracto, no cero compras. |
| **Transform** | Agrega PAS/PME/Agencia y OC con RBD único antes del join. | [`panel_rbd_anual.csv`](../datos/procesados/la_cisterna/panel_rbd_anual.csv): 238 filas; una por colegio y ejercicio, sin asignar compras compartidas. |
| **Validate** | Comprueba unicidad, pertenencia a censo anual, conservación de conteos y ausencia de multiplicación. | [`controles_etapas.csv`](../datos/procesados/la_cisterna/controles_etapas.csv); el programa falla si se rompe una aserción sustantiva. |
| **Explore again** | Relee cobertura y cambios después de validar. | PME con fila: 8/8 públicos y 38/51 particulares en 2024; se desconoce aplicabilidad exacta para los 13 sin fila. |

El diccionario operativo del [workshop](../workshop/GROUP_03_W1/data/DICCIONARIO.md) detalla cada unidad y campo. La llave financiera futura `RBD + ejercicio + subvención + cuenta + versión` sigue **propuesta**, a la espera de inspeccionar la rendición original. Para una transacción se necesita además identificador propio.

### Controles de calidad

Se emplean cinco nombres **provisionales** porque el grupo no confirmó la nomenclatura exacta del curso: **Complete** (nulos y cobertura), **Correct** (tipos/rangos), **Consistent** (mismo significado de RBD y año), **Currency** (fecha y versión), **Concordant/Unique** (uniones y llaves). La trazabilidad de decisiones y documentos se registra aparte. No se presenta esta lista como cita literal de la clase.

## Lectura por fuente y denominador

| Fuente | Unidad real | Resultado y lectura válida | No permite concluir |
|---|---|---|---|
| Directorio | RBD–año | Universo anual y dependencia. En 2025: 8 SLEP y 51 particulares, 42 de oferta básica/media regular y 17 especiales. | Que todos recibieron SEP/PIE o fueron fiscalizados. |
| Superintendencia PAS | PA_ID, asociado a RBD; año de archivo | 110 procesos en cuatro archivos; la materia específica queda sin antecedente en esta base. | Clasificación financiera, monto malgastado, tasa de fiscalización o ausencia de irregularidad si no hay fila. |
| ChileCompra OC | `codigoOC`; RBD solo con mención única | 1.034 OC seleccionadas, de ellas 637 con RBD único; flag de trato directo. | Pago, destino final, totalidad del gasto escolar o equivalencia con PME. |
| PME 2024 | Acción declarada; `fila_excel` localiza extracción | 767 acciones de 46 RBD; 134 de 8 públicos y 633 de 38 particulares. | Compra pagada, gasto aprobado o implementación efectivamente verificada. |
| SIMCE 2023–2025 | RBD–año–grado; medidas por área | [Cobertura por grado](../datos/procesados/la_cisterna/cobertura_agencia_por_grado.csv) separa fila de puntaje válido y muestra versión. | Un resultado único del colegio, efecto del gasto o puntaje cero si falta. |
| IDPS 2023–2025 | RBD–año–grado–indicador | Promedios por indicador y versión, solo cuando están publicados. | Comparación directa entre indicadores/grados o causalidad. |

El [portal de resultados de la Agencia](https://www.agenciaeducacion.cl/preguntas-frecuentes-simce/) ofrece fichas por establecimiento y perfiles de acceso. Las bases públicas ya permiten el cruce estadístico; **falta recopilar y cotejar los reportes individuales** de cada colegio. Las escuelas especiales no se deben evaluar mediante un SIMCE inexistente; requieren indicadores pertinentes a su oferta.

## Dos líneas analíticas y uso propuesto

**A — rendición y fiscalización territorial (principal).** Usuario propuesto: Superintendencia y sostenedores, para priorizar revisión documental y corregir registros. Integrar estados de resultados 2022–2024 y 2025 si están cerrados, por RBD–año–subvención–cuenta. Distinguir declarado, aceptado, rechazado, saldo, reintegro y estado de recurso. Seleccionar expedientes financieros y algunos sin hallazgo para controlar sesgo de selección. Un futuro tablero mostraría monto y documento por estado; un modelo predictivo solo sería defendible con etiquetas de resoluciones firmes, datos anteriores al desenlace y casos negativos revisados.

**B — planificación PME y resultados educativos (complementaria).** Usuario propuesto: equipos directivos y comunidades escolares, para identificar brechas de registro y acciones que requieran verificación. Un tablero mostraría presencia PME, dimensión, avance declarado, SIMCE/IDPS por grado y grupo pertinente, más versión y faltantes. Un futuro modelo de acciones no completadas requeriría varios años de acciones comparables, estados validados y definición estable de la variable objetivo. Ningún modelo se entrena con los datos actuales.

Las comparaciones entre estimación PME y resultados educativos quedan **descriptivas**: la cobertura PME 2024 llega a 46 RBD y sus acciones se agrupan en cuatro dimensiones; las medidas de Agencia se publican por grado e indicador. El número de casos comparables cambia con cada cruce. No se interpreta una correlación o regresión entre montos y puntajes como efecto del gasto ni se ocultan los denominadores de cada subconjunto.

## Regla para hablar de posible malgasto

1. **Señal:** dato atípico o proceso; activa revisión, no juicio.
2. **Observación documentada:** acto o rendición identifica hecho, monto, RBD/sostenedor, período y descargos.
3. **Resultado administrativo:** resolución y reclamaciones permiten saber si el rechazo o reintegro está firme.
4. **Efecto material:** pago, recepción, inventario o prestación acreditan si el recurso llegó y se usó.

No se suman multas a gasto rechazado. Un saldo puede trasladarse; una estimación PME no es pago. Un puntaje bajo no demuestra mal uso de dinero. Cuando falta un eslabón, la ficha queda «sin antecedente», no «cero» ni «irregular».

## Próxima obtención documental acotada

Los [borradores de solicitudes](Solicitudes_documentales_La_Cisterna.md) **no se han enviado**. La primera entrega debe incluir rendiciones agregadas y diccionario para el censo anual; la segunda, libros y respaldos solo de casos seleccionados tras clasificar materia PAS. Consultar cierre 2025 antes de pedirlo como ejercicio completo. Para colegios particulares subvencionados, solicitar al órgano público los registros que obren en su poder; no inferir que Mercado Público cubre todas sus compras.

### Fuentes

- DIPRES (2023), [*Evaluación Subvención Escolar Preferencial. Informe final*](https://www.dipres.gob.cl/597/articles-308400_informe_final.pdf).
- Biblioteca del Congreso Nacional, [Ley 20.248, texto vigente](https://www.bcn.cl/leychile/navegar?idNorma=269001), consultado 25-09-2026.
- Centro de Estudios Mineduc, [Directorio Oficial 2022–2025](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/).
- Mineduc, [bases PME 2024](https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/).
- Superintendencia de Educación, [PAS y diccionario 2022–2025](https://www.supereduc.cl/pas/).
- Agencia de Calidad, [SIMCE e IDPS](https://informacionestadistica.agenciaeducacion.cl/).
- ChileCompra, [descargas de órdenes y licitaciones](https://datos-abiertos.chilecompra.cl/descargas/ordenes-y-licitaciones), [guía de trato directo](https://www.chilecompra.cl/trato-directo-proveedor/) e [índice de casos del Observatorio](https://www.chilecompra.cl/casos/), consultados 27-09-2026.
- Mercado Público, Ficha Comprador de la [Municipalidad de La Cisterna](https://comprador.mercadopublico.cl/ficha/informacion-general/69.072.000-0) y del [SLEP Santa Rosa](https://comprador.mercadopublico.cl/ficha/informacion-general/61.981.070-8), consultadas 27-09-2026.
- Ayuda Mineduc, [rendición de cuentas SEP](https://ayudamineduc.cl/ficha/rendicion-de-cuentas-sep), consultada 27-09-2026.
