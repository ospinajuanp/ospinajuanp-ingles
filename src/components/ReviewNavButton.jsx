import { Link } from 'react-router-dom'
import { useSRSContext } from '../contexts/SRSContext'

export default function ReviewNavButton() {
  const srs = useSRSContext()
  const due = srs?.dueCount ?? 0

  return (
    <Link
      to="/repaso"
      aria-label={
        due > 0
          ? `Repaso espaciado, ${due} ${due === 1 ? 'tarjeta pendiente' : 'tarjetas pendientes'}`
          : 'Repaso espaciado'
      }
      className="group relative inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-indigo-300 hover:text-indigo-600 hover:shadow-md active:scale-95"
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="size-4"
        aria-hidden="true"
      >
        <path d="M3 12a9 9 0 0 1 15.5-6.36L21 8" />
        <path d="M21 3v5h-5" />
        <path d="M21 12a9 9 0 0 1-15.5 6.36L3 16" />
        <path d="M3 21v-5h5" />
      </svg>
      <span>Repaso</span>
      {due > 0 ? (
        <span
          aria-hidden="true"
          className="inline-flex min-w-5 items-center justify-center rounded-full bg-indigo-600 px-1.5 py-0.5 text-[0.65rem] font-bold leading-none text-white"
        >
          {due > 99 ? '99+' : due}
        </span>
      ) : null}
    </Link>
  )
}
