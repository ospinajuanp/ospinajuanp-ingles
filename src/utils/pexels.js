const API_BASE = 'https://api.pexels.com/v1'
const KEYS = [
  import.meta.env.VITE_PEXELS_API_KEY,
  import.meta.env.VITE_PEXELS_API_KEY_2,
].filter((k) => typeof k === 'string' && k.trim().length > 0)

let currentKeyIndex = 0
let hasWarnedFailure = false
let hasWarnedKeySwitch = false

const RETRYABLE_STATUSES = new Set([401, 403, 429, 500, 502, 503, 504])

function reasonForStatus(status) {
  if (status === 401) return 'API key inválida o expirada'
  if (status === 403) return 'Sin permisos (key bloqueada)'
  if (status === 429) return 'Cuota agotada (200/h o 20K/mes)'
  return `Error HTTP ${status}`
}

function resetWarning() {
  hasWarnedFailure = false
}

export function hasPexelsKey() {
  return KEYS.length > 0
}

function getAuthHeader() {
  return KEYS[currentKeyIndex].trim()
}

function rotateKey(reason) {
  if (KEYS.length <= 1) return
  const from = currentKeyIndex + 1
  currentKeyIndex = (currentKeyIndex + 1) % KEYS.length
  const to = currentKeyIndex + 1
  if (!hasWarnedKeySwitch) {
    hasWarnedKeySwitch = true
    console.warn(
      `[Pexels] Cambiando de key ${from} a ${to} (${reason})`,
    )
  }
}

async function tryFetch(url, key) {
  try {
    const res = await fetch(url, {
      headers: { Authorization: key.trim() },
    })
    if (res.ok) return { ok: true, response: res }
    return { ok: false, status: res.status }
  } catch (err) {
    return { ok: false, networkError: err }
  }
}

function extractPhoto(data) {
  const photo = data?.photos?.[0]
  if (!photo?.src?.large) return null
  return {
    url: photo.src.large,
    photographer: photo.photographer ?? '',
    photographerUrl: photo.photographer_url ?? '',
    pexelsUrl: photo.url ?? '',
  }
}

export async function fetchPexelsPhoto(query, page = 1) {
  if (!hasPexelsKey()) return null
  if (!query) return null

  const safePage = Math.max(1, Math.floor(page))
  const url = `${API_BASE}/search?query=${encodeURIComponent(query)}&per_page=1&orientation=landscape&page=${safePage}`

  for (let attempt = 0; attempt < KEYS.length; attempt++) {
    const result = await tryFetch(url, KEYS[currentKeyIndex])

    if (result.ok) {
      try {
        const data = await result.response.json()
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
          console.warn(
            `[Pexels] Error parseando respuesta: ${err?.message ?? err} — cayendo a Picsum`,
          )
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

    if (RETRYABLE_STATUSES.has(result.status)) {
      rotateKey(reasonForStatus(result.status))
      continue
    }

    if (!hasWarnedFailure) {
      hasWarnedFailure = true
      console.warn(
        `[Pexels] ${reasonForStatus(result.status)} — cayendo a Picsum`,
      )
    }
    return null
  }

  if (!hasWarnedFailure) {
    hasWarnedFailure = true
    console.warn('[Pexels] Todas las keys fallaron — cayendo a Picsum')
  }
  return null
}

export async function checkPexelsStatus() {
  if (!hasPexelsKey()) {
    console.info(
      '[Pexels] Sin VITE_PEXELS_API_KEY ni VITE_PEXELS_API_KEY_2 — usando Picsum + SVG',
    )
    return { ok: false, reason: 'no-key' }
  }

  for (let i = 0; i < KEYS.length; i++) {
    const result = await tryFetch(
      `${API_BASE}/search?query=test&per_page=1&orientation=landscape`,
      KEYS[i],
    )

    if (result.ok) {
      const data = await result.response.json()
      const remaining = result.response.headers.get('X-Ratelimit-Remaining')
      const limit = result.response.headers.get('X-Ratelimit-Limit')
      const photoCount = data?.photos?.length ?? 0
      const keyInfo =
        KEYS.length > 1 ? ` (key ${i + 1} de ${KEYS.length})` : ''
      const quotaInfo =
        remaining && limit ? ` (${remaining}/${limit} restantes esta hora)` : ''
      const photosInfo = photoCount > 0 ? ` — ${photoCount} foto(s) en prueba` : ''
      console.info(
        `[Pexels] ✅ OK${keyInfo}${quotaInfo}${photosInfo}`,
      )
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
    console.warn(`[Pexels] ❌ ${reasonForStatus(result.status)}`)
    return { ok: false, status: result.status }
  }

  return { ok: false, reason: 'no-key' }
}

export { resetWarning, KEYS, getAuthHeader as _testGetAuthHeader }