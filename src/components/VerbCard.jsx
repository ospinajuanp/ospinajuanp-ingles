import { useRef, useState } from 'react'
import ConjugationGrid from './ConjugationGrid'
import SentencesList from './SentencePill'
import NavButtons from './NavButtons'
import HeroIllustration from './HeroIllustration'

const SWIPE_THRESHOLD = 70
const SWIPE_AXIS_RATIO = 1.5
const SWIPE_MAX_ABS = 240
const DRAG_DAMPING = 0.32
const DRAG_FADE_MAX = 0.25

function remoteFallbackUrl(verb) {
  const word = verb?.infinitivo?.ing ?? 'english'
  return `https://source.unsplash.com/featured/?${encodeURIComponent(word)}`
}

function finalFallbackUrl(verb) {
  const word = verb?.infinitivo?.ing ?? 'english'
  return `https://picsum.photos/seed/${encodeURIComponent(word)}/800/400`
}

function VerbImage({ verb }) {
  const initial = verb.imagen?.trim() ? verb.imagen : remoteFallbackUrl(verb)
  const [src, setSrc] = useState(initial)
  const [stage, setStage] = useState(verb.imagen?.trim() ? 'custom' : 'remote')

  const onError = () => {
    if (stage === 'custom' || stage === 'remote') {
      setStage('picsum')
      setSrc(finalFallbackUrl(verb))
    }
  }

  if (stage === 'picsum') {
    return (
      <img
        src={src}
        alt={verb.infinitivo?.ing ?? ''}
        loading="lazy"
        decoding="async"
        onError={onError}
        className="h-44 w-full object-cover sm:h-52 md:h-56"
      />
    )
  }

  return (
    <div className="relative h-44 w-full overflow-hidden bg-slate-100 sm:h-52 md:h-56">
      <HeroIllustration className="absolute inset-0 h-full w-full" />
      {verb.imagen?.trim() ? (
        <img
          src={src}
          alt={verb.infinitivo?.ing ?? ''}
          loading="lazy"
          decoding="async"
          onError={onError}
          className="absolute inset-0 h-full w-full object-cover"
        />
      ) : null}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-slate-900/10" />
    </div>
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
