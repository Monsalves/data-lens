import ExcelJS from 'exceljs';
import JSZip from 'jszip';
import { readFile } from 'node:fs/promises';

function columnNumber(letters) {
  return [...letters].reduce((value, letter) => value * 26 + letter.charCodeAt(0) - 64, 0);
}

function color(value) {
  const argb = value?.argb;
  return typeof argb === 'string' && /^[0-9a-f]{8}$/i.test(argb) && argb.slice(0, 2).toUpperCase() === 'FF'
    ? `#${argb.slice(2)}` : undefined;
}

export async function readExcelPreview(path) {
  const workbook = new ExcelJS.Workbook();
  // Normaliza el prefijo XML que usa la exportación del anexo; solo afecta la copia de lectura.
  const zip = await JSZip.loadAsync(await readFile(path));
  for (const name of Object.keys(zip.files).filter((item) => item.endsWith('.xml'))) {
    let xml = await zip.file(name).async('string');
    xml = xml.replace(/xmlns:x="http:\/\/schemas\.openxmlformats\.org\/spreadsheetml\/2006\/main"/gu,
      'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"');
    xml = xml.replace(/<\/?x:/gu, (match) => match.replace('x:', ''));
    if (/^xl\/worksheets\/sheet\d+\.xml$/u.test(name)) xml = xml.replace(/<drawing\b[^>]*\/>/gu, '');
    zip.file(name, xml);
  }
  // Los dibujos no se muestran en la vista de celdas y ExcelJS no reconcilia uno de ellos.
  for (const name of Object.keys(zip.files).filter((item) => item.startsWith('xl/drawings/'))) zip.remove(name);
  for (const name of Object.keys(zip.files).filter((item) => /^xl\/worksheets\/_rels\/sheet\d+\.xml\.rels$/u.test(item))) {
    const xml = await zip.file(name).async('string');
    zip.file(name, xml.replace(/<Relationship\b[^>]*Type="[^"]*\/drawing"[^>]*\/>/gu, ''));
  }
  const types = await zip.file('[Content_Types].xml').async('string');
  zip.file('[Content_Types].xml', types.replace(/<Override\b[^>]*PartName="\/xl\/drawings\/[^"]+"[^>]*\/>/gu, ''));
  await workbook.xlsx.load(await zip.generateAsync({ type: 'nodebuffer' }));
  return {
    sheets: workbook.worksheets.map((sheet) => {
      const columns = Math.min(sheet.columnCount, 20);
      let lastContentRow = 0;
      for (let index = 1; index <= sheet.rowCount; index++) {
        for (let col = 1; col <= columns; col++) {
          if (sheet.getCell(index, col).text.trim()) lastContentRow = index;
        }
      }
      const maxRow = Math.min(100, Math.max(lastContentRow + 3, 16));
      const merged = new Map();
      const covered = new Set();
      for (const range of sheet.model.merges ?? []) {
        const match = /^([A-Z]+)(\d+):([A-Z]+)(\d+)$/i.exec(range);
        if (!match) continue;
        const left = columnNumber(match[1].toUpperCase());
        const top = Number(match[2]);
        const right = columnNumber(match[3].toUpperCase());
        const bottom = Number(match[4]);
        if (top > maxRow || left > columns) continue;
        merged.set(`${top}:${left}`, { colSpan: Math.min(right, columns) - left + 1, rowSpan: Math.min(bottom, maxRow) - top + 1 });
        for (let row = top; row <= Math.min(bottom, maxRow); row++) {
          for (let col = left; col <= Math.min(right, columns); col++) {
            if (row !== top || col !== left) covered.add(`${row}:${col}`);
          }
        }
      }
      const rows = Array.from({ length: maxRow }, (_, rowIndex) => {
        const row = rowIndex + 1;
        return Array.from({ length: columns }, (_, colIndex) => {
          const col = colIndex + 1;
          const key = `${row}:${col}`;
          if (covered.has(key)) return null;
          const cell = sheet.getCell(row, col);
          return {
            text: cell.text,
            bold: Boolean(cell.font?.bold),
            bg: color(cell.fill?.fgColor),
            fg: color(cell.font?.color),
            align: cell.alignment?.horizontal === 'center' ? 'center' : undefined,
            ...merged.get(key)
          };
        });
      });
      return { name: sheet.name, rows };
    })
  };
}
