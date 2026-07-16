import { useState } from 'react'
import ConjugationGrid from './ConjugationGrid'
import SentencesList from './SentencePill'
import NavButtons from './NavButtons'

function fallbackUrl(verb) {
  const word = verb?.infinitivo?.ing ?? 'english'
  return `https://source.unsplash.com/featured/?${encodeURIComponent(word)}`
}

function finalFallbackUrl(verb) {
  const word = verb?.infinitivo?.ing ?? 'english'
  return `https://picsum.photos/seed/${encodeURIComponent(word)}/800/400`
}

function VerbImage({ verb }) {
  const primary = verb.imagen?.trim() ? verb.imagen : fallbackUrl(verb)
  const [src, setSrc] = useState(primary)
  const [failed, setFailed] = useState(false)

  const onError = () => {
    if (!failed) {
      setFailed(true)
      setSrc(finalFallbackUrl(verb))
    }
  }

  return (
    <img
      src={src}
      alt={verb.infinitivo?.ing ?? ''}
      loading="lazy"
      decoding="async"
      onError={onError}
      className="h-56 w-full object-cover sm:h-64 md:h-72"
    />
  )
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
}) {
  if (!currentVerb) {
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

  const inf = currentVerb.infinitivo

  return (
    <article className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-md">
      <div className="overflow-hidden rounded-t-2xl bg-slate-100">
        <VerbImage verb={currentVerb} />
      </div>

      <div className="space-y-7 p-5 sm:p-7">
        <header className="text-center">
          <h1 className="text-5xl font-bold tracking-tight text-indigo-600 sm:text-6xl">
            {inf?.ing}
          </h1>
          <p className="mt-1 text-xl font-medium text-slate-500 sm:text-2xl">
            {inf?.esp}
          </p>
        </header>

        <section>
          <h2 className="mb-3 text-[0.7rem] font-bold uppercase tracking-[0.18em] text-slate-400">
            Conjugaciones
          </h2>
          <ConjugationGrid entries={conjugationEntries} />
        </section>

        <section>
          <h2 className="mb-3 text-[0.7rem] font-bold uppercase tracking-[0.18em] text-slate-400">
            Oraciones en contexto
          </h2>
          <SentencesList oraciones={oraciones} />
        </section>

        {current?.subcategory && (
          <p className="pt-1 text-center text-xs text-slate-300">
            {current.category} · {current.subcategory}
          </p>
        )}

        <NavButtons
          onPrev={onPrev}
          onNext={onNext}
          currentIndex={currentIndex}
          total={total}
        />
      </div>
    </article>
  )
}
