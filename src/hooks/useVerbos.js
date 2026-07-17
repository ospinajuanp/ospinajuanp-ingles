import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { collectCategories, flattenVerbos } from '../utils/flatten'
import { pickWeightedIndex } from '../utils/weightedRandom'
import { WEIGHT_MAP } from '../data/weightedVerbs'

const JSON_URL = `${import.meta.env.BASE_URL}verbos_estructura.json`

const TIME_KEYS = [
  'infinitivo',
  'pasadoSimple',
  'participio',
  'gerundio',
  'futuro',
  'condicional',
]

function getAllFilledOraciones(verb) {
  const oraciones = verb?.oraciones ?? {}
  return TIME_KEYS.map((key) => ({
    timeKey: key,
    data: oraciones[key],
  })).filter((entry) => entry.data?.ing?.trim?.())
}

function slugify(verb) {
  return verb?.infinitivo?.ing?.trim?.() ?? ''
}

export function resolveVerb(selector, list) {
  if (!selector || !list?.length) return null
  if (/^\d+$/.test(selector)) {
    const id = Number(selector)
    return list.find((i) => i.verb?.id === id) ?? null
  }
  const norm = selector.trim().toLowerCase()
  return (
    list.find((i) => i.verb?.infinitivo?.ing?.trim?.().toLowerCase() === norm) ??
    null
  )
}

export function useVerbos() {
  const [allVerbs, setAllVerbs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')
  const [subcategory, setSubcategory] = useState('all')

  const { verbSelector = null } = useParams()
  const navigate = useNavigate()
  const initialPickDone = useRef(false)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const res = await fetch(JSON_URL)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const json = await res.json()
        if (cancelled) return
        const flat = flattenVerbos(json)
        setAllVerbs(flat)
        setLoading(false)
      } catch (err) {
        if (cancelled) return
        setError(err)
        setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  // Root route ("/"): pick a weighted random verb once data is ready and
  // silently replace the URL. Guarded against StrictMode double-invoke via
  // initialPickDone ref (preserves the cameFromEmpty contract from the
  // pre-routing version).
  //
  // Also: if the URL has a selector that resolves to no verb in allVerbs
  // (e.g. /nope-123), redirect to "/" so the root handler picks a new one.
  // Both branches are guarded so they fire at most once per actual selector
  // change — no thrashing.
  useEffect(() => {
    if (allVerbs.length === 0) return

    if (verbSelector == null) {
      if (initialPickDone.current) return
      initialPickDone.current = true
      const idx = pickWeightedIndex(allVerbs, WEIGHT_MAP)
      const slug = slugify(allVerbs[idx]?.verb)
      if (slug) navigate(`/${encodeURIComponent(slug)}`, { replace: true })
      return
    }

    if (resolveVerb(verbSelector, allVerbs) == null) {
      navigate('/', { replace: true })
    }
  }, [verbSelector, allVerbs, navigate])

  const categories = useMemo(() => collectCategories(allVerbs), [allVerbs])

  const counts = useMemo(() => {
    const byCategory = new Map()
    const bySubcategory = new Map()
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
      subTotal: (category) => {
        let n = 0
        for (const item of allVerbs) if (item.category === category) n += 1
        return n
      },
      subForCategory: (cat) => {
        let n = 0
        for (const item of allVerbs) if (item.category === cat) n += 1
        return n
      },
    }
  }, [allVerbs])

  const filtered = useMemo(() => {
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

  const current = useMemo(
    () => resolveVerb(verbSelector, allVerbs),
    [verbSelector, allVerbs],
  )
  const currentVerb = current?.verb ?? null

  const currentIndex = useMemo(() => {
    if (!current || !currentVerb) return -1
    return filtered.findIndex(
      (i) => i.verb.infinitivo?.ing === currentVerb.infinitivo?.ing,
    )
  }, [current, currentVerb, filtered])

  // Auto-redirect when the URL selector points to a verb that exists in
  // allVerbs but is no longer reachable due to current filter. We still
  // want prev/next to navigate within `filtered`, so this only triggers
  // when the displayed verb is genuinely absent from the visible set.
  useEffect(() => {
    if (verbSelector == null) return
    if (loading || error) return
    if (allVerbs.length === 0) return
    if (current === null) return
    if (currentIndex !== -1) return
    // Selector matched a verb in allVerbs but not in filtered (filter
    // excluded it). Reset to / so the root-route effect picks a new one
    // inside the filter — or simply force-pick a random verb from the
    // filter to be predictable.
    if (filtered.length === 0) return
    const idx = Math.floor(Math.random() * filtered.length)
    const slug = slugify(filtered[idx]?.verb)
    if (slug) navigate(`/${encodeURIComponent(slug)}`, { replace: true })
  }, [
    verbSelector,
    loading,
    error,
    allVerbs.length,
    current,
    currentIndex,
    filtered,
    navigate,
  ])

  const goTo = useCallback(
    (idx) => {
      if (filtered.length === 0) return
      const nextIdx =
        ((idx % filtered.length) + filtered.length) % filtered.length
      const slug = slugify(filtered[nextIdx]?.verb)
      if (slug) navigate(`/${encodeURIComponent(slug)}`)
    },
    [filtered, navigate],
  )

  const next = useCallback(() => {
    if (currentIndex < 0) goTo(0)
    else goTo(currentIndex + 1)
  }, [goTo, currentIndex])

  const prev = useCallback(() => {
    if (currentIndex < 0) goTo(filtered.length - 1)
    else goTo(currentIndex - 1)
  }, [goTo, currentIndex, filtered.length])

  const shuffle = useCallback(() => {
    if (filtered.length === 0) return
    const idx = pickWeightedIndex(filtered, WEIGHT_MAP)
    const slug = slugify(filtered[idx]?.verb)
    if (slug) navigate(`/${encodeURIComponent(slug)}`)
  }, [filtered, navigate])

  useEffect(() => {
    function onKey(e) {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
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

  const oraciones = useMemo(
    () => (currentVerb ? getAllFilledOraciones(currentVerb) : []),
    [currentVerb],
  )

  const conjugationEntries = useMemo(() => {
    if (!currentVerb) return []
    return [
      { time: 'Pasado', value: currentVerb.pasadoSimple?.ing, valueEsp: currentVerb.pasadoSimple?.esp },
      { time: 'Participio', value: currentVerb.participio?.ing, valueEsp: currentVerb.participio?.esp },
      { time: 'Gerundio', value: currentVerb.gerundio?.ing, valueEsp: currentVerb.gerundio?.esp },
      { time: 'Futuro', value: currentVerb.futuro?.ing, valueEsp: currentVerb.futuro?.esp },
      { time: 'Condicional', value: currentVerb.condicional?.ing, valueEsp: currentVerb.condicional?.esp },
    ]
  }, [currentVerb])

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
    next,
    prev,
    shuffle,
    goTo,
    total: filtered.length,
    verbSelector,
  }
}