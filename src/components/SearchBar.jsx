import { Search, X } from 'lucide-react'

export default function SearchBar({ value, onChange }) {
  return (
    <div className="relative w-full">
      <label htmlFor="verb-search" className="sr-only">
        Buscar verbo en inglés o español
      </label>

      <Search
        className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 size-5 text-base-content/50"
        aria-hidden="true"
      />

      <input
        id="verb-search"
        type="search"
        inputMode="search"
        autoComplete="off"
        spellCheck={false}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Buscar verbo en inglés o español…"
        className="w-full rounded-full border border-base-300 bg-base-100 py-3.5 pl-12 pr-12 text-base text-base-content placeholder:text-base-content/50 shadow-sm outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/30"
      />

      {value && (
        <button
          type="button"
          onClick={() => onChange('')}
          aria-label="Limpiar búsqueda"
          className="absolute right-3 top-1/2 -translate-y-1/2 inline-flex size-8 items-center justify-center rounded-full text-base-content/50 transition hover:bg-base-200 hover:text-base-content active:scale-95"
        >
          <X className="size-4" aria-hidden="true" />
        </button>
      )}
    </div>
  )
}
