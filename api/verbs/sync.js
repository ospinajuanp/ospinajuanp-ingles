import { MongoClient } from 'mongodb'

const MONGODB_URI = process.env.MONGODB_URI
const DB_NAME = 'ingles-db'
const COLLECTION = 'verbos'

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
    { key: { id: 1 }, unique: true, name: 'id_unique' },
    { key: { ultima_vez_visto: -1 }, name: 'last_seen_desc' },
  ])
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = []
    req.on('data', (c) => chunks.push(c))
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

export async function syncVerb(verb) {
  if (!verb || typeof verb !== 'object' || verb.id == null) {
    const err = new Error('Invalid verb payload (missing id)')
    err.statusCode = 400
    throw err
  }

  const client = await connect()
  const db = client.db(DB_NAME)
  await ensureIndexes(db)

  const { id, ...rest } = verb

  // migrado_desde: lo aporta el cliente (o default). NO va en $set
  // para que un update no sobrescriba el marker original — solo se
  // estampa via $setOnInsert en inserts.
  const migrado_desde =
    typeof rest.migrado_desde === 'string'
      ? rest.migrado_desde
      : 'SPA_Lazy_Migration'
  delete rest.migrado_desde

  const safeId = Number(id)
  const now = new Date()

  const result = await db.collection(COLLECTION).findOneAndUpdate(
    { id: safeId },
    {
      $set: { ...rest, updatedAt: now },
      $setOnInsert: {
        id: safeId,
        createdAt: now,
        migrado_desde,
      },
      $inc: { contador_consultas: 1 },
      $currentDate: { ultima_vez_visto: true },
    },
    { upsert: true, returnDocument: 'after' },
  )

  return {
    id: safeId,
    contador_consultas: result?.contador_consultas ?? 1,
    wasInsert: !!result?.createdAt && result.createdAt.getTime() === now.getTime(),
  }
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return sendJson(res, 405, { error: 'Method not allowed' })
  }
  try {
    const verb = await readJsonBody(req)
    const result = await syncVerb(verb)
    return sendJson(res, 200, { ok: true, ...result })
  } catch (err) {
    console.error('[api/verbs/sync]', err)
    const status = err.statusCode ?? 500
    return sendJson(res, status, { ok: false, error: err.message })
  }
}