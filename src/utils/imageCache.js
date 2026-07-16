const cache = new Map()

function normalize(word) {
  return word?.trim().toLowerCase() ?? ''
}

export function getCachedImages(word) {
  return cache.get(normalize(word)) ?? null
}

export function addCachedImage(word, data) {
  const key = normalize(word)
  const arr = cache.get(key) ?? []
  arr.push(data)
  cache.set(key, arr)
}