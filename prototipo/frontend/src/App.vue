<script setup>
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import metrics from './data/metrics.json'
import { assets, databases, dataZoneAssets, populationFor } from './data/fixtures.js'
import DatabaseMap from './components/DatabaseMap.vue'
import GlueEvidence from './components/GlueEvidence.vue'
import MetricDetail from './components/MetricDetail.vue'

const sections = [
  { id: 'inicio', label: 'Inicio', icon: 'mdi-view-dashboard-outline' },
  { id: 'cuentas', label: 'Cuentas AWS', icon: 'mdi-cloud-outline' },
  { id: 'inventario', label: 'Inventario', icon: 'mdi-database-outline' },
  { id: 'mediciones', label: 'Mediciones', icon: 'mdi-chart-box-outline' },
  { id: 'ejecuciones', label: 'Ejecuciones', icon: 'mdi-progress-check' },
]
const icons = { Responsabilidad: 'mdi-account-key-outline', Visibilidad: 'mdi-eye-outline', Calidad: 'mdi-check-decagram-outline', 'Acceso y seguridad': 'mdi-shield-lock-outline', 'Cumplimiento y privacidad': 'mdi-file-lock-outline' }
const colors = { Responsabilidad: '#6674f4', Visibilidad: '#0ca7bd', Calidad: '#18a781', 'Acceso y seguridad': '#e6a13c', 'Cumplimiento y privacidad': '#aa74d8' }
const pillars = [...new Set(metrics.map(m => m.pillar))]
const defaultAccounts = [{ id: '111122223333', name: 'Cuenta de demostración', region: 'us-east-1', roleArn: '', mode: 'simulada', status: 'Demo local' }]
const fixtureVersion = 3
const appBase = import.meta.env.BASE_URL
function metricFromPath() {
  const path = window.location.pathname
  return path.startsWith(appBase) ? path.slice(appBase.length).match(/^metricas\/(M-\d{2})\/?$/)?.[1] || '' : ''
}
function readStorage(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback } catch { return fallback } }
function recordsFor(metric) {
  return populationFor(metric).map(row => {
    const evidenceRef = metric.id === 'M-09' && !row.inNumerator ? null : `${metric.id}-${row.id}-SIM`
    return { ...row, evidenceRef }
  })
}
function refreshDemoRun(run) {
  if (run.fixtureVersion === fixtureVersion || !run.id?.startsWith('SIM-')) return run
  const results = run.results.map(result => {
    const metric = metrics.find(item => item.id === result.metricId)
    return metric ? { ...result, records: recordsFor(metric) } : result
  })
  return { ...run, fixtureVersion, results }
}
const accounts = ref(readStorage('dl.accounts', defaultAccounts))
const active = ref('inicio')
const drawer = ref(true)
const search = ref('')
const pillarFilter = ref('Todos')
const serviceFilter = ref('Todos')
const inventoryView = ref('mapa')
const metricId = ref(metricFromPath())
const returnSection = ref('mediciones')
const selectedMetric = computed(() => metrics.find(m => m.id === metricId.value) || null)
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
const filteredMetrics = computed(() => metrics.filter(m => (pillarFilter.value === 'Todos' || m.pillar === pillarFilter.value) && `${m.id} ${m.name} ${m.dimension} ${m.pillar}`.toLowerCase().includes(search.value.toLowerCase())))
const filteredAssets = computed(() => assets.filter(a => (serviceFilter.value === 'Todos' || a.service === serviceFilter.value) && `${a.title} ${a.name} ${a.kind} ${a.owner} ${a.id}`.toLowerCase().includes(search.value.toLowerCase())))
const services = [...new Set(assets.map(a => a.service))]
const resultMap = computed(() => Object.fromEntries((lastRun.value?.results || []).map(r => [r.metricId, r])))
const selectedResult = computed(() => selectedMetric.value ? resultMap.value[selectedMetric.value.id] : null)
const progress = computed(() => currentRun.value ? Math.round(currentRun.value.done / metrics.length * 100) : 0)
const overviewBars = computed(() => pillars.map(p => ({ pillar: p, count: metrics.filter(m => m.pillar === p).length, done: (lastRun.value?.results || []).filter(r => metrics.find(m => m.id === r.metricId)?.pillar === p).length, color: colors[p] })))
const pageTitles = { inicio: ['Centro de control', 'Visión general del piloto técnico'], cuentas: ['Cuentas AWS', 'Acceso entre cuentas y regiones'], inventario: ['Inventario', 'Recursos del piloto y validación de descubrimiento'], mediciones: ['Mediciones', '13 métricas técnicas en cinco pilares'], ejecuciones: ['Ejecuciones', 'Seguimiento de las consultas y cálculos'] }
const inventoryViews = [
  { id: 'mapa', label: 'Mapa de bases', icon: 'mdi-sitemap-outline' },
  { id: 'lista', label: 'Lista de recursos', icon: 'mdi-format-list-bulleted' },
  { id: 'postman', label: 'Validación Postman', icon: 'mdi-clipboard-check-outline' },
]
const metricReturnLabel = computed(() => sections.find(section => section.id === returnSection.value).label)
function navigate(id) { active.value = id; search.value = ''; pillarFilter.value = 'Todos'; serviceFilter.value = 'Todos'; if (window.innerWidth < 960) drawer.value = false }
function showPostmanEvidence() { inventoryView.value = 'postman'; navigate('inventario') }
function openMetric(metric) { const id = typeof metric === 'string' ? metric : metric.id; if (!metrics.some(m => m.id === id)) return; if (!selectedMetric.value) returnSection.value = active.value; metricId.value = id; window.history.pushState({}, '', `${appBase}metricas/${id}/`); window.scrollTo(0, 0) }
function closeMetric() { metricId.value = ''; active.value = returnSection.value; window.history.pushState({}, '', appBase); window.scrollTo(0, 0) }
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
  notice.value = 'Configuración guardada localmente. La verificación AWS requiere el backend.'
}
function makeResult(m) {
  return { metricId: m.id, value: m.den > 0 ? Number((m.num / m.den * 100).toFixed(1)) : m.num, num: m.num, den: m.den, unit: m.unit, status: 'Calculada', source: 'Fixture local', coverage: m.id === 'M-09' ? 'Parcial: flujo piloto' : 'Escenario de prueba', evidence: m.operations.map((op, i) => `${m.id}-SIM-${String(i + 1).padStart(2, '0')}`), records: recordsFor(m) }
}
function startSimulation() {
  if (currentRun.value) return
  active.value = 'ejecuciones'
  currentRun.value = { id: `SIM-${Date.now().toString().slice(-8)}`, fixtureVersion, startedAt: new Date().toISOString(), endedAt: null, origin: 'Fixture local · sin llamadas AWS', accountId: account.value?.id || 'sin cuenta', region: account.value?.region || 'us-east-1', status: 'En curso', done: 0, results: [], events: ['Iniciando lote de medición simulado…'] }
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
      notice.value = 'Simulación finalizada: 13 resultados de ejemplo. No se consultó AWS.'
    }
  }, 240)
}
function downloadResults() {
  if (!lastRun.value) return
  const payload = { warning: 'DATOS SIMULADOS. No son resultados observados en AWS.', run: lastRun.value, metrics: metrics.map(m => ({ id: m.id, name: m.name, pillar: m.pillar, dimension: m.dimension, result: { ...resultFor(m), records: resultFor(m)?.records || recordsFor(m) } })) }
  const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }))
  const link = document.createElement('a'); link.href = url; link.download = `data-lens-${lastRun.value.id}.json`; link.click(); URL.revokeObjectURL(url)
}
function dateTime(value) { return value ? new Intl.DateTimeFormat('es-CL', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(value)) : '—' }
</script>

<template>
  <v-app>
    <v-navigation-drawer v-if="!selectedMetric" v-model="drawer" :permanent="$vuetify.display.mdAndUp" :temporary="$vuetify.display.smAndDown" width="252" class="side-nav" theme="dark">
      <div class="brand-wrap"><div class="brand-icon"><v-icon icon="mdi-chart-arc" size="23" /></div><div><div class="brand-name">data lens<span>.</span></div><div class="brand-sub">AWS DATA INTELLIGENCE</div></div></div>
      <div class="nav-caption">ESPACIO DE TRABAJO</div>
      <v-list nav density="comfortable" class="nav-list">
        <v-list-item v-for="item in sections" :key="item.id" :active="active === item.id" :prepend-icon="item.icon" :title="item.label" rounded="lg" @click="navigate(item.id)" />
      </v-list>
      <template #append><div class="nav-bottom"><div class="nav-system"><span class="pulse-dot" /> MODO DEMOSTRACIÓN</div><p>Simulación local. La prueba externa de Glue está en Inventario.</p><div class="nav-version">PILOTO 13 · V0.1</div></div></template>
    </v-navigation-drawer>

    <v-app-bar flat height="72" class="top-bar"><v-app-bar-nav-icon v-if="!selectedMetric && $vuetify.display.smAndDown" @click="drawer = !drawer" /><div class="top-context"><span class="top-breadcrumb">DATA LENS</span><v-icon icon="mdi-chevron-right" size="16" color="#a1aabc" /><span>{{ selectedMetric ? `${selectedMetric.id} · ${selectedMetric.dimension}` : pageTitles[active][0] }}</span></div><v-spacer /><div class="top-account"><v-icon icon="mdi-cloud-outline" size="17" /><span>{{ account?.name || 'Sin cuenta' }}</span><v-icon icon="mdi-chevron-down" size="15" /></div><div class="top-avatar">DL</div></v-app-bar>

    <v-main class="main-area"><MetricDetail v-if="selectedMetric" :key="selectedMetric.id" :metric="selectedMetric" :metrics="metrics" :result="selectedResult" :result-map="resultMap" :run="lastRun" :return-label="metricReturnLabel" @select="openMetric" @back="closeMetric" /><div v-else class="page-wrap">
      <div class="demo-banner"><v-icon icon="mdi-information-outline" size="19" /><div><strong>Entorno de demostración</strong><span> Inventario de ejemplo y mediciones simuladas. Las respuestas compartidas desde Postman están separadas en Inventario.</span></div></div>
      <div class="page-heading"><div><div class="eyebrow">PILOTO TÉCNICO / 13 DIMENSIONES</div><h1>{{ pageTitles[active][0] }}</h1><p>{{ pageTitles[active][1] }}</p></div><div class="heading-actions"><v-btn v-if="active === 'cuentas'" color="primary" prepend-icon="mdi-plus" rounded="lg" @click="accountDialog = true">Agregar cuenta</v-btn><v-btn v-else-if="active === 'mediciones' && lastRun" variant="outlined" prepend-icon="mdi-download-outline" rounded="lg" @click="downloadResults">Exportar JSON</v-btn><v-btn v-else-if="active !== 'ejecuciones'" color="primary" prepend-icon="mdi-play" rounded="lg" :disabled="!!currentRun" @click="startSimulation">Simular medición</v-btn></div></div>

      <template v-if="active === 'inicio'">
        <div class="kpi-grid">
          <div class="kpi-card"><div class="kpi-top"><span>CUENTAS CONFIGURADAS</span><div class="kpi-icon blue"><v-icon icon="mdi-cloud-check-outline" /></div></div><div class="kpi-value">{{ accounts.length.toString().padStart(2, '0') }}</div><div class="kpi-foot"><span class="mini-dot amber" /> Sin acceso AWS verificado</div></div>
          <div class="kpi-card"><div class="kpi-top"><span>MÉTRICAS PILOTO</span><div class="kpi-icon violet"><v-icon icon="mdi-chart-box-outline" /></div></div><div class="kpi-value">13<span class="kpi-suffix">/ 13 dimensiones</span></div><div class="kpi-foot">Distribuidas en 5 pilares</div></div>
          <div class="kpi-card"><div class="kpi-top"><span>RESULTADOS DISPONIBLES</span><div class="kpi-icon mint"><v-icon icon="mdi-check-circle-outline" /></div></div><div class="kpi-value">{{ completedCount.toString().padStart(2, '0') }}</div><div class="kpi-foot">{{ lastRun ? 'Solo datos simulados' : 'Ejecuta una simulación para explorar' }}</div></div>
          <div class="kpi-card"><div class="kpi-top"><span>ÚLTIMA EJECUCIÓN</span><div class="kpi-icon amber-icon"><v-icon icon="mdi-clock-outline" /></div></div><div class="kpi-value kpi-date">{{ lastRun ? dateTime(lastRun.endedAt).split(',')[0] : '—' }}</div><div class="kpi-foot">{{ lastRun ? lastRun.id : 'Sin ejecuciones' }}</div></div>
        </div>
        <section class="surface demo-evidence-link" aria-label="Prueba externa del piloto">
          <span class="kpi-icon mint"><v-icon icon="mdi-clipboard-check-outline" /></span>
          <div><div class="section-kicker">VALIDACIÓN TÉCNICA · POSTMAN</div><h2>Descubrimiento en AWS Glue</h2><p>Dos respuestas del laboratorio para el recorrido base → tablas.</p></div>
          <v-btn color="primary" variant="tonal" rounded="lg" append-icon="mdi-arrow-right" @click="showPostmanEvidence">Ver respuestas</v-btn>
        </section>
        <div class="overview-grid">
          <section class="surface panel-large"><div class="panel-head"><div><div class="section-kicker">COBERTURA DEL PILOTO</div><h2>Mediciones por pilar</h2></div><v-btn variant="text" color="primary" append-icon="mdi-arrow-right" @click="navigate('mediciones')">Ver catálogo</v-btn></div><p class="panel-desc">Una métrica seleccionada para cada dimensión. El avance aparece al ejecutar el lote de demostración.</p><div class="pillar-rows"><div v-for="bar in overviewBars" :key="bar.pillar" class="pillar-row"><div class="pillar-symbol" :style="{background: bar.color + '1c', color: bar.color}"><v-icon :icon="icons[bar.pillar]" size="20" /></div><div class="pillar-info"><div class="pillar-label"><strong>{{ bar.pillar }}</strong><span>{{ bar.done }} / {{ bar.count }}</span></div><div class="track"><div class="fill" :style="{width: `${bar.done / bar.count * 100}%`, background: bar.color}" /></div></div></div></div></section>
          <section class="surface workflow-panel"><div class="section-kicker">FLUJO DE MEDICIÓN</div><h2>De la cuenta al resultado</h2><p class="panel-desc">Recorrido operativo del producto.</p><div class="flow-steps"><div v-for="(step, i) in [{icon:'mdi-cloud-outline',name:'Conectar cuenta',body:'Rol de lectura y regiones'},{icon:'mdi-database-search-outline',name:'Descubrir activos',body:'Inventario por servicio'},{icon:'mdi-play-circle-outline',name:'Ejecutar mediciones',body:'13 cálculos trazables'},{icon:'mdi-chart-line',name:'Revisar resultados',body:'Valor, cobertura y evidencia'}]" :key="step.name" class="flow-step"><span class="step-number">{{ String(i + 1).padStart(2, '0') }}</span><span class="flow-icon"><v-icon :icon="step.icon" size="20" /></span><div><strong>{{ step.name }}</strong><small>{{ step.body }}</small></div></div></div><v-btn block color="primary" variant="tonal" rounded="lg" class="mt-5" @click="navigate('cuentas')">Explorar conexiones <v-icon end icon="mdi-arrow-right" /></v-btn></section>
        </div>
        <section class="surface table-panel"><div class="panel-head"><div><div class="section-kicker">EXPLORAR</div><h2>Métricas destacadas</h2></div><v-btn variant="text" color="primary" append-icon="mdi-arrow-right" @click="navigate('mediciones')">Ver las 13</v-btn></div><div class="table-scroll"><table class="data-table"><thead><tr><th>MÉTRICA</th><th>PILAR / DIMENSIÓN</th><th>OPERACIONES AWS</th><th>ESTADO</th><th></th></tr></thead><tbody><tr v-for="m in metrics.filter(x => ['M-04','M-11','M-22','M-29'].includes(x.id))" :key="m.id" @click="openMetric(m)"><td><span class="metric-id">{{ m.id }}</span><strong>{{ m.name }}</strong></td><td>{{ m.pillar }} <span class="cell-muted">/ {{ m.dimension }}</span></td><td>{{ m.operations.length }} operaciones</td><td><span class="status-pill" :class="lastRun ? 'success' : 'muted'">{{ lastRun ? 'Simulada' : 'Pendiente' }}</span></td><td><v-icon icon="mdi-chevron-right" size="18" color="#99a7b8" /></td></tr></tbody></table></div></section>
      </template>

      <template v-else-if="active === 'cuentas'"><div class="two-col"><section class="surface table-panel"><div class="panel-head"><div><div class="section-kicker">ACCESO ENTRE CUENTAS</div><h2>Cuentas registradas</h2></div><span class="count-label">{{ accounts.length }} cuenta{{ accounts.length === 1 ? '' : 's' }}</span></div><div v-for="a in accounts" :key="a.id" class="account-row"><div class="account-logo"><v-icon icon="mdi-aws" size="26" /></div><div class="account-main"><strong>{{ a.name }}</strong><small>{{ a.id }} · {{ a.region }}</small><small v-if="a.roleArn" class="arn">{{ a.roleArn }}</small></div><span class="status-pill" :class="a.mode === 'simulada' ? 'amber-status' : 'muted'">{{ a.status }}</span></div><div class="inline-info"><v-icon icon="mdi-lock-outline" size="18" /><span>La app guarda solo la configuración local. La comprobación real requiere que FastAPI asuma el rol desde AWS.</span></div></section><section class="surface guide-panel"><div class="section-kicker">PREPARACIÓN TÉCNICA</div><h2>Cómo funcionará la conexión</h2><div class="guide-item"><span>01</span><div><strong>Rol de solo lectura</strong><p>La cuenta evaluada crea un rol IAM con permisos para las operaciones del piloto.</p></div></div><div class="guide-item"><span>02</span><div><strong>Confianza entre cuentas</strong><p>El backend de Data Lens asume el rol mediante AWS STS; el navegador no recibe credenciales.</p></div></div><div class="guide-item"><span>03</span><div><strong>Comprobación y medición</strong><p>La aplicación muestra acceso por servicio, recursos visibles y errores de permisos.</p></div></div><v-alert type="info" variant="tonal" density="compact" class="mt-5">La integración AWS todavía no está implementada.</v-alert></section></div></template>

      <template v-else-if="active === 'inventario'">
        <div class="inventory-toolbar">
          <div><strong>Explorar el inventario</strong><span>Mapa, recursos y respuestas de descubrimiento</span></div>
          <div class="inventory-switch" role="group" aria-label="Vista de inventario">
            <button v-for="view in inventoryViews" :key="view.id" type="button" :class="{ active: inventoryView === view.id }" :aria-pressed="inventoryView === view.id" @click="inventoryView = view.id">
              <v-icon :icon="view.icon" size="17" /> {{ view.label }}
            </button>
          </div>
        </div>
        <section v-if="inventoryView === 'mapa'" class="surface"><DatabaseMap :databases="databases" :assets="dataZoneAssets" /></section>
        <GlueEvidence v-else-if="inventoryView === 'postman'" />
        <section v-else class="surface table-panel">
          <div class="panel-head"><div><div class="section-kicker">RECURSOS DE EJEMPLO</div><h2>Inventario de activos</h2></div><span class="count-label">{{ filteredAssets.length }} recursos</span></div>
          <div class="filter-row"><v-text-field v-model="search" label="Buscar activo, ID o responsable" prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details class="search-field" /><v-select v-model="serviceFilter" :items="['Todos', ...services]" label="Servicio" variant="outlined" density="compact" hide-details class="filter-select" /></div>
          <div class="table-scroll">
            <table class="data-table">
              <thead><tr><th>ACTIVO</th><th>SERVICIO</th><th>TIPO</th><th>REGIÓN</th><th>RESPONSABLE</th><th>ESTADO</th><th>MEDICIÓN</th></tr></thead>
              <tbody>
                <tr v-for="a in filteredAssets" :key="a.id">
                  <td><strong>{{ a.title }}</strong><small class="table-sub" :title="a.id">{{ a.name }}</small></td><td>{{ a.service }}</td><td>{{ a.kind }}</td><td>{{ a.region }}</td><td>{{ a.owner || 'Sin responsable' }}</td><td><span class="status-pill muted">Simulado</span></td>
                  <td><v-btn v-if="a.service === 'Glue' && a.kind === 'Job'" size="small" variant="tonal" color="primary" append-icon="mdi-arrow-top-right" @click="openMetric('M-16')">Ver M-16</v-btn><span v-else class="cell-muted">—</span></td>
                </tr>
              </tbody>
            </table>
            <div v-if="!filteredAssets.length" class="empty-row">No hay activos que coincidan con el filtro.</div>
          </div>
        </section>
      </template>

      <template v-else-if="active === 'mediciones'">
        <div v-if="lastRun" class="measurement-summary"><div><strong>13 / 13</strong><span>Métricas simuladas</span></div><div><strong>5 pilares</strong><span>Universo piloto</span></div><div><strong>{{ lastRun.id }}</strong><span>{{ dateTime(lastRun.endedAt) }}</span></div><span class="status-pill amber-status">Sin consultar AWS</span></div>
        <section class="surface table-panel"><div class="panel-head"><div><div class="section-kicker">CATÁLOGO TÉCNICO</div><h2>13 métricas · 14 tipos de operación</h2></div><span class="count-label">{{ filteredMetrics.length }} visibles</span></div><div class="filter-row"><v-text-field v-model="search" label="Buscar métrica o dimensión" prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details class="search-field" /><v-select v-model="pillarFilter" :items="['Todos', ...pillars]" label="Pilar" variant="outlined" density="compact" hide-details class="filter-select" /></div><div class="table-scroll"><table class="data-table"><thead><tr><th>ID / MÉTRICA</th><th>PILAR</th><th>DIMENSIÓN</th><th>OPERACIONES PREVISTAS</th><th>RESULTADO</th><th></th></tr></thead><tbody><tr v-for="m in filteredMetrics" :key="m.id" class="clickable" @click="openMetric(m)"><td><span class="metric-id">{{ m.id }}</span><strong>{{ m.name }}</strong></td><td><span class="pillar-chip" :style="{ color: colors[m.pillar], background: colors[m.pillar] + '16' }"><v-icon :icon="icons[m.pillar]" size="15" />{{ m.pillar }}</span></td><td>{{ m.dimension }}</td><td class="ops-cell">{{ m.operations.map(o => o.name).join(' · ') }}</td><td><span :class="lastRun ? 'result-text' : 'cell-muted'">{{ formatValue(m) }}</span></td><td><v-icon icon="mdi-arrow-top-right" size="18" color="#99a7b8" /></td></tr></tbody></table><div v-if="!filteredMetrics.length" class="empty-row">No hay métricas que coincidan con el filtro.</div></div></section>
      </template>

      <template v-else-if="active === 'ejecuciones'"><div class="two-col execution-layout"><section class="surface execution-main"><div class="section-kicker">MOTOR DE MEDICIÓN</div><h2>Ejecutar lote de 13 métricas</h2><p class="panel-desc">El modo local procesa respuestas de ejemplo. El flujo de consulta AWS se habilitará al integrar backend y permisos.</p><div class="run-console"><div class="console-top"><div><span class="console-signal" :class="currentRun ? 'running' : ''" />{{ currentRun ? 'EJECUCIÓN EN CURSO' : lastRun ? 'ÚLTIMA EJECUCIÓN' : 'LISTO PARA SIMULAR' }}</div><span>{{ displayedRun?.id || '—' }}</span></div><div class="console-content"><div class="console-stat"><span>Origen de datos</span><strong>Fixture local</strong></div><div class="console-stat"><span>Métricas procesadas</span><strong>{{ currentRun?.done ?? lastRun?.results.length ?? 0 }} / 13</strong></div><div class="console-stat"><span>Cuenta</span><strong>{{ account?.id || '—' }}</strong></div><div class="console-stat"><span>Estado</span><strong>{{ currentRun ? 'En curso' : lastRun ? 'Finalizada' : 'Pendiente' }}</strong></div></div><div v-if="currentRun" class="progress-wrap"><div class="progress-label"><span>Procesando datos simulados</span><strong>{{ progress }} %</strong></div><v-progress-linear :model-value="progress" color="primary" height="8" rounded /></div></div><div class="run-actions"><v-btn color="primary" prepend-icon="mdi-play" rounded="lg" :loading="!!currentRun" @click="startSimulation">{{ lastRun ? 'Repetir simulación' : 'Iniciar simulación' }}</v-btn><v-btn v-if="lastRun" variant="outlined" rounded="lg" prepend-icon="mdi-chart-line" @click="navigate('mediciones')">Ver métricas</v-btn></div><v-alert type="warning" variant="tonal" density="compact" class="mt-6">Esta acción no hace peticiones a AWS y no valida accesos.</v-alert></section><section class="surface events-panel"><div class="section-kicker">ACTIVIDAD</div><h2>Registro de ejecución</h2><div v-if="displayedRun" class="events-list"><div v-for="(event, i) in displayedRun.events.slice(0, 14)" :key="i" class="event-item"><span class="event-dot" /><span>{{ event }}</span></div></div><div v-else class="empty-events"><v-icon icon="mdi-text-box-search-outline" size="38" /><p>Aquí aparecerán los eventos de la simulación.</p></div></section></div><section v-if="runs.length" class="surface table-panel mt-5"><div class="panel-head"><div><div class="section-kicker">HISTORIAL LOCAL</div><h2>Ejecuciones anteriores</h2></div></div><div class="table-scroll"><table class="data-table"><thead><tr><th>ID</th><th>FECHA</th><th>ORIGEN</th><th>MÉTRICAS</th><th>ESTADO</th></tr></thead><tbody><tr v-for="r in runs.slice(0, 5)" :key="r.id"><td><strong>{{ r.id }}</strong></td><td>{{ dateTime(r.endedAt) }}</td><td>Fixture local</td><td>{{ r.results.length }} / 13</td><td><span class="status-pill success">Finalizada</span></td></tr></tbody></table></div></section></template>


    </div></v-main>

    <v-dialog v-model="accountDialog" max-width="610"><v-card rounded="xl" class="dialog-card"><div class="dialog-head"><div><div class="section-kicker">CONEXIÓN ENTRE CUENTAS</div><h2>Agregar cuenta AWS</h2></div><v-btn icon="mdi-close" variant="text" @click="accountDialog = false" /></div><p class="dialog-intro">Guarda los parámetros de conexión. La verificación del rol estará disponible al integrar el backend AWS.</p><v-form @submit.prevent="saveAccount"><div class="dialog-fields"><v-text-field v-model="accountForm.name" label="Nombre de la cuenta" variant="outlined" density="comfortable" /><v-text-field v-model="accountForm.id" label="ID de cuenta (12 dígitos)" variant="outlined" density="comfortable" /><v-text-field v-model="accountForm.roleArn" label="ARN del rol de lectura" variant="outlined" density="comfortable" placeholder="arn:aws:iam::123456789012:role/DataLensReadOnly" /><v-text-field v-model="accountForm.externalId" label="External ID (si corresponde)" variant="outlined" density="comfortable" /><v-select v-model="accountForm.region" :items="['us-east-1','us-east-2','us-west-2','sa-east-1','eu-west-1']" label="Región inicial" variant="outlined" density="comfortable" /></div><div class="dialog-actions"><v-btn variant="text" @click="accountDialog = false">Cancelar</v-btn><v-btn type="submit" color="primary">Guardar configuración</v-btn></div></v-form></v-card></v-dialog>

    <v-snackbar :model-value="!!notice" @update:model-value="value => { if (!value) notice = '' }" :timeout="5000" color="#172b48">{{ notice }}<template #actions><v-btn variant="text" @click="notice = ''">Cerrar</v-btn></template></v-snackbar>
  </v-app>
</template>
