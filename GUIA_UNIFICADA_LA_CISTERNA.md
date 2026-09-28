# Guía única del EDA y de la presentación · La Cisterna

> **Antecedente del 27-09-2026.** La revisión del 28-09 reemplaza esta pregunta, KPI principal y guion. El contenido vigente está reunido en el [notebook completo](notebooks/EDA_gasto_educativo.ipynb), su [HTML](informes/EDA_gasto_educativo.html) y las [diapositivas revisadas](presentacion/EDA_La_Cisterna_C1_revision.pptx). Se conserva este texto para documentar el cambio de enfoque; no usarlo como guion vigente.

**Versión:** 27 de septiembre de 2026. **Exposición:** 15 minutos ante el profesor. **Equipo:** Javier Alcaíno, Lucas Riquelme y Renato Varela. **Pregunta:** ¿qué se puede comprobar sobre el uso de recursos públicos destinados a los colegios de La Cisterna entre 2022 y 2025?

Esta es la entrada única para estudiar y presentar el avance vigente. El [análisis principal](informes/Analisis_La_Cisterna_2022_2025.md) contiene el detalle de cifras y filtros; las demás guías se conservan como anexos de evidencia. El [paquete W1](workshop/GROUP_03_W1/README.md) documenta una entrega anterior y no sustituye este corte, que ya integra ChileCompra. **Melipeuco no forma parte del EDA vigente.**

## 1. Tesis para la exposición

Construimos un mapa reproducible de establecimientos, compras públicas, planificación PME, procesos de fiscalización y resultados educativos. Permite saber **dónde hay registros y dónde falta evidencia**. Todavía no permite medir cuánto se malgastó ni demostrar si una compra mejoró el aprendizaje: faltan rendiciones desagregadas, pagos, recepción/uso y expedientes que aclaren la materia y estado de los procesos.

La investigación completa incluye establecimientos públicos y particulares subvencionados. La **nueva recolección de órdenes de compra** de este avance se concentra en los **ocho públicos**: municipales/DAEM hasta 2024 y SLEP Santa Rosa en 2025. Los particulares subvencionados permanecen en el censo y en otras fuentes, pero aún no tienen una base comparable de compras transaccionales.

## 2. Conceptos que debemos definir antes de mostrar cifras

| Término | Definición apropiada | Qué representa aquí |
|---|---|---|
| **RBD** | Rol Base de Datos: identificador del establecimiento educacional. | Llave para seguir un colegio por año. No identifica por sí mismo al comprador o al sostenedor. |
| **Sostenedor** | Entidad responsable de administrar uno o varios establecimientos. | Municipio/DAEM en 2022–2024, SLEP Santa Rosa en 2025 para los ocho públicos. Una compra central no se reparte entre RBD sin respaldo. |
| **OC** | Orden de compra: documento electrónico con que un comprador solicita un bien o servicio al proveedor en Mercado Público. | Unidad de la base ChileCompra. Su valor es el de la orden, no el pago acreditado. “Recepción conforme” es un estado de validación de entrega, no prueba de transferencia de fondos. |
| **Licitación** | Procedimiento de contratación mediante convocatoria y evaluación de ofertas, distinto del documento de orden de compra. | Este EDA trabaja principalmente con OC, no con expedientes completos de cada licitación; todavía no clasifica licitaciones. |
| **PME** | Plan de Mejoramiento Educativo. Organiza objetivos, estrategias y medidas anuales de mejora de cada establecimiento. | En el avance usamos la base pública de **Implementación PME 2024**. |
| **Acción PME** | Medida concreta de mejora que el establecimiento registra dentro de su planificación anual, con responsables, plazo, recursos y medios de verificación previstos. Durante Implementación registra su avance y puede ajustar la acción. | **Una fila del extracto 2024 es una acción registrada para un RBD.** No equivale a una licitación, OC, factura, pago ni colegio. `fila_excel` ubica la fila extraída; no es un identificador transaccional. El extracto reducido no conserva el nombre o descripción completa de la acción, por lo que no permite juzgar su pertinencia individual. |
| **Monto estimado PME** | Proyección de recursos declarada para una acción. | No es gasto ejecutado, rendido ni aprobado por la Superintendencia. |
| **Nivel de implementación PME** | Tramo de avance registrado por el establecimiento durante la etapa de implementación. | “Completa: 100%” significa **avance declarado**, no ejecución o efecto verificado por esta investigación. |
| **PAS** | Proceso administrativo sancionatorio de la Superintendencia de Educación. | La base pública lista procesos y estados, pero no trae la materia de cargos. Una multa no es el monto de un eventual gasto mal utilizado. |
| **SIMCE / IDPS** | SIMCE mide resultados de aprendizaje en grados y áreas evaluados; IDPS complementa con indicadores de desarrollo personal y social. | Contexto educativo por RBD, año, grado e indicador. No mide causalmente el efecto de una compra o acción PME. |
| **KPI** | Indicador clave de desempeño: medida con fórmula, unidad, período, denominador y decisión asociada. | Hoy la mayoría son **KPI de cobertura y trazabilidad**. Los KPI de uso eficiente requieren documentos aún no obtenidos. |

Definición PME y advertencia sobre estimaciones: [Mineduc, Bases de datos PME](https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/) y [Proceso de Verificación PME 2024](https://liderazgoeducativo.mineduc.cl/apoyo-tecnico-para-el-proceso-de-verificacion-2024/). Definición de OC: [ChileCompra, condiciones de uso](https://www.chilecompra.cl/terminos-y-condiciones-de-uso/). Definición de IDPS: [Agencia de Calidad](https://www.agenciaeducacion.cl/evaluar/otros-indicadores-de-calidad/).

## 3. Nuestros KPI en el EDA actual

Estos indicadores describen el **alcance y la calidad de la evidencia disponible**; no califican todavía si el dinero fue bien utilizado. Las cifras salen de [`metricas.json`](datos/procesados/la_cisterna/metricas.json), [`oc_cobertura_anual.csv`](datos/procesados/la_cisterna/oc_cobertura_anual.csv), [`pme_dimensiones.csv`](datos/procesados/la_cisterna/pme_dimensiones.csv) y los controles del panel.

| KPI o medida de control | Fórmula, universo y corte | Resultado | Decisión que permite; límite |
|---|---|---:|---|
| **Tamaño del censo anual** | RBD elegibles del Directorio Oficial, por año. | **60 / 60 / 59 / 59** en 2022–2025. | Fija el denominador; no usar 59 para todos los años. |
| **Cobertura de atribución escolar de OC** | OC seleccionadas con un RBD único / todas las OC seleccionadas. | **637 / 1.034 = 61,6%**. | El panel escolar usa esas 637. Las 397 restantes no se asignan a un colegio ni se reparten proporcionalmente. |
| **Participación de trato directo en OC seleccionadas** | OC con `ProcedenciaOC = Trato Directo` / OC seleccionadas. | **149 / 1.034 = 14,4%**. | Prioriza revisar causal y documentos. El trato directo puede ser legal; la tasa no mide irregularidad. |
| **Presencia de PME 2024** | RBD con al menos una fila de Implementación PME / RBD del grupo en el censo 2024. | **8/8 públicos; 38/51 particulares subvencionados**. | Describe presencia en esta base, no obligación/aplicabilidad exacta ni cumplimiento de cada colegio. |
| **Acciones PME declaradas completas** | Acciones con tramo “Implementación completa: 100%” / todas las acciones PME del extracto comunal. | **469 / 767 = 61,1%**. | Describe autorreporte de avance, no recepción, gasto ejecutado ni impacto. |
| **Acciones con estimación total cero** | Acciones con `ESTIM_TOTAL = 0` / todas las acciones PME. | **149 / 767 = 19,4%**. | Señala una condición del registro para revisar; no implica que la acción no se haya realizado o financiado por otra vía. |
| **Procesos PAS publicados** | Conteo de `PA_ID` y RBD distintos en archivos 2022–2025. | **110 procesos de 39 RBD; 47 multas en primera instancia**. | Permite pedir expedientes. No es tasa de fiscalización ni número de casos financieros: la materia de cargos falta. |
| **Cobertura de resultados educativos** | RBD con fila y con puntaje/promedio publicado, separado por año y grado. | **236 filas SIMCE; 936 IDPS**. | Permite describir disponibilidad. Las tasas deben calcularse por grado elegible, no sobre todos los colegios. Véase [tabla por grado](informes/Cobertura_Agencia_2023_2025.md). |

**Medidas auxiliares que no son KPI de eficiencia:** 767 acciones PME de 46 RBD; 134 acciones corresponden a los ocho públicos y 633 a 38 particulares. La suma de sus estimaciones es **$9.009.408.718**, que **no es gasto pagado**. El valor anual de OC aceptadas o con recepción conforme también es valor de órdenes, no desembolso. El año 2022 carece de Compra Ágil del segundo semestre en la descarga municipal; en 2025 solo seis OC del SLEP se atribuyeron inequívocamente a dos RBD. Las 26 OC candidatas de atribución dudosa quedaron aparte.

La **Ficha Comprador** ofrece reclamos, pagos y litigios del organismo comprador en ventanas recientes. Es contexto del municipio o SLEP completo, no un KPI de los ocho colegios ni del período 2022–2025. Tampoco se encontró una coincidencia textual de estos compradores en el índice consultado del Observatorio ChileCompra; eso no demuestra ausencia histórica de casos.

## 4. KPI necesarios para evaluar uso de recursos en la siguiente fase

**Estos aún no están calculados.** Requieren estados de resultados, libros de compras, facturas, pagos, recepción, resoluciones y seguimientos. Se presentan como diseño, nunca como hallazgos.

| KPI futuro | Fórmula o unidad propuesta | Evidencia indispensable | Interpretación correcta |
|---|---|---|---|
| **Cobertura de rendición** | RBD–año–subvención con estado de resultados / RBD–año elegibles para esa subvención. | Rendiciones y reglas de elegibilidad. | Mide si podemos estudiar el gasto, no su calidad. |
| **Gasto aceptado y rechazado** | Montos por RBD–año–subvención–cuenta, con versión y estado administrativo. Para tasa: rechazado firme / rendido del mismo universo. | Estado de resultados y resolución con reclamaciones. | “Observado”, “rechazado” y “firme” son estados distintos. |
| **Reintegro firme** | Monto con orden de reintegro firme por expediente y período. | Resolución final, reclamación y comprobante de reintegro. | No sumar a multas ni contar dos veces un rechazo. |
| **Gasto por estudiante** | Gasto aceptado o pagado del ejercicio / matrícula pertinente del mismo ejercicio. | Rendición/pago y matrícula, desagregados por fuente y nivel. | Magnitud contextual, no ranking automático de eficiencia. |
| **Trazabilidad completa de operación** | Operaciones con vínculo documentado entre propósito, OC/contrato, factura, pago, recepción y uso / operaciones revisadas. | Documentos transaccionales y beneficiario real. | Mide capacidad de justificar una operación. |
| **Costo por entrega útil** | Costo pagado / unidades o servicios efectivamente recibidos y utilizados, comparados con alternativas pertinentes. | Pago, actas, inventario/prestación y comparador válido. | Base para una evaluación de eficiencia; no se infiere del valor de OC. |

## 5. Cómo se hizo el EDA

1. **Delimitar universo.** Directorio 2022–2025, un RBD por año: 238 filas; ocho públicos en cada año. Excluir RBD 9860 de administración delegada, que pertenece a otra dependencia.
2. **Cargar seis fuentes.** Directorio, PAS, PME, SIMCE, IDPS y OC de ChileCompra. Guardar procedencia, año de archivo y versiones.
3. **Perfilar.** Declarar la unidad y llave de cada tabla; revisar duplicados y nulos. Las seis llaves propuestas quedan sin duplicados tras el procesamiento. En OC, **397 RBD vacíos** se conservan como no atribuibles.
4. **Limpiar sin fabricar información.** Normalizar RBD, años, grados y montos. No convertir ausencias de pago, puntaje o materia PAS en cero.
5. **Transformar.** Deduplicar CSV de OC por `codigoOC` antes de sumar, porque una misma orden aparece por ítem o cotización. Filtrar la unidad municipal EDUCACIÓN (2022–2024); en SLEP 2025 exigir mención inequívoca de RBD de La Cisterna. Agregar cada fuente a su unidad antes de unir.
6. **Validar y explorar de nuevo.** Panel final de **238 RBD–año**, sin multiplicar filas ni asignar compras compartidas. Verificar conteos originales, presencia PME y cobertura de Agencia por grado.

Archivos de reproducción: [script principal](scripts/analizar_la_cisterna.py), [cuaderno](notebooks/EDA_gasto_educativo.ipynb), [panel](datos/procesados/la_cisterna/panel_rbd_anual.csv), [controles](datos/procesados/la_cisterna/controles_etapas.csv) y [diccionario](datos/DICCIONARIO.md).

## 6. Qué podemos y qué no podemos concluir

- **Sí:** existe una base para seguir los 8 colegios públicos a través del cambio de sostenedor; las compras públicas tienen atribución escolar incompleta; el PME tiene 767 acciones declaradas en 2024; la base PAS no trae materia de cargos; SIMCE/IDPS aportan contexto con coberturas distintas por grado.
- **Todavía no:** cifra de malgasto, proporción de recursos bien utilizados, pagos efectivamente realizados, legalidad de cada trato directo, existencia de casos PAS financieros, calidad de cada acción PME o efecto causal del gasto sobre aprendizaje.
- **Interpretación temporal:** una OC de un año, una acción PME 2024 y un SIMCE posterior no forman automáticamente una secuencia causal. Las cohortes, grados, destinatarios y exposiciones pueden diferir.

## 7. Cuatro categorías de gasto: rúbrica propuesta, sin casos clasificados aún

La **unidad de clasificación** será una operación o partida identificada, con fuente de recursos, período y beneficiario. Se incluye un estado previo obligatorio, **«sin evidencia suficiente»**, cuando la cadena documental está incompleta. Por ello, los cuatro rótulos siguientes **no se aplicaron a las 1.034 OC ni a las 767 acciones**.

| Categoría propuesta | Condiciones mínimas para considerarla | Lo que falta comprobar ahora |
|---|---|---|
| **1. Gasto legítimo y bien utilizado** | Propósito permitido; pago, recepción y uso acreditados; producto o servicio pertinente y costo razonable frente a alternativa comparable. | Rendición, facturas, recepción, uso y comparador. Un SIMCE alto no sustituye esta prueba. |
| **2. Gasto legítimo pero aparentemente ineficiente** | Legalidad y entrega documentadas, pero costo por entrega, oportunidad o uso muestran una brecha relevante tras ajustar por contexto. | Costos pagados, cantidad útil, plazos y referencias comparables. “Aparentemente” obliga a revisar explicaciones. |
| **3. Gasto difícil de justificar respecto del objetivo declarado** | Hay operación documentada, pero el vínculo entre objetivo, destinatario y bien/servicio no queda acreditado tras solicitar respaldos. | Objetivo PME/contrato, beneficiario, medios de verificación y respuesta del sostenedor. No equivale automáticamente a ilegalidad. |
| **4. Gasto potencialmente irregular o improcedente** | Un acto oficial o evidencia material identifica una posible infracción, rechazo o contradicción sustantiva; se conserva el estado de descargos y recursos. | Expediente, resolución, reclamaciones y trazabilidad del monto. Solo una resolución firme permite llamar “firme” al resultado administrativo. |

La evaluación de **eficacia educativa causal** es una pregunta posterior y distinta. Requeriría definir intervención, escuelas y estudiantes expuestos, plazo de efecto, resultados pertinentes y un comparador creíble; un cruce simple con SIMCE posterior no demuestra causalidad.

## 8. Presentación de 15 minutos: contenido y guion

**Estructura:** 13 diapositivas principales y una lámina final de fuentes para consultas, alrededor de 1 minuto por diapositiva principal; reservar los últimos 2 minutos para conclusión y preguntas. Las cifras se muestran con fuente y denominador. El archivo editable está en [`presentacion/EDA_La_Cisterna_15min.pptx`](presentacion/EDA_La_Cisterna_15min.pptx).

### 1. Portada (0:30)
**En pantalla:** “Recursos escolares en La Cisterna, 2022–2025”; “EDA y trazabilidad del gasto”; Grupo 03 y nombres.
**Decir:** “Queremos saber qué se puede comprobar sobre el uso de recursos públicos en los colegios de la comuna. Presentamos lo que ya permiten las bases, y exactamente qué falta antes de emitir un juicio sobre el gasto.”

### 2. Pregunta, alcance y decisión (1:00)
**En pantalla:** pregunta rectora; investigación completa para públicos y particulares subvencionados; recolección nueva de OC para ocho públicos.
**Decir:** “El objetivo del EDA es decidir dónde pedir y revisar documentos. El panel territorial incluye a los particulares para dar contexto, pero hoy no existe una base de OC equivalente para sus compras.”

### 3. Universo y cambio de sostenedor (1:00)
**En pantalla:** censo 60/60/59/59; ocho públicos; DAEM hasta 2024, SLEP en 2025.
**Decir:** “El denominador cambia. Un RBD particular aparece solo hasta 2023. Mantuvimos cada año por separado y no atribuimos compras del SLEP de otras comunas a La Cisterna.”

### 4. Qué significa cada registro (1:15)
**En pantalla:** RBD = colegio; OC = solicitud/orden; acción PME = medida de mejora registrada; PAS = proceso; SIMCE/IDPS = contexto.
**Decir:** “Una acción PME es una medida de mejora con avance y recursos declarados por el establecimiento. No es una compra ni un pago. La base reducida que analizamos conserva dimensión, tramo de implementación y estimación, pero no la descripción íntegra de cada acción.”

### 5. Método EDA y controles (1:15)
**En pantalla:** delimitar, cargar, perfilar, limpiar, agregar, validar; 238 RBD–año.
**Decir:** “Resolvimos primero la unidad de análisis. Las órdenes originales se repetían por ítems; las deduplicamos por código. Solo unimos datos después de agregarlos a RBD y año, y dejamos los faltantes como faltantes.”

### 6. KPI actuales: cobertura y trazabilidad (1:15)
**En pantalla:** 637/1.034 OC atribuibles = 61,6%; PME 8/8 públicos y 38/51 particulares; 469/767 acciones completas declaradas = 61,1%.
**Decir:** “Estos son indicadores de qué podemos observar y de qué informa cada fuente. Ninguno mide todavía eficiencia o malgasto. Cada porcentaje tiene un denominador distinto.”

### 7. Compras públicas (1:15)
**En pantalla:** 1.034 OC seleccionadas; 637 con RBD único, 397 sin atribución; 149 de trato directo.
**Decir:** “Para el municipio filtramos la unidad EDUCACIÓN y para 2025 exigimos un colegio de La Cisterna identificable. Una OC no prueba pago. El trato directo activa revisión de causal y respaldos, sin presumir irregularidad. En 2022 y 2025 la cobertura es parcial.”

### 8. Planificación PME 2024 (1:15)
**En pantalla:** 767 acciones, 46 RBD; 469 completas declaradas; 149 con estimación cero; $9.009 millones estimados.
**Decir:** “La unidad es una acción, no un colegio. La suma es una estimación declarada. El 100% de avance informado no acredita ejecución financiera ni eficacia. Los 149 ceros son montos estimados de cero, no pruebas de falta de actividad.”

### 9. Fiscalización y resultados educativos (1:15)
**En pantalla:** 110 PAS de 39 RBD; 47 multas de primera instancia; 236 filas SIMCE y 936 IDPS.
**Decir:** “La base PAS no especifica los cargos. No podemos decir cuántos procesos son por mal uso de subvenciones. SIMCE e IDPS se leen por grado y año y ayudan a formular preguntas, no a atribuir efecto a una OC o acción PME.”

### 10. Lo que impide medir buen uso (1:00)
**En pantalla:** estimación PME ≠ OC ≠ pago ≠ recepción ≠ uso; “sin antecedente” no significa cero.
**Decir:** “Las fuentes actuales cubren distintos eslabones. Para seguir una operación necesitamos rendición, factura, pago, recepción y beneficiario. El dato ausente se reporta como pendiente.”

### 11. KPI que faltan para evaluar (1:15)
**En pantalla:** cobertura de rendición; gasto rechazado firme / rendido; trazabilidad completa de operación; costo por entrega útil.
**Decir:** “Estas métricas son propuestas, no resultados. Requieren documentos que aún no tenemos. Solo cuando podamos vincular pago, entrega y uso podremos hablar con fundamento de eficiencia.”

### 12. Rúbrica de cuatro categorías (1:15)
**En pantalla:** legítimo y bien utilizado; legítimo pero aparentemente ineficiente; difícil de justificar; potencialmente irregular; estado previo “sin evidencia suficiente”.
**Decir:** “No hemos clasificado ninguna acción ni OC. La etiqueta necesita una operación concreta y evidencia del propósito, legalidad, pago, entrega y uso. SIMCE posterior, por sí solo, no decide ninguna categoría.”

### 13. Conclusión y siguiente paso (1:15)
**En pantalla:** hallazgo: trazabilidad incompleta; próximo paso: rendiciones, materia PAS, facturas/pagos/recepción de casos seleccionados; pregunta para el profesor.
**Decir:** “El aporte actual es un mapa verificable de registros y vacíos. Pediremos primero datos agregados de rendición y expedientes para clasificar los PAS; después examinaremos operaciones focalizadas, incluyendo algunos casos sin señal para controlar falsas alarmas. Queremos feedback sobre el umbral de evidencia para la clasificación.”

### 14. Fuentes y trazabilidad (respaldo, sin tiempo asignado)
**En pantalla:** Mineduc, Superintendencia, Agencia de Calidad, ChileCompra y archivos de cálculo.
**Usar:** dejar visible durante preguntas; las URLs y versiones se detallan en las notas de la presentación y en esta guía.

**Tiempo objetivo de las 13 diapositivas principales:** 14:30–15:00. Si se acorta, reducir ejemplos de fuentes en las diapositivas 4 y 9; no suprimir la diferencia entre estimación, orden y pago.

## 9. Preguntas esperables del profesor

- **“¿Por qué 1.034 OC no son gasto?”** Una OC registra una solicitud o compromiso de adquisición. Los montos de órdenes aceptadas o con recepción conforme no demuestran pago; se necesita comprobante de factura y egreso.
- **“¿Qué significa una acción PME completa?”** Es el tramo de implementación registrado en la plataforma PME. No equivale a compra completada ni a objetivo educativo logrado.
- **“¿Por qué no concluyen malgasto de los PAS?”** La base publicada no incluye materia de cargos. La sanción de primera instancia puede cambiar y su multa no es un monto de gasto objetado.
- **“¿Por qué no comparan directamente privados y públicos?”** La compra pública deja OC en ChileCompra; las adquisiciones propias de particulares subvencionados no tienen el mismo rastro público. Primero se necesitan rendiciones comparables, con la misma unidad y período.
- **“¿Por qué SIMCE no demuestra eficacia del gasto?”** Falta identificar qué estudiantes estuvieron expuestos, a qué intervención, durante cuánto tiempo y frente a qué grupo comparable. Además cambian grados, cohortes y versiones de las bases.
- **“¿Qué significan los ceros?”** Cero OC vinculadas significa ninguna coincidencia inequívoca en nuestra selección. Cero de `ESTIM_TOTAL` es una estimación declarada. Ninguno significa gasto o beneficio nulo.

## 10. Mapa de respaldos, sin guías paralelas

| Necesidad | Archivo que se conserva como respaldo |
|---|---|
| Cifras y método completos | [Análisis principal](informes/Analisis_La_Cisterna_2022_2025.md) |
| Diseño de fases y KPI futuros | [Plan de investigación](informes/Plan_investigacion_La_Cisterna.md) |
| Umbral para clasificar gasto | [Marco documental](informes/Marco_evaluacion_gasto.md) |
| Censo nominal de 2025 | [Universo 2025](informes/Universo_2025.md) |
| Cobertura y versiones de SIMCE/IDPS | [Cobertura de Agencia](informes/Cobertura_Agencia_2023_2025.md) |
| Pedidos de información aún sin enviar | [Solicitudes documentales](informes/Solicitudes_documentales_La_Cisterna.md) |
| Procedencia y significado de columnas | [Diccionario](datos/DICCIONARIO.md) y [manifiestos](datos/procesados/la_cisterna/manifiesto_chilecompra.json) |

Los resúmenes antiguos de EDA y la guía breve son accesos a esta guía única. Las fuentes oficiales de [Mineduc PME](https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/), [ChileCompra](https://datos-abiertos.chilecompra.cl/descargas) y [Agencia de Calidad](https://informacionestadistica.agenciaeducacion.cl/) sostienen las definiciones externas; las cifras locales provienen de los archivos procesados enlazados arriba.
