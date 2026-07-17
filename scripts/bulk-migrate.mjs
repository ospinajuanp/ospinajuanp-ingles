import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const PROJECT_ROOT = path.resolve(__dirname, '..')
const JSON_PATH = path.join(PROJECT_ROOT, 'verbos_estructura.json')
const ENDPOINT =
  process.env.MIGRATE_ENDPOINT ?? 'http://localhost:5173/api/verbs/sync'
const RATE_LIMIT_MS = 100 // 10 req/sec
const BATCH_LOG = 100

function flattenVerbos(data) {
  const out = []
  const isVerbArray = (n) =>
    Array.isArray(n) && n.length > 0 && n[0]?.infinitivo
  const walk = (node, p) => {
    if (Array.isArray(node)) {
      if (isVerbArray(node)) {
        const [category, subcategory = null] = p
        for (const verb of node) {
          if (verb.infinitivo?.ing?.trim()) {
            out.push({ verb, category, subcategory })
          }
        }
      }
      return
    }
    if (node && typeof node === 'object') {
      for (const [k, v] of Object.entries(node)) walk(v, [...p, k])
    }
  }
  walk(data, [])
  return out
}

function picsumUrl(slug) {
  return `https://picsum.photos/seed/${encodeURIComponent(slug)}/800/400`
}

function buildPayload(item) {
  const { verb, category, subcategory } = item
  const slug = verb.infinitivo.ing
  return {
    ...verb,
    category,
    subcategory,
    imagen_url: picsumUrl(slug),
    image_source: 'picsum',
    audio_url: null,
    audio_source: 'pending',
    migrado_desde: 'SPA_Bulk_Migration',
  }
}

async function upsertOne(payload) {
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`)
  return res.json()
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

async function main() {
  if (!fs.existsSync(JSON_PATH)) {
    console.error(`[bulk-migrate] FATAL: ${JSON_PATH} not found`)
    process.exit(1)
  }

  console.log(`[bulk-migrate] reading ${JSON_PATH}…`)
  const data = JSON.parse(fs.readFileSync(JSON_PATH, 'utf-8'))
  const flat = flattenVerbos(data)
  console.log(`[bulk-migrate] flattened: ${flat.length} verbs`)
  console.log(`[bulk-migrate] endpoint:   ${ENDPOINT}`)
  console.log(
    `[bulk-migrate] rate limit: ${(1000 / RATE_LIMIT_MS).toFixed(1)}/sec`,
  )

  let inserted = 0
  let updated = 0
  let errors = 0
  const start = Date.now()

  for (let i = 0; i < flat.length; i++) {
    const payload = buildPayload(flat[i])
    try {
      const result = await upsertOne(payload)
      if (result.wasInsert) inserted++
      else updated++
    } catch (err) {
      errors++
      console.error(
        `[bulk-migrate] error on id=${payload.id} (${payload.infinitivo?.ing}):`,
        err.message,
      )
    }

    if ((i + 1) % BATCH_LOG === 0 || i === flat.length - 1) {
      const elapsed = ((Date.now() - start) / 1000).toFixed(1)
      console.log(
        `[bulk-migrate] ${i + 1}/${flat.length} — inserted: ${inserted}, updated: ${updated}, errors: ${errors}, elapsed: ${elapsed}s`,
      )
    }

    await sleep(RATE_LIMIT_MS)
  }

  const elapsed = ((Date.now() - start) / 1000).toFixed(1)
  console.log(
    `[bulk-migrate] DONE in ${elapsed}s — inserted: ${inserted}, updated: ${updated}, errors: ${errors}`,
  )
}

main().catch((err) => {
  console.error('[bulk-migrate] fatal:', err)
  process.exit(1)
})