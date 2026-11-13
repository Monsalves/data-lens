<script setup>
import { computed, nextTick, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useDisplay } from 'vuetify'
import metrics from './data/metrics.json'
import { assets, databases, dataZoneAssets, glueDemoJob, populationFor } from './data/fixtures.js'
import DataInventory from './components/DataInventory.vue'
import ProcessList from './components/ProcessList.vue'
import MetricDetail from './components/MetricDetail.vue'
import ControlSummary from './components/ControlSummary.vue'

const sections = [
  { id: 'inicio', label: 'Resumen', icon: 'mdi-view-dashboard-outline' },
  { id: 'inventario', label: 'Datos', icon: 'mdi-database-outline' },
  { id: 'procesos', label: 'Procesos', icon: 'mdi-cog-outline' },
  { id: 'controles', label: 'Controles transversales', icon: 'mdi-shield-check-outline' },
  { id: 'mediciones', label: 'Mediciones', icon: 'mdi-chart-box-outline' },
  { id: 'ejecuciones', label: 'Historial', icon: 'mdi-history' },
  { id: 'cuentas', label: 'Conexiones', icon: 'mdi-cloud-outline' },
]
const scopeFilters = [
  { id: 'todas', label: 'Todas' },
  { id: 'tablas', label: 'Tablas' },
  { id: 'procesos', label: 'Procesos' },
  { id: 'almacenamiento', label: 'Almacenamiento S3' },
  { id: 'controles', label: 'Controles transversales' },
]
const resourceName = id => assets.find(asset => asset.id === id)?.name
const orderTable = dataZoneAssets.find(asset => asset.table === 'pedidos_venta')?.name
const metricContexts = {
  'M-01': { scope: 'tablas', resource: 'Tablas inventariadas en DataZone' },
  'M-04': { scope: 'tablas', resource: 'Solicitudes vinculadas a tablas en DataZone' },
  'M-07': { scope: 'tablas', resource: 'Campos requeridos de las tablas en DataZone' },
  'M-09': { scope: 'tablas', resource: 'Conexiones registradas en el grafo de DataZone' },
  'M-11': { scope: 'tablas', resource: `Tabla ${orderTable}` },
  'M-16': { scope: 'procesos', resource: `Job Glue · ${glueDemoJob.name}` },
  'M-18': { scope: 'tablas', resource: 'Conjunto de reglas de calidad de Glue' },
  'M-21': { scope: 'controles', resource: `IAM Access Analyzer · ${resourceName('iam-analyzer-001')}` },
  'M-22': { scope: 'almacenamiento', resource: `Objetos del bucket S3 · ${resourceName('s3-bucket-002')}` },
  'M-25': { scope: 'controles', resource: `Archivo de CloudTrail · ${resourceName('cloudtrail-log-001')}` },
  'M-26': { scope: 'tablas', resource: 'Tablas inventariadas en DataZone' },
  'M-27': { scope: 'controles', resource: `Pruebas del guardrail de Bedrock · ${resourceName('bedrock-guardrail-001')}` },
  'M-29': { scope: 'almacenamiento', resource: 'Buckets S3 del escenario' },
}
const scopeCounts = Object.fromEntries(scopeFilters.map(({ id }) => [
  id, id === 'todas' ? metrics.length : metrics.filter(metric => metricContexts[metric.id]?.scope === id).length,
]))
const buckets = assets.filter(asset => asset.service === 'S3' && asset.kind === 'Bucket')
const controlMetrics = metrics.filter(metric => metricContexts[metric.id]?.scope === 'controles')
const overviewMetrics = ['M-01', 'M-11', 'M-16', 'M-29', 'M-21', 'M-25'].map(id => metrics.find(metric => metric.id === id))
const pillars = [...new Set(metrics.map(m => m.pillar))]
const defaultAccounts = [{ id: '111122223333', name: 'Cuenta de demostración', region: 'us-east-1', roleArn: '', mode: 'simulada', status: 'Demo local' }]
const fixtureVersion = 4
const appBase = import.meta.env.BASE_URL
function metricFromPath() {
  const path = window.location.pathname
  return path.startsWith(appBase) ? path.slice(appBase.length).match(/^metricas\/(M-\d{2})\/?$/)?.[1] || '' : ''
}
function readStorage(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback } catch { return fallback } }
function recordsFor(metric) {
  return populationFor(metric).map(row => {
    return { ...row, evidenceRef: `${metric.id}-${row.id}-SIM` }
  })
}
function refreshDemoRun(run) {
  if (run.fixtureVersion === fixtureVersion || !run.id?.startsWith('SIM-')) return run
  const results = run.results.map(result => {
    const metric = metrics.find(item => item.id === result.metricId)
    return metric ? { ...result, value: metric.den > 0 ? Number((metric.num / metric.den * 100).toFixed(1)) : metric.num, num: metric.num, den: metric.den, unit: metric.unit, coverage: 'Escenario de prueba', records: recordsFor(metric) } : result
  })
  return { ...run, fixtureVersion, results }
}
const accounts = ref(readStorage('dl.v2.accounts', defaultAccounts))
const active = ref('inicio')
const drawer = ref(null)
const { mdAndUp } = useDisplay()
const sidebarMinimized = ref(false)
const compactSidebar = computed(() => mdAndUp.value && sidebarMinimized.value)
const search = ref('')
const pillarFilter = ref('Todos')
const measurementScope = ref('todas')
const inventoryFocused = ref(false)
const inventoryEntryType = ref('Todos')
const measurementViews = [
  { id: 'lista', label: 'Lista', icon: 'mdi-format-list-bulleted' },
  { id: 'tarjetas', label: 'Tarjetas', icon: 'mdi-view-grid-outline' },
]
const measurementView = ref(readStorage('dl.v2.measurementView', 'lista') === 'tarjetas' ? 'tarjetas' : 'lista')
const metricId = ref(metricFromPath())
const metricOrigin = ref(null)
const returnSection = ref('mediciones')
let returnScroll = 0
let returnFocus = null
const selectedMetric = computed(() => metrics.find(m => m.id === metricId.value) || null)
const accountDialog = ref(false)
const accountForm = ref({ name: '', id: '', roleArn: '', externalId: '', region: 'us-east-1' })
const notice = ref('')
const currentRun = ref(null)
const runs = ref(readStorage('dl.v2.runs', []).map(refreshDemoRun))
let timer = null

watch(accounts, value => localStorage.setItem('dl.v2.accounts', JSON.stringify(value)), { deep: true })
watch(runs, value => localStorage.setItem('dl.v2.runs', JSON.stringify(value)), { deep: true })
watch(measurementView, value => localStorage.setItem('dl.v2.measurementView', JSON.stringify(value)))
async function syncPath() {
  const id = metricFromPath()
  const entry = window.history.state?.pilotMetric
  const wasInMetric = Boolean(metricId.value)
  metricId.value = id
  if (id) {
    returnSection.value = entry?.section || 'mediciones'
    metricOrigin.value = entry?.origin || null
    returnScroll = entry?.scroll || 0
    await scrollToMetric(metricOrigin.value)
  } else if (wasInMetric) {
    active.value = returnSection.value
    metricOrigin.value = null
    await nextTick()
    window.scrollTo(0, returnScroll)
    returnFocus?.focus({ preventScroll: true })
  }
}
onMounted(() => window.addEventListener('popstate', syncPath))
onBeforeUnmount(() => { if (timer) clearInterval(timer); window.removeEventListener('popstate', syncPath) })

const lastRun = computed(() => runs.value[0] || null)
const displayedRun = computed(() => currentRun.value || lastRun.value)
const completedCount = computed(() => lastRun.value?.results?.length || 0)
const account = computed(() => accounts.value[0] || null)
const filteredMetrics = computed(() => {
  const query = search.value.trim().toLowerCase()
  return metrics.filter(metric => {
    const context = metricContexts[metric.id]
    return (measurementScope.value === 'todas' || context?.scope === measurementScope.value)
      && (pillarFilter.value === 'Todos' || metric.pillar === pillarFilter.value)
      && `${metric.id} ${metric.name} ${metric.dimension} ${metric.pillar} ${context?.resource || ''}`.toLowerCase().includes(query)
  })
})
const resultMap = computed(() => Object.fromEntries((lastRun.value?.results || []).map(result => [result.metricId, result])))
const selectedResult = computed(() => selectedMetric.value ? resultMap.value[selectedMetric.value.id] : null)
const progress = computed(() => currentRun.value ? Math.round(currentRun.value.done / metrics.length * 100) : 0)
const pageTitles = { inicio: ['Resumen general', ''], procesos: ['Procesos', ''], controles: ['Controles transversales', ''], cuentas: ['Conexiones', 'Configuración local de accesos'], inventario: ['Datos', ''], mediciones: ['Mediciones', ''], ejecuciones: ['Historial', ''] }
const metricReturnLabel = computed(() => sections.find(section => section.id === returnSection.value)?.label || 'Mediciones')
const metricBackLabel = computed(() => {
  if (metricOrigin.value?.kind === 'Bucket S3') return 'Volver al bucket'
  if (metricOrigin.value?.kind === 'Resumen de buckets') return 'Volver al resumen de buckets'
  if (metricOrigin.value?.kind === 'Proceso Glue') return 'Volver al proceso'
  if (metricOrigin.value) return 'Volver a la ficha'
  return `Volver a ${metricReturnLabel.value}`
})
function closeTemporaryDrawer() { if (window.innerWidth < 960) drawer.value = false }
function selectMeasurementScope(scope) {
  measurementScope.value = scope
  search.value = ''
  pillarFilter.value = 'Todos'
}
function navigate(id, scope = 'todas') {
  if (metricId.value) {
    metricId.value = ''
    metricOrigin.value = null
    window.history.replaceState({}, '', appBase)
  }
  active.value = id
  search.value = ''
  if (id === 'mediciones') selectMeasurementScope(scope)
  if (id === 'inventario') inventoryEntryType.value = scope === 'todas' ? 'Todos' : scope
  closeTemporaryDrawer()
  window.scrollTo(0, 0)
}
async function openMetric(metric, origin = null) {
  const id = typeof metric === 'string' ? metric : metric.id
  if (!metrics.some(m => m.id === id)) return
  returnSection.value = active.value
  metricOrigin.value = origin
  returnScroll = window.scrollY
  returnFocus = document.activeElement
  metricId.value = id
  closeTemporaryDrawer()
  window.history.pushState({ pilotMetric: { section: active.value, origin, scroll: returnScroll } }, '', `${appBase}metricas/${id}/`)
  await scrollToMetric(origin)
}
async function scrollToMetric(origin) {
  await nextTick()
  if (origin?.focus) {
    const target = document.getElementById(origin.focus)
    target?.scrollIntoView({ block: 'start' })
    target?.focus({ preventScroll: true })
  } else {
    window.scrollTo(0, 0)
    document.getElementById('metric-title')?.focus({ preventScroll: true })
  }
}
function closeMetric() {
  closeTemporaryDrawer()
  if (window.history.state?.pilotMetric) {
    window.history.back()
    return
  }
  metricId.value = ''
  active.value = returnSection.value
  metricOrigin.value = null
  window.history.replaceState({}, '', appBase)
  window.scrollTo(0, 0)
}
function resultFor(metric) { return resultMap.value[metric.id] }
function formatValue(metric) {
  const result = resultFor(metric)
  if (!result) return '—'
  if (metric.id === 'M-04') return `${metric.num} solicitudes`
  if (metric.den > 0) return `${(metric.num / metric.den * 100).toFixed(1).replace('.', ',')} %`
  return `${metric.num} ${metric.unit}`
}
function saveAccount() {
  const f = accountForm.value
  if (!/^\d{12}$/.test(f.id) || !/^arn:aws:iam::\d{12}:role\/.+/.test(f.roleArn) || !f.name.trim()) { notice.value = 'Completa el nombre, un ID de cuenta de 12 dígitos y un ARN de rol válido.'; return }
  if (accounts.value.some(a => a.id === f.id)) { notice.value = 'Esa cuenta ya está en la lista.'; return }
  accounts.value.push({ id: f.id, name: f.name.trim(), region: f.region, roleArn: f.roleArn.trim(), externalId: f.externalId.trim(), mode: 'configurada', status: 'Sin verificar' })
  accountDialog.value = false
  accountForm.value = { name: '', id: '', roleArn: '', externalId: '', region: 'us-east-1' }
  notice.value = 'Configuración guardada en este navegador. La conexión todavía no se verifica.'
}
function makeResult(m) {
  return { metricId: m.id, value: m.den > 0 ? Number((m.num / m.den * 100).toFixed(1)) : m.num, num: m.num, den: m.den, unit: m.unit, status: 'Calculada', source: 'Fixture local', coverage: 'Escenario de prueba', evidence: m.operations.map((op, i) => `${m.id}-SIM-${String(i + 1).padStart(2, '0')}`), records: recordsFor(m) }
}
function startSimulation() {
  if (currentRun.value) return
  navigate('ejecuciones')
  currentRun.value = { id: `SIM-${Date.now().toString().slice(-8)}`, fixtureVersion, startedAt: new Date().toISOString(), endedAt: null, origin: 'Fixture local · sin consultas externas', accountId: account.value?.id || 'demo-local', region: account.value?.region || 'ejemplo', status: 'En curso', done: 0, results: [], events: ['Iniciando lote de medición…'] }
  const run = currentRun.value
  timer = setInterval(() => {
    const m = metrics[run.done]
    if (!m) return
    run.results.push(makeResult(m))
    run.done += 1
    run.events.unshift(`${m.id} · ${m.dimension}: datos de ejemplo procesados`)
    if (run.done === metrics.length) {
      clearInterval(timer); timer = null
      run.status = 'Finalizada'; run.endedAt = new Date().toISOString()
      runs.value.unshift({ ...run, results: [...run.results], events: [...run.events] }); runs.value = runs.value.slice(0, 5)
      currentRun.value = null
      notice.value = 'Simulación finalizada: 13 resultados de ejemplo. No se consultaron fuentes externas.'
    }
  }, 240)
}
function downloadResults() {
  if (!lastRun.value) return
  const payload = { warning: 'DATOS SIMULADOS. No son resultados observados en fuentes externas.', run: lastRun.value, metrics: metrics.map(m => ({ id: m.id, name: m.name, pillar: m.pillar, dimension: m.dimension, result: { ...resultFor(m), records: resultFor(m)?.records || recordsFor(m) } })) }
  const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }))
  const link = document.createElement('a'); link.href = url; link.download = `data-lens-${lastRun.value.id}.json`; link.click(); URL.revokeObjectURL(url)
}
function dateTime(value) { return value ? new Intl.DateTimeFormat('es-CL', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(value)) : '—' }
</script>

<template>
  <v-app>
    <v-navigation-drawer id="pilot-sidebar" v-model="drawer" :permanent="mdAndUp" :temporary="!mdAndUp" :rail="compactSidebar" :rail-width="64" width="252" class="side-nav">
      <template #prepend>
        <div class="brand-wrap"><div class="brand-icon" :title="compactSidebar ? 'Data Lens' : undefined"><v-icon icon="mdi-chart-arc" size="23" /></div><div v-if="!compactSidebar"><div class="brand-name">Data Lens<span>.</span></div><div class="brand-sub">ASSESSMENT DE DATOS</div></div></div>
      </template>
      <v-list nav density="comfortable" class="nav-list">
        <v-list-item v-for="item in sections" :key="item.id" :active="selectedMetric ? returnSection === item.id : active === item.id" :prepend-icon="item.icon" :title="item.label" @click="navigate(item.id)" />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar flat height="72" class="top-bar">
      <button v-if="mdAndUp" type="button" class="sidebar-toggle" aria-controls="pilot-sidebar"
        :aria-label="compactSidebar ? 'Ampliar menú lateral' : 'Minimizar menú lateral'"
        :aria-expanded="!compactSidebar" @click="sidebarMinimized = !sidebarMinimized">
        <v-icon :icon="compactSidebar ? 'mdi-chevron-double-right' : 'mdi-chevron-double-left'" size="20" />
        <v-tooltip activator="parent" location="bottom" :text="compactSidebar ? 'Ampliar menú lateral' : 'Minimizar menú lateral'" />
      </button>
      <v-app-bar-nav-icon v-else aria-label="Abrir menú" :aria-expanded="Boolean(drawer)" @click="drawer = !drawer" />
      <div class="top-context"><span class="top-breadcrumb">Data Lens</span><v-icon icon="mdi-chevron-right" size="16" color="#a1aabc" /><span>{{ selectedMetric ? metricReturnLabel : pageTitles[active][0] }}</span></div><v-spacer /><div class="top-avatar">DL</div>
    </v-app-bar>

    <v-main class="main-area">
      <MetricDetail v-if="selectedMetric" :key="selectedMetric.id" :metric="selectedMetric"
        :result="selectedResult" :display-value="formatValue(selectedMetric)"
        :resource="metricContexts[selectedMetric.id]?.resource" :run="lastRun"
        :return-label="metricBackLabel" :origin-name="metricOrigin?.name"
        :record-search="metricOrigin?.recordSearch" @back="closeMetric" />
      <div v-show="!selectedMetric" :key="active" :class="['page-wrap screen-enter', {
        'entity-focused': active === 'inventario' && inventoryFocused,
        'measurements-page': ['mediciones', 'controles'].includes(active),
      }]">
      <div class="demo-banner"><v-icon icon="mdi-information-outline" size="19" /><div><strong>Datos de ejemplo.</strong><span> Datos sintéticos · Sin conexión AWS real.</span></div></div>
      <div v-if="!(active === 'inventario' && inventoryFocused)" class="page-heading"><div><h1>{{ pageTitles[active][0] }}</h1><p v-if="pageTitles[active][1]">{{ pageTitles[active][1] }}</p></div><div class="heading-actions"><v-btn v-if="active === 'cuentas'" color="primary" prepend-icon="mdi-plus" rounded="lg" @click="accountDialog = true">Agregar cuenta</v-btn><v-btn v-else-if="['mediciones', 'ejecuciones'].includes(active) && lastRun" variant="outlined" prepend-icon="mdi-download-outline" rounded="lg" @click="downloadResults">Exportar JSON</v-btn><v-btn v-else-if="active === 'inicio'" color="primary" prepend-icon="mdi-play" rounded="lg" :disabled="!!currentRun" @click="startSimulation">Simular medición</v-btn></div></div>

      <template v-if="active === 'inicio'">
        <section class="summary-grid inventory-summary" aria-label="Inventario del escenario">
          <button type="button" class="surface summary-stat" @click="navigate('inventario', 'Agrupaciones')">
            <v-icon icon="mdi-database-outline" size="22" /><strong>{{ databases.length }}</strong><span>Agrupaciones</span>
          </button>
          <button type="button" class="surface summary-stat" @click="navigate('inventario', 'Agrupaciones')">
            <v-icon icon="mdi-table" size="22" /><strong>{{ dataZoneAssets.length }}</strong><span>Tablas / datasets</span>
          </button>
          <button type="button" class="surface summary-stat" @click="navigate('inventario', 'Buckets S3')">
            <v-icon icon="mdi-bucket-outline" size="22" /><strong>{{ buckets.length }}</strong><span>Buckets S3</span>
          </button>
          <button type="button" class="surface summary-stat" @click="navigate('procesos')">
            <v-icon icon="mdi-cog-outline" size="22" /><strong>1</strong><span>Proceso Glue</span>
          </button>
        </section>
        <section class="overview-results" aria-labelledby="summary-metrics-title">
          <div class="base-evaluation-heading">
            <div><h2 id="summary-metrics-title">Panorama general</h2><p>{{ lastRun ? `Última simulación · ${dateTime(lastRun.endedAt)}` : 'Vista previa con datos de ejemplo' }}</p></div>
            <v-btn color="primary" variant="tonal" size="small" append-icon="mdi-arrow-right" @click="navigate('mediciones')">Ver las {{ metrics.length }} métricas</v-btn>
          </div>
          <ControlSummary :metrics="overviewMetrics" :results="lastRun?.results || []" :contexts="metricContexts" @metric="openMetric" />
        </section>
      </template>

      <template v-else-if="active === 'cuentas'">
        <div class="two-col accounts-layout">
          <section class="surface table-panel">
            <div class="panel-head"><div><div class="section-kicker">CONFIGURACIÓN LOCAL</div><h2>Cuentas registradas</h2></div><span class="count-label">{{ accounts.length }} cuenta{{ accounts.length === 1 ? '' : 's' }}</span></div>
            <div v-for="a in accounts" :key="a.id" class="account-row"><div class="account-logo"><v-icon icon="mdi-cloud-outline" size="24" /></div><div class="account-main"><strong>{{ a.name }}</strong><small>{{ a.id }} · {{ a.region }}</small><small v-if="a.roleArn" class="arn">{{ a.roleArn }}</small></div><span class="status-pill" :class="a.mode === 'simulada' ? 'amber-status' : 'muted'">{{ a.status }}</span></div>
            <div class="inline-info"><v-icon icon="mdi-information-outline" size="18" /><span>Estas cuentas se guardan solo en este navegador. Todavía no se comprueba el acceso ni se consultan recursos.</span></div>
          </section>
          <section class="surface guide-panel"><div class="section-kicker">CONEXIÓN PREVISTA</div><h2>Cómo se usarán las cuentas</h2><div class="guide-item"><span>01</span><div><strong>Registrar la cuenta</strong><p>Ingresa el identificador, la región inicial y el rol de lectura del piloto.</p></div></div><div class="guide-item"><span>02</span><div><strong>Verificar acceso</strong><p>Una futura integración comprobará el rol y los permisos disponibles.</p></div></div><div class="guide-item"><span>03</span><div><strong>Medir con evidencia</strong><p>Solo después de la conexión se podrán consultar recursos y ejecutar mediciones reales.</p></div></div><v-alert type="info" variant="tonal" density="compact" class="mt-5">La conexión real todavía no está implementada.</v-alert></section>
        </div>
      </template>

      <template v-else-if="active === 'inventario'">
        <DataInventory :metrics="metrics" :buckets="buckets" :initial-type="inventoryEntryType"
          :results="lastRun?.results || []" :metric-contexts="metricContexts" @focus="inventoryFocused = $event"
          @metric="openMetric" @measurements="navigate('mediciones')" />
      </template>
      <template v-else-if="active === 'procesos'"><ProcessList @metric="openMetric" /></template>

      <template v-else-if="active === 'controles'">
        <p class="control-intro">Resultados generales de acceso, auditoría y privacidad.</p>
        <ControlSummary :metrics="controlMetrics" :results="lastRun?.results || []" :contexts="metricContexts" @metric="openMetric" />
      </template>

      <template v-else-if="active === 'mediciones'">
        <div class="measurement-controls"><span>Última simulación: {{ lastRun ? dateTime(lastRun.endedAt) : 'Sin ejecución' }} · {{ completedCount }} / 13 métricas</span></div>
        <div class="measurement-scopes" role="group" aria-label="Ámbito de medición">
          <v-btn v-for="scope in scopeFilters" :key="scope.id" size="small" color="primary"
            :variant="measurementScope === scope.id ? 'flat' : 'tonal'"
            :aria-pressed="measurementScope === scope.id" @click="selectMeasurementScope(scope.id)">
            {{ scope.label }} ({{ scopeCounts[scope.id] }})
          </v-btn>
        </div>
        <div class="catalog-toolbar"><v-text-field v-model="search" label="Buscar métrica, ID o recurso" prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details /><v-select v-model="pillarFilter" :items="['Todos', ...pillars]" label="Pilar" variant="outlined" density="compact" hide-details /><span aria-live="polite">{{ filteredMetrics.length }} métricas</span></div>
        <div class="measurement-view-switch" role="group" aria-label="Vista de mediciones">
          <v-btn v-for="view in measurementViews" :key="view.id" size="small" color="primary"
            :prepend-icon="view.icon" :variant="measurementView === view.id ? 'flat' : 'tonal'"
            :aria-pressed="measurementView === view.id" @click="measurementView = view.id">
            {{ view.label }}
          </v-btn>
        </div>
        <p v-if="!filteredMetrics.length" class="surface empty-row">Sin coincidencias.</p>
        <ControlSummary v-else-if="measurementView === 'tarjetas'" :metrics="filteredMetrics" :results="lastRun?.results || []"
          :contexts="metricContexts" catalog @metric="openMetric" />
        <section v-else class="surface" aria-label="Lista de métricas">
          <button v-for="m in filteredMetrics" :key="m.id" type="button" class="catalog-metric-row" @click="openMetric(m)">
            <span class="metric-list-copy"><span class="metric-code">{{ m.id }}</span><strong>{{ m.name }}</strong>
              <small class="measurement-resource">{{ metricContexts[m.id]?.resource }}</small>
            </span>
            <span>{{ formatValue(m) }}<small>{{ resultFor(m) ? 'Simulado' : 'Sin ejecución' }}</small></span>
            <v-icon icon="mdi-chevron-right" />
          </button>
        </section>
      </template>

      <template v-else-if="active === 'ejecuciones'">
        <div class="simulation-history"><div class="two-col execution-layout"><section class="surface execution-main"><div class="section-kicker">MOTOR DE MEDICIÓN</div><h2>Historial de simulaciones</h2><p class="panel-desc">La conexión a fuentes reales está pendiente de integración y permisos.</p><div class="run-console"><div class="console-top"><div><span class="console-signal" :class="currentRun ? 'running' : ''" />{{ currentRun ? 'EJECUCIÓN EN CURSO' : lastRun ? 'ÚLTIMA EJECUCIÓN' : 'LISTO PARA SIMULAR' }}</div><span>{{ displayedRun?.id || '—' }}</span></div><div class="console-content"><div class="console-stat"><span>Origen de datos</span><strong>Fixture local</strong></div><div class="console-stat"><span>Métricas procesadas</span><strong>{{ currentRun?.done ?? lastRun?.results.length ?? 0 }} / 13</strong></div><div class="console-stat"><span>Estado</span><strong>{{ currentRun ? 'En curso' : lastRun ? 'Finalizada' : 'Pendiente' }}</strong></div></div><div v-if="currentRun" class="progress-wrap"><div class="progress-label"><span>Procesando métricas</span><strong>{{ progress }} %</strong></div><v-progress-linear :model-value="progress" color="primary" height="8" rounded /></div></div><div v-if="lastRun" class="run-actions"><v-btn variant="outlined" rounded="lg" prepend-icon="mdi-chart-line" @click="navigate('mediciones')">Ver mediciones</v-btn></div><v-alert type="warning" variant="tonal" density="compact" class="mt-6">Esta acción no valida accesos a fuentes externas.</v-alert></section><section class="surface events-panel"><div class="section-kicker">ACTIVIDAD</div><h2>Eventos de la simulación</h2><div v-if="displayedRun" class="events-list"><div v-for="(event, i) in displayedRun.events.slice(0, 14)" :key="`${displayedRun.id}-${i}`" class="event-item event-enter"><span class="event-dot" /><span>{{ event.replace(/^M-\d{2} · /u, '') }}</span></div></div><div v-else class="empty-events"><v-icon icon="mdi-text-box-search-outline" size="38" /><p>Aquí aparecerán los eventos de la simulación.</p></div></section></div><section v-if="runs.length" class="surface table-panel mt-5"><div class="panel-head"><div><div class="section-kicker">HISTORIAL LOCAL</div><h2>Simulaciones finalizadas</h2></div></div><div class="table-scroll"><table class="data-table"><thead><tr><th>ID</th><th>FECHA</th><th>ORIGEN</th><th>MÉTRICAS</th><th>ESTADO</th></tr></thead><tbody><tr v-for="r in runs.slice(0, 5)" :key="r.id"><td><strong>{{ r.id }}</strong></td><td>{{ dateTime(r.endedAt) }}</td><td>Fixture local</td><td>{{ r.results.length }} / 13</td><td><span class="status-pill success">Finalizada</span></td></tr></tbody></table></div></section></div>
      </template>




    </div></v-main>

    <v-dialog v-model="accountDialog" max-width="610"><v-card rounded="xl" class="dialog-card"><div class="dialog-head"><div><div class="section-kicker">CONFIGURACIÓN DE ACCESO</div><h2>Agregar cuenta</h2></div><v-btn icon="mdi-close" variant="text" @click="accountDialog = false" /></div><p class="dialog-intro">Guarda los parámetros de conexión en este navegador. La verificación estará disponible cuando se integre el backend.</p><v-form @submit.prevent="saveAccount"><div class="dialog-fields"><v-text-field v-model="accountForm.name" label="Nombre de la cuenta" variant="outlined" density="comfortable" /><v-text-field v-model="accountForm.id" label="ID de cuenta (12 dígitos)" variant="outlined" density="comfortable" /><v-text-field v-model="accountForm.roleArn" label="ARN del rol de lectura" variant="outlined" density="comfortable" /><v-text-field v-model="accountForm.externalId" label="ID externo (si corresponde)" variant="outlined" density="comfortable" /><v-select v-model="accountForm.region" :items="['us-east-1','us-east-2','us-west-2','sa-east-1','eu-west-1']" label="Región inicial" variant="outlined" density="comfortable" /></div><div class="dialog-actions"><v-btn variant="text" @click="accountDialog = false">Cancelar</v-btn><v-btn type="submit" color="primary">Guardar configuración</v-btn></div></v-form></v-card></v-dialog>

    <v-snackbar :model-value="!!notice" @update:model-value="value => { if (!value) notice = '' }" :timeout="5000" color="#172b48">{{ notice }}<template #actions><v-btn variant="text" @click="notice = ''">Cerrar</v-btn></template></v-snackbar>
  </v-app>
</template>
