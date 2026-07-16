export default function NavButtons({ onPrev, onNext, currentIndex, total, disabled }) {
  const hasItems = !disabled && total > 0

  return (
    <div className="pointer-events-none sticky bottom-4 z-30 mt-6 flex items-center justify-center gap-4 sm:static sm:mt-8">
      <button
        type="button"
        onClick={onPrev}
        disabled={!hasItems}
        aria-label="Verbo anterior"
        className="pointer-events-auto inline-flex size-14 items-center justify-center rounded-full bg-white text-indigo-600 shadow-lg ring-1 ring-slate-200 transition hover:bg-indigo-50 hover:-translate-y-0.5 active:scale-95 disabled:opacity-40 disabled:hover:translate-y-0 disabled:shadow-md"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="size-6"
          aria-hidden="true"
        >
          <path d="m15 18-6-6 6-6" />
        </svg>
      </button>

      <div
        className="pointer-events-auto flex min-w-28 select-none items-center justify-center gap-1.5 rounded-full bg-white px-5 py-3 text-sm font-semibold text-slate-600 shadow-md ring-1 ring-slate-200"
        aria-live="polite"
      >
        <span className="text-slate-800 tabular-nums">
          {hasItems ? currentIndex + 1 : 0}
        </span>
        <span className="text-slate-300">/</span>
        <span className="tabular-nums">{total}</span>
      </div>

      <button
        type="button"
        onClick={onNext}
        disabled={!hasItems}
        aria-label="Siguiente verbo"
        className="pointer-events-auto inline-flex size-14 items-center justify-center rounded-full bg-indigo-600 text-white shadow-lg shadow-indigo-600/30 transition hover:bg-indigo-500 hover:-translate-y-0.5 active:scale-95 disabled:opacity-40 disabled:hover:translate-y-0"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="size-6"
          aria-hidden="true"
        >
          <path d="m9 18 6-6-6-6" />
        </svg>
      </button>
    </div>
  )
}
