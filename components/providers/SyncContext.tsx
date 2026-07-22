'use client'
import { createContext, useContext } from 'react'
import type { SyncApi } from '@/lib/types/sync'

const SyncContext = createContext<SyncApi | null>(null)

export function SyncProvider({ value, children }: { value: SyncApi; children: React.ReactNode }) {
  return <SyncContext.Provider value={value}>{children}</SyncContext.Provider>
}

export function useSyncContext(): SyncApi {
  const ctx = useContext(SyncContext)
  if (!ctx) {
    throw new Error('useSyncContext must be used inside a <SyncProvider>')
  }
  return ctx
}
