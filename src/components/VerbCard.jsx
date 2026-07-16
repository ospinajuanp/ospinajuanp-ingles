import { useState } from 'react'
import ConjugationGrid from './ConjugationGrid'
import SentencesList from './SentencePill'
import NavButtons from './NavButtons'
import HeroIllustration from './HeroIllustration'

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
      {!(verb.imagen?.trim()) ? null : (
        <img
          src={src}
          alt={verb.infinitivo?.ing ?? ''}
          loading="lazy"
          decoding="async"
          onError={onError}
          className="absolute inset-0 h-full w-full object-cover"
        />
      )}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-slate-900/10" />
    </div>
  )
}

function SectionHeader({ title, action }) {
  return (
    <div className="mb-4 flex items-center justify-between">
      <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-slate-900 sm:text-base">
        {title}
      </h2>
      {action}
    </div>
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
  const tipSeed = currentVerb.id ?? currentIndex ?? 0

  return (
    <article className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-md">
      <VerbImage verb={currentVerb} />

      <div className="space-y-8 p-5 sm:p-7 md:p-8">
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
