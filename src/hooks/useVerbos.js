import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
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

export function useVerbos() {
  const [allVerbs, setAllVerbs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')
  const [subcategory, setSubcategory] = useState('all')
  const [currentIndex, setCurrentIndex] = useState(0)

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
        if (!initialPickDone.current) {
          initialPickDone.current = true
          setCurrentIndex(pickWeightedIndex(flat, WEIGHT_MAP))
        }
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

  const categories = useMemo(() => collectCategories(allVerbs), [allVerbs])

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

  const lastFilteredLen = useRef(filtered.length)
  useEffect(() => {
    // The only transition that comes from an empty filtered list is the
    // initial data load. Skip resetting the index in that case so the
    // weighted-random pick survives. Filter/search changes always move
    // between two non-empty lengths.
    const cameFromEmpty = lastFilteredLen.current === 0
    if (!cameFromEmpty && filtered.length !== lastFilteredLen.current) {
      setCurrentIndex(0)
    }
    lastFilteredLen.current = filtered.length
  }, [filtered.length])

  const current = filtered[currentIndex] ?? null
  const currentVerb = current?.verb ?? null

  const goTo = useCallback(
    (idx) => {
      if (filtered.length === 0) return
      const next = ((idx % filtered.length) + filtered.length) % filtered.length
      setCurrentIndex(next)
    },
    [filtered.length],
  )

  const next = useCallback(() => goTo(currentIndex + 1), [goTo, currentIndex])
  const prev = useCallback(() => goTo(currentIndex - 1), [goTo, currentIndex])

  const shuffle = useCallback(() => {
    if (filtered.length === 0) return
    const idx = pickWeightedIndex(filtered, WEIGHT_MAP)
    setCurrentIndex(idx)
  }, [filtered])

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

  const oraciones = useMemo(() => (currentVerb ? getAllFilledOraciones(currentVerb) : []), [currentVerb])

  const conjugationEntries = useMemo(() => {
    if (!currentVerb) return []
    return [
      { time: 'Pasado', value: currentVerb.pasadoSimple?.ing },
      { time: 'Participio', value: currentVerb.participio?.ing },
      { time: 'Gerundio', value: currentVerb.gerundio?.ing },
      { time: 'Futuro', value: currentVerb.futuro?.ing },
      { time: 'Condicional', value: currentVerb.condicional?.ing },
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
  }
}
