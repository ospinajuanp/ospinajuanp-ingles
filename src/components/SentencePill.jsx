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
      className="group cursor-pointer rounded-xl border border-slate-100 bg-white px-4 py-3 transition hover:border-indigo-200 hover:bg-indigo-50/40 hover:shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-200"
    >
      <div className="flex items-center gap-2 text-[0.65rem] font-bold uppercase tracking-[0.12em] text-slate-400">
        <span className="rounded-full bg-indigo-50 px-2 py-0.5 text-indigo-600">
          {pronombreLabel(data.pronombre)}
        </span>
        <span>{TIME_LABEL[timeKey] ?? timeKey}</span>
      </div>

      <p className="mt-1.5 text-lg font-medium leading-snug text-slate-800">
        {data.ing}
      </p>

      <p
        className={
          'mt-1 text-base leading-snug text-slate-500 transition-all duration-300 ease-out select-none ' +
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
      <p className="rounded-xl border border-dashed border-slate-200 bg-slate-50/40 px-4 py-6 text-center text-sm text-slate-400">
        No hay oraciones para este verbo todavía.
      </p>
    )
  }

  return (
    <div className="space-y-2">
      {oraciones.map(({ timeKey, data }) => (
        <SentencePill key={timeKey} timeKey={timeKey} data={data} />
      ))}
      <p className="pt-1 text-center text-[0.7rem] text-slate-400">
        Toca una oración para revelar la traducción
      </p>
    </div>
  )
}
