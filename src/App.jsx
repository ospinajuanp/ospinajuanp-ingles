import { useEffect, useState } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import SearchBar from './components/SearchBar'
import CategoryFilter from './components/CategoryFilter'
import VerbCard from './components/VerbCard'
import { useVerbos } from './hooks/useVerbos'
import { VerbProvider, useVerbosContext } from './contexts/VerbContext'
import { checkPexelsStatus } from './utils/pexels'

function BrandIcon() {
  return (
    <img
      src="/icon.ico"
      alt=""
      width="32"
      height="32"
      className="size-10 shrink-0 rounded-xl"
    />
  )
}

function Header({ children }) {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-3 sm:px-6 sm:py-4 lg:grid lg:grid-cols-[1fr_2fr_1fr] lg:items-center lg:gap-8">
        {children}
      </div>
    </header>
  )
}

function LoadingSkeleton() {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="h-44 w-full animate-pulse bg-slate-100 sm:h-52 md:h-56" />
      <div className="space-y-8 p-5 sm:p-7 md:p-8">
        <div className="space-y-3 text-center">
          <div className="mx-auto h-12 w-40 animate-pulse rounded-lg bg-slate-100" />
          <div className="mx-auto h-6 w-32 animate-pulse rounded-lg bg-slate-100" />
        </div>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-16 animate-pulse rounded-xl bg-slate-100" />
          ))}
        </div>
        <div className="space-y-2.5">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-24 animate-pulse rounded-xl bg-slate-100" />
          ))}
        </div>
        <div className="flex justify-center">
          <div className="h-12 w-64 animate-pulse rounded-full bg-slate-100" />
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

function ShellHeader() {
  const verbos = useVerbosContext()
  return (
    <Header>
      <div className="flex items-center gap-3">
        <div className="shrink-0 overflow-hidden rounded-xl shadow-sm ring-1 ring-slate-200/80" aria-hidden="true">
          <BrandIcon />
        </div>
        <div className="min-w-0">
          <h1 className="truncate text-base font-bold text-slate-900 sm:text-lg">
            Verbos en Inglés
          </h1>
          <p className="hidden truncate text-xs text-slate-500 sm:block">
            Aprende conjugando, una frase a la vez
          </p>
        </div>
      </div>

      <div className="lg:mx-auto lg:w-full lg:max-w-xl">
        <SearchBar value={verbos.search} onChange={verbos.setSearch} />
      </div>

      <div className="lg:justify-self-end">
        <CategoryFilter
          categories={verbos.categories}
          category={verbos.category}
          setCategory={verbos.setCategory}
          subcategory={verbos.subcategory}
          setSubcategory={verbos.setSubcategory}
          counts={verbos.counts}
        />
      </div>
    </Header>
  )
}

function VerbView({ retryKey }) {
  const verbos = useVerbosContext()

  useEffect(() => {
    if (verbos.error) console.error('[verbos] failed to load', verbos.error)
  }, [verbos.error])

  return (
    <div key={retryKey} className="contents">
      <div style={{ position: 'fixed', top: 80, right: 8, zIndex: 9999, background: 'red', color: 'white', padding: 8, fontSize: 11, fontFamily: 'monospace', maxWidth: 320 }}>
        loading={String(verbos.loading)}<br/>
        filtered={verbos.filtered?.length ?? 'undef'}<br/>
        current={verbos.currentVerb?.infinitivo?.ing ?? 'NULL'}<br/>
        idx={verbos.currentIndex}<br/>
        error={String(verbos.error)}
      </div>
      {verbos.loading || !verbos.currentVerb ? (
        <LoadingSkeleton />
      ) : (
        <VerbCard
          current={verbos.current}
          currentVerb={verbos.currentVerb}
          oraciones={verbos.oraciones}
          conjugationEntries={verbos.conjugationEntries}
          currentIndex={verbos.currentIndex}
          total={verbos.total}
          onPrev={verbos.prev}
          onNext={verbos.next}
          onShuffle={verbos.shuffle}
        />
      )}
    </div>
  )
}

export default function App() {
  const [retryKey, setRetryKey] = useState(0)
  const verbos = useVerbos()

  useEffect(() => {
    checkPexelsStatus()
  }, [])

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <VerbProvider value={verbos}>
        <ShellHeader />

        <main className="mx-auto max-w-4xl px-4 py-6 sm:px-6 sm:py-8">
          {verbos.error && !verbos.loading ? (
            <ErrorState
              error={verbos.error}
              onRetry={() => setRetryKey((k) => k + 1)}
            />
          ) : (
            <Routes>
              <Route path="/" element={<VerbView retryKey={retryKey} />} />
              <Route
                path="/:verbSelector"
                element={<VerbView retryKey={retryKey} />}
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          )}
        </main>
      </VerbProvider>
    </div>
  )
}