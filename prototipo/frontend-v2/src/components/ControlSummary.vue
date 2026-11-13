<script setup>
import { computed } from 'vue'

const props = defineProps({
  metrics: { type: Array, required: true },
  results: { type: Array, required: true },
  contexts: { type: Object, default: () => ({}) },
  catalog: Boolean,
})
defineEmits(['metric'])

const presentation = {
  'M-01': {
    category: 'Tablas', title: 'Responsable informado', icon: 'mdi-account-check-outline', tone: 'blue',
    description: 'Tablas del catálogo con el campo de responsable informado.',
  },
  'M-04': {
    category: 'Acceso', title: 'Solicitudes de acceso', icon: 'mdi-key-outline', tone: 'violet',
    description: 'Solicitudes de acceso y estados de sus concesiones en el catálogo.',
  },
  'M-07': {
    category: 'Tablas', title: 'Metadatos requeridos', icon: 'mdi-format-list-checks', tone: 'blue',
    description: 'Campos obligatorios que tienen un valor informado.',
  },
  'M-09': {
    category: 'Linaje', title: 'Tramos de linaje', icon: 'mdi-source-branch', tone: 'blue',
    description: 'Conexiones registradas en el grafo del escenario.',
  },
  'M-11': {
    category: 'Calidad de datos', title: 'Filas con valor ausente', icon: 'mdi-table-search', tone: 'blue',
    description: 'Filas que fallan la regla de completitud de cliente_id.',
  },
  'M-16': {
    category: 'Procesos', title: 'Ejecuciones exitosas', icon: 'mdi-cog-outline', tone: 'teal',
    description: 'Ejecuciones terminales del job Glue que finalizaron con éxito.',
  },
  'M-18': {
    category: 'Calidad de datos', title: 'Reglas de calidad', icon: 'mdi-check-decagram-outline', tone: 'blue',
    description: 'Reglas configuradas para las que se obtuvo un resultado.',
  },
  'M-21': {
    category: 'Acceso', title: 'Permisos no utilizados', icon: 'mdi-key-outline', tone: 'violet',
    description: 'Hallazgos activos del analizador en la ventana de 90 días.',
  },
  'M-22': {
    category: 'Almacenamiento', title: 'Cifrado de objetos', icon: 'mdi-lock-outline', tone: 'teal',
    description: 'Proporción de objetos inspeccionados con SSE-KMS registrado.',
  },
  'M-25': {
    category: 'Auditoría', title: 'Campos de auditoría', icon: 'mdi-file-document-outline', tone: 'blue',
    description: 'Registros examinados con todos los campos exigidos.',
  },
  'M-26': {
    category: 'Tablas', title: 'Clasificación informada', icon: 'mdi-tag-outline', tone: 'blue',
    description: 'Activos del catálogo con una clasificación registrada.',
  },
  'M-27': {
    category: 'Privacidad', title: 'Intervenciones del guardrail', icon: 'mdi-shield-outline', tone: 'violet',
    description: 'Casos de prueba en los que el guardrail intervino.',
  },
  'M-29': {
    category: 'Almacenamiento', title: 'Ciclo de vida', icon: 'mdi-timer-outline', tone: 'teal',
    description: 'Buckets consultados con al menos una regla de ciclo de vida activa.',
  },
}
const percent = new Intl.NumberFormat('es-CL', { style: 'percent', maximumFractionDigits: 1 })
const resultsByMetric = computed(() => new Map(props.results.map(result => [result.metricId, result])))
const cards = computed(() => props.metrics.map(metric => {
  const result = resultsByMetric.value.get(metric.id)
  const { num, den } = result || metric
  return { metric, ...presentation[metric.id], num, den, simulated: Boolean(result) }
}))
</script>

<template>
  <div class="control-summary-grid">
    <button v-for="card in cards" :key="card.metric.id" type="button"
      class="surface control-summary-card" :class="`topic-${card.tone}`" @click="$emit('metric', card.metric)">
      <span class="control-card-top">
        <span class="assessment-topic"><v-icon :icon="card.icon" size="20" /></span>
        <span>{{ card.category }}</span>
        <span v-if="catalog" class="control-card-id">{{ card.metric.id }}</span>
      </span>
      <strong class="control-card-title">{{ catalog ? card.metric.name : card.title }}</strong>
      <span class="control-card-value">
        <strong>{{ card.den ? percent.format(card.num / card.den) : card.num }}</strong>
        <span>{{ card.den ? `${card.num} de ${card.den}` : card.metric.unit }}</span>
      </span>
      <span v-if="card.den" class="control-card-track" aria-hidden="true">
        <span :style="{ width: `${card.num / card.den * 100}%` }" />
      </span>
      <span class="control-card-description">{{ card.description }}</span>
      <span v-if="contexts[card.metric.id]" class="control-card-resource">{{ contexts[card.metric.id].resource }}</span>
      <span class="control-card-footer">
        <small>{{ card.simulated ? 'Resultado simulado' : 'Vista previa del escenario' }}</small>
        <span>Ver detalle <v-icon icon="mdi-arrow-right" size="17" /></span>
      </span>
    </button>
  </div>
</template>
