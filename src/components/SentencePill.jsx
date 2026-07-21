import { useCallback, useState } from 'react'

const PRONOMBRE_LABEL = {
  yo: 'Yo',
  tu: 'Tú',
  el_ella: 'Él/Ella',
  ellos: 'Ellos',
  nosotros: 'Nosotros',
  eso: 'Eso',
}

function pronombreLabel(p) {
  return PRONOMBRE_LABEL[p] ?? p
}

const TIME_LABEL = {
  infinitivo: 'Infinitivo',
  pasadoSimple: 'Pasado',
  participio: 'Participio',
  gerundio: 'Gerundio',
  futuro: 'Futuro',
  condicional: 'Condicional',
}

export function SentencePill({ timeKey, data }) {
  const [revealed, setRevealed] = useState(false)

  const onEnter = useCallback(() => setRevealed(true), [])
  const onLeave = useCallback(() => setRevealed(false), [])
  const onClick = useCallback(() => setRevealed((r) => !r), [])

  return (
    <div
      onMouseEnter={onEnter}
      onMouseLeave={onLeave}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          setRevealed((r) => !r)
        }
      }}
      aria-pressed={revealed}
      className="group cursor-pointer rounded-xl border border-base-300 bg-base-100 p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-primary/40 hover:bg-gradient-to-br hover:from-base-100 hover:to-primary/10 hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/40"
    >
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-primary/15 px-2.5 py-1 text-[0.65rem] font-bold uppercase tracking-[0.12em] text-primary">
            {pronombreLabel(data.pronombre)}
          </span>
          <span className="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-base-content/50">
            {TIME_LABEL[timeKey] ?? timeKey}
          </span>
        </div>

        <span
          className={
            'inline-flex size-7 items-center justify-center rounded-full border transition ' +
            (revealed
              ? 'border-primary/40 bg-primary/10 text-primary'
              : 'border-base-300 bg-base-200 text-base-content/50 group-hover:border-primary/40 group-hover:text-primary/80')
          }
          aria-hidden="true"
        >
          {revealed ? (
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="size-4"
            >
              <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z" />
              <circle cx="12" cy="12" r="3" />
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
            >
              <path d="M17.94 17.94A10.94 10.94 0 0 1 12 19c-7 0-10-7-10-7a18.45 18.45 0 0 1 4.06-5.94" />
              <path d="M9.9 4.24A10.94 10.94 0 0 1 12 4c7 0 10 7 10 7a18.5 18.5 0 0 1-2.16 3.19" />
              <path d="M14.12 14.12A3 3 0 1 1 9.88 9.88" />
              <path d="m1 1 22 22" />
            </svg>
          )}
        </span>
      </div>

      <p className="mt-3 text-lg font-medium leading-snug text-base-content">
        {data.ing}
      </p>

      <p
        className={
          'mt-2 text-base leading-snug text-base-content/70 transition-all duration-300 ease-out select-none ' +
          (revealed
            ? 'blur-0 opacity-100'
            : 'blur-sm opacity-60 group-hover:blur-0 group-hover:opacity-100')
        }
        aria-hidden={!revealed}
      >
        {data.esp}
      </p>
    </div>
  )
}

export default function SentencesList({ oraciones }) {
  if (!oraciones || oraciones.length === 0) {
    return (
      <p className="rounded-xl border border-dashed border-base-300 bg-base-200/40 px-4 py-6 text-center text-sm text-base-content/50">
        No hay oraciones para este verbo todavía.
      </p>
    )
  }

  return (
    <div className="space-y-2.5">
      {oraciones.map(({ timeKey, data }) => (
        <SentencePill key={timeKey} timeKey={timeKey} data={data} />
      ))}
      <p className="pt-1 text-center text-[0.7rem] text-base-content/50">
        Toca una oración para revelar la traducción
      </p>
    </div>
  )
}
