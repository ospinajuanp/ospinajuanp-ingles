'use client'
import { createContext, useContext } from 'react'
import type { FlatVerb, Verb, ConjugationGridEntry, OracionFillable } from '@/lib/types/verbs'

export interface VerbosApi {
  loading: boolean
  error: Error | null
  search: string
  setSearch: (next: string) => void
  category: string
  setCategory: (next: string) => void
  subcategory: string
  setSubcategory: (next: string) => void
  categories: { category: string; subcategories: string[] }[]
  counts: {
    total: number
    byCategory: Map<string, { total: number; sub: Map<string, number> }>
    bySubcategory: Map<string, number>
    subTotal: (cat: string) => number
    subForCategory: (cat: string) => number
  }
  filtered: FlatVerb[]
  currentIndex: number
  current: FlatVerb | null
  currentVerb: Verb | null
  oraciones: readonly OracionFillable[]
  conjugationEntries: readonly ConjugationGridEntry[]
  dueCount: number
  next: () => void
  prev: () => void
  shuffle: () => void
  goTo: (idx: number) => void
  goToRandomVerb: () => void
  total: number
  verbSelector: string | null
  reportEnrichment: (
    verb: Verb,
    enrichment: { imagen_url: string; image_source: string; audio_url: string | null; audio_source: string },
  ) => void
}

const VerbContext = createContext<VerbosApi | null>(null)

export function VerbProvider({ value, children }: { value: VerbosApi; children: React.ReactNode }) {
  return <VerbContext.Provider value={value}>{children}</VerbContext.Provider>
}

export function useVerbosContext(): VerbosApi {
  const ctx = useContext(VerbContext)
  if (!ctx) {
    throw new Error('useVerbosContext must be used inside a <VerbProvider>')
  }
  return ctx
}
