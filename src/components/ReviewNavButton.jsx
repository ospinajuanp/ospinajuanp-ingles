import { Link } from 'react-router-dom'
import { RotateCw } from 'lucide-react'
import { useSRSContext } from '../contexts/SRSContext'

export default function ReviewNavButton() {
  const srs = useSRSContext()
  const due = srs?.dueCount ?? 0

  return (
    <Link
      to="/v1/test"
      aria-label={
        due > 0
          ? `Repaso espaciado, ${due} ${due === 1 ? 'tarjeta pendiente' : 'tarjetas pendientes'}`
          : 'Repaso espaciado'
      }
      className="group relative inline-flex items-center gap-2 rounded-full border border-base-300 bg-base-100 px-4 py-2.5 text-sm font-semibold text-base-content shadow-sm transition hover:border-primary/40 hover:text-primary hover:shadow-md active:scale-95"
    >
      <RotateCw className="size-4" aria-hidden="true" />
      <span>Repaso</span>
      {due > 0 ? (
        <span
          aria-hidden="true"
          className="inline-flex min-w-5 items-center justify-center rounded-full bg-primary px-1.5 py-0.5 text-[0.65rem] font-bold leading-none text-primary-content"
        >
          {due > 99 ? '99+' : due}
        </span>
      ) : null}
    </Link>
  )
}
