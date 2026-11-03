import { readFile, writeFile, mkdir, copyFile, realpath, stat, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, relative, isAbsolute } from 'node:path';
import { parsePlanning, evidencePath } from './planning.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const at = (path) => resolve(root, path);
const methodologyPath = 'metodologia/Marco_Trabajo_Datos_v1_4.md';
const awsDocPath = 'investigacion/Servicios_AWS_S03_borrador.md';
const readme = await readFile(at('README.md'), 'utf8');
const activities = parsePlanning(readme);
const awsDoc = await readFile(at(awsDocPath), 'utf8');
const awsSection = awsDoc.split('## Mapa preliminar\n')[1]?.split('\n## ')[0] ?? '';
const awsRows = awsSection.split('\n').filter((line) => line.startsWith('| ') && !line.startsWith('| Pilar ') && !line.startsWith('| --- ')).map((line) => {
  const cells = line.slice(1, -1).split('|').map((cell) => cell.trim());
  if (cells.length !== 3 || !cells.every(Boolean)) throw new Error(`Fila incompleta del mapa AWS: ${line}`);
  const [pillar, dimension, services] = cells;
  return { pillar, dimension, services };
});
if (awsRows.length !== 13) throw new Error(`Se esperaban 13 dimensiones AWS; hay ${awsRows.length}`);
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
  writeFile(at('src/data/aws-map.json'), JSON.stringify(awsRows, null, 2) + '\n'),
  copyFile(at(methodologyPath), at('public/descargas/Marco_Trabajo_Datos_v1_4.md')),
  copyFile(at('planificacion/Planificacion.xlsx'), at('public/descargas/Planificacion.xlsx'))
]);
console.log(`Planificación sincronizada: ${activities.length} actividades, evidencias verificadas y descargas originales.`);
