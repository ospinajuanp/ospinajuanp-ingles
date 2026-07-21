// 3D flip card. Spanish on the front, English on the back.
//
// Animation: pure CSS (inline styles + Tailwind v4 utilities). The inner
// button rotates around its Y axis on click; the two faces use
// `[backface-visibility:hidden]` and one of them carries
// `[transform:rotateY(180deg)]` so it appears when the container flips.
//
// NO setState-in-useEffect: derived-state pattern is used for tracking
// the active card id (matches VerbCard's VerbImage pattern).
//
// Grading is 4-level SM-2: fail / hard / good / easy. EF delta per grade:
//   fail  → -0.20, interval = 1
//   hard  → -0.10, interval grows by EF (with 1d → 3d → *EF ramp)
//   good  →  0.00, interval grows by EF
//   easy  → +0.15, interval grows by EF
//   floor → 1.30 (SRS_MIN_EF, applied inside the algorithm)
//
// Theme notes: card surfaces use `bg-base-100` so the front re-skins per
// theme; the back keeps a primary-tinted gradient so the "answer" face
// stays visually distinct. The four grade buttons use semantic colors
// (rose / amber / emerald / sky) so the meaning travels across themes.

import { useCallback, useState } from 'react'

const FLIP_DURATION_MS = 600

const GRADE_BUTTONS = [
  {
    grade: 'fail',
    label: 'Otra vez',
    hint: 'Repetir mañana',
    classes:
      'border border-error/40 bg-base-100 text-error hover:bg-error/10',
    icon: (
      <path d="M18 6 6 18M6 6l12 12" />
    ),
  },
  {
    grade: 'hard',
    label: 'Difícil',
    hint: 'Me costó recordar',
    classes:
      'border border-warning/40 bg-base-100 text-warning hover:bg-warning/10',
    icon: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.8.4-1 .9-1 1.7" />
        <path d="M12 17h.01" />
      </>
    ),
  },
  {
    grade: 'good',
    label: 'Bien',
    hint: 'Lo recordé',
    classes:
      'border border-success/40 bg-base-100 text-success hover:bg-success/10',
    icon: <path d="M20 6 9 17l-5-5" />,
  },
  {
    grade: 'easy',
    label: 'Fácil',
    hint: 'Al instante',
    classes:
      'border border-info/40 bg-gradient-to-br from-info to-info/80 text-white shadow-md hover:from-info/90 hover:to-info/70',
    icon: (
      <>
        <path d="m12 2 2.4 5 5.6.6-4.2 3.7 1.2 5.7L12 14.3 7 17l1.2-5.7L4 7.6 9.6 7z" />
      </>
    ),
  },
]

export default function Flashcard({ card, onGrade }) {
  const [flipped, setFlipped] = useState(false)
  const [trackedId, setTrackedId] = useState(card?.id ?? null)
  const [busy, setBusy] = useState(false)

  // Derived-state reset: when the parent swaps in a new card (different
  // id), rewind flip + busy flags during render. The caller can also
  // `key={card.id}` to remount, but we keep this as a safety net.
  if (trackedId !== (card?.id ?? null)) {
    setTrackedId(card?.id ?? null)
    setFlipped(false)
    setBusy(false)
  }

  const handleFlip = useCallback(() => {
    if (busy) return
    setFlipped((f) => !f)
  }, [busy])

  const handleGrade = useCallback(
    (grade) => (e) => {
      e.stopPropagation()
      if (busy || !card) return
      setBusy(true)
      // Yield one frame so the user visually registers the result before
      // the parent advances to the next card.
      setTimeout(() => {
        onGrade?.(card.id, grade)
      }, 80)
    },
    [busy, card, onGrade],
  )

  if (!card) return null

  const isCustom = card.type === 'custom'
  const front = isCustom ? card.front?.es : card.infinitivo?.esp ?? ''
  const back = isCustom ? card.front?.en : card.infinitivo?.ing ?? ''
  const subtitle = isCustom ? 'Oración personalizada' : 'Verbo visto'
  const frontLabel = isCustom ? 'Español' : 'Español'
  const backLabel = isCustom ? 'Inglés' : 'Infinitivo'

  return (
    <div className="w-full">
      <div className="relative mx-auto aspect-[3/2] w-full max-w-xl [perspective:1200px]">
        <button
          type="button"
          onClick={handleFlip}
          aria-pressed={flipped}
          aria-label={flipped ? 'Mostrar pregunta' : 'Mostrar respuesta'}
          className="relative h-full w-full cursor-pointer rounded-3xl bg-transparent p-0 text-left [transform-style:preserve-3d]"
          style={{
            transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
            transition: `transform ${FLIP_DURATION_MS}ms cubic-bezier(0.22, 1, 0.36, 1)`,
          }}
        >
          {/* Front */}
          <div
            className="absolute inset-0 flex flex-col items-center justify-center rounded-3xl border border-base-300 bg-base-100 p-6 text-center shadow-md [backface-visibility:hidden]"
            aria-hidden={flipped}
          >
            <span className="mb-3 inline-flex items-center rounded-full bg-primary/15 px-3 py-1 text-[0.65rem] font-bold uppercase tracking-[0.18em] text-primary">
              {frontLabel}
            </span>
            <p className="text-balance text-2xl font-semibold leading-snug text-base-content sm:text-3xl">
              {front}
            </p>
            <p className="mt-6 text-xs text-base-content/50">{subtitle}</p>
            <p className="mt-2 text-[0.65rem] uppercase tracking-[0.2em] text-base-content/40">
              Toca para voltear
            </p>
          </div>

          {/* Back */}
          <div
            className="absolute inset-0 flex flex-col items-center justify-center rounded-3xl border border-primary/40 bg-gradient-to-br from-primary to-primary/80 p-6 text-center text-primary-content shadow-md [backface-visibility:hidden] [transform:rotateY(180deg)]"
            aria-hidden={!flipped}
          >
            <span className="mb-3 inline-flex items-center rounded-full bg-primary-content/15 px-3 py-1 text-[0.65rem] font-bold uppercase tracking-[0.18em] text-primary-content">
              {backLabel}
            </span>
            <p className="text-balance text-2xl font-semibold leading-snug sm:text-3xl">
              {back}
            </p>
            <p className="mt-6 text-xs text-primary-content/80">{subtitle}</p>
          </div>
        </button>
      </div>

      {/* Grade controls — 4-level SM-2. Only meaningful after the card is
          flipped; rendered as a 2-col grid on mobile, 4-col row on sm+. */}
      <div
        role="group"
        aria-label="Calificación de la tarjeta"
        aria-hidden={!flipped}
        className="mx-auto mt-6 grid max-w-xl grid-cols-2 gap-2 sm:grid-cols-4 sm:gap-3"
      >
        {GRADE_BUTTONS.map(({ grade, label, hint, classes, icon }) => (
          <button
            key={grade}
            type="button"
            onClick={handleGrade(grade)}
            disabled={!flipped || busy}
            aria-label={`${label} — ${hint}`}
            className={`inline-flex items-center justify-center gap-1.5 rounded-2xl px-3 py-2.5 text-sm font-semibold transition active:scale-95 disabled:cursor-not-allowed disabled:opacity-50 sm:flex-col sm:gap-0 sm:rounded-full sm:px-2 sm:py-2.5 ${classes}`}
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="size-4 shrink-0 sm:size-3.5"
              aria-hidden="true"
            >
              {icon}
            </svg>
            <span>{label}</span>
            <span className="hidden text-[0.65rem] font-medium uppercase tracking-wider opacity-70 sm:inline">
              {hint}
            </span>
          </button>
        ))}
      </div>

      {card.srs ? (
        <p className="mx-auto mt-4 max-w-xl text-center text-xs text-base-content/50">
          {card.srs.interval === 0
            ? 'Tarjeta nueva'
            : `Repaso cada ${card.srs.interval} ${card.srs.interval === 1 ? 'día' : 'días'} · EF ${card.srs.ef.toFixed(2)}`}
        </p>
      ) : null}
    </div>
  )
}
