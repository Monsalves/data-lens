import { readFile, writeFile, mkdir, copyFile, realpath, stat, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, relative, isAbsolute } from 'node:path';
import { parsePlanning, evidencePath } from './planning.mjs';
import { readExcelPreview } from './excel-preview.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const at = (path) => resolve(root, path);
const methodologyPath = 'metodologia/Marco_Trabajo_Datos_v1_4.md';
const awsDocPath = 'investigacion/Servicios_AWS_S03_borrador.md';
const templatePath = 'metodologia/Plantilla_Assessment_Datos_F0_F3.xlsx';
const metricsDiagramPath = 'investigacion/Diagrama_Metricas_Piloto_13.html';
const readme = await readFile(at('README.md'), 'utf8');
const activities = parsePlanning(readme);
const templatePreview = await readExcelPreview(at(templatePath));
const planningPreview = await readExcelPreview(at('planificacion/Planificacion.xlsx'));
if (templatePreview.sheets.map((sheet) => sheet.name).join('|') !== 'Guía de uso|F0|F1|F2|F3|Matriz') {
  throw new Error('La plantilla Excel no contiene las seis hojas esperadas.');
}
const metricsDiagram = await readFile(at(metricsDiagramPath), 'utf8');
const diagramStyle = metricsDiagram.match(/<style id="mp-styles">([\s\S]*?)<\/style>/u)?.[1];
const diagramMarkup = metricsDiagram.match(/<!--mp:start-->([\s\S]*?)<!--mp:end-->/u)?.[1]
  ?.replace(/<!--mp:intro-start-->[\s\S]*?<!--mp:intro-end-->/u, '');
const diagramScript = metricsDiagram.match(/<script>([\s\S]*?)<\/script>/u)?.[1];
if (!diagramStyle || !diagramMarkup || !diagramScript) throw new Error('El diagrama de métricas no tiene estilos, estructura o script reconocibles.');
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
  writeFile(at('src/data/metricas-piloto.json'), JSON.stringify({ style: diagramStyle, markup: diagramMarkup, script: diagramScript }) + '\n'),
  copyFile(at(metricsDiagramPath), at('public/descargas/Diagrama_Metricas_Piloto_13.html')),
  writeFile(at('src/data/template-preview.json'), JSON.stringify(templatePreview) + '\n'),
  writeFile(at('src/data/planning-preview.json'), JSON.stringify(planningPreview) + '\n'),
  copyFile(at(methodologyPath), at('public/descargas/Marco_Trabajo_Datos_v1_4.md')),
  copyFile(at(awsDocPath), at('public/descargas/Servicios_AWS_S03_borrador.md')),
  copyFile(at(templatePath), at('public/descargas/Plantilla_Assessment_Datos_F0_F3.xlsx')),
  copyFile(at('planificacion/Planificacion.xlsx'), at('public/descargas/Planificacion.xlsx'))
]);
console.log(`Planificación sincronizada: ${activities.length} actividades, evidencias verificadas y descargas originales.`);
