const cache = new Map()

function normalize(word) {
  return word?.trim().toLowerCase() ?? ''
}

export function getCachedImage(word) {
  return cache.get(normalize(word)) ?? null
}

export function setCachedImage(word, data) {
  cache.set(normalize(word), data)
}