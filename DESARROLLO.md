# Sitio web de Data Lens

Sitio estático con Astro. Requiere Node 24 LTS (mínimo 22.23.4) y npm.

La portada `/data-lens/` y `/data-lens/planificacion/` muestran el tablero. La metodología, el mapa preliminar AWS y las dos planillas Excel tienen páginas de lectura dentro del sitio, con retorno a la planificación. Los originales están disponibles para descarga.

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
- `npm run sync`, ejecutado también antes del desarrollo y de cada compilación, genera los datos del tablero, las vistas de lectura Excel y las copias de descarga. No editar esos archivos generados.
- La planificación admite búsqueda, filtros por estado, tabla y cronograma. Es una vista de consulta: los cambios persistentes se hacen en el README y se publican con Git.
- Los estados reflejan el seguimiento registrado, no una validación automática de avance. El límite del 18 de diciembre del entregable S08 se conserva aunque su intervalo termine el 22.
- Para añadir evidencia, subir el documento al repo y enlazar su ruta relativa desde la columna de evidencia del README. El generador comprueba que el archivo existe. Las evidencias de formato conocido se abren dentro del sitio; para otros archivos, el enlace sigue apuntando a GitHub hasta crear su vista interna.

El servidor de desarrollo vuelve a sincronizar las fuentes al iniciarse. Tras editar el README o los archivos fuente durante una sesión, ejecutar `npm run sync` para refrescar los datos.

## Publicación en GitHub Pages

La configuración corresponde a `https://monsalves.github.io/data-lens/`, con base `/data-lens`. En Settings → Pages, seleccionar GitHub Actions. El workflow valida, compila y publica cada cambio de `main`; en pull requests solo valida y compila.

La web publica solo los documentos que ya forman parte de este repositorio. La ruta antigua de metodología ahora muestra la guía dentro del sitio; `/entregables/` vuelve a la portada. El resto de investigaciones, mockups y antecedentes permanecen fuera.
