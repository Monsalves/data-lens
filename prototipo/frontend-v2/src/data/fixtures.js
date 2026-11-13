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
  ...demoBuckets.map((name, index) => ({ id: `s3-bucket-${String(index + 1).padStart(3, '0')}`, name, title: ['Entrada de pedidos', 'Ventas procesadas'][index] || name, service: 'S3', kind: 'Bucket', region: 'us-east-1', owner: index === 1 ? 'Equipo BI' : 'Ingeniería de Datos', state: 'Ejemplo' })),
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
  { id: 'dashboard', name: 'bi.ventas_diarias', title: 'Panel de ventas', kind: 'Consumo', x: 750, y: 165 },
].map(({ id, name, title, kind, x, y }) => ({ id, label: title, name, kind, x, y }))

const recordedEdges = [
  ['crm', 'raw_clients', 'Recibir los clientes desde el CRM'],
  ['erp', 'raw_orders', 'Recibir los pedidos de la tienda'],
  ['raw_clients', 'dim_clients', 'Depurar y consolidar el maestro de clientes'],
  ['raw_orders', 'fact_sales', 'Consolidar los pedidos para análisis'],
  ['dim_clients', 'fact_sales', 'Relacionar cada venta con un cliente'],
  ['fact_sales', 'dashboard', 'Alimentar los indicadores de ventas'],
  ['dim_clients', 'dashboard', 'Habilitar filtros por segmento de cliente'],
  ['raw_orders', 'dim_clients', 'Calcular la última fecha de compra del cliente'],
]
// Conexiones registradas en el ejemplo de respuesta; no forman un universo esperado.
export const lineageEdges = recordedEdges.map(([from, to, purpose], index) => ({
  id: `LIN-${String(index + 1).padStart(2, '0')}`,
  from, to, purpose, observed: true,
}))

// El tono describe la condición observada, nunca la pertenencia al numerador.
const states = {
  'M-07': [{ code: 'informado', label: 'Campo informado', tone: 'success' }, { code: 'faltante', label: 'Campo faltante', tone: 'error' }],
  'M-11': [{ code: 'ausente', label: 'Valor ausente', tone: 'error' }, { code: 'presente', label: 'Valor presente', tone: 'success' }],
  'M-16': [{ code: 'exitosa', label: 'Ejecución exitosa', tone: 'success' }, { code: 'fallida', label: 'Ejecución fallida', tone: 'error' }],
  'M-18': [{ code: 'verificable', label: 'Resultado verificable', tone: 'info' }, { code: 'sin_resultado', label: 'Sin resultado verificable', tone: 'warning' }],
  'M-22': [{ code: 'sse_kms', label: 'SSE-KMS informado', tone: 'info' }, { code: 'sse_s3', label: 'SSE-S3 informado', tone: 'info' }],
  'M-25': [{ code: 'completo', label: 'Registro completo', tone: 'success' }, { code: 'incompleto', label: 'Registro incompleto', tone: 'error' }],
  'M-26': [{ code: 'informada', label: 'Clasificación informada', tone: 'info' }, { code: 'sin_clasificacion', label: 'Sin clasificación', tone: 'warning' }],
  'M-27': [{ code: 'intervino', label: 'Hubo intervención', tone: 'info' }, { code: 'sin_intervencion', label: 'Sin intervención', tone: 'neutral' }],
  'M-29': [{ code: 'activa', label: 'Regla activa', tone: 'info' }, { code: 'deshabilitada', label: 'Regla deshabilitada', tone: 'warning' }],
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
const classifiedAssets = dataZoneAssets.map(asset => ({ name: asset.title, detail: asset.name }))

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
    detail: evaluated ? `Regla DQDL en ${assetByTable.pedidos_venta.name}` : 'Regla configurada sin resultado en el lote',
    ...(evaluated && { checkOutcome: i < 6 ? 'Aprobado' : 'Fallido' }),
  })],
  'M-22': ['OBJETO', (i, usesKms) => ({
    name: `pedidos/lote-2026-11-08/parte-${sequence(i)}.parquet`,
    detail: `${demoBuckets[1]} · versión v1 · ${usesKms ? 'SSE-KMS' : 'SSE-S3'}`,
  })],
  'M-25': ['EVENTO', (i, complete) => ({
    name: `${auditEventTypes[i % auditEventTypes.length]} · evento ${sequence(i)}`,
    detail: `${auditLogName} · ${complete ? 'Campos exigidos presentes' : 'Falta eventTime'}`,
  })],
  'M-26': ['ACTIVO', (i, classified) => ({
    name: classifiedAssets[i].name,
    detail: `${classifiedAssets[i].detail} · ${classified ? 'Clasificación registrada en DataZone' : 'Sin clasificación en DataZone'}`,
  })],
  'M-27': ['CASO', (i, intervened) => {
    const isInput = i < sensitiveData.length
    const action = isInput ? 'bloquear' : 'enmascarar'
    return {
      name: `${isInput ? 'Entrada' : 'Salida'} con ${sensitiveData[i % sensitiveData.length]}`,
      detail: `Resultado del ejemplo: ${intervened ? action : 'permitir'}`,
    }
  }],
  'M-29': ['BUCKET', (i, active) => ({
    name: demoBuckets[i],
    detail: `Prefijo exportaciones/ · ${active ? i === 8 ? 'Expira a los 90 días' : 'Expira a los 30 días' : 'Regla deshabilitada'}`,
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
      inNumerator: true,
    }, { code: 'registrado', label: 'Registrado', tone: 'info' })
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
