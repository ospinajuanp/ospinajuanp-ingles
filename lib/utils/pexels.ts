import type { PexelsPhoto } from '@/lib/types/media'

const API_BASE = 'https://api.pexels.com/v1'
const KEYS: string[] = [
  process.env.NEXT_PUBLIC_PEXELS_API_KEY,
  process.env.NEXT_PUBLIC_PEXELS_API_KEY_2,
].filter((k): k is string => typeof k === 'string' && k.trim().length > 0)

let currentKeyIndex = 0
let hasWarnedFailure = false
let hasWarnedKeySwitch = false

const RETRYABLE_STATUSES = new Set([401, 403, 429, 500, 502, 503, 504])

function reasonForStatus(status: number): string {
  if (status === 401) return 'API key inválida o expirada'
  if (status === 403) return 'Sin permisos (key bloqueada)'
  if (status === 429) return 'Cuota agotada (200/h o 20K/mes)'
  return `Error HTTP ${status}`
}

export function resetWarning(): void {
  hasWarnedFailure = false
}

export function hasPexelsKey(): boolean {
  return KEYS.length > 0
}

function getAuthHeader(): string {
  const key = KEYS[currentKeyIndex]
  return key ? key.trim() : ''
}

function rotateKey(reason: string): void {
  if (KEYS.length <= 1) return
  const from = currentKeyIndex + 1
  currentKeyIndex = (currentKeyIndex + 1) % KEYS.length
  const to = currentKeyIndex + 1
  if (!hasWarnedKeySwitch) {
    hasWarnedKeySwitch = true
    console.warn(`[Pexels] Cambiando de key ${from} a ${to} (${reason})`)
  }
}

type FetchResult =
  | { ok: true; response: Response }
  | { ok: false; status?: number; networkError?: Error }

async function tryFetch(url: string, key: string): Promise<FetchResult> {
  try {
    const res = await fetch(url, {
      headers: { Authorization: key.trim() },
    })
    if (res.ok) return { ok: true, response: res }
    return { ok: false, status: res.status }
  } catch (err) {
    return { ok: false, networkError: err instanceof Error ? err : new Error(String(err)) }
  }
}

interface PexelsPhotoData {
  photos?: Array<{
    src?: { large?: string }
    photographer?: string
    photographer_url?: string
    url?: string
  }>
}

function extractPhoto(data: PexelsPhotoData | null): PexelsPhoto | null {
  const photo = data?.photos?.[0]
  if (!photo?.src?.large) return null
  return {
    url: photo.src.large,
    photographer: photo.photographer ?? '',
    photographerUrl: photo.photographer_url ?? '',
    pexelsUrl: photo.url ?? '',
  }
}

export async function fetchPexelsPhoto(
  query: string,
  page: number = 1,
): Promise<PexelsPhoto | null> {
  if (!hasPexelsKey()) return null
  if (!query) return null

  const safePage = Math.max(1, Math.floor(page))
  const url = `${API_BASE}/search?query=${encodeURIComponent(query)}&per_page=1&orientation=landscape&page=${safePage}`

  for (let attempt = 0; attempt < KEYS.length; attempt++) {
    const currentKey = KEYS[currentKeyIndex]
    if (!currentKey) break
    const result = await tryFetch(url, currentKey)

    if (result.ok) {
      try {
        const data = (await result.response.json()) as PexelsPhotoData
        const photo = extractPhoto(data)
        if (!photo) {
          if (!hasWarnedFailure) {
            hasWarnedFailure = true
            console.warn('[Pexels] Respuesta sin fotos — cayendo a Picsum')
          }
          return null
        }
        return photo
      } catch (err) {
        if (!hasWarnedFailure) {
          hasWarnedFailure = true
          const message = err instanceof Error ? err.message : String(err)
          console.warn(`[Pexels] Error parseando respuesta: ${message} — cayendo a Picsum`)
        }
        return null
      }
    }

    if (result.networkError) {
      rotateKey(`red: ${result.networkError.message ?? result.networkError}`)
      if (!hasWarnedFailure) {
        hasWarnedFailure = true
        console.warn(
          `[Pexels] Error de red: ${result.networkError.message ?? result.networkError} — cayendo a Picsum`,
        )
      }
      continue
    }

    if (result.status !== undefined && RETRYABLE_STATUSES.has(result.status)) {
      rotateKey(reasonForStatus(result.status))
      continue
    }

    if (!hasWarnedFailure) {
      hasWarnedFailure = true
      const status = result.status ?? 0
      console.warn(`[Pexels] ${reasonForStatus(status)} — cayendo a Picsum`)
    }
    return null
  }

  if (!hasWarnedFailure) {
    hasWarnedFailure = true
    console.warn('[Pexels] Todas las keys fallaron — cayendo a Picsum')
  }
  return null
}

export type PexelsStatus =
  | { ok: true; remaining: string | null; limit: string | null; keyIndex: number }
  | { ok: false; reason: 'no-key' | 'network'; status?: number }

export async function checkPexelsStatus(): Promise<PexelsStatus> {
  if (!hasPexelsKey()) {
    console.info(
      '[Pexels] Sin NEXT_PUBLIC_PEXELS_API_KEY ni NEXT_PUBLIC_PEXELS_API_KEY_2 — usando Picsum + SVG',
    )
    return { ok: false, reason: 'no-key' }
  }

  for (let i = 0; i < KEYS.length; i++) {
    const key = KEYS[i]
    if (!key) continue
    const result = await tryFetch(
      `${API_BASE}/search?query=test&per_page=1&orientation=landscape`,
      key,
    )

    if (result.ok) {
      const data = (await result.response.json()) as PexelsPhotoData
      const remaining = result.response.headers.get('X-Ratelimit-Remaining')
      const limit = result.response.headers.get('X-Ratelimit-Limit')
      const photoCount = data?.photos?.length ?? 0
      const keyInfo = KEYS.length > 1 ? ` (key ${i + 1} de ${KEYS.length})` : ''
      const quotaInfo =
        remaining && limit ? ` (${remaining}/${limit} restantes esta hora)` : ''
      const photosInfo = photoCount > 0 ? ` — ${photoCount} foto(s) en prueba` : ''
      console.info(`[Pexels] ✅ OK${keyInfo}${quotaInfo}${photosInfo}`)
      currentKeyIndex = i
      return { ok: true, remaining, limit, keyIndex: i }
    }

    if (i < KEYS.length - 1) continue

    if (result.networkError) {
      console.warn(
        `[Pexels] ❌ Error de red: ${result.networkError.message ?? result.networkError}`,
      )
      return { ok: false, reason: 'network' }
    }
    const statusValue = result.status ?? 0
    console.warn(`[Pexels] ❌ ${reasonForStatus(statusValue)}`)
    return { ok: false, reason: 'network' as const, status: statusValue }
  }

  return { ok: false, reason: 'no-key' as const }
}

export { KEYS, getAuthHeader as _testGetAuthHeader }
