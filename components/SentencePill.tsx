'use client'
import { useCallback, useState } from 'react'
import { Eye, EyeOff } from 'lucide-react'
import type { TiempoConjugacion } from '@/lib/types/verbs'

const TIME_LABEL: Record<TiempoConjugacion, string> = {
  infinitivo: 'Infinitivo',
  pasadoSimple: 'Pasado',
  participio: 'Participio',
  gerundio: 'Gerundio',
  futuro: 'Futuro',
  condicional: 'Condicional',
}

export interface SentencePillData {
  ing: string
  esp: string
}

interface SentencePillProps {
  timeKey: TiempoConjugacion
  data: SentencePillData
}

export function SentencePill({ timeKey, data }: SentencePillProps) {
  const [revealed, setRevealed] = useState(false)

  const onEnter = useCallback(() => setRevealed(true), [])
  const onLeave = useCallback(() => setRevealed(false), [])
  const onClick = useCallback(() => setRevealed((r) => !r), [])
  const RevealIcon = revealed ? Eye : EyeOff

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
      aria-label={`${TIME_LABEL[timeKey] ?? timeKey}: ${data.ing}`}
      className="group cursor-pointer rounded-xl border border-base-300 bg-base-100 p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-primary/40 hover:bg-gradient-to-br hover:from-base-100 hover:to-primary/10 hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 motion-reduce:transition-none"
    >
      <div className="flex items-center justify-between gap-2">
        <span className="rounded-full bg-primary/15 px-2.5 py-1 text-[0.65rem] font-bold uppercase tracking-[0.12em] text-primary">
          {TIME_LABEL[timeKey] ?? timeKey}
        </span>

        <span
          className={
            'inline-flex size-7 items-center justify-center rounded-full border transition ' +
            (revealed
              ? 'border-primary/40 bg-primary/10 text-primary'
              : 'border-base-300 bg-base-200 text-base-content/60 group-hover:border-primary/40 group-hover:text-primary/80')
          }
          aria-hidden="true"
        >
          <RevealIcon className="size-4" />
        </span>
      </div>

      <p className="mt-3 text-lg font-medium leading-snug text-base-content">
        {data.ing}
      </p>

      <p
        className={
          'mt-2 text-base leading-snug text-base-content/70 transition-all duration-300 ease-out select-none motion-reduce:transition-none ' +
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

export default function SentencesList({
  oraciones,
}: {
  oraciones?: readonly { timeKey: TiempoConjugacion; data: SentencePillData }[]
}) {
  if (!oraciones || oraciones.length === 0) {
    return (
      <p className="rounded-xl border border-dashed border-base-300 bg-base-200/40 px-4 py-6 text-center text-sm text-base-content/70">
        No hay oraciones para este verbo todavía.
      </p>
    )
  }

  return (
    <div className="space-y-2.5">
      {oraciones.map(({ timeKey, data }) => (
        <SentencePill key={timeKey} timeKey={timeKey} data={data} />
      ))}
      <p className="pt-1 text-center text-[0.7rem] text-base-content/70">
        Toca una oración para revelar la traducción
      </p>
    </div>
  )
}
