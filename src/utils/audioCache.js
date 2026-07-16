const cache = new Map()

function normalize(word) {
  return word?.trim().toLowerCase() ?? ''
}

export function getCachedAudio(word) {
  return cache.get(normalize(word))
}

export function setCachedAudio(word, url) {
  cache.set(normalize(word), url)
}

export function setUnavailable(word) {
  cache.set(normalize(word), null)
}

export function isUnavailable(word) {
  return cache.has(normalize(word)) && cache.get(normalize(word)) === null
}