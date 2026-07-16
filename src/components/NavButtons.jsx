export default function NavButtons({
  onPrev,
  onNext,
  onShuffle,
  currentIndex,
  total,
  disabled,
}) {
  const hasItems = !disabled && total > 0

  return (
    <div className="mt-8 flex items-center justify-center gap-2 sm:gap-3">
      <button
        type="button"
        onClick={onPrev}
        disabled={!hasItems}
        aria-label="Verbo anterior"
        className="inline-flex size-12 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-600 shadow-sm transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-600 hover:-translate-y-0.5 active:scale-95 disabled:opacity-40 disabled:hover:translate-y-0 disabled:hover:bg-white disabled:hover:text-slate-600"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="size-5"
          aria-hidden="true"
        >
          <path d="m15 18-6-6 6-6" />
        </svg>
      </button>

      <div
        className="flex select-none items-baseline gap-1 rounded-full border border-slate-200 bg-white px-4 py-2 shadow-sm sm:px-5"
        aria-live="polite"
      >
        <span className="text-xl font-bold tabular-nums text-slate-900 sm:text-2xl">
          {hasItems ? currentIndex + 1 : 0}
        </span>
        <span className="text-sm font-medium text-slate-400">/</span>
        <span className="text-sm font-semibold tabular-nums text-slate-500 sm:text-base">
          {total}
        </span>
      </div>

      <button
        type="button"
        onClick={onNext}
        disabled={!hasItems}
        aria-label="Siguiente verbo"
        className="inline-flex size-12 items-center justify-center rounded-full bg-slate-900 text-white shadow-sm transition hover:bg-slate-800 hover:-translate-y-0.5 active:scale-95 disabled:opacity-40 disabled:hover:translate-y-0"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="size-5"
          aria-hidden="true"
        >
          <path d="m9 18 6-6-6-6" />
        </svg>
      </button>

      <button
        type="button"
        onClick={onShuffle}
        disabled={!hasItems}
        aria-label="Verbo aleatorio (sorpresa)"
        title="Verbo aleatorio"
        className="inline-flex size-12 items-center justify-center rounded-full border-2 border-indigo-200 bg-white text-indigo-600 shadow-sm transition hover:border-indigo-300 hover:bg-indigo-50 hover:-translate-y-0.5 active:scale-95 disabled:opacity-40 disabled:hover:translate-y-0 disabled:hover:bg-white"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="size-5"
          aria-hidden="true"
        >
          <rect x="3" y="3" width="18" height="18" rx="3" />
          <circle cx="8" cy="8" r="1.2" fill="currentColor" />
          <circle cx="16" cy="8" r="1.2" fill="currentColor" />
          <circle cx="12" cy="12" r="1.2" fill="currentColor" />
          <circle cx="8" cy="16" r="1.2" fill="currentColor" />
          <circle cx="16" cy="16" r="1.2" fill="currentColor" />
        </svg>
      </button>
    </div>
  )
}