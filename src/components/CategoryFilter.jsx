import { useEffect, useMemo, useRef, useState } from 'react'

const PRETTY_NAMES = {
  generales: 'Generales',
  tecnologia: 'Tecnología',
  simples: 'Simples',
  irregulares: 'Irregulares',
  compuestos: 'Compuestos',
}

function pretty(key) {
  return PRETTY_NAMES[key] ?? (key.charAt(0).toUpperCase() + key.slice(1))
}

function activeCategoryLabel(category, subcategory) {
  if (category === 'all') return 'Todas'
  const cat = pretty(category)
  if (subcategory !== 'all') return `${cat} · ${pretty(subcategory)}`
  return cat
}

export default function CategoryFilter({
  categories,
  category,
  setCategory,
  subcategory,
  setSubcategory,
  counts,
}) {
  const [open, setOpen] = useState(false)
  const containerRef = useRef(null)

  useEffect(() => {
    if (!open) return
    function onPointer(e) {
      if (!containerRef.current?.contains(e.target)) setOpen(false)
    }
    function onKey(e) {
      if (e.key === 'Escape') setOpen(false)
    }
    function onScroll() {
      setOpen(false)
    }
    document.addEventListener('mousedown', onPointer)
    document.addEventListener('keydown', onKey)
    window.addEventListener('scroll', onScroll, { passive: true, capture: true })
    return () => {
      document.removeEventListener('mousedown', onPointer)
      document.removeEventListener('keydown', onKey)
      window.removeEventListener('scroll', onScroll, { capture: true })
    }
  }, [open])

  const activeCat = categories.find((c) => c.category === category)
  const showSubs = activeCat?.subcategories?.length > 0

  const triggerCount = useMemo(() => {
    if (category === 'all') return counts?.total ?? null
    return counts?.subForCategory?.(category) ?? null
  }, [category, counts])

  const hasActiveFilter = category !== 'all' || subcategory !== 'all'

  function selectCategory(next) {
    setCategory(next)
    if (next !== category) setSubcategory('all')
  }

  function reset() {
    setCategory('all')
    setSubcategory('all')
    setOpen(false)
  }

  return (
    <div ref={containerRef} className="relative block w-full text-left sm:inline-block sm:w-auto">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-haspopup="dialog"
        aria-expanded={open}
        className={
          'inline-flex items-center gap-2 rounded-full border px-3.5 py-1.5 text-sm font-semibold shadow-sm transition active:scale-[0.98] ' +
          (hasActiveFilter
            ? 'border-primary/40 bg-primary/10 text-primary hover:bg-primary/15'
            : 'border-base-300 bg-base-100 text-base-content hover:bg-base-200')
        }
      >
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
          <path d="M3 6h18M6 12h12M10 18h4" />
        </svg>
        <span className="max-w-[10rem] truncate">
          {activeCategoryLabel(category, subcategory)}
        </span>
        {triggerCount !== null ? (
          <span
            className={
              'rounded-full px-1.5 text-[0.65rem] font-bold tabular-nums ' +
              (hasActiveFilter
                ? 'bg-primary text-primary-content'
                : 'bg-base-200 text-base-content/60')
            }
          >
            {triggerCount}
          </span>
        ) : null}
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className={'size-3.5 transition-transform ' + (open ? 'rotate-180' : '')}
          aria-hidden="true"
        >
          <path d="m6 9 6 6 6-6" />
        </svg>
      </button>

      {open ? (
        <div
          role="dialog"
          aria-label="Filtros"
          className="absolute right-0 z-40 mt-2 w-72 max-w-[calc(100vw-1rem)] origin-top-right overflow-hidden rounded-xl border border-base-300 bg-base-100 shadow-xl ring-1 ring-black/5"
        >
          <div className="border-b border-base-300 p-3">
            <div className="mb-2 flex items-center justify-between">
              <span className="text-[0.65rem] font-bold uppercase tracking-[0.14em] text-base-content/50">
                Categoría
              </span>
              <span className="text-[0.65rem] font-semibold text-base-content/50 tabular-nums">
                {counts?.total ?? 0}
              </span>
            </div>
            <div className="space-y-1">
              <Row
                active={category === 'all'}
                label="Todas"
                count={counts?.total}
                onClick={() => selectCategory('all')}
              />
              {categories.map(({ category: cat }) => (
                <Row
                  key={cat}
                  active={category === cat}
                  label={pretty(cat)}
                  count={counts?.byCategory?.get(cat)?.total}
                  onClick={() => selectCategory(cat)}
                />
              ))}
            </div>
          </div>

          <div className="p-3">
            <div className="mb-2 flex items-center justify-between">
              <span className="text-[0.65rem] font-bold uppercase tracking-[0.14em] text-base-content/50">
                Subcategoría
              </span>
              {showSubs ? (
                <span className="text-[0.65rem] font-semibold text-base-content/50 tabular-nums">
                  {counts?.subForCategory?.(category) ?? 0}
                </span>
              ) : null}
            </div>
            {showSubs ? (
              <div className="space-y-1">
                <Row
                  active={subcategory === 'all'}
                  label="Todas"
                  count={counts?.subForCategory?.(category)}
                  onClick={() => setSubcategory('all')}
                  disabled={category === 'all'}
                />
                {activeCat.subcategories.map((sub) => (
                  <Row
                    key={sub}
                    active={subcategory === sub}
                    label={pretty(sub)}
                    count={counts?.bySubcategory?.get(`${category}::${sub}`)}
                    onClick={() => setSubcategory(sub)}
                  />
                ))}
              </div>
            ) : (
              <p className="rounded-lg bg-base-200 px-3 py-2 text-center text-xs text-base-content/50">
                Selecciona una categoría
              </p>
            )}
          </div>

          {hasActiveFilter ? (
            <div className="border-t border-base-300 p-2">
              <button
                type="button"
                onClick={reset}
                className="inline-flex w-full items-center justify-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold text-base-content/70 transition hover:bg-base-200 hover:text-base-content"
              >
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
                  <path d="M3 12a9 9 0 1 0 9-9" />
                  <path d="M3 4v5h5" />
                </svg>
                Limpiar filtros
              </button>
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  )
}

function Row({ active, label, count, onClick, disabled = false }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={
        'flex w-full items-center justify-between gap-2 rounded-lg px-2.5 py-1.5 text-sm transition disabled:opacity-50 ' +
        (active
          ? 'bg-primary font-semibold text-primary-content shadow-sm'
          : 'text-base-content hover:bg-base-200')
      }
    >
      <span className="flex items-center gap-2">
        <span
          className={
            'inline-flex size-4 items-center justify-center rounded-full border ' +
            (active
              ? 'border-primary-content/40 bg-primary-content/20'
              : 'border-base-300 bg-base-100')
          }
          aria-hidden="true"
        >
          {active ? (
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="3"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="size-2.5"
            >
              <path d="m5 12 5 5 9-11" />
            </svg>
          ) : null}
        </span>
        <span className="truncate">{label}</span>
      </span>
      {count !== undefined && count !== null ? (
        <span
          className={
            'tabular-nums text-xs ' + (active ? 'opacity-90' : 'text-base-content/50')
          }
        >
          {count}
        </span>
      ) : null}
    </button>
  )
}
