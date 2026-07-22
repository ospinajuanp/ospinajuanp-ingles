'use client'

import { useEffect } from 'react'
import Link from 'next/link'

interface ErrorProps {
  error: Error & { digest?: string }
  reset: () => void
}

export default function GlobalError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('[app/error.tsx]', error)
  }, [error])

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center gap-6 px-6 py-16 text-center">
      <span className="badge badge-error badge-outline gap-2 px-3 py-3 text-[0.65rem] font-bold uppercase tracking-[0.18em]">
        Error
      </span>
      <h1 className="text-3xl font-bold tracking-tight text-base-content sm:text-4xl">
        Algo salió mal
      </h1>
      <p className="text-base text-base-content/70">
        {error?.message ?? 'Ocurrió un error inesperado al renderizar esta vista.'}
      </p>
      <div className="flex gap-3">
        <button
          type="button"
          onClick={reset}
          className="btn btn-primary rounded-full px-5 normal-case shadow-sm"
        >
          Reintentar
        </button>
        <Link
          href="/"
          className="btn btn-outline btn-primary rounded-full px-5 normal-case shadow-sm"
        >
          Ir al inicio
        </Link>
      </div>
    </main>
  )
}
