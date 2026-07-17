/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext } from 'react'

const VerbContext = createContext(null)

export function VerbProvider({ value, children }) {
  return <VerbContext.Provider value={value}>{children}</VerbContext.Provider>
}

export function useVerbosContext() {
  const ctx = useContext(VerbContext)
  if (!ctx) {
    throw new Error('useVerbosContext must be used inside a <VerbProvider>')
  }
  return ctx
}