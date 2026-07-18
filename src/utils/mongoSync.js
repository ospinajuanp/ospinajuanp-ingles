/**
 * Fire-and-forget POST to /api/verbs/sync.
 *
 * Survives navigations (`keepalive: true`), never throws back to the caller,
 * and logs warnings on failure rather than crashing the UI.
 */
export async function syncVerbToMongo(payload) {
  if (!payload || payload.id == null) return
  try {
    const res = await fetch('/api/verbs/sync', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
      keepalive: true,
    })
    if (!res.ok) {
      console.warn('[mongo-sync] non-ok response:', res.status)
    }
  } catch (err) {
    console.warn('[mongo-sync] request failed silently:', err?.message ?? err)
  }
}