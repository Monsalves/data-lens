import { copyFile, mkdir, readFile } from 'node:fs/promises';

const metricsPath = new URL('../prototipo/frontend/src/data/metrics.json', import.meta.url);
const pilot = new URL('../dist/piloto/', import.meta.url);
const entry = new URL('index.html', pilot);
const metrics = JSON.parse(await readFile(metricsPath, 'utf8'));

// Pages necesita un archivo para servir cada ruta cuando se abre o se recarga.
for (const { id } of metrics) {
  if (!/^M-\d{2}$/.test(id)) throw new Error(`Identificador de métrica inválido: ${id}`);
  const route = new URL(`metricas/${id}/`, pilot);
  await mkdir(route, { recursive: true });
  await copyFile(entry, new URL('index.html', route));
}
