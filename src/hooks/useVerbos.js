import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useLocation, useNavigate, useParams } from 'react-router-dom'
import { collectCategories, flattenVerbos } from '../utils/flatten'
import { pickWeightedIndex } from '../utils/weightedRandom'
import { WEIGHT_MAP } from '../data/weightedVerbs'
import { syncVerbToMongo } from '../utils/mongoSync'
import { useSRSContext } from '../contexts/SRSContext'

const JSON_URL = `${import.meta.env.BASE_URL}verbos_estructura.json`

export const VERBS_BASE = '/v1/verbs'

function verbHref(slug) {
  return `${VERBS_BASE}/${encodeURIComponent(slug)}`
}

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
  const location = useLocation()

  // The hook is invoked in <App>, ABOVE <Routes>, so useParams() returns {}
  // there even when the URL has a verb selector. Fall back to parsing the
  // pathname directly, scoped to the /v1/verbs/:verbSelector namespace so
  // that /, /v1/test, and any other route return null instead of being
  // mistaken for verb selectors.
  const verbSelectorFromUrl = useMemo(() => {
    const m = location.pathname.match(/^\/v1\/verbs\/([^/]+)\/?$/)
    if (!m || !m[1]) return null
    let raw
    try {
      raw = decodeURIComponent(m[1])
    } catch {
      raw = m[1]
    }
    return raw
  }, [location.pathname])
  const effectiveSelector = verbSelector ?? verbSelectorFromUrl

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

  // If we're on a verb URL but the selector doesn't resolve (deleted verb,
  // typo, etc.), bounce the user back to the home page so the menu is
  // always reachable. No random-pick on `/` — HomePage owns that flow now
  // via goToRandomVerb().
  useEffect(() => {
    if (allVerbs.length === 0) return
    if (effectiveSelector == null) return
    if (resolveVerb(effectiveSelector, allVerbs) == null) {
      navigate('/', { replace: true })
    }
  }, [effectiveSelector, allVerbs, navigate])

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
    () => resolveVerb(effectiveSelector, allVerbs),
    [effectiveSelector, allVerbs],
  )
  const currentVerb = current?.verb ?? null

  // ── SRS auto-register ──
  // Every verb the user lands on gets added to the SRS "Verbos vistos"
  // deck. `registerVerb` is idempotent per `verbKey`, so re-visits are
  // safe (no duplicate cards). `currentVerb` is memoized upstream, so
  // its reference is stable while the verb stays the same.
  const srs = useSRSContext()
  useEffect(() => {
    if (currentVerb && srs) srs.registerVerb(currentVerb)
  }, [currentVerb, srs])

  const currentIndex = useMemo(() => {
    if (!current || !currentVerb) return -1
    return filtered.findIndex(
      (i) => i.verb.infinitivo?.ing === currentVerb.infinitivo?.ing,
    )
  }, [current, currentVerb, filtered])

  // Auto-redirect when the URL selector points to a verb that exists in
  // allVerbs but is no longer reachable due to the current filter. We
  // still want prev/next to navigate within `filtered`, so this only
  // triggers when the displayed verb is genuinely absent from the
  // visible set.
  useEffect(() => {
    if (effectiveSelector == null) return
    if (loading || error) return
    if (allVerbs.length === 0) return
    if (current === null) return
    if (currentIndex !== -1) return
    if (filtered.length === 0) return
    const idx = Math.floor(Math.random() * filtered.length)
    const slug = slugify(filtered[idx]?.verb)
    if (slug) navigate(verbHref(slug), { replace: true })
  }, [
    effectiveSelector,
    loading,
    error,
    allVerbs.length,
    current,
    currentIndex,
    filtered,
    navigate,
  ])

  // ── MongoDB sync ──
  // VerbCard reports enrichment (image + audio) via reportEnrichment().
  // When both arrive for the current verb, fire a fire-and-forget POST
  // to /api/verbs/sync. A Set<id> guards against StrictMode duplicates.
  const syncedThisSession = useRef(new Set())

  useEffect(() => {
    syncedThisSession.current = new Set()
  }, [currentVerb?.id])

  const reportEnrichment = useCallback(
    (verb, enrichment) => {
      if (verb?.id == null) return
      if (syncedThisSession.current.has(verb.id)) return
      syncedThisSession.current.add(verb.id)
      syncVerbToMongo({ ...verb, ...enrichment })
    },
    [],
  )

  const goTo = useCallback(
    (idx) => {
      if (filtered.length === 0) return
      const nextIdx =
        ((idx % filtered.length) + filtered.length) % filtered.length
      const slug = slugify(filtered[nextIdx]?.verb)
      if (slug) navigate(verbHref(slug))
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
    if (slug) navigate(verbHref(slug))
  }, [filtered, navigate])

  // Exposed for HomePage's "Explorar Verbos" CTA. Picks a weighted-random
  // verb from the FULL corpus (not the current filter, since there is no
  // filter on the home page) and navigates into the verb view.
  const goToRandomVerb = useCallback(() => {
    if (allVerbs.length === 0) return
    const idx = pickWeightedIndex(allVerbs, WEIGHT_MAP)
    const slug = slugify(allVerbs[idx]?.verb)
    if (slug) navigate(verbHref(slug))
  }, [allVerbs, navigate])

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
    goToRandomVerb,
    total: filtered.length,
    verbSelector: effectiveSelector,
    reportEnrichment,
  }
}
