// Pure Last-Write-Wins merge of two SRS stores.
//
// The SRS store shape (see src/hooks/useSRS.js) is:
//
//   { version: 1, cards: { [id]: Card }, order: string[] }
//
// Merge rules:
//   - Cards present in only one side → kept.
//   - Cards present in BOTH sides → the card whose SRS state has the
//     latest `lastReviewed` (falling back to `nextReview`, then
//     `createdAt`) wins field-by-field. Card identity (`type`, `verbKey`,
//     `front`, `infinitivo`) follows the survivor so verb metadata
//     stays consistent on the receiving device.
//   - `order` is the union of both sides, de-duplicated, with the
//     relative ordering of each side preserved.
//
// This module is pure: no localStorage, no fetch, no React. The engine
// in useSyncEngine decides WHEN to call it and WHAT to do with the
// result (write back to localStorage, push to Atlas).

const FALLBACK_TS = 0

function cardTimestamp(card) {
  if (!card || !card.srs) return card?.createdAt ?? FALLBACK_TS
  const srs = card.srs
  if (typeof srs.lastReviewed === 'number') return srs.lastReviewed
  if (typeof srs.nextReview === 'number') return srs.nextReview
  return card.createdAt ?? FALLBACK_TS
}

function pickWinner(local, remote) {
  const localTs = cardTimestamp(local)
  const remoteTs = cardTimestamp(remote)
  // Tie-breaker: prefer the remote copy (more authoritative for the
  // device that joined later). Falls back to local if remote is missing.
  if (remoteTs > localTs) return 'remote'
  if (remoteTs < localTs) return 'local'
  return 'remote'
}

function mergeCard(local, remote) {
  const winner = pickWinner(local, remote)
  const survivor = winner === 'remote' ? remote : local
  // Merge SRS state field-by-field using the newer timestamp. This keeps
  // structural fields (type/verbKey/front/infinitivo) from the survivor
  // while never losing recent schedule data.
  const localTs = cardTimestamp(local)
  const remoteTs = cardTimestamp(remote)
  const newerSrs =
    remoteTs > localTs ? remote.srs : remoteTs < localTs ? local.srs : survivor.srs

  return {
    ...survivor,
    srs: { ...newerSrs },
    // Preserve the latest createdAt as well (cards created on either
    // device share the same `id` if we ever migrate to a stable key).
    createdAt: Math.max(local?.createdAt ?? 0, remote?.createdAt ?? 0),
  }
}

/**
 * Merge two SRS stores. Returns a new store object; inputs are not
 * mutated. Either side may be `null`/missing — treated as empty.
 */
export function mergeSRSStores(local, remote) {
  const localCards = local?.cards ?? {}
  const remoteCards = remote?.cards ?? {}
  const mergedCards = { ...localCards }

  for (const id of Object.keys(remoteCards)) {
    if (!mergedCards[id]) {
      mergedCards[id] = remoteCards[id]
    } else {
      mergedCards[id] = mergeCard(mergedCards[id], remoteCards[id])
    }
  }

  // Order: union, preserving each side's relative order. Cards that
  // exist only on one side keep their position; merged cards stay at
  // the earliest position they appeared in.
  const localOrder = Array.isArray(local?.order) ? local.order : []
  const remoteOrder = Array.isArray(remote?.order) ? remote.order : []
  const seen = new Set()
  const order = []
  const len = Math.max(localOrder.length, remoteOrder.length)
  for (let i = 0; i < len; i++) {
    const l = localOrder[i]
    const r = remoteOrder[i]
    if (l && !seen.has(l) && mergedCards[l]) {
      seen.add(l)
      order.push(l)
    }
    if (r && !seen.has(r) && mergedCards[r]) {
      seen.add(r)
      order.push(r)
    }
  }
  // Append any leftover (in case one side had more cards than the other).
  for (const id of [...localOrder, ...remoteOrder]) {
    if (!seen.has(id) && mergedCards[id]) {
      seen.add(id)
      order.push(id)
    }
  }

  return { version: 1, cards: mergedCards, order }
}

/**
 * Pick which side wins outright. Useful for "first-time bootstrap push"
 * where the remote is empty/null — we just send whatever the user has
 * locally without any merge work.
 */
export function shouldPushLocal(local, remote) {
  const localCount = Object.keys(local?.cards ?? {}).length
  const remoteCount = Object.keys(remote?.cards ?? {}).length
  if (remoteCount === 0) return localCount > 0
  return false
}