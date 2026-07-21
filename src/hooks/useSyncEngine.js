// Local-first silent sync engine.
//
// Architecture in one paragraph:
//
//   • The UI reads/writes only localStorage. Nothing in this hook blocks
//     the first paint or the first interaction.
//   • On mount (and whenever the syncToken changes) we lazily GET the
//     remote snapshot from Atlas. We hash the local state and the remote
//     state with FNV-1a (see syncHash.js) and short-circuit if they
//     match — no merge work, no React updates, no re-render flicker.
//     Otherwise we LWW-merge (see syncMerge.js) and call `replaceStore`
//     on the SRS context. The theme is mirrored the same way.
//   • Whenever the local SRS store mutates (we watch a `revision`
//     counter exposed by useSRS) or the theme changes, we re-hash the
//     current state and compare against `lastSyncedHashRef`. If the hash
//     is unchanged we abort the debounce timer entirely (no network
//     call). Otherwise we debounce-push 2s after the last edit.
//   • `pushCurrent` itself re-checks the hash and short-circuits to a
//     no-op if the local state hasn't changed since the last successful
//     sync — this catches the pagehide flush + 5-min safety-net firing
//     with no real mutations.
//   • On `visibilitychange → hidden` or `pagehide` we flush any pending
//     push synchronously (`keepalive: true` on the server).
//   • A periodic 5-minute safety-net re-push catches edge cases (rapid
//     tab close, races between merge + user commit). The hash check
//     inside `pushCurrent` makes this safe — if nothing changed, the
//     safety-net just records a "synced" status without a network call.
//
// Why a custom hook rather than embedding the logic inside useSRS:
//   - Keeps useSRS focused on its single responsibility (SRS state).
//   - The engine is fully optional — disabling it (e.g. for tests or
//     for users who explicitly opt out) is as simple as not mounting
//     the engine.
//
// Anti-flicker design notes:
//   - `lastSyncedHashRef` is a useRef, NOT useState — it's never read
//     during render, so writing to it doesn't trigger re-renders. It's
//     only used inside callbacks and effects.
//   - `replaceStore` (in useSRS.js) ALSO hash-checks before calling
//     `setStore` + `writeStore` + bumping `revision`. So even if the
//     engine's hash check missed something, the SRS layer itself is
//     idempotent against no-op merges.
//   - The previous `skipNextPushRef` escape hatch was REMOVED. With the
//     hash check in place, the next mutation watcher fire naturally
//     sees `currentHash === lastSyncedHashRef` after a no-op merge
//     and skips the debounce. After a real merge, the watcher correctly
//     schedules a push because the merged state has a new hash.

import { useCallback, useEffect, useRef, useState } from 'react'
import { fetchUserState, pushUserState } from '../utils/syncClient'
import {
  getSyncToken,
  linkSyncToken,
  resetSyncToken,
  isValidSyncToken,
} from '../utils/syncIdentity'
import { compareStatesByHash, shouldPushLocal } from '../utils/syncMerge'
import { calculateStoreHash, readThemeFromLocalStorage } from '../utils/syncHash'

const PUSH_DEBOUNCE_MS = 2000
const SAFETY_NET_PUSH_MS = 5 * 60 * 1000
const LINK_QUERY_PARAM = 'syncToken'

function readSRSFromLocalStorage() {
  if (typeof window === 'undefined') return { version: 1, cards: {}, order: [] }
  try {
    const raw = window.localStorage.getItem('ospinajuanp-ingles:srs:v1')
    if (!raw) return { version: 1, cards: {}, order: [] }
    const parsed = JSON.parse(raw)
    return {
      version: 1,
      cards:
        parsed && typeof parsed.cards === 'object' && parsed.cards !== null
          ? parsed.cards
          : {},
      order: Array.isArray(parsed?.order) ? parsed.order : [],
    }
  } catch {
    return { version: 1, cards: {}, order: [] }
  }
}

/**
 * Adopt a syncToken from the URL if present and valid. Strips the
 * query param to avoid leaking the token in browser history and in
 * shared links after the page has loaded.
 */
export function consumeLinkTokenFromUrl() {
  if (typeof window === 'undefined') return null
  try {
    const url = new URL(window.location.href)
    const raw = url.searchParams.get(LINK_QUERY_PARAM)
    if (!raw) return null
    if (!isValidSyncToken(raw)) return null
    url.searchParams.delete(LINK_QUERY_PARAM)
    window.history.replaceState({}, '', url.toString())
    return raw
  } catch {
    return null
  }
}

/**
 * Build the absolute URL a QR should encode so the second device can
 * open it and auto-adopt the token. Falls back to the SPA origin if
 * `window` is not available (SSR / tests).
 */
export function buildLinkUrl(token) {
  if (!token) return ''
  if (typeof window === 'undefined') return `?${LINK_QUERY_PARAM}=${token}`
  const base = `${window.location.origin}${window.location.pathname}`
  return `${base}?${LINK_QUERY_PARAM}=${encodeURIComponent(token)}`
}

/**
 * Hash of the current local sync state. Read from localStorage so the
 * engine doesn't depend on React state being up-to-date (e.g. inside
 * pagehide handlers or inside async callbacks fired from the bootstrap
 * pull). Cheap: ~10 microseconds for a typical deck.
 */
function hashCurrentLocalState() {
  return calculateStoreHash(
    readSRSFromLocalStorage(),
    readThemeFromLocalStorage(),
  )
}

export function useSyncEngine({ srs, themeApi }) {
  const [syncToken, setSyncToken] = useState(() => {
    // URL wins (user just scanned a QR or clicked a link) over the
    // previously-stored token, so the merge targets the right device.
    const fromUrl = consumeLinkTokenFromUrl()
    if (fromUrl) {
      linkSyncToken(fromUrl)
      return fromUrl
    }
    return getSyncToken()
  })

  const [status, setStatus] = useState('idle') // 'idle' | 'pulling' | 'pushing' | 'synced' | 'error'
  const [lastError, setLastError] = useState(null)
  const [lastSyncedAt, setLastSyncedAt] = useState(null)
  const [pendingPush, setPendingPush] = useState(false)

  // ── lastSyncedHashRef ───────────────────────────────────────────────
  // Hash of the last state we KNOW is synced with Atlas. Updated after
  // a successful push OR after a pull that confirmed Atlas's state
  // matches ours (no-op merge).
  //
  // Used by:
  //   • the mutation watcher (skip the debounce if the user-visible
  //     state hasn't actually changed since the last sync), and
  //   • `pushCurrent` itself (skip the network call entirely if
  //     called from pagehide / safety-net with nothing new to send).
  //
  // This is a useRef, not useState — it's never read during render,
  // so writes don't trigger re-renders. It's also the replacement for
  // the old `skipNextPushRef` escape hatch.
  const lastSyncedHashRef = useRef(null)

  // Latest refs of the SRS + theme APIs. We need them inside async
  // callbacks that we want to keep stable across re-renders. Keeping
  // the ref in sync is done inside an effect (NOT during render) to
  // satisfy the React 19 hooks purity rules.
  const srsRef = useRef(srs)
  const themeApiRef = useRef(themeApi)
  useEffect(() => {
    srsRef.current = srs
  }, [srs])
  useEffect(() => {
    themeApiRef.current = themeApi
  }, [themeApi])

  // ── Apply remote snapshot to local SRS + theme ───────────────────────
  // Hash-compares first; if local matches remote we skip everything.
  // Otherwise runs the LWW merge and applies it.
  const applyRemote = useCallback((remote) => {
    if (!remote || typeof remote !== 'object') return false

    const localStore = readSRSFromLocalStorage()
    const localTheme = readThemeFromLocalStorage()
    const remoteStore = remote.srsStore
    const remoteTheme = typeof remote.theme === 'string' ? remote.theme : null

    const result = compareStatesByHash({
      localStore,
      localTheme,
      remoteStore,
      remoteTheme,
    })

    // No-op: local already matches remote exactly. Record the hash so
    // the mutation watcher doesn't schedule a follow-up push.
    if (!result.hasChanges) {
      lastSyncedHashRef.current = result.hash
      return false
    }

    let touchedSRS = false
    let touchedTheme = false

    if (
      result.mergedStore &&
      srsRef.current?.replaceStore
    ) {
      // replaceStore itself runs a hash check; it may still no-op if
      // only the theme differed (SRS unchanged). Either way, we rely
      // on its boolean return to know if anything actually changed.
      if (srsRef.current.replaceStore(result.mergedStore)) {
        touchedSRS = true
      }
    }

    if (
      remoteTheme &&
      themeApiRef.current?.theme &&
      remoteTheme !== themeApiRef.current.theme &&
      themeApiRef.current.setTheme
    ) {
      themeApiRef.current.setTheme(remoteTheme)
      touchedTheme = true
    }

    // Only mark `lastSyncedHashRef` if at least one side actually
    // changed. Otherwise we'd be lying about Atlas having the latest
    // state — and we'd accidentally swallow a subsequent user edit
    // that differs only because of a still-pending local mutation.
    //
    // When `touched` is false (remote had data but local already
    // matched it), the hash short-circuit above already updated the
    // ref. When `touched` is true, we leave the ref as-is — the merge
    // result may include local-only cards not yet on Atlas, so the
    // mutation watcher should push the merged state back to Atlas.
    return touchedSRS || touchedTheme
  }, [])

  // ── Push current local snapshot ──────────────────────────────────────
  // Closes over `syncToken` directly (no ref dance). The push effect
  // already depends on `syncToken`, so pushCurrent is recreated safely
  // when the token changes — and the visibility / interval handlers
  // re-bind to the new closure via their own syncToken deps.
  const pushCurrent = useCallback(async () => {
    if (!syncToken) return
    const srsStore = readSRSFromLocalStorage()
    const theme = readThemeFromLocalStorage()
    const currentHash = calculateStoreHash(srsStore, theme)

    // No-op sync: nothing has changed since the last successful push.
    // This is the common case for the 5-min safety-net + pagehide flush
    // when the user has been idle. Record a "synced" status without
    // hitting the network.
    if (currentHash === lastSyncedHashRef.current) {
      setPendingPush(false)
      setStatus('synced')
      return
    }

    setStatus('pushing')
    setPendingPush(false)
    const res = await pushUserState({ syncToken, srsStore, theme })
    if (res.ok) {
      setStatus('synced')
      setLastError(null)
      setLastSyncedAt(Date.now())
      lastSyncedHashRef.current = currentHash
    } else {
      setStatus('error')
      setLastError(res.reason ?? `HTTP ${res.status ?? '???'}`)
      // Intentionally do NOT update lastSyncedHashRef on failure — we
      // want the next mutation watcher / safety-net to retry.
    }
  }, [syncToken])

  // ── Bootstrap: pull on mount / token change ──────────────────────────
  useEffect(() => {
    if (!syncToken) return
    let cancelled = false

    async function pull() {
      setStatus('pulling')
      const res = await fetchUserState(syncToken)
      if (cancelled) return
      if (!res.ok) {
        setStatus('error')
        setLastError(res.reason ?? `HTTP ${res.status ?? '???'}`)
        return
      }
      const remote = res.state
      if (!remote) {
        // No remote record yet — bootstrap by pushing whatever the user
        // already has locally. Silent, idempotent.
        const local = readSRSFromLocalStorage()
        if (shouldPushLocal(local, null)) {
          await pushCurrent()
        } else {
          // Both sides are empty: mark synced and lock in the hash so
          // the mutation watcher doesn't try to push an empty deck.
          setStatus('synced')
          lastSyncedHashRef.current = hashCurrentLocalState()
        }
        return
      }
      // If remote is empty AND local is empty too, mark synced and bail.
      const localNow = readSRSFromLocalStorage()
      const remoteHasCards =
        remote.srsStore && Object.keys(remote.srsStore.cards ?? {}).length > 0
      if (!remoteHasCards && Object.keys(localNow.cards).length === 0) {
        setStatus('synced')
        lastSyncedHashRef.current = hashCurrentLocalState()
        return
      }
      applyRemote(remote)
      setStatus('synced')
      setLastSyncedAt(Date.now())
    }

    pull().catch((err) => {
      if (cancelled) return
      console.warn('[sync-engine] pull crashed:', err)
      setStatus('error')
      setLastError(err?.message ?? String(err))
    })

    return () => {
      cancelled = true
    }
  }, [syncToken, applyRemote, pushCurrent])

  // ── Debounced push on local mutations (SRS revision + theme) ─────────
  // Hash short-circuit: if the current local state hashes to the same
  // value as the last known-synced state, skip the debounce entirely.
  // This catches "the context re-rendered but nothing actually changed"
  // (StrictMode double-invoke, hot-reload, parent re-renders).
  const srsRevision = srs?.revision
  const currentTheme = themeApi?.theme
  useEffect(() => {
    if (!syncToken) return
    const currentHash = hashCurrentLocalState()
    if (currentHash === lastSyncedHashRef.current) {
      // No-op: nothing to push. Reset pendingPush in case it was true
      // from a previous race, but otherwise stay quiet.
      setPendingPush(false)
      return
    }
    setPendingPush(true)
    const timer = setTimeout(() => {
      pushCurrent()
    }, PUSH_DEBOUNCE_MS)
    return () => clearTimeout(timer)
    // We deliberately depend on the primitive counters (revision +
    // theme) rather than the full srs/themeApi objects. The effect
    // only cares about "did the user-visible state change?", not about
    // identity churn of the wrapper objects.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [syncToken, srsRevision, currentTheme])

  // ── Flush on tab hide / pagehide so the last edit isn't lost ─────────
  useEffect(() => {
    if (!syncToken) return
    function flush() {
      // Read localStorage directly (don't depend on React state being
      // current in a pagehide handler) AND hash before calling
      // pushCurrent — pushCurrent itself does the same check, but
      // doing it here avoids even setting the pendingPush flag.
      const currentHash = hashCurrentLocalState()
      if (currentHash === lastSyncedHashRef.current) return
      const local = readSRSFromLocalStorage()
      const hasCards = Object.keys(local.cards ?? {}).length > 0
      if (!hasCards) return
      pushCurrent()
    }
    function onVisibility() {
      if (document.visibilityState === 'hidden') flush()
    }
    document.addEventListener('visibilitychange', onVisibility)
    window.addEventListener('pagehide', flush)
    return () => {
      document.removeEventListener('visibilitychange', onVisibility)
      window.removeEventListener('pagehide', flush)
    }
  }, [syncToken, pushCurrent])

  // ── Periodic safety-net push ─────────────────────────────────────────
  // The hash check inside pushCurrent makes this safe: if the user has
  // been idle, the safety-net is a no-op (no network call).
  useEffect(() => {
    if (!syncToken) return
    const timer = setInterval(() => {
      pushCurrent()
    }, SAFETY_NET_PUSH_MS)
    return () => clearInterval(timer)
  }, [syncToken, pushCurrent])

  // ── Public actions for the modal UI ──────────────────────────────────
  const linkNewToken = useCallback((token) => {
    if (!isValidSyncToken(token)) return false
    linkSyncToken(token)
    setSyncToken(token)
    setStatus('pulling')
    setLastError(null)
    // Reset the hash ref so the bootstrap pull on the new token starts
    // with a clean slate.
    lastSyncedHashRef.current = null
    return true
  }, [])

  const unlink = useCallback(() => {
    resetSyncToken()
    const fresh = getSyncToken()
    setSyncToken(fresh)
    setStatus('pulling')
    setLastError(null)
    lastSyncedHashRef.current = null
  }, [])

  const forcePushNow = useCallback(() => {
    pushCurrent()
  }, [pushCurrent])

  const forcePullNow = useCallback(async () => {
    setStatus('pulling')
    const res = await fetchUserState(syncToken)
    if (res.ok && res.state) {
      applyRemote(res.state)
      setStatus('synced')
      setLastSyncedAt(Date.now())
    } else if (res.ok) {
      setStatus('synced')
      lastSyncedHashRef.current = hashCurrentLocalState()
    } else {
      setStatus('error')
      setLastError(res.reason ?? `HTTP ${res.status ?? '???'}`)
    }
  }, [syncToken, applyRemote])

  return {
    syncToken,
    status,
    lastError,
    lastSyncedAt,
    pendingPush,
    linkNewToken,
    unlink,
    forcePushNow,
    forcePullNow,
  }
}