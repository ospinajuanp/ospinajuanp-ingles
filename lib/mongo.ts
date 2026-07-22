import { MongoClient, type Db } from 'mongodb'

const MONGODB_URI = process.env.MONGODB_URI

let cachedClient: MongoClient | null = null

export async function getMongoClient(): Promise<MongoClient> {
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

export async function getDb(name: string = 'ingles-db'): Promise<Db> {
  const client = await getMongoClient()
  return client.db(name)
}
