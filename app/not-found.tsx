import Link from 'next/link'

export default function NotFound() {
  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center gap-6 px-6 py-16 text-center">
      <span className="badge badge-warning badge-outline gap-2 px-3 py-3 text-[0.65rem] font-bold uppercase tracking-[0.18em]">
        404
      </span>
      <h1 className="text-3xl font-bold tracking-tight text-base-content sm:text-4xl">
        Página no encontrada
      </h1>
      <p className="text-base text-base-content/70">
        La ruta que buscás no existe o se movió. Volvé al inicio para seguir aprendiendo.
      </p>
      <Link
        href="/"
        className="btn btn-primary rounded-full px-5 normal-case shadow-sm"
      >
        Ir al inicio
      </Link>
    </main>
  )
}
