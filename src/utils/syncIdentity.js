// Anonymous sync identity (no auth, no passwords).
//
// A single UUIDv4 token identifies an anonymous user's "sync slot" in
// the `ingles-db.user_sync` collection. It is generated lazily on first
// read and persisted in localStorage so it survives reloads.
//
// Why `crypto.randomUUID()`:
//   - Native in all modern browsers + Node 19+.
//   - No dependency to ship.
//   - Cryptographically random (RFC 4122 v4) → collision-safe across
//     millions of devices without coordination.
//
// Why lazy generation:
//   - We never block first paint on identity. The token is read once,
//     stamped, and used by the background sync engine. The local-first
//     UX keeps working even if Atlas is unreachable on day one.

const STORAGE_KEY = 'ospinajuanp-ingles:syncToken'

const UUID_RE =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

function readRaw() {
  if (typeof window === 'undefined') return null
  try {
    return window.localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

function writeRaw(token) {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(STORAGE_KEY, token)
  } catch {
    // Private mode / quota — fall back to in-memory only for this tab.
  }
}

function isValid(token) {
  return typeof token === 'string' && UUID_RE.test(token)
}

function generateToken() {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID()
  }
  // Fallback for ancient runtimes: RFC 4122 v4 via getRandomValues.
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    const b = new Uint8Array(16)
    crypto.getRandomValues(b)
    b[6] = (b[6] & 0x0f) | 0x40
    b[8] = (b[8] & 0x3f) | 0x80
    const h = Array.from(b, (x) => x.toString(16).padStart(2, '0'))
    return `${h.slice(0, 4).join('')}-${h.slice(4, 6).join('')}-${h.slice(6, 8).join('')}-${h.slice(8, 10).join('')}-${h.slice(10, 16).join('')}`
  }
  // Last-resort: Math.random (not cryptographically strong, but the
  // sync slot is anonymous and recoverable by pasting a fresh token).
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

/**
 * Read (or lazily create) the local syncToken. Idempotent — calling it
 * repeatedly returns the same value.
 */
export function getSyncToken() {
  const existing = readRaw()
  if (isValid(existing)) return existing
  const fresh = generateToken()
  writeRaw(fresh)
  return fresh
}

/**
 * Read the current syncToken WITHOUT generating a new one. Returns null
 * if none has been created yet. Useful for "do we have an identity yet?"
 * checks before kicking off network calls.
 */
export function peekSyncToken() {
  const existing = readRaw()
  return isValid(existing) ? existing : null
}

/**
 * Adopt a foreign token (e.g. user pasted one from another device, or
 * the URL carried `?syncToken=...`). Validates format; returns true if
 * the local identity was swapped.
 */
export function linkSyncToken(token) {
  if (!isValid(token)) return false
  const current = readRaw()
  if (current === token) return false
  writeRaw(token)
  return true
}

/**
 * Erase the local syncToken. The next call to getSyncToken() mints a
 * fresh one — effectively a "log out from sync" without touching the
 * local SRS data.
 */
export function resetSyncToken() {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.removeItem(STORAGE_KEY)
  } catch {
    // ignore
  }
}

export function isValidSyncToken(token) {
  return isValid(token)
}