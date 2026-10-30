import { readFile, writeFile, mkdir, copyFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { parsePlanning } from './planning.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const at = (path) => resolve(root, path);
const methodologyPath = 'metodologia/Marco_Trabajo_Datos_v1_4.md';
const [readme, methodology] = await Promise.all([
  readFile(at('README.md'), 'utf8'), readFile(at(methodologyPath), 'utf8')
]);
const activities = parsePlanning(readme);
await Promise.all(['src/data', 'src/content/docs', 'public/descargas'].map((path) => mkdir(at(path), { recursive: true })));
const body = methodology.replace(/^# .+\r?\n/u, '').trimStart();
await Promise.all([
  writeFile(at('src/data/planning.json'), JSON.stringify({ source: 'README.md', activities }, null, 2) + '\n'),
  writeFile(at('src/content/docs/metodologia.md'), `---\ntitle: Marco de trabajo para la evaluación de datos\ndescription: Metodología oficial 1.4, con las cuatro fases de evaluación y el menú de métricas propuestas.\n---\n\n${body}`),
  copyFile(at(methodologyPath), at('public/descargas/Marco_Trabajo_Datos_v1_4.md')),
  copyFile(at('planificacion/Planificacion.xlsx'), at('public/descargas/Planificacion.xlsx'))
]);
console.log(`Contenido sincronizado: metodología 1.4, ${activities.length} actividades y descargas originales.`);
