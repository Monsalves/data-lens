// Escenario sintético de una tienda en línea y su plataforma de datos.
export const databases = [
  {
    id: 'crm', name: 'crm_clientes', domain: 'Clientes', title: 'CRM de clientes', owner: 'Equipo CRM',
    tables: [
      ['maestro_clientes', 'Maestro de clientes'],
      ['canales_contacto', 'Canales de contacto'],
      ['consentimientos_marketing', 'Consentimientos de marketing'],
      ['segmentos_fidelizacion', 'Segmentos de fidelización', false],
      ['direcciones_entrega', 'Direcciones de entrega'],
    ],
  },
  {
    id: 'ventas', name: 'comercio_ventas', domain: 'Ventas', title: 'Ventas en línea', owner: 'Equipo Comercio',
    tables: [
      ['pedidos_venta', 'Pedidos de venta'],
      ['lineas_pedido', 'Líneas de pedido'],
      ['catalogo_productos', 'Catálogo de productos'],
      ['pagos_checkout', 'Pagos en caja', false],
      ['devoluciones_pedido', 'Devoluciones de pedidos'],
    ],
  },
  {
    id: 'finanzas', name: 'finanzas_cobros', domain: 'Finanzas', title: 'Facturación y cobros', owner: 'Equipo Finanzas',
    tables: [
      ['facturas_emitidas', 'Facturas emitidas'],
      ['cobros_confirmados', 'Cobros confirmados'],
      ['presupuesto_mensual', 'Presupuesto mensual'],
      ['centros_de_costo', 'Centros de costo'],
      ['conciliacion_bancaria', 'Conciliación bancaria', false],
    ],
  },
  {
    id: 'analytics', name: 'analitica_comercial', domain: 'Analítica', title: 'Analítica comercial', owner: 'Equipo BI',
    tables: [
      ['dimension_clientes', 'Dimensión clientes'],
      ['hechos_ventas', 'Ventas consolidadas'],
      ['clientes_recibidos', 'Clientes recibidos'],
      ['pedidos_recibidos', 'Pedidos recibidos'],
      ['auditoria_cargas', 'Auditoría de cargas', false],
    ],
  },
]

export const dataZoneAssets = databases.flatMap(db => db.tables.map(([table, title, hasOwner = true], index) => ({
  id: `dz-${db.id}-${String(index + 1).padStart(2, '0')}`,
  name: `${db.name}.${table}`,
  title,
  domain: db.domain,
  databaseId: db.id,
  table,
  service: 'DataZone',
  kind: 'Activo de datos',
  region: 'us-east-1',
  owner: hasOwner ? db.owner : '',
  state: 'Ejemplo',
})))

const demoBuckets = [
  'tienda-demo-ingesta-pedidos', 'tienda-demo-ventas-curadas', 'tienda-demo-exportaciones-crm',
  'tienda-demo-conciliaciones', 'tienda-demo-devoluciones', 'tienda-demo-catalogo-productos',
  'tienda-demo-reportes-finanzas', 'tienda-demo-auditoria', 'tienda-demo-temporales-crm', 'tienda-demo-intercambio-cobros',
]
const auditLogName = 'cloudtrail-tienda-2026-11-08.json.gz'
export const glueDemoJob = {
  id: 'glue-job-001', name: 'etl_clientes_a_analitica', title: 'Carga de clientes a Analítica',
  service: 'Glue', kind: 'Job', region: 'us-east-1', owner: 'Ingeniería de Datos', state: 'Ejemplo',
}
export const otherAssets = [
  ...databases.map(db => ({ id: `glue-db-${db.id}`, name: db.name, title: db.title, service: 'Glue', kind: 'Base de datos', region: 'us-east-1', owner: db.owner, state: 'Ejemplo' })),
  glueDemoJob,
  { id: 's3-bucket-001', name: demoBuckets[0], title: 'Entrada de pedidos', service: 'S3', kind: 'Bucket', region: 'us-east-1', owner: 'Ingeniería de Datos', state: 'Ejemplo' },
  { id: 's3-bucket-002', name: demoBuckets[1], title: 'Ventas procesadas', service: 'S3', kind: 'Bucket', region: 'us-east-1', owner: 'Equipo BI', state: 'Ejemplo' },
  { id: 'iam-analyzer-001', name: 'tienda-accesos-sin-uso', title: 'Accesos sin uso de la tienda', service: 'IAM Access Analyzer', kind: 'Analizador', region: 'us-east-1', owner: 'Seguridad', state: 'Ejemplo' },
  { id: 'bedrock-guardrail-001', name: 'proteccion-datos-asistente-pedidos', title: 'Privacidad del asistente de pedidos', service: 'Bedrock', kind: 'Guardrail', region: 'us-east-1', owner: 'Seguridad', state: 'Ejemplo' },
  { id: 'cloudtrail-log-001', name: auditLogName, title: 'Registro de auditoría de la tienda', service: 'CloudTrail', kind: 'Archivo de log', region: 'us-east-1', owner: 'Seguridad', state: 'Ejemplo' },
]
export const assets = [...dataZoneAssets, ...otherAssets]

const assetByTable = Object.fromEntries(dataZoneAssets.map(asset => [asset.table, asset]))

export const lineageNodes = [
  { ...assetByTable.maestro_clientes, id: 'crm', kind: 'Origen', x: 12, y: 66 },
  { ...assetByTable.pedidos_venta, id: 'erp', kind: 'Origen', x: 12, y: 275 },
  { ...assetByTable.clientes_recibidos, id: 'raw_clients', kind: 'Ingesta', x: 260, y: 52 },
  { ...assetByTable.pedidos_recibidos, id: 'raw_orders', kind: 'Ingesta', x: 260, y: 290 },
  { ...assetByTable.dimension_clientes, id: 'dim_clients', kind: 'Transformación', x: 505, y: 50 },
  { ...assetByTable.hechos_ventas, id: 'fact_sales', kind: 'Transformación', x: 505, y: 290 },
  { ...assetByTable.devoluciones_pedido, id: 'returns', kind: 'Origen', x: 12, y: 365 },
  { ...assetByTable.catalogo_productos, id: 'products', kind: 'Origen', x: 260, y: 365 },
  { id: 'dashboard', name: 'bi.ventas_diarias', title: 'Panel de ventas', kind: 'Consumo', x: 750, y: 165 },
].map(({ id, name, title, kind, x, y }) => ({ id, label: title, name, kind, x, y }))

export const lineageReferenceId = 'REF-LIN-01'
export const lineageReference = `Diseño ficticio del flujo de ventas · ${lineageReferenceId}`
const referenceEdges = [
  ['crm', 'raw_clients', 'Recibir los clientes desde el CRM'],
  ['erp', 'raw_orders', 'Recibir los pedidos de la tienda'],
  ['raw_clients', 'dim_clients', 'Depurar y consolidar el maestro de clientes'],
  ['raw_orders', 'fact_sales', 'Consolidar los pedidos para análisis'],
  ['dim_clients', 'fact_sales', 'Relacionar cada venta con un cliente'],
  ['fact_sales', 'dashboard', 'Alimentar los indicadores de ventas'],
  ['dim_clients', 'dashboard', 'Habilitar filtros por segmento de cliente'],
  ['raw_orders', 'dim_clients', 'Calcular la última fecha de compra del cliente'],
  ['returns', 'fact_sales', 'Descontar devoluciones para obtener las ventas netas'],
  ['products', 'fact_sales', 'Incorporar la categoría del producto a cada venta'],
]
// Pares registrados en el ejemplo de respuesta de DataZone.
const observedPairs = new Set([
  'crm→raw_clients', 'erp→raw_orders', 'raw_clients→dim_clients', 'raw_orders→fact_sales',
  'dim_clients→fact_sales', 'fact_sales→dashboard', 'dim_clients→dashboard', 'raw_orders→dim_clients',
])
export const lineageEdges = referenceEdges.map(([from, to, purpose], index) => ({
  id: `LIN-${String(index + 1).padStart(2, '0')}`,
  from, to, purpose, observed: observedPairs.has(`${from}→${to}`),
}))

// El tono describe la condición observada, nunca la pertenencia al numerador.
const states = {
  'M-07': [{ code: 'informado', label: 'Campo informado', tone: 'success' }, { code: 'faltante', label: 'Campo faltante', tone: 'error' }],
  'M-11': [{ code: 'ausente', label: 'Valor ausente', tone: 'error' }, { code: 'presente', label: 'Valor presente', tone: 'success' }],
  'M-16': [{ code: 'exitosa', label: 'Ejecución exitosa', tone: 'success' }, { code: 'fallida', label: 'Ejecución fallida', tone: 'error' }],
  'M-18': [{ code: 'verificable', label: 'Resultado verificable', tone: 'info' }, { code: 'sin_resultado', label: 'Sin resultado verificable', tone: 'warning' }],
  'M-22': [{ code: 'conforme', label: 'Cifrado conforme', tone: 'success' }, { code: 'no_conforme', label: 'Cifrado no conforme', tone: 'error' }],
  'M-25': [{ code: 'completo', label: 'Registro completo', tone: 'success' }, { code: 'incompleto', label: 'Registro incompleto', tone: 'error' }],
  'M-26': [{ code: 'vigente', label: 'Clasificación vigente', tone: 'success' }, { code: 'sin_vigencia', label: 'Sin clasificación vigente', tone: 'error' }],
  'M-27': [{ code: 'esperada', label: 'Acción esperada', tone: 'success' }, { code: 'distinta', label: 'Acción distinta', tone: 'error' }],
  'M-29': [{ code: 'coherente', label: 'Regla coherente', tone: 'success' }, { code: 'no_coherente', label: 'Regla no coherente', tone: 'error' }],
}
const withStatus = (row, status) => ({ ...row, statusCode: status.code, statusLabel: status.label, tone: status.tone })

const sequence = (index, width = 3) => String(index + 1).padStart(width, '0')

const accessRequests = [
  ['Equipo BI', 'hechos_ventas', 'Tablero de ventas'],
  ['Equipo Comercio', 'catalogo_productos', 'Seguimiento de surtido'],
  ['Equipo Finanzas', 'cobros_confirmados', 'Cierre de caja'],
  ['Equipo CRM', 'consentimientos_marketing', 'Control de campañas'],
  ['Equipo Finanzas', 'facturas_emitidas', 'Conciliación de facturas'],
  ['Equipo Logística', 'direcciones_entrega', 'Preparar despachos'],
  ['Agencia de marketing', 'maestro_clientes', 'Audiencia para campaña'],
  ['Equipo Soporte', 'centros_de_costo', 'Consulta de gastos'],
  ['Equipo Comercio', 'devoluciones_pedido', 'Análisis de devoluciones'],
  ['Equipo BI', 'pagos_checkout', 'Seguimiento del pago'],
]

const catalogFields = [
  ['descripcion', asset => ['canales_contacto', 'presupuesto_mensual'].includes(asset.table) ? '' : asset.title],
  ['responsable', asset => asset.owner],
  ['dominio', asset => asset.domain],
  ['frecuencia_actualizacion', asset => ['lineas_pedido', 'catalogo_productos', 'centros_de_costo', 'auditoria_cargas'].includes(asset.table) ? '' : 'Diaria'],
  ['contacto_soporte', asset => `Mesa de datos · ${asset.domain}`],
]

const outputChecks = [
  'Cliente identificado en cada pedido', 'Número de pedido único', 'Fecha del pedido válida',
  'Estado de pedido permitido', 'Moneda registrada', 'Total del pedido no negativo',
  'Medio de pago reconocido', 'Dirección en pedidos con despacho',
  'Producto registrado en cada línea', 'Monto de devolución dentro del total pagado',
]

const accessFindings = [
  ['etl-clientes', 's3:DeleteObject'], ['bi-ventas', 'glue:UpdateTable'],
  ['cierre-finanzas', 's3:PutObject'], ['soporte-pedidos', 'dynamodb:UpdateItem'],
  ['carga-productos', 'glue:DeleteTable'], ['logistica-despachos', 's3:ListBucket'],
  ['auditoria-tienda', 'cloudtrail:StopLogging'], ['integracion-cobros', 's3:GetObject'],
]

const auditEventTypes = ['GetObject', 'PutObject', 'StartJobRun', 'AssumeRole', 'UpdateTable']
const sensitiveData = [
  'correo electrónico', 'teléfono de contacto', 'dirección de entrega', 'número de identificación',
  'tarjeta de pago', 'cuenta bancaria', 'clave de acceso', 'contraseña', 'código de verificación', 'token de sesión',
]
const classifiedAssets = [
  ...dataZoneAssets.map(asset => ({ name: asset.title, detail: asset.name })),
  ...['pedidos', 'contactos', 'cobros'].flatMap(type => Array.from({ length: 10 }, (_, day) => ({
    name: `Exportación de ${type} · 2026-11-${sequence(day, 2)}`,
    detail: `intercambios.${type}_202611${sequence(day, 2)}`,
  }))),
]

const sampleRows = {
  'M-11': ['VALOR', (i, missing) => ({
    name: `cliente_id · PED-${sequence(i, 5)}`,
    detail: `${assetByTable.pedidos_venta.name} · ${missing ? 'NULL' : `CLI-${sequence(i, 5)}`}`,
  })],
  'M-16': ['RUN', (i, success) => ({
    name: `Carga de clientes · 2026-11-${sequence(Math.floor(i / 2), 2)} ${i % 2 ? '18:00' : '06:00'}`,
    detail: `${glueDemoJob.name} · ${success ? 'Carga terminada' : 'Falló la validación de entrada'}`,
  })],
  'M-18': ['CONTROL', (i, evaluated) => ({
    name: outputChecks[i],
    detail: evaluated ? `Regla DQDL en ${assetByTable.pedidos_venta.name}` : 'Control planificado sin evaluación en el lote',
    ...(evaluated && { checkOutcome: i < 6 ? 'Aprobado' : 'Fallido' }),
  })],
  'M-22': ['OBJETO', (i, compliant) => ({
    name: `pedidos/lote-2026-11-08/parte-${sequence(i)}.parquet`,
    detail: `${demoBuckets[1]} · versión v1 · ${compliant ? 'SSE-KMS' : 'SSE-S3 (se exige SSE-KMS)'}`,
  })],
  'M-25': ['EVENTO', (i, complete) => ({
    name: `${auditEventTypes[i % auditEventTypes.length]} · evento ${sequence(i)}`,
    detail: `${auditLogName} · ${complete ? 'Campos exigidos presentes' : 'Falta eventTime'}`,
  })],
  'M-26': ['ACTIVO', (i, classified) => ({
    name: classifiedAssets[i].name,
    detail: `${classifiedAssets[i].detail} · ${classified ? 'Clasificación registrada en DataZone' : 'Clasificación sin registrar en DataZone'}`,
  })],
  'M-27': ['CASO', (i, expected) => {
    const isInput = i < sensitiveData.length
    const action = isInput ? 'bloquear' : 'enmascarar'
    return {
      name: `${isInput ? 'Entrada' : 'Salida'} con ${sensitiveData[i % sensitiveData.length]}`,
      detail: `Esperado: ${action} · Resultado: ${expected ? action : 'permitir'}`,
    }
  }],
  'M-29': ['BUCKET', (i, compliant) => ({
    name: demoBuckets[i],
    detail: `Prefijo exportaciones/ · ${compliant ? 'Expira a los 30 días' : i === 8 ? 'Regla deshabilitada' : 'Expira a los 90 días (se exigen 30)'}`,
  })],
}

export function populationFor(metric) {
  if (metric.id === 'M-01') return dataZoneAssets.map(a => withStatus({
    id: a.id, name: a.title, detail: `${a.name} · ${a.owner || 'Responsable sin asignar'}`, inNumerator: !!a.owner,
  }, a.owner ? { code: 'con_responsable', label: 'Con responsable', tone: 'success' } : { code: 'sin_responsable', label: 'Sin responsable', tone: 'error' }))

  if (metric.id === 'M-04') return accessRequests.map(([team, table, purpose], i) => {
    const asset = assetByTable[table]
    const request = i < 6 ? { code: 'aprobada', label: 'Aprobada', tone: 'info' } : i < 8 ? { code: 'rechazada', label: 'Rechazada', tone: 'neutral' } : { code: 'pendiente', label: 'Pendiente', tone: 'warning' }
    const grant = i < 5 ? { code: 'activo', label: 'Grant activo', tone: 'success' } : i === 5 ? { code: 'fallido', label: 'Grant fallido', tone: 'error' } : { code: 'sin_grant', label: 'Sin grant', tone: 'neutral' }
    const row = { id: `SOL-${sequence(i)}`, name: `${team} → ${asset.title}`, detail: `${purpose} · ${asset.name}`, inNumerator: true }
    return { ...withStatus(row, request), grantCode: grant.code, grantLabel: grant.label, grantTone: grant.tone }
  })

  if (metric.id === 'M-07') return dataZoneAssets.flatMap((asset, assetIndex) =>
    catalogFields.map(([field, valueFor], fieldIndex) => {
      const value = valueFor(asset)
      const row = {
        id: `CAMPO-${sequence(assetIndex * catalogFields.length + fieldIndex)}`,
        name: `${field} · ${asset.title}`,
        detail: `${asset.name} · ${value || 'Sin valor'}`,
        inNumerator: Boolean(value),
      }
      return withStatus(row, states[metric.id][value ? 0 : 1])
    }),
  )

  if (metric.id === 'M-09') return lineageEdges.map(edge => {
    const from = lineageNodes.find(node => node.id === edge.from)
    const to = lineageNodes.find(node => node.id === edge.to)
    return withStatus({
      id: edge.id, name: `${from.label} → ${to.label}`, detail: `${edge.purpose} · ${from.name} → ${to.name}`,
      referenceId: lineageReferenceId, inNumerator: edge.observed,
    }, edge.observed ? { code: 'observado', label: 'Registrado', tone: 'info' } : { code: 'no_observado', label: 'Sin evidencia en la consulta', tone: 'warning' })
  })

  if (metric.id === 'M-21') return accessFindings.map(([role, permission], i) => withStatus({
    id: `FINDING-${sequence(i)}`, name: `Rol ${role}`, detail: `${permission} · Sin uso en la ventana de 90 días`, inNumerator: true,
  }, { code: 'activo', label: 'Hallazgo activo', tone: 'error' }))

  const [prefix, example] = sampleRows[metric.id]
  const [inStatus, outStatus] = states[metric.id]
  return Array.from({ length: metric.den }, (_, i) => {
    const inNumerator = i < metric.num
    return withStatus({ id: `${prefix}-${sequence(i)}`, ...example(i, inNumerator), inNumerator }, inNumerator ? inStatus : outStatus)
  })
}

export function statusOptionsFor(rows, field = 'statusCode', labelField = 'statusLabel', toneField = 'tone') {
  const options = new Map()
  for (const row of rows) {
    const code = row[field]
    if (!code) continue
    const option = options.get(code) || { code, label: row[labelField], tone: row[toneField], count: 0 }
    option.count += 1
    options.set(code, option)
  }
  return [...options.values()]
}
