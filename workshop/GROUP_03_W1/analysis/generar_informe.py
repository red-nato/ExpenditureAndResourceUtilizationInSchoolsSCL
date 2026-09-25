"""Construye el informe autónomo W1 desde los resultados guardados del paquete."""
from pathlib import Path
import csv, json
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/outputs'
PDF=ROOT/'report/GROUP_03_W1_Report.pdf'
M=json.loads((OUT/'metricas.json').read_text())
def csvrows(name):
    with (OUT/name).open(newline='') as f:return list(csv.DictReader(f))
DIM=csvrows('b_resumen_dimensiones.csv')
COV=csvrows('b_cobertura_dependencia.csv')
BGS={
    'paper':colors.HexColor('#ffffff'),
    'navy':colors.HexColor('#183849'),
    'teal':colors.HexColor('#1d6677'),
    'light':colors.HexColor('#eef4f5'),
    'line':colors.HexColor('#d6e1e4'),
    'ink':colors.HexColor('#20343b'),
    'muted':colors.HexColor('#52646b'),
}
arial=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
arial_bold=Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
if arial.exists() and arial_bold.exists():
    pdfmetrics.registerFont(TTFont('ArialW1',str(arial)))
    pdfmetrics.registerFont(TTFont('ArialW1-Bold',str(arial_bold)))
    BODY_FONT,BOLD_FONT='ArialW1','ArialW1-Bold'
else:
    BODY_FONT,BOLD_FONT='Helvetica','Helvetica-Bold'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleW1',fontName=BOLD_FONT,fontSize=22,leading=26,textColor=BGS['navy'],spaceAfter=9))
styles.add(ParagraphStyle(name='SubW1',fontName=BODY_FONT,fontSize=11,leading=16,textColor=BGS['teal'],spaceAfter=10))
styles.add(ParagraphStyle(name='H1W1',fontName=BOLD_FONT,fontSize=13.2,leading=17,textColor=BGS['navy'],spaceBefore=15,spaceAfter=7,keepWithNext=True))
styles.add(ParagraphStyle(name='H2W1',fontName=BOLD_FONT,fontSize=10.6,leading=14,textColor=BGS['teal'],spaceBefore=11,spaceAfter=5,keepWithNext=True))
styles.add(ParagraphStyle(name='BodyW1',fontName=BODY_FONT,fontSize=8.8,leading=13,textColor=BGS['ink'],spaceAfter=7))
styles.add(ParagraphStyle(name='SmallW1',fontName=BODY_FONT,fontSize=7.8,leading=11,textColor=BGS['ink'],spaceAfter=5))
styles.add(ParagraphStyle(name='TinyW1',fontName=BODY_FONT,fontSize=7,leading=9.5,textColor=BGS['ink']))
styles.add(ParagraphStyle(name='CalloutW1',fontName=BOLD_FONT,fontSize=8.9,leading=13,textColor=BGS['navy'],spaceAfter=8))
styles.add(ParagraphStyle(name='CapW1',fontName=BODY_FONT,fontSize=7.7,leading=10,textColor=BGS['muted'],alignment=TA_CENTER,spaceAfter=9))
styles.add(ParagraphStyle(name='RefW1',fontName=BODY_FONT,fontSize=7.5,leading=10.3,textColor=BGS['ink'],spaceAfter=4,wordWrap='CJK'))
def P(s,sty='BodyW1'):return Paragraph(s,styles[sty])
def H(s,l=1):return P(s,'H1W1' if l==1 else 'H2W1')
def t(rows,widths,header=True):
    formatted=[[P(str(x),'TinyW1') for x in row] for row in rows]
    tb=Table(formatted,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT')
    commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),
              ('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),
              ('BOTTOMPADDING',(0,0),(-1,-1),5),('GRID',(0,0),(-1,-1),0.35,BGS['line'])]
    if header:commands += [('BACKGROUND',(0,0),(-1,0),BGS['navy']),
                           ('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    for i in range(1,len(rows)):
        if i%2==0:commands.append(('BACKGROUND',(0,i),(-1,i),BGS['light']))
    tb.setStyle(TableStyle(commands))
    # Header paragraph text color needs custom inline font, handled via dark row? dark text is readable enough?
    return tb
def table(rows,widths):
    new=[]
    for i,row in enumerate(rows):
        new.append([('<font color="#ffffff"><b>'+str(x)+'</b></font>') if i==0 else str(x) for x in row])
    return t(new,widths)
def fig(name,w=470):
    im=Image(str(OUT/name))
    scale=w/im.imageWidth
    im.drawWidth=w;im.drawHeight=im.imageHeight*scale
    return im
def fmt_int(n):return f"{int(n):,}".replace(',','.')
def fmt_clp(n):return '$'+fmt_int(n)
def pct(n):return f"{float(n):.1f}".replace('.',',')+'%'
def ref(url,label):
    safe=escape(url)
    return f'<link href="{safe}" color="#1d6677">{escape(label)}</link>'
story=[]
story += [Spacer(1,12),P('W1 · Preguntas que vale la pena investigar','TitleW1'),
          P('Gasto educativo en Chile | Grupo 03 | 25 de septiembre de 2026','SubW1'),
          P('<b>Integrantes:</b> Javier Alcaíno · Lucas Riquelme · Renato Varela','SmallW1'),
          P('<b>Adaptación del tema:</b> el grupo informó que el profesor autorizó usar su problemática y bases educativas en este workshop. Por ello, las referencias de MINSAL en la pauta se sustituyen aquí por normas, datos y fiscalización de educación. La autorización del tema no constituye validación de hallazgos.','SmallW1'),
          H('Resumen para recibir feedback'),
          P('Este W1 se apoya en una investigación de varias semanas sobre el gasto educativo. Para el workshop se comparan dos opciones distintas. <b>A</b> pregunta por la custodia y disponibilidad de bienes tecnológicos adquiridos en Melipeuco entre 2020 y 2022, a partir de un caso fiscalizado. <b>B</b> pregunta qué tan interpretable es la implementación declarada de acciones PME 2024 y dónde se concentran brechas de cobertura y calidad del registro. Ambas usan archivos reales y procedimientos que se pueden volver a ejecutar con este paquete.'),
          table([['Decisión provisional','Por qué y condición de cambio'],
                 ['Preferir A para C1, con B como contexto de calidad de datos.',
                  'A permite seguir activos y reconciliar una observación material. Cambiaríamos si el seguimiento de bienes no está disponible o si las rendiciones/uso del PME permiten una pregunta evaluativa mejor delimitada.']], [145,355]),
          Spacer(1,7),
          P('Una compra declarada no es un pago; un bien observado como no habido en 2023 no equivale a pérdida definitiva hoy; una acción PME al 100% no demuestra uso ni impacto. Estas tres fronteras guían el informe.','CalloutW1'),
          H('1. Línea A - disponibilidad de bienes de Melipeuco'),
          P('<b>Problema y alcance.</b> Contraloría Regional de La Araucanía fiscalizó equipos adquiridos para seis escuelas y el DEM entre 2020 y 2022, con visitas en diciembre de 2023 e informe final 43/2024 de junio de 2024 [1]. La pregunta tentativa es: ¿qué cantidad y valor histórico de bienes del universo fiscalizado no pudo validarse físicamente, y qué documentación permitiría cerrar la observación por activo?'),
          P('<b>Relevancia y uso propuesto.</b> La SEP exige vincular recursos a medidas del Plan de Mejoramiento Educativo [2]. La observación CGR documenta una interrupción de la cadena entre adquisición, comodato y disponibilidad [1]. Proponemos que sostenedor, fiscalizador o comunidad escolar usen el desglose para priorizar inventarios, recuperaciones y descargos; no afirmamos que esas entidades hayan solicitado este tablero. La ISSAI 300 distingue economía, eficiencia y eficacia [3].'),
          H('Datos abiertos y primera inspección',2),
          P('El PDF CGR de 91 páginas y una extracción tabular conservan página y fila. El CSV de compras tiene <b>29 partidas destino-documento-modelo</b>, no 29 contratos independientes; suma <b>776 unidades</b>. La tabla de observaciones contiene <b>628 filas de bienes</b>; la tabla de comodatos, 600 certificados. La clave factura + serie, normalizada exactamente, permite verificar el cruce entre anexos.'),
          table([['Medida del universo fiscalizado','Resultado','Interpretación'],
                 ['Equipos con existencia o ubicación no validada',f"{M['a']['equipos_observados']} / {M['a']['equipos_adquiridos']} = 80,93%",'Hallazgo histórico en el universo CGR.'],
                 ['Costo histórico de bienes observados',f"{fmt_clp(M['a']['valor_observado_clp'])} / {fmt_clp(M['a']['valor_impreso_cgr_clp'])} = 77,43%",'Exposición a valor de adquisición, no pérdida firme.'],
                 ['Comodatos que coinciden con no habidos',f"{M['a']['coincidencias']} / {M['a']['comodatos']} = 79,33%",'Certificado no acredita localización posterior.']], [175,140,185]),
          P('La suma extraída de partidas es $176.164.030: <b>$1 más</b> que el total impreso de $176.164.029. Se conserva la diferencia y las tasas monetarias usan el total publicado. Entre las 628 filas, 10.a aporta 625, 10.b dos con identificación insuficiente y 10.c una impresora; no se trata cada 10.b como desaparición individual.'),
          fig('a_valor_observado.png',455),
          P('Fuente: elaboración propia con anexo 4 y tablas 3-4 del informe CGR 43/2024 [1]. Las Lenovo P11 suman $80.849.769, 59,27% del valor observado; el gráfico muestra costo histórico y no valor recuperable.','CapW1'),
          H('Qué resuelve y qué falta',2),
          P('La inspección permite priorizar por familia y serie. <b>No</b> permite saber si los equipos funcionaron antes de la visita ni cuánto se recuperó después. De 628 registros observados, 147 carecen de serie usable y 18 carecen de RBD individualizable en la tabla reducida. El caso se eligió por un hallazgo conocido: su 80,93% no estima prevalencia nacional. Se necesitan seguimiento por serie, baja contable, restitución, garantía, fuente de financiamiento por ítem y documentos de uso; no se atribuye todo a SEP.'),
          H('2. Línea B - implementación declarada del PME 2024'),
          P('<b>Problema y alcance.</b> Mineduc publica acciones PME con estimaciones de monto y niveles declarados de implementación [4]. La pregunta tentativa es: ¿qué diferencias y problemas de registro aparecen al comparar dimensiones, dependencia y escuelas del piloto, antes de usar el PME como base de un tablero de seguimiento? Es una decisión de <b>validación y focalización de revisión</b>, no de auditoría de pagos.'),
          P('<b>Relevancia y uso propuesto.</b> La ley SEP relaciona los recursos con medidas PME [2]. El catálogo ministerial advierte que los montos publicados son estimaciones declaradas, no aprobación ni aceptación del gasto [4]. Proponemos que Mineduc o un SLEP utilicen señales de cobertura, valores extremos y avance reportado para decidir qué registros verificar primero; es una propuesta de uso, no una opinión atribuida a esas instituciones.'),
          H('Datos abiertos y primera inspección',2),
          P(f"El extracto de Implementación PME 2024 contiene <b>{fmt_int(M['b']['acciones'])} acciones</b> de <b>{fmt_int(M['b']['escuelas'])} RBD</b>; una fila es una acción, con `fila_excel` como referencia. El Directorio Oficial 2024 contiene una fila por RBD (16.694) y permite agregar por escuela antes de unir. Se comprobó la unión de <b>8.240/8.240 RBD</b>. Los ocho RBD públicos de La Cisterna reúnen <b>134 acciones</b> en el extracto."),
          table([['Dimensión PME','Acciones','Mediana estimada / acción','Declaradas al 100%']] +
                [[r['DIMENSION'],fmt_int(r['acciones']),fmt_clp(float(r['estimacion_mediana_clp'])),pct(r['porcentaje_completo'])] for r in sorted(DIM,key=lambda r:r['DIMENSION'])],
                [145,73,143,139]),
          P('Fuente: elaboración propia con Implementación PME 2024 [4]. La mediana de Gestión de Recursos es $6 millones; el porcentaje completo es una fracción de acciones, no ejecución financiera.'),
          fig('b_implementacion_dimensiones.png',455),
          P('Fuente: cálculos del cuaderno W1 sobre acciones PME 2024. Los tramos 75-99% no se convierten en un avance exacto.','CapW1'),
          P('En escuelas activas con matrícula positiva del directorio, la cobertura PME es <b>95,51%</b> para DAEM (código 2), <b>96,27%</b> para SLEP (6) y <b>64,32%</b> para particulares subvencionados (3). Son tasas de presencia en la base, no tasas de ejecución. Entre las acciones, 27.569 tienen estimación cero y 38 carecen de estimación SEP; cuatro filas exactamente repetidas adicionales se conservan por falta de ID único. Sólo 19 acciones >$1.000 millones explican 12,80% del total declarado: la media cae de $13,21 a $11,52 millones al excluirlas como sensibilidad, mientras la mediana queda en $2 millones. Nada de ello prueba pagos excesivos.'),
          H('Qué resuelve y qué falta',2),
          P('La pregunta es viable para calidad, distribución e implementación <i>declarada</i>. No se puede clasificar una licitación como bien o mal utilizada desde estos archivos: faltan pagos, asignación a RBD, recepción y uso. Tampoco procede cruzar SIMCE posterior para atribuir efecto sin exposición, objetivo, cohorte y comparador. El piloto de La Cisterna debe respetar el cambio de sostenedor en 2025; este W1 mantiene el corte 2024.'),
          H('3. Comparación y decisión provisional'),
          table([['Criterio','A: custodia de bienes','B: registro PME'],
                 ['Unidad y decisión','Activo/partida CGR; localizar, recuperar o justificar bajas.','Acción/RBD 2024; validar calidad y priorizar seguimiento.'],
                 ['Base documental','Informe CGR con anexos y descargos [1].','Ley SEP, catálogos y diccionario Mineduc [2,4,5].'],
                 ['Ajuste pregunta-dato','Fuerte para observación histórica, débil para estado actual o impacto.','Fuerte para planificación declarada, nulo para pago y uso real.'],
                 ['Oportunidad C1','Conciliar series, montos, fondos y estado de seguimiento.','EDA por dimensión/dependencia y consistencia; ampliar a rendiciones.'],
                 ['Riesgo principal','Caso seleccionado por hallazgo; no extrapolar.','Autorreporte, valores extremos y cobertura desigual.'],
                 ['ML futuro (condicional)','Predecir no disponibilidad sólo con inventarios completos y etiquetas de activos revisados, incluidos los encontrados.','Predecir acciones que no concluyen sólo con series históricas y estados validados; evitar aprender errores de reporte.'],
                 ['Tablero futuro','Sostenedor: activos, ubicación, último control y saldo de observaciones.','SLEP/Mineduc: cobertura, tramos de avance, montos estimados y calidad del dato.']], [99,201,200]),
          P('<b>Preferencia.</b> A responde mejor a la inquietud original sobre destino material de recursos y ya dispone de contraste documental. B es una segunda línea genuina: evalúa la calidad de la planificación e implementación reportada, no el mismo hallazgo reetiquetado. Mantener B como módulo de contexto evita presentar cifras PME como compras. Si no se obtiene seguimiento de activos, reconsiderar A o limitar C1 explícitamente a una auditoría histórica.'),
          H('Preguntas concretas para el profesor',2),
          P('1. ¿Considera suficiente un caso CGR seleccionado por hallazgo para C1 si el objetivo es reconstruir trazabilidad y no estimar prevalencia? 2. ¿Qué evidencia mínima de seguimiento aceptaría para afirmar que una observación sigue abierta o fue cerrada? 3. ¿Conviene que B permanezca como análisis de calidad del dato, o que pase a línea principal sólo cuando se obtengan rendiciones y documentos de uso? 4. ¿Qué nivel de desagregación y resguardo pediría para un futuro modelo de riesgo de activos sin sesgo de selección?'),
          H('4. Encuadre inicial en siete pasos'),
          table([['Paso de Class 03','Línea A','Línea B'],
                 ['Decisión','Priorizar localización y cierre de observaciones.','Priorizar validación de registros PME.'],
                 ['Éxito','Estado acreditado por activo, fecha y documento.','Cobertura y avance interpretables sin confundir pagos.'],
                 ['Pregunta de negocio','¿Qué bienes y valor siguen observados?','¿Dónde hay brechas de registro y avance?'],
                 ['Proceso','Compra > entrega > comodato > uso > control.','Plan PME > declaración > verificación.'],
                 ['Entidades/eventos/estados','Factura, serie, RBD, entrega, baja, restitución.','Acción, RBD, dimensión, tramo, año.'],
                 ['Representación','Anexos PDF a filas; clave factura+serie.','Acciones a RBD; directorio 2024.'],
                 ['Medición','Unidades, valor histórico, seguimiento.','Cobertura, medianas, % al 100%, extremos.']], [117,192,191]),
          H('Primeras verificaciones: Five Cs',2),
          table([['C','Riesgo observado y control inicial'],
                 ['Clean','La suma CGR difiere $1; 19 montos PME extremos se mantienen y se analizan aparte.'],
                 ['Consistent','Factura+serie se comprueba única en anexos; RBD y año se verifican antes de unir.'],
                 ['Complete','147 registros observados sin serie usable; 38 estimaciones SEP ausentes. Ausente no es cero.'],
                 ['Current','Compras 2020-2022, visita 2023 e indicador PME 2024 no forman una serie temporal común.'],
                 ['Collaborative','Diccionario, página/fila, URLs, hashes, código y salidas guardadas hacen revisables las decisiones.']], [94,406]),
          H('Process record'),
          H('Decisions and checks',2),
          table([['Etapa / decisión','Alternativa y motivo','Comprobación / evidencia en paquete'],
                 ['Investigación previa y W1','El equipo ya había definido el núcleo del problema; para W1 se contrastaron A: bienes auditados y B: registro PME como líneas diferentes.','PDF secciones 1-3; cuaderno secciones 2-3.'],
                 ['CGR: mantener cifra impresa','No corregir el $1 ni llamar pérdida a todo el valor observado.','Script: aserciones; outputs/a_tipos_observacion.csv; fuente PDF.'],
                 ['PME: seleccionar unidad escolar','No repetir matrícula por acción; agregación previa por RBD.','Script y outputs/b_panel_cisterna.csv; unión 8.240/8.240.'],
                 ['Criterio de eficacia','No usar SIMCE años después como prueba de compra útil.','Marco_evaluacion_gasto.md y PDF sección 3.']], [105,181,214]),
          H('Instructor feedback and response',2),
          P('El grupo informó que el profesor permitió emplear sus bases y problema educativo en W1. Se aceptó esa adaptación y se reemplazó el contexto de salud por SEP, Mineduc y CGR. <b>Feedback sobre la elección A/B y sus resultados: pendiente</b>; la preferencia A es provisional y las cuatro preguntas anteriores buscan orientación específica. No se atribuye al profesor una aprobación de conclusiones.'),
          H('Individual contributions',2),
          table([['Integrante','Aporte al desarrollo del proyecto'],
                 ['Javier Alcaíno','Asumió la mayor parte de la implementación y depuración del código analítico, y colaboró en la estructura, redacción y revisión del informe de resultados.'],
                 ['Lucas Riquelme','Examinó críticamente las fuentes y el contexto institucional una vez definido el núcleo del proyecto; ayudó a precisar el alcance de los datos y de las conclusiones posibles.'],
                 ['Renato Varela','Desarrolló la investigación preliminar que ayudó a definir el núcleo del proyecto y colaboró en el análisis de datos y la revisión del código.']], [104,396]),
          H('AI use and verification',2),
          P('<b>Herramienta:</b> Codex. Se utilizó en esta etapa para organizar el paquete W1, apoyar la ejecución del código y revisar cálculos y formato. La formulación del problema y la investigación previa son trabajo del equipo. Los extractos siguientes documentan ajustes de formato, una dependencia faltante y verificaciones numéricas de W1; se pueden cotejar con el script, sus salidas y el informe.'),
          table([['Tarea técnica','Extracto o resultado comprobable','Verificación / decisión'],
                 ['Formato del informe','Se renderizaron todas las páginas del PDF para revisar legibilidad, tablas, gráficos y saltos.','Revisión visual del informe final y sus figuras guardadas en analysis/outputs/.'],
                 ['Error de ejecución','ModuleNotFoundError: No module named reportlab al regenerar el PDF en un entorno sin esa biblioteca.','Se usó un entorno con reportlab instalado; requirements.txt declara la dependencia.'],
                 ['Control del cruce','x.merge(y, on=["factura","serie"], validate="one_to_one") → 476 coincidencias.','Se comprobaron claves únicas en ambos anexos; un certificado no prueba ubicación actual.'],
                 ['Chequeo de cálculos','29 partidas = 776 equipos; 628 observados; la suma de partidas da $176.164.030 frente a $176.164.029 impreso.','Aserciones en analysis/w1_analisis.py; se conservó la diferencia de $1 y se usó la cifra publicada como denominador.'],
                 ['Chequeo de cobertura','La unión por RBD conserva 8.240/8.240 escuelas PME.','Se agregó a nivel escuela antes de unir para evitar contar matrícula una vez por acción.']], [104,190,206]),
          P('La clasificación de gasto y la lectura causal se contrastaron con Ley 20.529 art. 55 [6], ISSAI 300 [3] y el informe CGR [1]. Los controles verifican consistencia interna, no acreditan pagos, uso real ni efectos en aprendizaje. No se incorporaron microdatos estudiantiles.','SmallW1'),
          H('Referencias'),
          P('[1] Contraloría Regional de La Araucanía. <i>Informe final de investigación especial N° 43/2024, DEM Melipeuco</i>, 10-06-2024; compras 2020-2022 y visita diciembre 2023. Copia del informe incluida en data/. '+ref('https://www.ciperchile.cl/wp-content/uploads/FIRMADO_Informe-final-de-investigacion-especial-N%C2%B043_de-2024_DEM_Melipeuco_.pdf','PDF consultable')+'.','RefW1'),
          P('[2] Biblioteca del Congreso Nacional. <i>Ley N° 20.248, Subvención Escolar Preferencial</i>, texto vigente consultado 25-09-2026. '+ref('https://www.bcn.cl/leychile/navegar?idNorma=269001','Texto legal')+'.','RefW1'),
          P('[3] INTOSAI. <i>ISSAI 300: Performance Audit Principles</i>, edición 2019. '+ref('https://www.issai.org/pronouncements/issai-300-performance-audit-principles/','Norma')+'.','RefW1'),
          P('[4] Ministerio de Educación, División de Educación General. <i>Bases de datos PME: Implementación PME 2024 y advertencia de uso</i>; extracción ministerial 16-01-2025, archivo publicado 2025. '+ref('https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/','Catálogo')+'.','RefW1'),
          P('[5] Centro de Estudios Mineduc. <i>Directorio Oficial de Establecimientos Educacionales 2024</i>, corte matrícula 30-04-2024. '+ref('https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/','Catálogo y diccionario')+'.','RefW1'),
          P('[6] Biblioteca del Congreso Nacional. <i>Ley N° 20.529</i>, art. 55, texto vigente consultado 25-09-2026. La rendición juzga legalidad y no mérito de uso. '+ref('https://www.bcn.cl/leychile/navegar?idNorma=1028635','Texto legal')+'.','RefW1'),
          P('[7] Ugarte, G. <i>Gasto social en la mira: propuestas para un nuevo foco en la política social chilena</i>. CEP, Puntos de Referencia 752, diciembre 2025. Referencia metodológica de focalización; no audita estas compras. '+ref('https://static.cepchile.cl/uploads/cepchile/2025/11/28-155617_h03g_pder752_Ugarte.pdf','Estudio CEP')+'.','RefW1'),
          P('Alcance de referencias: los documentos CGR y Mineduc sostienen los datos; la ley e ISSAI sostienen el encuadre. El estudio CEP inspira el uso de criterio previo y escenarios, pero sus tasas no se trasladan a compras escolares.','SmallW1')]

def footer(canvas,doc):
    canvas.saveState()
    w,h=doc.pagesize
    canvas.setStrokeColor(BGS['line']);canvas.line(42,37,w-42,37)
    canvas.setFont(BODY_FONT,7.5);canvas.setFillColor(BGS['muted'])
    canvas.drawString(42,25,'GROUP_03_W1  |  Gasto educativo en Chile  |  25-09-2026')
    canvas.drawRightString(w-42,25,f'{doc.page}')
    canvas.restoreState()

doc=SimpleDocTemplate(str(PDF),pagesize=(595.276,841.89),
                      rightMargin=42,leftMargin=42,topMargin=43,bottomMargin=52,
                      title='GROUP_03_W1 - Dos preguntas de investigación',
                      author='Javier Alcaíno, Lucas Riquelme y Renato Varela (Grupo 03)')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(PDF)
