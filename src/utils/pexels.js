const API_BASE = 'https://api.pexels.com/v1'
const API_KEY = import.meta.env.VITE_PEXELS_API_KEY

let hasWarnedFailure = false

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
  return typeof API_KEY === 'string' && API_KEY.trim().length > 0
}

export async function fetchPexelsPhoto(query, page = 1) {
  if (!hasPexelsKey()) return null
  if (!query) return null

  const safePage = Math.max(1, Math.floor(page))
  const url = `${API_BASE}/search?query=${encodeURIComponent(query)}&per_page=1&orientation=landscape&page=${safePage}`

  try {
    const res = await fetch(url, {
      headers: { Authorization: API_KEY.trim() },
    })
    if (!res.ok) {
      if (!hasWarnedFailure) {
        hasWarnedFailure = true
        console.warn(
          `[Pexels] ${reasonForStatus(res.status)} — cayendo a Picsum`,
        )
      }
      return null
    }
    const data = await res.json()
    const photo = data?.photos?.[0]
    if (!photo?.src?.large) {
      if (!hasWarnedFailure) {
        hasWarnedFailure = true
        console.warn('[Pexels] Respuesta sin fotos — cayendo a Picsum')
      }
      return null
    }
    return {
      url: photo.src.large,
      photographer: photo.photographer ?? '',
      photographerUrl: photo.photographer_url ?? '',
      pexelsUrl: photo.url ?? '',
    }
  } catch (err) {
    if (!hasWarnedFailure) {
      hasWarnedFailure = true
      console.warn(
        `[Pexels] Error de red: ${err?.message ?? err} — cayendo a Picsum`,
      )
    }
    return null
  }
}

export async function checkPexelsStatus() {
  if (!hasPexelsKey()) {
    console.info('[Pexels] Sin VITE_PEXELS_API_KEY — usando Picsum + SVG')
    return { ok: false, reason: 'no-key' }
  }

  try {
    const res = await fetch(
      `${API_BASE}/search?query=test&per_page=1&orientation=landscape`,
      { headers: { Authorization: API_KEY.trim() } },
    )
    if (!res.ok) {
      const reason = reasonForStatus(res.status)
      console.warn(`[Pexels] ❌ ${reason}`)
      return { ok: false, status: res.status, reason }
    }
    const data = await res.json()
    const remaining = res.headers.get('X-Ratelimit-Remaining')
    const limit = res.headers.get('X-Ratelimit-Limit')
    const photoCount = data?.photos?.length ?? 0
    const quotaInfo =
      remaining && limit ? ` (${remaining}/${limit} restantes esta hora)` : ''
    const photosInfo = photoCount > 0 ? ` — ${photoCount} foto(s) en prueba` : ''
    console.info(`[Pexels] ✅ OK${quotaInfo}${photosInfo}`)
    return { ok: true, remaining, limit }
  } catch (err) {
    console.warn(
      `[Pexels] ❌ Error de red: ${err?.message ?? err}`,
    )
    return { ok: false, reason: 'network' }
  }
}

export { resetWarning }