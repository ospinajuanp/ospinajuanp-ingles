import { selectTip } from '../utils/tips'

export default function ConjugationGrid({ entries, seed = 0 }) {
  const tip = selectTip(seed)
  const allCells = [
    ...(entries ?? []).map((e) => ({ kind: 'entry', ...e })),
    { kind: 'tip', time: 'Tip', value: tip.text, tipTitle: tip.title },
  ]

  return (
    <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3 sm:gap-3">
      {allCells.map((cell, i) => {
        if (cell.kind === 'tip') {
          return (
            <div
              key={`tip-${i}`}
              className="relative overflow-hidden rounded-xl border border-indigo-100 bg-gradient-to-br from-indigo-50 via-white to-amber-50 px-3 py-2.5 sm:px-4 sm:py-3"
            >
              <div className="flex items-center gap-1.5 text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-indigo-500">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="size-3.5"
                  aria-hidden="true"
                >
                  <path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.74V17a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-2.26A7 7 0 0 0 12 2z" />
                </svg>
                <span>{cell.tipTitle}</span>
              </div>
              <p className="mt-1 text-sm font-medium leading-snug text-slate-700">
                {cell.value}
              </p>
            </div>
          )
        }

        return (
          <div
            key={`${cell.time}-${i}`}
            className="rounded-xl border border-slate-100 bg-white px-3 py-2.5 sm:px-4 sm:py-3"
          >
            <div className="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-slate-400">
              {cell.time}
            </div>
            <div className="mt-0.5 text-base font-semibold text-slate-800 truncate sm:text-lg">
              {cell.value || '—'}
            </div>
          </div>
        )
      })}
    </div>
  )
}
