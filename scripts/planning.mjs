const months = { ene: 1, feb: 2, mar: 3, abr: 4, may: 5, jun: 6, jul: 7, ago: 8, sep: 9, oct: 10, nov: 11, dic: 12 };
const repositoryRoot = 'https://github.com/Monsalves/data-lens/blob/main/';

export function evidencePath(url) {
  const resolved = new URL(url);
  if (!resolved.href.startsWith(repositoryRoot) || resolved.search || resolved.hash) {
    throw new Error(`La evidencia debe apuntar a un archivo de este repositorio: ${url}`);
  }
  const path = decodeURIComponent(resolved.pathname.slice(new URL(repositoryRoot).pathname.length));
  if (!path || path.includes('\\') || path.includes('\0') || path.split('/').some((part) => !part || part === '.' || part === '..')) {
    throw new Error(`Ruta de evidencia inválida: ${url}`);
  }
  return path;
}

function datePart(value) {
  const match = value.trim().match(/^(\d{1,2})(?:\s+([a-z]{3}))?(?:\s+(\d{4}))?$/u);
  if (!match || (match[2] && !months[match[2]])) throw new Error(`Fecha no reconocida: ${value}`);
  return { day: Number(match[1]), month: months[match[2]], year: match[3] ? Number(match[3]) : undefined };
}

function iso({ day, month, year }) {
  if (!month || !year) throw new Error('Falta mes o año en el intervalo.');
  const value = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  if (new Date(`${value}T00:00:00Z`).toISOString().slice(0, 10) !== value) throw new Error(`Fecha inválida: ${value}`);
  return value;
}

export function parseDates(value) {
  const parts = value.split(/[–—]/u);
  if (parts.length !== 2) throw new Error(`Intervalo no reconocido: ${value}`);
  const left = datePart(parts[0]);
  const right = datePart(parts[1]);
  right.month ??= left.month;
  right.year ??= left.year;
  left.month ??= right.month;
  left.year ??= right.year ? right.year - (left.month > right.month ? 1 : 0) : undefined;
  const start = iso(left);
  const end = iso(right);
  if (end < start) throw new Error(`Intervalo invertido: ${value}`);
  return { start, end };
}

export function parsePlanning(markdown) {
  const rows = markdown.split(/\r?\n/u).filter((line) => /^\|\s*S\d+\s*\|/u.test(line));
  if (!rows.length) throw new Error('El README no contiene actividades semanales.');
  const seen = new Set();
  return rows.map((line) => {
    const cells = line.trim().slice(1, -1).split(/(?<!\\)\|/u).map((cell) => cell.trim().replaceAll('\\|', '|'));
    if (cells.length !== 6) throw new Error(`La actividad requiere seis columnas: ${line}`);
    const [week, dates, activity, deliverable, rawStatus, rawEvidence] = cells;
    const activityKey = `${week}:${activity}`;
    if (seen.has(activityKey)) throw new Error(`Actividad duplicada en ${week}: ${activity}`);
    seen.add(activityKey);
    const statusKey = /en progreso|en curso/iu.test(rawStatus) ? 'progress'
      : /bloquead/iu.test(rawStatus) ? 'blocked'
      : /pendiente/iu.test(rawStatus) ? 'pending'
      : /terminad|completad/iu.test(rawStatus) ? 'done' : null;
    if (!statusKey) throw new Error(`Estado no reconocido: ${rawStatus}`);
    const status = { progress: 'En progreso', blocked: 'Bloqueado', pending: 'Pendiente', done: 'Terminado' }[statusKey];
    const evidence = [...rawEvidence.matchAll(/\[([^\]]+)\]\(([^)]+)\)/gu)].map(([, label, url]) => {
      const resolved = new URL(url, repositoryRoot);
      if (!resolved.href.startsWith(repositoryRoot) || url.startsWith('/') || url.includes('\\')) {
        throw new Error(`La evidencia debe apuntar a un archivo de este repositorio: ${url}`);
      }
      evidencePath(resolved.href);
      return { label, url: resolved.href };
    });
    if (rawEvidence !== '—' && !evidence.length) throw new Error(`Evidencia sin enlace reconocible: ${rawEvidence}`);
    return { week, dates, ...parseDates(dates), activity, deliverable, status, statusKey, evidence };
  });
}
