/**
 * Salin hasil pipeline Python (dashboard-streamlit/data/derived/) menjadi JSON statis
 * yang dibundel oleh Vite. Jalankan setelah `python dashboard-streamlit/analysis.py`.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const sourceDir = resolve(root, '../dashboard-streamlit/data/derived')
const outDir = resolve(root, 'src/data')

const FILES = {
  'kota-clean.csv': 'kota.json',
  'makro-clean.csv': 'makro.json',
  'industri-rank.csv': 'industri.json',
  'pain-priority.csv': 'pain.json',
  'trust-gap.csv': 'trust.json',
  'kompetitor-clean.csv': 'kompetitor.json',
  'kompetitor-by-city.csv': 'kompetitor-kota.json',
  'kompetitor-by-type.csv': 'kompetitor-tipe.json',
  'service-counts.csv': 'layanan-count.json',
  'service-matrix.csv': 'service-matrix.json',
  'layanan-supply.csv': 'layanan-supply.json',
  'harga-kompetitor.csv': 'harga-kompetitor.json',
  'platform-summary.csv': 'platform.json',
  'ecommerce-summary.csv': 'ecommerce.json',
  'biaya-iklan-clean.csv': 'biaya-iklan.json',
  'channel-matrix-clean.csv': 'channel-matrix.json',
  'layanan-winning.csv': 'layanan-winning.json',
  'layanan-industri.csv': 'layanan-industri.json',
  'layanan-addon.csv': 'layanan-addon.json',
  'impost-layanan.csv': 'impost-layanan.json',
  'sumber-clean.csv': 'sumber.json',
}

function parseCsv(text) {
  const rows = []
  let row = []
  let field = ''
  let quoted = false

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i]
    if (quoted) {
      if (char === '"' && text[i + 1] === '"') {
        field += '"'
        i += 1
      } else if (char === '"') {
        quoted = false
      } else {
        field += char
      }
    } else if (char === '"') {
      quoted = true
    } else if (char === ',') {
      row.push(field)
      field = ''
    } else if (char === '\n') {
      row.push(field)
      if (row.some((cell) => cell !== '')) rows.push(row)
      row = []
      field = ''
    } else if (char !== '\r') {
      field += char
    }
  }
  row.push(field)
  if (row.some((cell) => cell !== '')) rows.push(row)

  const [header, ...body] = rows
  return body.map((cells) =>
    Object.fromEntries(header.map((key, index) => [key.trim(), coerce(cells[index])])),
  )
}

function coerce(value) {
  if (value === '') return null
  if (value === 'True') return true
  if (value === 'False') return false
  if (/^-?\d+(\.\d+)?([eE][+-]?\d+)?$/.test(value)) return Number(value)
  return value
}

mkdirSync(outDir, { recursive: true })

for (const [input, output] of Object.entries(FILES)) {
  const csv = readFileSync(resolve(sourceDir, input), 'utf8').replace(/^\uFEFF/, '')
  const rows = parseCsv(csv)
  writeFileSync(resolve(outDir, output), JSON.stringify(rows))
  console.log(`${input} -> ${output} (${rows.length} baris)`)
}

writeFileSync(
  resolve(outDir, 'metrics.json'),
  readFileSync(resolve(sourceDir, 'metrics.json'), 'utf8').replace(/^\uFEFF/, ''),
)
console.log('metrics.json disalin')
