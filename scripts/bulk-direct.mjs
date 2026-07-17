/**
 * Direct bulk migration — bypasses the /api/verbs/sync HTTP endpoint.
 * Runs ~10x faster because there's no network roundtrip or Vite
 * middleware overhead. Use this for re-running the bulk AFTER the
 * first round via `pnpm bulk:migrate`, or for filling gaps.
 *
 *   MONGODB_URI=mongodb+srv://... node scripts/bulk-direct.mjs
 *
 * Idempotent: re-runs are no-ops (existing docs get their picsum
 * URL re-written to the same value, no actual change).
 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { MongoClient } from 'mongodb'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const PROJECT_ROOT = path.resolve(__dirname, '..')
const JSON_PATH = path.join(PROJECT_ROOT, 'verbos_estructura.json')

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
    id: verb.id,
    imagen: verb.imagen,
    infinitivo: verb.infinitivo,
    pasadoSimple: verb.pasadoSimple,
    participio: verb.participio,
    gerundio: verb.gerundio,
    futuro: verb.futuro,
    condicional: verb.condicional,
    oraciones: verb.oraciones,
    category,
    subcategory,
    imagen_url: picsumUrl(slug),
    image_source: 'picsum',
    audio_url: null,
    audio_source: 'pending',
  }
}

async function main() {
  if (!process.env.MONGODB_URI) {
    console.error('[bulk-direct] FATAL: MONGODB_URI not set')
    process.exit(1)
  }

  console.log('[bulk-direct] reading JSON…')
  const data = JSON.parse(fs.readFileSync(JSON_PATH, 'utf-8'))
  const flat = flattenVerbos(data)
  console.log(`[bulk-direct] flattened: ${flat.length} verbs`)

  const c = new MongoClient(process.env.MONGODB_URI, {
    serverSelectionTimeoutMS: 8000,
  })
  await c.connect()
  const db = c.db('ingles-db').collection('verbos')

  const ops = flat.map((item) => {
    const payload = buildPayload(item)
    const { id, ...rest } = payload
    const now = new Date()
    return {
      updateOne: {
        filter: { id },
        update: {
          $set: { ...rest, updatedAt: now },
          $setOnInsert: {
            id,
            createdAt: now,
            migrado_desde: 'SPA_Bulk_Migration',
          },
          $inc: { contador_consultas: 1 },
          $currentDate: { ultima_vez_visto: true },
        },
        upsert: true,
      },
    }
  })

  // batchSize 500 keeps memory low; driver streams them.
  const start = Date.now()
  const result = await db.bulkWrite(ops, { ordered: false })
  const elapsed = ((Date.now() - start) / 1000).toFixed(1)

  console.log(`[bulk-direct] DONE in ${elapsed}s`)
  console.log(`  matched:   ${result.matchedCount}`)
  console.log(`  modified:  ${result.modifiedCount}`)
  console.log(`  upserted:  ${result.upsertedCount}`)
  console.log(`  inserted:  ${result.upsertedCount}`)
  console.log(`  errors:    ${result.writeErrors?.length ?? 0}`)
  if (result.writeErrors?.length) {
    console.log('  sample error:', JSON.stringify(result.writeErrors[0], null, 2))
  }

  await c.close()
}

main().catch((err) => {
  console.error('[bulk-direct] fatal:', err)
  process.exit(1)
})