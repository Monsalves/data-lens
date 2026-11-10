<script setup>
const observations = [
  {
    operation: 'GetDatabases',
    title: 'Base de catálogo visible',
    description: 'La respuesta incluyó una base llamada default.',
    excerpt: { DatabaseList: [{ Name: 'default' }] },
  },
  {
    operation: 'GetTables',
    title: 'Sin tablas visibles',
    description: 'La consulta a default devolvió una lista de tablas vacía para esa sesión.',
    excerpt: { TableList: [] },
  },
]
</script>

<template>
  <section class="surface table-panel glue-evidence" aria-labelledby="glue-evidence-heading">
    <div class="panel-head">
      <div>
        <div class="section-kicker">PRUEBA DE DESCUBRIMIENTO · AWS GLUE</div>
        <h2 id="glue-evidence-heading">Respuestas de AWS en Postman</h2>
      </div>
      <span class="status-pill success">Observación externa</span>
    </div>
    <p class="panel-desc">Dos respuestas compartidas por el operador. Los extractos omiten los identificadores de la cuenta y se muestran separados del inventario de demostración.</p>
    <ol class="glue-evidence-steps">
      <li v-for="item in observations" :key="item.operation">
        <code>{{ item.operation }}</code>
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
        <details>
          <summary>Ver extracto JSON</summary>
          <pre>{{ JSON.stringify(item.excerpt, null, 2) }}</pre>
        </details>
      </li>
    </ol>
    <div class="inline-info">
      <v-icon icon="mdi-information-outline" size="18" />
      <span>Alcance de la prueba: descubrimiento de bases y tablas. Las mediciones del piloto se ilustran con datos simulados.</span>
    </div>
  </section>
</template>
