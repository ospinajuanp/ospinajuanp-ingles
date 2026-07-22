'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import SearchBar from './SearchBar'
import CategoryFilter from './CategoryFilter'
import ReviewNavButton from './ReviewNavButton'
import SyncButton from './SyncButton'
import SyncModal from './SyncModal'
import ThemeSwitcher from './ThemeSwitcher'
import { useVerbosContext } from './providers/VerbContext'
import { useUiStore } from '@/lib/stores/ui'

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

interface CrumbDescriptor {
  label: string
  href: string
}

function buildCrumbs(pathname: string): CrumbDescriptor[] {
  if (!pathname || pathname === '/') return []
  if (pathname === '/v1/test') {
    return [{ label: 'Repaso espaciado', href: '/v1/test' }]
  }
  const verbMatch = pathname.match(/^\/v1\/verbs\/([^/]+)\/?$/)
  if (verbMatch) {
    const slug = decodeURIComponent(verbMatch[1] ?? '')
    return [
      { label: 'Verbos', href: '/' },
      { label: slug, href: pathname },
    ]
  }
  return []
}

export default function Header() {
  const pathname = usePathname()
  const verbos = useVerbosContext()
  const syncOpen = useUiStore((s) => s.syncModalOpen)
  const openSyncModal = useUiStore((s) => s.openSyncModal)
  const closeSyncModal = useUiStore((s) => s.closeSyncModal)

  const isVerbRoute = pathname?.startsWith('/v1/verbs') ?? false
  const crumbs = buildCrumbs(pathname ?? '')

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-base-300 bg-base-100/85 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-3 sm:px-6 sm:py-4 lg:flex-row lg:flex-wrap lg:items-center lg:gap-x-6 lg:gap-y-3">
          <Link
            href="/"
            aria-label="Ir a la página principal"
            className="group flex items-center gap-3 rounded-xl outline-none transition hover:opacity-80 focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-base-100"
          >
            <div
              className="shrink-0 overflow-hidden rounded-xl shadow-sm ring-1 ring-base-300/80"
              aria-hidden="true"
            >
              <BrandIcon />
            </div>
            <div className="min-w-0">
              <span className="block truncate text-base font-bold text-base-content transition-colors group-hover:text-primary sm:text-lg">
                Verbos en Inglés
              </span>
              <p className="hidden truncate text-xs text-base-content/70 sm:block">
                Aprende conjugando, una frase a la vez
              </p>
            </div>
          </Link>

          {crumbs.length > 0 ? (
            <nav
              aria-label="Ruta de navegación"
              className="flex items-center gap-2 text-xs font-semibold text-base-content/70 lg:ml-auto lg:mr-0"
            >
              {crumbs.map((c, i) => {
                const isLast = i === crumbs.length - 1
                return (
                  <span key={c.href} className="flex items-center gap-2">
                    {i > 0 ? (
                      <span aria-hidden="true" className="text-base-content/40">
                        /
                      </span>
                    ) : null}
                    {isLast ? (
                      <span className="truncate text-base-content" title={c.label}>
                        {c.label}
                      </span>
                    ) : (
                      <Link
                        href={c.href}
                        className="rounded px-1.5 py-0.5 outline-none transition hover:bg-base-200 hover:text-base-content focus-visible:ring-2 focus-visible:ring-primary"
                      >
                        {c.label}
                      </Link>
                    )}
                  </span>
                )
              })}
            </nav>
          ) : null}

          <div className="lg:min-w-[16rem] lg:flex-1 lg:max-w-xl">
            {isVerbRoute && verbos ? (
              <SearchBar value={verbos.search} onChange={verbos.setSearch} />
            ) : null}
          </div>

          <div className="flex flex-wrap items-center justify-end gap-2">
            {isVerbRoute && verbos ? (
              <CategoryFilter
                categories={verbos.categories}
                category={verbos.category}
                setCategory={verbos.setCategory}
                subcategory={verbos.subcategory}
                setSubcategory={verbos.setSubcategory}
                counts={verbos.counts}
              />
            ) : null}
            {isVerbRoute ? <ReviewNavButton /> : null}
            <SyncButton onClick={openSyncModal} />
            <ThemeSwitcher />
          </div>
        </div>
      </header>

      <SyncModal open={syncOpen} onClose={closeSyncModal} />
    </>
  )
}
