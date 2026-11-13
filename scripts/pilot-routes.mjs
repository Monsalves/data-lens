import { copyFile, mkdir, readFile } from 'node:fs/promises';

const versions = [
  { source: 'frontend', route: 'piloto' },
  { source: 'frontend-v2', route: 'piloto-v2' },
];

// Pages necesita un archivo para servir cada ruta cuando se abre o se recarga.
for (const { source, route } of versions) {
  const metricsPath = new URL(`../prototipo/${source}/src/data/metrics.json`, import.meta.url);
  const pilot = new URL(`../dist/${route}/`, import.meta.url);
  const entry = new URL('index.html', pilot);
  const metrics = JSON.parse(await readFile(metricsPath, 'utf8'));
  for (const { id } of metrics) {
    if (!/^M-\d{2}$/.test(id)) throw new Error(`Identificador de métrica inválido: ${id}`);
    const detail = new URL(`metricas/${id}/`, pilot);
    await mkdir(detail, { recursive: true });
    await copyFile(entry, new URL('index.html', detail));
  }
}
