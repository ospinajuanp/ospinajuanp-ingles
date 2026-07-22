'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useParams, usePathname, useRouter } from 'next/navigation'
import { collectCategories, flattenVerbos, resolveVerb } from '@/lib/utils/flatten'
import { pickWeightedIndex } from '@/lib/utils/weightedRandom'
import { WEIGHT_MAP } from '@/lib/data/weightedVerbs'
import { syncVerbToMongo } from '@/lib/utils/mongoSync'
import { useSRSContext } from '@/components/providers/SRSContext'
import { checkPexelsStatus } from '@/lib/utils/pexels'
import type {
  CategoryCounts,
  ConjugationGridEntry,
  FlatVerb,
  OracionFillable,
  TiempoConjugacion,
  Verb,
} from '@/lib/types/verbs'
import type { VerbosApi } from '@/components/providers/VerbContext'

const VERBS_JSON_URL = '/verbos_estructura.json'

export const VERBS_BASE = '/v1/verbs'

function verbHref(slug: string): string {
  return `${VERBS_BASE}/${encodeURIComponent(slug)}`
}

const TIME_KEYS: readonly TiempoConjugacion[] = [
  'infinitivo',
  'pasadoSimple',
  'participio',
  'gerundio',
  'futuro',
  'condicional',
] as const

function getAllFilledOraciones(verb: Verb | null): OracionFillable[] {
  if (!verb) return []
  const oraciones = verb.oraciones ?? {}
  return TIME_KEYS.map((key) => {
    const data = oraciones[key] ?? { ing: '', esp: '' }
    return { timeKey: key, data: { ing: data.ing ?? '', esp: data.esp ?? '' } }
  }).filter((entry) => Boolean(entry.data.ing.trim()))
}

function slugify(verb: Verb | null | undefined): string {
  return verb?.infinitivo?.ing?.trim?.() ?? ''
}

export function useVerbos(): VerbosApi {
  const [allVerbs, setAllVerbs] = useState<FlatVerb[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')
  const [subcategory, setSubcategory] = useState('all')

  const router = useRouter()
  const pathname = usePathname()
  const params = useParams<{ verbSelector?: string }>()

  const verbSelectorFromUrl = useMemo<string | null>(() => {
    const m = pathname.match(/^\/v1\/verbs\/([^/]+)\/?$/)
    if (!m || !m[1]) return null
    let raw: string
    try {
      raw = decodeURIComponent(m[1])
    } catch {
      raw = m[1]
    }
    return raw
  }, [pathname])
  const effectiveSelector = params?.verbSelector ?? verbSelectorFromUrl

  useEffect(() => {
    let cancelled = false
    checkPexelsStatus()
    ;(async () => {
      try {
        const res = await fetch(VERBS_JSON_URL, { cache: 'no-store' })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const json: unknown = await res.json()
        if (cancelled) return
        const flat = flattenVerbos(json)
        setAllVerbs(flat)
        setLoading(false)
      } catch (err) {
        if (cancelled) return
        setError(err instanceof Error ? err : new Error(String(err)))
        setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    if (allVerbs.length === 0) return
    if (effectiveSelector == null) return
    if (resolveVerb(effectiveSelector, allVerbs) == null) {
      router.replace('/')
    }
  }, [effectiveSelector, allVerbs, router])

  const categories = useMemo(() => collectCategories(allVerbs), [allVerbs])

  const counts = useMemo<CategoryCounts>(() => {
    const byCategory = new Map<string, { total: number; sub: Map<string, number> }>()
    const bySubcategory = new Map<string, number>()
    for (const item of allVerbs) {
      if (item.category) {
        const cat = byCategory.get(item.category) ?? { total: 0, sub: new Map() }
        cat.total += 1
        byCategory.set(item.category, cat)
      }
      if (item.category && item.subcategory) {
        const key = `${item.category}::${item.subcategory}`
        bySubcategory.set(key, (bySubcategory.get(key) ?? 0) + 1)
      }
    }
    return {
      total: allVerbs.length,
      byCategory,
      bySubcategory,
      subTotal: (cat: string): number => {
        let n = 0
        for (const item of allVerbs) if (item.category === cat) n += 1
        return n
      },
      subForCategory: (cat: string): number => {
        let n = 0
        for (const item of allVerbs) if (item.category === cat) n += 1
        return n
      },
    }
  }, [allVerbs])

  const filtered = useMemo<FlatVerb[]>(() => {
    const q = search.trim().toLowerCase()
    return allVerbs.filter(({ verb, category: cat, subcategory: sub }) => {
      if (category !== 'all' && cat !== category) return false
      if (subcategory !== 'all' && sub !== subcategory) return false
      if (q) {
        const ing = verb.infinitivo?.ing?.toLowerCase() ?? ''
        const esp = verb.infinitivo?.esp?.toLowerCase() ?? ''
        if (!ing.includes(q) && !esp.includes(q)) return false
      }
      return true
    })
  }, [allVerbs, search, category, subcategory])

  const current = useMemo<FlatVerb | null>(
    () => resolveVerb(effectiveSelector ?? null, allVerbs),
    [effectiveSelector, allVerbs],
  )
  const currentVerb: Verb | null = current?.verb ?? null

  const srs = useSRSContext()
  useEffect(() => {
    if (currentVerb && srs) {
      srs.registerVerb(currentVerb)
    }
  }, [currentVerb, srs])

  const currentIndex = useMemo<number>(() => {
    if (!current || !currentVerb) return -1
    return filtered.findIndex(
      (i) => i.verb.infinitivo?.ing === currentVerb.infinitivo?.ing,
    )
  }, [current, currentVerb, filtered])

  useEffect(() => {
    if (effectiveSelector == null) return
    if (loading || error) return
    if (allVerbs.length === 0) return
    if (current === null) return
    if (currentIndex !== -1) return
    if (filtered.length === 0) return
    const idx = Math.floor(Math.random() * filtered.length)
    const slug = slugify(filtered[idx]?.verb)
    if (slug) router.replace(verbHref(slug))
  }, [effectiveSelector, loading, error, allVerbs.length, current, currentIndex, filtered, router])

  const syncedThisSession = useRef(new Set<number>())

  useEffect(() => {
    syncedThisSession.current = new Set()
  }, [currentVerb?.id])

  const dueCount = srs?.dueCount ?? 0
  void dueCount

  const reportEnrichment = useCallback(
    (verb: unknown, enrichment: { imagen_url: string; image_source: string; audio_url: string | null; audio_source: string }): void => {
      const v = verb as Verb | null
      if (!v || v.id == null) return
      if (syncedThisSession.current.has(v.id)) return
      syncedThisSession.current.add(v.id)
      void syncVerbToMongo({ ...v, ...enrichment })
    },
    [],
  )

  const goTo = useCallback(
    (idx: number): void => {
      if (filtered.length === 0) return
      const nextIdx = ((idx % filtered.length) + filtered.length) % filtered.length
      const slug = slugify(filtered[nextIdx]?.verb)
      if (slug) router.push(verbHref(slug))
    },
    [filtered, router],
  )

  const next = useCallback((): void => {
    if (currentIndex < 0) goTo(0)
    else goTo(currentIndex + 1)
  }, [goTo, currentIndex])

  const prev = useCallback((): void => {
    if (currentIndex < 0) goTo(filtered.length - 1)
    else goTo(currentIndex - 1)
  }, [goTo, currentIndex, filtered.length])

  const shuffle = useCallback((): void => {
    if (filtered.length === 0) return
    const idx = pickWeightedIndex(filtered, WEIGHT_MAP)
    const slug = slugify(filtered[idx]?.verb)
    if (slug) router.push(verbHref(slug))
  }, [filtered, router])

  const goToRandomVerb = useCallback((): void => {
    if (allVerbs.length === 0) return
    const idx = pickWeightedIndex(allVerbs, WEIGHT_MAP)
    const slug = slugify(allVerbs[idx]?.verb)
    if (slug) router.push(verbHref(slug))
  }, [allVerbs, router])

  useEffect(() => {
    function onKey(e: KeyboardEvent): void {
      const target = e.target
      if (
        target instanceof HTMLInputElement ||
        target instanceof HTMLTextAreaElement
      ) {
        return
      }
      if (e.key === 'ArrowRight') {
        e.preventDefault()
        next()
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault()
        prev()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [next, prev])

  const oraciones = useMemo<OracionFillable[]>(
    () => getAllFilledOraciones(currentVerb),
    [currentVerb],
  )

  const conjugationEntries = useMemo<ConjugationGridEntry[]>(() => {
    if (!currentVerb) return []
    const v = currentVerb as unknown as {
      pasadoSimple?: { ing?: string; esp?: string }
      participio?: { ing?: string; esp?: string }
      gerundio?: { ing?: string; esp?: string }
      futuro?: { ing?: string; esp?: string }
      condicional?: { ing?: string; esp?: string }
    }
    return [
      { time: 'Pasado', value: v.pasadoSimple?.ing, valueEsp: v.pasadoSimple?.esp },
      { time: 'Participio', value: v.participio?.ing, valueEsp: v.participio?.esp },
      { time: 'Gerundio', value: v.gerundio?.ing, valueEsp: v.gerundio?.esp },
      { time: 'Futuro', value: v.futuro?.ing, valueEsp: v.futuro?.esp },
      { time: 'Condicional', value: v.condicional?.ing, valueEsp: v.condicional?.esp },
    ]
  }, [currentVerb])

  void currentVerb

  return {
    loading,
    error,
    search,
    setSearch,
    category,
    setCategory,
    subcategory,
    setSubcategory,
    categories,
    counts,
    filtered,
    currentIndex,
    current,
    currentVerb,
    oraciones,
    conjugationEntries,
    dueCount,
    next,
    prev,
    shuffle,
    goTo,
    goToRandomVerb,
    total: filtered.length,
    verbSelector: effectiveSelector,
    reportEnrichment,
  }
}
