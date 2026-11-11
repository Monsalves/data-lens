<script setup>
import { computed, ref, watch } from 'vue'
import { glueDemoJob, lineageEdges, lineageNodes, populationFor, statusOptionsFor } from '../data/fixtures.js'
import LineageGraph from './LineageGraph.vue'

const props = defineProps({
  metric: { type: Object, required: true },
  metrics: { type: Array, required: true },
  result: { type: Object, default: null },
  displayValue: { type: String, required: true },
  run: { type: Object, default: null },
  returnLabel: { type: String, required: true },
})
const emit = defineEmits(['select', 'back'])
const statusFilter = ref('Todos')
const grantFilter = ref('Todos')
const contributionFilter = ref('Todos')
const search = ref('')
const page = ref(1)
const selectedEdgeId = ref('')
const index = computed(() => props.metrics.findIndex(m => m.id === props.metric.id))
const previous = computed(() => props.metrics[index.value - 1] || null)
const next = computed(() => props.metrics[index.value + 1] || null)
const rows = computed(() => props.result?.records || populationFor(props.metric))
const options = computed(() => statusOptionsFor(rows.value))
const grantOptions = computed(() => props.metric.id === 'M-04' ? statusOptionsFor(rows.value, 'grantCode', 'grantLabel', 'grantTone') : [])
const filtered = computed(() => rows.value.filter(row =>
  (contributionFilter.value === 'Todos' || row.inNumerator) &&
  (statusFilter.value === 'Todos' || row.statusCode === statusFilter.value) &&
  (grantFilter.value === 'Todos' || row.grantCode === grantFilter.value) &&
  `${row.id} ${row.name} ${row.detail} ${row.statusLabel} ${row.grantLabel || ''}`.toLowerCase().includes(search.value.toLowerCase()),
))
const pages = computed(() => Math.max(1, Math.ceil(filtered.value.length / 25)))
const visibleRows = computed(() => filtered.value.slice((page.value - 1) * 25, page.value * 25))
watch([statusFilter, grantFilter, contributionFilter, search], () => { page.value = 1 })
watch(() => props.metric.id, () => { statusFilter.value = 'Todos'; grantFilter.value = 'Todos'; contributionFilter.value = 'Todos'; search.value = ''; page.value = 1; selectedEdgeId.value = '' })

function onEdgeSelected(id) {
  selectedEdgeId.value = id
  statusFilter.value = 'Todos'
  contributionFilter.value = 'Todos'
  search.value = id
}
function inspectContribution(kind) {
  contributionFilter.value = kind
  statusFilter.value = 'Todos'
  grantFilter.value = 'Todos'
  search.value = ''
  selectedEdgeId.value = ''
  document.getElementById('metric-records')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
function iconFor(tone) {
  return { success: 'mdi-check-circle-outline', error: 'mdi-alert-circle-outline', warning: 'mdi-clock-alert-outline', info: 'mdi-information-outline', neutral: 'mdi-minus-circle-outline' }[tone] || 'mdi-information-outline'
}
function displayReference(reference) {
  return reference.replace(/^M-\d{2}-/u, '')
}
function recordRef(row) {
  return props.result ? displayReference(row.evidenceRef || `${row.id}-SIM`) : 'Sin ejecución'
}
function formattedDate(value) { return value ? new Intl.DateTimeFormat('es-CL', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(value)) : '—' }
</script>

<template>
  <div class="metric-full-main">
    <div class="metric-mobile-select"><v-select :model-value="metric.id" :items="metrics.map(m => ({ title: m.name, value: m.id }))" item-title="title" item-value="value" label="Ir a otra métrica" variant="outlined" density="compact" hide-details @update:model-value="id => emit('select', id)" /></div>
    <div class="metric-full-top"><button type="button" @click="emit('back')"><v-icon icon="mdi-arrow-left" size="17" /> {{ returnLabel }}</button><span>{{ metric.pillar }} <v-icon icon="mdi-chevron-right" size="15" /> {{ metric.dimension }}</span><div class="metric-nav-arrows"><button type="button" :disabled="!previous" :title="previous ? `Anterior: ${previous.name}` : 'Primera métrica'" @click="previous && emit('select', previous.id)"><v-icon icon="mdi-arrow-left" size="18" /></button><button type="button" :disabled="!next" :title="next ? `Siguiente: ${next.name}` : 'Última métrica'" @click="next && emit('select', next.id)"><v-icon icon="mdi-arrow-right" size="18" /></button></div></div>
    <div class="metric-full-banner"><v-icon icon="mdi-flask-outline" size="18" /><span>Escenario de demostración. Los elementos, estados y evidencias de esta página son sintéticos.</span></div>
    <header class="metric-full-header"><div><span class="metric-full-context">{{ metric.pillar }} / {{ metric.dimension }}</span><h1>{{ metric.name }}</h1><p>{{ result ? `Ejecución ${run?.id || 'local'} · ${formattedDate(run?.endedAt)}` : 'Aún no hay ejecución; se muestra el universo ilustrativo.' }}</p></div><span class="metric-run-state" :class="result ? 'ready' : 'pending'">{{ result ? 'Calculada' : 'Pendiente' }}</span></header>
    <v-alert v-if="metric.id === 'M-09'" type="info" variant="tonal" density="compact" class="mb-4">Aquí se ilustran ocho conexiones registradas. Con una fuente conectada, Data Lens podrá leerlas automáticamente. Este conteo no mide la completitud del linaje.</v-alert>
    <div class="metric-full-grid"><section class="metric-full-card result-card"><div class="metric-card-label">RESULTADO</div><div class="metric-full-value">{{ displayValue }}</div><div class="metric-full-formula">{{ metric.formula }}</div><div class="metric-counts"><button type="button" @click="inspectContribution('Numerador')"><small>{{ metric.kind === 'count' ? 'CONTEO' : 'NUMERADOR' }} <v-icon icon="mdi-arrow-down-right" size="13" /></small><strong>{{ metric.num_desc || metric.num }}</strong></button><button v-if="metric.den > 0" type="button" @click="inspectContribution('Todos')"><small>DENOMINADOR <v-icon icon="mdi-arrow-down-right" size="13" /></small><strong>{{ metric.den_desc || metric.den }}</strong></button></div></section><section class="metric-full-card context-card"><div class="metric-card-label">CONTEXTO DE MEDICIÓN</div><div class="metric-context-row"><span>Universo</span><strong>{{ rows.length }} elementos de ejemplo</strong></div><div class="metric-context-row"><span>Parámetros</span><strong>{{ metric.reference }}</strong></div><div class="metric-context-row"><span>Origen</span><strong>Fixture local · sin consultas externas</strong></div><div class="metric-context-row"><span>Operaciones</span><strong>{{ metric.operations.length }} previstas</strong></div><div class="metric-context-row"><span>Alcance</span><strong>{{ metric.scope_note }}</strong></div></section></div>

    <section v-if="metric.id === 'M-16'" class="metric-full-card">
      <div class="metric-card-label">PROCESO DE EJEMPLO · GLUE</div>
      <div class="metric-context-row"><span>Job del inventario</span><strong>{{ glueDemoJob.title }} · {{ glueDemoJob.name }}</strong></div>
      <p class="panel-desc">En la integración prevista, <code>ListJobs</code> llena el inventario y <code>GetJobRuns</code> consulta el historial del job seleccionado.</p>
    </section>
    <section v-if="metric.id === 'M-04' && result" class="metric-full-card metric-grants"><div class="metric-card-label">SOLICITUDES Y CONCESIONES</div><div class="grant-breakdown"><div><strong>{{ metric.states.requests.ACCEPTED }}</strong><span>Aprobadas</span></div><div><strong>{{ metric.states.requests.REJECTED }}</strong><span>Rechazadas</span></div><div><strong>{{ metric.states.requests.PENDING }}</strong><span>Pendientes</span></div><div><strong>{{ metric.states.grants.ACTIVE }}</strong><span>Grants activos</span></div><div><strong>{{ metric.states.grants.FAILED }}</strong><span>Grants fallidos</span></div></div></section>
    <section v-if="metric.id === 'M-09'" class="metric-full-card metric-graph"><div class="metric-section-head"><div><div class="metric-card-label">CONEXIONES DEL EJEMPLO</div><h2>Grafo de linaje registrado</h2></div><span>{{ metric.num }} conexiones registradas</span></div><LineageGraph :nodes="lineageNodes" :edges="lineageEdges" :selected-edge-id="selectedEdgeId" @select="onEdgeSelected" /></section>

    <section id="metric-records" class="metric-full-card metric-population"><div class="metric-section-head"><div><div class="metric-card-label">TRAZABILIDAD DEL CÁLCULO</div><h2>Elementos revisados</h2><p>Filtra por la condición mostrada. El resultado agregado conserva el universo completo.</p></div><span>{{ filtered.length }} de {{ rows.length }} visibles</span></div>
      <div v-if="contributionFilter === 'Numerador'" class="contribution-note">Mostrando elementos que integran el numerador. <button type="button" @click="contributionFilter = 'Todos'">Ver universo completo</button></div>
      <div class="metric-filter-bar"><div class="metric-status-filters"><button type="button" class="status-filter" :class="{ active: statusFilter === 'Todos' }" :aria-pressed="statusFilter === 'Todos'" @click="statusFilter = 'Todos'; contributionFilter = 'Todos'; selectedEdgeId = ''">Todos <b>{{ rows.length }}</b></button><button v-for="option in options" :key="option.code" type="button" class="status-filter" :class="[`tone-${option.tone}`, { active: statusFilter === option.code }]" :aria-pressed="statusFilter === option.code" @click="statusFilter = option.code; contributionFilter = 'Todos'; selectedEdgeId = ''"><v-icon :icon="iconFor(option.tone)" size="15" />{{ option.label }} <b>{{ option.count }}</b></button></div><v-text-field v-model="search" label="Buscar ID o elemento" prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details class="metric-record-search" /></div>
      <div v-if="metric.id === 'M-04'" class="metric-grant-filters"><span>Estado del grant</span><button type="button" :class="{ active: grantFilter === 'Todos' }" @click="grantFilter = 'Todos'">Todos</button><button v-for="option in grantOptions" :key="option.code" type="button" :class="[`tone-${option.tone}`, { active: grantFilter === option.code }]" @click="grantFilter = option.code">{{ option.label }} ({{ option.count }})</button></div>
      <div class="metric-record-scroll"><table class="metric-record-table"><thead><tr><th>ID / ELEMENTO</th><th>DETALLE</th><th>{{ metric.id === 'M-04' ? 'SOLICITUD' : 'ESTADO' }}</th><th v-if="metric.id === 'M-04'">GRANT</th><th v-if="metric.id === 'M-18'">EVALUACIÓN</th><th>REFERENCIA</th></tr></thead><tbody><tr v-for="row in visibleRows" :key="row.id" :class="{ 'focused-row': selectedEdgeId === row.id }"><td><strong>{{ row.id }}</strong><small>{{ row.name }}</small></td><td>{{ row.detail }}</td><td><span class="record-status" :class="`tone-${row.tone}`"><v-icon :icon="iconFor(row.tone)" size="15" />{{ row.statusLabel }}</span></td><td v-if="metric.id === 'M-04'"><span class="record-status" :class="`tone-${row.grantTone}`"><v-icon :icon="iconFor(row.grantTone)" size="15" />{{ row.grantLabel }}</span></td><td v-if="metric.id === 'M-18'"><span v-if="row.checkOutcome" class="record-status" :class="row.checkOutcome === 'Aprobado' ? 'tone-success' : 'tone-error'">{{ row.checkOutcome }}</span><span v-else>—</span></td><td class="record-ref">{{ recordRef(row) }}</td></tr></tbody></table><div v-if="!visibleRows.length" class="metric-empty">No hay elementos con estos filtros.</div></div><div v-if="pages > 1" class="metric-record-pager"><span>Página {{ page }} de {{ pages }}</span><div><v-btn icon="mdi-chevron-left" variant="text" size="small" :disabled="page === 1" @click="page--" /><v-btn icon="mdi-chevron-right" variant="text" size="small" :disabled="page === pages" @click="page++" /></div></div>
    </section>

    <section class="metric-full-card metric-operations"><div class="metric-card-label">FUENTES TÉCNICAS</div><h2>Operaciones previstas</h2><div class="metric-op-grid"><div v-for="op in metric.operations" :key="op.name" class="operation-card"><div><span class="method-badge">{{ op.method }}</span><strong>{{ op.name }}</strong></div><small>Servicio del ejemplo: {{ op.service.replace(/^AWS /u, '') }}</small><small>Campos esperados: {{ op.fields.join(', ') }}</small><a :href="op.docs" target="_blank" rel="noopener noreferrer">Documentación técnica <v-icon icon="mdi-open-in-new" size="13" /></a></div></div></section>
    <section class="metric-full-card metric-evidence"><div class="metric-card-label">EVIDENCIA DE LA EJECUCIÓN</div><h2>Referencias</h2><div v-if="result" class="metric-evidence-list"><div v-for="id in result.evidence" :key="id" class="evidence-row"><v-icon icon="mdi-file-code-outline" size="18" /><div><strong>{{ displayReference(id) }}</strong><small>Referencia sintética · fixture local</small></div></div></div><p v-else>Ejecuta la simulación para generar referencias de ejemplo.</p></section>
  </div>
</template>
