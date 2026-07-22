'use client'
import { useCallback, useEffect, useRef, useState } from 'react'
import { fetchUserState, pushUserState } from '@/lib/utils/syncClient'
import {
  getSyncToken,
  linkSyncToken,
  resetSyncToken,
  isValidSyncToken,
} from '@/lib/utils/syncIdentity'
import { compareStatesByHash, shouldPushLocal } from '@/lib/utils/syncMerge'
import { calculateStoreHash, readThemeFromLocalStorage } from '@/lib/utils/syncHash'
import type { SrsApi } from '@/lib/types/srs'
import type { ThemeApi, ThemeId } from '@/lib/types/theme'
import type { SyncApi, SyncStatus, SyncUserState } from '@/lib/types/sync'
import type { SrsStore } from '@/lib/types/srs'

const PUSH_DEBOUNCE_MS = 2000
const SAFETY_NET_PUSH_MS = 5 * 60 * 1000
const LINK_QUERY_PARAM = 'syncToken'

function readSRSFromLocalStorage(): SrsStore {
  if (typeof window === 'undefined') return { version: 1, cards: {}, order: [] }
  try {
    const raw = window.localStorage.getItem('ospinajuanp-ingles:srs:v1')
    if (!raw) return { version: 1, cards: {}, order: [] }
    const parsed: unknown = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object') return { version: 1, cards: {}, order: [] }
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
    return { version: 1, cards: {}, order: [] }
  }
}

export function consumeLinkTokenFromUrl(): string | null {
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

export function buildLinkUrl(token: string): string {
  if (!token) return ''
  if (typeof window === 'undefined') return `?${LINK_QUERY_PARAM}=${token}`
  const base = `${window.location.origin}${window.location.pathname}`
  return `${base}?${LINK_QUERY_PARAM}=${encodeURIComponent(token)}`
}

function hashCurrentLocalState(): string {
  return calculateStoreHash(
    readSRSFromLocalStorage(),
    (readThemeFromLocalStorage() ?? null) as ThemeId | null,
  )
}

interface UseSyncEngineInput {
  srs: SrsApi | null
  themeApi: ThemeApi | null
}

export function useSyncEngine({ srs, themeApi }: UseSyncEngineInput): SyncApi {
  const [syncToken, setSyncToken] = useState<string>(() => {
    const fromUrl = consumeLinkTokenFromUrl()
    if (fromUrl) {
      linkSyncToken(fromUrl)
      return fromUrl
    }
    return getSyncToken()
  })

  const [status, setStatus] = useState<SyncStatus>('idle')
  const [lastError, setLastError] = useState<string | null>(null)
  const [lastSyncedAt, setLastSyncedAt] = useState<number | null>(null)
  const [pendingPush, setPendingPush] = useState(false)

  const lastSyncedHashRef = useRef<string | null>(null)

  const srsRef = useRef(srs)
  const themeApiRef = useRef(themeApi)
  useEffect(() => {
    srsRef.current = srs
  }, [srs])
  useEffect(() => {
    themeApiRef.current = themeApi
  }, [themeApi])

  const applyRemote = useCallback((remote: SyncUserState | null): boolean => {
    if (!remote || typeof remote !== 'object') return false

    const localStore = readSRSFromLocalStorage()
    const localTheme = readThemeFromLocalStorage()
    const remoteStore = remote.srsStore
    const remoteTheme = typeof remote.theme === 'string' ? remote.theme : null

    const result = compareStatesByHash({
      localStore,
      localTheme: (localTheme ?? null) as ThemeId | null,
      remoteStore,
      remoteTheme: (remoteTheme ?? null) as ThemeId | null,
    })

    if (!result.hasChanges) {
      lastSyncedHashRef.current = result.hash
      return false
    }

    let touchedSRS = false
    let touchedTheme = false

    if (result.mergedStore && srsRef.current?.replaceStore) {
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

    return touchedSRS || touchedTheme
  }, [])

  const pushCurrent = useCallback(async (): Promise<void> => {
    if (!syncToken) return
    const srsStore = readSRSFromLocalStorage()
    const theme = readThemeFromLocalStorage()
    const currentHash = calculateStoreHash(srsStore, (theme ?? null) as ThemeId | null)

    if (currentHash === lastSyncedHashRef.current) {
      setPendingPush(false)
      setStatus('synced')
      return
    }

    setStatus('pushing')
    setPendingPush(false)
    const res = await pushUserState({
      syncToken,
      srsStore,
      theme: (theme ?? null) as ThemeId | null,
    })
    if (res.ok) {
      setStatus('synced')
      setLastError(null)
      setLastSyncedAt(Date.now())
      lastSyncedHashRef.current = currentHash
    } else {
      setStatus('error')
      const reason = 'reason' in res && res.reason ? res.reason : `HTTP ${res.status ?? '???'}`
      setLastError(reason)
    }
  }, [syncToken])

  useEffect(() => {
    if (!syncToken) return
    let cancelled = false

    async function pull(): Promise<void> {
      setStatus('pulling')
      const res = await fetchUserState(syncToken)
      if (cancelled) return
      if (!res.ok) {
        setStatus('error')
        const reason = 'reason' in res && res.reason ? res.reason : `HTTP ${res.status ?? '???'}`
        setLastError(reason)
        return
      }
      const remote = res.state ?? null
      if (!remote) {
        const local = readSRSFromLocalStorage()
        if (shouldPushLocal(local, null)) {
          await pushCurrent()
        } else {
          setStatus('synced')
          lastSyncedHashRef.current = hashCurrentLocalState()
        }
        return
      }
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

    pull().catch((err: unknown) => {
      if (cancelled) return
      const message = err instanceof Error ? err.message : String(err)
      console.warn('[sync-engine] pull crashed:', message)
      setStatus('error')
      setLastError(message)
    })

    return () => {
      cancelled = true
    }
  }, [syncToken, applyRemote, pushCurrent])

  const srsRevision = srs?.revision
  const currentTheme = themeApi?.theme
  useEffect(() => {
    if (!syncToken) return
    const currentHash = hashCurrentLocalState()
    if (currentHash === lastSyncedHashRef.current) {
      setPendingPush(false)
      return
    }
    setPendingPush(true)
    const timer = setTimeout(() => {
      void pushCurrent()
    }, PUSH_DEBOUNCE_MS)
    return () => clearTimeout(timer)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [syncToken, srsRevision, currentTheme])

  useEffect(() => {
    if (!syncToken) return
    function flush(): void {
      const currentHash = hashCurrentLocalState()
      if (currentHash === lastSyncedHashRef.current) return
      const local = readSRSFromLocalStorage()
      const hasCards = Object.keys(local.cards ?? {}).length > 0
      if (!hasCards) return
      void pushCurrent()
    }
    function onVisibility(): void {
      if (document.visibilityState === 'hidden') flush()
    }
    document.addEventListener('visibilitychange', onVisibility)
    window.addEventListener('pagehide', flush)
    return () => {
      document.removeEventListener('visibilitychange', onVisibility)
      window.removeEventListener('pagehide', flush)
    }
  }, [syncToken, pushCurrent])

  useEffect(() => {
    if (!syncToken) return
    const timer = setInterval(() => {
      void pushCurrent()
    }, SAFETY_NET_PUSH_MS)
    return () => clearInterval(timer)
  }, [syncToken, pushCurrent])

  const linkNewToken = useCallback((token: string): boolean => {
    if (!isValidSyncToken(token)) return false
    linkSyncToken(token)
    setSyncToken(token)
    setStatus('pulling')
    setLastError(null)
    lastSyncedHashRef.current = null
    return true
  }, [])

  const unlink = useCallback((): void => {
    resetSyncToken()
    const fresh = getSyncToken()
    setSyncToken(fresh)
    setStatus('pulling')
    setLastError(null)
    lastSyncedHashRef.current = null
  }, [])

  const forcePushNow = useCallback((): void => {
    void pushCurrent()
  }, [pushCurrent])

  const forcePullNow = useCallback(async (): Promise<void> => {
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
      const reason = 'reason' in res && res.reason ? res.reason : `HTTP ${res.status ?? '???'}`
      setLastError(reason)
    }
  }, [syncToken, applyRemote])

  return {
    status,
    syncToken,
    lastError,
    lastSyncedAt,
    pendingPush,
    forcePullNow,
    forcePushNow,
    linkNewToken,
    unlink,
  }
}
