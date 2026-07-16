const API_BASE = 'https://api.pexels.com/v1'
const API_KEY = import.meta.env.VITE_PEXELS_API_KEY

export function hasPexelsKey() {
  return typeof API_KEY === 'string' && API_KEY.trim().length > 0
}

export async function fetchPexelsPhoto(query) {
  if (!hasPexelsKey()) return null
  if (!query) return null

  const url = `${API_BASE}/search?query=${encodeURIComponent(query)}&per_page=1&orientation=landscape`

  try {
    const res = await fetch(url, {
      headers: { Authorization: API_KEY.trim() },
    })
    if (!res.ok) return null
    const data = await res.json()
    const photo = data?.photos?.[0]
    if (!photo?.src?.large) return null
    return {
      url: photo.src.large,
      photographer: photo.photographer ?? '',
      photographerUrl: photo.photographer_url ?? '',
      pexelsUrl: photo.url ?? '',
    }
  } catch {
    return null
  }
}