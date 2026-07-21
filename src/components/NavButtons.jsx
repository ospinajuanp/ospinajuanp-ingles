import { ChevronLeft, ChevronRight, Dices } from 'lucide-react'

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
        className="inline-flex size-12 items-center justify-center rounded-full border border-base-300 bg-base-100 text-base-content/80 shadow-sm transition hover:border-primary/40 hover:bg-primary/10 hover:text-primary hover:-translate-y-0.5 active:scale-95 disabled:opacity-40 disabled:hover:translate-y-0 disabled:hover:bg-base-100 disabled:hover:text-base-content/80"
      >
        <ChevronLeft className="size-5" aria-hidden="true" />
      </button>

      <div
        className="flex select-none items-baseline gap-1 rounded-full border border-base-300 bg-base-100 px-4 py-2 shadow-sm sm:px-5"
        aria-live="polite"
      >
        <span className="text-xl font-bold tabular-nums text-base-content sm:text-2xl">
          {hasItems ? currentIndex + 1 : 0}
        </span>
        <span className="text-sm font-medium text-base-content/50">/</span>
        <span className="text-sm font-semibold tabular-nums text-base-content/70 sm:text-base">
          {total}
        </span>
      </div>

      <button
        type="button"
        onClick={onNext}
        disabled={!hasItems}
        aria-label="Siguiente verbo"
        className="btn btn-primary inline-flex size-12 min-h-0 items-center justify-center rounded-full p-0 shadow-sm transition hover:-translate-y-0.5 active:scale-95 disabled:opacity-40 disabled:hover:translate-y-0"
      >
        <ChevronRight className="size-5" aria-hidden="true" />
      </button>

      <button
        type="button"
        onClick={onShuffle}
        disabled={!hasItems}
        aria-label="Verbo aleatorio (sorpresa)"
        title="Verbo aleatorio"
        className="inline-flex size-12 items-center justify-center rounded-full border-2 border-primary/40 bg-base-100 text-primary shadow-sm transition hover:border-primary hover:bg-primary/10 hover:-translate-y-0.5 active:scale-95 disabled:opacity-40 disabled:hover:translate-y-0 disabled:hover:bg-base-100"
      >
        <Dices className="size-5" aria-hidden="true" />
      </button>
    </div>
  )
}
