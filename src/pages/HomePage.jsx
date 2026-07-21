// Landing page. Two big actions:
//
//   • "Explorar Verbos" → calls goToRandomVerb() (weighted random from
//     the full corpus, then navigates into /v1/verbs/<slug>).
//   • "Repasar"        → navigates to /v1/test.
//
// Uses DaisyUI primitives (`hero`, `card`, `btn`) so the page adopts the
// active theme tokens automatically. The existing VerbCard keeps its
// hand-rolled styling on the verb view to avoid touching unrelated
// visuals — only this page + the theme switcher pull from DaisyUI.

import { Link } from 'react-router-dom'
import { Sparkles, LayoutGrid, ArrowRight } from 'lucide-react'
import { useVerbosContext } from '../contexts/VerbContext'

export default function HomePage() {
  const verbos = useVerbosContext()
  const totalVerbs = verbos?.counts?.total ?? 0
  const dueCount = verbos?.dueCount ?? 0

  const handleExplore = () => {
    verbos?.goToRandomVerb?.()
  }

  return (
    <div className="hero bg-base-200 rounded-3xl border border-base-300 shadow-sm">
      <div className="hero-content w-full max-w-5xl flex-col gap-10 py-12 sm:py-16">
        <div className="text-center">
          <span className="badge badge-primary badge-outline mb-4 gap-2 px-3 py-3 text-[0.65rem] font-bold uppercase tracking-[0.18em]">
            <Sparkles className="size-4" aria-hidden="true" />
            Aprende conjugando
          </span>
          <h1 className="text-balance text-4xl font-extrabold tracking-tight text-base-content sm:text-5xl">
            Una frase a la vez, un verbo a la vez.
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-balance text-base sm:text-lg text-base-content/70">
            Explora conjugaciones en contexto o repasa lo que ya has
            visitado con repetición espaciada.
          </p>
          {totalVerbs > 0 ? (
            <p className="mt-4 text-xs uppercase tracking-[0.18em] text-base-content/50">
              {totalVerbs} verbos disponibles
              {dueCount > 0 ? ` · ${dueCount} para repasar hoy` : ''}
            </p>
          ) : null}
        </div>

        <div className="grid w-full grid-cols-1 gap-5 sm:grid-cols-2">
          <article className="card bg-base-100 border border-base-300 shadow-sm transition hover:shadow-md">
            <div className="card-body gap-4">
              <div className="inline-flex size-12 items-center justify-center rounded-2xl bg-primary/15 text-primary">
                <LayoutGrid className="size-6" aria-hidden="true" />
              </div>
              <h2 className="card-title text-2xl font-bold text-base-content">
                Explorar Verbos
              </h2>
              <p className="text-sm text-base-content/70">
                Lanza un verbo al azar y trabaja con sus conjugaciones y
                oraciones de ejemplo. Usa las flechas para moverte o el
                atajo de teclado.
              </p>
              <div className="card-actions justify-end pt-2">
                <button
                  type="button"
                  onClick={handleExplore}
                  disabled={totalVerbs === 0}
                  className="btn btn-primary gap-2 rounded-full px-5 normal-case shadow-sm transition active:scale-95 disabled:opacity-60"
                >
                  Empezar
                  <ArrowRight className="size-4" aria-hidden="true" />
                </button>
              </div>
            </div>
          </article>

          <article className="card bg-base-100 border border-base-300 shadow-sm transition hover:shadow-md">
            <div className="card-body gap-4">
              <div className="inline-flex size-12 items-center justify-center rounded-2xl bg-success/15 text-success">
                <Sparkles className="size-6" aria-hidden="true" />
              </div>
              <h2 className="card-title text-2xl font-bold text-base-content">
                Repasar
              </h2>
              <p className="text-sm text-base-content/70">
                Sesión de tarjetas con SM-2 de 4 niveles: mezcla tus
                oraciones personalizadas con los verbos que ya visitaste.
              </p>
              <div className="card-actions justify-end pt-2">
                <Link
                  to="/v1/test"
                  className="btn btn-outline btn-primary gap-2 rounded-full px-5 normal-case shadow-sm transition active:scale-95"
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
  )
}
