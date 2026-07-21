import { useEffect, useState } from 'react'
import { Navigate, Route, Routes, useLocation, useParams, Link } from 'react-router-dom'
import { TriangleAlert } from 'lucide-react'
import SearchBar from './components/SearchBar'
import CategoryFilter from './components/CategoryFilter'
import VerbCard from './components/VerbCard'
import ReviewNavButton from './components/ReviewNavButton'
import ThemeSwitcher from './components/ThemeSwitcher'
import { useVerbos } from './hooks/useVerbos'
import { VerbProvider, useVerbosContext } from './contexts/VerbContext'
import { checkPexelsStatus } from './utils/pexels'
import SRSStudyPage from './pages/SRSStudyPage'
import HomePage from './pages/HomePage'

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
    <header className="sticky top-0 z-40 border-b border-base-300 bg-base-100/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-3 sm:px-6 sm:py-4 lg:grid lg:grid-cols-[1fr_2fr_1fr] lg:items-center lg:gap-8">
        {children}
      </div>
    </header>
  )
}

function LoadingSkeleton() {
  return (
    <div className="overflow-hidden rounded-2xl border border-base-300 bg-base-100 shadow-sm">
      <div className="h-44 w-full animate-pulse bg-base-300 sm:h-52 md:h-56" />
      <div className="space-y-8 p-5 sm:p-7 md:p-8">
        <div className="space-y-3 text-center">
          <div className="mx-auto h-12 w-40 animate-pulse rounded-lg bg-base-300" />
          <div className="mx-auto h-6 w-32 animate-pulse rounded-lg bg-base-300" />
        </div>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-16 animate-pulse rounded-xl bg-base-300" />
          ))}
        </div>
        <div className="space-y-2.5">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-24 animate-pulse rounded-xl bg-base-300" />
          ))}
        </div>
        <div className="flex justify-center">
          <div className="h-12 w-64 animate-pulse rounded-full bg-base-300" />
        </div>
      </div>
    </div>
  )
}

function ErrorState({ error, onRetry }) {
  return (
    <div className="rounded-2xl border border-error/30 bg-base-100 p-8 text-center shadow-sm">
      <div className="mx-auto mb-3 inline-flex size-12 items-center justify-center rounded-full bg-error/10 text-error">
        <TriangleAlert className="size-6" aria-hidden="true" />
      </div>
      <p className="text-lg font-semibold text-base-content">No pudimos cargar los verbos</p>
      <p className="mt-1 text-sm text-base-content/70">{error?.message ?? 'Error desconocido'}</p>
      <button
        type="button"
        onClick={onRetry}
        className="btn btn-primary mt-4 rounded-full px-5 normal-case"
      >
        Reintentar
      </button>
    </div>
  )
}

function ShellHeader() {
  const verbos = useVerbosContext()
  const { pathname } = useLocation()
  const isVerbRoute = pathname.startsWith('/v1/verbs')

  return (
    <Header>
      <Link
        to="/"
        aria-label="Ir a la página principal"
        className="group flex items-center gap-3 rounded-xl outline-none transition hover:opacity-80 focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-base-100"
      >
        <div className="shrink-0 overflow-hidden rounded-xl shadow-sm ring-1 ring-base-300/80" aria-hidden="true">
          <BrandIcon />
        </div>
        <div className="min-w-0">
          <h1 className="truncate text-base font-bold text-base-content transition-colors group-hover:text-primary sm:text-lg">
            Verbos en Inglés
          </h1>
          <p className="hidden truncate text-xs text-base-content/60 sm:block">
            Aprende conjugando, una frase a la vez
          </p>
        </div>
      </Link>

      <div className="lg:mx-auto lg:w-full lg:max-w-xl">
        {isVerbRoute ? (
          <SearchBar value={verbos.search} onChange={verbos.setSearch} />
        ) : null}
      </div>

      <div className="flex flex-wrap items-center justify-end gap-2 lg:justify-self-end">
        {isVerbRoute ? (
          <CategoryFilter
            categories={verbos.categories}
            category={verbos.category}
            setCategory={verbos.setCategory}
            subcategory={verbos.subcategory}
            setSubcategory={verbos.setSubcategory}
            counts={verbos.counts}
          />
        ) : null}
        <ReviewNavButton />
        <ThemeSwitcher />
      </div>
    </Header>
  )
}

function VerbView({ retryKey }) {
  const verbos = useVerbosContext()

  useEffect(() => {
    if (verbos?.error) console.error('[verbos] failed to load', verbos.error)
  }, [verbos?.error])

  return (
    <div key={retryKey} className="contents">
      {verbos?.loading || !verbos?.currentVerb ? (
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
          onEnriched={verbos.reportEnrichment}
        />
      )}
    </div>
  )
}

// Backward-compat redirects. The verb namespace moved from /<slug> to
// /v1/verbs/<slug> and SRS moved from /repaso to /v1/test. Old links
// keep working instead of 404'ing.
function LegacyVerbRedirect() {
  const { verbSelector } = useParams()
  const target = verbSelector
    ? `/v1/verbs/${encodeURIComponent(verbSelector)}`
    : '/'
  return <Navigate to={target} replace />
}

export default function App() {
  const [retryKey, setRetryKey] = useState(0)
  const verbos = useVerbos()

  useEffect(() => {
    checkPexelsStatus()
  }, [])

  return (
    <div className="min-h-screen bg-base-200 text-base-content">
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
              <Route path="/" element={<HomePage />} />
              <Route
                path="/v1/verbs/:verbSelector"
                element={<VerbView retryKey={retryKey} />}
              />
              <Route path="/v1/test" element={<SRSStudyPage />} />
              <Route path="/v1/test/" element={<SRSStudyPage />} />
              <Route path="/repaso" element={<Navigate to="/v1/test" replace />} />
              <Route path="/:verbSelector" element={<LegacyVerbRedirect />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          )}
        </main>
      </VerbProvider>
    </div>
  )
}
