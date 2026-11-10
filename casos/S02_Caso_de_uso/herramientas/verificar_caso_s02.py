# -*- coding: utf-8 -*-
"""Comprueba la trazabilidad del caso S02 leyendo los archivos entregados (no el modelo de datos).

Uso: python verificar_caso_s02.py   (escribe el informe en la salida estándar)
"""
import csv
import hashlib
import os
import re
import sys

import openpyxl
from docx import Document

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
XLSX = os.path.join(RAIZ, "Plantilla_S02_Banco_Tinamu_Digital_rellena.xlsx")
MD = os.path.join(RAIZ, "Contexto_Caso_S02_Banco_Tinamu_Digital.md")
DOCX = os.path.join(RAIZ, "Contexto_Caso_S02_Banco_Tinamu_Digital.docx")
_CANDIDATAS = [
    os.path.join(RAIZ, "..", "..", "..", "publicacion", "data-lens", "metodologia", "Plantilla_Assessment_Datos_F0_F3.xlsx"),
    os.path.join(RAIZ, "..", "..", "metodologia", "Plantilla_Assessment_Datos_F0_F3.xlsx"),
]
ORIGEN = next((os.path.abspath(c) for c in _CANDIDATAS if os.path.exists(c)), os.path.abspath(_CANDIDATAS[0]))

fallos, ok = [], []


def chk(cond, msg):
    (ok if cond else fallos).append(msg)


def tabla(ws, fila_ini, ncols, fila_fin=None):
    filas = []
    r = fila_ini
    while True:
        vals = [ws.cell(row=r, column=c).value for c in range(1, ncols + 1)]
        if vals[0] in (None, "") or (fila_fin and r > fila_fin):
            break
        filas.append([("" if v is None else str(v)) for v in vals])
        r += 1
    return filas


wb = openpyxl.load_workbook(XLSX)
chk(wb.sheetnames == ["Guía de uso", "F0", "F1", "F2", "F3", "Matriz"], f"Hojas: {wb.sheetnames}")

# ---- cabeceras iguales a la plantilla original
wo = openpyxl.load_workbook(ORIGEN)
def cab(ws, fila, n):
    return [ws.cell(row=fila, column=c).value for c in range(1, n + 1)]
for hoja, fila, n in (("F0", 4, 2), ("F0", 17, 6), ("F0", 25, 4), ("F1", 4, 6), ("F2", 4, 5), ("F2", 18, 5), ("F3", 4, 4), ("Matriz", 3, 7)):
    chk(cab(wb[hoja], fila, n) == cab(wo[hoja], fila, n), f"Cabecera de {hoja} fila {fila} igual a la plantilla")
chk([wb["F3"].cell(row=17, column=c).value for c in range(1, 7)] == cab(wo["F3"], 9, 6), "Cabecera de AC en F3 igual a la plantilla (movida a la fila 17)")

F = tabla(wb["F0"], 18, 6, fila_fin=24)
REQ = tabla(wb["F0"], 26, 4)
EXA = tabla(wb["F1"], 5, 6)
RES = tabla(wb["F2"], 5, 5)
EV = tabla(wb["F2"], 19, 5)
DX = tabla(wb["F3"], 5, 4)
AC = tabla(wb["F3"], 18, 6)
MZ = tabla(wb["Matriz"], 4, 7)

fid = {r[0] for r in F}; rid = {r[0] for r in REQ}; eid = {r[0] for r in EXA}
sid = {r[0] for r in RES}; vid = {r[0] for r in EV}; did = {r[0] for r in DX}; aid = {r[0] for r in AC}
print(f"F={len(F)} REQ={len(REQ)} EXA={len(EXA)} RES={len(RES)} EV={len(EV)} DX={len(DX)} AC={len(AC)} Matriz={len(MZ)}")

# ---- formatos e IDs únicos
for nombre, lista, pat in (("F", F, r"F-\d{2}"), ("REQ", REQ, r"REQ-\d{2}"), ("EXA", EXA, r"EXA-\d{2}"), ("RES", RES, r"RES-\d{2}"),
                           ("EV", EV, r"EV-\d{2}"), ("DX", DX, r"DX-\d{2}"), ("AC", AC, r"AC-\d{2}")):
    ids = [r[0] for r in lista]
    chk(all(re.fullmatch(pat, i) for i in ids), f"Formato de ID {nombre}")
    chk(len(ids) == len(set(ids)), f"IDs {nombre} únicos")

# ---- F0 -> F1: la fuente de F1 corresponde al vínculo de F0
req_f = {r[0]: r[1] for r in REQ}
chk(all(f in fid for f in req_f.values()), "Cada REQ apunta a una fuente existente en F0")
chk(all(r[1] in rid for r in EXA), "Cada EXA apunta a un REQ existente")
chk(all(r[2] in fid for r in EXA), "Cada EXA apunta a una fuente existente")
chk(all(r[2] == req_f[r[1]] for r in EXA), "La fuente de F1 corresponde al vínculo de F0 (REQ->F)")
chk(all(any(e[1] == q for e in EXA) for q in rid), "Cada REQ tiene al menos un examen")
chk(all(any(r[1] == f for r in REQ) for f in fid), "Cada fuente sirve a al menos un REQ")
# ---- F1 -> F2
chk(all(r[1] in eid for r in RES), "Cada RES apunta a un EXA existente")
chk(all(any(r[1] == e for r in RES) for e in eid), "Cada EXA tiene un resultado")
crit = {e[0]: e[4] for e in EXA}
chk(all(r[3] == crit[r[1]] for r in RES), "La regla aplicada en F2 es idéntica al criterio de F1 (todos los RES)")
estados = {"Cumple", "No cumple", "No verificable", "Sin evidencia suficiente", "Descriptivo (sin estado de cumplimiento)"}
chk(all(r[4] in estados for r in RES), "Estados válidos en F2")
chk(all("Sin casos" != r[4] for r in RES), "No se usa «Sin casos» (no se comprobó población cero)")
# ---- EV -> RES
chk(all(r[1] in sid for r in EV), "Cada EV respalda un RES existente")
chk(all(any(e[1] == s for e in EV) for s in sid), "Cada RES tiene al menos una EV")
carpeta_ev = RAIZ
for e in EV:
    m = re.search(r"ruta: (\S+)", e[3])
    existe = bool(m) and os.path.exists(os.path.join(carpeta_ev, m.group(1)))
    chk(existe and "SIMULADO" in e[3] and f"SIM-S02-{e[0]}" in e[3], f"{e[0]}: ruta recuperable y marcada como simulada")
    if m and existe:
        txt = open(os.path.join(carpeta_ev, m.group(1)), encoding="utf-8").read(400)
        chk("SIMULADO" in txt, f"{e[0]}: el archivo declara que es simulado")
# ---- F3
res_text = {r[0]: r[2] for r in RES}
for d in DX:
    refs = [x.strip() for x in d[1].split(",")]
    chk(all(x in sid for x in refs), f"{d[0]}: resultados existentes")
chk(all(a[1] in did for a in AC), "Cada AC apunta a un DX existente")
dx_con_ac = {a[1] for a in AC}
dx_sin_ac = sorted(did - dx_con_ac)
print("DX sin acción:", dx_sin_ac)
chk(len(dx_sin_ac) >= 1, "Hay al menos un diagnóstico (resultado favorable) sin acción")
# resultado favorable sin ninguna acción en ningún camino
favorables = [r[0] for r in RES if r[4] == "Cumple"]
sin_accion = []
for rr in favorables:
    dxs = [d[0] for d in DX if rr in [x.strip() for x in d[1].split(",")]]
    if all(d not in dx_con_ac for d in dxs):
        sin_accion.append(rr)
print("Resultados favorables sin acción en ningún camino:", sin_accion)
chk(len(sin_accion) >= 1, "Al menos un resultado favorable queda sin acción")
chk(all(a[3] and a[4] and a[5] for a in AC), "Toda acción tiene prioridad, criterio de cierre y estado")
chk(all(a[5] == "Propuesta" for a in AC), "Ninguna acción se presenta como ejecutada")
# ---- Matriz
dx_res = {d[0]: [x.strip() for x in d[1].split(",")] for d in DX}
ac_dx = {a[0]: a[1] for a in AC}
exa_req = {e[0]: e[1] for e in EXA}; res_exa = {r[0]: r[1] for r in RES}; ev_res = {e[0]: e[1] for e in EV}
bien = True
for m in MZ:
    f_, rq, ex, rs, ev, dx, ac = m
    c = (f_ in fid and rq in rid and ex in eid and rs in sid and ev in vid and dx in did and (ac == "—" or ac in aid))
    c = c and req_f[rq] == f_ and exa_req[ex] == rq and res_exa[rs] == ex and ev_res[ev] == rs and rs in dx_res[dx] and (ac == "—" or ac_dx[ac] == dx)
    if not c:
        bien = False; print("Fila de matriz inconsistente:", m)
chk(bien, "Cada fila de la matriz es un camino coherente")
chk({m[4] for m in MZ} == vid, "Todas las EV aparecen en la matriz")
chk({m[5] for m in MZ} == did, "Todos los DX aparecen en la matriz")
chk({m[6] for m in MZ if m[6] != "—"} == aid, "Todas las AC aparecen en la matriz")
chk({m[1] for m in MZ} == rid, "Todos los REQ aparecen en la matriz")

# ---- las cifras de F2 se recomputan desde las evidencias
def leer_csv(nombre):
    with open(os.path.join(RAIZ, "evidencias_simuladas", nombre), encoding="utf-8") as fh:
        lin = [l for l in fh if not l.startswith("#")]
    return list(csv.DictReader(lin))

def pc(a, b):
    return f"{a / b * 100:.1f}".replace(".", ",") + " %"

r = leer_csv("catalogo_responsables.csv"); a = sum(1 for x in r if x["informado"] == "sí")
chk(f"{a} de {len(r)} activos catalogados con responsable ({pc(a, len(r))})" in res_text["RES-02"], f"RES-02 coincide con EV-03 ({a}/{len(r)})")
r = leer_csv("catalogo_metadatos.csv"); campos = [c for c in r[0] if c not in ("id_activo", "activo", "campos_informados_de_5")]
tot = len(r) * len(campos); a = sum(1 for x in r for c in campos if x[c] == "informado")
chk(f"{a} de {tot} pares activo-campo informados ({pc(a, tot)})" in res_text["RES-03"], f"RES-03 coincide con EV-04 ({a}/{tot})")
r = leer_csv("linaje_tramos.csv"); a = sum(1 for x in r if x["registrado_en_grafo"] == "sí")
chk(f"{a} de {len(r)} tramos esperados con linaje registrado ({pc(a, len(r))})" in res_text["RES-04"], f"RES-04 coincide con EV-05 ({a}/{len(r)})")
r = leer_csv("catalogo_clasificacion.csv"); a = sum(1 for x in r if x["informado"] == "sí")
chk(f"{a} de {len(r)} activos catalogados con clasificación registrada ({pc(a, len(r))})" in res_text["RES-05"], f"RES-05 coincide con EV-07 ({a}/{len(r)})")
r = leer_csv("ciclo_de_vida_por_bucket.csv"); a = sum(1 for x in r if x["coherente_con_politica"] == "sí")
chk(f"{a} de {len(r)} buckets con regla de conservación coherente ({pc(a, len(r))})" in res_text["RES-07"], f"RES-07 coincide con EV-09 ({a}/{len(r)})")
r = [x for x in leer_csv("glue_ejecuciones_90d.csv") if x["job"] != "TOTAL"]
t = sum(int(x["terminadas"]) for x in r); a = sum(int(x["exitosas"]) for x in r)
chk(t == a + sum(int(x["fallidas"]) for x in r), "EV-11: terminadas = exitosas + fallidas")
chk(f"{a} de {t} ejecuciones terminadas con éxito ({pc(a, t)})" in res_text["RES-08"], f"RES-08 coincide con EV-11 ({a}/{t})")
r = leer_csv("hallazgos_permisos_sin_uso.csv")
chk(f"{len(r)} hallazgos activos de permisos sin uso" in res_text["RES-10"], f"RES-10 coincide con EV-13 ({len(r)})")
chk("%" not in res_text["RES-10"].split("hallazgos activos")[0], "RES-10 es un conteo, sin porcentaje")
inv = leer_csv("inventario_observado.csv")
chk(f"Se observaron {len(inv)} activos" in res_text["RES-01"], f"RES-01 coincide con EV-01 ({len(inv)})")
chk(sum(1 for x in inv if x["en_catalogo"] == "sí") == 40, "EV-01: 40 activos catalogados (universo de M-01/M-07/M-26)")
muestra = open(os.path.join(RAIZ, "evidencias_simuladas", "muestra_cifrado_objetos.md"), encoding="utf-8").read()
chk("**2.400**" in muestra and "**2.388**" in muestra and "**12**" in muestra, "EV-12: 2.400 revisados, 2.388 conformes, 12 no conformes")
chk("2.388 de 2.400 objetos revisados" in res_text["RES-09"], "RES-09 coincide con EV-12")
chk(res_text["RES-06"].count("%") == 0 and not re.search(r"\d{2,}", res_text["RES-06"]), "RES-06 no contiene cifras de gasto")

# ---- términos que no debe usar el cliente en F0
f0 = wb["F0"]
cliente = " ".join(str(f0.cell(row=r_, column=2).value or "") for r_ in (7, 10, 11, 12))
chk(not re.search(r"nulo|ca[ií]d[oa]|sin cifr|falta de cifrado|no cifrad", cliente, re.I), "Las descripciones del cliente (F0) no nombran fallos técnicos evidentes")
chk("«No sé con exactitud qué datos tengo, dónde están ni quién responde por ellos. Cada área me entrega una lista distinta.»" in cliente, "Preocupación 1 literal en F0")
chk("«La factura de AWS crece cada mes más que el negocio y nadie me dice qué parte es necesaria.»" in cliente, "Preocupación 2 literal en F0")
chk("«No sé si estamos listos para poner un modelo que aprueba créditos con datos de clientes, y no quiero enterarme de un problema después.»" in cliente, "Preocupación 3 literal en F0")
chk("PENDIENTES DE CONFIRMAR" in cliente and "«el gasto sube por el modelo»" in cliente and "«ciframos todo»" in cliente, "Creencias registradas como declaradas y pendientes")

# ---- métricas usadas
usadas = set(re.findall(r"M-\d{2}", " ".join(e[5] + e[3] for e in EXA)))
chk(usadas == {"M-01", "M-07", "M-09", "M-16", "M-21", "M-22", "M-25", "M-26", "M-29"}, f"Métricas en F1: {sorted(usadas)}")
chk(not (usadas & {"M-04", "M-11", "M-18", "M-27"}) or all(
    re.findall(r"M-(?:04|11|18|27)", e[3] + e[4]) == [] for e in EXA), "M-04, M-11, M-18 y M-27 no se usan como métricas en F1")

# ---- documento: IDs, sincronía md/docx
md = open(MD, encoding="utf-8").read()
ids_doc = set(re.findall(r"\b(?:F|REQ|EXA|RES|EV|DX|AC)-\d{2}\b", md))
todos = fid | rid | eid | sid | vid | did | aid
chk(ids_doc <= todos, f"Todos los IDs del documento existen en el expediente (faltan: {sorted(ids_doc - todos)})")
chk("Cómo leer este ejemplo" in md, "Sección «Cómo leer este ejemplo»")
for k in ("P-01", "P-02", "P-03", "P-04", "P-05", "P-06", "P-07"):
    chk(k in md, f"El documento sigue {k}")
if not os.path.exists(DOCX):
    print("AVISO: no hay .docx en esta ubicación (el repositorio publica solo Markdown); se omite la comprobación de sincronía md/Word.")
    dx = None
else:
    dx = Document(DOCX)
texto_docx = []
for blk in (dx.element.body.iterchildren() if dx is not None else []):
    if blk.tag.endswith("}p"):
        texto_docx.append("".join(t.text or "" for t in blk.iter() if t.tag.endswith("}t")))
    elif blk.tag.endswith("}tbl"):
        for tr in blk.iter():
            if tr.tag.endswith("}tc"):
                texto_docx.append("".join(t.text or "" for t in tr.iter() if t.tag.endswith("}t")))
plano_docx = re.sub(r"\s+", " ", " ".join(texto_docx))
def plano_md(s):
    s = s.replace("\\|", "¦").replace("**", "").replace("`", "")
    s = re.sub(r"^\*(.*)\*$", r"\1", s, flags=re.M)    # línea en cursiva (subtítulo)
    s = re.sub(r"(?<=\w)\*|\*(?=\w)", "", s)           # cursivas pegadas a palabras
    s = re.sub(r"^\s*>\s?", "", s, flags=re.M)         # citas
    s = re.sub(r"^#+\s", "", s, flags=re.M)            # títulos
    s = re.sub(r"^\s*- ", "", s, flags=re.M)           # viñetas
    s = re.sub(r"^\|\s*(---\s*\|\s*)+$", " ", s, flags=re.M)
    s = s.replace("|", " ").replace("¦", "|")
    return re.sub(r"\s+", " ", s)
palabras_md = plano_md(md).split()
palabras_docx = set(plano_docx.split())
faltan = [w for w in palabras_md if w not in palabras_docx and w.strip("-| ") not in ("", "---")]
if dx is not None:
    chk(len(faltan) == 0, f"Md y Word contienen las mismas palabras (diferencias: {faltan[:8]})")
    chk(len(md.split("\n## ")) - 1 == len([p for p in dx.paragraphs if p.style.name == "Heading 2"]), "Mismo número de secciones en md y Word")
    chk(len(re.findall(r"^\| --- ", md, flags=re.M)) == len(dx.tables) - len([1 for t in dx.tables if len(t.columns) == 1]), "Mismo número de tablas en md y Word")

# ---- el original no se modificó
chk(hashlib.sha256(open(ORIGEN, "rb").read()).hexdigest() != hashlib.sha256(open(XLSX, "rb").read()).hexdigest(), "La copia difiere del original (el original no se tocó)")
chk(wo.sheetnames == ["Guía de uso", "F0", "F1", "F2", "F3", "Matriz"] and wo["F0"]["A18"].value == "F-01" and wo["F0"]["B18"].value == "Datos_historicos", "El original conserva su contenido de ejemplo")

for m in ok:
    print("OK     ", m)
for m in fallos:
    print("FALLO  ", m)
print(f"\n{len(ok)} comprobaciones correctas, {len(fallos)} fallos")
sys.exit(1 if fallos else 0)
