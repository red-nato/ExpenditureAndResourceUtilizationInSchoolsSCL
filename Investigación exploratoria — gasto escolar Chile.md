# Investigación exploratoria: recursos públicos y uso educativo en colegios de Chile

**Fecha de revisión:** 23 de septiembre de 2026. **Propósito:** propuesta verificable para la primera entrega de Business Intelligence (BI). No se ha calculado todavía un ranking ni se ha comprobado un caso de despilfarro.

## 1. Propuesta para presentar

**Título de trabajo:** *Public Education Expenditure and Resource Utilization in Chile: A Pilot Study of State-Funded Schools in La Cisterna.* La Cisterna es el piloto, no una restricción definitiva. En español: *Trazabilidad del gasto público y uso de recursos educativos: piloto en establecimientos subvencionados de La Cisterna*.

**Pregunta:** *To what extent do public resources allocated to state-funded schools correspond to their stated educational objectives, actual expenditure, utilization, and educational outcomes?*

**Aporte BI de la primera entrega:** construir un mapa de datos y un tablero que siga la secuencia **asignación → ingreso recibido → plan PME → gasto rendido → compra/pago → entrega → uso → resultado**, dejando visible dónde faltan pruebas. La evaluación de las cuatro categorías se define por partida pagada, con un estado previo «pendiente de clasificación» cuando faltan pruebas. Véase el [marco de evaluación](informes/Marco_evaluacion_gasto.md). El tablero debe ayudar a priorizar preguntas, no clasificar escuelas como “corruptas”.

**Unidad de análisis recomendada:** (a) establecimiento–año–tipo de subvención para ingresos y rendiciones; (b) partida pagada de compra/contrato, fondo, período y sus beneficiarios para adquisiciones; (c) acción PME–año para objetivos; (d) establecimiento–grado–asignatura–año para SIMCE. El **RBD** es la llave escolar, pero **no suele venir en las compras de Mercado Público**: ese enlace requiere documentación y, a menudo, revisión humana. Tampoco se debe atribuir automáticamente un gasto de la administración central a cada RBD.

### Alcance inicial

El SLEP Santa Rosa enumera **ocho** establecimientos escolares de La Cisterna: Colegio Antu, Colegio Naciones Unidas, Colegio Palestino, Escuela Esperanza Joven, Escuela Óscar Encalada, Liceo Ciencia y Tecnología, Liceo Olof Palme y Liceo Portal La Cisterna. Se deben confirmar sus RBD y estado de funcionamiento en el **Directorio Oficial del año analizado**, antes de unir bases; los nombres y direcciones pueden cambiar. [Listado del SLEP Santa Rosa](https://slepsantarosa.gob.cl/establecimientos-educacionales-2/), [Centro de Estudios Mineduc](https://datosabiertos.mineduc.cl/).

| Establecimiento público de La Cisterna | RBD de referencia |
|---|---:|
| Liceo Politécnico Ciencia y Tecnología | 9693 |
| Colegio Naciones Unidas | 9699 |
| Colegio Palestino | 9700 |
| Liceo Polivalente Olof Palme | 9701 |
| Escuela Esperanza Joven | 9703 |
| Escuela Óscar Encalada | 9706 |
| Liceo Portal La Cisterna | 9722 |
| Colegio Antu/Antü | 9730 |

Los RBD aparecen en las fichas del [Plan Anual Local 2026 del SLEP Santa Rosa](https://educacionpublica.gob.cl/wp-content/uploads/2026/01/REX-PAL-Santa-Rosa.pdf), y el 9693 se confirma además en la [ficha MIME del Liceo Ciencia y Tecnología](https://mi.mineduc.cl/mvc/mime/ficha?rbd=9693). Esta tabla es el punto de partida; la dependencia y matrícula deben tomarse del directorio/año correspondiente.

El traspaso de estos establecimientos desde la administración municipal al SLEP fue **el 1 de enero de 2025**. Por tanto, separar compras y rendiciones **hasta 2024** (municipio/corporación, según corresponda) y **desde 2025** (SLEP); revisar además contratos celebrados antes del traspaso y pagados o ejecutados después. Comparar 2024 con 2025 como si el sostenedor y sus procesos fueran idénticos induciría errores. [Cuenta Pública de la DEP](https://educacionpublica.gob.cl/wp-content/uploads/2025/07/Cuenta-Publica-2025-baja.pdf), [SLEP Santa Rosa](https://slepsantarosa.gob.cl/direccion-educacion-publica/emotiva-ceremonia-de-traspaso-de-los-establecimientos-educacionales-al-slep-santa-rosa/).

## 2. Correcciones al archivo de contexto

| Afirmación o enfoque anterior | Corrección para el proyecto |
|---|---|
| “PME = contrato/autoridad que aprueba el gasto” | El PME contiene acciones y montos **estimados y declarados**. Mineduc advierte expresamente que publicarlos **no significa aprobación ministerial ni aceptación del gasto por la Superintendencia**. La implementación reportada tampoco equivale necesariamente al desembolso rendido. [Advertencia oficial y bases PME](https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/). |
| “Las 350 licencias de antivirus son un posible gasto SEP escolar” | La licitación **2767-66-LE22** es de la Municipalidad de La Cisterna, se refiere a equipos institucionales y figura **desierta**. No prueba una compra, un pago ni un destino escolar. El ejemplo debe retirarse como hallazgo. [Ficha oficial](https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=2767-66-LE22). |
| “Toda compra municipal de educación se paga con SEP” | La licitación de tablets/conectividad para Liceo Portal y Colegio Antu indica **FAEP 2020 para tablets y SEP para componentes de internet**. Hay que separar partida, establecimiento y pago efectivo. El monto en la licitación es **presupuesto estimado**, no gasto ejecutado. [Ficha oficial](https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=3bk8fNG4Hv5pbl48w6ybYQ%3D%3D). |
| “La OC de 30 licencias Microsoft 365 A3 es gasto SEP de un colegio” | La [OC por $1.717.099](https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?qs=MJUckcBH3GIu%2FFRfBcuRJA%3D%3D) identifica al comprador municipal y las 30 licencias, pero el extracto público revisado **no acredita RBD, fuente de financiamiento, pago ni uso**. Es un candidato para solicitar respaldos, no un caso probado. |
| “La Cisterna tiene cuatro colegios a estudiar” | El SLEP lista ocho públicos; además existen particulares subvencionados. Seleccionar cuatro sólo tras medir cobertura de datos. Mercado Público sirve para el municipio y SLEP, pero **no es un censo de compras de sostenedores privados**. [SLEP](https://slepsantarosa.gob.cl/establecimientos-educacionales-2/), [ChileCompra](https://www.chilecompra.cl/api/). |
| “Un aumento de gasto seguido de SIMCE bajo demuestra despilfarro” | No demuestra causalidad: cambian cohortes, asistencia, vulnerabilidad, tamaño de muestra y metas del gasto. SIMCE es sólo uno de los resultados posibles; para licencias o infraestructura importa primero la entrega y el uso. [Bases y llaves de la Agencia](https://informacionestadistica.agenciaeducacion.cl/anexos/Anexo1_BBDD_ACE_publico.pdf). |

## 3. Cómo se financia: subvención general y SEP

**Subvención general de escolaridad:** el DFL N.º 2 de 1998 fija en su artículo 9 valores unitarios mensuales en **USE**, diferenciados por nivel/modalidad y condiciones como jornada; el artículo 13 usa la **asistencia media promedio de los tres meses anteriores** para el cálculo mensual, con reglas especiales para meses sin clases o inicio del año escolar. Por eso `matrícula × tarifa × 12` **no reproduce** los pagos reales. Existen además aportes distintos de la subvención base (por ejemplo, mantenimiento, gratuidad, PIE, SEP); deben identificarse por separado. [DFL N.º 2, texto vigente](https://www.bcn.cl/leychile/navegar?idNorma=127911), [tabla oficial de otros valores y USE](https://www.comunidadescolar.cl/wp-content/uploads/2026/03/otros-valores-subvenciones-DICIEMBRE-2025-ley21806-Reaj-200-2.pdf).

**SEP:** Ley N.º 20.248. Requiere convenio del sostenedor; atiende a estudiantes **prioritarios** y **preferentes** en niveles habilitados. La condición se determina por Mineduc; un estudiante preferente no es prioritario. El valor unitario del preferente es **la mitad** del prioritario, no una segunda subvención sumada por el mismo alumno. Se agrega, cuando corresponde, una **subvención por concentración de alumnos prioritarios**, calculada según el tramo de concentración del establecimiento y la asistencia promedio de *todos* los alumnos de los niveles correspondientes. Los arts. 14, 14 bis, 15 y 16 de la ley distinguen estas piezas y la asistencia de los tres meses precedentes. [Ley SEP](https://www.bcn.cl/leychile/navegar?idNorma=269001), [evaluación DIPRES](https://www.dipres.gob.cl/597/articles-308400_informe_final.pdf).

**Esquema de cálculo mensual para entender, no para reemplazar la liquidación oficial:**

```text
SEP base estimada (mes m, RBD r)
  = USE(m) × Σ_niveles [f_prioritario(n, categoría_r) × AMP_prioritarios(r,n,m)
                        + f_preferente(n, categoría_r) × AMP_preferentes(r,n,m)]

SEP concentración estimada
  = USE(m) × Σ_niveles [f_concentración(n, tramo_r) × AMP_total(r,n,m)]

AMP = asistencia media promedio legal de los tres meses precedentes.
Total a contrastar = SEP base + concentración + ajustes/reliquidaciones que figuren en pago real.
```

La tabla oficial publicada con **USE de $35.798,0316 a diciembre de 2025** muestra para alumnado **prioritario**: categoría autónomo, **2,0328 USE** desde 1.º nivel de transición hasta 6.º básico y **1,3548 USE** de 7.º básico a 4.º medio; categoría emergente, **1,0164** y **0,6774 USE**, respectivamente. El preferente recibe la mitad. El incremento por concentración va de **0,118 a 0,302 USE** para NT1–6.º básico y **0,078 a 0,202 USE** para 7.º básico–4.º medio, según tramos de 15% a 60% o más. El ejemplo de pesos de diciembre de 2025 **no debe aplicarse a todos los meses ni a 2026**: cambia la USE y pueden existir reajustes y reliquidaciones. [Tabla oficial, pág. 2](https://www.comunidadescolar.cl/wp-content/uploads/2026/03/otros-valores-subvenciones-DICIEMBRE-2025-ley21806-Reaj-200-2.pdf).

**Ejemplo pedagógico:** para 100 alumnos prioritarios de 4.º básico con asistencia media promedio de 90, en categoría autónomo, sólo el componente base hipotético de diciembre de 2025 sería `90 × 2,0328 × 35.798,0316 ≈ $6.549.321`. No incluye preferentes, concentración, otros cursos ni ajustes. Para presentar cifras reales, usar las **liquidaciones de subvenciones pagadas** y la base de alumnos beneficiarios del mismo año, no esta simulación.

**Destino y rendición:** el sostenedor debe vincular los recursos SEP con el convenio y PME, rendir ingresos/gastos y acreditar saldos. La Superintendencia puede **no aceptar** un gasto tras fiscalizar; un gasto “rendido” no es necesariamente un gasto “aceptado”. Tampoco todo saldo de un año es despilfarro: puede trasladarse al año siguiente, sujeto a reglas y acreditación. [Ayuda Mineduc: rendición SEP](https://www.ayudamineduc.cl/ficha/rendicion-de-cuentas-sep), [guía técnica de la Superintendencia](https://s3.us-east-1.amazonaws.com/documentos.anid.cl/investigacion-aplicada/2025/DesafiosPublicos/Guia_tecnica_Superintendencia_Educacion.pdf), [Portal de Transparencia Financiera](https://ptf.supereduc.cl/).

## 4. Inventario de fuentes y qué permite afirmar cada una

| Fuente oficial | Datos útiles / llave | Acceso y límite para el análisis |
|---|---|---|
| [Centro de Estudios Mineduc — Datos Abiertos](https://datosabiertos.mineduc.cl/) | Directorio de establecimientos y sostenedores; matrícula por RBD y nivel; asistencia; resumen de alumnos prioritarios, preferentes y beneficiarios SEP; subvenciones. | Descargar **diccionarios y año específico**, registrar fecha de extracción. Verificar si la serie de subvenciones es pago mensual, devengo o agregado antes de usarla como “ingreso recibido”. El [Centro de Estudios enumera explícitamente directorios, matrícula y asistencia](https://centroestudios.mineduc.cl/2024/11/19/novedades-en-datosabiertos-bases-de-datos-y-nueva-seccion-de-indicadores/). |
| [PME, planificación e implementación](https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/) | Acciones, dimensiones, indicadores, montos planificados y reporte de implementación por establecimiento desde 2023. | Descarga pública. Son **declaraciones y estimaciones**; no incluyen, por sí solas, factura, pago ni aceptación normativa. En septiembre de 2026 constan planificación 2026 e implementación 2025. |
| [Superintendencia: PTF y manuales](https://ptf.supereduc.cl/) | Rendición anual por RBD/subvención/cuenta; ingresos, gastos, saldos, libros de compras/honorarios/remuneraciones; fiscalización y montos no aceptados. | El organismo dispone de estos registros, pero **no se verificó una descarga pública masiva de transacciones RBD–factura**. Obtener los estados, libros y resoluciones por solicitudes de acceso; no presumir que toda la base interna está abierta. La [guía técnica oficial](https://s3.us-east-1.amazonaws.com/documentos.anid.cl/investigacion-aplicada/2025/DesafiosPublicos/Guia_tecnica_Superintendencia_Educacion.pdf) describe estructura y período disponible internamente. |
| [ChileCompra: descargas](https://datos-abiertos.chilecompra.cl/descargas) y [API](https://www.chilecompra.cl/api/) | Licitaciones, ofertas, adjudicaciones, órdenes de compra, contratos, comprador, proveedor, ítem y precio. | Cobertura de organismos que compran por la plataforma. La API requiere **ticket**; las descargas permiten explorar sin programar. Una licitación u OC no acredita por sí sola pago, imputación SEP ni uso. No hay llave RBD universal. |
| [DIPRES: ejecución del SLEP Santa Rosa](https://www.dipres.gob.cl/597/w3-multipropertyvalues-25916-37782.html) | Presupuesto y ejecución por capítulo/subtítulo para el servicio. | Agregado **SLEP**, no gasto de un colegio ni exclusivamente SEP. Sirve para contextualizar y conciliar, no dividir sin criterio entre sus escuelas. La [evaluación SEP 2017–2021](https://www.dipres.gob.cl/597/articles-308400_informe_final.pdf) ofrece metodología y categorías históricas, no la cifra local actual. |
| [Agencia de Calidad: SIMCE/IDPS](https://informacionestadistica.agenciaeducacion.cl/) | Resultado por RBD, año, grado y asignatura; IDPS. | La [ficha de bases públicas](https://informacionestadistica.agenciaeducacion.cl/anexos/Anexo1_BBDD_ACE_publico.pdf) documenta llaves y cobertura. Comparar sólo mismo grado/asignatura y atender supresión, significancia y cambios de cohorte. No usar puntaje como prueba directa de una compra. |
| [Mineduc: rendimiento y asistencia](https://datosabiertos.mineduc.cl/) | Aprobación, repitencia, retiro/desvinculación y asistencia por RBD y año. | Resultados intermedios a menudo más pertinentes que SIMCE para iniciativas de retención o convivencia. Mantener las definiciones del año y del nivel. |
| [DEP / SLEP Santa Rosa](https://educacionpublica.gob.cl/wp-content/uploads/2026/01/REX-PAL-Santa-Rosa.pdf) | Plan Estratégico Local (PEL), Plan Anual Local (PAL), metas y seguimiento territorial. | Objetivos de nivel **servicio**, no sustituyen el PME de cada escuela. El PAL 2026 también ofrece contexto presupuestario del SLEP. |
| [Contraloría: búsqueda pública](https://transparencia.contraloria.cl/search) | Informes de auditoría, observaciones, seguimiento. | Buscar institución, período, número de informe y **estado final** de la observación. Cobertura más directa del gasto de organismos públicos; complementar con la Superintendencia en todos los sostenedores. |
| [Portal de Transparencia](https://www.portaltransparencia.cl/) | Solicitudes de actos, rendiciones, contratos, facturas y antecedentes de uso al SLEP, municipio y organismos competentes. | Para sostenedores privados la vía más sólida puede ser solicitar a **Mineduc/Superintendencia** los documentos que obran en su poder; el portal no convierte automáticamente al particular subvencionado en organismo público. Solicitar registros existentes, períodos y RBD concretos. |
| [JUNAEB](https://bibliotecadatos.sead.junaeb.cl/) | Vulnerabilidad y programas de apoyo, según base disponible. | Contexto de comparabilidad; **IVE no equivale** al porcentaje SEP prioritario. Alimentación escolar es otro flujo y no se debe sumar mecánicamente al gasto SEP de un colegio. [Explicación oficial de IVE/PAE](https://capacita.junaeb.cl/encargadopae/herramientas-pae/). |

**Fuentes complementarias para casos:** PEI y cuenta pública del establecimiento (buscar en su sitio y [MIME](https://mi.mineduc.cl/mvc/mime/portada)); PADEM municipal para 2024 y anteriores; inventarios y actas de recepción del SLEP; registro de asistencia a capacitaciones; logs agregados de plataformas (sin datos personales); contratos de asesorías ATE; resoluciones de fiscalización. El portal MIME aún muestra en algunas fichas cifras SEP **2008–2010**: no confundirlas con datos financieros actuales. [Ejemplo de ficha](https://mi.mineduc.cl/mvc/mime/ficha?rbd=5).

## 5. Modelo de datos mínimo y emparejamiento

**Tablas:** `establecimiento_hist` (RBD, nombre, comuna, dependencia, sostenedor, fecha de vigencia), `matricula_asistencia` (RBD, año/mes, nivel, matrícula, asistencia), `beneficiarios_sep` (RBD, año, nivel, prioritarios, preferentes), `transferencias` (RBD, mes, subvención, monto pagado), `rendicion` (RBD o administración central, año, subvención, cuenta, monto declarado/aceptado, saldo), `pme_accion` (RBD, año, ID de acción, objetivo, indicador, presupuesto, estado reportado), `contratacion` (ID licitación/OC, comprador, proveedor, ítems, monto, estado, fuente declarada), `compra_beneficiario` (ID contrato/OC, RBD, porcentaje o monto asignado y documento que lo respalda), `uso` (ID contrato/activo, RBD, período, métrica y documento), `resultado` (RBD, año, grado, asignatura/indicador), `evidencia` (URL, fecha, documento, página, extracción, nivel de certeza).

**Regla de unión:** sólo el directorio, matrícula, SEP, PME, rendición y SIMCE deben intentar enlace automático por `RBD + año` (y nivel donde corresponda). Para ChileCompra: `comprador + ID de compra + texto de bases/anexos + acta de entrega + RBD`. Registrar estados: **confirmado**, **probable**, **sin asignar**, **descartado**. Si una compra sirve a varios colegios, repartir el costo sólo con una regla documentada (cantidad entregada, usuarios, contrato); mantener el total sin repartir cuando no exista. No unir gastos de “administración central SEP” a los colegios mediante una división simple.

**Cadena probatoria de una compra:** `planificación PME` → `fuente de financiamiento identificada` → `contrato/OC adjudicada` → `factura` → `comprobante de pago` → `imputación en rendición` → `recepción conforme/inventario` → `uso verificable` → `indicador pertinente`. Una etapa ausente es **“sin evidencia disponible”**, no “no ocurrió”. Una licitación desierta se descarta como gasto.

## 6. KPIs: empezar por los que realmente se pueden construir

| KPI y fórmula | Nivel / fuente | Qué responde y precaución |
|---|---|---|
| **Ingreso público por estudiante** = transferencias efectivamente pagadas / matrícula media anual | RBD–año; Mineduc. | Escala del financiamiento. Separar SEP, base, PIE, etc.; matrícula de abril puede no representar todo el año. |
| **SEP por beneficiario equivalente** = SEP base pagada / (`prioritarios + 0,5 × preferentes`, promediados por mes/nivel) | RBD–año; Mineduc. | Comparación exploratoria del ingreso SEP. Mantener **concentración separada**, pues beneficia a toda la matrícula y no sigue el mismo denominador. |
| **Ejecución SEP** = gasto SEP rendido / (`saldo inicial SEP + ingresos SEP del año`) | RBD–año; Superintendencia. | Uso financiero de recursos disponibles. Conciliar saldos/ajustes; bajo valor no equivale automáticamente a malgasto. Usar estado de rendición. |
| **Saldo SEP no ejecutado** = saldo final / recursos disponibles | RBD–año; Superintendencia. | Señal para preguntar por retrasos y plan de uso, nunca condena por sí sola. |
| **Gasto SEP por categoría y alumno** = gasto rendido en cuenta / matrícula media | RBD–año–cuenta. | Prioridades financieras. Distinguir remuneraciones, recursos pedagógicos, tecnología y administración central. |
| **Trazabilidad gasto→objetivo** = monto **pagado y conciliado** con acción PME documentada / monto pagado del subconjunto analizado | Compra o muestra auditada. | Calidad de vinculación documental. “No vinculado todavía” no significa gasto improcedente; doble revisión manual. |
| **Entrega comprobada** = unidades con recepción/inventario / unidades pagadas | Compra–RBD. | Brecha de ejecución física. Requiere actas/inventario; en servicios, sustituir por hitos aceptados. |
| **Utilización de licencias** = usuarios activos únicos / licencias contratadas; **intensidad** = usuarios activos mensuales / usuarios habilitados | Contrato–mes–RBD. | Uso real. Definir “activo” (p. ej., al menos un acceso significativo en 30 días), ventana contractual y licencias de reserva. Pedir métricas agregadas. |
| **Costo por usuario activo** = pago del período / usuarios activos del mismo período | Contrato–período. | Más informativo que costo por matrícula para software. No mezclar contratos de diferente duración o soporte. |
| **Precio unitario comparable** = pago neto / unidades equivalentes; desvío = precio propio / mediana de compras comparables − 1 | Compra–producto. | Señal de precio. Normalizar IVA, fecha, cantidad, duración, implementación, garantía y soporte; un desvío no prueba sobreprecio irregular. |
| **Concentración de proveedores** = suma de cuadrados de participaciones de gasto por proveedor (HHI) | Sostenedor–categoría–año. | Dependencia de proveedores. Concentración puede deberse a convenio marco o mercado pequeño; revisar competencia y recurrencia. |
| **Gasto no aceptado firme** = monto no aceptado con resolución firme / gasto fiscalizado | RBD/sostenedor–año fiscalizado. | Hallazgo administrativo real. Si no hubo fiscalización o la resolución está pendiente, mostrar `N/D` y nunca cero. [Definición y advertencia oficial](https://s3.us-east-1.amazonaws.com/documentos.anid.cl/investigacion-aplicada/2025/DesafiosPublicos/Guia_tecnica_Superintendencia_Educacion.pdf). |
| **Indicador de resultado alineado** = cambio del resultado definido en la acción (asistencia, retención, IDPS o SIMCE pertinente) respecto de línea base | RBD–año/curso. | Seguimiento, **sin atribución causal**. Exigir mismo grado/asignatura, período posterior razonable y, de ser posible, comparadores semejantes. |

**Categorías evaluativas:** 1. legítimo y bien utilizado; 2. legítimo pero aparentemente ineficiente; 3. difícil de justificar respecto del objetivo declarado; 4. potencialmente irregular o improcedente. Exigen criterios y evidencia distintos. «Pendiente de clasificación» identifica falta de información y se muestra por separado. El [marco operativo](informes/Marco_evaluacion_gasto.md) define requisitos, prioridad ante señales superpuestas, costos comparables y límites de inferencia. La base PME no permite clasificar licitaciones.

**Disponibilidad del tablero:** KPI financiero y PME con bases públicas/solicitudes; KPIs de entrega y uso **sólo después** de recibir inventarios/logs. Mostrar `N/D`, nunca convertirlo en cero. No publicar un “índice de corrupción” combinado: mezcla falta de acceso, ineficiencia e infracción.

## 7. Primer piloto documental verificable

1. **Equipos PLC y pantallas HMI para el Liceo Ciencia y Tecnología:** la [licitación 2769-10-L124](https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=2769-10-L124) figura adjudicada, identifica seis PLC y seis pantallas HMI para la especialidad de electrónica. Preguntar: monto de OC/pago; fuente contable; fecha/acta de entrega; inventario; docentes capacitados; matrícula de la especialidad; sesiones de laboratorio y uso durante 2025–2026. La ficha **no prueba subutilización**.
2. **Tablets + conectividad para Liceo Portal y Colegio Antu:** la [licitación histórica](https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=3bk8fNG4Hv5pbl48w6ybYQ%3D%3D) nombra ambos establecimientos y combina FAEP con SEP. Separar tablet, línea/datos, meses y RBD; verificar adjudicación, órdenes, facturas, recepción y usuarios efectivos. Este es un buen caso BI precisamente porque muestra el problema de **una compra, dos colegios y dos fondos**.
3. **Licencias Microsoft 365 A3:** la [OC de octubre de 2024](https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?qs=MJUckcBH3GIu%2FFRfBcuRJA%3D%3D) señala 30 unidades por $1.717.099 IVA incluido. Antes de incluirla en el piloto, confirmar destino escolar y fondo. Si no se acredita, clasificarla **sin asignar**, no como SEP.

La [licitación de 350 antivirus](https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=2767-66-LE22) queda como **ejemplo de control de calidad**, porque el estado desierta impide contarla como gasto.

## 8. Elección de comuna y plan de trabajo BI

**Mantener La Cisterna para la primera entrega:** ocho escuelas públicas permiten universo acotado; existen bases PME, Agencia, directorios y compras de dos sostenedores sucesivos. La transición 2025 es interesante, aunque complica series. Ampliar después a las cinco comunas del SLEP Santa Rosa para tener más comparadores bajo el **mismo sostenedor** desde 2025. Pivotear a otra comuna de RM sólo si se verifica mejor acceso a **rendiciones RBD/cuenta, documentos de compras, beneficiario y evidencia de uso**. Una comuna con más compras publicadas pero sin enlace a escuela no es necesariamente mejor. [Territorio del SLEP](https://slepsantarosa.gob.cl/establecimientos-educacionales/).

**Secuencia para la entrega del ramo:**

1. **Universo:** descargar directorio oficial 2023–2025; filtrar comuna, dependencia, RBD y sostenedor por año. Añadir 2026 si existe directorio comparable. Contar faltantes y duplicados.
2. **Panel público reproducible:** unir matrícula, asistencia, beneficiarios SEP, PME y resultados de Agencia por RBD/año. Mostrar montos PME como **planificados/reportados**, nunca como pagos. Incorporar transferencias sólo tras comprobar definición de la base.
3. **Capa financiera:** pedir a Superintendencia estados de resultados por `RBD × año × subvención × cuenta` 2022–2025 y, para 2–3 casos, libro de compras y estado de fiscalización. Pedir al municipio/SLEP facturas, OC, pagos y actas del piloto.
4. **Casos:** asignar manualmente compras a RBD con documento respaldo; evaluar entrega y uso. Calcular costos sólo cuando el denominador esté verificado.
5. **Resultados:** escoger para cada acción PME el indicador que **ella pretendía mover**. Usar SIMCE sólo si el objetivo pedagógico, nivel y plazo lo justifican; acompañar con asistencia, retención o IDPS cuando sean más pertinentes.
6. **Presentación:** tablero con filtros de año, comuna, dependencia, RBD, subvención y categoría; al hacer clic en una anomalía, mostrar cifras, fuentes originales, documentos faltantes y siguiente pregunta de investigación.

**Regla de priorización interna de casos (sin llamarla riesgo de corrupción):** alta prioridad si concurren monto material, beneficiario identificado, brecha comprobable de entrega/uso o precio comparable, y documentos suficientes. Baja prioridad si sólo hay monto planificado, licitación desierta, gasto de administración central sin reparto o RBD no acreditado.

### Solicitudes de información ya delimitadas

- **A la Superintendencia:** “Solicito, en formato reutilizable si existe, estados de resultados y rendiciones 2022–2025 por RBD de los ocho establecimientos públicos de La Cisterna, desagregados por subvención, cuenta contable, ingresos, gastos, saldos y estado de rendición; indicar rectificaciones y gastos no aceptados con su estado de firmeza. Solicito también el diccionario de campos.”
- **Al SLEP y, para 2024, al municipio:** “Para la licitación/OC [ID], solicito contrato, órdenes, facturas, comprobantes de pago, fuente de financiamiento por ítem, RBD beneficiarios, actas de recepción, inventario y documentos existentes de seguimiento de uso. Entregar cantidades agregadas de licencias habilitadas y activas o equipos operativos por mes, sin datos personales.”
- **Si hay PME concreto:** “Para la acción PME [ID, RBD, año], solicito los informes de ejecución/medios de verificación existentes y documentos que relacionen los gastos rendidos con dicha acción.”

Pedir **documentos existentes**, no que la institución produzca una evaluación nueva. Si responde que no posee logs, registrar “sin registro recibido” y buscar evidencia alternativa; no inferir utilización cero. [Portal de Transparencia](https://www.portaltransparencia.cl/).

## 9. Riesgos metodológicos que deben figurar en las diapositivas

- **Asignado ≠ pagado ≠ rendido ≠ aceptado.** Cada término debe tener columna y fecha propia. La rendición y la fiscalización operan con rezago; la [Superintendencia lo describe](https://s3.us-east-1.amazonaws.com/documentos.anid.cl/investigacion-aplicada/2025/DesafiosPublicos/Guia_tecnica_Superintendencia_Educacion.pdf).
- **Comprador ≠ beneficiario.** Municipio/SLEP compra para varias unidades; la descripción de la OC puede no identificar RBD.
- **Gasto nominal ≠ gasto comparable.** Ajustar año monetario con IPC oficial cuando compare períodos, y controlar duración/calidad de compras.
- **Prioritarios SEP ≠ IVE JUNAEB.** Son sistemas y poblaciones con reglas diferentes.
- **Asociación ≠ impacto.** SIMCE puede fluctuar por cambios de cohorte y contexto; mostrar incertidumbre y resultados alternativos.
- **Falta de dato ≠ irregularidad.** Las categorías finales son `confirmado`, `declarado`, `no corroborado`, `descartado` y `pendiente de fiscalización`. Reservar términos de infracción para resoluciones o evidencia suficiente.

**Contraste W1 (25-09-2026):** se compararon dos preguntas con datos reales: custodia de activos observados en Melipeuco e implementación declarada de acciones PME 2024. La primera quedó como preferencia provisional para C1; la segunda aporta controles de cobertura, extremos y diferencias entre dimensiones, pero no evalúa pagos ni uso. El [paquete del workshop](workshop/GROUP_03_W1/report/GROUP_03_W1_Report.pdf) conserva el análisis, los datos reducidos y las preguntas al profesor. Su elección está sujeta al seguimiento documental de bienes.

**Resultado honesto de la primera parte:** un tablero piloto con cobertura y brechas de información, una matriz de fuentes verificadas y uno o dos casos documentales en seguimiento. Eso ya demuestra una pregunta de BI exigente y un método capaz de detectar malgasto más adelante, sin prometer una acusación antes de contar con la evidencia.

### Guion de seis diapositivas para la primera presentación

1. **Problema y pregunta:** por qué importa seguir el dinero hasta su uso, con La Cisterna como piloto.
2. **Sistema de financiamiento:** subvención general, SEP base, preferentes y concentración; pagos según asistencia y USE.
3. **Mapa de fuentes:** qué aporta Mineduc, PME, Superintendencia, ChileCompra, DIPRES y Agencia; dónde se corta el enlace automático.
4. **Modelo BI y KPIs:** RBD como llave escolar, tabla puente manual para compras, métricas financieras y de utilización, `N/D` visible.
5. **Demostración documental:** tablets financiadas con FAEP/SEP o PLC/HMI, mostrando qué está confirmado y qué documento falta.
6. **Siguiente etapa:** obtener rendiciones y pruebas de entrega/uso; seleccionar casos con evidencia suficiente y comparar resultados pertinentes sin afirmar causalidad.
