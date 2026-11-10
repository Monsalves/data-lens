# -*- coding: utf-8 -*-
"""Genera el documento de contexto del caso S02 en Markdown y Word desde un único modelo de bloques."""
import os
import re

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from caso_s02_expediente import *  # noqa: F401,F403

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MD = os.path.join(RAIZ, "Contexto_Caso_S02_Banco_Tinamu_Digital.md")
DOCX = os.path.join(RAIZ, "Contexto_Caso_S02_Banco_Tinamu_Digital.docx")
XLSX_NOMBRE = "Plantilla_S02_Banco_Tinamu_Digital_rellena.xlsx"

B = []  # bloques


def h(nivel, t): B.append(("h", nivel, t))
def p(t): B.append(("p", t))
def q(t): B.append(("q", t))
def ul(items): B.append(("ul", items))
def tabla(cab, filas, anchos=None): B.append(("t", cab, filas, anchos))


def corto(res_id):
    """Resumen corto de un resultado, para las tablas del documento."""
    r = RES[res_id]
    return r[2]


# ------------------------------------------------------------------ contenido
B.append(("title", "Caso de uso S02 · Banco Tinamú Digital",
          "¿Está el banco listo para lanzar un modelo de preaprobación de créditos? · Documento de contexto del caso · Versión 0.1 · " + FECHA_DOC))

q("**Ejemplo ilustrativo.** El banco, las personas, las cifras, los resultados y las evidencias de este documento son ficticios y simulados para explicar la metodología 1.4. "
  "No es una evaluación real, no hay pruebas ejecutadas en una cuenta AWS y no se promete cumplimiento normativo ni se cita normativa concreta. "
  "Los criterios de aceptación son supuestos del cliente ficticio.")

p(f"Este documento explica el contexto. Los datos del expediente (fuentes, requisitos, exámenes, evidencias, resultados, diagnósticos y acciones) están en la plantilla "
  f"`{XLSX_NOMBRE}` y las evidencias simuladas en la carpeta `{EVDIR}/`.")

h(2, "Cómo leer este ejemplo")
p("El expediente sigue un solo hilo: **necesidad → criterio → evidencia → hallazgo → recomendación**. Cada paso tiene un ID que se puede buscar en la plantilla. "
  "La regla de lectura es: el examen (EXA) comprueba, la evidencia (EV) respalda, el resultado (RES) describe lo observado, el diagnóstico (DX) interpreta y la acción (AC) dice qué hacer.")
p("Un recorrido completo, con los IDs reales del expediente:")
tabla(["Paso", "ID", "Qué dice en este caso"], [
    ["Necesidad (F0)", "REQ-07 · F-02", "«Los datos de clientes y de crédito deben conservarse solo el tiempo que indica la política de conservación.» Nace de las preocupaciones de costos y seguridad."],
    ["Criterio (F1)", "EXA-07", f"Al menos el 90 % de los buckets con una regla de eliminación coherente con la política (métrica M-29). Acordado el {FECHA_CRITERIOS}, antes de revisar. Es un supuesto del cliente ficticio."],
    ["Evidencia (F2)", "EV-09, EV-10", "Tabla de reglas por bucket y listado de objetos del bucket de clientes dados de baja. Ambas simuladas."],
    ["Resultado (F2)", "RES-07", f"{B_OK} de {B_TOT} buckets conformes ({pct(B_OK, B_TOT)}). Estado: No cumple."],
    ["Hallazgo (F3)", "DX-06", "Dos buckets sin regla de eliminación; uno guarda datos de clientes dados de baja y nadie lo tiene en su lista. Riesgo observado; costo solo como hipótesis."],
    ["Recomendación (F3)", "AC-07, AC-06, AC-08", "Primero proteger lo que sirva a una auditoría, luego separar lo que se conserva de lo que se elimina y al final eliminar."],
])
p("Otros finales posibles en el mismo expediente:")
ul([
    "**Favorable, sin acción:** REQ-09 → EXA-09 → RES-09 → DX-07. El cifrado de los objetos revisados cumple el criterio y no se crea ninguna acción.",
    "**No verificable:** REQ-11 → EXA-11 → RES-11 → DX-09 → AC-10. No se pudo leer el contenido de los registros de auditoría; el motivo queda explicado.",
    "**Sin evidencia suficiente:** REQ-06 → EXA-06 → RES-06 → DX-05 → AC-05. El gasto no se midió; las causas se presentan como hipótesis.",
    "**Descriptivo, sin umbral:** REQ-01 → EXA-01 → RES-01 → DX-01 → AC-01. Cuenta lo que existe y no emite estado de cumplimiento.",
])

h(2, "1. La organización y su situación")
p(f"{BANCO} es un banco digital ficticio, de tamaño mediano. No tiene sucursales: sus clientes abren cuentas, tarjetas y créditos de consumo desde una aplicación. "
  "Como referencia inventada para el ejemplo, tiene unas 600 personas y unos 380.000 clientes.")
p("El banco usa una sola cuenta de AWS. Allí el equipo de Datos e IA mantiene un catálogo de datos, un data lake y los datos con que quiere entrenar un modelo que preapruebe créditos. "
  "La Gerencia General quiere lanzar ese modelo este trimestre, antes del 31 de diciembre de 2026. Antes de decidir quiere saber en qué estado están sus datos.")

h(2, "2. La decisión y las tres preocupaciones (P-01 y P-02)")
p("**Problema y quién usa el resultado (P-01).** La Gerencia General y la Gerencia de Riesgo de Crédito usarán el resultado para decidir si lanzan el modelo.")
p("**Decisión que depende del resultado.** ¿Está el banco listo para lanzar este trimestre un modelo de preaprobación de créditos y qué debe corregir antes?")
p("**Las tres preocupaciones, tal como las declara el cliente:**")
tabla(["Preocupación", "En palabras del cliente", "REQ que la descomponen en F0"], [
    ["1. Control de activos", "«No sé con exactitud qué datos tengo, dónde están ni quién responde por ellos. Cada área me entrega una lista distinta.»", "REQ-01 a REQ-05"],
    ["2. Costos", "«La factura de AWS crece cada mes más que el negocio y nadie me dice qué parte es necesaria.»", "REQ-06 a REQ-08"],
    ["3. Seguridad", "«No sé si estamos listos para poner un modelo que aprueba créditos con datos de clientes, y no quiero enterarme de un problema después.»", "REQ-09 a REQ-11"],
])
p("**Creencias del cliente.** Se registran en F0 como declaradas y pendientes de confirmar. Una declaración no es una comprobación.")
tabla(["Creencia", "La declara", "Qué examen la contrasta"], [
    ["«El gasto sube por el modelo»", f"{GONZALO}, Finanzas", "EXA-06 (gasto por servicio y producto). Queda sin confirmar y sin descartar."],
    ["«Ciframos todo»", f"{DANIELA}, Tecnología", "EXA-09 (cifrado de objetos). Se confirma para los objetos de S3 revisados; no se verificó en otros almacenes."],
])
p("**Resultado esperado e indicadores de éxito (P-02).** Se considera logrado si (a) la Gerencia General puede decidir con una lista clara de condiciones, "
  "(b) cada preocupación tiene una respuesta o un límite explícito y (c) cada acción tiene prioridad y criterio de cierre.")

h(2, "3. Actores y referentes")
tabla(["Persona (ficticia)", "Rol", "Qué aporta o qué le importa"], [
    [ELENA, "Gerenta General", "Patrocina la decisión de lanzar el modelo."],
    [JOAQUIN, "Gerente de Riesgo de Crédito", "Usará el modelo; es responsable de negocio de los datos de originación y de scoring."],
    [DANIELA, "Gerenta de Tecnología", "Administra la cuenta AWS, las bases y los permisos."],
    [RODRIGO, "Jefe de Datos e IA", "Mantiene el catálogo, el data lake y los jobs que preparan los datos del modelo."],
    [NATALIA, "Oficial de Seguridad de la Información", "Define el cifrado y administra los registros de auditoría; autoriza su lectura."],
    [GONZALO, "Gerente de Finanzas", "Recibe la factura de AWS."],
    [ISABEL, "Jefa de Cumplimiento", "Debe indicar los plazos de conservación y los requisitos de privacidad."],
    ["Equipo evaluador", "Aplica la metodología", "Recoge la información, define exámenes y redacta el diagnóstico. Trabaja con un rol de solo lectura."],
])

h(2, "4. Las fuentes de datos y su estado actual (P-03 a P-06)")
p("**Qué fuentes necesita el caso, dónde están y qué formato tienen (P-03).** Son siete. El detalle por campo está en F0 de la plantilla; aquí solo se resume.")
tabla(["ID", "Qué es", "Dónde está", "Quién responde (declarado)"], [
    [x[0], x[1], x[2], x[5].split(". Sensibilidad")[0]] for x in F0_FUENTES
])
p("**Dificultades para obtener los datos (P-04).** Cada área guarda su lista de datos en hojas de cálculo propias y la entrega a pedido. Juntarlas toma varios días y varios correos. "
  "La factura de AWS llega a Finanzas como un documento mensual y hasta ahora no se ha pedido un reporte por producto. El contenido de los registros de auditoría solo lo lee Seguridad.")
p("**Frecuencia de actualización (P-05).** Hoy las listas de las áreas se actualizan cuando alguien las pide. El catálogo se revisa cada mes. Los jobs de preparación corren a diario o cada hora. "
  "El modelo necesitaría datos de solicitudes al día (lo declara Riesgo). Para este ejemplo se supone que el inventario debe poder revisarse cada trimestre.")
p("**Quién responde y quién autoriza el uso (P-06).** Datos e IA responde por el catálogo, el data lake y los jobs; Tecnología por la cuenta, las bases y los permisos; Seguridad por el cifrado y los registros de auditoría; "
  "Finanzas por la factura; Riesgo de Crédito por los datos de originación y de scoring; Cumplimiento por los plazos de conservación y la privacidad. "
  "Autoriza el uso de datos para el modelo Riesgo de Crédito junto con Cumplimiento (por confirmar). Quién responde por cada activo en particular es justamente una de las cosas que se examina (EXA-02).")

h(2, "5. Información sensible y requisitos regulatorios (P-07)")
p("Las fuentes contienen datos personales y financieros de clientes: identificación, contacto, ingresos declarados e historial de crédito. "
  "Los requisitos regulatorios que condicionan su uso deben ser indicados por Cumplimiento. Este ejemplo no cita normativa ni promete cumplimiento. "
  "Los plazos de conservación que usa son supuestos del cliente ficticio:")
ul([
    "extracciones temporales para modelado: 30 días;",
    "solicitudes de crédito: 12 meses;",
    "datos personales de clientes dados de baja: 24 meses;",
    "decisiones de crédito y contratos: 60 meses.",
])

h(2, "6. El entorno AWS")
ul([
    f"Una cuenta AWS (ID de ejemplo {CUENTA.split(' ')[0]}, no real). Región principal us-east-2; el cliente dice que no hay otras regiones activas, pendiente de confirmar.",
    "Servicios que intervienen: Amazon S3, AWS Glue, Amazon DataZone (catálogo y linaje), Amazon Aurora/RDS, Amazon DynamoDB, IAM con su analizador de acceso no utilizado, "
    "AWS CloudTrail y un entorno de pruebas del modelo.",
    "Activos de datos que existen según el descubrimiento simulado: 48 (12 buckets, 26 tablas Glue, 4 bases Aurora/RDS y 6 tablas DynamoDB).",
    "Acceso del equipo evaluador: rol de solo lectura sobre el catálogo, Glue, IAM y la configuración de S3, y revisión de metadatos de una muestra de objetos. "
    "No tiene acceso al contenido de los registros de auditoría ni a la consola de facturación.",
    "Importante: no se ejecutó nada en AWS. Las consultas que menciona el plan de medición son plantillas sin ejecutar; los resultados de este caso son tablas simuladas.",
])

h(2, "7. Qué se midió y qué quedó fuera")
p("Se usaron 9 métricas del piloto de 13, un examen descriptivo de inventario y un examen documental de gasto. Se respetan la fórmula, la unidad y el universo de cada métrica del plan de medición. "
  "M-21 es un conteo de hallazgos, no un porcentaje. Los criterios son supuestos del cliente ficticio, acordados antes de interpretar los resultados.")
crit_corto = {"EXA-01": "Sin umbral", "EXA-02": "≥ 90 %", "EXA-03": "≥ 85 %", "EXA-04": "≥ 80 %", "EXA-05": "≥ 95 %",
              "EXA-06": "Sin umbral; exige desglose de 12 meses", "EXA-07": "≥ 90 %", "EXA-08": "≥ 90 %", "EXA-09": "≥ 99 %",
              "EXA-10": "Máximo 5 hallazgos", "EXA-11": "≥ 98 %"}
res_corto = {"EXA-01": f"{N_ACT} activos; {len(NO_CAT)} sin catálogo; {EN_NINGUNA} sin lista",
             "EXA-02": f"{CON_RESP} de {N_CAT} ({pct(CON_RESP, N_CAT)})", "EXA-03": f"{PARES_OK} de {N_PARES} ({pct(PARES_OK, N_PARES)})",
             "EXA-04": f"{TR_OK} de {TR_TOT} ({pct(TR_OK, TR_TOT)})", "EXA-05": f"{CON_CLASIF} de {N_CAT} ({pct(CON_CLASIF, N_CAT)})",
             "EXA-06": "Gasto no medido", "EXA-07": f"{B_OK} de {B_TOT} ({pct(B_OK, B_TOT)})",
             "EXA-08": f"{RUN_OK} de {RUN_TERM} ({pct(RUN_OK, RUN_TERM)})", "EXA-09": f"{n(CIF_OK)} de {n(MUESTRA)} ({pct(CIF_OK, MUESTRA)})",
             "EXA-10": f"{H_TOT} hallazgos", "EXA-11": "Sin lectura de registros"}
metr = {"EXA-01": "Descriptivo", "EXA-06": "Documental (sin métrica)"}
unidad = {"M-01": "% cobertura", "M-07": "% completitud", "M-09": "% cobertura", "M-26": "% cobertura", "M-29": "% conformidad",
          "M-16": "% éxito", "M-21": "conteo", "M-22": "% conformidad", "M-25": "% completitud"}
preoc = {1: "1 · Control de activos", 2: "2 · Costos", 3: "3 · Seguridad"}
req_pre = {r[0]: r[4] for r in F0_REQ}
filas = []
for e in F1_EXA:
    r = [x for x in F2_RES if x[1] == e[0]][0]
    m = e[3]
    mtxt = f"{m} ({unidad[m]})" if m else metr[e[0]]
    if e[0] in ("EXA-07", "EXA-08"):
        mtxt += ", indirecta"
    filas.append([preoc[req_pre[e[1]]], f"{e[1]} → {e[0]}", mtxt, crit_corto[e[0]], res_corto[e[0]], r[2]])
tabla(["Preocupación", "REQ → EXA", "Métrica (unidad)", "Criterio supuesto", "Resultado simulado", "Estado final"], filas)
p("**Por qué las otras cuatro métricas del piloto quedan fuera:**")
tabla(["Métrica", "Por qué no se usa en este caso"], [
    ["M-04 · Solicitudes y concesiones por estado", "Responde cómo se tramitan los permisos de acceso a datos en DataZone. Ninguna de las tres preocupaciones lo pregunta, y en este caso el banco gestiona los accesos fuera de DataZone, así que la métrica no tendría universo."],
    ["M-11 · Nulos y ausentes", "Mide la calidad del contenido de una tabla. Las tres preocupaciones se refieren a control, costos y seguridad, no al contenido. Queda como siguiente paso recomendable antes de entrenar el modelo."],
    ["M-18 · Cobertura de controles de salida", "Necesita una lista previa de controles de calidad acordada con el cliente, que este caso no tiene; la calidad queda fuera de las tres preocupaciones."],
    ["M-27 · Casos infractores con acción esperada", "Prueba filtros de privacidad de IA generativa con casos sintéticos y requiere autorización específica. El modelo de preaprobación no es generativo y no usa ese filtro."],
])
p("**Sobre el gasto.** Ninguna de las métricas aplicadas mide gasto. M-29 y M-16 son indicios indirectos (datos guardados de más y trabajo que podría repetirse), no mediciones del costo. "
  "Por eso el examen de gasto (EXA-06) termina como «Sin evidencia suficiente», el diagnóstico dice que el gasto no se midió y las causas se presentan como hipótesis. El ejemplo no incluye ninguna cifra de ahorro.")

h(2, "8. Restricciones, límites y dudas abiertas")
tabla(["Duda o límite", "Responsable", "Siguiente paso"], [
    ["Los plazos de conservación son supuestos del cliente ficticio.", ISABEL + " (Cumplimiento)", "Validarlos antes de AC-06 y AC-08."],
    ["Que no haya otras regiones ni cuentas es lo que declara el cliente; no se verificó.", DANIELA + " (Tecnología)", "Confirmarlo al repetir el inventario (AC-01)."],
    ["No se leyó el contenido de los registros de auditoría.", NATALIA + " (Seguridad)", "Acordar un acceso controlado de solo lectura (AC-10)."],
    ["No se tuvo acceso a la facturación; el gasto no se midió.", GONZALO + " (Finanzas)", "Entregar el desglose mensual de 12 meses (AC-05)."],
    ["No se sabe qué parte de los servicios de pruebas del modelo consume recursos hoy.", RODRIGO + " (Datos e IA)", "Listar los servicios que usa el entorno de pruebas, como insumo de AC-05."],
    ["«Ciframos todo» se confirma solo para los objetos de S3 revisados; bases y respaldos no se revisaron.", DANIELA + " (Tecnología)", "Decidir si se amplía el alcance en una segunda revisión."],
    ["La fecha de baja de cada cliente no está en S3; no se puede confirmar cuántos objetos pasaron el plazo de 24 meses.", JOAQUIN + " (Riesgo de Crédito)", "Aportar las fechas de baja como parte de AC-06."],
    ["No se evaluó la calidad del contenido de los datos ni el comportamiento o la equidad del modelo.", "Gerencia General", "Decidir si se incluyen en una segunda revisión."],
])
p("**Restricciones.** Plazo de la decisión: antes del 31 de diciembre de 2026. Trabajo con un rol de solo lectura. Todo dato, resultado y evidencia es simulado. "
  "Los criterios de aceptación son supuestos. No se cita normativa ni se afirma cumplimiento.")

h(2, "9. Dónde está cada cosa")
ul([
    f"`{XLSX_NOMBRE}`: plantilla 1.4 rellena (Guía de uso, F0, F1, F2, F3 y Matriz).",
    f"`{EVDIR}/`: 14 evidencias simuladas, una por cada ID EV de F2 (cada archivo lo indica en su primera línea).",
    "`herramientas/`: modelo de datos y scripts que generan las cifras y comprueban la trazabilidad (`verificar_caso_s02.py`).",
])


# ------------------------------------------------------------------ render Markdown
def esc(s):
    return s.replace("|", "\\|")


def render_md():
    out = []
    for b in B:
        k = b[0]
        if k == "title":
            out.append(f"# {b[1]}\n\n*{b[2]}*\n")
        elif k == "h":
            out.append(f"{'#' * b[1]} {b[2]}\n")
        elif k == "p":
            out.append(b[1] + "\n")
        elif k == "q":
            out.append("> " + b[1] + "\n")
        elif k == "ul":
            out.append("\n".join(f"- {i}" for i in b[1]) + "\n")
        elif k == "t":
            cab, filas = b[1], b[2]
            lin = ["| " + " | ".join(cab) + " |", "| " + " | ".join("---" for _ in cab) + " |"]
            for f_ in filas:
                lin.append("| " + " | ".join(esc(str(x)) for x in f_) + " |")
            out.append("\n".join(lin) + "\n")
    with open(MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))


# ------------------------------------------------------------------ render Word
TOK = re.compile(r"(\*\*.+?\*\*|`.+?`|\*[^*]+?\*)")


def runs(par, texto, size=None, color=None):
    for parte in TOK.split(texto):
        if not parte:
            continue
        if parte.startswith("**") and parte.endswith("**"):
            r = par.add_run(parte[2:-2]); r.bold = True
        elif parte.startswith("`") and parte.endswith("`"):
            r = par.add_run(parte[1:-1]); r.font.name = "Consolas"; r._element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
        elif parte.startswith("*") and parte.endswith("*") and len(parte) > 2:
            r = par.add_run(parte[1:-1]); r.italic = True
        else:
            r = par.add_run(parte)
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor(*color)


def sombrear(cell, hex_):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hex_)
    tcPr.append(shd)


def render_docx():
    d = Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(1.8)
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    st = d.styles["Normal"]
    st.font.name = "Calibri"; st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    for nivel, tam in ((1, 20), (2, 14), (3, 12)):
        hs = d.styles[f"Heading {nivel}"]
        hs.font.name = "Calibri"; hs.font.size = Pt(tam); hs.font.color.rgb = RGBColor(0x18, 0x3B, 0x5A)
        hs.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    for b in B:
        k = b[0]
        if k == "title":
            d.add_heading(b[1], level=1)
            par = d.add_paragraph(); runs(par, b[2], size=11, color=(0x55, 0x55, 0x55)); par.runs[0].italic = True
        elif k == "h":
            d.add_heading(b[2], level=b[1])
        elif k == "p":
            par = d.add_paragraph(); runs(par, b[1]); par.paragraph_format.space_after = Pt(6)
        elif k == "q":
            t = d.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
            c = t.rows[0].cells[0]; sombrear(c, "FFF3DB")
            c.paragraphs[0].text = ""
            runs(c.paragraphs[0], b[1], size=10)
            d.add_paragraph()
        elif k == "ul":
            for item in b[1]:
                par = d.add_paragraph(style="List Bullet"); runs(par, item)
        elif k == "t":
            cab, filas = b[1], b[2]
            t = d.add_table(rows=1, cols=len(cab)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
            for i, x in enumerate(cab):
                c = t.rows[0].cells[i]; c.text = ""
                runs(c.paragraphs[0], f"**{x}**", size=9); sombrear(c, "DCE9F5")
            for f_ in filas:
                cells = t.add_row().cells
                for i, x in enumerate(f_):
                    cells[i].text = ""
                    runs(cells[i].paragraphs[0], str(x), size=9)
            # anchos proporcionales al contenido (17,4 cm útiles)
            largo = [max([len(str(cab[i]))] + [min(len(str(f_[i])), 120) for f_ in filas]) for i in range(len(cab))]
            largo = [max(l, 10) for l in largo]
            total = sum(largo)
            t.autofit = False
            for i in range(len(cab)):
                w = Cm(max(1.8, 17.4 * largo[i] / total))
                t.columns[i].width = w
                for row in t.rows:
                    row.cells[i].width = w
            # repetir encabezado
            trPr = t.rows[0]._tr.get_or_add_trPr(); th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)
            d.add_paragraph()
    d.core_properties.title = "Caso de uso S02 · Banco Tinamú Digital (ficticio)"
    d.core_properties.author = "Equipo evaluador del ejemplo S02"
    d.save(DOCX)


if __name__ == "__main__":
    render_md()
    render_docx()
    print("documento generado")
