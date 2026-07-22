import Link from 'next/link'

const GITHUB_URL = 'https://github.com/ospinajuanp/ingles'

export default function Footer() {
  return (
    <footer className="mt-12 border-t border-base-300 bg-base-100/60 py-6">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-3 px-4 text-center text-xs text-base-content/70 sm:flex-row sm:justify-between sm:text-left">
        <p>
          Hecho con <span aria-hidden="true">☕</span> y mucha práctica de
          conjugaciones.
        </p>
        <nav aria-label="Enlaces secundarios" className="flex flex-wrap items-center gap-3">
          <Link
            href="/"
            className="rounded px-2 py-1 outline-none transition hover:bg-base-200 hover:text-base-content focus-visible:ring-2 focus-visible:ring-primary"
          >
            Inicio
          </Link>
          <Link
            href="/v1/test"
            className="rounded px-2 py-1 outline-none transition hover:bg-base-200 hover:text-base-content focus-visible:ring-2 focus-visible:ring-primary"
          >
            Repaso
          </Link>
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded px-2 py-1 outline-none transition hover:bg-base-200 hover:text-base-content focus-visible:ring-2 focus-visible:ring-primary"
          >
            GitHub
          </a>
        </nav>
      </div>
    </footer>
  )
}

