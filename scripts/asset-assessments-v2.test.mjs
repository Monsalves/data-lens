import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { assessmentsForAssets, recordsForAsset, recordsForBucket } from '../prototipo/frontend-v2/src/data/assetAssessments.js'
import { dataZoneAssets, otherAssets, populationFor } from '../prototipo/frontend-v2/src/data/fixtures.js'
const metrics = JSON.parse(readFileSync(new URL('../prototipo/frontend-v2/src/data/metrics.json', import.meta.url)))
const metric = id => metrics.find(m => m.id === id)
const orders = dataZoneAssets.find(a => a.table === 'pedidos_venta')
const clients = dataZoneAssets.find(a => a.table === 'maestro_clientes')

test('only explicit table references receive quality records', () => {
  assert.equal(recordsForAsset(orders, metric('M-11')).length, populationFor(metric('M-11')).length)
  assert.equal(recordsForAsset(clients, metric('M-11')).length, 0)
  const controls = recordsForAsset(orders, metric('M-18'))
  assert.ok(controls.length > 0)
  assert.ok(controls.length < populationFor(metric('M-18')).length)
  assert.ok(controls.every(r => r.detail === `Regla DQDL en ${orders.name}`))
  assert.equal(recordsForAsset({ ...orders, name: orders.name + '_archive' }, metric('M-11')).length, 0)
})

test('stable owner ID and complete catalog/classification names do not leak', () => {
  for (const asset of dataZoneAssets) {
    assert.deepEqual(recordsForAsset(asset, metric('M-01')).map(r => r.id), [asset.id])
    assert.equal(recordsForAsset(asset, metric('M-07')).length, 5)
    assert.equal(recordsForAsset(asset, metric('M-26')).length, 1)
    assert.equal(recordsForAsset(asset, metric('M-16')).length, 0)
  }
})

test('database grouping deduplicates shared lineage without mutating fixture records', () => {
  const before = JSON.stringify(populationFor(metric('M-09')))
  const groups = assessmentsForAssets(dataZoneAssets, metrics)
  const lineage = groups.find(g => g.metric.id === 'M-09')
  assert.equal(lineage.records.length, populationFor(metric('M-09')).length)
  assert.equal(new Set(lineage.records.map(r => r.id)).size, lineage.records.length)
  assert.ok(lineage.records.some(r => r.assets.length === 2))
  assert.equal(JSON.stringify(populationFor(metric('M-09'))), before)
  assert.ok(groups.every(g => !['M-16', 'M-21', 'M-22', 'M-25', 'M-27', 'M-29'].includes(g.metric.id)))
  assert.deepEqual(assessmentsForAssets([], metrics), [])
})

test('S3 controls match only the bucket named in each record', () => {
  const curated = otherAssets.find(asset => asset.id === 's3-bucket-002')
  const ingestion = otherAssets.find(asset => asset.id === 's3-bucket-001')
  assert.deepEqual(recordsForBucket(curated, metric('M-29')).map(row => row.id), ['BUCKET-002'])
  assert.deepEqual(recordsForBucket(ingestion, metric('M-29')).map(row => row.id), ['BUCKET-001'])
  assert.equal(recordsForBucket(curated, metric('M-22')).length, populationFor(metric('M-22')).length)
  assert.deepEqual(recordsForBucket(ingestion, metric('M-22')), [])
  for (const id of ['M-22', 'M-29']) {
    assert.deepEqual(recordsForBucket({ name: curated.name + '-backup' }, metric(id)), [])
  }
})
