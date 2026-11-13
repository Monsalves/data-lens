<script setup>
import { computed, nextTick, ref, watch, watchEffect } from 'vue'
import { databases, dataZoneAssets } from '../data/fixtures.js'
import ContextLineage from './ContextLineage.vue'
import AssetAssessments from './AssetAssessments.vue'
import ControlSummary from './ControlSummary.vue'
import { assessmentsForAssets, recordsForBucket } from '../data/assetAssessments.js'
const props = defineProps({
  metrics: Array, buckets: Array, initialType: { type: String, default: 'Todos' },
  results: { type: Array, default: () => [] },
  metricContexts: { type: Object, default: () => ({}) },
})
const emit = defineEmits(['metric', 'focus', 'measurements'])
function selectMetric(metric) { emit('metric', metric, { name: asset.value?.name || database.value.name, kind: asset.value ? 'Tabla / dataset' : 'Base / agrupación' }) }
const databaseId = ref('')
const assetId = ref('')
const bucketId = ref('')
watchEffect(() => emit('focus', !!(databaseId.value || bucketId.value)))
const query = ref('')
const inventoryType = ref(props.initialType)
const showBucketList = ref(false)
const bucketListReturn = ref(null)
const bucketListButton = ref(null)
watch(() => props.initialType, type => { inventoryType.value = type })
watch(query, value => {
  if (value.trim() && !databaseId.value && !bucketId.value) showBucketList.value = true
})
const tab = ref('Resumen')
const databaseTab = ref('Resumen')
const databaseTables = computed(() => dataZoneAssets.filter(a => a.databaseId === databaseId.value))
const databaseAssessments = computed(() => assessmentsForAssets(databaseTables.value, props.metrics))
const tableAssessments = computed(() => asset.value ? assessmentsForAssets([asset.value], props.metrics) : [])
function backToDatabase() { assetId.value = ''; window.scrollTo(0, 0) }
const database = computed(() => databases.find(d => d.id === databaseId.value))
const asset = computed(() => dataZoneAssets.find(a => a.id === assetId.value))
const tables = computed(() => dataZoneAssets.filter(a => a.databaseId === databaseId.value && `${a.name} ${a.owner}`.toLowerCase().includes(query.value.toLowerCase())))
const groups = computed(() => databases.filter(d => `${d.name} ${d.domain}`.toLowerCase().includes(query.value.toLowerCase())))
const matchingBuckets = computed(() => props.buckets.filter(item =>
  `${item.name} ${item.title} ${item.owner}`.toLowerCase().includes(query.value.toLowerCase()),
))
const bucket = computed(() => props.buckets.find(item => item.id === bucketId.value))
const bucketMetrics = computed(() => props.metrics
  .filter(metric => ['M-29', 'M-22'].includes(metric.id))
  .sort((a, b) => b.id.localeCompare(a.id)))
const bucketChecks = computed(() => bucket.value
  ? bucketMetrics.value.map(metric => ({ metric, rows: recordsForBucket(bucket.value, metric) }))
  : [])
const showBases = computed(() => inventoryType.value !== 'Buckets S3' && groups.value.length > 0)
const showBuckets = computed(() => inventoryType.value !== 'Agrupaciones' && matchingBuckets.value.length > 0)
function openBucket(item) {
  bucketId.value = item.id
  window.scrollTo(0, 0)
}
async function openBucketList() {
  showBucketList.value = true
  await nextTick()
  bucketListReturn.value?.$el.focus()
}
async function closeBucketList() {
  query.value = ''
  showBucketList.value = false
  await nextTick()
  bucketListButton.value?.focus()
}
function backToInventory() {
  if (!bucketId.value) query.value = ''
  bucketId.value = ''; databaseId.value = ''; assetId.value = ''
  window.scrollTo(0, 0)
}
function openBucketMetric(check) {
  const recordSearch = check.metric.id === 'M-29' ? check.rows[0].id : bucket.value.name
  emit('metric', check.metric, {
    name: bucket.value.name, kind: 'Bucket S3', focus: 'metric-records', recordSearch,
  })
}
function openDatabase(id) { databaseId.value = id; assetId.value = ''; query.value = ''; databaseTab.value = 'Resumen'; window.scrollTo(0, 0) }
function openNamedAsset(name) { const found = dataZoneAssets.find(a => a.name === name); if (found) { databaseId.value = found.databaseId; openAsset(found.id) } }
function openAsset(id) { assetId.value = id; tab.value = 'Resumen'; window.scrollTo(0, 0) }
</script>
<template>
  <nav class="entity-breadcrumb" aria-label="Ruta de datos"><button @click="backToInventory">Datos</button><template v-if="database"> / <button @click="backToDatabase">{{ database.name }}</button></template><span v-if="asset"> / {{ asset.table }}</span><span v-if="bucket"> / {{ bucket.name }}</span></nav>
  <div :key="databaseId || bucketId || 'groups'" class="entity-stage">
  <template v-if="bucket">
    <header class="entity-heading asset-heading bucket-heading">
      <div class="entity-heading-icon"><v-icon icon="mdi-bucket-outline" size="28" /></div>
      <div><h2>{{ bucket.name }}</h2><p>Bucket S3 · {{ bucket.region }} · {{ bucket.owner }}</p></div>
    </header>
    <section class="surface assessment-panel">
      <h3>Controles del bucket</h3>
      <p class="assessment-caption">Registros sintéticos vinculados a este bucket.</p>
      <article v-for="check in bucketChecks" :key="check.metric.id" class="bucket-check">
        <div>
          <strong>{{ check.metric.id === 'M-29' ? 'Ciclo de vida' : 'Cifrado de objetos' }}</strong>
          <template v-if="check.rows.length">
            <div v-if="check.metric.id === 'M-29'" class="bucket-check-status">
              <span class="observation-status" :class="check.rows[0].tone === 'warning' ? 'observation-warning' : 'observation-info'">{{ check.rows[0].statusLabel }}</span>
              <span>{{ check.rows[0].detail }}</span>
            </div>
            <div v-else class="bucket-check-status">
              <span>{{ check.rows.length }} objetos de ejemplo</span>
              <span class="observation-status observation-info">{{ check.rows.filter(row => row.statusCode === 'sse_kms').length }} con SSE-KMS</span>
              <span class="observation-status observation-neutral">{{ check.rows.filter(row => row.statusCode === 'sse_s3').length }} con SSE-S3</span>
            </div>
          </template>
          <p v-else class="assessment-caption">Sin registros vinculados</p>
        </div>
        <v-btn v-if="check.rows.length" color="primary" variant="tonal" size="small" append-icon="mdi-arrow-right"
          :aria-label="`Ver registros de ${check.metric.id === 'M-29' ? 'ciclo de vida' : 'cifrado de objetos'}`"
          @click="openBucketMetric(check)">Ver registros</v-btn>
      </article>
    </section>
  </template>
  <template v-else-if="!database">
    <div class="data-explorer-toolbar">
      <v-text-field v-model="query" label="Buscar agrupación o bucket" prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details />
      <v-select v-model="inventoryType" :items="['Todos', 'Agrupaciones', 'Buckets S3']" label="Tipo de recurso" variant="outlined" density="compact" hide-details />
    </div>
    <h2 v-if="showBases" class="inventory-group-title">Agrupaciones <small>{{ groups.length }}</small></h2>
    <div v-if="showBases" class="database-grid">
      <button v-for="(d, index) in groups" :key="d.id" class="database-card" :style="{ '--enter-delay': `${index * 45}ms` }" @click="openDatabase(d.id)">
        <span class="database-card-top"><span class="database-glyph"><v-icon icon="mdi-database-outline" size="30" /></span><span class="database-domain">{{ d.domain }}</span></span>
        <strong>{{ d.name }}</strong><span class="database-description">{{ d.title }}</span>
        <span class="database-owner"><v-icon icon="mdi-account-outline" size="16" />{{ d.owner }}</span>
        <span class="database-card-foot"><span><b>{{ d.tables.length }}</b> tablas / datasets</span><span class="card-explore">Explorar <v-icon icon="mdi-arrow-right" size="18" /></span></span>
      </button>
    </div>
    <section v-if="showBuckets" class="inventory-buckets" aria-labelledby="inventory-buckets-title">
      <h2 id="inventory-buckets-title" class="inventory-group-title">Buckets S3</h2>
      <div v-if="!showBucketList" class="bucket-overview">
        <button ref="bucketListButton" type="button" class="surface bucket-total" @click="openBucketList">
          <span class="assessment-topic topic-teal"><v-icon icon="mdi-bucket-outline" size="22" /></span>
          <span><strong>{{ buckets.length }} buckets</strong><small>Ver listado de buckets</small></span>
          <v-icon icon="mdi-arrow-right" size="19" />
        </button>
        <ControlSummary :metrics="bucketMetrics" :results="results" :contexts="metricContexts"
          @metric="metric => emit('metric', metric, { kind: 'Resumen de buckets' })" />
      </div>
      <div v-else class="surface bucket-list">
        <div class="bucket-list-toolbar">
          <span>{{ matchingBuckets.length }} de {{ buckets.length }} buckets</span>
          <v-btn ref="bucketListReturn" color="primary" variant="tonal" size="small" prepend-icon="mdi-arrow-left"
            @click="closeBucketList">Volver al resumen de buckets</v-btn>
        </div>
        <button v-for="item in matchingBuckets" :key="item.id" type="button" class="bucket-list-row" @click="openBucket(item)">
          <span class="assessment-topic topic-teal"><v-icon icon="mdi-bucket-outline" size="20" /></span>
          <span><strong>{{ item.name }}</strong><small>{{ item.region }} · {{ item.owner }}</small></span>
          <v-icon icon="mdi-chevron-right" size="20" />
        </button>
      </div>
    </section>
    <div v-if="!showBases && !showBuckets" class="designed-empty"><v-icon icon="mdi-magnify" size="32" /><h3>Sin coincidencias</h3><p>Prueba con otro nombre o tipo de recurso.</p></div>
  </template>
  <div v-else v-show="!asset">
    <header class="entity-heading asset-heading database-heading"><div class="entity-heading-icon"><v-icon icon="mdi-database-outline" size="28" /></div><div><h2>{{ database.name }}</h2><p>{{ database.title }} · {{ database.domain }}</p><div class="entity-tags"><span>{{ databaseTables.length }} tablas</span><span>{{ database.owner }}</span><span>Inventario de catálogo</span></div></div></header>
    <v-tabs v-model="databaseTab" color="primary" show-arrows><v-tab v-for="t in ['Resumen', 'Tablas']" :key="t" :value="t">{{ t }}</v-tab></v-tabs>
    <div :key="databaseTab" class="tab-content mt-5">
      <section v-if="databaseTab === 'Resumen'" class="surface assessment-panel">
        <div class="base-evaluation-heading">
          <div>
            <h3>Evaluaciones de sus tablas</h3>
            <p>{{ databaseAssessments.length }} métricas con registros vinculados a esta base</p>
          </div>
          <v-btn color="primary" variant="tonal" size="small" append-icon="mdi-arrow-right"
            @click="emit('measurements')">Ver las {{ metrics.length }} métricas</v-btn>
        </div>
        <AssetAssessments :groups="databaseAssessments" :results="results" database @asset="openNamedAsset" @metric="selectMetric" />
      </section>
      <template v-else>
        <v-text-field v-model="query" label="Buscar tabla o responsable" prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details class="entity-search mb-5" />
    <section class="surface table-scroll tables-surface"><div class="list-caption"><span><v-icon icon="mdi-table-large" size="18" /> Tablas de {{ database.name }}</span><span>{{ tables.length }} visibles</span></div><table class="data-table"><thead><tr><th>TABLA / DATASET</th><th>ORIGEN</th><th>RESPONSABLE</th><th></th></tr></thead><tbody>
      <tr v-for="a in tables" :key="a.id"><td><div class="table-identity"><span class="table-glyph"><v-icon icon="mdi-table" size="20" /></span><div><button class="entity-link" @click="openAsset(a.id)">{{ a.table }}</button><small class="table-sub">{{ a.id }}</small></div></div></td><td class="inventory-origin"><span class="inventory-mobile-label" aria-hidden="true">Origen</span>{{ a.service }} · Catálogo</td><td class="inventory-owner"><span class="inventory-mobile-label" aria-hidden="true">Responsable</span>{{ a.owner || 'Sin información' }}</td><td class="inventory-action"><v-btn color="primary" variant="tonal" size="small" append-icon="mdi-arrow-right" @click="openAsset(a.id)">Ver ficha</v-btn></td></tr>
    </tbody></table></section>
        <div v-if="!tables.length" class="designed-empty"><h3>Sin coincidencias</h3><p>Prueba con otro nombre o responsable.</p></div>
      </template>
    </div>
  </div>
  <div v-if="asset" :key="assetId">
    <header class="entity-heading asset-heading"><div class="entity-heading-icon"><v-icon icon="mdi-table" size="28" /></div><div><h2>{{ asset.table }}</h2><p>{{ asset.name }} · {{ asset.service }} · {{ asset.region }}</p></div></header>
    <v-tabs v-model="tab" color="primary" show-arrows><v-tab v-for="t in ['Resumen', 'Evaluaciones', 'Linaje']" :key="t" :value="t">{{ t }}</v-tab></v-tabs>
    <section :key="tab" class="surface table-panel mt-5 tab-content">
      <dl v-if="tab === 'Resumen'" class="asset-metadata"><template v-for="(value, key) in { Identificador: asset.id, Nombre: asset.title, Agrupación: database.name, 'Origen del metadato': asset.service, Región: asset.region, Responsable: asset.owner || 'Sin información', Columnas: 'Sin información', 'Motor físico': 'No verificable con estos metadatos' }" :key="key"><dt>{{ key }}</dt><dd>{{ value }}</dd></template></dl>
      <div v-if="tab === 'Resumen'" class="table-observation-preview"><span class="eyebrow">OBSERVACIONES DISPONIBLES</span><p>{{ tableAssessments.length }} métricas con registros asociados a esta tabla.</p><div v-for="g in tableAssessments.filter(g => ['M-01', 'M-07', 'M-26'].includes(g.metric.id))" :key="g.metric.id" class="table-observation-line"><strong>{{ g.metric.name }}</strong><span>{{ [...new Set(g.records.map(r => r.statusLabel))].join(' · ') }}</span></div><v-btn variant="flat" color="primary" prepend-icon="mdi-clipboard-text-search-outline" @click="tab = 'Evaluaciones'">Examinar observaciones y registros</v-btn><p v-if="!tableAssessments.some(g => ['M-11', 'M-18'].includes(g.metric.id))" class="panel-desc">No hay evaluación de calidad asociada a esta tabla.</p></div>
      <template v-if="tab === 'Evaluaciones'"><AssetAssessments :groups="tableAssessments" :results="results" @lineage="tab = 'Linaje'" @metric="selectMetric" /></template>
      <template v-if="tab === 'Linaje'"><ContextLineage :asset="asset" @asset="openNamedAsset" @metric="selectMetric" /></template>
    </section>
  </div>
  </div>
</template>
