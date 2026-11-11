<script setup>
import { computed, ref } from 'vue'
const props = defineProps({ databases: { type: Array, required: true }, assets: { type: Array, required: true } })
const selected = ref(props.databases[0]?.id)
const database = computed(() => props.databases.find(db => db.id === selected.value) || props.databases[0])
const tables = computed(() => props.assets.filter(asset => asset.databaseId === database.value?.id))
</script>

<template>
  <div class="db-map">
    <div class="db-map-heading"><div><span>MAPA DEL CATÁLOGO</span><h2>Bases de datos y sus tablas</h2><p>Selecciona una base para ver sus tablas y el responsable de cada activo.</p></div><span class="db-count">{{ databases.length }} bases · {{ assets.length }} tablas</span></div>
    <div class="db-picker">
      <button v-for="db in databases" :key="db.id" type="button" class="db-choice" :class="{ selected: selected === db.id }" :aria-pressed="selected === db.id" @click="selected = db.id">
        <span class="db-choice-icon">▤</span><span><strong>{{ db.name }}</strong><small>{{ db.tables.length }} tablas</small></span>
      </button>
    </div>
    <div v-if="database" class="db-diagram">
      <div class="db-root"><span class="db-root-icon">▤</span><div><small>BASE DE DATOS</small><strong>{{ database.name }}</strong></div></div>
      <div class="db-connector" />
      <div class="db-children">
        <div v-for="table in tables" :key="table.id" class="db-table">
          <span class="db-table-icon">▦</span>
          <div><strong>{{ table.table }}</strong><span>{{ table.owner || 'Sin responsable' }}</span></div>
          <span class="db-owner-dot" :class="{ missing: !table.owner }" :title="table.owner ? 'Con responsable' : 'Sin responsable'" />
        </div>
      </div>
    </div>
  </div>
</template>
