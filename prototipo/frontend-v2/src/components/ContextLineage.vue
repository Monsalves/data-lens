<script setup>
import { computed, ref, watch } from 'vue'
import { dataZoneAssets, lineageNodes, lineageEdges } from '../data/fixtures.js'
const props = defineProps({ asset: { type: Object, required: true } })
defineEmits(['asset', 'metric'])
const selected = ref('')
const center = computed(() => lineageNodes.find(n => n.name === props.asset.name))
const edges = computed(() => center.value ? lineageEdges.filter(e => e.from === center.value.id || e.to === center.value.id) : [])
const incoming = computed(() => edges.value.filter(e => e.to === center.value.id))
const outgoing = computed(() => edges.value.filter(e => e.from === center.value.id))
const height = computed(() => Math.max(180, Math.max(incoming.value.length, outgoing.value.length) * 100 + 40))
const nodes = computed(() => center.value ? [{ ...center.value, px: 450, py: height.value / 2 }, ...incoming.value.map((e, i) => ({ ...node(e.from), px: 145, py: 70 + i * 100 })), ...outgoing.value.map((e, i) => ({ ...node(e.to), px: 755, py: 70 + i * 100 }))] : [])
const detail = computed(() => edges.value.find(e => e.id === selected.value))
function node(id) { return lineageNodes.find(n => n.id === id) }
function inventory(name) { return dataZoneAssets.find(a => a.name === name) }
function path(e) { const from = nodes.value.find(n => n.id === e.from); const to = nodes.value.find(n => n.id === e.to); return `M ${from.px + 125} ${from.py} C ${from.px + 170} ${from.py}, ${to.px - 170} ${to.py}, ${to.px - 125} ${to.py}` }
watch(() => props.asset.id, () => { selected.value = '' })
</script>
<template>
  <div v-if="!edges.length" class="designed-empty"><v-icon icon="mdi-source-branch" size="30" /><h3>Sin relaciones registradas en este escenario</h3></div>
  <div v-else>
    <p class="assessment-caption">Vecinos directos · Relaciones sintéticas; no acreditan cobertura completa ni vínculos con jobs.</p>
    <svg class="context-lineage" :viewBox="`0 0 900 ${height}`" role="group" aria-label="Grafo de entradas y salidas de la tabla">
      <defs><marker id="context-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b" /></marker></defs>
      <g v-for="e in edges" :key="e.id" role="button" tabindex="0" :aria-label="`${e.id}: ${node(e.from).name} hacia ${node(e.to).name}`" :aria-pressed="selected === e.id" class="context-edge" @click="selected = e.id" @keydown.enter.prevent="selected = e.id" @keydown.space.prevent="selected = e.id"><path :d="path(e)" class="edge-hit" /><path :d="path(e)" class="context-edge-line" marker-end="url(#context-arrow)" /><text :x="(nodes.find(n => n.id === e.from).px + nodes.find(n => n.id === e.to).px) / 2" :y="(nodes.find(n => n.id === e.from).py + nodes.find(n => n.id === e.to).py) / 2 - 10">{{ e.id }}</text></g>
      <g v-for="n in nodes" :key="`${n.id}-${n.px}`" :transform="`translate(${n.px - 125}, ${n.py - 30})`" :class="['context-node', { center: n.id === center.id, navigable: inventory(n.name) }]" :role="inventory(n.name) && n.id !== center.id ? 'button' : undefined" :tabindex="inventory(n.name) && n.id !== center.id ? 0 : undefined" :aria-label="inventory(n.name) && n.id !== center.id ? `Abrir ${n.name}` : n.name" @click="inventory(n.name) && n.id !== center.id && $emit('asset', n.name)" @keydown.enter.prevent="inventory(n.name) && n.id !== center.id && $emit('asset', n.name)" @keydown.space.prevent="inventory(n.name) && n.id !== center.id && $emit('asset', n.name)"><rect width="250" height="60" rx="9" /><text x="12" y="24">{{ n.name.split('.')[0] }}</text><text x="12" y="43" class="node-table">{{ n.name.split('.').slice(1).join('.') || n.name }}</text></g>
    </svg>
    <div class="lineage-lists"><section v-for="direction in ['Entradas', 'Salidas']" :key="direction"><h3>{{ direction }}</h3><p v-if="!(direction === 'Entradas' ? incoming : outgoing).length" class="assessment-caption">Sin {{ direction.toLowerCase() }} registradas.</p><button v-for="e in direction === 'Entradas' ? incoming : outgoing" :key="e.id" class="lineage-relation" :aria-pressed="selected === e.id" @click="selected = e.id"><strong>{{ e.id }}</strong><span>{{ node(direction === 'Entradas' ? e.from : e.to).name }}</span><v-icon icon="mdi-chevron-right" size="16" /></button></section></div>
    <section v-if="detail" class="lineage-detail"><h3>{{ detail.id }} · Relación registrada</h3><dl><dt>Origen</dt><dd>{{ node(detail.from).name }}</dd><dt>Destino</dt><dd>{{ node(detail.to).name }}</dd><dt>Propósito</dt><dd>{{ detail.purpose }}</dd></dl><v-btn v-for="id in [detail.from, detail.to].filter(id => inventory(node(id).name) && id !== center.id)" :key="id" variant="text" size="small" @click="$emit('asset', node(id).name)">Abrir {{ node(id).name }}</v-btn></section>
    <v-btn variant="text" class="mt-3" @click="$emit('metric', 'M-09')">Explorar grafo completo en M-09</v-btn>
  </div>
</template>
