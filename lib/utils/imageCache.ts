import type { PexelsPhoto } from '@/lib/types/media'

const STORAGE_KEY = 'verbos:pexelsCache'

function normalize(word: string): string {
  return word?.trim().toLowerCase() ?? ''
}

function load(): Map<string, PexelsPhoto[]> {
  if (typeof window === 'undefined') return new Map()
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) return new Map()
    const parsed: unknown = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return new Map()
    return new Map(Object.entries(parsed as Record<string, PexelsPhoto[]>))
  } catch {
    return new Map()
  }
}

function persist(map: Map<string, PexelsPhoto[]>): void {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(Object.fromEntries(map)))
  } catch {
    // quota exceeded, private mode, etc. — fall back to in-memory only
  }
}

const cache = load()

export function getCachedImages(word: string): PexelsPhoto[] | null {
  return cache.get(normalize(word)) ?? null
}

export function addCachedImage(word: string, data: PexelsPhoto): void {
  const key = normalize(word)
  const arr = cache.get(key) ?? []
  arr.push(data)
  cache.set(key, arr)
  persist(cache)
}
