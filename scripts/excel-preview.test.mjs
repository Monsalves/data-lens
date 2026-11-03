import test from 'node:test';
import assert from 'node:assert/strict';
import { readExcelPreview } from './excel-preview.mjs';

test('la previsualización se genera desde las seis hojas del Excel publicado', async () => {
  const path = new URL('../metodologia/Plantilla_Assessment_Datos_F0_F3.xlsx', import.meta.url).pathname;
  const preview = await readExcelPreview(path);
  assert.deepEqual(preview.sheets.map((sheet) => sheet.name), ['Guía de uso', 'F0', 'F1', 'F2', 'F3', 'Matriz']);
  assert.match(preview.sheets[1].rows[0][0].text, /^F0/);
  assert.match(preview.sheets[2].rows[3][0].text, /ID Examen/);
  assert.ok(preview.sheets.every((sheet) => sheet.rows.length < 100));
});
