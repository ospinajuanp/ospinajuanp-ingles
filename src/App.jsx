import { useEffect, useState } from 'react'
import SearchBar from './components/SearchBar'
import CategoryFilter from './components/CategoryFilter'
import VerbCard from './components/VerbCard'
import { useVerbos } from './hooks/useVerbos'

function Header() {
  return (
    <header className="border-b border-slate-200/80 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-3xl items-center gap-3 px-4 py-4 sm:px-6">
        <div
          className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-sm"
          aria-hidden="true"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="size-5"
          >
            <path d="M4 5h12a3 3 0 0 1 3 3v11" />
            <path d="M2 5h14" />
            <path d="M5 8h9" />
            <path d="M9 19a2 2 0 1 1-2-2" />
            <path d="M19 19a2 2 0 1 1-2-2" />
          </svg>
        </div>
        <div className="min-w-0">
          <h1 className="truncate text-base font-bold text-slate-800 sm:text-lg">
            Verbos en Inglés
          </h1>
          <p className="truncate text-xs text-slate-500 sm:text-sm">
            Aprende conjugando, una frase a la vez
          </p>
        </div>
      </div>
    </header>
  )
}

function LoadingSkeleton() {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="h-56 w-full animate-pulse bg-slate-100 sm:h-64 md:h-72" />
      <div className="space-y-7 p-5 sm:p-7">
        <div className="space-y-3 text-center">
          <div className="mx-auto h-12 w-40 animate-pulse rounded-lg bg-slate-100" />
          <div className="mx-auto h-6 w-32 animate-pulse rounded-lg bg-slate-100" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-14 animate-pulse rounded-xl bg-slate-100" />
          ))}
        </div>
        <div className="space-y-2">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-20 animate-pulse rounded-xl bg-slate-100" />
          ))}
        </div>
      </div>
    </div>
  )
}

function ErrorState({ error, onRetry }) {
  return (
    <div className="rounded-2xl border border-red-100 bg-white p-8 text-center shadow-sm">
      <div className="mx-auto mb-3 inline-flex size-12 items-center justify-center rounded-full bg-red-50 text-red-500">
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
          <path d="M12 9v4" />
          <path d="M12 17h.01" />
          <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
        </svg>
      </div>
      <p className="text-lg font-semibold text-slate-800">No pudimos cargar los verbos</p>
      <p className="mt-1 text-sm text-slate-500">{error?.message ?? 'Error desconocido'}</p>
      <button
        type="button"
        onClick={onRetry}
        className="mt-4 inline-flex items-center gap-2 rounded-full bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-500 active:scale-95"
      >
        Reintentar
      </button>
    </div>
  )
}

export default function App() {
  const v = useVerbos()
  const [retryKey, setRetryKey] = useState(0)

  useEffect(() => {
    if (v.error) console.error('[verbos] failed to load', v.error)
  }, [v.error])

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <Header />

      <main className="mx-auto max-w-3xl space-y-5 px-4 py-5 pb-32 sm:px-6 sm:py-6">
        <SearchBar value={v.search} onChange={v.setSearch} />

        <CategoryFilter
          categories={v.categories}
          category={v.category}
          setCategory={v.setCategory}
          subcategory={v.subcategory}
          setSubcategory={v.setSubcategory}
        />

        {v.loading ? (
          <LoadingSkeleton />
        ) : v.error ? (
          <ErrorState error={v.error} onRetry={() => setRetryKey((k) => k + 1)} />
        ) : (
          <div key={retryKey}>
            <VerbCard
              current={v.current}
              currentVerb={v.currentVerb}
              oraciones={v.oraciones}
              conjugationEntries={v.conjugationEntries}
              currentIndex={v.currentIndex}
              total={v.total}
              onPrev={v.prev}
              onNext={v.next}
            />
          </div>
        )}

        {!v.loading && !v.error && v.total > 0 && (
          <p className="pt-2 text-center text-xs text-slate-400">
            Usa las flechas <kbd className="rounded border border-slate-200 bg-white px-1.5 py-0.5 font-mono text-[0.65rem]">←</kbd>{' '}
            <kbd className="rounded border border-slate-200 bg-white px-1.5 py-0.5 font-mono text-[0.65rem]">→</kbd>{' '}
            para cambiar de verbo.
          </p>
        )}
      </main>
    </div>
  )
}
