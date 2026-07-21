// Serverless handler for the anonymous multi-device sync slot.
//
// Collection: ingles-db.user_sync
// Document shape:
//
//   {
//     _id: ObjectId,
//     syncToken: "UUIDv4 (indexed, unique)",
//     createdAt: ISODate,           // stamped once on first upsert
//     lastActiveAt: ISODate,        // bumped on every GET/POST
//     srsStore: { ... copia de ospinajuanp-ingles:srs:v1 ... },
//     theme: "light|dark|dracula|cupcake"
//   }
//
// Routes:
//   GET  /api/sync/user?token=…      → 200 { ok, state } | 200 { ok, state: null }
//   POST /api/sync/user {syncToken, srsStore, theme}
//                                       → 200 { ok, wasInsert }
//
// Why a dedicated collection (not `verbos`):
//   - Verb payloads and user-sync snapshots have very different access
//     patterns. Mixing them inflates document count and confuses
//     indexing. Each gets its own collection, its own indexes.
//   - A unique index on `syncToken` gives us atomic upserts AND
//     free de-duplication if a buggy client ever POSTs the same token
//     twice.
//
// Why we trust client-supplied `srsStore`/`theme`:
//   - The whole model is anonymous + client-owned. There is no auth,
//     so any "validation" would be theatre. We still cap the document
//     size to keep one malicious payload from filling the cluster.

import { MongoClient } from 'mongodb'

const MONGODB_URI = process.env.MONGODB_URI
const DB_NAME = 'ingles-db'
const COLLECTION = 'user_sync'

// 256 KB per document. Mongo's hard limit is 16 MB; we stay well under
// because the SRS store is bounded by the number of cards the user has
// personally added (typically <1000) and is JSON-serialised once.
const MAX_SRS_BYTES = 256 * 1024

let cachedClient = null

async function connect() {
  if (cachedClient) return cachedClient
  if (!MONGODB_URI) throw new Error('MONGODB_URI not set')
  const client = new MongoClient(MONGODB_URI, {
    serverSelectionTimeoutMS: 8000,
    maxPoolSize: 10,
    retryWrites: true,
  })
  await client.connect()
  cachedClient = client
  return client
}

async function ensureIndexes(db) {
  await db.collection(COLLECTION).createIndexes([
    { key: { syncToken: 1 }, unique: true, name: 'syncToken_unique' },
    { key: { lastActiveAt: -1 }, name: 'lastActive_desc' },
  ])
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = []
    let total = 0
    req.on('data', (c) => {
      total += c.length
      if (total > MAX_SRS_BYTES * 2) {
        // Reject early — even before parsing — to avoid buffering a
        // malicious megabyte payload in memory.
        const err = new Error('Payload too large')
        err.statusCode = 413
        req.destroy(err)
        reject(err)
        return
      }
      chunks.push(c)
    })
    req.on('end', () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString('utf-8')))
      } catch (err) {
        reject(err)
      }
    })
    req.on('error', reject)
  })
}

function sendJson(res, status, payload) {
  res.statusCode = status
  res.setHeader('content-type', 'application/json')
  res.setHeader('cache-control', 'no-store')
  res.end(JSON.stringify(payload))
}

const TOKEN_RE =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

function isValidToken(token) {
  return typeof token === 'string' && TOKEN_RE.test(token)
}

function isValidSrsStore(store) {
  if (store == null) return false
  if (typeof store !== 'object') return false
  if (store.version !== 1) return false
  if (!store.cards || typeof store.cards !== 'object') return false
  if (!Array.isArray(store.order)) return false
  // Optional size cap to keep individual updates cheap.
  try {
    const bytes = Buffer.byteLength(JSON.stringify(store), 'utf-8')
    return bytes <= MAX_SRS_BYTES
  } catch {
    return false
  }
}

const ALLOWED_THEMES = new Set(['light', 'dark', 'dracula', 'cupcake'])

async function handleGet(req, res, url) {
  const token = url.searchParams.get('token')
  if (!isValidToken(token)) {
    return sendJson(res, 400, { ok: false, error: 'Invalid token' })
  }
  const client = await connect()
  const db = client.db(DB_NAME)
  await ensureIndexes(db)

  const doc = await db
    .collection(COLLECTION)
    .findOneAndUpdate(
      { syncToken: token },
      { $currentDate: { lastActiveAt: true } },
      { returnDocument: 'after' },
    )

  if (!doc) {
    return sendJson(res, 200, { ok: true, state: null })
  }
  return sendJson(res, 200, {
    ok: true,
    state: {
      syncToken: doc.syncToken,
      createdAt: doc.createdAt,
      lastActiveAt: doc.lastActiveAt,
      srsStore: doc.srsStore ?? null,
      theme: doc.theme ?? null,
    },
  })
}

async function handlePost(req, res) {
  const body = await readJsonBody(req)
  const { syncToken, srsStore, theme } = body ?? {}

  if (!isValidToken(syncToken)) {
    return sendJson(res, 400, { ok: false, error: 'Invalid syncToken' })
  }
  if (!isValidSrsStore(srsStore)) {
    return sendJson(res, 400, { ok: false, error: 'Invalid srsStore' })
  }
  if (theme != null && !ALLOWED_THEMES.has(theme)) {
    return sendJson(res, 400, { ok: false, error: 'Invalid theme' })
  }

  const client = await connect()
  const db = client.db(DB_NAME)
  await ensureIndexes(db)

  const now = new Date()

  const update = {
    $set: {
      syncToken,
      srsStore,
      ...(theme != null ? { theme } : {}),
    },
    $setOnInsert: { createdAt: now },
    $currentDate: { lastActiveAt: true },
  }

  const result = await db.collection(COLLECTION).findOneAndUpdate(
    { syncToken },
    update,
    { upsert: true, returnDocument: 'after' },
  )

  const wasInsert = !!(
    result &&
    result.createdAt &&
    Math.abs(result.createdAt.getTime() - now.getTime()) < 1500
  )

  return sendJson(res, 200, {
    ok: true,
    wasInsert,
    lastActiveAt: result?.lastActiveAt ?? now,
  })
}

export default async function handler(req, res) {
  try {
    const url = new URL(req.url, 'http://localhost')
    if (req.method === 'GET') {
      return await handleGet(req, res, url)
    }
    if (req.method === 'POST') {
      return await handlePost(req, res)
    }
    return sendJson(res, 405, { ok: false, error: 'Method not allowed' })
  } catch (err) {
    console.error('[api/sync/user]', err)
    const status = err.statusCode ?? 500
    return sendJson(res, status, { ok: false, error: err.message })
  }
}