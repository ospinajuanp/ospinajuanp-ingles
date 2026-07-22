const STORAGE_KEY = 'ospinajuanp-ingles:syncToken'

const UUID_RE =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

function readRaw(): string | null {
  if (typeof window === 'undefined') return null
  try {
    return window.localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

function writeRaw(token: string): void {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(STORAGE_KEY, token)
  } catch {
    // Private mode / quota — fall back to in-memory only for this tab.
  }
}

function isValid(token: string | null): token is string {
  return typeof token === 'string' && UUID_RE.test(token)
}

function generateToken(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID()
  }
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    const b = new Uint8Array(16)
    crypto.getRandomValues(b)
    const b6 = b[6] as number
    const b8 = b[8] as number
    b[6] = (b6 & 0x0f) | 0x40
    b[8] = (b8 & 0x3f) | 0x80
    const h = Array.from(b, (x) => x.toString(16).padStart(2, '0'))
    return `${h.slice(0, 4).join('')}-${h.slice(4, 6).join('')}-${h.slice(6, 8).join('')}-${h.slice(8, 10).join('')}-${h.slice(10, 16).join('')}`
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

export function getSyncToken(): string {
  const existing = readRaw()
  if (isValid(existing)) return existing
  const fresh = generateToken()
  writeRaw(fresh)
  return fresh
}

export function peekSyncToken(): string | null {
  const existing = readRaw()
  return isValid(existing) ? existing : null
}

export function linkSyncToken(token: string): boolean {
  if (!isValid(token)) return false
  const current = readRaw()
  if (current === token) return false
  writeRaw(token)
  return true
}

export function resetSyncToken(): void {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.removeItem(STORAGE_KEY)
  } catch {
    // ignore
  }
}

export function isValidSyncToken(token: string): boolean {
  return isValid(token)
}
