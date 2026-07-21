// Theme switcher — DaisyUI v5 dropdown.
//
// Uses daisyUI's `.dropdown` primitive (focused, accessible by default)
// plus the `.btn .btn-circle .btn-ghost` modifiers so it inherits our
// theme tokens (`base-100`, `base-content`, `primary`) without any
// custom colors. Sits next to ReviewNavButton in the ShellHeader.

import { useTheme } from '../hooks/useTheme'

export default function ThemeSwitcher({ className = '' }) {
  const { theme, setTheme, themes } = useTheme()
  const currentLabel = themes.find((t) => t.id === theme)?.label ?? theme

  return (
    <div className={`dropdown dropdown-end ${className}`.trim()}>
      <div
        tabIndex={0}
        role="button"
        aria-label={`Cambiar tema (actual: ${currentLabel})`}
        className="inline-flex items-center justify-center rounded-full border border-slate-200 bg-white p-2.5 text-slate-700 shadow-sm transition hover:border-indigo-300 hover:text-indigo-600 hover:shadow-md active:scale-95"
        title={`Tema: ${currentLabel}`}
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
          <circle cx="12" cy="12" r="9" />
          <path d="M12 3v18" />
          <path d="M12 3a9 9 0 0 1 0 18" />
        </svg>
      </div>
      <ul
        tabIndex={0}
        className="menu dropdown-content z-50 mt-2 w-44 rounded-2xl border border-slate-200 bg-base-100 p-2 shadow-lg"
      >
        <li className="menu-title px-2 pt-1 text-[0.65rem] uppercase tracking-[0.18em] text-slate-400">
          Tema
        </li>
        {themes.map(({ id, label }) => (
          <li key={id}>
            <button
              type="button"
              onClick={() => setTheme(id)}
              aria-pressed={theme === id}
              className={`flex items-center justify-between gap-3 rounded-xl px-3 py-2 text-sm font-medium transition ${
                theme === id
                  ? 'bg-indigo-50 text-indigo-700'
                  : 'text-slate-700 hover:bg-base-200'
              }`}
            >
              <span>{label}</span>
              {theme === id ? (
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="size-4 shrink-0 text-indigo-600"
                  aria-hidden="true"
                >
                  <path d="M20 6 9 17l-5-5" />
                </svg>
              ) : null}
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
