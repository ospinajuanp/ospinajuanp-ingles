import type { SrsCardSrs, SrsStore } from '@/lib/types/srs'
import type { ThemeId } from '@/lib/types/theme'
import { calculateStoreHash } from './syncHash'

interface MergeableCard {
  type?: 'verb' | 'custom'
  id?: string
  verbKey?: string
  front?: { es?: string; en?: string }
  infinitivo?: { ing?: string; esp?: string }
  verbId?: number | null
  createdAt?: number
  srs?: SrsCardSrs
  [key: string]: unknown
}

const FALLBACK_TS = 0

function cardTimestamp(card: MergeableCard | undefined): number {
  if (!card?.srs) return card?.createdAt ?? FALLBACK_TS
  const srs = card.srs
  if (typeof srs.lastReviewed === 'number') return srs.lastReviewed
  if (typeof srs.nextReview === 'number') return srs.nextReview
  return card.createdAt ?? FALLBACK_TS
}

function pickWinner(local: MergeableCard, remote: MergeableCard): 'remote' | 'local' {
  const localTs = cardTimestamp(local)
  const remoteTs = cardTimestamp(remote)
  if (remoteTs > localTs) return 'remote'
  if (remoteTs < localTs) return 'local'
  return 'remote'
}

function mergeCard(local: MergeableCard, remote: MergeableCard): MergeableCard {
  const winner = pickWinner(local, remote)
  const survivor = winner === 'remote' ? remote : local
  const localTs = cardTimestamp(local)
  const remoteTs = cardTimestamp(remote)
  const newerSrs =
    remoteTs > localTs ? remote.srs : remoteTs < localTs ? local.srs : survivor.srs

  return {
    ...survivor,
    srs: newerSrs
      ? { ...newerSrs }
      : survivor.srs,
    createdAt: Math.max(local?.createdAt ?? 0, remote?.createdAt ?? 0),
  }
}

export function mergeSRSStores(
  local: SrsStore | null | undefined,
  remote: SrsStore | null | undefined,
): SrsStore {
  const localCards = (local?.cards ?? {}) as Record<string, MergeableCard>
  const remoteCards = (remote?.cards ?? {}) as Record<string, MergeableCard>
  const mergedCards: Record<string, MergeableCard> = { ...localCards }

  for (const id of Object.keys(remoteCards)) {
    const remoteCard = remoteCards[id]
    if (!remoteCard) continue
    const existing = mergedCards[id]
    if (!existing) {
      mergedCards[id] = remoteCard
    } else {
      mergedCards[id] = mergeCard(existing, remoteCard)
    }
  }

  const localOrder = Array.isArray(local?.order) ? local.order : []
  const remoteOrder = Array.isArray(remote?.order) ? remote.order : []
  const seen = new Set<string>()
  const order: string[] = []
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
  for (const id of [...localOrder, ...remoteOrder]) {
    if (!seen.has(id) && mergedCards[id]) {
      seen.add(id)
      order.push(id)
    }
  }

  return { version: 1, cards: mergedCards as SrsStore['cards'], order }
}

export function shouldPushLocal(
  local: SrsStore | null | undefined,
  remote: SrsStore | null | undefined,
): boolean {
  const localCount = Object.keys(local?.cards ?? {}).length
  const remoteCount = Object.keys(remote?.cards ?? {}).length
  if (remoteCount === 0) return localCount > 0
  return false
}

export interface CompareStatesResult {
  hasChanges: boolean
  mergedStore: SrsStore
  hash: string
}

export function compareStatesByHash({
  localStore,
  localTheme,
  remoteStore,
  remoteTheme,
}: {
  localStore: SrsStore | null | undefined
  localTheme: ThemeId | null | undefined
  remoteStore: SrsStore | null | undefined
  remoteTheme: ThemeId | null | undefined
}): CompareStatesResult {
    const localHash = calculateStoreHash(localStore ?? null, (localTheme ?? null) as ThemeId | null)
    const remoteHash = calculateStoreHash(remoteStore ?? null, (remoteTheme ?? null) as ThemeId | null)
  if (localHash === remoteHash) {
    return {
      hasChanges: false,
      mergedStore: localStore ?? { version: 1, cards: {}, order: [] },
      hash: localHash,
    }
  }
  const mergedStore = mergeSRSStores(localStore, remoteStore)
  const mergedHash = calculateStoreHash(mergedStore, (remoteTheme ?? null) as ThemeId | null)
  return { hasChanges: true, mergedStore, hash: mergedHash }
}
