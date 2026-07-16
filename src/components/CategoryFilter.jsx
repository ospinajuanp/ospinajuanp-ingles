const PRETTY_NAMES = {
  generales: 'Generales',
  tecnologia: 'Tecnología',
  simples: 'Simples',
  irregulares: 'Irregulares',
  compuestos: 'Compuestos',
}

function pretty(key) {
  return PRETTY_NAMES[key] ?? key.charAt(0).toUpperCase() + key.slice(1)
}

function Pill({ active, onClick, children, ariaLabel }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      aria-label={ariaLabel}
      className={
        'whitespace-nowrap rounded-full px-3 py-1.5 text-xs font-semibold transition active:scale-95 sm:text-sm ' +
        (active
          ? 'bg-slate-900 text-white shadow-sm'
          : 'bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900')
      }
    >
      {children}
    </button>
  )
}

export default function CategoryFilter({
  categories,
  category,
  setCategory,
  subcategory,
  setSubcategory,
}) {
  if (!categories || categories.length === 0) return null

  const activeCat = categories.find((c) => c.category === category)
  const showSubs = activeCat?.subcategories?.length > 0

  return (
    <div className="space-y-2">
      <div className="flex flex-wrap items-center gap-2">
        <Pill active={category === 'all'} onClick={() => setCategory('all')}>
          Todas
        </Pill>
        {categories.map(({ category: cat }) => (
          <Pill
            key={cat}
            active={category === cat}
            onClick={() => {
              setCategory(cat)
              setSubcategory('all')
            }}
          >
            {pretty(cat)}
          </Pill>
        ))}
      </div>

      {showSubs && (
        <div className="flex flex-wrap items-center gap-1.5 pl-2 sm:gap-2 sm:pl-3">
          <span className="text-[0.65rem] font-bold uppercase tracking-[0.12em] text-slate-400">
            ·
          </span>
          <Pill active={subcategory === 'all'} onClick={() => setSubcategory('all')}>
            Todas
          </Pill>
          {activeCat.subcategories.map((sub) => (
            <Pill
              key={sub}
              active={subcategory === sub}
              onClick={() => setSubcategory(sub)}
            >
              {pretty(sub)}
            </Pill>
          ))}
        </div>
      )}
    </div>
  )
}
