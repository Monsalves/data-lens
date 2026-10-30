# Sitio web de Data Lens

Sitio estático con Astro, centrado exclusivamente en la planificación. Requiere Node 24 LTS (mínimo 22.23.4) y npm.

La portada `/data-lens/` y el acceso existente `/data-lens/planificacion/` muestran directamente el mismo tablero a todo el ancho, sin menú lateral ni navegación de documentación. Las evidencias se abren en el repositorio desde el cronograma y desde la tabla. La cabecera solo identifica el proyecto y permite volver al inicio.

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
- `npm run sync`, ejecutado también antes del desarrollo y de cada compilación, genera los datos del tablero y las copias de descarga. No editar esos archivos generados.
- La planificación admite búsqueda, filtros por estado, tabla y cronograma. Es una vista de consulta: los cambios persistentes se hacen en el README y se publican con Git.
- Los estados reflejan el seguimiento registrado, no una validación automática de avance. El límite del 18 de diciembre del entregable S08 se conserva aunque su intervalo termine el 22.
- Para añadir evidencia, subir el documento al repo y enlazar su ruta relativa desde la columna de evidencia del README. El generador crea el enlace directo a GitHub y comprueba que el archivo existe. El acceso al documento conserva los permisos del repositorio privado.

El servidor de desarrollo vuelve a sincronizar las fuentes al iniciarse. Tras editar el README o los archivos fuente durante una sesión, ejecutar `npm run sync` para refrescar los datos.

## Publicación en GitHub Pages

La configuración corresponde a `https://monsalves.github.io/data-lens/`, con base `/data-lens`. En Settings → Pages, seleccionar GitHub Actions. El workflow valida, compila y publica cada cambio de `main`; en pull requests solo valida y compila.

Pages requiere un plan compatible para repositorios privados. El sitio publicado puede ser público aunque el repositorio sea privado; no cambiar la visibilidad del repositorio para resolver una limitación del plan. La web muestra solo la planificación y enlaza las evidencias en GitHub. Se conservan las descargas originales para compatibilidad; los accesos antiguos de metodología y entregables redirigen al repositorio. Investigaciones, mockups y antecedentes permanecen fuera.
