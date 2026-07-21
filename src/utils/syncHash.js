// Lightweight deterministic hash for the sync engine.
//
// Why a custom hash instead of plain JSON.stringify comparison:
//   - JSON.stringify is correct for shallow equality but it's expensive
//     (allocates a full string for both sides on every comparison) and
//     order-sensitive — two objects with the same keys but different
//     insertion orders would stringify to different strings even when
//     logically equal.
//   - FNV-1a 32-bit is fast (~tens of ns per KB), produces a fixed-size
//     8-char hex string we can store in a useRef cheaply, and is plenty
//     uniform for change-detection (we don't need cryptographic strength).
//
// Where it's used:
//   - src/utils/syncMerge.js: `compareStatesByHash` short-circuits the
//     LWW merge when both sides hash identically, saving the O(n) merge
//     work and the React `replaceStore` round-trip.
//   - src/hooks/useSRS.js: `replaceStore` no-ops when the incoming store
//     hashes to the same value as the current store, preventing
//     re-renders when the sync engine pulls a remote snapshot that
//     matches local exactly.
//   - src/hooks/useSyncEngine.js: tracks `lastSyncedHashRef` so that:
//       (a) the mutation watcher doesn't schedule a push when nothing
//           actually changed since the last successful push, and
//       (b) `pushCurrent` itself short-circuits when called repeatedly
//           (pagehide flush + 5-min safety-net) without any new edits.
//
// Zero deps. Stable across runs and devices.

const FNV_OFFSET_BASIS = 0x811c9dc5
const FNV_PRIME = 0x01000193

/**
 * FNV-1a 32-bit hash. Returns an 8-character lowercase hex string.
 * Non-cryptographic; collision-resistant enough for change detection.
 */
function fnv1a(input) {
  let hash = FNV_OFFSET_BASIS
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i)
    hash = Math.imul(hash, FNV_PRIME)
  }
  // Force unsigned 32-bit
  return (hash >>> 0).toString(16).padStart(8, '0')
}

/**
 * Stable, order-independent JSON-ish serialization. Object keys are
 * sorted alphabetically; arrays preserve order; null/undefined/NaN/
 * Infinity are normalized so two "logically equal" objects always
 * serialize to the same string.
 */
function stableStringify(value) {
  if (value === null || value === undefined) return 'null'
  if (typeof value === 'boolean') return value ? '1' : '0'
  if (typeof value === 'number') {
    return Number.isFinite(value) ? JSON.stringify(value) : 'null'
  }
  if (typeof value === 'string') return JSON.stringify(value)
  if (Array.isArray(value)) {
    let out = '['
    for (let i = 0; i < value.length; i++) {
      if (i > 0) out += ','
      out += stableStringify(value[i])
    }
    return out + ']'
  }
  if (typeof value === 'object') {
    const keys = Object.keys(value).sort()
    let out = '{'
    for (let i = 0; i < keys.length; i++) {
      const k = keys[i]
      if (i > 0) out += ','
      out += JSON.stringify(k) + ':' + stableStringify(value[k])
    }
    return out + '}'
  }
  return 'null'
}

const THEME_LOCAL_STORAGE_KEY = 'ospinajuanp-ingles:theme'

/**
 * Read the theme currently persisted in localStorage. Returns `null`
 * in SSR/test environments where `window` is not available, or if
 * reading fails (private mode, quota).
 */
export function readThemeFromLocalStorage() {
  if (typeof window === 'undefined') return null
  try {
    return window.localStorage.getItem(THEME_LOCAL_STORAGE_KEY)
  } catch {
    return null
  }
}

/**
 * Hash a single SRS card deterministically. Strips the per-device `id`
 * field so two cards on different devices that share every other field
 * hash identically — `id` is `makeId()`-generated and unique per device,
 * so it's part of the wire-format identity but NOT part of the logical
 * content identity we use for change detection.
 */
export function calculateCardHash(card) {
  if (!card || typeof card !== 'object') return fnv1a('null')
  // Drop the per-device-generated `id`. Cards are matched by content
  // (verbKey, type, front) by the sync engine's LWW merge — id is the
  // dictionary key in `cards`, not part of the card's identity.
  const { id: _ignored, ...rest } = card
  return fnv1a(stableStringify(rest))
}

/**
 * Hash the full sync state — SRS store + theme — deterministically.
 * Both sides of the sync (the engine + each call site) feed this the
 * SAME shape so equality means "logically identical, no work to do".
 *
 * - `cards` are hashed in id-sorted order (so insertion order in `order`
 *   doesn't affect the hash; the `order` array is hashed separately).
 * - `order` is hashed as a comma-joined string of card ids.
 * - `theme` is included so a theme-only change is detectable.
 *
 * Returning a short fixed-length hex string keeps refs / state cheap.
 */
export function calculateStoreHash(srsStore, theme) {
  const cards =
    srsStore && typeof srsStore === 'object' && srsStore.cards
      ? srsStore.cards
      : {}
  const order =
    srsStore && Array.isArray(srsStore.order) ? srsStore.order : []
  const cardIds = Object.keys(cards).sort()
  const cardsPart = fnv1a(
    cardIds.map((id) => `${id}:${calculateCardHash(cards[id])}`).join('|'),
  )
  const orderPart = fnv1a(order.join(','))
  const themePart = fnv1a(typeof theme === 'string' ? theme : '')
  return fnv1a(`s=${cardsPart}|o=${orderPart}|t=${themePart}`)
}
