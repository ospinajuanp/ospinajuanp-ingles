'use client'

import Link from 'next/link'
import { Sparkles, LayoutGrid, ArrowRight } from 'lucide-react'
import { useVerbosContext } from '@/components/providers/VerbContext'
import HeroIllustration from '@/components/HeroIllustration'

export function HomePage() {
  const verbos = useVerbosContext()
  const totalVerbs = verbos?.counts?.total ?? 0
  const dueCount = verbos?.dueCount ?? 0

  const handleExplore = () => {
    verbos?.goToRandomVerb?.()
  }

  const statsLine =
    totalVerbs > 0
      ? `${totalVerbs} verbos disponibles${dueCount > 0 ? ` · ${dueCount} para repasar hoy` : ''}`
      : null

  return (
    <section className="mx-auto max-w-4xl px-4 py-6 sm:px-6 sm:py-8">
      <div className="hero relative overflow-hidden rounded-3xl border border-base-300 bg-base-200 shadow-sm">
        <HeroIllustration
          decorative
          className="pointer-events-none absolute inset-0 h-full w-full opacity-25"
        />
        <div className="hero-content relative w-full max-w-5xl flex-col gap-10 py-12 sm:py-16">
          <div className="text-center">
            <span className="badge badge-primary badge-outline mb-4 gap-2 px-3 py-3 text-[0.65rem] font-bold uppercase tracking-[0.18em]">
              <Sparkles className="size-4" aria-hidden="true" />
              Aprende conjugando
            </span>
            <h1 className="text-balance text-4xl font-extrabold tracking-tight text-base-content sm:text-5xl">
              Una frase a la vez, un verbo a la vez.
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-balance text-base sm:text-lg text-base-content/80">
              Explora conjugaciones en contexto o repasa lo que ya has
              visitado con repetición espaciada.
            </p>
            <p
              aria-live="polite"
              className="mt-4 min-h-[1.25rem] text-xs uppercase tracking-[0.18em] text-base-content/70"
            >
              {statsLine ?? '\u00A0'}
            </p>
          </div>

          <div className="grid w-full grid-cols-1 gap-5 sm:grid-cols-2">
            <article className="card border border-base-300 bg-base-100/95 shadow-sm backdrop-blur-sm transition hover:shadow-md motion-reduce:transition-none">
              <div className="card-body gap-4">
                <div className="inline-flex size-12 items-center justify-center rounded-2xl bg-primary/15 text-primary">
                  <LayoutGrid className="size-6" aria-hidden="true" />
                </div>
                <h2 className="card-title text-2xl font-bold text-base-content">
                  Explorar Verbos
                </h2>
                <p className="text-sm text-base-content/80">
                  Lanza un verbo al azar y trabaja con sus conjugaciones y
                  oraciones de ejemplo. Usa las flechas del teclado o los
                  botones para moverte entre verbos.
                </p>
                <div className="card-actions justify-end pt-2">
                  <button
                    type="button"
                    onClick={handleExplore}
                    disabled={totalVerbs === 0}
                    className="btn btn-primary gap-2 rounded-full px-5 normal-case shadow-sm transition active:scale-95 motion-reduce:transform-none disabled:opacity-60"
                  >
                    Empezar
                    <ArrowRight className="size-4" aria-hidden="true" />
                  </button>
                </div>
              </div>
            </article>

            <article className="card border border-base-300 bg-base-100/95 shadow-sm backdrop-blur-sm transition hover:shadow-md motion-reduce:transition-none">
              <div className="card-body gap-4">
                <div className="inline-flex size-12 items-center justify-center rounded-2xl bg-success/15 text-success">
                  <Sparkles className="size-6" aria-hidden="true" />
                </div>
                <h2 className="card-title text-2xl font-bold text-base-content">
                  Repasar
                </h2>
                <p className="text-sm text-base-content/80">
                  Sesión de tarjetas con SM-2 de 4 niveles: mezcla tus
                  oraciones personalizadas con los verbos que ya visitaste.
                </p>
                <div className="card-actions justify-end pt-2">
                  <Link
                    href="/v1/test"
                    className="btn btn-outline btn-primary gap-2 rounded-full px-5 normal-case shadow-sm transition active:scale-95 motion-reduce:transform-none"
                  >
                    Abrir repaso
                    <ArrowRight className="size-4" aria-hidden="true" />
                  </Link>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </section>
  )
}
