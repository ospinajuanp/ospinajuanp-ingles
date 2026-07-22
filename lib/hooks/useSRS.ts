import { useCallback, useEffect, useRef, useState } from 'react'
import { createInitialSRSState, calculateNextReview, isDue } from '@/lib/utils/srs'
import { calculateStoreHash, readThemeFromLocalStorage } from '@/lib/utils/syncHash'
import type {
  Grade,
  SrsApi,
  SrsCard,
  SrsCardSrs,
  SrsStore,
  SrsVerbCard,
  SrsCustomCard,
} from '@/lib/types/srs'

const LOCAL_STORAGE_KEY = 'ospinajuanp-ingles:srs:v1'

function emptyStore(): SrsStore {
  return { version: 1, cards: {}, order: [] }
}

function readStore(): SrsStore {
  if (typeof window === 'undefined') return emptyStore()
  try {
    const raw = window.localStorage.getItem(LOCAL_STORAGE_KEY)
    if (!raw) return emptyStore()
    const parsed: unknown = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object') return emptyStore()
    const obj = parsed as Record<string, unknown>
    return {
      version: 1,
      cards:
        obj.cards && typeof obj.cards === 'object' && obj.cards !== null
          ? (obj.cards as SrsStore['cards'])
          : {},
      order: Array.isArray(obj.order) ? (obj.order as string[]) : [],
    }
  } catch {
    return emptyStore()
  }
}

function writeStore(store: SrsStore): void {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(store))
  } catch {
    // Private mode / quota — silently ignore.
  }
}

function makeId(prefix: string): string {
  const rand = Math.random().toString(36).slice(2, 10)
  return `${prefix}_${Date.now().toString(36)}_${rand}`
}

export interface VerbToRegister {
  id?: number | null
  infinitivo?: { ing?: string; esp?: string }
}

interface UseSrsApi extends SrsApi {}

export function useSRS(): UseSrsApi {
  const [store, setStore] = useState<SrsStore>(() => readStore())
  const [revision, setRevision] = useState(0)

  const storeRef = useRef<SrsStore>(store)
  useEffect(() => {
    storeRef.current = store
  }, [store])

  useEffect(() => {
    function onStorage(e: StorageEvent): void {
      if (e.key !== LOCAL_STORAGE_KEY) return
      setStore(readStore())
      setRevision((r) => r + 1)
    }
    window.addEventListener('storage', onStorage)
    return () => window.removeEventListener('storage', onStorage)
  }, [])

  const commit = useCallback((updater: (draft: SrsStore) => SrsStore): void => {
    setStore((prev) => {
      const draft: SrsStore = {
        version: 1,
        cards: { ...prev.cards },
        order: [...prev.order],
      }
      const next = updater(draft)
      const safeNext: SrsStore =
        next && typeof next === 'object' && next.cards && next.order ? next : draft
      writeStore(safeNext)
      return safeNext
    })
    setRevision((r) => r + 1)
  }, [])

  const addCustomSentence = useCallback(
    ({ es, en }: { es: string; en: string }): SrsCustomCard | null => {
      const trimmedEs = (es ?? '').trim()
      const trimmedEn = (en ?? '').trim()
      if (!trimmedEs || !trimmedEn) return null
      const id = makeId('custom')
      let created: SrsCustomCard | null = null
      commit((draft) => {
        const card: SrsCustomCard = {
          id,
          type: 'custom',
          front: { es: trimmedEs, en: trimmedEn },
          createdAt: Date.now(),
          srs: { ...createInitialSRSState(0) } as SrsCardSrs,
        }
        draft.cards[id] = card
        draft.order.push(id)
        created = card
        return draft
      })
      return created
    },
    [commit],
  )

  const registerVerb = useCallback(
    (verb: VerbToRegister): SrsVerbCard | null => {
      if (!verb) return null
      const verbId = verb.id ?? null
      const infinitivo = verb.infinitivo ?? {}
      const ingSlug = infinitivo?.ing?.trim?.() ?? null
      if (ingSlug == null && verbId == null) return null

      const verbKey =
        verbId != null
          ? `id:${verbId}`
          : `slug:${String(ingSlug).toLowerCase()}`

      let found: SrsVerbCard | null = null
      for (const id of Object.keys(store.cards)) {
        const c = store.cards[id]
        if (c && c.type === 'verb' && c.verbKey === verbKey) {
          found = c
          break
        }
      }
      if (found) return found

      const id = makeId('verb')
      let created: SrsVerbCard | null = null
      commit((draft) => {
        const card: SrsVerbCard = {
          id,
          type: 'verb',
          verbKey,
          infinitivo: {
            ing: infinitivo?.ing ?? '',
            esp: infinitivo?.esp ?? '',
          },
          createdAt: Date.now(),
          srs: { ...createInitialSRSState(0) } as SrsCardSrs,
        }
        draft.cards[id] = card
        draft.order.push(id)
        created = card
        return draft
      })
      return created
    },
    [commit, store.cards],
  )

  const gradeCard = useCallback(
    (cardId: string, grade: Grade): void => {
      commit((draft) => {
        const card = draft.cards[cardId]
        if (!card) return draft
        const next = calculateNextReview(
          card.srs?.interval ?? 0,
          card.srs?.ef ?? 2.5,
          grade,
        )
        card.srs = {
          interval: next.interval,
          ef: next.ef,
          repetitions: next.repetitions,
          nextReview: next.nextReview,
          lastReviewed: next.lastReviewed ?? undefined,
        }
        return draft
      })
    },
    [commit],
  )

  const removeCard = useCallback(
    (cardId: string): void => {
      commit((draft) => {
        delete draft.cards[cardId]
        draft.order = draft.order.filter((id) => id !== cardId)
        return draft
      })
    },
    [commit],
  )

  const editCustomCard = useCallback(
    (cardId: string, { es, en }: { es: string; en: string }): SrsCustomCard | null => {
      const trimmedEs = (es ?? '').trim()
      const trimmedEn = (en ?? '').trim()
      if (!trimmedEs || !trimmedEn) return null

      const existing = store.cards[cardId]
      if (!existing || existing.type !== 'custom') return null

      let updated: SrsCustomCard | null = null
      commit((draft) => {
        const card = draft.cards[cardId]
        if (!card || card.type !== 'custom') return draft
        card.front = { es: trimmedEs, en: trimmedEn }
        updated = card
        return draft
      })
      return updated
    },
    [commit, store.cards],
  )

  const replaceStore = useCallback((incoming: SrsStore | null | undefined): boolean => {
    if (!incoming || typeof incoming !== 'object') return false
    const safe: SrsStore = {
      version: 1,
      cards:
        incoming.cards && typeof incoming.cards === 'object' && incoming.cards !== null
          ? incoming.cards
          : {},
      order: Array.isArray(incoming.order) ? incoming.order : [],
    }
    const theme = readThemeFromLocalStorage()
    const currentHash = calculateStoreHash(storeRef.current, theme)
    const incomingHash = calculateStoreHash(safe, theme)
    if (currentHash === incomingHash) return false
    setStore(safe)
    writeStore(safe)
    setRevision((r) => r + 1)
    return true
  }, [])

  const allCards = store.order
    .map((id) => store.cards[id])
    .filter((c): c is SrsCard => Boolean(c))

  const dueCards = allCards.filter((c) => isDue(c.srs ?? null))
  const dueCount = dueCards.length
  const totalCount = allCards.length
  const customCount = allCards.filter((c) => c.type === 'custom').length
  const verbCount = allCards.filter((c) => c.type === 'verb').length

  return {
    cards: allCards,
    cardsById: store.cards,
    dueCount,
    totalCount,
    customCount,
    verbCount,
    dueCards,
    revision,
    addCustomSentence,
    registerVerb,
    gradeCard,
    removeCard,
    editCustomCard,
    replaceStore,
  }
}
