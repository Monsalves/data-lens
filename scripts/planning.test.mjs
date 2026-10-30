import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { parseDates, parsePlanning } from './planning.mjs';

test('interpreta intervalos con mes compartido y cambio de mes/año', () => {
  assert.deepEqual(parseDates('04–10 nov 2026'), { start: '2026-11-04', end: '2026-11-10' });
  assert.deepEqual(parseDates('27 oct–03 nov 2026'), { start: '2026-10-27', end: '2026-11-03' });
  assert.deepEqual(parseDates('30 dic 2026–05 ene 2027'), { start: '2026-12-30', end: '2027-01-05' });
});

test('rechaza fechas y estados que producirían un cronograma incorrecto', () => {
  assert.throws(() => parseDates('31–32 feb 2026'));
  assert.throws(() => parseDates('10–04 nov 2026'));
  assert.throws(() => parsePlanning('| S01 | 04–10 nov 2026 | Actividad | Resultado | Desconocido | — |'));
});

test('conserva actividades, estados y evidencia del README sin fijar el avance futuro', async () => {
  const markdown = await readFile(new URL('../README.md', import.meta.url), 'utf8');
  const rows = parsePlanning(markdown);
  assert.equal(rows.length, 14);
  const sourceRows = markdown.split('\n').filter((line) => /^\| S\d+ \|/.test(line));
  for (const [index, row] of rows.entries()) {
    assert.ok(sourceRows[index].includes(row.activity));
    assert.ok(sourceRows[index].includes(row.deliverable));
    assert.ok(sourceRows[index].includes(row.status));
  }
  assert.equal(rows.at(-1).end, '2027-02-02');
  assert.match(rows.find((row) => row.week === 'S08').deliverable, /18 dic/);
  assert.deepEqual(rows[0].evidence, [{ label: 'Marco de trabajo 1.4', url: 'metodologia/' }]);
});

test('admite cambiar el seguimiento a terminado sin alterar fechas', () => {
  const rows = parsePlanning('| S01 | 04–10 nov 2026 | Actividad | Entregable | 🟢 Terminado | — |');
  assert.equal(rows[0].statusKey, 'done');
  assert.equal(rows[0].start, '2026-11-04');
});
