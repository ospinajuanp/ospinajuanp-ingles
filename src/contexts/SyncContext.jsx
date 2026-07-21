/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext } from 'react'

const SyncContext = createContext(null)

export function SyncProvider({ value, children }) {
  return <SyncContext.Provider value={value}>{children}</SyncContext.Provider>
}

export function useSyncContext() {
  const ctx = useContext(SyncContext)
  return ctx
}