const STORAGE_KEY = 'verbos:pexelsCache'

function normalize(word) {
  return word?.trim().toLowerCase() ?? ''
}

function load() {
  if (typeof window === 'undefined') return new Map()
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) return new Map()
    const parsed = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object') return new Map()
    return new Map(Object.entries(parsed))
  } catch {
    return new Map()
  }
}

function persist(map) {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(Object.fromEntries(map)))
  } catch {
    // quota exceeded, private mode, etc. — fall back to in-memory only
  }
}

const cache = load()

export function getCachedImages(word) {
  return cache.get(normalize(word)) ?? null
}

export function addCachedImage(word, data) {
  const key = normalize(word)
  const arr = cache.get(key) ?? []
  arr.push(data)
  cache.set(key, arr)
  persist(cache)
}
