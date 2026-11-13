<script setup>
import { ref } from 'vue'
import metrics from '../data/metrics.json'
import { glueDemoJob as job, populationFor } from '../data/fixtures.js'

const opened = ref(false)
const rows = populationFor(metrics.find(metric => metric.id === 'M-16'))
const successful = rows.filter(row => row.statusCode === 'exitosa').length
const failed = rows.filter(row => row.statusCode === 'fallida').length
const rate = rows.length ? new Intl.NumberFormat('es-CL', { style: 'percent', maximumFractionDigits: 1 })
  .format(successful / rows.length) : 'Sin datos'
defineEmits(['metric'])
</script>

<template>
  <section class="surface process-overview">
    <header class="process-overview-heading">
      <div class="assessment-topic topic-blue"><v-icon icon="mdi-cog-transfer-outline" size="24" /></div>
      <div><h2>Procesos ETL</h2><p>Ejecuciones de ejemplo por job</p></div>
    </header>
    <div class="table-scroll">
      <table class="data-table process-table">
        <thead><tr>
          <th scope="col">Job</th><th scope="col">Ejecuciones</th><th scope="col">Exitosas</th>
          <th scope="col">Fallidas</th><th scope="col">Tasa de éxito</th><th scope="col">Historial</th>
        </tr></thead>
        <tbody><tr>
          <td class="process-job">
            <button class="entity-link process-job-name" :aria-expanded="opened" aria-controls="process-job-details"
              @click="opened = !opened">
              {{ job.name }} <v-icon :icon="opened ? 'mdi-chevron-up' : 'mdi-chevron-down'" size="16" />
            </button>
            <small class="table-sub">{{ job.service }} · {{ job.region }}</small>
          </td>
          <td class="process-stat"><span class="process-mobile-label">Ejecuciones</span><strong>{{ rows.length }}</strong></td>
          <td class="process-stat"><span class="process-mobile-label">Exitosas</span>
            <span class="observation-status observation-success"><v-icon icon="mdi-check-circle-outline" size="16" />{{ successful }}</span>
          </td>
          <td class="process-stat"><span class="process-mobile-label">Fallidas</span>
            <span class="observation-status" :class="failed ? 'observation-error' : 'observation-neutral'">
              <v-icon :icon="failed ? 'mdi-alert-circle-outline' : 'mdi-minus-circle-outline'" size="16" />{{ failed }}
            </span>
          </td>
          <td class="process-stat"><span class="process-mobile-label">Tasa de éxito</span>
            <strong class="process-rate">{{ rate }}</strong>
          </td>
          <td class="process-history"><v-btn color="primary" variant="tonal" size="small" append-icon="mdi-arrow-right"
            @click="$emit('metric', 'M-16', { name: job.name, kind: 'Proceso Glue', focus: 'metric-records' })">
            Ver ejecuciones del job
          </v-btn></td>
        </tr></tbody>
      </table>
    </div>
    <div v-show="opened" id="process-job-details" class="process-details">
      <h3>{{ job.title }}</h3>
      <p>{{ job.id }} · {{ job.owner }}</p>
      <p>Sin relaciones de entrada/salida verificables en el escenario.</p>
    </div>
  </section>
</template>
