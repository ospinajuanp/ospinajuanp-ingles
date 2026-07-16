export default function ConjugationGrid({ entries }) {
  if (!entries || entries.length === 0) return null

  return (
    <div className="grid grid-cols-2 gap-2 sm:gap-3">
      {entries.map(({ time, value }) => (
        <div
          key={time}
          className="rounded-xl border border-slate-100 bg-slate-50/60 px-3 py-2.5"
        >
          <div className="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-slate-400">
            {time}
          </div>
          <div className="mt-0.5 text-base font-semibold text-slate-800 truncate">
            {value || '—'}
          </div>
        </div>
      ))}
    </div>
  )
}
