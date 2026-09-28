# Cómo se usan los recursos escolares en La Cisterna

**Anexo de diseño.** La [guía unificada](../GUIA_UNIFICADA_LA_CISTERNA.md) presenta el avance actual; el [análisis principal](Analisis_La_Cisterna_2022_2025.md) contiene los resultados. Este plan conserva las decisiones y preguntas para las siguientes fases.

**Diseño de estudio: 25 de septiembre de 2026; avance acotado actualizado el 27.** La unidad territorial es La Cisterna. El estudio completo comprende a todos los establecimientos públicos y particulares subvencionados que funcionan con matrícula, y sigue a cada RBD en el tiempo. **Para la entrega del martes 29-09, la nueva recolección se limita a los ocho públicos**; los particulares subvencionados permanecen como contexto ya incorporado y siguiente fase documental. La pregunta rectora es: **¿qué se puede comprobar sobre el uso de los recursos públicos destinados a estos colegios?** Las preguntas operativas son qué recibieron y rindieron, qué gastos fueron observados o rechazados, qué pasó tras la fiscalización y qué entrega o servicio se pudo verificar.

## 1. Punto de partida comprobado

El [Directorio Oficial 2025 del Mineduc](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/) registra **59 establecimientos** de estas dos dependencias funcionando con matrícula en La Cisterna: **8 del SLEP Santa Rosa y 51 particulares subvencionados**. Entre los particulares subvencionados, **34** imparten básica o media y **17** educación especial. Los ocho públicos imparten básica o media. El [listado de los 59 RBD](Universo_2025.md) permite revisar cada inclusión. El panel anual reconstruido identifica **60 RBD en 2022 y 2023, y 59 en 2024 y 2025**; RBD 9830 solo aparece en los dos primeros años. En 2024 los ocho públicos eran **municipales DAEM** y en 2025 el directorio los clasifica como **SLEP**. Las escuelas de educación especial permanecen en el censo financiero y de fiscalización, pero se analizan con indicadores adecuados a su oferta.

El censo es anual: una escuela cerrada, en receso o sin matrícula no entra al denominador de ese año. Una escuela que abrió, cerró o cambió de sostenedor se registra en el período correspondiente. El RBD identifica al establecimiento; el RUT del sostenedor permite examinar gastos centralizados sin atribuirlos automáticamente a una escuela. El establecimiento de administración delegada RBD **9860** aparece en el directorio, pero es una dependencia distinta y se deja documentado como posible ampliación, fuera de los dos grupos pedidos.

## 2. Ventana histórica y preguntas por fuente

| Capa | Período de trabajo | Unidad | Qué responde | Estado de acceso |
|---|---|---|---|---|
| Directorio Mineduc | 2022–2025, cuatro archivos incorporados | RBD–año | Quién funcionó, dependencia, oferta y matrícula | Censo anual 60/60/59/59; [análisis reproducible](Analisis_La_Cisterna_2022_2025.md). |
| Rendición Superintendencia | **2022–2025**, máximo cuatro ejercicios; 2025 sujeto a disponibilidad y cierre | RBD–año–subvención–cuenta | Ingreso, gasto declarado, saldo, gasto aceptado/rechazado y reintegro | La Superintendencia describe estados de resultados y libros a nivel RBD. No se verificó descarga pública íntegra de esas transacciones; [solicitud preparada](Solicitudes_documentales_La_Cisterna.md). |
| Procesos administrativos Superintendencia | **2022–2025**, por año del archivo descargado | PA_ID y RBD | Proceso, sanción, reclamación y estado | Descargas oficiales [2022–2025](https://www.supereduc.cl/pas/) incorporadas; año de ingreso o término se conserva aparte. |
| Agencia de Calidad | **2023–2025**, solo grados y pruebas efectivamente aplicados | RBD–año–grado–área o indicador | SIMCE, IDPS, variación significativa y grupo socioeconómico | [Bases públicas](https://informacionestadistica.agenciaeducacion.cl/) ya descargadas y cruzadas; [cobertura y versiones](Cobertura_Agencia_2023_2025.md). |
| PME y contexto Mineduc | **2022–2025**, según disponibilidad | RBD–año–acción; asistencia y matrícula | Objetivos, recursos estimados, implementación declarada y población atendida | [PME](https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/) y [Datos Abiertos Mineduc](https://datosabiertos.mineduc.cl/). |
| ChileCompra OC, avance público | 2022–2024 municipio; 2025 SLEP | `codigoOC`, con vínculo a RBD solo si es único | Bien o servicio solicitado, monto de orden, estado y modalidad | [1.034 OC seleccionadas y cobertura](../datos/procesados/la_cisterna/oc_cobertura_anual.csv). No acredita pago; el SLEP cubre cinco comunas. |

Cuatro años permiten observar repetición y el cambio de administración pública en 2025 sin almacenar una década de expedientes. El [documento técnico de la Superintendencia](https://s3.us-east-1.amazonaws.com/documentos.anid.cl/investigacion-aplicada/2025/DesafiosPublicos/Guia_tecnica_Superintendencia_Educacion.pdf) describe estados de resultados por RBD, subvención y cuenta, además de libros de compras con montos declarados, rechazados o aceptados; allí su disponibilidad interna se informa hasta 2024. Por eso **2025 se solicitará y usará solo si está cerrado y disponible**, sin inventar un cero. Los procesos administrativos de 2022–2025 sí están publicados por separado.

## 3. La investigación en dos pasadas

**Primera pasada: censo anual de 60/60/59/59 establecimientos.** Para cada RBD y año, reunir ingresos por fuente (general, SEP, PIE y otras), gastos rendidos por cuenta, saldos y su acreditación, PME, matrícula y asistencia. Separar el financiamiento público de aportes privados cuando aparezcan. Los resultados SIMCE e IDPS de 2023–2025 ya están cruzados por grado y RBD; se usarán para establecimientos de básica/media regular solo cuando exista un resultado publicado. En 2025 son 42 regulares y 17 de educación especial; estos últimos requieren indicadores pertinentes sin rellenar SIMCE ausente como cero. Los procesos de Superintendencia se conservan por `PA_ID` y `RBD`, con fechas, instancia y reclamaciones. La lista de casos debe distinguir ausencia de proceso publicado de ausencia de fiscalización.

**Segunda pasada: expedientes concretos.** Elegir casos con gasto rechazado, reintegro ordenado, saldos no acreditados, anomalías persistentes de rendición o una brecha verificable entre compra, entrega y uso. Revisar acto fiscalizador, descargos, resolución y seguimiento. Solicitar primero documentos agregados para el censo anual y libros/facturas solo de las operaciones seleccionadas: contiene el volumen de datos y permite comprobar montos. Incluir ejemplos sin hallazgo para evaluar si la regla de selección produce falsas alarmas. Los procesos por convivencia, seguridad u otras materias se etiquetan como tales y no se suman como «malgasto».

**Resultado esperado:** una ficha por establecimiento y año que muestre `ingreso recibido → gasto rendido → gasto aceptado/rechazado → saldo/reintegro → compra/servicio comprobado → resultado educativo pertinente`. Cada flecha requiere evidencia. Si falta una, la ficha indica «sin antecedente» y la pregunta documental pendiente. El tablero territorial mostrará cobertura por dependencia y año antes de cualquier comparación.

## 4. Indicadores y reglas de interpretación

| Indicador | Fórmula o registro | Lectura válida |
|---|---|---|
| Cobertura | RBD con dato / RBD elegibles del año, por dependencia y fuente | Mide cuánto sabemos; evita tratar faltantes como cero. |
| Gasto por estudiante | Gasto rendido de un ejercicio / matrícula o asistencia del mismo ejercicio, con nivel y fuente explícitos | Describe magnitud. Ajustar por oferta, tamaño y composición; no es un ranking de eficiencia por sí solo. |
| Gasto observado | Monto expresamente no aceptado o sujeto a reintegro en acto oficial, con fecha y estado | Mantener separado de gasto rendido y de pérdida definitiva. |
| Saldos | Saldo inicial + ingresos – gastos y ajustes = saldo final; comprobar acreditación | Un saldo sin ejecutar puede trasladarse al año siguiente. No es despilfarro por definición. |
| Brecha de ejecución | Objetivo PME y monto estimado frente a rendición, factura, recepción y uso | El PME registra estimaciones declaradas, no pagos ni aprobación del gasto. |
| Resultado educativo | SIMCE/IDPS del mismo grado y área, significancia, contexto y tamaño de cohorte | Ayuda a formular preguntas; una baja de puntaje no prueba mal uso de recursos. |

Para comparar sostenedores, mantener separadas las modalidades de básica, media técnico profesional, educación de adultos y especial. Usar el gasto del año correspondiente y valores reales cuando se comparen pesos entre años. En 2025 separar la administración pública del SLEP de la etapa municipal anterior. Los contratos de la administración central se asignan a un RBD solo si los antecedentes identifican al beneficiario y el monto.

## 5. Primer cruce real con la Superintendencia

Los archivos oficiales de [procesos administrativos sancionatorios](https://www.supereduc.cl/pas/) de 2022–2025 contienen **110 procesos** asociados a **39 RBD** del censo: 21 filas en el archivo 2022, 39 en 2023, 31 en 2024 y 19 en 2025. En la primera instancia se registran **47 multas** y **ninguna orden de reintegro** en este subconjunto. De los 110, **20 figuran pendientes de segunda instancia y uno en la corte**. Las multas están expresadas en **UTM** según el [diccionario oficial](https://www.supereduc.cl/pas/), no en pesos. El año del archivo se conserva distinto del año de ingreso y del término del proceso. El campo de dependencia de algunos procesos de 2025 todavía dice «Municipal DAEM» para RBD transferidos al SLEP, por lo que prevalece el directorio del año para el panel escolar y se conserva el valor original del expediente.

Este cruce **no responde todavía cuánto se malgastó**. Un proceso puede tratar convivencia u otra materia; el archivo no contiene el detalle del gasto imputado ni prueba que el establecimiento recibiera o usara mal un recurso. Una multa tampoco equivale al monto de recursos mal utilizados. El [extracto con identificador, estado y fila original](../datos/procesados/procesos_supereduc_la_cisterna_2022_2025.json) sirve para seleccionar y pedir expedientes sin repetir procesos.

La [revisión de los 110 PAS](../datos/procesados/la_cisterna/pas_revision_materia.csv) confirma que ni el extracto ni los XLSX originales incluyen materia de cargos. Todos quedan como `sin_antecedente_en_base_pas` para los motivos “rendición de cuentas” y “uso de subvención”; no se puede convertir eso en cero casos. El avance de [ChileCompra](Analisis_La_Cisterna_2022_2025.md#avance-de-compras-públicas-ficha-comprador-y-cruces) sí deja OC deduplicadas, 637 vínculos escolares únicos y un flag de trato directo, pero el valor de la orden tampoco es gasto pagado. La Ficha Comprador se mide por organismo completo en ventanas recientes, no por RBD ni retrospectivamente para 2022–2025. En el índice público de casos del Observatorio no hubo coincidencia textual para los dos compradores al 27-09-2026.

**Asimetría de trazabilidad:** las compras de los sostenedores particulares subvencionados no dejan por regla general la misma huella pública de OC y Ficha Comprador que las entidades estatales. Sí rinden subvenciones a la Superintendencia; en este avance no se verificó acceso público reutilizable al detalle transaccional por RBD. Por eso la solicitud documental preparada, aún sin enviar, es el siguiente paso para la comparación completa. PAS y PME no rellenan esa brecha.

## 6. Criterio para afirmar un hallazgo

1. **Señal:** dato atípico, denuncia o proceso. Solo activa revisión.
2. **Observación documentada:** acto oficial identifica hecho, RBD/sostenedor, período y monto; se incorporan descargos.
3. **Resultado administrativo:** resolución y reclamaciones establecen qué gasto se rechazó, qué se reintegró y qué sigue pendiente.
4. **Efecto material:** documentos de pago, recepción, inventario o prestación muestran si el recurso llegó y se utilizó.

Publicar cada nivel con su fecha. «Gasto rendido», «gasto no aceptado», «multa», «reintegro» y «pérdida» son medidas distintas. La conclusión sobre uso indebido exige al menos los niveles 2 y 3; la afirmación de recurso efectivamente desaprovechado exige además pruebas de entrega y uso. Los resultados académicos ayudan a contextualizar, no reemplazan esos documentos.

## 7. Próximas operaciones

1. Revisar cambios del censo anual y elegibilidad por grado y subvención; la extracción 2022–2025 ya está completa.
2. Verificar si la Agencia publicó versiones finales para los archivos aún marcados como preliminares; mantener la versión extraída hasta entonces.
3. Obtener los estados de resultados del censo anual para 2022–2024 y consultar 2025; registrar gasto declarado frente a aceptado y saldo acreditado.
4. Obtener actas y resoluciones para clasificar materia de los 110 PAS; la base publicada no contiene los motivos específicos. Solicitar expedientes y libros de compras de un subconjunto definido por evidencia financiera.
5. Construir el tablero con una vista de cobertura antes de los hallazgos, y auditar manualmente cada caso que se quiera describir públicamente.
