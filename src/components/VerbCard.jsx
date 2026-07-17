import { useCallback, useEffect, useRef, useState } from 'react'
import ConjugationGrid from './ConjugationGrid'
import SentencesList from './SentencePill'
import NavButtons from './NavButtons'
import HeroIllustration from './HeroIllustration'
import AudioButton from './AudioButton'
import ImageCredit from './ImageCredit'
import { addCachedImage, getCachedImages } from '../utils/imageCache'
import { fetchPexelsPhoto, hasPexelsKey } from '../utils/pexels'

const SWIPE_THRESHOLD = 70
const SWIPE_AXIS_RATIO = 1.5
const SWIPE_MAX_ABS = 240
const DRAG_DAMPING = 0.32
const DRAG_FADE_MAX = 0.25

function picsumUrl(verb) {
  const word = verb?.infinitivo?.ing ?? 'english'
  return `https://picsum.photos/seed/${encodeURIComponent(word)}/800/400`
}

function VerbImage({ verb }) {
  const word = verb.infinitivo?.ing ?? null
  const hasCustom = Boolean(verb.imagen?.trim())
  const pexelsAvailable = hasPexelsKey()

  const cachedAtMount = !hasCustom && word ? getCachedImages(word) : null
  const initialPhoto = cachedAtMount?.[0] ?? null

  const [src, setSrc] = useState(() => {
    if (hasCustom) return verb.imagen
    if (!pexelsAvailable) return picsumUrl(verb)
    return initialPhoto?.url ?? null
  })
  const [credit, setCredit] = useState(() => initialPhoto)
  const [stage, setStage] = useState(() => {
    if (hasCustom) return 'custom'
    if (!pexelsAvailable) return 'picsum'
    return initialPhoto ? 'pexels' : 'svg'
  })
  const [picsumFailed, setPicsumFailed] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [heroExpanded, setHeroExpanded] = useState(() => {
    if (typeof window === 'undefined') return false
    try {
      return window.localStorage.getItem('verbos:heroExpanded') === 'true'
    } catch {
      return false
    }
  })
  const audioWord = word

  const toggleHeroExpanded = useCallback(() => {
    setHeroExpanded((prev) => {
      const next = !prev
      try {
        window.localStorage.setItem('verbos:heroExpanded', String(next))
      } catch {
        // ignore storage failures (private mode, quota, etc.)
      }
      return next
    })
  }, [])

  useEffect(() => {
    if (hasCustom || !word) return
    if (getCachedImages(word)) return
    if (!pexelsAvailable) return

    let cancelled = false

    fetchPexelsPhoto(word).then((result) => {
      if (cancelled) return
      if (result) {
        addCachedImage(word, result)
        setSrc(result.url)
        setCredit(result)
        setStage('pexels')
      } else {
        setSrc(picsumUrl(verb))
        setStage('picsum')
      }
    })

    return () => {
      cancelled = true
    }
  }, [word, hasCustom, pexelsAvailable, verb])

  const refreshImage = useCallback(async () => {
    if (!word || hasCustom || !pexelsAvailable || refreshing) return
    const existing = getCachedImages(word) ?? []
    const nextPage = existing.length + 1
    setRefreshing(true)
    try {
      const result = await fetchPexelsPhoto(word, nextPage)
      if (result) {
        addCachedImage(word, result)
        setSrc(result.url)
        setCredit(result)
        setStage('pexels')
      }
    } finally {
      setRefreshing(false)
    }
  }, [word, hasCustom, pexelsAvailable, refreshing])

  const onImgError = () => {
    if (stage === 'pexels') {
      setSrc(picsumUrl(verb))
      setCredit(null)
      setStage('picsum')
    } else if (stage === 'picsum' && !picsumFailed) {
      setPicsumFailed(true)
    }
  }

  const canRefresh = !hasCustom && pexelsAvailable && Boolean(word)

  const heightClass = heroExpanded
    ? 'h-[calc(100dvh-1rem)]'
    : 'h-44 sm:h-52 md:h-56'

  if (hasCustom) {
    return (
      <div className={`group relative w-full overflow-hidden bg-slate-100 ${heightClass}`}>
        <HeroIllustration className="absolute inset-0 h-full w-full" />
        <img
          src={src}
          alt={verb.infinitivo?.ing ?? ''}
          loading="lazy"
          decoding="async"
          onError={onImgError}
          className="absolute inset-0 h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-slate-900/10" />
        <ImageCredit credit={credit} />
        <VerbImageOverlay
          audioWord={audioWord}
          heroExpanded={heroExpanded}
          onToggleExpand={toggleHeroExpanded}
        />
      </div>
    )
  }

  const showImg = Boolean(src) && !picsumFailed

  return (
    <div className={`group relative w-full overflow-hidden bg-slate-100 ${heightClass}`}>
      <HeroIllustration className="absolute inset-0 h-full w-full" />
      {showImg ? (
        <img
          src={src}
          alt={verb.infinitivo?.ing ?? ''}
          loading="lazy"
          decoding="async"
          onError={onImgError}
          className="absolute inset-0 h-full w-full object-cover"
        />
      ) : null}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-slate-900/10" />
      <ImageCredit credit={credit} />
      <VerbImageOverlay
        audioWord={audioWord}
        onRefresh={refreshImage}
        canRefresh={canRefresh}
        refreshing={refreshing}
        heroExpanded={heroExpanded}
        onToggleExpand={toggleHeroExpanded}
      />
    </div>
  )
}

function VerbImageOverlay({
  audioWord,
  onRefresh,
  canRefresh,
  refreshing,
  heroExpanded,
  onToggleExpand,
}) {
  const buttonRef = useRef(null)

  const handleOverlayClick = (e) => {
    if (e.target.closest('button[data-overlay-control]')) return
    const btn = buttonRef.current
    if (btn && (e.target === btn || btn.contains(e.target))) return
    btn?.click()
  }

  return (
    <>
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-slate-900/30 opacity-100 transition-opacity duration-300 md:opacity-0 md:group-hover:opacity-100 md:bg-slate-900/50 md:backdrop-blur-[2px]"
      />
      <button
        type="button"
        data-overlay-control="expand"
        onClick={(e) => {
          e.stopPropagation()
          onToggleExpand?.()
        }}
        aria-label={heroExpanded ? 'Restaurar tamaño de imagen' : 'Maximizar imagen'}
        title={heroExpanded ? 'Restaurar tamaño' : 'Maximizar'}
        className="absolute top-2 left-2 z-30 inline-flex size-9 items-center justify-center rounded-full bg-slate-900/50 text-white shadow-md backdrop-blur-sm transition hover:scale-105 hover:bg-slate-900/70 active:scale-95 motion-reduce:animate-none"
      >
        {heroExpanded ? (
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="size-4"
            aria-hidden="true"
          >
            <path d="M8 3v3a2 2 0 0 1-2 2H3" />
            <path d="M21 8h-3a2 2 0 0 1-2-2V3" />
            <path d="M3 16h3a2 2 0 0 1 2 2v3" />
            <path d="M16 21v-3a2 2 0 0 1 2-2h3" />
          </svg>
        ) : (
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="size-4"
            aria-hidden="true"
          >
            <path d="M8 3H5a2 2 0 0 0-2 2v3" />
            <path d="M21 8V5a2 2 0 0 0-2-2h-3" />
            <path d="M3 16v3a2 2 0 0 0 2 2h3" />
            <path d="M16 21h3a2 2 0 0 0 2-2v-3" />
          </svg>
        )}
      </button>
      <div
        className="absolute inset-0 z-10 flex cursor-pointer items-center justify-center"
        onClick={handleOverlayClick}
      >
        <div className="transition-transform duration-300 group-hover:scale-110">
          <AudioButton ref={buttonRef} key={audioWord} word={audioWord} />
        </div>
      </div>
      {canRefresh ? (
        <button
          type="button"
          data-overlay-control="refresh"
          onClick={(e) => {
            e.stopPropagation()
            onRefresh?.()
          }}
          disabled={refreshing}
          aria-label="Buscar otra foto"
          title="Buscar otra foto"
          className="absolute top-2 right-2 z-30 inline-flex size-9 items-center justify-center rounded-full bg-slate-900/50 text-white shadow-md backdrop-blur-sm transition hover:scale-105 hover:bg-slate-900/70 active:scale-95 disabled:opacity-50 disabled:hover:scale-100 motion-reduce:animate-none"
        >
          {refreshing ? (
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="size-4 animate-spin motion-reduce:animate-none"
              aria-hidden="true"
            >
              <path d="M21 12a9 9 0 1 1-6.219-8.56" />
            </svg>
          ) : (
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="size-4"
              aria-hidden="true"
            >
              <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" />
              <circle cx="12" cy="13" r="3.5" />
              <path d="M21 8l-2-2" />
              <path d="m17 6 4 4" />
            </svg>
          )}
        </button>
      ) : null}
    </>
  )
}

function SectionHeader({ title }) {
  return (
    <h2 className="mb-4 text-sm font-bold uppercase tracking-[0.18em] text-slate-900 sm:text-base">
      {title}
    </h2>
  )
}

function EmptyState() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center shadow-sm">
      <div className="mx-auto mb-3 inline-flex size-12 items-center justify-center rounded-full bg-slate-100 text-slate-400">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="size-6"
          aria-hidden="true"
        >
          <circle cx="11" cy="11" r="7" />
          <path d="m20 20-3.5-3.5" />
        </svg>
      </div>
      <p className="text-lg font-semibold text-slate-800">No se encontraron verbos</p>
      <p className="mt-1 text-sm text-slate-500">
        Ajusta la búsqueda o cambia los filtros para ver más resultados.
      </p>
    </div>
  )
}

function applyDragStyle(el, x) {
  if (!el) return
  el.style.transform = `translate3d(${x * DRAG_DAMPING}px, 0, 0)`
  el.style.opacity = String(
    Math.max(1 - DRAG_FADE_MAX, 1 - Math.min(DRAG_FADE_MAX, Math.abs(x) * 0.0035)),
  )
}

function clearDragStyle(el) {
  if (!el) return
  el.style.transition = 'transform 220ms cubic-bezier(0.22, 1, 0.36, 1), opacity 220ms ease-out'
  el.style.transform = 'translate3d(0, 0, 0)'
  el.style.opacity = '1'
}

export default function VerbCard({
  current,
  currentVerb,
  oraciones,
  conjugationEntries,
  currentIndex,
  total,
  onPrev,
  onNext,
  onShuffle,
}) {
  const articleRef = useRef(null)
  const startRef = useRef(null)
  const lastRef = useRef({ x: 0, y: 0 })

  const verbKey = currentVerb?.id ?? currentVerb?.infinitivo?.ing ?? null
  const [trackedVerbKey, setTrackedVerbKey] = useState(verbKey)
  if (trackedVerbKey !== verbKey) {
    setTrackedVerbKey(verbKey)
  }
  const shouldAnimateVerbEnter =
    trackedVerbKey !== null && trackedVerbKey !== verbKey

  function handleTouchStart(e) {
    if (!e.touches || e.touches.length !== 1) return
    const t = e.touches[0]
    startRef.current = { x: t.clientX, y: t.clientY }
    lastRef.current = { x: 0, y: 0 }
    const el = articleRef.current
    if (el) {
      el.style.transition = 'none'
      applyDragStyle(el, 0)
    }
  }

  function handleTouchMove(e) {
    const start = startRef.current
    if (!start) return
    const t = e.touches[0]
    const dx = t.clientX - start.x
    const dy = t.clientY - start.y
    lastRef.current = { x: dx, y: dy }
    applyDragStyle(articleRef.current, dx)
  }

  function handleTouchEnd() {
    const start = startRef.current
    if (!start) return
    startRef.current = null
    const { x, y } = lastRef.current
    lastRef.current = { x: 0, y: 0 }
    clearDragStyle(articleRef.current)

    const ax = Math.abs(x)
    const ay = Math.abs(y)
    const isHorizontal = ay * SWIPE_AXIS_RATIO < ax
    if (isHorizontal && ax >= SWIPE_THRESHOLD && ax <= SWIPE_MAX_ABS) {
      if (x < 0) onNext?.()
      else onPrev?.()
    }
  }

  if (!currentVerb) return <EmptyState />

  const inf = currentVerb.infinitivo
  const tipSeed = currentVerb.id ?? currentIndex ?? 0

  return (
    <article
      ref={articleRef}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      onTouchCancel={handleTouchEnd}
      style={{ touchAction: 'pan-y', willChange: 'transform, opacity' }}
      className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition-shadow hover:shadow-md"
    >
      <VerbImage verb={currentVerb} />

      <div className="flex items-center justify-center border-b border-slate-100 bg-slate-50/60 px-4 py-3 sm:px-6">
        <NavButtons
          onPrev={onPrev}
          onNext={onNext}
          onShuffle={onShuffle}
          currentIndex={currentIndex}
          total={total}
        />
      </div>

      <div
        key={verbKey}
        style={shouldAnimateVerbEnter ? { willChange: 'transform, opacity' } : undefined}
        className={
          'space-y-8 p-5 sm:p-7 md:p-8 ' +
          (shouldAnimateVerbEnter ? 'animate-verb-enter motion-reduce:animate-none' : '')
        }
      >
        <header className="text-center">
          <h1 className="text-5xl font-bold tracking-tight text-indigo-600 sm:text-6xl">
            {inf?.ing}
          </h1>
          <p className="mt-2 text-xl font-medium text-slate-500 sm:text-2xl">
            {inf?.esp}
          </p>
        </header>

        <section>
          <SectionHeader title="Conjugaciones" />
          <ConjugationGrid entries={conjugationEntries} seed={tipSeed} />
        </section>

        <section>
          <SectionHeader title="Oraciones en contexto" />
          <SentencesList oraciones={oraciones} />
        </section>

        {current?.category && (
          <p className="pt-1 text-center text-[0.7rem] uppercase tracking-[0.18em] text-slate-300">
            {current.category}
            {current.subcategory ? ` · ${current.subcategory}` : ''}
          </p>
        )}
      </div>
    </article>
  )
}
