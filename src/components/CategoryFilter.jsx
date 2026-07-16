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

function Chip({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={
        'whitespace-nowrap rounded-full border px-4 py-2 text-sm font-semibold transition active:scale-95 ' +
        (active
          ? 'border-indigo-600 bg-indigo-600 text-white shadow-sm'
          : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300 hover:bg-slate-50 hover:text-slate-800')
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
    <div className="space-y-3">
      <div className="flex gap-2 overflow-x-auto pb-1 -mx-4 px-4 [&::-webkit-scrollbar]:hidden [scrollbar-width:none]">
        <Chip active={category === 'all'} onClick={() => setCategory('all')}>
          Todas
        </Chip>
        {categories.map(({ category: cat }) => (
          <Chip
            key={cat}
            active={category === cat}
            onClick={() => {
              setCategory(cat)
              setSubcategory('all')
            }}
          >
            {pretty(cat)}
          </Chip>
        ))}
      </div>

      {showSubs && (
        <div className="flex gap-2 overflow-x-auto pb-1 -mx-4 px-4 [&::-webkit-scrollbar]:hidden [scrollbar-width:none]">
          <Chip active={subcategory === 'all'} onClick={() => setSubcategory('all')}>
            Todas
          </Chip>
          {activeCat.subcategories.map((sub) => (
            <Chip
              key={sub}
              active={subcategory === sub}
              onClick={() => setSubcategory(sub)}
            >
              {pretty(sub)}
            </Chip>
          ))}
        </div>
      )}
    </div>
  )
}
