import { z } from 'zod'
import { getDb } from '@/lib/mongo'

const ParBilingueSchema = z.object({
  ing: z.string(),
  esp: z.string(),
})

const ConjugacionesSchema = z.object({
  infinitivo: ParBilingueSchema.optional(),
  pasadoSimple: ParBilingueSchema.optional(),
  participio: ParBilingueSchema.optional(),
  gerundio: ParBilingueSchema.optional(),
  futuro: ParBilingueSchema.optional(),
  condicional: ParBilingueSchema.optional(),
})

export const VerbSyncSchema = z.object({
  id: z.number().int().positive(),
  infinitivo: ParBilingueSchema,
  pasadoSimple: ParBilingueSchema.optional(),
  participio: ParBilingueSchema.optional(),
  gerundio: ParBilingueSchema.optional(),
  futuro: ParBilingueSchema.optional(),
  condicional: ParBilingueSchema.optional(),
  conjugaciones: ConjugacionesSchema.optional(),
  tips: z.string().optional(),
  imagen: z.string().url().optional(),
  imagen_url: z.string().url().optional(),
  image_source: z.enum(['custom', 'pexels', 'picsum', 'svg']).optional(),
  audio_url: z.string().url().nullable().optional(),
  audio_source: z.enum(['dictionaryapi.dev', 'tts', 'none']).optional(),
  categoria: z.string().optional(),
  categoria_principal: z.string().optional(),
  migrado_desde: z.string().optional(),
})

export type VerbSyncPayload = z.infer<typeof VerbSyncSchema>

export interface VerbSyncResult {
  id: number
  contador_consultas: number
  wasInsert: boolean
}

export async function upsertVerb(payload: VerbSyncPayload): Promise<VerbSyncResult> {
  const db = await getDb()
  const collection = db.collection('verbos')
  await collection.createIndexes([
    { key: { id: 1 }, unique: true, name: 'id_unique' },
    { key: { ultima_vez_visto: -1 }, name: 'last_seen_desc' },
  ])

  const { id, migrado_desde: migrado, ...rest } = payload
  const migrado_desde =
    typeof migrado === 'string' ? migrado : 'SPA_Lazy_Migration'

  const safeId = Number(id)
  const now = new Date()

  const result = await collection.findOneAndUpdate(
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

  const contador_consultas =
    typeof result?.contador_consultas === 'number' ? result.contador_consultas : 1

  return {
    id: safeId,
    contador_consultas,
    wasInsert: Boolean(result?.createdAt && result.createdAt.getTime() === now.getTime()),
  }
}
