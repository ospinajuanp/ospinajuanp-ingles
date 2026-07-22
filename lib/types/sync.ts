import type { SrsStore } from './srs'
import type { ThemeId } from './theme'

export type SyncStatus = 'idle' | 'pulling' | 'pushing' | 'synced' | 'error'

export interface SyncUserState {
  syncToken: string
  createdAt?: string
  lastActiveAt?: string
  srsStore: SrsStore | null
  theme: ThemeId | null
}

export interface SyncApi {
  status: SyncStatus
  syncToken: string
  lastError: string | null
  lastSyncedAt: number | null
  pendingPush: boolean
  forcePullNow: () => void
  forcePushNow: () => void
  linkNewToken: (token: string) => boolean
  unlink: () => void
}
