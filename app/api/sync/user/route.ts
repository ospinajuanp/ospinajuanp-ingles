import { NextResponse } from 'next/server'
import { z } from 'zod'
import {
  UserSyncGetSchema,
  UserSyncPostSchema,
  getUserState,
  upsertUserState,
} from '@/services/userSync'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

const MAX_SRS_BYTES = 256 * 1024

function jsonError(message: string, status: number): Response {
  return NextResponse.json({ ok: false, error: message }, { status })
}

export async function GET(req: Request): Promise<Response> {
  const url = new URL(req.url)
  const parsed = UserSyncGetSchema.safeParse({ token: url.searchParams.get('token') })
  if (!parsed.success) {
    return jsonError('Invalid token', 400)
  }

  try {
    const doc = await getUserState(parsed.data.token)
    if (!doc) {
      return NextResponse.json({ ok: true, state: null }, { status: 200 })
    }
    return NextResponse.json(
      {
        ok: true,
        state: {
          syncToken: doc.syncToken,
          createdAt: doc.createdAt?.toISOString?.() ?? null,
          lastActiveAt: doc.lastActiveAt?.toISOString?.() ?? null,
          srsStore: doc.srsStore ?? null,
          theme: doc.theme ?? null,
        },
      },
      { status: 200 },
    )
  } catch (err) {
    console.error('[api/sync/user] GET', err)
    const message = err instanceof Error ? err.message : 'Internal error'
    const status = (err as { statusCode?: number })?.statusCode ?? 500
    return jsonError(message, status)
  }
}

export async function POST(req: Request): Promise<Response> {
  let body: unknown
  try {
    body = await req.json()
  } catch {
    return jsonError('Invalid JSON body', 400)
  }

  const parsed = UserSyncPostSchema.safeParse(body)
  if (!parsed.success) {
    return jsonError(parsed.error.issues[0]?.message ?? 'Invalid payload', 400)
  }

  try {
    const result = await upsertUserState(parsed.data)
    return NextResponse.json(
      {
        ok: true,
        wasInsert: result.wasInsert,
        lastActiveAt: result.lastActiveAt.toISOString(),
      },
      { status: 200 },
    )
  } catch (err) {
    console.error('[api/sync/user] POST', err)
    const message = err instanceof Error ? err.message : 'Internal error'
    const status = (err as { statusCode?: number })?.statusCode ?? 500
    if (message.toLowerCase().includes('payload too large')) {
      return jsonError(message, 413)
    }
    return jsonError(message, status)
  }
}

void MAX_SRS_BYTES
void z
