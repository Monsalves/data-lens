<script setup>
import { computed } from 'vue'
const props = defineProps({ nodes: { type: Array, required: true }, edges: { type: Array, required: true }, statusFilter: { type: String, default: 'Todos' }, selectedEdgeId: { type: String, default: '' } })
const emit = defineEmits(['select'])
const positions = computed(() => Object.fromEntries(props.nodes.map(n => [n.id, n])))
function pathFor(edge) {
  const from = positions.value[edge.from], to = positions.value[edge.to]
  const x1 = from.x + 176, y1 = from.y + 30, x2 = to.x, y2 = to.y + 30
  return `M ${x1} ${y1} C ${x1 + 45} ${y1}, ${x2 - 45} ${y2}, ${x2} ${y2}`
}
const selectedEdge = computed(() => props.edges.find(e => e.id === props.selectedEdgeId))
function label(id) { return positions.value[id]?.label || id }
</script>

<template>
  <div class="lineage-wrap"><div class="lineage-summary"><span><i class="legend-line observed" /> Registrado en el ejemplo de DataZone</span><span><i class="legend-line missing" /> En el diseño, sin evidencia en la consulta</span></div><div class="lineage-scroll"><svg viewBox="0 0 938 440" role="img" aria-label="Comparación simulada de los tramos del diseño con el linaje registrado en DataZone"><defs><marker id="arrow-observed" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="#5082dd" /></marker><marker id="arrow-missing" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="#bb8a3e" /></marker></defs><g v-for="edge in edges" :key="edge.id" class="edge" :class="{ chosen: selectedEdgeId === edge.id, dimmed: statusFilter !== 'Todos' && statusFilter !== (edge.observed ? 'observado' : 'no_observado') }" role="button" tabindex="0" :aria-label="`${edge.id}: ${edge.observed ? 'registrado' : 'sin evidencia en la consulta'}`" @click="emit('select', edge.id)" @keydown.enter="emit('select', edge.id)"><path :d="pathFor(edge)" class="edge-hit" /><path :d="pathFor(edge)" class="edge-line" :class="edge.observed ? 'observed' : 'missing'" :marker-end="edge.observed ? 'url(#arrow-observed)' : 'url(#arrow-missing)'" /></g><g v-for="node in nodes" :key="node.id" :transform="`translate(${node.x}, ${node.y})`"><title>{{ node.label }} · {{ node.name }}</title><rect width="176" height="60" rx="10" class="node-card" /><rect x="10" y="12" width="35" height="35" rx="8" class="node-icon" /><text x="27" y="35" text-anchor="middle" class="node-glyph">▦</text><text x="55" y="25" class="node-kind">{{ node.kind.toUpperCase() }}</text><text x="55" y="43" class="node-label">{{ node.label }}</text></g></svg></div><div v-if="selectedEdge" class="lineage-selected"><strong>{{ selectedEdge.id }}</strong><span>{{ label(selectedEdge.from) }} → {{ label(selectedEdge.to) }}</span><span>{{ selectedEdge.purpose }}</span><b :class="selectedEdge.observed ? 'yes' : 'no'">{{ selectedEdge.observed ? 'Registrado' : 'Sin evidencia en la consulta' }}</b></div><p>Selecciona un tramo para ver sus extremos y la razón por la que figura en el diseño. La captura de eventos y el alcance de la consulta determinan qué relaciones se pueden observar.</p></div>
</template>
