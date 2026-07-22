'use client'
import { useCallback, useState } from 'react'
import { Eye, EyeOff, Lightbulb } from 'lucide-react'
import { selectTip } from '@/lib/utils/tips'

interface ConjugationCellProps {
  time: string
  value: string | undefined
  valueEsp?: string | undefined
}

function ConjugationCell({ time, value, valueEsp }: ConjugationCellProps) {
  const [revealed, setRevealed] = useState(false)

  const onEnter = useCallback(() => setRevealed(true), [])
  const onLeave = useCallback(() => setRevealed(false), [])
  const onClick = useCallback(() => setRevealed((r) => !r), [])

  const onKeyDown = useCallback((e: React.KeyboardEvent<HTMLDivElement>) => {
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
  const RevealIcon = revealed ? Eye : EyeOff

  return (
    <div
      onMouseEnter={onEnter}
      onMouseLeave={onLeave}
      onClick={onClick}
      onKeyDown={onKeyDown}
      role="button"
      tabIndex={0}
      aria-pressed={revealed}
      aria-label={`${time}: ${value ?? ''}${valueEsp ? `, traducción: ${valueEsp}` : ''}`}
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
            <RevealIcon className="size-3" />
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

function TipCell({ tipTitle, value }: { tipTitle: string; value: string }) {
  return (
    <div className="relative overflow-hidden rounded-xl border border-primary/20 bg-gradient-to-br from-primary/10 via-base-100 to-warning/10 px-3 py-2.5 sm:px-4 sm:py-3">
      <div className="flex items-center gap-1.5 text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-primary">
        <Lightbulb className="size-3.5" aria-hidden="true" />
        <span>{tipTitle}</span>
      </div>
      <p className="mt-1 whitespace-pre-line text-sm font-medium leading-snug text-base-content/80">
        {value}
      </p>
    </div>
  )
}

interface ConjugationGridProps {
  entries?: readonly {
    time: string
    value: string | undefined
    valueEsp?: string | undefined
  }[]
  seed?: number
}

export default function ConjugationGrid({ entries, seed = 0 }: ConjugationGridProps) {
  const tip = selectTip(seed)
  const allCells = [
    ...(entries ?? []).map((e) => ({ kind: 'entry' as const, ...e })),
    { kind: 'tip' as const, time: 'Tip', tipTitle: tip.title, value: tip.text },
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
