<script setup>
import { computed, nextTick, ref, watch } from 'vue'

const props = defineProps({
  groups: { type: Array, required: true },
  results: { type: Array, default: () => [] },
  database: Boolean,
})
defineEmits(['metric', 'lineage', 'asset'])

const selected = ref('')
const overview = ref(null)
const detailTitle = ref(null)
const status = ref('Todos')
const query = ref('')
const page = ref(1)
const pageSize = ref(10)
const group = computed(() => props.groups.find(item => item.metric.id === selected.value))
const statusOptions = computed(() => ['Todos', ...new Set(group.value?.records.map(row => row.statusLabel))])

function normalize(text) {
  return text.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase()
}

const filtered = computed(() => {
  const words = normalize(query.value || '').trim().split(/\s+/u).filter(Boolean)
  return (group.value?.records || []).filter(row => {
    if (status.value !== 'Todos' && row.statusLabel !== status.value) return false
    const text = normalize([row.id, row.name, row.detail, ...row.assets].join(' '))
    return words.every(word => text.includes(word))
  })
})
const first = computed(() => (page.value - 1) * pageSize.value)
const visible = computed(() => filtered.value.slice(first.value, first.value + pageSize.value))
const pages = computed(() => Math.max(1, Math.ceil(filtered.value.length / pageSize.value)))
const references = computed(() => new Map(
  props.results.find(result => result.metricId === selected.value)?.records?.map(row => [row.id, row.evidenceRef]),
))

watch([status, query, pageSize], () => { page.value = 1 })

async function openRecords(id) {
  status.value = 'Todos'
  query.value = ''
  page.value = 1
  selected.value = id
  await nextTick()
  detailTitle.value?.focus()
}

async function closeRecords() {
  const id = selected.value
  selected.value = ''
  await nextTick()
  overview.value?.querySelector(`[data-assessment="${id}"]`)?.focus()
}

const topics = {
  'M-01': { label: 'Responsabilidad', icon: 'mdi-account-check-outline', color: 'violet', unit: 'activos' },
  'M-04': { label: 'Solicitudes de acceso', icon: 'mdi-key-outline', color: 'blue', unit: 'solicitudes' },
  'M-07': { label: 'Metadatos requeridos', icon: 'mdi-format-list-checks', color: 'teal', unit: 'campos' },
  'M-09': { label: 'Linaje', icon: 'mdi-source-branch', color: 'blue', unit: 'conexiones' },
  'M-11': { label: 'Completitud de datos', icon: 'mdi-table-search', color: 'teal', unit: 'filas' },
  'M-18': { label: 'Reglas de calidad', icon: 'mdi-check-decagram-outline', color: 'teal', unit: 'reglas' },
  'M-26': { label: 'Clasificación', icon: 'mdi-tag-outline', color: 'violet', unit: 'activos' },
}
const stateIcons = {
  success: 'mdi-check-circle-outline',
  error: 'mdi-alert-circle-outline',
  warning: 'mdi-alert-outline',
  declined: 'mdi-close-circle-outline',
  info: 'mdi-information-outline',
  neutral: 'mdi-minus-circle-outline',
}
const stateOrder = ['error', 'declined', 'warning', 'success', 'info', 'neutral']
const pluralStates = {
  aprobada: 'Aprobadas',
  rechazada: 'Rechazadas',
  pendiente: 'Pendientes',
  informado: 'Campos informados',
  faltante: 'Campos faltantes',
  registrado: 'Conexiones registradas',
  ausente: 'Valores ausentes',
  presente: 'Valores presentes',
  verificable: 'Resultados verificables',
  sin_resultado: 'Sin resultado verificable',
  informada: 'Con clasificación',
}

function tone(row) {
  return row.statusCode === 'rechazada' ? 'declined' : row.tone
}

function summary(group) {
  const counts = new Map()
  for (const row of group.records) {
    const item = counts.get(row.statusCode)
    if (item) item.count++
    else counts.set(row.statusCode, { code: row.statusCode, label: row.statusLabel, tone: tone(row), count: 1 })
  }
  return [...counts.values()].sort((a, b) => stateOrder.indexOf(a.tone) - stateOrder.indexOf(b.tone))
}

function owner(group) {
  return group.records[0].statusCode === 'con_responsable'
    ? group.records[0].detail.split(' · ').slice(1).join(' · ')
    : ''
}
</script>

<template>
  <div v-if="!groups.length" class="assessment-empty">
    <v-icon icon="mdi-clipboard-text-off-outline" size="24" />
    <div><strong>Sin evaluación asociada</strong><p>No hay registros para este alcance.</p></div>
  </div>
  <div v-else-if="!group" ref="overview" class="compact-assessments" :class="{ 'base-assessments': database }">
    <p class="assessment-caption">Registros sintéticos<span v-if="database"> de las tablas de esta base · Linaje compartido contado una sola vez</span></p>
    <div class="assessment-columns" aria-hidden="true">
      <span>Evaluación</span><span>Estados observados</span><span v-if="database">Alcance</span><span></span>
    </div>
    <article v-for="item in groups" :key="item.metric.id" class="assessment-row">
      <div class="assessment-identity">
        <span class="assessment-topic" :class="`topic-${topics[item.metric.id].color}`">
          <v-icon :icon="topics[item.metric.id].icon" size="20" />
        </span>
        <span><strong>{{ topics[item.metric.id].label }}</strong><small>{{ item.metric.id }}</small></span>
      </div>
      <div class="assessment-observed">
        <span v-for="state in summary(item)" :key="state.label" class="observation-status" :class="`observation-${state.tone}`">
          <v-icon :icon="stateIcons[state.tone]" size="15" />
          <b v-if="database || item.records.length > 1 || item.metric.id === 'M-04'">{{ state.count }}</b>
          {{ state.count > 1 ? pluralStates[state.code] || state.label : state.label }}
        </span>
        <span v-if="!database && item.metric.id === 'M-01' && owner(item)" class="assessment-owner">{{ owner(item) }}</span>
      </div>
      <span v-if="database" class="assessment-unit">
        {{ item.records.length }} {{ topics[item.metric.id].unit }}
        <small>{{ new Set(item.records.flatMap(row => row.assets)).size }} tabla(s)</small>
      </span>
      <v-btn :data-assessment="item.metric.id" :aria-label="`Ver registros de ${topics[item.metric.id].label}`"
        class="assessment-action" color="primary" variant="tonal" size="small" append-icon="mdi-arrow-right"
        @click="openRecords(item.metric.id)">Ver registros</v-btn>
    </article>
  </div>
  <div v-else class="assessment-detail">
    <v-btn variant="tonal" color="primary" size="small" prepend-icon="mdi-arrow-left"
      @click="closeRecords">Volver a evaluaciones</v-btn>
    <header class="assessment-detail-header" :class="`topic-${topics[group.metric.id].color}`">
      <span class="assessment-topic"><v-icon :icon="topics[group.metric.id].icon" size="24" /></span>
      <div>
        <small>{{ group.metric.id }} · Registros sintéticos</small>
        <h3 ref="detailTitle" tabindex="-1">{{ group.metric.name }}</h3>
      </div>
    </header>
    <div class="assessment-record-toolbar">
      <v-text-field v-model="query" label="Buscar registro, campo o tabla" prepend-inner-icon="mdi-magnify"
        variant="outlined" density="compact" clearable hide-details @click:clear="query = ''" />
      <v-select v-model="status" :items="statusOptions" label="Estado" variant="outlined" density="compact" hide-details />
    </div>
    <div class="assessment-record-count" aria-live="polite">
      <span v-if="filtered.length">{{ first + 1 }}–{{ first + visible.length }} de {{ filtered.length }}</span>
      <span v-else>0 registros</span>
      <span v-if="filtered.length !== group.records.length"> · {{ group.records.length }} en total</span>
    </div>
    <div v-if="!visible.length" class="assessment-empty">
      <v-icon icon="mdi-magnify" size="24" />
      <div><strong>Sin coincidencias</strong><p>Prueba con otro término o estado.</p></div>
    </div>
    <div v-else class="table-scroll assessment-records">
      <table class="data-table">
        <thead><tr><th>Registro</th><th>Estado</th><th>Detalle y tabla</th><th>Referencia sintética</th></tr></thead>
        <tbody>
          <tr v-for="row in visible" :key="row.id">
            <td><strong>{{ row.id }}</strong><small class="table-sub">{{ row.name }}</small></td>
            <td>
              <span class="observation-status" :class="`observation-${tone(row)}`">
                <v-icon :icon="stateIcons[tone(row)]" size="15" />{{ group.metric.id === 'M-04' ? 'Solicitud: ' : '' }}{{ row.statusLabel }}
              </span>
              <small v-if="row.grantLabel" class="table-sub">Concesión: {{ row.grantLabel }}</small>
              <small v-if="row.checkOutcome" class="table-sub">Resultado: {{ row.checkOutcome }}</small>
            </td>
            <td>{{ row.detail }}
              <div v-if="database" class="assessment-record-assets">
                <button v-for="name in row.assets" :key="name" class="entity-link" @click="$emit('asset', name)">{{ name }}</button>
              </div>
            </td>
            <td><span class="assessment-mobile-label" aria-hidden="true">Referencia sintética</span>{{ references.get(row.id) || 'Sin referencia de ejecución' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="group.records.length > 10" class="assessment-pager">
      <v-select v-model="pageSize" :items="[10, 25, 50]" label="Por página" variant="outlined" density="compact" hide-details />
      <div v-if="pages > 1" class="assessment-page-buttons">
        <v-btn size="small" variant="outlined" :disabled="page === 1" aria-label="Página anterior"
          icon="mdi-chevron-left" @click="page--" />
        <span>Página {{ page }} de {{ pages }}</span>
        <v-btn size="small" variant="outlined" :disabled="page === pages" aria-label="Página siguiente"
          icon="mdi-chevron-right" @click="page++" />
      </div>
    </div>
    <p v-if="group.metric.id === 'M-18'" class="assessment-caption">Se muestran las reglas con referencia explícita a la tabla.</p>
    <div class="assessment-detail-actions">
      <v-btn v-if="group.metric.id === 'M-09' && !database" size="small" color="primary" variant="outlined"
        @click="$emit('lineage')">Ver linaje contextual</v-btn>
      <v-btn size="small" color="primary" variant="outlined" append-icon="mdi-arrow-right"
        @click="$emit('metric', group.metric)">Consultar métrica general</v-btn>
    </div>
  </div>
</template>
