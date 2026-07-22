import { NextResponse } from 'next/server'
import { z } from 'zod'
import { VerbSyncSchema, upsertVerb } from '@/services/verbSync'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

const ErrorResponseSchema = z.object({
  ok: z.literal(false),
  error: z.string(),
})

const SuccessResponseSchema = z.object({
  ok: z.literal(true),
  id: z.number(),
  contador_consultas: z.number(),
  wasInsert: z.boolean(),
})

export async function POST(req: Request): Promise<Response> {
  let body: unknown
  try {
    body = await req.json()
  } catch {
    return NextResponse.json(
      { ok: false, error: 'Invalid JSON body' },
      { status: 400 },
    )
  }

  const parsed = VerbSyncSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json(
      { ok: false, error: parsed.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('; ') },
      { status: 400 },
    )
  }

  try {
    const result = await upsertVerb(parsed.data)
    return NextResponse.json(
      {
        ok: true,
        id: result.id,
        contador_consultas: result.contador_consultas,
        wasInsert: result.wasInsert,
      },
      { status: 200 },
    )
  } catch (err) {
    console.error('[api/verbs/sync]', err)
    const message = err instanceof Error ? err.message : 'Internal error'
    return NextResponse.json({ ok: false, error: message }, { status: 500 })
  }
}

export async function GET(): Promise<Response> {
  return NextResponse.json({ ok: false, error: 'Method not allowed' }, { status: 405 })
}

void ErrorResponseSchema
void SuccessResponseSchema
