import type { VerbEnrichment } from '@/lib/types/media'

interface VerbWithEnrichment {
  id?: number | null
  infinitivo?: { ing?: string; esp?: string }
  [key: string]: unknown
}

export async function syncVerbToMongo(payload: VerbWithEnrichment): Promise<void> {
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
    const message = err instanceof Error ? err.message : String(err)
    console.warn('[mongo-sync] request failed silently:', message)
  }
}

export type { VerbEnrichment }
