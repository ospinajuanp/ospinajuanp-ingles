// localStorage-backed SRS store for both:
//   • custom sentences created by the user (Mazo Personalizado)
//   • verbs auto-registered the first time the user views them
//     in the main app (Mazo de Verbos Vistos)
//
// JSON schema stored under LOCAL_STORAGE_KEY:
//
//   {
//     version: 1,
//     cards: {
//       [cardId]: {
//         id: string,
//         type: 'custom' | 'verb',
//         // custom only
//         front: { es: string, en: string },
//         // verb only
//         verbId: number|null, verbKey: string,
//         infinitivo: { ing: string, esp: string },
//         // shared
//         createdAt: number,
//         srs: { interval, ef, repetitions, lastReviewed, nextReview },
//       },
//       ...
//     },
//     order: string[]   // FIFO insertion order
//   }
//
// All mutations go through one reducer (`commit`) that writes back to
// localStorage synchronously. The hook itself is a thin React wrapper
// that re-reads from the same source of truth on every change — no
// duplicate in-memory cache to keep in sync. Cross-tab updates are
// observed via the `storage` event.

import { useCallback, useEffect, useState } from 'react'
import {
  createInitialSRSState,
  calculateNextReview,
  isDue,
} from '../utils/srs'

const LOCAL_STORAGE_KEY = 'ospinajuanp-ingles:srs:v1'

function readStore() {
  if (typeof window === 'undefined') return emptyStore()
  try {
    const raw = window.localStorage.getItem(LOCAL_STORAGE_KEY)
    if (!raw) return emptyStore()
    const parsed = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object') return emptyStore()
    return {
      version: 1,
      cards: parsed.cards && typeof parsed.cards === 'object' ? parsed.cards : {},
      order: Array.isArray(parsed.order) ? parsed.order : [],
    }
  } catch {
    return emptyStore()
  }
}

function emptyStore() {
  return { version: 1, cards: {}, order: [] }
}

function writeStore(store) {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(store))
  } catch {
    // Private mode / quota — silently ignore. UI keeps working from memory.
  }
}

function makeId(prefix) {
  const rand = Math.random().toString(36).slice(2, 10)
  return `${prefix}_${Date.now().toString(36)}_${rand}`
}

export function useSRS() {
  const [store, setStore] = useState(() => readStore())

  // Cross-tab sync: another tab wrote to the same key, pull it in.
  useEffect(() => {
    function onStorage(e) {
      if (e.key !== LOCAL_STORAGE_KEY) return
      setStore(readStore())
    }
    window.addEventListener('storage', onStorage)
    return () => window.removeEventListener('storage', onStorage)
  }, [])

  const commit = useCallback((updater) => {
    setStore((prev) => {
      const draft = {
        version: 1,
        cards: { ...prev.cards },
        order: [...prev.order],
      }
      const next = updater(draft)
      // Guard: if a caller forgets `return draft`, `setStore(undefined)`
      // would nuke the store on the next render. Default to returning
      // the draft in that case.
      const safeNext =
        next && typeof next === 'object' && next.cards && next.order
          ? next
          : draft
      writeStore(safeNext)
      return safeNext
    })
  }, [])

  // ── Mutations ────────────────────────────────────────────────────────

  const addCustomSentence = useCallback(
    ({ es, en }) => {
      const trimmedEs = (es ?? '').trim()
      const trimmedEn = (en ?? '').trim()
      if (!trimmedEs || !trimmedEn) return null
      const id = makeId('custom')
      let created = null
      commit((draft) => {
        draft.cards[id] = {
          id,
          type: 'custom',
          front: { es: trimmedEs, en: trimmedEn },
          createdAt: Date.now(),
          srs: createInitialSRSState(0),
        }
        draft.order.push(id)
        created = draft.cards[id]
        return draft
      })
      return created
    },
    [commit],
  )

  /**
   * Register a verb card. Idempotent per verb — repeated calls are a no-op.
   * Pass the same `verb` object that `useVerbos` exposes (`verb.infinitivo`,
   * `verb.id`).
   */
  const registerVerb = useCallback(
    (verb) => {
      if (!verb) return null
      const verbId = verb.id ?? null
      const infinitivo = verb.infinitivo ?? {}
      const ingSlug = infinitivo?.ing?.trim?.() ?? null
      if (ingSlug == null && verbId == null) return null

      const verbKey =
        verbId != null
          ? `id:${verbId}`
          : `slug:${String(ingSlug).toLowerCase()}`

      // Look up an existing card for this verb in the current store snapshot.
      // We read store.cards directly (not the draft) so this is safe to
      // call inside another commit's updater if needed.
      let found = null
      for (const id of Object.keys(store.cards)) {
        const c = store.cards[id]
        if (c?.type === 'verb' && c.verbKey === verbKey) {
          found = c
          break
        }
      }
      if (found) return found

      const id = makeId('verb')
      let created = null
      commit((draft) => {
        draft.cards[id] = {
          id,
          type: 'verb',
          verbId,
          verbKey,
          infinitivo: {
            ing: infinitivo?.ing ?? '',
            esp: infinitivo?.esp ?? '',
          },
          createdAt: Date.now(),
          srs: createInitialSRSState(0),
        }
        draft.order.push(id)
        created = draft.cards[id]
        return draft
      })
      return created
    },
    [commit, store.cards],
  )

  const gradeCard = useCallback(
    (cardId, grade) => {
      commit((draft) => {
        const card = draft.cards[cardId]
        if (!card) return draft
        const next = calculateNextReview(
          card.srs.interval,
          card.srs.ef,
          grade,
        )
        card.srs = { ...card.srs, ...next }
        return draft
      })
    },
    [commit],
  )

  const removeCard = useCallback(
    (cardId) => {
      commit((draft) => {
        delete draft.cards[cardId]
        draft.order = draft.order.filter((id) => id !== cardId)
        return draft
      })
    },
    [commit],
  )

  /**
   * Edit a custom sentence's front fields (es/en). Only `type: 'custom'`
   * cards are editable; verb cards come from the official dataset and are
   * immutable on the SRS side. SRS state (interval/ef/repetitions/etc.)
   * is preserved — editing the prompt does not reset the schedule.
   * Returns the updated card or `null` if the id is missing / not custom.
   */
  const editCustomCard = useCallback(
    (cardId, { es, en }) => {
      const trimmedEs = (es ?? '').trim()
      const trimmedEn = (en ?? '').trim()
      if (!trimmedEs || !trimmedEn) return null

      const existing = store.cards[cardId]
      if (!existing || existing.type !== 'custom') return null

      let updated = null
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

  // ── Selectors (derived state — safe to recompute every render) ───────

  const allCards = store.order
    .map((id) => store.cards[id])
    .filter(Boolean)

  const dueCards = allCards.filter((c) => isDue(c.srs))
  const dueCount = dueCards.length
  const totalCount = allCards.length
  const customCount = allCards.filter((c) => c.type === 'custom').length
  const verbCount = allCards.filter((c) => c.type === 'verb').length

  return {
    // raw
    cards: allCards,
    cardsById: store.cards,

    // counts
    dueCount,
    totalCount,
    customCount,
    verbCount,

    // lists
    dueCards,

    // actions
    addCustomSentence,
    registerVerb,
    gradeCard,
    removeCard,
    editCustomCard,
  }
}
