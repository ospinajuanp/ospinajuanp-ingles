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
    'mt-0.5 text-sm text-slate-500 transition-all duration-300 ease-out select-none ' +
    (revealed
      ? 'blur-0 opacity-100'
      : 'blur-sm opacity-60 group-hover:blur-0 group-hover:opacity-100')

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
      className="group cursor-pointer rounded-xl border border-slate-100 bg-white px-3 py-2.5 transition-all hover:border-indigo-200 hover:bg-indigo-50/40 hover:shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-200 sm:px-4 sm:py-3"
    >
      <div className="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-slate-400">
        {time}
      </div>
      <div className="mt-0.5 truncate text-base font-semibold text-slate-800 sm:text-lg">
        {value || '—'}
      </div>
      {valueEsp ? (
        <div className={spanishClass} aria-hidden={!revealed}>
          {valueEsp}
        </div>
      ) : null}
    </div>
  )
}

function TipCell({ tipTitle, value }) {
  return (
    <div className="relative overflow-hidden rounded-xl border border-indigo-100 bg-gradient-to-br from-indigo-50 via-white to-amber-50 px-3 py-2.5 sm:px-4 sm:py-3">
      <div className="flex items-center gap-1.5 text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-indigo-500">
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
      <p className="mt-1 text-sm font-medium leading-snug text-slate-700">{value}</p>
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