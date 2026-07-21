// Local-first silent sync engine.
//
// Architecture in one paragraph:
//
//   • The UI reads/writes only localStorage. Nothing in this hook blocks
//     the first paint or the first interaction.
//   • On mount (and whenever the syncToken changes) we lazily GET the
//     remote snapshot from Atlas. If remote has data, we merge it with
//     the local SRS store via Last-Write-Wins (see syncMerge.js) and
//     call `replaceStore` on the SRS context. The theme is mirrored
//     the same way.
//   • Whenever the local SRS store mutates (we watch a `revision`
//     counter exposed by useSRS) or the theme changes, we debounce-push
//     the latest snapshot to Atlas 2s after the last edit. The push is
//     idempotent (server upserts by syncToken) so retries are safe.
//   • On `visibilitychange → hidden` or `pagehide` we flush any pending
//     push synchronously (`keepalive: true` on the server).
//   • A periodic 5-minute safety-net re-push catches edge cases (rapid
//     tab close, races between merge + user commit).
//
// Why a custom hook rather than embedding the logic inside useSRS:
//   - Keeps useSRS focused on its single responsibility (SRS state).
//   - The engine is fully optional — disabling it (e.g. for tests or
//     for users who explicitly opt out) is as simple as not mounting
//     the engine.

import { useCallback, useEffect, useRef, useState } from 'react'
import { fetchUserState, pushUserState } from '../utils/syncClient'
import {
  getSyncToken,
  linkSyncToken,
  resetSyncToken,
  isValidSyncToken,
} from '../utils/syncIdentity'
import { mergeSRSStores, shouldPushLocal } from '../utils/syncMerge'

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

function readThemeFromLocalStorage() {
  if (typeof window === 'undefined') return null
  try {
    return window.localStorage.getItem('ospinajuanp-ingles:theme')
  } catch {
    return null
  }
}

function shallowEqualStore(a, b) {
  if (!a || !b) return false
  if (a.version !== b.version) return false
  if (a.order?.length !== b.order?.length) return false
  const aCards = a.cards ?? {}
  const bCards = b.cards ?? {}
  const aKeys = Object.keys(aCards)
  const bKeys = Object.keys(bCards)
  if (aKeys.length !== bKeys.length) return false
  for (const k of aKeys) {
    if (!bCards[k]) return false
  }
  return true
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
  // Set by the merge path so the revision watcher ignores the bump
  // it just caused (otherwise we'd immediately push the merged state
  // back to Atlas — wasteful round-trip).
  const skipNextPushRef = useRef(false)

  const applyRemote = useCallback((remote) => {
    if (!remote || typeof remote !== 'object') return false

    const remoteSRS = remote.srsStore
    const remoteTheme = remote.theme

    let touchedSRS = false
    let touchedTheme = false

    if (
      remoteSRS &&
      typeof remoteSRS === 'object' &&
      remoteSRS.version === 1 &&
      srsRef.current?.replaceStore
    ) {
      const local = readSRSFromLocalStorage()
      const merged = mergeSRSStores(local, remoteSRS)
      if (!shallowEqualStore(merged, local)) {
        skipNextPushRef.current = true
        touchedSRS = srsRef.current.replaceStore(merged)
      }
    }

    if (
      remoteTheme &&
      themeApiRef.current?.theme &&
      remoteTheme !== themeApiRef.current.theme &&
      themeApiRef.current.setTheme
    ) {
      skipNextPushRef.current = true
      themeApiRef.current.setTheme(remoteTheme)
      touchedTheme = true
    }

    return touchedSRS || touchedTheme
  }, [])

  // ── Push current local snapshot ──────────────────────────────────────
  // Closes over `syncToken` directly (no ref dance). The push effect
  // already depends on `syncToken`, so pushCurrent is recreated safely
  // when the token changes — and the visibility / interval handlers
  // re-bind to the new closure via their own syncToken deps.
  const pushCurrent = useCallback(async () => {
    if (!syncToken) return
    setStatus('pushing')
    setPendingPush(false)
    const srsStore = readSRSFromLocalStorage()
    const theme = readThemeFromLocalStorage()
    const res = await pushUserState({ syncToken, srsStore, theme })
    if (res.ok) {
      setStatus('synced')
      setLastError(null)
      setLastSyncedAt(Date.now())
    } else {
      setStatus('error')
      setLastError(res.reason ?? `HTTP ${res.status ?? '???'}`)
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
          setStatus('synced')
        }
        return
      }
      // If remote is empty AND local is empty too, mark synced and bail.
      const localNow = readSRSFromLocalStorage()
      const remoteHasCards =
        remote.srsStore && Object.keys(remote.srsStore.cards ?? {}).length > 0
      if (!remoteHasCards && Object.keys(localNow.cards).length === 0) {
        setStatus('synced')
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
  const srsRevision = srs?.revision
  const currentTheme = themeApi?.theme
  useEffect(() => {
    if (!syncToken) return
    if (skipNextPushRef.current) {
      skipNextPushRef.current = false
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
      // Only flush if there's actually something to push. Read from
      // localStorage directly so we don't depend on React state being
      // up-to-date in a pagehide handler.
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
    return true
  }, [])

  const unlink = useCallback(() => {
    resetSyncToken()
    const fresh = getSyncToken()
    setSyncToken(fresh)
    setStatus('pulling')
    setLastError(null)
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