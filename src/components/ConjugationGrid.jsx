import { useCallback, useState } from 'react'
import { selectTip } from '../utils/tips'

function ConjugationCell({ time, value, valueEsp }) {
  const [revealed, setRevealed] = useState(false)

  const onEnter = useCallback(() => setRevealed(true), [])
  const onLeave = useCallback(() => setRevealed(false), [])
  const onClick = useCallback(() => setRevealed((r) => !r), [])

  const onKeyDown = useCallback((e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      setRevealed((r) => !r)
    }
  }, [])

  const spanishClass =
    'mt-0.5 text-sm text-base-content/70 transition-all duration-300 ease-out select-none ' +
    (revealed
      ? 'blur-0 opacity-100'
      : 'blur-sm opacity-60 group-hover:blur-0 group-hover:opacity-100')

  const hasSpanish = Boolean(valueEsp)

  return (
    <div
      onMouseEnter={onEnter}
      onMouseLeave={onLeave}
      onClick={onClick}
      onKeyDown={onKeyDown}
      role="button"
      tabIndex={0}
      aria-pressed={revealed}
      aria-label={`${time}: ${value}${valueEsp ? `, traducción: ${valueEsp}` : ''}`}
      className="group cursor-pointer rounded-xl border border-base-300 bg-base-100 px-3 py-2.5 transition-all hover:border-primary/40 hover:bg-primary/5 hover:shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 sm:px-4 sm:py-3"
    >
      <div className="flex items-center justify-between gap-2">
        <div className="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-base-content/50">
          {time}
        </div>
        {hasSpanish ? (
          <span
            className={
              'inline-flex size-5 items-center justify-center rounded-full border transition ' +
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
                className="size-3"
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
                className="size-3"
              >
                <path d="M17.94 17.94A10.94 10.94 0 0 1 12 19c-7 0-10-7-10-7a18.45 18.45 0 0 1 4.06-5.94" />
                <path d="M9.9 4.24A10.94 10.94 0 0 1 12 4c7 0 10 7 10 7a18.5 18.5 0 0 1-2.16 3.19" />
                <path d="M14.12 14.12A3 3 0 1 1 9.88 9.88" />
                <path d="m1 1 22 22" />
              </svg>
            )}
          </span>
        ) : null}
      </div>
      <div className="mt-0.5 truncate text-base font-semibold text-base-content sm:text-lg">
        {value || '—'}
      </div>
      {hasSpanish ? (
        <div className={spanishClass} aria-hidden={!revealed}>
          {valueEsp}
        </div>
      ) : null}
    </div>
  )
}

function TipCell({ tipTitle, value }) {
  return (
    <div className="relative overflow-hidden rounded-xl border border-primary/20 bg-gradient-to-br from-primary/10 via-base-100 to-warning/10 px-3 py-2.5 sm:px-4 sm:py-3">
      <div className="flex items-center gap-1.5 text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-primary">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="size-3.5"
          aria-hidden="true"
        >
          <path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.74V17a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-2.26A7 7 0 0 0 12 2z" />
        </svg>
        <span>{tipTitle}</span>
      </div>
      <p className="mt-1 whitespace-pre-line text-sm font-medium leading-snug text-base-content/80">{value}</p>
    </div>
  )
}

export default function ConjugationGrid({ entries, seed = 0 }) {
  const tip = selectTip(seed)
  const allCells = [
    ...(entries ?? []).map((e) => ({ kind: 'entry', ...e })),
    { kind: 'tip', time: 'Tip', tipTitle: tip.title, value: tip.text },
  ]

  return (
    <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3 sm:gap-3">
      {allCells.map((cell, i) =>
        cell.kind === 'tip' ? (
          <TipCell
            key={`tip-${i}`}
            tipTitle={cell.tipTitle}
            value={cell.value}
          />
        ) : (
          <ConjugationCell
            key={`${cell.time}-${i}`}
            time={cell.time}
            value={cell.value}
            valueEsp={cell.valueEsp}
          />
        ),
      )}
    </div>
  )
}
