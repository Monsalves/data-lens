# Data Lens · frontend del piloto técnico

SPA local en Vue 3 + Vuetify + Vite para recorrer el piloto de 13 métricas. El marco metodológico del assessment es independiente de esta aplicación.

[Abrir la demo del piloto en Data Lens](https://monsalves.github.io/data-lens/piloto/)

## Ejecutar

```bash
npm ci
npm run dev
```

Abrir `http://127.0.0.1:5173/`. Para generar los archivos estáticos: `npm run build`.

## Recorrido para la demostración

1. En **Inicio → Ver respuestas**, mostrar `GetDatabases` y `GetTables` en **Inventario → Validación Postman**. Son extractos de las respuestas reportadas por el operador, con los identificadores omitidos.
2. En **Inventario → Mapa de bases**, recorrer una base y sus tablas de ejemplo. En **Lista de recursos**, buscar «Carga de clientes a Analítica» y abrir **Ver M-16** para explicar el paso de `ListJobs` a `GetJobRuns`.
3. Ejecutar **Simular medición** y abrir **Ver métricas**. En M-09, usar el filtro «Sin evidencia en la consulta» y seleccionar un enlace del grafo para ver por qué figura en el diseño ficticio. Para M-01, usar «Sin responsable».

## Qué funciona

- Navegación: Inicio, Cuentas AWS, Inventario, Mediciones y Ejecuciones. Los resultados se consultan directamente en Mediciones.
- Catálogo de 13 métricas con operaciones y enlaces a documentación AWS, filtros y detalle técnico.
- Desglose identificable de numerador y universo por métrica. M-09 compara 10 tramos de un diseño ficticio con 8 coincidencias en una consulta simulada. En una evaluación real se requiere una referencia validada e independiente para calcular cobertura. Con el registro de DataZone solo se pueden describir los tramos visibles en la consulta.
- Inventario con mapa seleccionable de cuatro bases de datos y sus tablas, además de la lista filtrable de recursos.
- Simulación local de un lote de medición, progreso, historial, resultados y referencias de evidencia sintéticas.
- Registro local de parámetros de cuenta y exportación JSON de resultados simulados.

**Estado:** el inventario de ejemplo y las mediciones son simulados. La pestaña **Validación Postman** muestra dos extractos de descubrimiento reportados por el operador. La conexión directa con AWS depende de la integración con FastAPI. El registro de cuentas se guarda en `localStorage`.

El archivo `src/data/metrics.json` contiene el catálogo técnico derivado del explorador local de 13 métricas. El escenario de ejemplo sigue una tienda en línea. Sus nombres se reutilizan en el inventario, el linaje y las filas de las métricas. Los resultados conservan los numeradores y denominadores del dataset simulado. No representan mediciones observadas.
