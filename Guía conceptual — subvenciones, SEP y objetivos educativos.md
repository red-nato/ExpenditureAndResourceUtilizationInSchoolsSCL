# Cómo llega y se usa el dinero público en un colegio chileno

Esta guía sigue **un peso público** desde su cálculo hasta la pregunta que interesa al proyecto: ¿se usó para el propósito educativo declarado? Las fórmulas describen la **regla central** del sistema. Para calcular un pago real se necesita la liquidación del mes: existen excepciones, reajustes y reliquidaciones.

## 1. ¿Quién recibe el dinero?

Un **establecimiento educacional** es la escuela o liceo donde estudian los alumnos. Cada uno tiene un **RBD** (*Rol Base de Datos*), su identificador administrativo. El **sostenedor** es la entidad responsable de administrar el establecimiento y sus recursos; por eso una compra puede aparecer a nombre del sostenedor y beneficiar a varios colegios.

En Chile, un colegio **público** puede estar a cargo de una municipalidad o de un **SLEP** (*Servicio Local de Educación Pública*). Un colegio **particular subvencionado** tiene un sostenedor privado, pero recibe aportes estatales si cumple los requisitos. La Cisterna sirve para ver el cambio: sus establecimientos públicos pasaron de la administración municipal al SLEP Santa Rosa el **1 de enero de 2025**. Al analizar una compra hay que identificar quién era el sostenedor **en la fecha de esa compra**. [Dirección de Educación Pública](https://educacionpublica.gob.cl/wp-content/uploads/2025/07/Cuenta-Publica-2025-baja.pdf).

El Ministerio de Educación (**Mineduc**) establece el marco educativo y administra el sistema de subvenciones. Una **subvención** es un aporte estatal calculado según reglas legales para financiar la educación. No es un monto idéntico para todos los colegios ni una bolsa que la dirección pueda gastar sin rendir. La subvención general y la **SEP** son fuentes distintas, con reglas de cálculo y uso que deben seguirse por separado. [DFL N.º 2 de 1998](https://www.bcn.cl/leychile/navegar?idNorma=127911), [Ley SEP](https://www.bcn.cl/leychile/navegar?idNorma=269001).

## 2. Primero: la subvención general de escolaridad

La subvención general ayuda a financiar el funcionamiento regular del establecimiento. La ley fija un **valor mensual por alumno** que varía según el nivel y modalidad de enseñanza y, cuando corresponde, la **JEC** (*Jornada Escolar Completa*) u otros incrementos legales. Esos valores se expresan en **USE** (*Unidad de Subvención Educacional*): una unidad cuyo valor en pesos puede reajustarse. La ley no paga simplemente por tener estudiantes inscritos; el cálculo ordinario usa su **asistencia media**. [DFL N.º 2, arts. 9 y 13](https://www.bcn.cl/leychile/navegar?idNorma=127911).

Para leer la fórmula, llamemos \(e\) al establecimiento, \(c\) a un curso y \(m\) al mes de pago. La asistencia media de un curso en un mes escolar se puede entender así:

$$
A_{e,c,m}=
\frac{\text{suma de alumnos presentes en los días de clase del mes}}
{\text{número de días de clase del mes}}.
$$

En el régimen ordinario, el pago mensual se basa en el promedio de las asistencias medias de los **tres meses anteriores**. Si \(f^{\mathrm{gen}}_{e,c,m}\) es el factor USE aplicable a ese curso, la idea central es:

$$
\begin{aligned}
\overline A^{(3)}_{e,c,m}
&=\frac{A_{e,c,m-1}+A_{e,c,m-2}+A_{e,c,m-3}}{3},\\[2mm]
G^{\mathrm{gen}}_{e,m}
&\approx \mathrm{USE}_{m}\sum_{c}\left(f^{\mathrm{gen}}_{e,c,m}\,\overline A^{(3)}_{e,c,m}\right).
\end{aligned}
$$

La suma recorre los cursos elegibles. El signo \(\approx\) recuerda que la liquidación puede incluir otros incrementos, descuentos y ajustes. La ley usa reglas especiales para vacaciones, inicio del año escolar y suspensión de clases, y reliquida los primeros meses cuando ya cuenta con la asistencia correspondiente. Por ello, **matrícula × tarifa × 12** no reproduce el ingreso anual efectivo. Si un curso tiene 100 matriculados pero una asistencia media de 80, su base de cálculo ordinaria se aproxima a **80 alumnos asistentes**, no a 100. [DFL N.º 2, art. 13](https://www.bcn.cl/leychile/navegar?idNorma=127911).

## 3. Después: ¿qué añade la SEP?

La **SEP** (*Subvención Escolar Preferencial*, Ley N.º 20.248) agrega recursos para mejorar las oportunidades educativas de estudiantes con mayor vulnerabilidad. El sostenedor debe estar incorporado mediante un **convenio SEP**. Mineduc determina la condición de cada estudiante:

- **Prioritario:** su situación socioeconómica dificulta enfrentar el proceso educativo, según los criterios legales.
- **Preferente:** no es prioritario y cumple el criterio socioeconómico legal para esta categoría. Su valor unitario SEP es **la mitad** del de un prioritario del mismo nivel y categoría de establecimiento.

Un alumno no se cuenta simultáneamente como prioritario y preferente. Tampoco todos los alumnos de un colegio son beneficiarios SEP. [Ley N.º 20.248, arts. 1–4 y 14 bis](https://www.bcn.cl/leychile/navegar?idNorma=269001).

La SEP tiene **dos piezas**. La primera depende de la asistencia media de prioritarios y preferentes. La segunda es un aporte **por concentración de prioritarios**: si su proporción en el establecimiento cae en un tramo legal, se aplica un factor por la asistencia media de **todos los alumnos** de los niveles elegibles. Ese tramo se determina con la proporción de prioritarios del período que fija la ley, por lo que no conviene inferirlo a partir de una sola foto de matrícula. [Ley SEP, arts. 14–16](https://www.bcn.cl/leychile/navegar?idNorma=269001).

Llamemos \(n\) al nivel educativo; \(P_{e,n,m}\), \(F_{e,n,m}\) y \(T_{e,n,m}\) a las asistencias medias promedio de los tres meses anteriores de prioritarios, preferentes y **todos** los alumnos. Si \(s^P_{e,n}\) es el factor SEP del prioritario y \(k_{e,n}\) el factor de concentración que corresponda, entonces:

$$
\begin{aligned}
\mathrm{SEP}^{\mathrm{base}}_{e,m}
&\approx \mathrm{USE}_{m}\sum_n
s^P_{e,n}\left(P_{e,n,m}+\tfrac12 F_{e,n,m}\right),\\[2mm]
\mathrm{SEP}^{\mathrm{conc}}_{e,m}
&\approx \mathrm{USE}_{m}\sum_n k_{e,n}T_{e,n,m},\\[2mm]
\mathrm{SEP}^{\mathrm{total}}_{e,m}
&\approx \mathrm{SEP}^{\mathrm{base}}_{e,m}
+\mathrm{SEP}^{\mathrm{conc}}_{e,m}.
\end{aligned}
$$

Los factores dependen del nivel y de la categoría que corresponda al establecimiento. **Ejemplo de la tabla oficial de diciembre de 2025:** para un prioritario de 1.º nivel de transición a 6.º básico, el factor era **2,0328 USE** en un establecimiento autónomo y **1,0164 USE** en uno emergente; para el preferente, la mitad. La concentración tenía factores distintos según tramo y nivel. Como la USE y las circunstancias del pago pueden cambiar, estos valores sirven para **entender el mecanismo**, no para estimar automáticamente 2026. [Tabla oficial de Mineduc, pág. 2](https://www.comunidadescolar.cl/wp-content/uploads/2026/03/otros-valores-subvenciones-DICIEMBRE-2025-ley21806-Reaj-200-2.pdf).

**Ejemplo ilustrativo completo.** Supongamos un colegio autónomo de básica, 100 alumnos de un nivel elegible, de los cuales 50 son prioritarios y 10 preferentes; la asistencia media promedio es 80% en cada grupo. Si el tramo de concentración aplicable es **45% a menos de 60%**, el factor para ese nivel en diciembre de 2025 es \(0{,}269\) USE. Con \(\mathrm{USE}=\$35.798{,}0316\):

$$
\begin{aligned}
P&=50\times0{,}8=40,\qquad
F=10\times0{,}8=8,\qquad T=100\times0{,}8=80,\\[1mm]
\mathrm{SEP}^{\mathrm{base}}
&=(40\times2{,}0328+8\times1{,}0164)\times\$35.798{,}0316
\approx\$3.201.891,\\[1mm]
\mathrm{SEP}^{\mathrm{conc}}
&=80\times0{,}269\times\$35.798{,}0316
\approx\$770.374,\\[1mm]
\mathrm{SEP}^{\mathrm{total}}&\approx\$3.972.264.
\end{aligned}
$$

Es **una simulación**, no la liquidación de un colegio: supone que ese es el tramo legal aplicable, que la asistencia de cada grupo es 80% y que no hay reliquidaciones. Su utilidad es mostrar por qué **preferentes, concentración y asistencia** cambian el monto.

Hay otros aportes —por ejemplo, **PIE** (*Programa de Integración Escolar*), mantenimiento o aporte de gratuidad— con finalidades y reglas propias. **FAEP** (*Fondo de Apoyo a la Educación Pública*) es otra fuente que puede financiar proyectos de educación pública. Para saber “cuánto recibió un colegio” hay que sumar sólo flujos realmente recibidos, identificando **fuente, período y beneficiario**, sin tratar todo como SEP. [Mineduc: rendición de diversas subvenciones](https://www.ayudamineduc.cl/ficha/rendicion-de-cuentas-sep), [tabla de otras subvenciones](https://www.comunidadescolar.cl/wp-content/uploads/2026/03/otros-valores-subvenciones-DICIEMBRE-2025-ley21806-Reaj-200-2.pdf).

## 4. ¿Qué significa que un colegio declare “objetivos educativos”?

Los objetivos no son una lista de compras. Primero está el **PEI** (*Proyecto Educativo Institucional*): expresa la identidad del establecimiento, su visión, misión, sellos y propósitos formativos. Después viene el **PME** (*Plan de Mejoramiento Educativo*): traduce esos propósitos y el diagnóstico escolar en **objetivos estratégicos, estrategias, acciones e indicadores**. Las acciones pueden referirse a gestión pedagógica, convivencia, liderazgo o gestión de recursos. En la fase anual, el establecimiento planifica acciones, reporta su implementación y las evalúa. El **sostenedor** revisa y aprueba lo registrado en la plataforma PME. [Orientaciones PME 2026, sección 1.6](https://liderazgoeducativo.mineduc.cl/wp-content/uploads/sites/55/2026/01/Orientaciones-PME-2026.pdf), [bases PME](https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/).

Una acción comprensible podría ser: “fortalecer lectura en 4.º básico mediante sesiones semanales y material digital”. Su **objetivo** es mejorar una capacidad; la **acción** describe lo que se hará; el **indicador** debe permitir comprobar ejecución o avance, por ejemplo sesiones realizadas y alumnos participantes. La eventual compra de licencias es **un medio**, no el resultado educativo en sí. Un buen análisis pregunta sucesivamente: ¿estaba contemplada la acción?, ¿se pagó la compra?, ¿llegó el recurso?, ¿se utilizó?, ¿mejoró el indicador pertinente?

Hay una distinción decisiva: el monto escrito en el PME es **planificado o declarado**. Mineduc advierte que publicar el PME **no significa que el ministerio apruebe el gasto ni que la Superintendencia lo acepte en una rendición**. El reporte de “implementada” tampoco reemplaza factura, comprobante de pago o evidencia de uso. [Advertencia oficial de Mineduc](https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/).

## 5. Del objetivo a la rendición y al resultado

El sostenedor informa ingresos y gastos en la **rendición de cuentas** ante la **Superintendencia de Educación**. Esta institución fiscaliza el cumplimiento de las reglas y la **legalidad del uso de los recursos**. La Ley N.º 20.529 dice expresamente que el análisis de la rendición **no juzga el mérito** del uso: un gasto puede cumplir las reglas y, aun así, resultar poco útil. Esa es precisamente una pregunta de eficiencia que nuestro proyecto debe estudiar con evidencia adicional. [Ley N.º 20.529, arts. 48 y 54](https://www.bcn.cl/leychile/navegar?idNorma=1028635), [Mineduc: rendición SEP](https://www.ayudamineduc.cl/ficha/rendicion-de-cuentas-sep).

La rendición obliga a distinguir **flujo** y **saldo**. Los recursos recibidos en un año pueden gastarse ese año o permanecer disponibles para otro, sujetos a las reglas y acreditaciones correspondientes. La relación básica para **cada fuente**, antes de ajustes contables, es:

$$
\text{saldo final}
=\text{saldo inicial}+\text{ingresos recibidos}-\text{gastos pagados}.
$$

Por eso “recibió $X y gastó menos de $X” no demuestra despilfarro; primero hay que revisar el saldo y su destino posterior. Asimismo, **gasto rendido** significa que el sostenedor lo declaró, mientras que **gasto aceptado** significa que superó la revisión que corresponda. [Guía técnica de la Superintendencia](https://s3.us-east-1.amazonaws.com/documentos.anid.cl/investigacion-aplicada/2025/DesafiosPublicos/Guia_tecnica_Superintendencia_Educacion.pdf).

Para una compra pública, **ChileCompra/Mercado Público** puede mostrar licitación, proveedor y **OC** (*orden de compra*). La OC es un **compromiso de compra**, no prueba por sí sola pago o entrega. Después hay que buscar factura, pago, acta de recepción e inventario; para software, cuentas activadas y uso agregado. Los sostenedores particulares subvencionados no quedan representados exhaustivamente por las compras publicadas allí. [ChileCompra: alcance de sus datos](https://datos-abiertos.chilecompra.cl/datos-abiertos).

La **Agencia de Calidad de la Educación** aporta resultados como **SIMCE** (*Sistema de Medición de la Calidad de la Educación*) e **IDPS** (*Indicadores de Desarrollo Personal y Social*). También pueden interesar asistencia, retención o titulación, según el objetivo. Comprar una plataforma de lectura no implica que deba subir inmediatamente el SIMCE general: el indicador elegido debe corresponder al curso, propósito y plazo de la acción. Comparar antes y después **describe una asociación**, pero no demuestra por sí solo que la compra causó el cambio. [Agencia: SIMCE e IDPS](https://www.agenciaeducacion.cl/preguntas-frecuentes-simce/).

Hay dos instituciones adicionales útiles para no mezclar preguntas: **DIPRES** (*Dirección de Presupuestos*) informa el presupuesto y su ejecución a nivel de organismos como un SLEP; **Contraloría General de la República** audita la administración pública. Sus datos pueden señalar problemas del sostenedor, pero un presupuesto agregado del SLEP no es el gasto específico de un RBD. [DIPRES: SLEP Santa Rosa](https://www.dipres.gob.cl/597/w3-multipropertyvalues-25916-37782.html), [Contraloría: buscador público](https://transparencia.contraloria.cl/search).

La cadena completa del proyecto queda así:

$$
\underbrace{\text{asistencia y reglas}}_{\text{cálculo}}
\longrightarrow
\underbrace{\text{aporte al sostenedor}}_{\text{ingreso}}
\longrightarrow
\underbrace{\text{PEI/PME}}_{\text{propósito y acción}}
\longrightarrow
\underbrace{\text{compra y pago}}_{\text{gasto}}
\longrightarrow
\underbrace{\text{entrega y uso}}_{\text{ejecución real}}
\longrightarrow
\underbrace{\text{indicador educativo}}_{\text{resultado observado}}.
$$

**Regla para leer los datos:** “asignado”, “pagado”, “rendido”, “aceptado” y “utilizado” son estados diferentes. Si falta un documento, la conclusión correcta es **“aún no verificado”**, no “no se usó” ni “hubo corrupción”.

### Siglas que aparecieron en la explicación

| Sigla | Nombre y papel en esta investigación |
|---|---|
| **Mineduc** | Ministerio de Educación: marco educativo y subvenciones. |
| **RBD** | Rol Base de Datos: identificador de cada establecimiento. |
| **USE** | Unidad de Subvención Educacional: unidad en que se fijan tarifas legales. |
| **JEC** | Jornada Escolar Completa: régimen de jornada relevante para algunos valores de subvención. |
| **SEP** | Subvención Escolar Preferencial: financiamiento adicional asociado a alumnos prioritarios y preferentes y a concentración. |
| **PIE** | Programa de Integración Escolar: apoyo a estudiantes con necesidades educativas especiales; fuente distinta de SEP. |
| **FAEP** | Fondo de Apoyo a la Educación Pública: recursos para iniciativas de educación pública. |
| **PEI / PME** | Proyecto Educativo Institucional / Plan de Mejoramiento Educativo: propósito general / planificación de mejoras. |
| **SLEP / DEP** | Servicio Local de Educación Pública / Dirección de Educación Pública: sostenedor territorial público / entidad que conduce el sistema de educación pública. [DEP](https://educacionpublica.gob.cl/wp-content/uploads/sites/16/2023/04/CUENTA-2023-R.pdf). |
| **OC** | Orden de compra: compromiso registrado en un proceso de adquisición. |
| **SIMCE / IDPS** | Pruebas de aprendizaje / indicadores de desarrollo personal y social evaluados por la Agencia. |
| **DIPRES** | Dirección de Presupuestos: informa presupuesto y ejecución de organismos públicos. |

**Para el análisis exploratorio:** usar el [archivo de investigación de fuentes y KPIs](<Investigación exploratoria — gasto escolar Chile.md>) junto con esta guía conceptual.
