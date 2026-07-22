'use client'
import { createContext, useContext } from 'react'
import type { SrsApi } from '@/lib/types/srs'

const SRSContext = createContext<SrsApi | null>(null)

export function SRSProvider({ value, children }: { value: SrsApi; children: React.ReactNode }) {
  return <SRSContext.Provider value={value}>{children}</SRSContext.Provider>
}

export function useSRSContext(): SrsApi {
  const ctx = useContext(SRSContext)
  if (!ctx) {
    throw new Error('useSRSContext must be used inside a <SRSProvider>')
  }
  return ctx
}
