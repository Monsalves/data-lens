# -*- coding: utf-8 -*-
"""Modelo de datos del caso S02 (Banco Tinamú Digital, ficticio).

TODO es ilustrativo y simulado. Este módulo es la fuente única de las cifras:
las evidencias, la plantilla y el documento de contexto se generan desde aquí.
"""
import math

BANCO = "Banco Tinamú Digital"
CASO_ID = "S02-TINAMU"
CORTE = "02-nov-2026"
FECHA_CRITERIOS = "29-oct-2026"
FECHA_DOC = "9 de noviembre de 2026"
SUP = "SUPUESTO del cliente ficticio, acordado el 29-oct-2026 antes de revisar"


def n(x):
    """Entero con punto de miles (formato español)."""
    return f"{x:,}".replace(",", ".")


def pct(a, b, dec=1):
    return f"{a / b * 100:.{dec}f}".replace(".", ",") + " %"


# ---------------------------------------------------------------- activos
RDS = ["tnm-sim-aurora-core", "tnm-sim-aurora-originacion", "tnm-sim-aurora-crm", "tnm-sim-aurora-riesgo"]
GLUE = {
    "originacion": ["solicitudes_curado", "solicitantes", "consultas_buro", "ofertas_historicas",
                    "decisiones_credito", "garantias", "productos_credito", "canales_captacion",
                    "features_solicitante"],
    "clientes": ["clientes_activos", "cuentas", "contactos", "productos_contratados", "bajas_clientes",
                 "segmentos", "consentimientos", "movimientos_resumen", "transacciones_diarias"],
    "riesgo": ["scoring_historico", "ingresos_declarados", "mora_mensual", "limites_credito",
               "alertas_fraude", "politicas_riesgo", "cartera_resumen", "indicadores_cartera"],
}
DDB_CAT = ["tnm-sim-ddb-perfil-digital", "tnm-sim-ddb-preferencias", "tnm-sim-ddb-eventos-app",
           "tnm-sim-ddb-limites-vigentes"]
BUCKETS_CAT = ["tnm-sim-extractos-modelado-a", "tnm-sim-solicitudes-raw", "tnm-sim-solicitudes-curado",
               "tnm-sim-decisiones-credito", "tnm-sim-contratos", "tnm-sim-lago-analitico-a"]
BUCKETS_NOCAT_LISTADOS = ["tnm-sim-auditoria-trail", "tnm-sim-logs-aplicacion", "tnm-sim-lago-analitico-b",
                          "tnm-sim-artefactos-modelo"]
SIN_LISTA = [("tnm-sim-clientes-baja", "Bucket S3"), ("tnm-sim-extractos-modelado-b", "Bucket S3"),
             ("tnm-sim-ddb-sesiones-tmp", "Tabla DynamoDB"), ("tnm-sim-ddb-cache-scoring-tmp", "Tabla DynamoDB")]

SIN_RESPONSABLE = {"tnm-sim-aurora-riesgo", "riesgo.scoring_historico", "riesgo.ingresos_declarados",
                   "originacion.ofertas_historicas", "clientes.bajas_clientes", "tnm-sim-ddb-eventos-app",
                   "tnm-sim-ddb-preferencias", "tnm-sim-extractos-modelado-a", "tnm-sim-lago-analitico-a"}
SIN_CLASIFICACION = {"riesgo.scoring_historico", "riesgo.ingresos_declarados", "originacion.ofertas_historicas",
                     "tnm-sim-ddb-eventos-app", "tnm-sim-extractos-modelado-a", "tnm-sim-lago-analitico-a"}
CAMPOS_META = ["descripción", "dominio de negocio", "frecuencia de actualización",
               "fecha de última actualización", "ubicación técnica"]
META_FALTANTE = {
    "riesgo.scoring_historico": ["descripción", "frecuencia de actualización", "fecha de última actualización"],
    "riesgo.ingresos_declarados": ["descripción", "frecuencia de actualización", "fecha de última actualización"],
    "originacion.ofertas_historicas": ["descripción", "frecuencia de actualización"],
    "clientes.bajas_clientes": ["descripción", "dominio de negocio", "frecuencia de actualización"],
    "tnm-sim-ddb-eventos-app": ["descripción", "dominio de negocio", "frecuencia de actualización",
                                "fecha de última actualización"],
    "tnm-sim-ddb-preferencias": ["descripción", "frecuencia de actualización"],
    "tnm-sim-extractos-modelado-a": ["descripción", "dominio de negocio", "frecuencia de actualización",
                                     "fecha de última actualización"],
    "tnm-sim-lago-analitico-a": ["descripción", "frecuencia de actualización", "fecha de última actualización"],
}


def _membresia(i):
    """Listas de área en que aparece el activo número i (1..48)."""
    if i <= 17:
        return {"Riesgo", "Producto", "TI"}
    if i <= 23:
        return {"TI", "Riesgo"}
    if i <= 28:
        return {"TI", "Producto"}
    if i <= 36:
        return {"TI"}
    if i <= 44:
        return {"Riesgo"}
    return set()


def _owner(nombre, tipo):
    if nombre in SIN_RESPONSABLE:
        return ""
    if tipo == "Base Aurora/RDS" or tipo == "Tabla DynamoDB":
        return "Tecnología"
    if tipo == "Bucket S3":
        return "Datos e IA"
    if nombre.startswith("riesgo.") or nombre.startswith("originacion."):
        return "Riesgo de Crédito"
    return "Producto"


def _clasif(nombre, tipo):
    if nombre in SIN_CLASIFICACION:
        return ""
    if tipo == "Bucket S3":
        return "Interno"
    if tipo == "Tabla DynamoDB" or nombre.startswith("riesgo."):
        return "Confidencial"
    return "Restringido"


def construir_activos():
    lista = []
    for r in RDS:
        lista.append((r, "Base Aurora/RDS"))
    for db, tablas in GLUE.items():
        for t in tablas:
            lista.append((f"{db}.{t}", "Tabla Glue"))
    for d in DDB_CAT:
        lista.append((d, "Tabla DynamoDB"))
    for b in BUCKETS_CAT:
        lista.append((b, "Bucket S3"))
    for b in BUCKETS_NOCAT_LISTADOS:
        lista.append((b, "Bucket S3"))
    for nombre, tipo in SIN_LISTA:
        lista.append((nombre, tipo))
    activos = []
    for i, (nombre, tipo) in enumerate(lista, start=1):
        cat = i <= 40
        a = {
            "n": i, "nombre": nombre, "tipo": tipo, "catalogado": cat, "listas": _membresia(i),
            "responsable": _owner(nombre, tipo) if cat else None,
            "clasificacion": _clasif(nombre, tipo) if cat else None,
            "meta_faltante": META_FALTANTE.get(nombre, []) if cat else None,
        }
        activos.append(a)
    return activos


ACTIVOS = construir_activos()
CATALOGO = [a for a in ACTIVOS if a["catalogado"]]

# cifras derivadas (se usan en todos los textos)
N_ACT = len(ACTIVOS)                                            # 48
N_CAT = len(CATALOGO)                                           # 40
TIPOS = {}
for _a in ACTIVOS:
    TIPOS[_a["tipo"]] = TIPOS.get(_a["tipo"], 0) + 1
LISTA_N = {k: sum(1 for a in ACTIVOS if k in a["listas"]) for k in ("Riesgo", "Producto", "TI")}
EN_LAS_TRES = sum(1 for a in ACTIVOS if len(a["listas"]) == 3)
EN_ALGUNA = sum(1 for a in ACTIVOS if a["listas"])
EN_NINGUNA = N_ACT - EN_ALGUNA
NO_CAT = [a for a in ACTIVOS if not a["catalogado"]]
CON_RESP = sum(1 for a in CATALOGO if a["responsable"])
SIN_RESP = [a for a in CATALOGO if not a["responsable"]]
N_PARES = N_CAT * len(CAMPOS_META)
PARES_VACIOS = sum(len(a["meta_faltante"]) for a in CATALOGO)
PARES_OK = N_PARES - PARES_VACIOS
CON_CLASIF = sum(1 for a in CATALOGO if a["clasificacion"])
SIN_CLASIF = [a for a in CATALOGO if not a["clasificacion"]]

# ---------------------------------------------------------------- linaje (12 tramos esperados)
TRAMOS = [
    ("tnm-sim-aurora-originacion", "tnm-sim-solicitudes-raw", True),
    ("tnm-sim-aurora-crm", "tnm-sim-solicitudes-raw", True),
    ("tnm-sim-aurora-core", "tnm-sim-solicitudes-raw", False),
    ("tnm-sim-solicitudes-raw", "originacion.solicitudes_curado", True),
    ("originacion.solicitudes_curado", "originacion.features_solicitante", True),
    ("tnm-sim-aurora-riesgo", "riesgo.scoring_historico", False),
    ("riesgo.scoring_historico", "originacion.features_solicitante", True),
    ("riesgo.ingresos_declarados", "originacion.features_solicitante", True),
    ("tnm-sim-lago-analitico-a", "originacion.ofertas_historicas", False),
    ("originacion.features_solicitante", "tnm-sim-extractos-modelado-a", True),
    ("tnm-sim-extractos-modelado-a", "tnm-sim-artefactos-modelo", True),
    ("tnm-sim-artefactos-modelo", "modelo de preaprobación (destino)", True),
]
TR_TOT = len(TRAMOS)
TR_OK = sum(1 for t in TRAMOS if t[2])

# ---------------------------------------------------------------- buckets F-02
# (bucket, tipo de dato, política, regla configurada, coherente, objetos inventario, muestra, no conformes cifrado)
BUCKETS_F02 = [
    ("tnm-sim-extractos-modelado-a", "Extracción temporal para modelado", "30 días", "Expira a los 30 días", True, 38400, 343, 0),
    ("tnm-sim-extractos-modelado-b", "Extracción temporal para modelado", "30 días", "Sin regla de ciclo de vida", False, 52100, 343, 4),
    ("tnm-sim-solicitudes-raw", "Solicitudes de crédito (zona de trabajo)", "12 meses", "Expira a los 12 meses", True, 96300, 343, 3),
    ("tnm-sim-solicitudes-curado", "Solicitudes de crédito (zona de trabajo)", "12 meses", "Expira a los 12 meses", True, 71800, 343, 0),
    ("tnm-sim-clientes-baja", "Datos personales de clientes dados de baja", "24 meses", "Sin regla de ciclo de vida", False, 118200, 343, 5),
    ("tnm-sim-decisiones-credito", "Decisiones de crédito", "60 meses", "Expira a los 60 meses", True, 21500, 343, 0),
    ("tnm-sim-contratos", "Contratos", "60 meses", "Expira a los 60 meses", True, 14300, 342, 0),
]
B_TOT = len(BUCKETS_F02)
B_OK = sum(1 for b in BUCKETS_F02 if b[4])
INV_OBJ = sum(b[5] for b in BUCKETS_F02)
MUESTRA = sum(b[6] for b in BUCKETS_F02)
NC_CIFRADO = sum(b[7] for b in BUCKETS_F02)
CIF_OK = MUESTRA - NC_CIFRADO

BAJA_PREFIJOS = [  # prefijo, objetos, con última modificación anterior a 24 meses
    ("perfil/", 52000, 31900),
    ("contacto/", 38200, 22800),
    ("decisiones-historicas/", 28000, 16600),
]
BAJA_TOT = sum(p[1] for p in BAJA_PREFIJOS)
BAJA_VIEJOS = sum(p[2] for p in BAJA_PREFIJOS)
assert BAJA_TOT == 118200

# ---------------------------------------------------------------- jobs Glue (ventana de 90 días)
# job, terminales, exitosas, fallidas, canceladas, en curso
JOBS = [
    ("tnm-sim-prep-solicitudes", 180, 172, 8, 1, 1),
    ("tnm-sim-prep-clientes", 90, 85, 5, 1, 1),
    ("tnm-sim-prep-buro", 90, 80, 10, 1, 0),
    ("tnm-sim-features-solicitante", 90, 87, 3, 1, 0),
    ("tnm-sim-extracto-entrenamiento", 30, 27, 3, 1, 0),
    ("tnm-sim-carga-ofertas", 60, 57, 3, 0, 1),
]
RUN_TERM = sum(j[1] for j in JOBS)
RUN_OK = sum(j[2] for j in JOBS)
RUN_FAIL = sum(j[3] for j in JOBS)
RUN_STOP = sum(j[4] for j in JOBS)
RUN_ACT = sum(j[5] for j in JOBS)
assert RUN_TERM == RUN_OK + RUN_FAIL

# ---------------------------------------------------------------- hallazgos de permisos sin uso (19)
# (tipo, principal, días sin uso, toca F-02)
HALLAZGOS = [
    ("Rol sin uso", "tnm-sim-rol-etl-legado", 212, True),
    ("Rol sin uso", "tnm-sim-rol-analista-ext", 147, True),
    ("Rol sin uso", "tnm-sim-rol-pruebas-modelo", 120, False),
    ("Rol sin uso", "tnm-sim-rol-migracion-2024", 301, False),
    ("Rol sin uso", "tnm-sim-rol-reportes-riesgo", 98, False),
    ("Rol sin uso", "tnm-sim-rol-soporte-temporal", 133, False),
    ("Clave de acceso sin uso", "usr-sim-analista01", 176, True),
    ("Clave de acceso sin uso", "usr-sim-analista02", 94, False),
    ("Clave de acceso sin uso", "usr-sim-integracion", 260, False),
    ("Clave de acceso sin uso", "usr-sim-practicante03", 118, False),
    ("Permiso sin uso", "tnm-sim-rol-etl-prep: permisos de Redshift", 105, False),
    ("Permiso sin uso", "tnm-sim-rol-etl-prep: escritura en S3 de contratos", 112, True),
    ("Permiso sin uso", "tnm-sim-rol-features: permisos de DynamoDB", 97, False),
    ("Permiso sin uso", "tnm-sim-rol-features: lectura de clientes-baja", 91, True),
    ("Permiso sin uso", "tnm-sim-rol-scoring: permisos de RDS", 156, False),
    ("Permiso sin uso", "tnm-sim-rol-scoring: administración de claves KMS", 189, True),
    ("Permiso sin uso", "tnm-sim-rol-bi: lectura de extractos-modelado-b", 129, True),
    ("Permiso sin uso", "tnm-sim-rol-bi: permisos de Athena", 142, False),
    ("Permiso sin uso", "tnm-sim-rol-soporte: permisos de CloudWatch", 99, False),
]
H_TOT = len(HALLAZGOS)
H_TIPOS = {}
for _h in HALLAZGOS:
    H_TIPOS[_h[0]] = H_TIPOS.get(_h[0], 0) + 1
H_F02 = sum(1 for h in HALLAZGOS if h[3])

# ---------------------------------------------------------------- personas (ficticias)
ELENA = "Elena Marchetti"      # Gerenta General
JOAQUIN = "Joaquín Arévalo"    # Riesgo de Crédito
DANIELA = "Daniela Pinilla"    # Tecnología
RODRIGO = "Rodrigo Velasco"    # Datos e IA
NATALIA = "Natalia Ferrer"     # Seguridad
GONZALO = "Gonzalo Bravo"      # Finanzas
ISABEL = "Isabel Cornejo"      # Cumplimiento

# ---------------------------------------------------------------- aserciones de coherencia de diseño
assert (N_ACT, N_CAT, EN_LAS_TRES, EN_ALGUNA, EN_NINGUNA) == (48, 40, 17, 44, 4)
assert (LISTA_N["Riesgo"], LISTA_N["Producto"], LISTA_N["TI"]) == (31, 22, 36)
assert (CON_RESP, len(SIN_RESP), PARES_OK, PARES_VACIOS, CON_CLASIF, len(SIN_CLASIF)) == (31, 9, 176, 24, 34, 6)
assert (TR_OK, TR_TOT, B_OK, B_TOT, RUN_OK, RUN_TERM, CIF_OK, MUESTRA, INV_OBJ) == (9, 12, 5, 7, 508, 540, 2388, 2400, 412600)
assert (H_TOT, H_F02, RUN_STOP, RUN_ACT, BAJA_VIEJOS) == (19, 7, 5, 3, 71300)
assert TIPOS == {"Base Aurora/RDS": 4, "Tabla Glue": 26, "Tabla DynamoDB": 6, "Bucket S3": 12}
