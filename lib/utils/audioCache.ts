const TTS = '__tts__'
const NONE = '__none__'

const cache = new Map<string, string>()

function normalize(word: string): string {
  return word?.trim().toLowerCase() ?? ''
}

function raw(word: string): string | undefined {
  return cache.get(normalize(word))
}

export function getCachedAudio(word: string): string | null {
  const v = raw(word)
  return typeof v === 'string' && v !== TTS && v !== NONE ? v : null
}

export function isTTSSupported(word: string): boolean {
  return raw(word) === TTS
}

export function isUnavailable(word: string): boolean {
  return raw(word) === NONE
}

export function setCachedAudio(word: string, url: string): void {
  cache.set(normalize(word), url)
}

export function markTTSSupported(word: string): void {
  cache.set(normalize(word), TTS)
}

export function setUnavailable(word: string): void {
  cache.set(normalize(word), NONE)
}
