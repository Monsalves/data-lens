import { readFile, writeFile, mkdir, copyFile, realpath, stat, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, relative, isAbsolute } from 'node:path';
import { parsePlanning, evidencePath } from './planning.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const at = (path) => resolve(root, path);
const methodologyPath = 'metodologia/Marco_Trabajo_Datos_v1_4.md';
const readme = await readFile(at('README.md'), 'utf8');
const activities = parsePlanning(readme);
for (const activity of activities) {
  for (const evidence of activity.evidence) {
    const path = await realpath(at(evidencePath(evidence.url)));
    const localPath = relative(root, path);
    if (localPath.startsWith('..') || isAbsolute(localPath) || !(await stat(path)).isFile()) {
      throw new Error(`La evidencia debe ser un archivo dentro del repositorio: ${evidence.label}`);
    }
  }
}
await Promise.all(['src/data', 'public/descargas'].map((path) => mkdir(at(path), { recursive: true })));
// Elimina únicamente la página derivada que generaba la versión anterior del sitio.
await rm(at('src/content/docs/metodologia.md'), { force: true });
await Promise.all([
  writeFile(at('src/data/planning.json'), JSON.stringify({ source: 'README.md', activities }, null, 2) + '\n'),
  copyFile(at(methodologyPath), at('public/descargas/Marco_Trabajo_Datos_v1_4.md')),
  copyFile(at('planificacion/Planificacion.xlsx'), at('public/descargas/Planificacion.xlsx'))
]);
console.log(`Planificación sincronizada: ${activities.length} actividades, evidencias verificadas y descargas originales.`);
