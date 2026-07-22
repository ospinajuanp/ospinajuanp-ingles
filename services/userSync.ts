import { z } from 'zod'
import { getDb } from '@/lib/mongo'

export const THEME_IDS = ['light', 'dark', 'dracula', 'cupcake'] as const

const SRS_VERSION = 1
const MAX_SRS_BYTES = 256 * 1024

export const SrsCardSchema = z.object({
  type: z.enum(['custom', 'verb']),
  id: z.string(),
  front: z
    .object({
      es: z.string(),
      en: z.string(),
    })
    .optional(),
  verbKey: z.string().optional(),
  verbId: z.number().nullable().optional(),
  infinitivo: z
    .object({
      ing: z.string(),
      esp: z.string(),
    })
    .optional(),
  srs: z
    .object({
      interval: z.number(),
      ef: z.number(),
      repetitions: z.number().optional(),
      nextReview: z.number().optional(),
      lastReviewed: z.number().optional(),
    })
    .optional(),
  createdAt: z.number().optional(),
})

export const SrsStoreSchema = z.object({
  version: z.literal(SRS_VERSION),
  cards: z.record(z.string(), SrsCardSchema),
  order: z.array(z.string()),
})

const TOKEN_RE =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

const TokenSchema = z
  .string()
  .regex(TOKEN_RE, 'Invalid syncToken (must be UUIDv4)')

export const UserSyncGetSchema = z.object({
  token: TokenSchema,
})

export const UserSyncPostSchema = z.object({
  syncToken: TokenSchema,
  srsStore: SrsStoreSchema.refine(
    (s) => {
      try {
        const bytes = Buffer.byteLength(JSON.stringify(s), 'utf-8')
        return bytes <= MAX_SRS_BYTES
      } catch {
        return false
      }
    },
    { message: `srsStore exceeds ${MAX_SRS_BYTES} bytes` },
  ),
  theme: z.enum(THEME_IDS).nullable().optional(),
})

export type UserSyncPostPayload = z.infer<typeof UserSyncPostSchema>

export interface UserStateRecord {
  syncToken: string
  createdAt: Date
  lastActiveAt: Date
  srsStore: z.infer<typeof SrsStoreSchema> | null
  theme: string | null
}

export async function getUserState(token: string): Promise<UserStateRecord | null> {
  const db = await getDb()
  const collection = db.collection<UserStateRecord>('user_sync')
  await collection.createIndexes([
    { key: { syncToken: 1 }, unique: true, name: 'syncToken_unique' },
    { key: { lastActiveAt: -1 }, name: 'lastActive_desc' },
  ])

  const doc = await collection.findOneAndUpdate(
    { syncToken: token },
    { $currentDate: { lastActiveAt: true } },
    { returnDocument: 'after' },
  )

  return doc ?? null
}

export interface UpsertResult {
  wasInsert: boolean
  lastActiveAt: Date
}

export async function upsertUserState(
  payload: UserSyncPostPayload,
): Promise<UpsertResult> {
  const db = await getDb()
  const collection = db.collection<UserStateRecord>('user_sync')
  await collection.createIndexes([
    { key: { syncToken: 1 }, unique: true, name: 'syncToken_unique' },
  ])

  const now = new Date()
  const update: Record<string, unknown> = {
    $set: {
      syncToken: payload.syncToken,
      srsStore: payload.srsStore,
    },
    $setOnInsert: { createdAt: now },
    $currentDate: { lastActiveAt: true },
  }
  if (payload.theme != null) {
    const set = update.$set as Record<string, unknown>
    set.theme = payload.theme
  }

  const result = await collection.findOneAndUpdate(
    { syncToken: payload.syncToken },
    update,
    { upsert: true, returnDocument: 'after' },
  )

  const wasInsert = Boolean(
    result &&
      result.createdAt &&
      Math.abs(result.createdAt.getTime() - now.getTime()) < 1500,
  )

  return {
    wasInsert,
    lastActiveAt: result?.lastActiveAt ?? now,
  }
}
