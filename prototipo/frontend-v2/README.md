# Data Lens · Prototipo 2.0

[Abrir el prototipo 2.0](https://monsalves.github.io/data-lens/piloto-v2/) · [Abrir el prototipo 1.0](https://monsalves.github.io/data-lens/piloto/)

Demo de navegación por activos basada en el checkpoint `046df60`. En **Datos** se pueden explorar agrupaciones, tablas y buckets S3 y abrir sus observaciones. **Procesos** muestra el job Glue del escenario. **Mediciones** permite consultar las 13 métricas y sus registros, y **Historial** muestra los lotes de simulación.

Los recursos y resultados son sintéticos. El formulario de Conexiones guarda la configuración en el navegador sin verificar el acceso a AWS. El historial, las conexiones y la preferencia de vista de 2.0 se guardan con sus propias claves.

## Ejecutar

```bash
npm ci
npm run dev
```

La publicación en GitHub Pages se genera desde la raíz del repositorio. [Construcción y despliegue](../../DESARROLLO.md) · [Alcance de las métricas](ALCANCE_METRICAS.md)
