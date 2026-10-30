# Sitio web de Data Lens

Sitio estático con Astro y Starlight. Requiere Node 24 LTS (mínimo 22.23.4) y npm.

## Abrir y construir

```bash
npm ci
npm run dev
```

Abrir la dirección local que imprime Astro, con la base `/data-lens/`.

```bash
npm test
npm run check
npm run build
npm run preview
```

`dist/` es el sitio generado. No se versiona. `npm run preview` permite revisarlo después de compilar.

## Actualizar el contenido

- Editar la metodología original en `metodologia/Marco_Trabajo_Datos_v1_4.md`.
- Editar actividades, fechas, entregables, estados y evidencia en la tabla de `README.md`.
- Mantener el Excel original en `planificacion/Planificacion.xlsx`; se ofrece como descarga, sin modificarlo ni usarlo para deducir estados.
- `npm run sync`, ejecutado también antes del desarrollo y de cada compilación, genera las páginas y datos derivados. No editar esos archivos generados.
- La planificación admite búsqueda, filtros por estado, tabla y cronograma. Es una vista de consulta: los cambios persistentes se hacen en el README y se publican con Git.
- Los estados reflejan el seguimiento registrado, no una validación automática de avance. El límite del 18 de diciembre del entregable S08 se conserva aunque su intervalo termine el 22.
- Si se añade un documento de evidencia, definir su ruta web en `scripts/planning.mjs`; la compilación rechaza enlaces no resueltos.

El servidor de desarrollo vuelve a sincronizar las fuentes al iniciarse. Tras editar el README o la metodología original durante una sesión, ejecutar `npm run sync` para refrescar las páginas.

## Publicación en GitHub Pages

La configuración corresponde a `https://monsalves.github.io/data-lens/`, con base `/data-lens`. En Settings → Pages, seleccionar GitHub Actions. El workflow valida, compila y publica cada cambio de `main`; en pull requests solo valida y compila.

Pages requiere un plan compatible para repositorios privados. El sitio publicado puede ser público aunque el repositorio sea privado; no cambiar la visibilidad del repositorio para resolver una limitación del plan. El sitio contiene solo la metodología, las actividades y las descargas expresamente incorporadas. Investigaciones, mockups y antecedentes permanecen fuera.
