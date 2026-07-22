'use client'
import { useCallback, useEffect, useRef, useState } from 'react'
import { Maximize2, Minimize2, Loader2, Camera, SearchX } from 'lucide-react'
import ConjugationGrid from './ConjugationGrid'
import SentencesList from './SentencePill'
import NavButtons from './NavButtons'
import HeroIllustration from './HeroIllustration'
import AudioButton from './AudioButton'
import ImageCredit from './ImageCredit'
import { addCachedImage, getCachedImages } from '@/lib/utils/imageCache'
import { fetchPexelsPhoto, hasPexelsKey } from '@/lib/utils/pexels'
import type { ConjugationGridEntry } from '@/lib/types/verbs'
import type { FlatVerb } from '@/lib/types/verbs'
import type { OracionFillable } from '@/lib/types/verbs'
import type { Verb } from '@/lib/types/verbs'
import type { AudioResolution, ImageResolution } from '@/lib/types/media'
import type { ImageCreditInfo } from './ImageCredit'

const SWIPE_THRESHOLD = 70
const SWIPE_AXIS_RATIO = 1.5
const SWIPE_MAX_ABS = 240
const DRAG_DAMPING = 0.32
const DRAG_FADE_MAX = 0.25

function picsumUrl(verb: Verb): string {
  const word = verb?.infinitivo?.ing ?? 'english'
  return `https://picsum.photos/seed/${encodeURIComponent(word)}/800/400`
}

function VerbImage({
  verb,
  onReady,
  onAudioResolved,
}: {
  verb: Verb
  onReady?: (info: ImageResolution) => void
  onAudioResolved?: (info: AudioResolution | null) => void
}) {
  const word = verb.infinitivo?.ing ?? null
  const hasCustom = Boolean(verb.imagen?.trim())
  const pexelsAvailable = hasPexelsKey()

  const cachedAtMount = !hasCustom && word ? getCachedImages(word) : null
  const initialPhoto = cachedAtMount?.[0] ?? null

  const [src, setSrc] = useState<string | null>(() => {
    if (hasCustom && verb.imagen) return verb.imagen
    if (!pexelsAvailable) return picsumUrl(verb)
    return initialPhoto?.url ?? null
  })
  const [credit, setCredit] = useState<ImageCreditInfo | null>(
    () => initialPhoto ?? null,
  )
  const [stage, setStage] = useState<'custom' | 'pexels' | 'picsum' | 'svg'>(() => {
    if (hasCustom) return 'custom'
    if (!pexelsAvailable) return 'picsum'
    return initialPhoto ? 'pexels' : 'svg'
  })
  const [picsumFailed, setPicsumFailed] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [heroExpanded, setHeroExpanded] = useState<boolean>(() => {
    if (typeof window === 'undefined') return false
    try {
      return window.localStorage.getItem('verbos:heroExpanded') === 'true'
    } catch {
      return false
    }
  })
  const audioWord = word

  const toggleHeroExpanded = useCallback((): void => {
    setHeroExpanded((prev) => {
      const next = !prev
      try {
        window.localStorage.setItem('verbos:heroExpanded', String(next))
      } catch {
        // ignore
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
        setCredit({ ...result, source: 'pexels' })
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

  const [trackedWord, setTrackedWord] = useState<string | null>(word)
  if (trackedWord !== word) {
    setTrackedWord(word)
    if (hasCustom && verb.imagen) {
      setSrc(verb.imagen)
    } else if (!pexelsAvailable) {
      setSrc(picsumUrl(verb))
      setCredit({ source: 'picsum' })
      setStage('picsum')
    } else {
      const cached = word ? getCachedImages(word) : null
      const first = cached?.[0]
      if (first) {
        setSrc(first.url)
        setCredit({ ...first, source: 'pexels' })
        setStage('pexels')
      } else {
        setSrc(null)
        setCredit(null)
        setStage('svg')
      }
    }
  }

  const refreshImage = useCallback(async (): Promise<void> => {
    if (!word || hasCustom || !pexelsAvailable || refreshing) return
    const existing = getCachedImages(word) ?? []
    const nextPage = existing.length + 1
    setRefreshing(true)
    try {
      const result = await fetchPexelsPhoto(word, nextPage)
      if (result) {
        addCachedImage(word, result)
        setSrc(result.url)
        setCredit({ ...result, source: 'pexels' })
        setStage('pexels')
      }
    } finally {
      setRefreshing(false)
    }
  }, [word, hasCustom, pexelsAvailable, refreshing])

  const onImgError = (): void => {
    if (stage === 'pexels') {
      setSrc(picsumUrl(verb))
      setCredit({ source: 'picsum' })
      setStage('picsum')
    } else if (stage === 'picsum' && !picsumFailed) {
      setPicsumFailed(true)
    }
  }

  const canRefresh = !hasCustom && pexelsAvailable && Boolean(word)

  useEffect(() => {
    if (!src || !onReady) return
    const source = hasCustom ? 'custom' : stage
    onReady({ imagen_url: src, image_source: source })
  }, [src, stage, hasCustom, onReady])

  const heightClass = heroExpanded
    ? 'h-[min(70vh,560px)] min-h-[280px]'
    : 'h-44 sm:h-52 md:h-56'
  const bgClass = heroExpanded ? 'bg-black/95' : 'bg-base-300'

  const imgClass = heroExpanded
    ? 'absolute inset-0 m-auto max-h-full max-w-full object-contain p-3'
    : 'absolute inset-0 h-full w-full object-cover'

  if (hasCustom) {
    return (
      <div className={`group relative w-full overflow-hidden ${bgClass} ${heightClass}`}>
        <HeroIllustration className="absolute inset-0 h-full w-full" />
        <img
          src={src ?? ''}
          alt={verb.infinitivo?.ing ?? ''}
          loading="lazy"
          decoding="async"
          onError={onImgError}
          className={imgClass}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/10" />
        <ImageCredit credit={credit} />
        <VerbImageOverlay
          audioWord={audioWord}
          heroExpanded={heroExpanded}
          onToggleExpand={toggleHeroExpanded}
          onAudioResolved={onAudioResolved}
        />
      </div>
    )
  }

  const showImg = Boolean(src) && !picsumFailed

  return (
    <div className={`group relative w-full overflow-hidden ${bgClass} ${heightClass}`}>
      <HeroIllustration className="absolute inset-0 h-full w-full" />
      {showImg ? (
        <img
          src={src ?? ''}
          alt={verb.infinitivo?.ing ?? ''}
          loading="lazy"
          decoding="async"
          onError={onImgError}
          className={imgClass}
        />
      ) : null}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/10" />
      <ImageCredit credit={credit} />
      <VerbImageOverlay
        audioWord={audioWord}
        onRefresh={refreshImage}
        canRefresh={canRefresh}
        refreshing={refreshing}
        heroExpanded={heroExpanded}
        onToggleExpand={toggleHeroExpanded}
        onAudioResolved={onAudioResolved}
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
  onAudioResolved,
}: {
  audioWord: string | null
  onRefresh?: () => void
  canRefresh?: boolean
  refreshing?: boolean
  heroExpanded?: boolean
  onToggleExpand?: () => void
  onAudioResolved?: (info: AudioResolution | null) => void
}) {
  const buttonRef = useRef<HTMLButtonElement | null>(null)

  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>): void => {
    const target = e.target as HTMLElement
    if (target.closest('button[data-overlay-control]')) return
    const btn = buttonRef.current
    if (!btn) return
    if (target === btn || btn.contains(target)) return
    btn.click()
  }

  return (
    <>
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-black/30 opacity-100 transition-opacity duration-300 md:opacity-0 md:group-hover:opacity-100 md:bg-black/50 md:backdrop-blur-[2px]"
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
        className="absolute top-2 left-2 z-30 inline-flex size-10 items-center justify-center rounded-full bg-black/50 text-white shadow-md backdrop-blur-sm transition hover:scale-105 hover:bg-black/70 active:scale-95 motion-reduce:animate-none"
      >
        {heroExpanded ? (
          <Minimize2 className="size-5" aria-hidden="true" />
        ) : (
          <Maximize2 className="size-5" aria-hidden="true" />
        )}
      </button>
      <div
        className="absolute inset-0 z-10 flex cursor-pointer items-center justify-center"
        onClick={handleOverlayClick}
      >
        <div className="transition-transform duration-300 group-hover:scale-110">
          <AudioButton ref={buttonRef} key={audioWord ?? ''} word={audioWord} onResolved={onAudioResolved} />
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
          className="absolute top-2 right-2 z-30 inline-flex size-10 items-center justify-center rounded-full bg-black/50 text-white shadow-md backdrop-blur-sm transition hover:scale-105 hover:bg-black/70 active:scale-95 disabled:opacity-50 disabled:hover:scale-100 motion-reduce:animate-none"
        >
          {refreshing ? (
            <Loader2
              className="size-5 animate-spin motion-reduce:animate-none"
              aria-hidden="true"
            />
          ) : (
            <Camera className="size-5" aria-hidden="true" />
          )}
        </button>
      ) : null}
    </>
  )
}

function SectionHeader({ title }: { title: string }) {
  return (
    <h2 className="mb-4 text-sm font-bold uppercase tracking-[0.18em] text-base-content sm:text-base">
      {title}
    </h2>
  )
}

function EmptyState() {
  return (
    <div className="rounded-2xl border border-base-300 bg-base-100 p-10 text-center shadow-sm">
      <div className="mx-auto mb-3 inline-flex size-12 items-center justify-center rounded-full bg-base-200 text-base-content/70">
        <SearchX className="size-6" aria-hidden="true" />
      </div>
      <p className="text-lg font-semibold text-base-content">No se encontraron verbos</p>
      <p className="mt-1 text-sm text-base-content/70">
        Ajusta la búsqueda o cambia los filtros para ver más resultados.
      </p>
    </div>
  )
}

function applyDragStyle(el: HTMLElement | null, x: number): void {
  if (!el) return
  el.style.transform = `translate3d(${x * DRAG_DAMPING}px, 0, 0)`
  el.style.opacity = String(
    Math.max(1 - DRAG_FADE_MAX, 1 - Math.min(DRAG_FADE_MAX, Math.abs(x) * 0.0035)),
  )
}

function clearDragStyle(el: HTMLElement | null): void {
  if (!el) return
  el.style.transition = 'transform 220ms cubic-bezier(0.22, 1, 0.36, 1), opacity 220ms ease-out'
  el.style.transform = `translate3d(0, 0, 0)`
  el.style.opacity = '1'
}

interface VerbCardProps {
  current: FlatVerb | null
  currentVerb: Verb | null
  oraciones: readonly OracionFillable[]
  conjugationEntries: readonly ConjugationGridEntry[]
  currentIndex: number
  total: number
  onPrev?: () => void
  onNext?: () => void
  onShuffle?: () => void
  onEnriched?: (
    verb: Verb,
    enrichment: {
      imagen_url: string
      image_source: string
      audio_url: string | null
      audio_source: string
    },
  ) => void
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
  onEnriched,
}: VerbCardProps) {
  const articleRef = useRef<HTMLElement | null>(null)
  const startRef = useRef<{ x: number; y: number } | null>(null)
  const lastRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 })

  const [imageInfo, setImageInfo] = useState<ImageResolution | null>(null)
  const [audioInfo, setAudioInfo] = useState<AudioResolution | null>(null)
  const [trackedVerbKey, setTrackedVerbKey] = useState<string | null>(
    currentVerb?.id != null ? String(currentVerb.id) : (currentVerb?.infinitivo?.ing ?? null),
  )
  const [renderId, setRenderId] = useState(0)
  const enrichedForVerb = useRef<string | null>(null)

  const verbKey: string | null =
    currentVerb?.id != null ? String(currentVerb.id) : (currentVerb?.infinitivo?.ing ?? null)
  if (trackedVerbKey !== verbKey) {
    setTrackedVerbKey(verbKey)
    setImageInfo(null)
    setAudioInfo(null)
    setRenderId((r) => r + 1)
  }

  useEffect(() => {
    enrichedForVerb.current = null
  }, [verbKey])

  const handleImageReady = useCallback((info: ImageResolution): void => {
    setImageInfo(info)
  }, [])

  const handleAudioResolved = useCallback((info: AudioResolution | null): void => {
    setAudioInfo(info)
  }, [])

  useEffect(() => {
    if (!imageInfo || !audioInfo) return
    if (currentVerb?.id == null) return
    const id = String(currentVerb.id)
    if (enrichedForVerb.current === id) return
    enrichedForVerb.current = id
    onEnriched?.(currentVerb, {
      imagen_url: imageInfo.imagen_url,
      image_source: imageInfo.image_source,
      audio_url: audioInfo.audio_url,
      audio_source: audioInfo.audio_source,
    })
  }, [imageInfo, audioInfo, currentVerb, onEnriched])

  const shouldAnimateVerbEnter =
    trackedVerbKey !== null && trackedVerbKey !== verbKey

  function handleTouchStart(e: React.TouchEvent<HTMLElement>): void {
    if (!e.touches || e.touches.length !== 1) return
    const t = e.touches[0]
    if (!t) return
    startRef.current = { x: t.clientX, y: t.clientY }
    lastRef.current = { x: 0, y: 0 }
    const el = articleRef.current
    if (el) {
      el.style.transition = 'none'
      applyDragStyle(el, 0)
    }
  }

  function handleTouchMove(e: React.TouchEvent<HTMLElement>): void {
    const start = startRef.current
    if (!start) return
    const t = e.touches[0]
    if (!t) return
    const dx = t.clientX - start.x
    const dy = t.clientY - start.y
    lastRef.current = { x: dx, y: dy }
    applyDragStyle(articleRef.current, dx)
  }

  function handleTouchEnd(): void {
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
  const tipSeed = currentVerb.id != null ? Number(currentVerb.id) : currentIndex

  return (
    <article
      ref={articleRef}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      onTouchCancel={handleTouchEnd}
      style={{ touchAction: 'pan-y', willChange: 'transform, opacity' }}
      className="overflow-hidden rounded-2xl border border-base-300 bg-base-100 shadow-sm transition-shadow hover:shadow-md"
    >
      <div key={`${verbKey}-${renderId}`}>
        <VerbImage
          verb={currentVerb}
          onReady={handleImageReady}
          onAudioResolved={handleAudioResolved}
        />
      </div>

      <div className="flex items-center justify-center border-b border-base-300 bg-base-200 px-4 py-3 sm:px-6">
        <NavButtons
          onPrev={onPrev}
          onNext={onNext}
          onShuffle={onShuffle}
          currentIndex={currentIndex}
          total={total}
        />
      </div>

      <div
        key={verbKey ?? ''}
        style={shouldAnimateVerbEnter ? { willChange: 'transform, opacity' } : undefined}
        className={
          'space-y-8 p-5 sm:p-7 md:p-8 ' +
          (shouldAnimateVerbEnter ? 'animate-verb-enter motion-reduce:animate-none' : '')
        }
      >
        <header className="text-center">
          <h1 className="text-5xl font-bold tracking-tight text-primary sm:text-6xl">
            {inf?.ing}
          </h1>
          <p className="mt-2 text-xl font-medium text-base-content/70 sm:text-2xl">
            {inf?.esp}
          </p>
        </header>

        <section>
          <SectionHeader title="Conjugaciones" />
          <ConjugationGrid entries={[...conjugationEntries]} seed={tipSeed} />
        </section>

        <section>
          <SectionHeader title="Oraciones en contexto" />
          <SentencesList oraciones={[...oraciones].map((o) => ({ timeKey: o.timeKey, data: { ing: o.data.ing, esp: o.data.esp } }))} />
        </section>

        {current?.category && (
          <p className="pt-1 text-center text-[0.7rem] uppercase tracking-[0.18em] text-base-content/70">
            {current.category}
            {current.subcategory ? ` · ${current.subcategory}` : ''}
          </p>
        )}
      </div>
    </article>
  )
}
