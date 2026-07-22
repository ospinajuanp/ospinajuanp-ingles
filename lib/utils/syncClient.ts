import type { SrsStore } from '@/lib/types/srs'
import type { ThemeId } from '@/lib/types/theme'

const ENDPOINT = '/api/sync/user'
const REQUEST_TIMEOUT_MS = 8000

interface UserStateResponse {
  ok: boolean
  state?: {
    syncToken: string
    createdAt?: string
    lastActiveAt?: string
    srsStore: SrsStore | null
    theme: ThemeId | null
  } | null
}

function withTimeout(ms: number, controller: AbortController): () => void {
  const timer = setTimeout(() => controller.abort(), ms)
  return () => clearTimeout(timer)
}

async function parseJsonSafe(res: Response): Promise<unknown> {
  try {
    return await res.json()
  } catch {
    return null
  }
}

export type FetchUserStateResult =
  | { ok: true; state: UserStateResponse['state'] }
  | { ok: false; reason?: 'no-token' | 'network' | 'timeout'; status?: number; data?: unknown }

export async function fetchUserState(token: string): Promise<FetchUserStateResult> {
  if (!token) return { ok: false, reason: 'no-token' }
  const controller = new AbortController()
  const cancel = withTimeout(REQUEST_TIMEOUT_MS, controller)
  try {
    const res = await fetch(`${ENDPOINT}?token=${encodeURIComponent(token)}`, {
      method: 'GET',
      signal: controller.signal,
      cache: 'no-store',
    })
    const data = (await parseJsonSafe(res)) as UserStateResponse | null
    if (!res.ok || !data?.ok) {
      return { ok: false, status: res.status, data }
    }
    return { ok: true, state: data.state ?? null }
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err)
    const reason = err instanceof Error && err.name === 'AbortError' ? 'timeout' : 'network'
    console.warn('[sync-client] fetchUserState failed:', message)
    return { ok: false, reason }
  } finally {
    cancel()
  }
}

export interface PushUserStatePayload {
  syncToken: string
  srsStore: SrsStore
  theme?: ThemeId | null
}

export type PushUserStateResult =
  | { ok: true; data?: unknown }
  | { ok: false; reason?: 'no-token' | 'network' | 'timeout'; status?: number; data?: unknown }

export async function pushUserState(
  payload: PushUserStatePayload,
): Promise<PushUserStateResult> {
  if (!payload?.syncToken) return { ok: false, reason: 'no-token' }
  const controller = new AbortController()
  const cancel = withTimeout(REQUEST_TIMEOUT_MS, controller)
  try {
    const res = await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
      signal: controller.signal,
      keepalive: true,
      cache: 'no-store',
    })
    const data = await parseJsonSafe(res)
    if (!res.ok || !(data as UserStateResponse | null)?.ok) {
      console.warn('[sync-client] pushUserState non-ok:', res.status, data)
      return { ok: false, status: res.status, data }
    }
    return { ok: true, data }
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err)
    const reason = err instanceof Error && err.name === 'AbortError' ? 'timeout' : 'network'
    console.warn('[sync-client] pushUserState failed:', message)
    return { ok: false, reason }
  } finally {
    cancel()
  }
}
