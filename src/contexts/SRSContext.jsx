/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext } from 'react'

const SRSContext = createContext(null)

export function SRSProvider({ value, children }) {
  return <SRSContext.Provider value={value}>{children}</SRSContext.Provider>
}

export function useSRSContext() {
  const ctx = useContext(SRSContext)
  if (!ctx) {
    throw new Error('useSRSContext must be used inside a <SRSProvider>')
  }
  return ctx
}
