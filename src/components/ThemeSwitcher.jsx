// Theme switcher — DaisyUI v5 dropdown.
//
// Uses daisyUI's `.dropdown` primitive (focused, accessible by default)
// plus the `.btn .btn-circle .btn-ghost` modifiers so it inherits our
// theme tokens (`base-100`, `base-content`, `primary`) without any
// custom colors. Sits next to ReviewNavButton in the ShellHeader.
//
// Icons:
//   - Trigger renders the icon for the CURRENTLY ACTIVE theme (changes
//     on switch: Sun ↔ Moon ↔ Skull ↔ Cake). Fallback to Sun if the
//     theme id has no entry in THEME_ICONS.
//   - Each dropdown row renders its theme's icon next to the label, plus
//     a Check for the active row.

import { Check } from 'lucide-react'
import { useTheme } from '../hooks/useTheme'

export default function ThemeSwitcher({ className = '' }) {
  const { theme, setTheme, themes, themeIcons } = useTheme()
  const currentLabel = themes.find((t) => t.id === theme)?.label ?? theme
  const TriggerIcon = themeIcons[theme] ?? themeIcons.light

  return (
    <div className={`dropdown dropdown-end ${className}`.trim()}>
      <div
        tabIndex={0}
        role="button"
        aria-label={`Cambiar tema (actual: ${currentLabel})`}
        className="inline-flex items-center justify-center rounded-full border border-base-300 bg-base-100 p-2.5 text-base-content shadow-sm transition hover:border-primary/40 hover:text-primary hover:shadow-md active:scale-95"
        title={`Tema: ${currentLabel}`}
      >
        <TriggerIcon className="size-4" aria-hidden="true" />
      </div>
      <ul
        tabIndex={0}
        className="menu dropdown-content z-50 mt-2 w-44 rounded-2xl border border-base-300 bg-base-100 p-2 shadow-lg"
      >
        <li className="menu-title px-2 pt-1 text-[0.65rem] uppercase tracking-[0.18em] text-base-content/50">
          Tema
        </li>
        {themes.map(({ id, label }) => {
          const RowIcon = themeIcons[id] ?? themeIcons.light
          const isActive = theme === id
          return (
            <li key={id}>
              <button
                type="button"
                onClick={() => setTheme(id)}
                aria-pressed={isActive}
                className={`flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition ${
                  isActive
                    ? 'bg-primary/15 text-primary'
                    : 'text-base-content hover:bg-base-200'
                }`}
              >
                <RowIcon className="size-4 shrink-0" aria-hidden="true" />
                <span className="flex-1 truncate">{label}</span>
                {isActive ? (
                  <Check className="size-4 shrink-0" aria-hidden="true" />
                ) : null}
              </button>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
