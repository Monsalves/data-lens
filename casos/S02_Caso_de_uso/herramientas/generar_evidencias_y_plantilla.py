# -*- coding: utf-8 -*-
"""Genera las evidencias simuladas y la plantilla rellena del caso S02.

Uso:  python generar_evidencias_y_plantilla.py
Parte de la plantilla publicada (copia; el original no se modifica).
"""
import csv
import math
import os
import shutil
from copy import copy

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

from caso_s02_expediente import *  # noqa: F401,F403

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# La plantilla publicada está en publicacion/data-lens/metodologia/ (espacio local) o en metodologia/ (repositorio data-lens).
_CANDIDATAS = [
    os.path.join(RAIZ, "..", "..", "..", "publicacion", "data-lens", "metodologia", "Plantilla_Assessment_Datos_F0_F3.xlsx"),
    os.path.join(RAIZ, "..", "..", "metodologia", "Plantilla_Assessment_Datos_F0_F3.xlsx"),
]
PLANTILLA_ORIGEN = next((os.path.abspath(c) for c in _CANDIDATAS if os.path.exists(c)), os.path.abspath(_CANDIDATAS[0]))
SALIDA_XLSX = os.path.join(RAIZ, "Plantilla_S02_Banco_Tinamu_Digital_rellena.xlsx")
EV_PATH = os.path.join(RAIZ, EVDIR)

BANNER_EV = (f"SIMULADO · {BANCO} (ficticio) · Tabla de trabajo ilustrativa. "
             "No es salida de AWS ni evidencia ejecutada en una cuenta real.")


# ------------------------------------------------------------------ evidencias
def escribir_csv(nombre, cabecera, filas):
    with open(os.path.join(EV_PATH, nombre), "w", newline="", encoding="utf-8") as f:
        f.write(f"# {BANNER_EV}\n")
        w = csv.writer(f)
        w.writerow(cabecera)
        w.writerows(filas)


def escribir_md(nombre, texto):
    with open(os.path.join(EV_PATH, nombre), "w", encoding="utf-8") as f:
        f.write(f"> **{BANNER_EV}**\n\n{texto.strip()}\n")


def generar_evidencias():
    os.makedirs(EV_PATH, exist_ok=True)
    for viejo in os.listdir(EV_PATH):
        os.remove(os.path.join(EV_PATH, viejo))

    sn = lambda b: "sí" if b else "no"
    # EV-01
    escribir_csv("inventario_observado.csv",
                 ["id_activo", "activo", "tipo", "en_catalogo", "lista_riesgo", "lista_producto", "lista_ti"],
                 [[f"A-{a['n']:02d}", a["nombre"], a["tipo"], sn(a["catalogado"]), sn("Riesgo" in a["listas"]),
                   sn("Producto" in a["listas"]), sn("TI" in a["listas"])] for a in ACTIVOS])
    # EV-02
    combos = {}
    for a in ACTIVOS:
        k = " + ".join(sorted(a["listas"])) if a["listas"] else "(ninguna)"
        combos[k] = combos.get(k, 0) + 1
    filas = "\n".join(f"| {k} | {v} |" for k, v in sorted(combos.items(), key=lambda x: -x[1]))
    sin_lista = ", ".join(f"`{a['nombre']}`" for a in ACTIVOS if not a["listas"])
    escribir_md("contraste_listas_areas.md", f"""
# EV-02 · Contraste de las listas de las áreas (corte {CORTE})

| Lista | Activos |
| --- | --- |
| Riesgo | {LISTA_N['Riesgo']} |
| Producto | {LISTA_N['Producto']} |
| TI | {LISTA_N['TI']} |

| Combinación de listas en que aparece el activo | Activos |
| --- | --- |
{filas}

- Activos observados en la cuenta: {N_ACT}. En las tres listas: {EN_LAS_TRES}. En al menos una: {EN_ALGUNA}. En ninguna: {EN_NINGUNA}.
- Activos en ninguna lista: {sin_lista}.
- Fuente de los activos: `inventario_observado.csv` (EV-01).
""")
    # EV-03
    escribir_csv("catalogo_responsables.csv", ["id_activo", "activo", "campo_responsable", "informado"],
                 [[f"A-{a['n']:02d}", a["nombre"], a["responsable"] or "", sn(bool(a["responsable"]))] for a in CATALOGO])
    # EV-04
    escribir_csv("catalogo_metadatos.csv", ["id_activo", "activo"] + CAMPOS_META + ["campos_informados_de_5"],
                 [[f"A-{a['n']:02d}", a["nombre"]] + [("vacío" if c in a["meta_faltante"] else "informado") for c in CAMPOS_META]
                  + [5 - len(a["meta_faltante"])] for a in CATALOGO])
    # EV-05
    escribir_csv("linaje_tramos.csv", ["tramo", "origen", "destino", "registrado_en_grafo"],
                 [[f"T-{i:02d}", o, d, sn(ok)] for i, (o, d, ok) in enumerate(TRAMOS, start=1)])
    # EV-06
    lista = "\n".join(f"{i}. `{o}` → `{d}`" for i, (o, d, _) in enumerate(TRAMOS, start=1))
    escribir_md("especificacion_flujo_modelo.md", f"""
# EV-06 · Diagrama de flujo de datos del modelo de preaprobación, v0.3 (documento simulado)

Autor: Arquitectura de {BANCO} (ficticio). Fecha del documento: 26-oct-2026. Es la lista independiente de tramos esperados que usa EXA-04.
Nivel de detalle: tabla o bucket.

Tramos esperados ({TR_TOT}):

{lista}
""")
    # EV-07
    escribir_csv("catalogo_clasificacion.csv", ["id_activo", "activo", "clasificacion_registrada", "informado"],
                 [[f"A-{a['n']:02d}", a["nombre"], a["clasificacion"] or "", sn(bool(a["clasificacion"]))] for a in CATALOGO])
    # EV-08
    escribir_md("acta_solicitud_facturacion.md", f"""
# EV-08 · Acta de la solicitud de facturación (documento simulado)

- **Fecha:** 05-nov-2026 (simulada).
- **Solicitud:** el equipo evaluador pide a Finanzas ({GONZALO}) y a Tecnología ({DANIELA}) el gasto mensual de AWS de los últimos 12 meses (nov-2025 a oct-2026),
  desglosado por servicio y por producto o etiqueta, incluido lo asociado al modelo.
- **Respuesta de Finanzas:** dispone de la factura mensual como documento, sin etiquetas de producto. No existe un reporte por producto.
- **Respuesta de Tecnología:** la consola de facturación está reservada a Finanzas; no se concedió acceso al rol de evaluación en este ciclo.
- **Qué se obtuvo:** nada que permita atribuir el gasto a un servicio o a un producto. Este acta no reproduce cifras de gasto.
- **Consecuencia:** EXA-06 no puede interpretarse. Estado: «Sin evidencia suficiente». El gasto no se midió.
- **Siguiente paso propuesto:** AC-05.
""")
    # EV-09
    escribir_csv("ciclo_de_vida_por_bucket.csv", ["bucket", "tipo_de_dato", "politica_supuesta", "regla_configurada", "coherente_con_politica"],
                 [[b[0], b[1], b[2], b[3], sn(b[4])] for b in BUCKETS_F02])
    # EV-10
    escribir_csv("versiones_clientes_baja.csv", ["prefijo", "objetos", "con_ultima_modificacion_anterior_al_05-nov-2024", "porcentaje"],
                 [[p, o, v, f"{v / o * 100:.1f}".replace(".", ",") + " %"] for p, o, v in BAJA_PREFIJOS]
                 + [["TOTAL tnm-sim-clientes-baja", BAJA_TOT, BAJA_VIEJOS, pct(BAJA_VIEJOS, BAJA_TOT)]])
    # EV-11
    escribir_csv("glue_ejecuciones_90d.csv",
                 ["job", "terminadas", "exitosas", "fallidas", "canceladas_fuera_del_calculo", "en_curso_fuera_del_calculo"],
                 [list(j) for j in JOBS] + [["TOTAL", RUN_TERM, RUN_OK, RUN_FAIL, RUN_STOP, RUN_ACT]])
    # EV-12
    tabla = "\n".join(f"| {b[0]} | {n(b[5])} | {b[6]} | {b[6] - b[7]} | {b[7]} |" for b in BUCKETS_F02)
    exc = []
    k = 1
    for b in BUCKETS_F02:
        for _ in range(b[7]):
            exc.append(f"| tnm-sim-muestra/{b[0]}/obj-sim-{k:04d} | {b[0]} | cifrado con clave gestionada por el servicio (no la del banco) |")
            k += 1
    escribir_md("muestra_cifrado_objetos.md", f"""
# EV-12 · Muestra de cifrado de objetos (tabla simulada)

Fecha de la revisión: 05-nov-2026 (simulada). Muestra aleatoria; el requisito (supuesto): cifrado en servidor con la clave del banco.

| Bucket | Objetos en el inventario | Objetos revisados | Conformes | No conformes |
| --- | --- | --- | --- | --- |
{tabla}
| **TOTAL** | **{n(INV_OBJ)}** | **{n(MUESTRA)}** | **{n(CIF_OK)}** | **{NC_CIFRADO}** |

Cobertura del inventario: {n(MUESTRA)} de {n(INV_OBJ)} objetos ({pct(MUESTRA, INV_OBJ)}), informada aparte como indica M-22.

## Objetos no conformes ({NC_CIFRADO})

| Clave simulada | Bucket | Motivo |
| --- | --- | --- |
{chr(10).join(exc)}
""")
    # EV-13
    escribir_csv("hallazgos_permisos_sin_uso.csv", ["id", "tipo", "rol_o_usuario", "dias_sin_uso", "se_relaciona_con_F-02"],
                 [[f"H-{i:02d}", h[0], h[1], h[2], sn(h[3])] for i, h in enumerate(HALLAZGOS, start=1)])
    # EV-14
    escribir_md("acta_acceso_auditoria.md", f"""
# EV-14 · Acta de la solicitud de acceso a los registros de auditoría (documento simulado)

- **Fecha:** 06-nov-2026 (simulada).
- **Solicitud:** leer el contenido de una muestra de archivos de log del bucket `tnm-sim-auditoria-trail` para comprobar los campos obligatorios (quién, qué, sobre qué recurso, cuándo y con qué resultado).
- **Respuesta de Seguridad ({NATALIA}):** el acceso al contenido de los logs está reservado a su equipo. La autorización para el rol de evaluación quedó pendiente de un comité interno posterior a la fecha de cierre de la revisión.
- **Declarado por Seguridad, sin verificar:** la auditoría de la cuenta está activa.
- **Qué se obtuvo:** ningún registro. No se calculó ninguna proporción.
- **Consecuencia:** EXA-11 no es verificable. Estado: «No verificable». No se interpreta como favorable ni desfavorable.
- **Siguiente paso propuesto:** AC-10.
""")
    return sorted(os.listdir(EV_PATH))


# ------------------------------------------------------------------ plantilla
def copiar_estilo(origen, destino):
    destino._style = copy(origen._style)


def limpiar(ws, r1, r2, c1, c2):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            cell = ws.cell(row=r, column=c)
            cell.value = None


def altura(ws, fila, cols, textos, minimo=18):
    lineas = 1
    for c, t in zip(cols, textos):
        if t is None:
            continue
        ancho = ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width or 12
        cap = max(8, int(ancho * 1.05))
        total = 0
        for parte in str(t).split("\n"):
            total += max(1, math.ceil(len(parte) / cap))
        lineas = max(lineas, total)
    ws.row_dimensions[fila].height = max(minimo, min(409, lineas * 14.5 + 4))


def escribir_fila(ws, fila, valores, col_ini=1, plantilla_celda=None):
    cols = list(range(col_ini, col_ini + len(valores)))
    for c, v in zip(cols, valores):
        cell = ws.cell(row=fila, column=c)
        cell.value = v
        if plantilla_celda is not None:
            copiar_estilo(plantilla_celda, cell)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    altura(ws, fila, cols, valores)


def banner(ws, celda="A3", ancho_hasta=None):
    c = ws[celda]
    c.value = AVISO
    c.font = Font(bold=True, color="9C4A00")
    c.fill = PatternFill("solid", fgColor="FFF3DB")
    c.alignment = Alignment(wrap_text=False, vertical="center")
    if ancho_hasta:
        for col in range(openpyxl.utils.column_index_from_string(celda[0]) + 1, ancho_hasta + 1):
            ws.cell(row=int(celda[1:]), column=col).fill = PatternFill("solid", fgColor="FFF3DB")


def f(a):  # fecha simulada
    return a


def ruta_ev(ev):
    # ev = (ID, RES, instrumento, archivo, contenido, fecha)
    return f"SIMULADO · ID SIM-S02-{ev[0]} · ruta: {EVDIR}/{ev[3]} · contiene: {ev[4]}"


def generar_plantilla():
    if not os.path.exists(PLANTILLA_ORIGEN):
        raise SystemExit(f"No se encuentra la plantilla de origen: {PLANTILLA_ORIGEN}")
    shutil.copyfile(PLANTILLA_ORIGEN, SALIDA_XLSX)
    wb = openpyxl.load_workbook(SALIDA_XLSX)
    hdr_estilo_celda = {}

    # ---------------- Guía de uso: el ejemplo de la guía pasa a ser el de este caso
    g = wb["Guía de uso"]
    g["A24"].value = ("Fuente evaluada: F-02 (buckets de datos de clientes) y F-01 (catálogo). Dos caminos independientes de ESTE caso ficticio muestran por qué "
                      "no todo diagnóstico exige una acción. Todos los datos son simulados.")
    g["D26"].value = ("F-02  →  REQ-09  →  EXA-09  →  EV-12 / RES-09  →  DX-07  →  sin acción obligatoria\n"
                      "Observación: 99,5 % de los objetos revisados con el cifrado exigido; cumple el criterio (≥ 99 %).")
    g["D29"].value = ("F-01  →  REQ-02  →  EXA-02  →  EV-03 / RES-02  →  DX-02  →  AC-02\n"
                      "Observación: 31 de 40 activos con responsable (77,5 %); no cumple el criterio (≥ 90 %); la acción es asignar y registrar responsable.")
    g["A47"].value = ("Antes de cerrar: comprueba que cada ID exista en su fase, que una evidencia respalde lo observado y que el criterio sea idéntico en F1 y F2. "
                      "En este ejemplo la «Regla aplicada» de F2 es copia literal del «Criterio» de F1 (comprobado con herramientas/verificar_caso_s02.py).")
    g["A49"].value = ("Notas: un resultado sin evidencia suficiente no debe presentarse como comprobado. Una acción puede no existir si el diagnóstico es favorable. "
                      "AVISO: ejemplo ilustrativo del caso Banco Tinamú Digital (ficticio); datos, resultados y evidencias simulados; sin pruebas ejecutadas en AWS.")

    for fila, alto in ((24, 34), (26, 34), (27, 34), (29, 34), (30, 34), (47, 34), (48, 34), (49, 52)):
        g.row_dimensions[fila].height = alto
    for celda in ("A24", "D26", "D29", "A47", "A49"):
        g[celda].alignment = Alignment(wrap_text=True, vertical="center")

    # ---------------- F0
    ws = wb["F0"]
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 38
    ws.column_dimensions["C"].width = 40.88
    ws.column_dimensions["D"].width = 42.38
    ws.column_dimensions["E"].width = 26
    ws.column_dimensions["F"].width = 46
    ws.column_dimensions["G"].width = 12
    banner(ws, "A3", 6)
    for fila, texto in F0_PREGUNTAS.items():
        ws.merge_cells(start_row=fila, start_column=2, end_row=fila, end_column=6)
        c = ws.cell(row=fila, column=2)
        c.value = texto
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=fila, column=1).alignment = Alignment(wrap_text=True, vertical="top")
        cap = 150
        ws.row_dimensions[fila].height = max(30, math.ceil(len(texto) / cap) * 14.5 + 6)
    limpiar(ws, 18, 24, 1, 7)
    limpiar(ws, 26, 40, 1, 7)
    base = ws["A18"]
    for i, fu in enumerate(F0_FUENTES):
        escribir_fila(ws, 18 + i, list(fu), 1)
    for i, r in enumerate(F0_REQ):
        escribir_fila(ws, 26 + i, [r[0], r[1], r[2], r[3]], 1)

    # ---------------- F1
    ws = wb["F1"]
    banner(ws, "A3", 6)
    for col, w in zip("ABCDEF", (14.25, 18, 20, 44, 46, 74)):
        ws.column_dimensions[col].width = w
    limpiar(ws, 5, 30, 1, 7)
    for i, e in enumerate(F1_EXA):
        escribir_fila(ws, 5 + i, [e[0], e[1], e[2], e[4], e[5], e[6]], 1)

    # ---------------- F2
    ws = wb["F2"]
    banner(ws, "A3", 5)
    for col, w in zip("ABCDE", (16, 19, 80, 56, 26)):
        ws.column_dimensions[col].width = w
    limpiar(ws, 5, 17, 1, 6)
    limpiar(ws, 19, 40, 1, 6)
    for i, r in enumerate(F2_RES):
        regla = EXA[r[1]][5]  # copia literal del criterio de F1
        escribir_fila(ws, 5 + i, [r[0], r[1], r[3], regla, r[2]], 1)
    for i, e in enumerate(F2_EV):
        escribir_fila(ws, 19 + i, [e[0], e[1], e[2], ruta_ev(e), f"{e[5]} (fecha simulada)"], 1)
    # el ancho de D sirve a ambas tablas; recalcular alturas de EV con D=56
    for i, e in enumerate(F2_EV):
        altura(ws, 19 + i, [3, 4], [e[2], ruta_ev(e)])

    # ---------------- F3
    ws = wb["F3"]
    banner(ws, "A3", 6)
    for col, w in zip("ABCDEF", (15.63, 23.38, 80, 70, 52, 20)):
        ws.column_dimensions[col].width = w
    hdr_ac = [copy(ws.cell(row=9, column=c)._style) for c in range(1, 7)]
    limpiar(ws, 5, 40, 1, 7)
    # fila 9 deja de ser encabezado de AC: se restablece al estilo de una celda vacía
    for c in range(1, 7):
        ws.cell(row=9, column=c)._style = copy(ws.cell(row=7, column=c)._style)
    for i, d in enumerate(F3_DX):
        escribir_fila(ws, 5 + i, [d[0], ", ".join(d[1]), d[2], d[3]], 1)
    fila_hdr = 5 + len(F3_DX) + 2   # 17
    for c, (txt, st) in enumerate(zip(("ID AC", "Diagnóstico relacionado", "Acción propuesta", "Prioridad", "Criterio de cierre", "Estado"), hdr_ac), start=1):
        cell = ws.cell(row=fila_hdr, column=c)
        cell.value = txt
        cell._style = copy(st)
    for i, a in enumerate(F3_AC):
        escribir_fila(ws, fila_hdr + 1 + i, [a[0], a[1], a[2], a[3], a[4], a[5]], 1)
    # D se usa para "Impacto / limitación" (70) y "Prioridad": el texto de prioridad es corto

    # ---------------- Matriz
    ws = wb["Matriz"]
    ws["A2"].value = AVISO
    ws["A2"].font = Font(bold=True, color="9C4A00")
    limpiar(ws, 4, 120, 1, 8)
    for c, w in zip("ABCDEFG", (14, 14, 12, 12, 12, 14, 12)):
        ws.column_dimensions[c].width = w
    filas = matriz()
    for i, fila in enumerate(filas):
        for c, v in enumerate(fila, start=1):
            ws.cell(row=4 + i, column=c).value = v
    for hoja in ("F0", "F1", "F2", "F3", "Matriz"):
        w_ = wb[hoja]
        w_.page_setup.orientation = "landscape"
        w_.page_setup.fitToWidth = 1
        w_.page_setup.fitToHeight = 0
        w_.sheet_properties.pageSetUpPr = openpyxl.worksheet.properties.PageSetupProperties(fitToPage=True)
    wb.save(SALIDA_XLSX)
    return len(filas)


if __name__ == "__main__":
    archivos = generar_evidencias()
    nfilas = generar_plantilla()
    print("evidencias:", len(archivos), "| filas de matriz:", nfilas)
