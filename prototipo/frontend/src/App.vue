<script setup>
import { computed, nextTick, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useDisplay } from 'vuetify'
import metrics from './data/metrics.json'
import { assets, databases, dataZoneAssets, populationFor } from './data/fixtures.js'
import DatabaseMap from './components/DatabaseMap.vue'
import MetricDetail from './components/MetricDetail.vue'

const sections = [
  { id: 'inicio', label: 'Resumen', icon: 'mdi-view-dashboard-outline' },
  { id: 'cuentas', label: 'Cuentas', icon: 'mdi-cloud-outline' },
  { id: 'inventario', label: 'Inventario', icon: 'mdi-database-outline' },
  { id: 'mediciones', label: 'Métricas', icon: 'mdi-chart-box-outline' },
  { id: 'ejecuciones', label: 'Ejecuciones', icon: 'mdi-progress-check' },
]
const icons = { Responsabilidad: 'mdi-account-key-outline', Visibilidad: 'mdi-eye-outline', Calidad: 'mdi-check-decagram-outline', 'Acceso y seguridad': 'mdi-shield-lock-outline', 'Cumplimiento y privacidad': 'mdi-file-lock-outline' }
const colors = { Responsabilidad: '#6674f4', Visibilidad: '#0ca7bd', Calidad: '#18a781', 'Acceso y seguridad': '#e6a13c', 'Cumplimiento y privacidad': '#aa74d8' }
const signalLabels = {
  'M-01': 'activos sin responsable informado', 'M-04': 'solicitudes pendientes',
  'M-07': 'campos requeridos faltantes', 'M-09': 'tramos de linaje registrados',
  'M-11': 'filas que fallan la regla', 'M-16': 'ejecuciones fallidas',
  'M-18': 'reglas sin resultado', 'M-21': 'hallazgos de permisos activos',
  'M-22': 'objetos con SSE-KMS', 'M-25': 'registros con campos faltantes',
  'M-26': 'activos sin clasificación informada', 'M-27': 'casos con intervención',
  'M-29': 'reglas deshabilitadas',
}
const pillars = [...new Set(metrics.map(m => m.pillar))]
const metricGroups = pillars.map(pillar => ({ pillar, items: metrics.filter(metric => metric.pillar === pillar) }))
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
const accounts = ref(readStorage('dl.accounts', defaultAccounts))
const active = ref('inicio')
const drawer = ref(null)
const { mdAndUp } = useDisplay()
const sidebarMinimized = ref(false)
const compactSidebar = computed(() => mdAndUp.value && sidebarMinimized.value)
const search = ref('')
const openCatalogPillars = ref([pillars[0]])
const serviceFilter = ref('Todos')
const inventoryView = ref('mapa')
const metricId = ref(metricFromPath())
const returnSection = ref('mediciones')
const selectedMetric = computed(() => metrics.find(m => m.id === metricId.value) || null)
const openPillar = ref(null)
watch(selectedMetric, metric => { openPillar.value = metric?.pillar ?? null }, { immediate: true })
const accountDialog = ref(false)
const accountForm = ref({ name: '', id: '', roleArn: '', externalId: '', region: 'us-east-1' })
const notice = ref('')
const currentRun = ref(null)
const runs = ref(readStorage('dl.runs', []).map(refreshDemoRun))
let timer = null

watch(accounts, value => localStorage.setItem('dl.accounts', JSON.stringify(value)), { deep: true })
watch(runs, value => localStorage.setItem('dl.runs', JSON.stringify(value)), { deep: true })
function syncPath() { metricId.value = metricFromPath(); if (!metricId.value) active.value = returnSection.value }
onMounted(() => window.addEventListener('popstate', syncPath))
onBeforeUnmount(() => { if (timer) clearInterval(timer); window.removeEventListener('popstate', syncPath) })

const lastRun = computed(() => runs.value[0] || null)
const displayedRun = computed(() => currentRun.value || lastRun.value)
const completedCount = computed(() => lastRun.value?.results?.length || 0)
const account = computed(() => accounts.value[0] || null)
const filteredMetrics = computed(() => metrics.filter(m => `${m.name} ${m.dimension} ${m.pillar}`.toLowerCase().includes(search.value.toLowerCase())))
const catalogGroups = computed(() => pillars.map(pillar => ({ pillar, items: filteredMetrics.value.filter(metric => metric.pillar === pillar) })).filter(group => group.items.length))
const filteredAssets = computed(() => assets.filter(a => (serviceFilter.value === 'Todos' || a.service === serviceFilter.value) && `${a.title} ${a.name} ${a.kind} ${a.owner} ${a.id}`.toLowerCase().includes(search.value.toLowerCase())))
const services = [...new Set(assets.map(a => a.service))]
const resultMap = computed(() => Object.fromEntries((lastRun.value?.results || []).map(r => [r.metricId, r])))
const metricSignals = computed(() => metrics.map(metric => {
  const records = resultMap.value[metric.id]?.records || recordsFor(metric)
  const informational = ['M-09', 'M-22', 'M-27'].includes(metric.id)
  const observedShare = metric.id === 'M-22' || metric.id === 'M-27'
  const attention = metric.kind === 'count' || observedShare ? records.filter(row => row.inNumerator).length : records.filter(row => row.tone === 'error' || row.tone === 'warning').length
  return { metric, total: records.length, attention, informational, pct: metric.kind === 'count' ? null : records.length ? Math.round(attention / records.length * 100) : 0, signalLabel: signalLabels[metric.id] }
}))
const pillarSignals = computed(() => pillars.map(pillar => {
  const items = metricSignals.value.filter(item => item.metric.pillar === pillar)
  return { pillar, items }
}))
const selectedResult = computed(() => selectedMetric.value ? resultMap.value[selectedMetric.value.id] : null)
const progress = computed(() => currentRun.value ? Math.round(currentRun.value.done / metrics.length * 100) : 0)
const pageTitles = { inicio: ['Resumen general', ''], cuentas: ['Cuentas', 'Configuración local de accesos'], inventario: ['Inventario', ''], mediciones: ['Métricas por pilar', 'Selecciona un pilar y después una métrica'], ejecuciones: ['Ejecuciones', ''] }
const inventoryViews = [
  { id: 'mapa', label: 'Mapa de bases', icon: 'mdi-sitemap-outline' },
  { id: 'lista', label: 'Lista de recursos', icon: 'mdi-format-list-bulleted' },
]
const metricReturnLabel = computed(() => sections.find(section => section.id === returnSection.value).label)
function closeTemporaryDrawer() { if (window.innerWidth < 960) drawer.value = false }
async function expandCompactPillar(pillar, index) {
  sidebarMinimized.value = false
  openPillar.value = pillar
  await nextTick()
  document.getElementById(`pilot-pillar-toggle-${index}`)?.focus()
}
function navigate(id) { active.value = id; search.value = ''; serviceFilter.value = 'Todos'; closeTemporaryDrawer() }
function showPillarMetrics(pillar) { if (!openCatalogPillars.value.includes(pillar)) openCatalogPillars.value.push(pillar); search.value = ''; active.value = 'mediciones'; window.scrollTo(0, 0) }
function toggleCatalogPillar(pillar) { openCatalogPillars.value = openCatalogPillars.value.includes(pillar) ? openCatalogPillars.value.filter(item => item !== pillar) : [...openCatalogPillars.value, pillar] }
function openMetric(metric) {
  const id = typeof metric === 'string' ? metric : metric.id
  if (!metrics.some(m => m.id === id)) return
  if (!selectedMetric.value) returnSection.value = active.value
  metricId.value = id
  closeTemporaryDrawer()
  window.history.pushState({}, '', `${appBase}metricas/${id}/`)
  window.scrollTo(0, 0)
}
function closeMetric() {
  metricId.value = ''
  active.value = returnSection.value
  closeTemporaryDrawer()
  window.history.pushState({}, '', appBase)
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
  active.value = 'ejecuciones'
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
      <nav v-if="compactSidebar" class="compact-nav" :aria-label="selectedMetric ? 'Navegación de métricas' : 'Espacio de trabajo'">
        <template v-if="selectedMetric">
          <button type="button" class="compact-nav-button" :aria-label="`Volver a ${metricReturnLabel}`" @click="closeMetric">
            <v-icon icon="mdi-arrow-left" size="20" />
            <v-tooltip activator="parent" location="end" :text="`Volver a ${metricReturnLabel}`" />
          </button>
          <button v-for="({ pillar }, index) in metricGroups" :key="pillar" type="button" class="compact-nav-button" :style="{ color: colors[pillar] }"
            :aria-current="selectedMetric.pillar === pillar ? 'true' : undefined" :aria-label="pillar" @click="expandCompactPillar(pillar, index)">
            <v-icon :icon="icons[pillar]" size="20" />
            <v-tooltip activator="parent" location="end" :text="pillar" />
          </button>
        </template>
        <template v-else>
          <button v-for="item in sections" :key="item.id" type="button" class="compact-nav-button"
            :aria-current="active === item.id ? 'page' : undefined" :aria-label="item.label" @click="navigate(item.id)">
            <v-icon :icon="item.icon" size="20" />
            <v-tooltip activator="parent" location="end" :text="item.label" />
          </button>
        </template>
      </nav>
      <nav v-else-if="selectedMetric" class="metric-rail" aria-label="Navegación de métricas">
        <button type="button" class="metric-back" @click="closeMetric"><v-icon icon="mdi-arrow-left" size="18" /> Volver a {{ metricReturnLabel }}</button>
        <div class="metric-rail-title">MÉTRICAS DEL PILOTO <span>{{ metrics.length }}</span></div>
        <div v-for="({ pillar, items }, index) in metricGroups" :key="pillar" class="metric-rail-group" :style="{ '--pillar-color': colors[pillar], '--pillar-soft': colors[pillar] + '18' }">
          <button :id="`pilot-pillar-toggle-${index}`" type="button" class="metric-rail-pillar" :class="{ current: selectedMetric.pillar === pillar }"
            :aria-expanded="openPillar === pillar" :aria-controls="`pilot-pillar-${index}`"
            :aria-label="`${pillar}, ${items.length} métricas${selectedMetric.pillar === pillar ? ', pilar de la métrica actual' : ''}`"
            @click="openPillar = openPillar === pillar ? null : pillar">
            <v-icon :icon="icons[pillar]" size="17" aria-hidden="true" />
            <span class="metric-rail-pillar-name">{{ pillar }}</span>
            <span class="metric-rail-pillar-count" aria-hidden="true">{{ items.length }}</span>
            <v-icon :icon="openPillar === pillar ? 'mdi-chevron-up' : 'mdi-chevron-down'" size="16" aria-hidden="true" />
          </button>
          <div v-show="openPillar === pillar" :id="`pilot-pillar-${index}`" class="metric-rail-pillar-items">
            <button v-for="item in items" :key="item.id" type="button" class="metric-rail-item" :class="{ active: item.id === selectedMetric.id }" :aria-current="item.id === selectedMetric.id ? 'page' : undefined" @click="openMetric(item.id)">
              <span class="metric-rail-copy"><strong>{{ item.name }}</strong><small>{{ resultFor(item) ? `Calculada · ${formatValue(item)}` : 'Pendiente' }}</small></span>
              <span class="metric-rail-dot" :class="resultFor(item) ? 'calculated' : 'pending'" />
            </button>
          </div>
        </div>
      </nav>
      <template v-else>
        <div class="nav-caption">ESPACIO DE TRABAJO</div>
        <v-list nav density="comfortable" class="nav-list">
          <v-list-item v-for="item in sections" :key="item.id" :active="active === item.id" :prepend-icon="item.icon" :title="item.label" rounded="lg" @click="navigate(item.id)" />
        </v-list>
      </template>
    </v-navigation-drawer>

    <v-app-bar flat height="72" class="top-bar">
      <button v-if="mdAndUp" type="button" class="sidebar-toggle" aria-controls="pilot-sidebar"
        :aria-label="compactSidebar ? 'Ampliar menú lateral' : 'Minimizar menú lateral'"
        :aria-expanded="!compactSidebar" @click="sidebarMinimized = !sidebarMinimized">
        <v-icon :icon="compactSidebar ? 'mdi-chevron-double-right' : 'mdi-chevron-double-left'" size="20" />
        <v-tooltip activator="parent" location="bottom" :text="compactSidebar ? 'Ampliar menú lateral' : 'Minimizar menú lateral'" />
      </button>
      <v-app-bar-nav-icon v-else :aria-label="selectedMetric ? 'Abrir navegación de métricas' : 'Abrir menú'" :aria-expanded="Boolean(drawer)" @click="drawer = !drawer" />
      <div class="top-context"><span class="top-breadcrumb">Data Lens</span><v-icon icon="mdi-chevron-right" size="16" color="#a1aabc" /><span>{{ selectedMetric ? selectedMetric.dimension : pageTitles[active][0] }}</span></div><v-spacer /><div class="top-avatar">DL</div>
    </v-app-bar>

    <v-main class="main-area"><MetricDetail v-if="selectedMetric" :key="selectedMetric.id" :metric="selectedMetric" :metrics="metrics" :result="selectedResult" :display-value="formatValue(selectedMetric)" :run="lastRun" :return-label="metricReturnLabel" @select="openMetric" @back="closeMetric" /><div v-else class="page-wrap">
      <div class="demo-banner"><v-icon icon="mdi-information-outline" size="19" /><div><strong>Datos de ejemplo.</strong><span> Las mediciones son simuladas.</span></div></div>
      <div class="page-heading"><div><h1>{{ pageTitles[active][0] }}</h1><p v-if="pageTitles[active][1]">{{ pageTitles[active][1] }}</p></div><div class="heading-actions"><v-btn v-if="active === 'cuentas'" color="primary" prepend-icon="mdi-plus" rounded="lg" @click="accountDialog = true">Agregar cuenta</v-btn><v-btn v-else-if="active === 'mediciones' && lastRun" variant="outlined" prepend-icon="mdi-download-outline" rounded="lg" @click="downloadResults">Exportar JSON</v-btn><v-btn v-else-if="active !== 'ejecuciones'" color="primary" prepend-icon="mdi-play" rounded="lg" :disabled="!!currentRun" @click="startSimulation">Simular medición</v-btn></div></div>

      <template v-if="active === 'inicio'">
        <section class="overview-surface surface" aria-label="Resumen por pilar">
          <div class="overview-head"><strong>Resultados por pilar</strong><div class="overview-legend"><span><i class="legend-clear" />Sin condición señalada</span><span><i class="legend-issue" />A revisar</span><span><i class="legend-info" />Descriptivo</span><small>Porcentaje sobre el universo de cada métrica</small></div></div>
          <button v-for="item in pillarSignals" :key="item.pillar" type="button" class="overview-row" @click="showPillarMetrics(item.pillar)">
            <span class="overview-pillar"><span class="pillar-symbol" :style="{ background: colors[item.pillar] + '1c', color: colors[item.pillar] }"><v-icon :icon="icons[item.pillar]" size="19" /></span><span><strong>{{ item.pillar }}</strong><small>{{ item.items.length }} métricas</small></span></span>
            <span class="overview-metrics"><span v-for="signal in item.items" :key="signal.metric.id" class="overview-metric" :class="{ informational: signal.informational }"><span class="overview-metric-title">{{ signal.signalLabel }}</span><span class="overview-metric-value">{{ signal.pct === null ? signal.attention : `${signal.attention} de ${signal.total} · ${signal.pct} %` }}</span><span v-if="signal.pct !== null" class="metric-bar" aria-hidden="true"><span class="metric-bar-clear" :style="{ width: `${100 - signal.pct}%` }" /><span class="metric-bar-issue" :style="{ width: `${signal.pct}%` }" /></span></span></span>
            <v-icon icon="mdi-chevron-right" size="20" class="overview-chevron" />
          </button>
          <div class="overview-foot">Las barras muestran condiciones de cada métrica; no son una calificación global ni permiten comparar directamente los pilares.</div>
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
        <div class="inventory-toolbar">
          <div><strong>Explorar el inventario</strong></div>
          <div class="inventory-switch" role="group" aria-label="Vista de inventario">
            <button v-for="view in inventoryViews" :key="view.id" type="button" :class="{ active: inventoryView === view.id }" :aria-pressed="inventoryView === view.id" @click="inventoryView = view.id">
              <v-icon :icon="view.icon" size="17" /> {{ view.label }}
            </button>
          </div>
        </div>
        <section v-if="inventoryView === 'mapa'" class="surface"><DatabaseMap :databases="databases" :assets="dataZoneAssets" /></section>
        <section v-else class="surface table-panel">
          <div class="panel-head"><div><div class="section-kicker">RECURSOS</div><h2>Inventario de activos</h2></div><span class="count-label">{{ filteredAssets.length }} recursos</span></div>
          <div class="filter-row"><v-text-field v-model="search" label="Buscar activo, ID o responsable" prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details class="search-field" /><v-select v-model="serviceFilter" :items="['Todos', ...services]" label="Servicio" variant="outlined" density="compact" hide-details class="filter-select" /></div>
          <div class="table-scroll">
            <table class="data-table inventory-data-table">
              <thead><tr><th>ACTIVO</th><th>SERVICIO</th><th>TIPO</th><th>REGIÓN</th><th>RESPONSABLE</th><th>ESTADO</th></tr></thead>
              <tbody>
                <tr v-for="a in filteredAssets" :key="a.id">
                  <td><strong>{{ a.title }}</strong><small class="table-sub" :title="a.id">{{ a.name }}</small></td><td>{{ a.service }}</td><td>{{ a.kind }}</td><td>{{ a.region }}</td><td>{{ a.owner || 'Sin responsable' }}</td><td><span class="status-pill muted">Simulado</span></td>
                </tr>
              </tbody>
            </table>
            <div v-if="!filteredAssets.length" class="empty-row">No hay activos que coincidan con el filtro.</div>
          </div>
        </section>
      </template>

      <template v-else-if="active === 'mediciones'">
        <div class="catalog-toolbar"><v-text-field v-model="search" label="Buscar métrica o dimensión" prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details class="search-field" /><span>{{ filteredMetrics.length }} métricas</span></div>
        <div v-for="(group, index) in catalogGroups" :key="group.pillar" class="metric-accordion surface" :style="{ '--pillar-color': colors[group.pillar], '--pillar-soft': colors[group.pillar] + '18' }">
          <button type="button" class="metric-accordion-toggle" :aria-expanded="openCatalogPillars.includes(group.pillar) || !!search" :aria-controls="`catalog-pillar-${index}`" @click="toggleCatalogPillar(group.pillar)">
            <span class="pillar-symbol" :style="{ background: colors[group.pillar] + '1c', color: colors[group.pillar] }"><v-icon :icon="icons[group.pillar]" size="20" /></span><span class="metric-accordion-title"><strong>{{ group.pillar }}</strong><small>{{ group.items.length }} métricas</small></span><v-icon :icon="openCatalogPillars.includes(group.pillar) || search ? 'mdi-chevron-up' : 'mdi-chevron-down'" size="22" />
          </button>
          <div v-show="openCatalogPillars.includes(group.pillar) || !!search" :id="`catalog-pillar-${index}`" class="metric-accordion-body">
            <button v-for="m in group.items" :key="m.id" type="button" class="catalog-metric-row" @click="openMetric(m)">
              <span><strong>{{ m.name }}</strong><small>{{ m.dimension }}</small></span><span class="catalog-metric-result">{{ formatValue(m) }}<small>{{ resultFor(m) ? 'Calculada' : 'Sin ejecución' }}</small></span><v-icon icon="mdi-chevron-right" size="18" />
            </button>
          </div>
        </div>
        <div v-if="!catalogGroups.length" class="surface catalog-empty">No hay métricas que coincidan con la búsqueda.</div>
      </template>

      <template v-else-if="active === 'ejecuciones'"><div class="two-col execution-layout"><section class="surface execution-main"><div class="section-kicker">MOTOR DE MEDICIÓN</div><h2>Ejecutar lote de 13 métricas</h2><p class="panel-desc">La conexión a fuentes reales está pendiente de integración y permisos.</p><div class="run-console"><div class="console-top"><div><span class="console-signal" :class="currentRun ? 'running' : ''" />{{ currentRun ? 'EJECUCIÓN EN CURSO' : lastRun ? 'ÚLTIMA EJECUCIÓN' : 'LISTO PARA SIMULAR' }}</div><span>{{ displayedRun?.id || '—' }}</span></div><div class="console-content"><div class="console-stat"><span>Origen de datos</span><strong>Fixture local</strong></div><div class="console-stat"><span>Métricas procesadas</span><strong>{{ currentRun?.done ?? lastRun?.results.length ?? 0 }} / 13</strong></div><div class="console-stat"><span>Estado</span><strong>{{ currentRun ? 'En curso' : lastRun ? 'Finalizada' : 'Pendiente' }}</strong></div></div><div v-if="currentRun" class="progress-wrap"><div class="progress-label"><span>Procesando métricas</span><strong>{{ progress }} %</strong></div><v-progress-linear :model-value="progress" color="primary" height="8" rounded /></div></div><div class="run-actions"><v-btn color="primary" prepend-icon="mdi-play" rounded="lg" :loading="!!currentRun" @click="startSimulation">{{ lastRun ? 'Repetir simulación' : 'Iniciar simulación' }}</v-btn><v-btn v-if="lastRun" variant="outlined" rounded="lg" prepend-icon="mdi-chart-line" @click="navigate('mediciones')">Ver métricas</v-btn></div><v-alert type="warning" variant="tonal" density="compact" class="mt-6">Esta acción no valida accesos a fuentes externas.</v-alert></section><section class="surface events-panel"><div class="section-kicker">ACTIVIDAD</div><h2>Registro de ejecución</h2><div v-if="displayedRun" class="events-list"><div v-for="(event, i) in displayedRun.events.slice(0, 14)" :key="i" class="event-item"><span class="event-dot" /><span>{{ event.replace(/^M-\d{2} · /u, '') }}</span></div></div><div v-else class="empty-events"><v-icon icon="mdi-text-box-search-outline" size="38" /><p>Aquí aparecerán los eventos de la simulación.</p></div></section></div><section v-if="runs.length" class="surface table-panel mt-5"><div class="panel-head"><div><div class="section-kicker">HISTORIAL LOCAL</div><h2>Ejecuciones anteriores</h2></div></div><div class="table-scroll"><table class="data-table"><thead><tr><th>ID</th><th>FECHA</th><th>ORIGEN</th><th>MÉTRICAS</th><th>ESTADO</th></tr></thead><tbody><tr v-for="r in runs.slice(0, 5)" :key="r.id"><td><strong>{{ r.id }}</strong></td><td>{{ dateTime(r.endedAt) }}</td><td>Fixture local</td><td>{{ r.results.length }} / 13</td><td><span class="status-pill success">Finalizada</span></td></tr></tbody></table></div></section></template>


    </div></v-main>

    <v-dialog v-model="accountDialog" max-width="610"><v-card rounded="xl" class="dialog-card"><div class="dialog-head"><div><div class="section-kicker">CONFIGURACIÓN DE ACCESO</div><h2>Agregar cuenta</h2></div><v-btn icon="mdi-close" variant="text" @click="accountDialog = false" /></div><p class="dialog-intro">Guarda los parámetros de conexión en este navegador. La verificación estará disponible cuando se integre el backend.</p><v-form @submit.prevent="saveAccount"><div class="dialog-fields"><v-text-field v-model="accountForm.name" label="Nombre de la cuenta" variant="outlined" density="comfortable" /><v-text-field v-model="accountForm.id" label="ID de cuenta (12 dígitos)" variant="outlined" density="comfortable" /><v-text-field v-model="accountForm.roleArn" label="ARN del rol de lectura" variant="outlined" density="comfortable" /><v-text-field v-model="accountForm.externalId" label="ID externo (si corresponde)" variant="outlined" density="comfortable" /><v-select v-model="accountForm.region" :items="['us-east-1','us-east-2','us-west-2','sa-east-1','eu-west-1']" label="Región inicial" variant="outlined" density="comfortable" /></div><div class="dialog-actions"><v-btn variant="text" @click="accountDialog = false">Cancelar</v-btn><v-btn type="submit" color="primary">Guardar configuración</v-btn></div></v-form></v-card></v-dialog>

    <v-snackbar :model-value="!!notice" @update:model-value="value => { if (!value) notice = '' }" :timeout="5000" color="#172b48">{{ notice }}<template #actions><v-btn variant="text" @click="notice = ''">Cerrar</v-btn></template></v-snackbar>
  </v-app>
</template>
