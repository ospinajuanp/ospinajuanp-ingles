// HTTP client for the user-sync endpoint.
//
// Mirrors the philosophy of src/utils/mongoSync.js: every call is
// fire-and-forget from the caller's perspective (errors are logged, not
// thrown), so a network blip never breaks the UI.
//
// Two operations:
//   - fetchUserState(token): GET /api/sync/user?token=…
//   - pushUserState({syncToken, srsStore, theme}): POST /api/sync/user
//
// Both return a structured `{ ok, ... }` envelope so the engine can
// reason about partial failures (offline vs. server error vs. invalid
// token).

const ENDPOINT = '/api/sync/user'
const REQUEST_TIMEOUT_MS = 8000

function withTimeout(ms, controller) {
  // Caller owns the AbortController so they can cancel early if needed.
  const timer = setTimeout(() => controller.abort(), ms)
  return () => clearTimeout(timer)
}

async function parseJsonSafe(res) {
  try {
    return await res.json()
  } catch {
    return null
  }
}

/**
 * GET the persisted state for a given syncToken. Returns null on any
 * non-2xx (including 404 "no record yet"), logs once on persistent
 * failure to avoid console spam.
 */
export async function fetchUserState(token) {
  if (!token) return { ok: false, reason: 'no-token' }
  const controller = new AbortController()
  const cancel = withTimeout(REQUEST_TIMEOUT_MS, controller)
  try {
    const res = await fetch(
      `${ENDPOINT}?token=${encodeURIComponent(token)}`,
      { method: 'GET', signal: controller.signal, cache: 'no-store' },
    )
    const data = await parseJsonSafe(res)
    if (!res.ok || !data?.ok) {
      return { ok: false, status: res.status, data }
    }
    return { ok: true, state: data.state ?? null }
  } catch (err) {
    console.warn('[sync-client] fetchUserState failed:', err?.message ?? err)
    return { ok: false, reason: err?.name === 'AbortError' ? 'timeout' : 'network' }
  } finally {
    cancel()
  }
}

/**
 * POST a snapshot of the user's local state. Body shape:
 *   { syncToken, srsStore, theme }
 *
 * Server is idempotent (upsert by syncToken). We never throw — errors
 * are logged and returned. The engine decides whether to retry later.
 */
export async function pushUserState(payload) {
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
    if (!res.ok || !data?.ok) {
      console.warn('[sync-client] pushUserState non-ok:', res.status, data)
      return { ok: false, status: res.status, data }
    }
    return { ok: true, data }
  } catch (err) {
    console.warn('[sync-client] pushUserState failed:', err?.message ?? err)
    return { ok: false, reason: err?.name === 'AbortError' ? 'timeout' : 'network' }
  } finally {
    cancel()
  }
}