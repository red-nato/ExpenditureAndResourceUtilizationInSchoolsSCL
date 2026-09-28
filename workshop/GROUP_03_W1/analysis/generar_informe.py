"""Informe W1 verificable a partir de analysis/outputs/metricas.json."""
from pathlib import Path
import csv
import json
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
M = json.loads((ROOT / "analysis/outputs/metricas.json").read_text())
with (ROOT / "analysis/outputs/pme_dimensiones.csv").open(encoding="utf-8", newline="") as handle:
    PME_DIM = list(csv.DictReader(handle))
PDF = ROOT / "report/GROUP_03_W1_Report.pdf"
normal = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
bold = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
if normal.exists() and bold.exists():
    pdfmetrics.registerFont(TTFont("ArialW1", str(normal)))
    pdfmetrics.registerFont(TTFont("ArialW1-Bold", str(bold)))
    FONT, BOLD = "ArialW1", "ArialW1-Bold"
else:
    FONT, BOLD = "Helvetica", "Helvetica-Bold"
NAVY = colors.HexColor("#17394b")
TEAL = colors.HexColor("#176e7b")
ORANGE = colors.HexColor("#c27330")
PALE = colors.HexColor("#ecf3f5")
INK = colors.HexColor("#243940")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleW", fontName=BOLD, fontSize=19, leading=23, textColor=NAVY, spaceAfter=9))
styles.add(ParagraphStyle(name="SubW", fontName=FONT, fontSize=9, leading=12, textColor=TEAL, spaceAfter=10))
styles.add(ParagraphStyle(name="H1W", fontName=BOLD, fontSize=11.8, leading=15, textColor=NAVY, spaceBefore=10, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="H2W", fontName=BOLD, fontSize=9.4, leading=12.4, textColor=TEAL, spaceBefore=8, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="BW", fontName=FONT, fontSize=8.25, leading=11.5, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="SW", fontName=FONT, fontSize=7.3, leading=10.0, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle(name="TW", fontName=FONT, fontSize=7.0, leading=9.1, textColor=INK))
styles.add(ParagraphStyle(name="THW", fontName=BOLD, fontSize=7.0, leading=9.1, textColor=colors.white))


def p(text, style="BW"):
    return Paragraph(text, styles[style])


def h(text, level=1):
    return p(text, "H1W" if level == 1 else "H2W")


def table(rows, widths):
    data = [[p(str(x), "THW" if i == 0 else "TW") for x in row] for i, row in enumerate(rows)]
    tab = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    tab.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#cad9de")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tab


def link(url, label):
    return f'<link href="{escape(url)}" color="#176e7b">{escape(label)}</link>'


def coverage_chart():
    # Resumen visual: presencia de registro PME, no elegibilidad ni ejecución.
    d = Drawing(495, 112)
    d.add(String(3, 98, "PME 2024: establecimientos con al menos una acción en el extracto", fontName=BOLD, fontSize=8.5, fillColor=NAVY))
    labels = [("Públicos", 8, 8, TEAL), ("Particulares subv.", 38, 51, ORANGE)]
    for i, (name, found, total, color) in enumerate(labels):
        y = 63 - i * 36
        d.add(String(3, y + 6, name, fontName=FONT, fontSize=8, fillColor=INK))
        d.add(Rect(118, y, 300, 18, fillColor=PALE, strokeColor=None))
        d.add(Rect(118, y, 300 * found / total, 18, fillColor=color, strokeColor=None))
        d.add(String(427, y + 5, f"{found}/{total}", fontName=BOLD, fontSize=8.5, fillColor=NAVY))
    d.add(Line(118, 9, 418, 9, strokeColor=colors.HexColor("#a8bac0"), strokeWidth=.5))
    return d


story = [
    Spacer(1, 8), p("W1 | Cómo se usan los recursos escolares", "TitleW"),
    p("La Cisterna · Grupo 03 · 25 de septiembre de 2026", "SubW"),
    p("<b>Integrantes:</b> Javier Alcaíno, Lucas Riquelme y Renato Varela. El grupo informó autorización docente para usar el tema educativo en vez de los datos de salud sugeridos por la pauta. W1 aún no ha sido entregado ni ha recibido feedback sobre este análisis.", "SW"),
    h("Decisión, problema y fundamento"),
    p("<b>Pregunta principal:</b> ¿qué recursos públicos reciben y rinden los establecimientos públicos y particulares subvencionados de La Cisterna, qué gastos presentan observaciones documentadas y qué evidencia acredita entrega y uso? La comparación de resultados educativos se mantiene como contexto y nunca como prueba aislada de malgasto."),
    p("La relevancia excede las bases de datos: la evaluación de la Subvención Escolar Preferencial de <b>DIPRES (marzo de 2023)</b> examinó uso de recursos y procesos de rendición; la <b>Ley 20.248</b>, texto vigente consultado el 25-09-2026, vincula SEP con medidas del PME y exige informar su uso a la Superintendencia y la comunidad [1, 2]. La decisión territorial consiste en reconstruir esa cadena para cada RBD, sin suponer que una anomalía equivale a infracción."),
    table([["Línea", "Usuario y uso propuestos", "Pregunta inicial"],
           ["A · Rendición y fiscalización", "Superintendencia y sostenedores: elegir expedientes, corregir rendiciones y verificar observaciones.", "¿Qué gasto declarado fue aceptado, rechazado o sujeto a reintegro, y por qué?"],
           ["B · PME y Agencia", "Equipos directivos y comunidades escolares: contrastar planificación declarada, cobertura y resultados pertinentes.", "¿Qué brechas de registro o implementación requieren evidencia adicional?"]], [109, 177, 209]),
    p("<b>Preferencia provisional:</b> A responde directamente al uso de recursos. B ayuda a definir preguntas y comparaciones. Las rendiciones detalladas y expedientes aún no están disponibles, de modo que W1 demuestra viabilidad y límites, no cuantifica dinero malgastado.", "SW"),
    h("Primera inspección de datos"),
    p("El Directorio aporta 60 RBD en 2022 y 2023, y 59 en 2024 y 2025. Los ocho públicos figuran DAEM hasta 2024 y SLEP en 2025; RBD 9830 aparece solo en los dos primeros años. La extracción PME 2024 registra 767 acciones de 46 RBD. La figura cuenta establecimientos con al menos una fila, no cobertura de elegibles ni gasto ejecutado."),
    coverage_chart(),
    p("Figura 1. El extracto PME incluye 8/8 públicos y 38/51 particulares subvencionados del censo 2024. Los 13 sin fila exigen revisar aplicabilidad y fuente; no se clasifican como incumplimiento. Fuente: Directorio Oficial 2024 y PME 2024, cálculo en `analysis/outputs/metricas.json`.", "SW"),
    PageBreak(),
    h("1. Datos inspeccionados y diccionario"),
    table([["Fuente y fila", "Llave propuesta antes de unir", "Resultado observado y límite"],
           ["Directorio: RBD–año (2022–2025)", "`anio + rbd`", "238 filas, 60/60/59/59. Oferta, dependencia y matrícula definen censo anual."],
           ["PAS: proceso (archivos 2022–2025)", "`pa_id`", "110 procesos de 39 RBD; 47 multas y 0 reintegros en primera instancia. Materia financiera no disponible en extracto."],
           ["PME: acción declarada 2024", "`fila_excel` es localizador de extracción, no ID oficial", "767 acciones, 46 RBD; monto total estimado $9.009.408.718, no pago."],
           ["SIMCE: RBD–año–grado", "`anio + rbd + grado`", "236 filas. Puntaje puede faltar aun con fila."],
           ["IDPS: RBD–año–grado–indicador", "`anio + rbd + grado + indicador`", "936 filas. Un promedio ausente no es cero."]], [126, 134, 235]),
    p("El diccionario `data/DICCIONARIO.md` define campos, períodos y unidad; `analysis/outputs/perfil_fuentes.csv` reporta nulos y duplicados reales. Las llaves de esta tabla fueron <b>propuestas</b>; el flujo primero las perfiló y después comprobó unicidad, pertenencia y conservación en `Validate`. Ninguna unión se asumió segura por compartir el nombre RBD.", "SW"),
    h("2. Preparación analítica: ocho etapas"),
    table([["Etapa", "Acción y evidencia que deja"],
           ["Load", "Lee cinco extractos sin filtros adicionales; 238 + 110 + 767 + 236 + 936 filas."],
           ["Profile", "Registra llave propuesta, nulos críticos y duplicados por fuente (`perfil_fuentes.csv`)."],
           ["Explore", "Cuenta censo por año y PAS por archivo antes de cruzar (`controles_etapas.csv`)."],
           ["Clean", "Convierte RBD/año a enteros, montos a Decimal y grados a código uniforme; no borra filas."],
           ["Impute", "Mantiene `NA` en gasto, rendición y puntajes. Cero PAS/PME es conteo de filas publicadas, con marca de presencia."],
           ["Transform", "Agrega cada fuente antes del join; construye 238 RBD–año (`panel_rbd_anual.csv`)."],
           ["Validate", "Comprueba llaves únicas, pertenencia anual, totales conservados y cero pérdida por join."],
           ["Explore again", "Relee 60/60/59/59 y 8/8 frente a 38/51 tras validar; distingue ausencia de registro y ausencia de gasto."]], [93, 402]),
    h("Segundo vistazo: diferencias dentro del PME", 2),
    table([["Dimensión", "Acciones", "Declaradas 100%", "Estimación $0"]] +
          [[r["dimension"], r["acciones"], r["declaradas_completas"], r["estimacion_cero"]] for r in PME_DIM],
          [195, 80, 115, 105]),
    p("De 767 acciones, 469 se declararon completas y 149 tienen estimación total cero. La mayor mediana estimada por acción es Gestión de Recursos ($11.775.000). Estos son estados y montos <i>declarados</i>; la tabla no mide ejecución financiera ni calidad del servicio.", "SW"),
    h("Controles de calidad y límites"),
    p("Como nomenclatura <b>provisional</b> de cinco controles: <b>Complete</b> (nulos y cobertura), <b>Correct</b> (tipos/rangos), <b>Consistent</b> (mismo RBD y año), <b>Currency</b> (versión/fecha), <b>Concordant/Unique</b> (llaves y joins). El grupo no confirmó que estos sean los nombres exactos usados en clase. La trazabilidad documental se evalúa aparte, en el Process record.", "SW"),
    PageBreak(),
    h("3. Comparación crítica para decidir C1"),
    table([["Dimensión de la pauta", "A · Rendición / PAS", "B · PME / Agencia"],
           ["Relevancia respaldada", "Ley SEP y evaluación DIPRES 2023 [1,2]: uso y rendición son parte del diseño público.", "Ley SEP y Agencia [2,3]: planificación PME y resultados orientan mejora educativa."],
           ["Ajuste pregunta–dato inspeccionado", "PAS muestra proceso, instancia y sanción; falta gasto aceptado/rechazado por cuenta.", "PME mide declaración; SIMCE/IDPS por grado contextualizan, no verifican pago o uso."],
           ["Oportunidad analítica C1", "Cruzar rendición, expediente y documentos de entrega; comparar casos con y sin observación.", "Panel de calidad y cobertura por RBD/año/grado; casos para pedir respaldo de acciones."],
           ["Principal límite/incertidumbre", "PAS no es censo de fiscalizaciones ni monto malgastado. Cierre 2025 de rendición sujeto a disponibilidad.", "Aplicabilidad PME y elegibilidad por grado aún no resueltas; no hay causalidad educativa."],
           ["Alcance viable; ML y tablero", "Tablero documental ahora. ML solo con etiquetas de resoluciones firmes, exposición y negativos revisados.", "Tablero de cobertura ahora. ML solo con varias cohortes, resultados comparables y estados validados."]], [114, 190, 191]),
    h("Potencial futuro, condicionado a nuevos datos", 2),
    p("<b>A - ML:</b> clasificar si una rendición tendrá gasto no aceptado <i>firme</i>, con datos previos al cierre, cuenta/subvención, historial y etiquetas administrativas con fechas. Faltan rendiciones, universo fiscalizado y casos negativos revisados; hoy no se entrena modelo. <b>Tablero A:</b> para Superintendencia/sostenedores, RBD, año, subvención, declarado/aceptado/rechazado, estado de recurso, expediente y documento faltante."),
    p("<b>B - ML:</b> estimar riesgo de que una acción PME no complete su implementación declarada en el siguiente ciclo, con panel de acciones de varios años y estados comprobados. Falta historia comparable, definición estable de acción y validación de autorreporte. <b>Tablero B:</b> para equipos directivos/comunidad, presencia de PME, acciones por dimensión, resultados SIMCE/IDPS por grado y versiones, con marcas de no aplicabilidad y faltantes."),
    h("4. Siete pasos de formulación de la pregunta (Clase 03)"),
    table([["Paso", "Aplicación a La Cisterna"],
           ["1 Decisión", "Elegir dónde revisar documentos y qué afirmación se puede publicar."],
           ["2 Éxito", "Cobertura visible y hallazgos con monto, estado y respaldo, sin falsos ceros."],
           ["3 Pregunta de negocio", "¿Qué recursos recibidos, rendidos y observados llegaron a servicio verificable?"],
           ["4 Proceso", "Transferencia → rendición → fiscalización → resolución → recepción/uso."],
           ["5 Entidades/eventos/estados", "RBD, sostenedor, subvención, cuenta, acción, PAS, documento, estado de apelación."],
           ["6 Representación", "RBD–año como panel; cuentas y expedientes en tablas separadas; puente para compras compartidas."],
           ["7 Medición", "Monto aceptado/rechazado firme, cobertura por fuente, saldo y entrega/uso acreditados."]], [140, 355]),
    p("Los siete pasos formulan el problema; las ocho etapas de la página anterior preparan los datos. La pregunta no se resuelve con una correlación entre monto PME y puntaje SIMCE.", "SW"),
    PageBreak(),
    h("5. Process record"),
    h("Decisions and checks", 2),
    table([["Fecha/etapa; decisión", "Alternativa, razón y evidencia", "Chequeo / resultado / archivo"],
           ["25-09-2026 · alcance: La Cisterna y ambas dependencias", "Se descartó seguir un caso externo; responde la pregunta territorial del grupo. Directorios 2022–2025 [4].", "60/60/59/59 RBD, RBD 9830 solo 2022–23. `data/universo_la_cisterna_2022_2025.json`; `outputs/universo_anual.csv`."],
           ["25-09-2026 · dos líneas A/B; A preferida", "Alternativa: PME como prueba de malgasto. Se rechazó porque son estimaciones declaradas [5].", "767 acciones de 46 RBD; no pagos. `outputs/metricas.json`; páginas 1 y 3."],
           ["25-09-2026 · unir por RBD–año tras perfilar", "Alternativa: join directo por RBD que multiplicaría acciones y filas Agencia.", "Llaves únicas, 238 filas conservadas; `outputs/perfil_fuentes.csv`, `outputs/controles_etapas.csv`, `outputs/panel_rbd_anual.csv`."],
           ["25-09-2026 · no imputar gasto/puntaje", "Alternativa: rellenar ausentes con cero; produciría falsa evidencia de inactividad o bajo resultado.", "Marcas de presencia y `NA` conservados; `analysis/pipeline_la_cisterna.py`, etapa Impute."]], [133, 178, 184]),
    h("Instructor feedback and response", 2),
    p("<b>Estado real al 25-09-2026:</b> W1 aún no se entrega; no existe feedback docente sobre las dos líneas, las cifras o la metodología. La autorización previa del tema educativo se registra como decisión de alcance, no como evaluación. Las preguntas para solicitar feedback están al cierre de este informe. No hay consejo aceptado, adaptado o rechazado que atribuir al profesor.", "SW"),
    h("Individual contributions", 2),
    table([["Integrante", "Aporte informado por el grupo"],
           ["Javier Alcaíno", "Parte de la implementación y depuración del código analítico; estructura, redacción y revisión del informe."],
           ["Lucas Riquelme", "Examen crítico de fuentes y contexto institucional; precisión del alcance de datos y conclusiones."],
           ["Renato Varela", "Investigación preliminar del núcleo del proyecto; análisis de datos y revisión del código."]], [112, 383]),
    p("Estos aportes fueron confirmados por el grupo para esta revisión. Las ubicaciones de trabajo verificables en el paquete son `analysis/`, `data/` y `report/`; el paquete no contiene historial de edición individual para atribuir líneas concretas de código.", "SW"),
    h("AI use and verification", 2),
    table([["Propósito y extracto de instrucción", "Salida y decisión humana/analítica", "Verificación"],
           ["Replantear alcance: «Vuelve a La Cisterna... particulares subvencionados». Codex organizó censo y cruces.", "Se aceptó censo anual; se modificó el corte fijo de 59 al detectar RBD 9830 en 2022–23. No se aceptó extrapolar 2025 a años anteriores.", "Directorio original, `data/universo...2022_2025.json`, `outputs/universo_anual.csv`."],
           ["Corregir W1: «Load → Profile → Explore → Clean → Impute → Transform → Validate → Explore again». Codex escribió el flujo.", "Se aceptaron ocho etapas. Se rechazó imputar montos y puntajes sin base. Las llaves propuestas se validaron antes del panel.", "`analysis/pipeline_la_cisterna.py`, `outputs/controles_etapas.csv`, `outputs/perfil_fuentes.csv`."],
           ["Revisar cifras y PDF. Codex regeneró análisis, cuaderno y documento.", "Se aceptaron 110 PAS, 767 PME y 236/936 filas Agencia tras controles. Se corrigió la distinción fila/puntaje.", "`analysis/W1_analisis_ejecutado.ipynb`, `outputs/metricas.json`; render visual del PDF."]], [164, 182, 149]),
    h("Individual reflection", 2),
    p("<b>Pendiente de cada integrante.</b> Este apartado se completa personalmente después de revisar el workshop; no se redacta en nombre de ellos.", "SW"),
    PageBreak(),
    h("6. Vacíos, documentos siguientes y preguntas al profesor"),
    p("<b>Datos todavía no obtenidos:</b> rendiciones por RBD–año–subvención–cuenta para 2022–2024 y 2025 si existe cierre; gasto aceptado/rechazado, saldo y recurso; expedientes de PAS con materia financiera; facturas, recepción y uso de operaciones seleccionadas. El paquete contiene bases estadísticas públicas de la Agencia, pero no una colección de informes individuales por colegio. Los 17 establecimientos de educación especial requieren resultados pertinentes a su oferta, sin imputarles SIMCE cero."),
    p("<b>Selección de casos:</b> tras clasificar materia PAS y recibir rendiciones, priorizar gastos no aceptados o saldos sin acreditar con monto y estado verificables; incluir una muestra sin señal para evaluar falsas alarmas. Una multa es sanción, no importe malgastado. Un saldo sin ejecutar puede trasladarse. El resultado escolar posterior no prueba uso causal de una compra."),
    p("<b>Preguntas para feedback:</b> 1) ¿Es adecuado mantener educación especial en el censo financiero y separarla en resultados? 2) ¿Qué evidencia mínima exige C1 para pasar de PAS a hallazgo de gasto? 3) ¿La ventana de cuatro ejercicios es suficiente si 2025 aún no tiene rendición cerrada? 4) ¿Conviene que B permanezca como contexto o evaluarse como pregunta alternativa autónoma?"),
    h("Referencias y política oficial"),
    p("[1] DIPRES (2023), <i>Evaluación Subvención Escolar Preferencial. Informe final</i>, marzo de 2023; uso de recursos y procesos de rendición. " + link("https://www.dipres.gob.cl/597/articles-308400_informe_final.pdf", "Informe oficial"), "SW"),
    p("[2] Biblioteca del Congreso Nacional, <i>Ley 20.248 de Subvención Escolar Preferencial</i>, texto vigente consultado 25-09-2026; arts. 6–8, PME y rendición. " + link("https://www.bcn.cl/leychile/navegar?idNorma=269001", "Texto legal"), "SW"),
    p("[3] Agencia de Calidad (2026), <i>Preguntas frecuentes Simce y entrega de resultados educativos 2025</i>; información por establecimiento, grado, IDPS y comparación contextual. " + link("https://www.agenciaeducacion.cl/preguntas-frecuentes-simce/", "Página oficial"), "SW"),
    p("[4] Centro de Estudios Mineduc, <i>Directorio Oficial de Establecimientos Educacionales</i>, archivos 2022, 2023, 2024 y 2025, corte de matrícula anual. " + link("https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/", "Catálogo"), "SW"),
    p("[5] Mineduc, <i>Bases de datos PME, Implementación PME 2024</i>, archivo público y descripción de estimaciones declaradas. " + link("https://liderazgoeducativo.mineduc.cl/bases-de-datos-pme/", "Catálogo"), "SW"),
    p("[6] Superintendencia de Educación, <i>Procesos administrativos sancionatorios</i>, archivos 2022–2025 y diccionario. " + link("https://www.supereduc.cl/pas/", "Datos oficiales"), "SW"),
    p("[7] Agencia de Calidad, <i>Información Estadística</i>, bases públicas SIMCE e IDPS 2023–2025. " + link("https://informacionestadistica.agenciaeducacion.cl/", "Bases oficiales"), "SW"),
    p("Archivos de extracción, versiones y límites: `data/PROCEDENCIA.md`, `data/DICCIONARIO.md`, `data/fuentes.json` y `data/manifiesto_extraccion.json`. Cifras y controles: `analysis/outputs/`. El código permite reproducirlos sin conexión de red.", "SW"),
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#ccdade"))
    canvas.line(1.65*cm, 1.35*cm, A4[0]-1.65*cm, 1.35*cm)
    canvas.setFont(FONT, 7.2)
    canvas.setFillColor(colors.HexColor("#61747b"))
    canvas.drawString(1.7*cm, 1.1*cm, "GROUP_03_W1 | La Cisterna | 25-09-2026")
    canvas.drawRightString(A4[0]-1.7*cm, 1.1*cm, str(doc.page))
    canvas.restoreState()


PDF.parent.mkdir(exist_ok=True)
SimpleDocTemplate(str(PDF), pagesize=A4, leftMargin=1.7*cm, rightMargin=1.7*cm,
                  topMargin=1.55*cm, bottomMargin=1.75*cm,
                  title="GROUP_03_W1 - Recursos escolares en La Cisterna",
                  author="Javier Alcaíno, Lucas Riquelme y Renato Varela (Grupo 03)").build(story, onFirstPage=footer, onLaterPages=footer)
print(PDF)
