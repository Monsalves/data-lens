# -*- coding: utf-8 -*-
"""Contenido del expediente F0-F3 del caso S02. Todo es ilustrativo y simulado."""
from caso_s02_datos import *  # noqa: F401,F403

AVISO = ("EJEMPLO ILUSTRATIVO · TODOS LOS DATOS, RESULTADOS Y EVIDENCIAS SON SIMULADOS · "
         "No hay pruebas ejecutadas en AWS · Banco y personas ficticios · Sin referencia normativa")
CUENTA = "123456789012 (ID de ejemplo, no real)"
EVDIR = "evidencias_simuladas"

# ===================================================================== F0
F0_PREGUNTAS = {
    5: (f"Evaluación S02 · {BANCO} (ficticio). Aplicación de ejemplo de la metodología 1.4 (no es una evaluación real). "
        "Ficha abierta el 26-oct-2026 (fecha simulada). Evaluador: equipo evaluador del ejemplo S02."),
    6: (f"Una cuenta AWS ({CUENTA}). Región principal us-east-2; el cliente declara que no hay otras regiones activas (por confirmar). "
        f"Referentes de negocio: {ELENA} (Gerencia General, patrocinadora), {JOAQUIN} (Riesgo de Crédito, usuario del modelo), "
        f"{GONZALO} (Finanzas). Referentes técnicos: {DANIELA} (Tecnología, administra la cuenta), {RODRIGO} (Datos e IA), "
        f"{NATALIA} (Seguridad), {ISABEL} (Cumplimiento)."),
    7: ("Preocupaciones tal como las declara el cliente. (1) Control de activos: «No sé con exactitud qué datos tengo, dónde están ni "
        "quién responde por ellos. Cada área me entrega una lista distinta.» (2) Costos: «La factura de AWS crece cada mes más que el "
        "negocio y nadie me dice qué parte es necesaria.» (3) Seguridad: «No sé si estamos listos para poner un modelo que aprueba "
        "créditos con datos de clientes, y no quiero enterarme de un problema después.» Usan el resultado: Gerencia General y Riesgo de Crédito. "
        f"CREENCIAS DECLARADAS, PENDIENTES DE CONFIRMAR (no son comprobaciones): «el gasto sube por el modelo» (declarada por {GONZALO}, Finanzas) "
        f"y «ciframos todo» (declarada por {DANIELA}, Tecnología). Se contrastan con EXA-06 y EXA-09."),
    8: ("Decisión: si el banco está listo para lanzar este trimestre (antes del 31-dic-2026) un modelo de preaprobación de créditos y qué "
        "debe corregir antes. Resultado esperado: una respuesta con condiciones, basada en evidencia, y acciones con prioridad. "
        "Éxito se reconoce si (a) la Gerencia General puede decidir con una lista clara de condiciones, (b) cada preocupación tiene una "
        "respuesta o un límite explícito y (c) cada acción tiene prioridad y criterio de cierre."),
    9: ("Siete fuentes (F-01 a F-07, tabla siguiente). Volúmenes declarados al abrir la ficha: catálogo con unos 40 activos; 5 buckets de datos "
        "de clientes y crédito (se confirma en EXA-01); 6 jobs de preparación de datos. Formatos: fichas de catálogo, archivos en S3, "
        "historial de ejecuciones, hojas de cálculo y facturas en PDF."),
    10: ("Las tres áreas mantienen sus listas de datos en hojas de cálculo propias y las entregan a pedido; juntarlas toma varios días y "
         "varios correos. La factura de AWS llega a Finanzas como documento mensual y hasta ahora no se ha pedido un reporte por producto. "
         "El contenido de los registros de auditoría solo lo lee Seguridad."),
    11: ("Hoy: las listas de las áreas se actualizan cuando alguien las pide (declarado); el catálogo se revisa cada mes (declarado); los jobs de "
         "preparación corren a diario o cada hora según el job; la factura es mensual. Se necesita: datos de solicitudes al día para el modelo "
         "(declarado por Riesgo) e inventario revisable cada trimestre (supuesto de este ejemplo)."),
    12: ("Datos e IA: catálogo, data lake y jobs. Tecnología: cuenta, bases y permisos. Seguridad: política de cifrado y registros de auditoría. "
         "Finanzas: factura. Riesgo de Crédito: datos de originación y scoring. Cumplimiento: plazos de conservación y privacidad. "
         "Autoriza el uso de datos para el modelo: Riesgo de Crédito con Cumplimiento (por confirmar). Responsable de cada activo: por confirmar (EXA-02)."),
    13: ("Las fuentes contienen datos personales y financieros de clientes (identificación, contacto, ingresos declarados, historial de crédito). "
         "Los requisitos regulatorios aplicables los debe indicar Cumplimiento; este ejemplo no cita normativa ni promete cumplimiento. "
         "Los plazos de conservación usados son supuestos del cliente ficticio."),
    14: ("Incluye: una cuenta AWS; datos de originación y de clientes; 9 métricas del piloto (M-01, M-07, M-09, M-16, M-21, M-22, M-25, M-26, M-29), "
         "un examen descriptivo de inventario y un examen documental de gasto. Excluye: calidad del contenido de los datos (M-11, M-18), "
         "flujos de acceso de DataZone (M-04), filtros de privacidad de IA generativa (M-27), desempeño y equidad del modelo, sistemas fuera de AWS y normativa. "
         f"Periodo: datos al {CORTE}; ventana de 90 días para jobs y permisos; revisión del 02 al 06-nov-2026 (simulada)."),
}

F0_FUENTES = [
    ("F-01", "Catálogo de datos corporativo (Amazon DataZone, dominio tnm-sim-datos)", "AWS · us-east-2 · cuenta de ejemplo",
     "Fichas de activos y grafo de linaje", "Revisión mensual manual (declarado)",
     f"Datos e IA ({RODRIGO}). Sensibilidad: las fichas describen datos sensibles; las fichas en sí son de nivel interno."),
    ("F-02", "Buckets S3 con datos de clientes, solicitudes y decisiones de crédito", "S3 · us-east-2 · 5 buckets declarados (se confirman en EXA-01)",
     "Archivos parquet y CSV (declarado)", "Carga diaria (declarado)",
     "Datos e IA y Tecnología (por confirmar por bucket). Sensibilidad alta: datos personales y financieros."),
    ("F-03", "Jobs ETL de AWS Glue que preparan los datos del modelo", "Glue · us-east-2 · 6 jobs", "Historial de ejecuciones de jobs",
     "Diaria u horaria según el job (declarado)", f"Datos e IA ({RODRIGO}). Sensibilidad media: procesan datos de F-02."),
    ("F-04", "Identidades y permisos IAM de la cuenta", f"IAM · cuenta {CUENTA.split(' ')[0]}", "Roles, usuarios, claves de acceso y políticas",
     "Cambios por solicitud a Tecnología", f"Tecnología ({DANIELA}). Sensibilidad alta: controlan el acceso a los datos."),
    ("F-05", "Registros de auditoría de la cuenta (CloudTrail)", "S3 · bucket tnm-sim-auditoria-trail", "Archivos JSON comprimidos",
     "Continua (declarado por Seguridad, sin verificar)", f"Seguridad ({NATALIA}). Sensibilidad alta."),
    ("F-06", "Inventario de activos de datos: listas de Riesgo, Producto y TI, y descubrimiento en la cuenta",
     "Hojas de cálculo de las áreas + servicios S3, Glue, Aurora/RDS y DynamoDB", "Hojas de cálculo (listas)", "Cuando alguien las pide",
     "Sin responsable único (se define con AC-01). Sensibilidad baja: nombres de activos."),
    ("F-07", "Facturación mensual de AWS", "Facturas en poder de Finanzas; consola de facturación sin acceso para el evaluador",
     "Facturas en PDF", "Mensual", f"Finanzas ({GONZALO}). Sensibilidad media: información financiera interna."),
]

# (ID, fuente, condición, propósito, preocupación)
F0_REQ = [
    ("REQ-01", "F-06", "¿Qué datos hay en la cuenta, de qué tipo son y dónde están? ¿Coinciden las listas de las áreas con lo que existe?",
     "Preocupación 1 · Control de activos. Tener una base común de lo que existe antes de decidir.", 1),
    ("REQ-02", "F-01", "Cada activo catalogado debe tener un responsable identificado.",
     "Preocupación 1 · Control de activos. Saber quién responde por cada dato.", 1),
    ("REQ-03", "F-01", "Cada activo catalogado debe tener completa su ficha descriptiva.",
     "Preocupación 1 · Control de activos. Que todas las áreas entiendan un dato de la misma manera.", 1),
    ("REQ-04", "F-01", "Debe poder reconstruirse de dónde vienen los datos que alimentan al modelo.",
     "Preocupación 1 · Control de activos. Poder explicar un dato ante un error o un reclamo.", 1),
    ("REQ-05", "F-01", "Cada activo catalogado debe tener registrado su nivel de sensibilidad.",
     "Preocupación 1 · Control de activos. Saber qué datos son sensibles antes de usarlos en un modelo.", 1),
    ("REQ-06", "F-07", "¿Cuánto del gasto mensual de AWS corresponde a cada servicio y producto, incluido el modelo, y cuánto es necesario?",
     "Preocupación 2 · Costos. Responder «qué parte es necesaria». Creencia declarada, por confirmar: «el gasto sube por el modelo».", 2),
    ("REQ-07", "F-02", "Los datos de clientes y de crédito deben conservarse solo el tiempo que indica la política de conservación.",
     "Preocupación 2 · Costos (indicio indirecto, no mide gasto). También importa a la Preocupación 3: menos datos guardados de más.", 2),
    ("REQ-08", "F-03", "Los procesos que preparan los datos del modelo deben terminar bien.",
     "Preocupación 2 · Costos (indicio indirecto, no mide gasto). Señal de trabajo que podría repetirse.", 2),
    ("REQ-09", "F-02", "Los datos de clientes guardados deben estar cifrados como exige la política.",
     "Preocupación 3 · Seguridad. Creencia declarada, por confirmar: «ciframos todo».", 3),
    ("REQ-10", "F-04", "Las identidades que acceden a los datos deben tener solo los permisos que usan.",
     "Preocupación 3 · Seguridad. Reducir quién puede llegar a datos de clientes cuando funcione el modelo.", 3),
    ("REQ-11", "F-05", "Los registros de auditoría deben permitir saber quién hizo qué con los datos.",
     "Preocupación 3 · Seguridad. «No quiero enterarme de un problema después»: poder reconstruirlo.", 3),
]

# ===================================================================== F1
def _sup(txt):
    return f"{txt} · {SUP}"

# (EXA, REQ, F, métrica, comprobación, criterio, cómo)
F1_EXA = [
    ("EXA-01", "REQ-01", "F-06", None,
     "Describir qué activos de datos existen en la cuenta, de qué tipo son, cuáles están en el catálogo y en cuáles listas de área aparece cada uno (inventario de activos).",
     "Sin umbral (examen descriptivo). Se informan conteos por tipo y por lista; no se emite estado de cumplimiento.",
     f"Descubrimiento de activos por servicio (S3, Glue, Aurora/RDS, DynamoDB) en la cuenta, contrastado con las tres listas de Riesgo, Producto y TI y con el catálogo (F-01). "
     f"Universo: toda la cuenta; datos al {CORTE}. No tiene métrica asociada; solo conteos."),
    ("EXA-02", "REQ-02", "F-01", "M-01",
     "Calcular qué proporción de los activos catalogados tiene un responsable informado en su ficha (M-01).",
     _sup("≥ 90 % de los activos catalogados con responsable informado (% cobertura)"),
     "M-01: activos con el campo de responsable informado ÷ activos del universo. Universo: los 40 activos del catálogo al 02-nov-2026; "
     "los no catalogados no tienen ficha y se informan en EXA-01. Revisión de las fichas del catálogo; no valida que la persona acepte la función."),
    ("EXA-03", "REQ-03", "F-01", "M-07",
     "Calcular qué proporción de los campos descriptivos obligatorios está completa en las fichas (M-07).",
     _sup("≥ 85 % de los pares activo-campo obligatorio con valor (% completitud)"),
     "M-07: pares activo-campo con valor no vacío ÷ pares aplicables. 5 campos obligatorios definidos por el cliente (descripción, dominio de negocio, "
     "frecuencia de actualización, fecha de última actualización, ubicación técnica) × 40 activos = 200 pares. Mide presencia, no exactitud. "
     "Responsable y clasificación se miden aparte (EXA-02 y EXA-05)."),
    ("EXA-04", "REQ-04", "F-01", "M-09",
     "Calcular qué proporción de los tramos esperados del flujo de datos del modelo tiene linaje registrado (M-09).",
     _sup("≥ 80 % de los tramos esperados con linaje registrado (% cobertura)"),
     "M-09: pares dirigidos (origen, destino) esperados y observados en el grafo ÷ tramos esperados de una especificación independiente. "
     "Especificación: diagrama de flujo de datos del modelo v0.3 de Arquitectura (12 tramos, a nivel de tabla o bucket). Se observa el grafo de linaje del catálogo (F-01). "
     "Mide tramos, no activos."),
    ("EXA-05", "REQ-05", "F-01", "M-26",
     "Calcular qué proporción de los activos catalogados tiene una clasificación vigente registrada (M-26).",
     _sup("≥ 95 % de los activos catalogados con clasificación registrada (% cobertura)"),
     "M-26: activos elegibles con clasificación registrada ÷ activos elegibles. Universo: los 40 activos del catálogo. Mide que exista la clasificación, "
     "no que sea correcta; su exactitud requiere contrastar con el contenido y queda fuera."),
    ("EXA-06", "REQ-06", "F-07", None,
     "Obtener el gasto mensual de AWS de los últimos 12 meses desglosado por servicio y por producto (incluido el modelo), para saber qué parte crece y qué parte es necesaria.",
     _sup("Sin umbral numérico. El examen se puede interpretar solo si existe un desglose mensual por servicio y por producto de 12 meses (nov-2025 a oct-2026). "
          "Si no existe o no se puede acceder a él, el estado es «Sin evidencia suficiente»"),
     "Ninguna de las 29 métricas de la matriz v1.3 mide gasto, por eso el examen es documental: solicitud del desglose a Finanzas y revisión de lo entregado. "
     "El rol de evaluación no tiene acceso a la consola de facturación. No se estiman ahorros."),
    ("EXA-07", "REQ-07", "F-02", "M-29",
     "Calcular qué proporción de los buckets con datos de clientes y crédito tiene una regla de conservación coherente con la política (M-29).",
     _sup("≥ 90 % de los buckets sujetos a la política con regla de ciclo de vida coherente (% conformidad)"),
     "M-29: buckets con reglas de retención coherentes con la política ÷ buckets sujetos a la política. Universo: los buckets de datos de clientes y crédito "
     "que identifica EXA-01 (7 al 02-nov-2026). Política (supuesto): extracciones temporales 30 días; solicitudes de crédito 12 meses; datos personales de clientes "
     "dados de baja 24 meses; decisiones de crédito y contratos 60 meses. Mide la configuración, no prueba que se haya eliminado. Como apoyo, "
     "listado de versiones del bucket de clientes dados de baja (observación complementaria, fuera del cálculo)."),
    ("EXA-08", "REQ-08", "F-03", "M-16",
     "Calcular qué proporción de las ejecuciones terminadas de los jobs de preparación termina con éxito (M-16).",
     _sup("≥ 90 % de las ejecuciones terminadas con éxito (% éxito)"),
     "M-16: ejecuciones terminales exitosas ÷ ejecuciones terminales de la cohorte. Cohorte: 6 jobs de preparación de datos del modelo; ventana de 90 días "
     "(04-ago a 02-nov-2026). Definiciones: cada reintento cuenta como una ejecución; las canceladas y las que siguen en curso quedan fuera del denominador."),
    ("EXA-09", "REQ-09", "F-02", "M-22",
     "Calcular qué proporción de los objetos revisados en los buckets de clientes y crédito tiene el cifrado exigido (M-22).",
     _sup("≥ 99 % de los objetos revisados con cifrado en servidor con la clave del banco, que exige la política (% conformidad); la cobertura del inventario se informa aparte"),
     "M-22: objetos con cifrado conforme ÷ objetos revisados con estado verificable. Muestra aleatoria de 2.400 objetos (unos 343 por bucket) de los 7 buckets de F-02, "
     "sobre un inventario de 412.600 objetos. Se revisa el cifrado de cada objeto; la configuración del bucket no basta. No incluye bases de datos ni otros almacenes."),
    ("EXA-10", "REQ-10", "F-04", "M-21",
     "Contar los hallazgos activos de permisos no utilizados en la cuenta durante la ventana observada (M-21).",
     _sup("Máximo 5 hallazgos activos de permisos sin uso en la ventana de 90 días (conteo)"),
     "M-21: hallazgos de permisos sin uso activos en la ventana observada, contados por cuenta y por tipo. Es un conteo, no un porcentaje; no se calcula tasa. "
     "Analizador de acceso no utilizado con ventana de 90 días sobre la cuenta. Un hallazgo es una lista para revisar; no confirma exceso."),
    ("EXA-11", "REQ-11", "F-05", "M-25",
     "Calcular qué proporción de los registros de auditoría examinados contiene todos los campos obligatorios (M-25).",
     _sup("≥ 98 % de los registros examinados con todos los campos obligatorios de su tipo de evento (% completitud). Campos acordados con Seguridad: quién, qué, sobre qué recurso, cuándo y con qué resultado"),
     "M-25: registros con todos los campos obligatorios de su tipo de evento ÷ registros examinados. Requiere leer el contenido de una muestra autorizada de archivos de log "
     "del bucket de auditoría; la autorización la da Seguridad. No basta comprobar que los archivos existen."),
]
EXA = {e[0]: e for e in F1_EXA}

# ===================================================================== F2
NO_CUMPLE, CUMPLE, NV, SEI, DESC = "No cumple", "Cumple", "No verificable", "Sin evidencia suficiente", "Descriptivo (sin estado de cumplimiento)"

sin_resp_modelo = [a["nombre"] for a in SIN_RESP if a["nombre"] in ("riesgo.scoring_historico", "riesgo.ingresos_declarados")]
assert len(sin_resp_modelo) == 2
asset_meta8 = [a["nombre"] for a in CATALOGO if a["meta_faltante"]]
assert len(asset_meta8) == 8 and all(not a["responsable"] for a in CATALOGO if a["meta_faltante"])
tr_falt = [t for t in TRAMOS if not t[2]]

F2_RES = [
    ("RES-01", "EXA-01", DESC,
     f"Se observaron {N_ACT} activos de datos: {TIPOS['Bucket S3']} buckets S3, {TIPOS['Tabla Glue']} tablas Glue, {TIPOS['Base Aurora/RDS']} bases Aurora/RDS y "
     f"{TIPOS['Tabla DynamoDB']} tablas DynamoDB. {N_CAT} están en el catálogo y {len(NO_CAT)} no (6 buckets y 2 tablas DynamoDB). "
     f"Listas de las áreas: Riesgo {LISTA_N['Riesgo']}, Producto {LISTA_N['Producto']}, TI {LISTA_N['TI']}; {EN_LAS_TRES} activos aparecen en las tres, "
     f"{EN_ALGUNA} en al menos una y {EN_NINGUNA} en ninguna (los buckets tnm-sim-clientes-baja y tnm-sim-extractos-modelado-b y dos tablas DynamoDB temporales)."),
    ("RES-02", "EXA-02", NO_CUMPLE,
     f"{CON_RESP} de {N_CAT} activos catalogados con responsable ({pct(CON_RESP, N_CAT)}). {len(SIN_RESP)} sin responsable; entre ellos riesgo.scoring_historico y "
     "riesgo.ingresos_declarados, que según EV-06 alimentan las variables del modelo."),
    ("RES-03", "EXA-03", CUMPLE,
     f"{PARES_OK} de {N_PARES} pares activo-campo informados ({pct(PARES_OK, N_PARES)}). {PARES_VACIOS} campos vacíos, repartidos en {len(asset_meta8)} activos."),
    ("RES-04", "EXA-04", NO_CUMPLE,
     f"{TR_OK} de {TR_TOT} tramos esperados con linaje registrado ({pct(TR_OK, TR_TOT)}). Faltan: tnm-sim-aurora-core → tnm-sim-solicitudes-raw; "
     "tnm-sim-aurora-riesgo → riesgo.scoring_historico; tnm-sim-lago-analitico-a → originacion.ofertas_historicas."),
    ("RES-05", "EXA-05", NO_CUMPLE,
     f"{CON_CLASIF} de {N_CAT} activos catalogados con clasificación registrada ({pct(CON_CLASIF, N_CAT)}). {len(SIN_CLASIF)} sin clasificación, "
     "entre ellos riesgo.scoring_historico y riesgo.ingresos_declarados."),
    ("RES-06", "EXA-06", SEI,
     "No se obtuvo un desglose del gasto por servicio ni por producto. Finanzas dispone de la factura mensual como documento sin etiquetas de producto, "
     "y el rol de evaluación no tuvo acceso a la consola de facturación. El gasto no se midió: no hay cifra que interpretar."),
    ("RES-07", "EXA-07", NO_CUMPLE,
     f"{B_OK} de {B_TOT} buckets con regla de conservación coherente ({pct(B_OK, B_TOT)}). Sin regla de ciclo de vida: tnm-sim-clientes-baja (política: 24 meses) y "
     f"tnm-sim-extractos-modelado-b (política: 30 días). Observación complementaria, fuera del cálculo: en tnm-sim-clientes-baja, {n(BAJA_VIEJOS)} de {n(BAJA_TOT)} objetos "
     f"({pct(BAJA_VIEJOS, BAJA_TOT)}) tienen última modificación anterior al 05-nov-2024."),
    ("RES-08", "EXA-08", CUMPLE,
     f"{RUN_OK} de {RUN_TERM} ejecuciones terminadas con éxito ({pct(RUN_OK, RUN_TERM)}); {RUN_FAIL} fallidas. Fuera del cálculo: {RUN_STOP} canceladas y {RUN_ACT} en curso."),
    ("RES-09", "EXA-09", CUMPLE,
     f"{n(CIF_OK)} de {n(MUESTRA)} objetos revisados con el cifrado exigido ({pct(CIF_OK, MUESTRA)}); {NC_CIFRADO} no conformes (cifrados con clave gestionada por el servicio, "
     f"no con la del banco) en 3 buckets. Cobertura del inventario: {n(MUESTRA)} de {n(INV_OBJ)} objetos ({pct(MUESTRA, INV_OBJ)})."),
    ("RES-10", "EXA-10", NO_CUMPLE,
     f"{H_TOT} hallazgos activos de permisos sin uso en 90 días: {H_TIPOS['Rol sin uso']} roles sin uso, {H_TIPOS['Clave de acceso sin uso']} claves de acceso sin uso y "
     f"{H_TIPOS['Permiso sin uso']} permisos sin uso. {H_F02} se relacionan con buckets de F-02 o con sus claves."),
    ("RES-11", "EXA-11", NV,
     "No se leyó ningún registro de auditoría, por lo que no se puede calcular la completitud. Motivo: Seguridad no autorizó la lectura del contenido de los logs dentro del plazo de la revisión."),
]
RES = {r[0]: r for r in F2_RES}

# (EV, RES, instrumento, salida (qué contiene), archivo, fecha)
F2_EV = [
    ("EV-01", "RES-01", "Descubrimiento de activos por servicio (colección de descubrimiento del proyecto) · resultado SIMULADO",
     "inventario_observado.csv", "48 filas: tipo de activo, si está en el catálogo y en cuáles listas de área aparece.", "02-nov-2026"),
    ("EV-02", "RES-01", "Contraste de las tres listas de las áreas con lo observado · cálculo SIMULADO",
     "contraste_listas_areas.md", "Conteos por lista y por combinación de listas; activos que ninguna área lista.", "02-nov-2026"),
    ("EV-03", "RES-02", "Revisión de fichas del catálogo, campo de responsable (plan de medición M-01) · SIMULADO",
     "catalogo_responsables.csv", "40 filas: activo y valor del campo de responsable; marca de los vacíos.", "03-nov-2026"),
    ("EV-04", "RES-03", "Revisión de fichas del catálogo, campos obligatorios (plan de medición M-07) · SIMULADO",
     "catalogo_metadatos.csv", "40 filas × 5 campos obligatorios: informado o vacío.", "03-nov-2026"),
    ("EV-05", "RES-04", "Contraste del grafo de linaje con los tramos esperados (plan de medición M-09) · SIMULADO",
     "linaje_tramos.csv", "12 tramos esperados, con marca de si el grafo los registra.", "04-nov-2026"),
    ("EV-06", "RES-04", "Revisión documental de la especificación independiente del flujo del modelo · documento SIMULADO",
     "especificacion_flujo_modelo.md", "Diagrama de flujo de datos del modelo v0.3 (de Arquitectura, 26-oct-2026): lista de los 12 tramos esperados.", "04-nov-2026"),
    ("EV-07", "RES-05", "Revisión de fichas del catálogo, campo de clasificación (plan de medición M-26) · SIMULADO",
     "catalogo_clasificacion.csv", "40 filas: activo y clasificación registrada; marca de los vacíos.", "03-nov-2026"),
    ("EV-08", "RES-06", "Solicitud documental a Finanzas y Tecnología · acta SIMULADA",
     "acta_solicitud_facturacion.md", "Solicitud del desglose, respuesta recibida y razón por la que no se pudo examinar el gasto. No contiene cifras de gasto.", "05-nov-2026"),
    ("EV-09", "RES-07", "Lectura de reglas de ciclo de vida por bucket (plan de medición M-29) · SIMULADO",
     "ciclo_de_vida_por_bucket.csv", "7 buckets: tipo de dato, política, regla configurada y si es coherente.", "04-nov-2026"),
    ("EV-10", "RES-07", "Listado de versiones del bucket de clientes dados de baja (apoyo de M-29) · SIMULADO",
     "versiones_clientes_baja.csv", "3 prefijos: total de objetos y objetos anteriores al 05-nov-2024. Fuera del cálculo de M-29.", "05-nov-2026"),
    ("EV-11", "RES-08", "Historial de ejecuciones de jobs, 90 días (plan de medición M-16) · SIMULADO",
     "glue_ejecuciones_90d.csv", "6 jobs: terminadas, exitosas, fallidas, canceladas y en curso.", "03-nov-2026"),
    ("EV-12", "RES-09", "Revisión de cifrado de una muestra de objetos (plan de medición M-22) · SIMULADO",
     "muestra_cifrado_objetos.md", "Por bucket: inventario, muestra, conformes y no conformes; lista de los 12 objetos no conformes.", "05-nov-2026"),
    ("EV-13", "RES-10", "Lista de hallazgos del analizador de acceso no utilizado (plan de medición M-21) · SIMULADO",
     "hallazgos_permisos_sin_uso.csv", "19 hallazgos: tipo, rol o usuario, días sin uso y si se relaciona con F-02.", "04-nov-2026"),
    ("EV-14", "RES-11", "Solicitud de acceso al contenido de logs · acta SIMULADA",
     "acta_acceso_auditoria.md", "Solicitud a Seguridad, respuesta y motivo de que el examen no sea verificable.", "06-nov-2026"),
]
EV = {e[0]: e for e in F2_EV}

# ===================================================================== F3
F3_DX = [
    ("DX-01", ["RES-01"],
     f"Hecho: el banco no tiene una sola lista de sus datos. Las tres áreas entregan listas distintas ({LISTA_N['Riesgo']}, {LISTA_N['Producto']} y {LISTA_N['TI']} activos; solo {EN_LAS_TRES} coinciden en las tres) "
     f"y {len(NO_CAT)} de los {N_ACT} activos existentes no están en el catálogo. {EN_NINGUNA} activos no figuran en ninguna lista. Esto confirma lo que el cliente describió sobre las listas.",
     "Impacto: sin inventario único no se puede asegurar quién responde ni qué datos están protegidos; los 4 activos sin lista incluyen dos buckets con datos de clientes (ver DX-06). "
     "Limitación: el descubrimiento cubrió S3, Glue, Aurora/RDS y DynamoDB; no se buscaron otros servicios ni archivos fuera de AWS."),
    ("DX-02", ["RES-02", "RES-05"],
     f"Hecho: {len(SIN_RESP)} de {N_CAT} activos catalogados no tienen responsable ({pct(CON_RESP, N_CAT)} con responsable) y {len(SIN_CLASIF)} de {N_CAT} no tienen clasificación "
     f"({pct(CON_CLASIF, N_CAT)} clasificados); ambas cifras quedan bajo el criterio. Dos de esos activos, riesgo.scoring_historico y riesgo.ingresos_declarados, alimentan las variables del modelo. "
     "No se pudo establecer: si los responsables registrados aceptaron la función ni si las clasificaciones registradas son correctas.",
     "Impacto: parte de los datos con que el modelo decidiría créditos no tiene dueño reconocido ni sensibilidad registrada. "
     "Limitación: las cifras cubren solo los 40 activos catalogados; los 8 no catalogados no tienen ficha y no entraron en el porcentaje."),
    ("DX-03", ["RES-03"],
     f"Hecho: {pct(PARES_OK, N_PARES)} de los campos descriptivos obligatorios están informados y se cumple el criterio (≥ 85 %). Las fichas del catálogo bastan para describir la mayoría de los activos.",
     "Limitación: mide que el campo esté lleno, no que lo escrito sea correcto. Los 24 campos vacíos están en 8 activos que también figuran entre los 9 sin responsable (DX-02). Resultado favorable: no se propone acción."),
    ("DX-04", ["RES-04"],
     f"Hecho: {TR_OK} de {TR_TOT} tramos esperados del flujo del modelo tienen linaje registrado ({pct(TR_OK, TR_TOT)}), bajo el criterio (≥ 80 %). Faltan los tramos desde la base central, desde la base de riesgo y desde el lago analítico. "
     "Hipótesis, no verificada: el linaje se registra solo para los flujos construidos en Glue y no para las cargas desde las bases.",
     "Impacto: ante un error o un reclamo no se podría reconstruir de dónde salió el dato en 3 de 12 tramos. "
     "Limitación: se midió a nivel de tabla o bucket, con una lista de tramos esperados de Arquitectura; no se verificó que los tramos registrados sean exactos."),
    ("DX-05", ["RES-06", "RES-08"],
     "El gasto no se midió. Ninguna métrica aplicada lo mide y no se obtuvo un desglose por servicio ni por producto (RES-06, sin evidencia suficiente). Por eso no se puede decir cuánto del gasto es necesario "
     "ni si el modelo explica el aumento: la creencia «el gasto sube por el modelo» queda sin confirmar y sin descartar. Hipótesis para investigar, sin comprobar: "
     "(H1) datos guardados más tiempo del definido (ver DX-06); (H2) trabajo repetido por ejecuciones fallidas, explicación menos probable porque RES-08 muestra 94,1 % de éxito, pero no descartada; "
     "(H3) consumo de las pruebas del modelo; (H4) otros servicios no examinados.",
     "Impacto: la Preocupación 2 queda sin respuesta hasta tener el desglose (AC-05). Limitación: no se estima ningún ahorro y no está demostrada la relación entre estos indicadores y la factura."),
    ("DX-06", ["RES-07", "RES-01"],
     f"Hallazgo no esperado. Hecho: dos buckets no tienen regla de eliminación ({B_OK} de {B_TOT} conformes): el de clientes dados de baja (política: 24 meses) y uno de extracciones para modelado (política: 30 días). "
     f"Ninguno está en el catálogo ni en las listas de las áreas, es decir, nadie los reclama. En el bucket de baja, {pct(BAJA_VIEJOS, BAJA_TOT)} de los objetos son anteriores al 05-nov-2024. "
     "Hipótesis, no verificada: al no tener dueño conocido nadie configuró la eliminación; parte de esos objetos podría ser de clientes dados de baja hace más de 24 meses (la fecha de baja no está en S3 y no se verificó).",
     "Riesgo (observado): datos personales de ex clientes siguen disponibles y podrían entrar al entrenamiento del modelo. Costo (hipótesis): almacenamiento innecesario; no se midió gasto y no se estima ahorro. "
     "Tensión: borrar para reducir riesgo y gasto choca con conservar registros que sirvan a una auditoría; el bucket contiene decisiones-historicas/ (28.000 objetos) que la política (supuesto) manda conservar 60 meses. "
     "Se resuelve por orden de prioridades: primero proteger (AC-07), luego separar (AC-06), al final eliminar (AC-08)."),
    ("DX-07", ["RES-09"],
     f"Hecho: {pct(CIF_OK, MUESTRA)} de los {n(MUESTRA)} objetos revisados tienen el cifrado exigido (criterio ≥ 99 %). La creencia «ciframos todo» se confirma para los objetos de S3 revisados en los 7 buckets de F-02.",
     f"Resultado favorable: no se propone acción. Limitación: la muestra cubre {pct(MUESTRA, INV_OBJ)} del inventario; no se revisaron bases Aurora/RDS, tablas DynamoDB ni respaldos, así que «ciframos todo» no queda confirmado en general. "
     "Los 12 objetos no conformes están listados en EV-12 para conocimiento del equipo de datos."),
    ("DX-08", ["RES-10"],
     f"Hecho: {H_TOT} hallazgos activos de permisos sin uso en 90 días (criterio: máximo 5); {H_F02} se relacionan con los buckets de datos de clientes o con sus claves. "
     "Hipótesis, no verificada: roles y claves creados para migraciones o pruebas que no se retiraron.",
     "Impacto: más personas o procesos de los necesarios podrían llegar a datos de clientes cuando funcione el modelo. Limitación: un hallazgo es una lista para revisar; un permiso poco usado puede ser necesario."),
    ("DX-09", ["RES-11"],
     "No se pudo establecer si los registros de auditoría están completos: no se leyó su contenido porque Seguridad no autorizó el acceso dentro del plazo. Es una limitación del examen; no es un resultado favorable ni desfavorable.",
     "Limitación: sin esta verificación no puede afirmarse que, tras el lanzamiento, el banco podrá reconstruir quién accedió a qué dato. Este examen tampoco comprobó la existencia de los archivos de log; que la auditoría esté activa es solo lo declarado por Seguridad."),
    ("DX-10", ["RES-02", "RES-04", "RES-05", "RES-07", "RES-09", "RES-10", "RES-11"],
     "Respuesta a la decisión, dentro de lo revisado: el banco no está listo para lanzar el modelo este trimestre sin corregir antes cinco puntos: responsables y clasificación de los datos que alimentan al modelo (DX-02), "
     "permisos sin uso (DX-08), verificación de los registros de auditoría (DX-09), datos de clientes dados de baja sin eliminación definida (DX-06) y linaje incompleto (DX-04). "
     "El cifrado de los objetos de S3 revisados es un punto fuerte (DX-07).",
     "Limitación: no se examinó la calidad del contenido de los datos, el comportamiento ni la equidad del modelo, ni el gasto. Esta conclusión no certifica cumplimiento normativo. "
     "Las condiciones y fechas de lanzamiento las decide la Gerencia General a partir de AC-11."),
]
DX = {d[0]: d for d in F3_DX}

# (AC, DX, acción, prioridad, cierre, estado)
F3_AC = [
    ("AC-01", "DX-01",
     f"Construir un inventario único de activos de datos que reemplace las tres listas: incluir los {N_ACT} activos observados (en particular los 4 que ninguna área lista) y catalogar los 8 que no están en el catálogo. Responsable propuesto: {RODRIGO} (Datos e IA) con Tecnología.",
     "Media · antes del cierre del trimestre",
     "Inventario único aprobado por Datos e IA. Al repetir EXA-01 no quedan activos sin lista ni sin catálogo, o cada excepción está justificada por escrito.", "Propuesta"),
    ("AC-02", "DX-02",
     "Asignar y registrar un responsable para los 9 activos catalogados que no lo tienen (empezando por riesgo.scoring_historico y riesgo.ingresos_declarados) y para los 8 no catalogados cuando se catalogen. "
     "Responsables propuestos: Riesgo de Crédito y Tecnología, que nombran a las personas.",
     "Alta · condición para lanzar",
     "Al repetir EXA-02 sobre el catálogo actualizado, ≥ 90 % de los activos tiene responsable y los 2 activos que alimentan al modelo lo tienen confirmado por escrito.", "Propuesta"),
    ("AC-03", "DX-02",
     "Registrar la clasificación de los 6 activos que no la tienen, con revisión de Seguridad y Cumplimiento, empezando por los dos que alimentan al modelo.",
     "Alta · condición para lanzar",
     "Al repetir EXA-05, ≥ 95 % de los activos catalogados está clasificado y los 6 nuevos registros fueron revisados por Seguridad.", "Propuesta"),
    ("AC-04", "DX-04",
     "Registrar el linaje de los 3 tramos que faltan (desde la base central, la base de riesgo y el lago analítico) y acordar quién lo mantiene cuando se agreguen flujos.",
     "Media · con fecha comprometida",
     "Al repetir EXA-04, ≥ 80 % de los tramos esperados tiene linaje registrado (al menos 10 de 12).", "Propuesta"),
    ("AC-05", "DX-05",
     f"Obtener, con autorización de Finanzas, el gasto mensual de 12 meses por servicio y por producto (con etiquetas) y repetir EXA-06 antes de atribuir el gasto al modelo o a otra causa. No se propone reducir gasto hasta tener ese desglose. Responsable propuesto: {GONZALO} (Finanzas) con Tecnología.",
     "Media · no bloquea el lanzamiento; responde la Preocupación 2",
     "Existe un desglose mensual de 12 meses por servicio y por producto, recuperable, y EXA-06 se repite con un estado distinto de «Sin evidencia suficiente».", "Propuesta"),
    ("AC-06", "DX-06",
     f"Separar, con Cumplimiento y Riesgo, los registros que deben conservarse para auditoría (por ejemplo decisiones-historicas/) de los datos personales a eliminar en tnm-sim-clientes-baja, y confirmar los plazos de conservación. Responsable propuesto: {ISABEL} (Cumplimiento).",
     "Alta · 2.º de DX-06 (después de AC-07)",
     "Lista aprobada por Cumplimiento que indica qué se conserva, hasta cuándo y qué se elimina.", "Propuesta"),
    ("AC-07", "DX-06",
     "Proteger primero lo que podría servir a una auditoría: no ejecutar ninguna eliminación masiva en tnm-sim-clientes-baja hasta cerrar AC-06 y asegurar que las decisiones históricas de crédito tengan una copia protegida contra borrado. Responsable propuesto: Tecnología con Seguridad.",
     "Alta · 1.º de DX-06 (primero)",
     "Instrucción escrita de no eliminar, vigente, y confirmación de Tecnología de que existe una copia protegida de las decisiones históricas.", "Propuesta"),
    ("AC-08", "DX-06",
     "Configurar reglas de eliminación para tnm-sim-clientes-baja (datos personales, 24 meses) y tnm-sim-extractos-modelado-b (30 días) según lo aprobado en AC-06, y nombrar responsable de ambos buckets. Solo después de cerrar AC-07 y AC-06.",
     "Media · 3.º de DX-06 (al final)",
     "Al repetir EXA-07, los 7 buckets tienen regla coherente (≥ 90 %) y Cumplimiento confirma que lo eliminado no incluye registros de auditoría.", "Propuesta"),
    ("AC-09", "DX-08",
     f"Revisar los {H_TOT} hallazgos con los dueños de cada rol o clave; retirar lo que no se necesite y documentar el motivo de lo que se mantenga. Responsable propuesto: {NATALIA} (Seguridad) con Tecnología.",
     "Alta · condición para lanzar",
     "Al repetir EXA-10, hay como máximo 5 hallazgos activos y cada uno tiene justificación escrita.", "Propuesta"),
    ("AC-10", "DX-09",
     "Acordar con Seguridad un acceso controlado y de solo lectura a una muestra de archivos de log y repetir EXA-11.",
     "Alta · condición para lanzar",
     "RES-11 se repite con un estado distinto de «No verificable» y se evalúa la regla de ≥ 98 %.", "Propuesta"),
    ("AC-11", "DX-10",
     "Presentar a la Gerencia General las condiciones de lanzamiento: lanzar el modelo solo cuando estén cerradas AC-02, AC-03, AC-07, AC-09 y AC-10, con fecha comprometida para AC-04, AC-06 y AC-08. "
     "Si no se alcanzan antes del cierre del trimestre, decidir si se pospone el lanzamiento.",
     "Alta · decisión de la Gerencia General",
     "Acta de la Gerencia General con las condiciones, los responsables y las fechas.", "Propuesta"),
]
AC = {a[0]: a for a in F3_AC}


def matriz():
    """Una fila por camino sustentado: EV × DX × AC. Fuente tomada del REQ."""
    req_f = {r[0]: r[1] for r in F0_REQ}
    filas = []
    for ev in F2_EV:
        res_id = ev[1]
        exa_id = RES[res_id][1]
        req_id = EXA[exa_id][1]
        f_id = req_f[req_id]
        dxs = [d for d in F3_DX if res_id in d[1]]
        for d in dxs:
            acs = [a for a in F3_AC if a[1] == d[0]]
            if not acs:
                filas.append((f_id, req_id, exa_id, res_id, ev[0], d[0], "—"))
            for a in acs:
                filas.append((f_id, req_id, exa_id, res_id, ev[0], d[0], a[0]))
    return filas
