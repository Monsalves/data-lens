import { lineageNodes, lineageEdges, populationFor } from './fixtures.js'

// Match complete identifiers in the fixture's known record formats, never substrings.
export function recordsForAsset(asset, metric) {
  const rows = populationFor(metric)
  switch (metric.id) {
    case 'M-01': return rows.filter(row => row.id === asset.id)
    case 'M-04': return rows.filter(row => row.detail.split(' · ').at(-1) === asset.name)
    case 'M-07':
    case 'M-11':
    case 'M-26': return rows.filter(row => row.detail.split(' · ')[0] === asset.name)
    case 'M-18': return rows.filter(row => row.detail === `Regla DQDL en ${asset.name}`)
    case 'M-09': {
      const node = lineageNodes.find(item => item.name === asset.name)
      const ids = new Set(node ? lineageEdges.filter(edge => edge.from === node.id || edge.to === node.id).map(edge => edge.id) : [])
      return rows.filter(row => ids.has(row.id))
    }
    default: return []
  }
}

export function assessmentsForAssets(assets, metrics) {
  return metrics.filter(metric => ['M-01', 'M-04', 'M-07', 'M-09', 'M-11', 'M-18', 'M-26'].includes(metric.id)).map(metric => {
    const unique = new Map()
    for (const asset of assets) {
      for (const row of recordsForAsset(asset, metric)) {
        if (!unique.has(row.id)) unique.set(row.id, { ...row, assets: [] })
        unique.get(row.id).assets.push(asset.name)
      }
    }
    return { metric, records: [...unique.values()] }
  }).filter(group => group.records.length)
}

export function recordsForBucket(bucket, metric) {
  if (metric.id === 'M-29') return populationFor(metric).filter(row => row.name === bucket.name)
  if (metric.id === 'M-22') return populationFor(metric).filter(row => row.detail.split(' · ')[0] === bucket.name)
  return []
}
