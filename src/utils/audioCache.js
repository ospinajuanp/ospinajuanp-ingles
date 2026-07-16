const cache = new Map()

const TTS = '__tts__'
const NONE = '__none__'

function normalize(word) {
  return word?.trim().toLowerCase() ?? ''
}

function raw(word) {
  return cache.get(normalize(word))
}

export function getCachedAudio(word) {
  const v = raw(word)
  return typeof v === 'string' && v !== TTS && v !== NONE ? v : null
}

export function isTTSSupported(word) {
  return raw(word) === TTS
}

export function isUnavailable(word) {
  return raw(word) === NONE
}

export function setCachedAudio(word, url) {
  cache.set(normalize(word), url)
}

export function markTTSSupported(word) {
  cache.set(normalize(word), TTS)
}

export function setUnavailable(word) {
  cache.set(normalize(word), NONE)
}