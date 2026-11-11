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

1. Abrir **Resumen**: una fila compacta por pilar muestra las situaciones de sus métricas con barra, conteo y porcentaje cuando hay denominador. Los resultados son simulados y no se califican como madurez. Verde/amarillo distingue la parte sin la condición señalada de la parte a revisar; azul identifica proporciones descriptivas sin juicio favorable o desfavorable.
2. Seleccionar un pilar para abrir **Métricas** con su acordeón desplegado. Se pueden mantener abiertos varios pilares a la vez. Desde cada métrica se abre el detalle con cálculo y elementos revisados. M-21 muestra solo ocho hallazgos, sin una tasa inventada.
3. Ejecutar **Simular medición** para producir los 13 resultados de ejemplo. En **Inventario** se pueden explorar bases, tablas y recursos del escenario sintético.

## Qué funciona

- Navegación: Resumen, Cuentas, Inventario, Métricas y Ejecuciones. El Resumen presenta los cinco pilares en una vista compacta; Métricas los agrupa en acordeones con el color propio de cada pilar antes de abrir cada detalle. La tipografía de la interfaz es IBM Plex Sans. Un aviso superior identifica los datos de ejemplo sin repetir esa indicación en cada resultado.
- Cuentas registradas y formulario para agregar una cuenta. La configuración se guarda en el navegador; no verifica el acceso ni consulta recursos externos.
- Catálogo de 13 métricas con operaciones y enlaces a documentación AWS, filtros y detalle técnico.
- Desglose identificable de numerador y universo por métrica cuando corresponde. M-09 cuenta ocho conexiones registradas en el grafo de ejemplo, sin porcentaje de cobertura ni tramos faltantes inferidos. Cada detalle explica el alcance de la cifra mostrada.
- Inventario con mapa seleccionable de cuatro bases de datos y sus tablas, además de la lista filtrable de recursos. La lista conserva «Simulado» en Estado y no muestra una columna de medición.
- Simulación local de un lote de medición, progreso, historial, resultados y referencias de evidencia sintéticas.
- Exportación JSON de resultados simulados.

**Estado:** el inventario de ejemplo y las mediciones son simulados. La vista de Validación Postman se retiró del frontend; los dos extractos reportados por el operador siguen documentados en el contexto del proyecto. La conexión directa con fuentes externas sigue pendiente de integración. El frontend conserva en el catálogo técnico las operaciones y enlaces propios del piloto actual, mientras la identidad y la navegación de Data Lens son neutrales respecto de la nube.

El archivo `src/data/metrics.json` contiene el catálogo técnico derivado del explorador local de 13 métricas. El escenario de ejemplo sigue una tienda en línea. Sus nombres se reutilizan en el inventario, el linaje y las filas de las métricas. Los resultados muestran conteos y universos cuando corresponde. No representan mediciones observadas.

[Revisión del alcance de las 13 métricas](ALCANCE_METRICAS.md): indicador mostrado, fuente técnica prevista y conclusión que no se puede extraer de ese dato. Las versiones más ambiciosas de cobertura o conformidad siguen como hipótesis metodológicas, no como capacidades demostradas por este frontend.
