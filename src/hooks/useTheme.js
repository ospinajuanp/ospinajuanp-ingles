// Theme persistence + application hook.
//
// DaisyUI 5 reads the active theme from the `data-theme` attribute on
// <html>. We persist the user's choice under localStorage
// 'ospinajuanp-ingles:theme' so it survives reloads, and we mirror that
// key in a small inline <script> in index.html to avoid a flash of the
// default theme before React mounts.

import { useCallback, useEffect, useState } from 'react'
import { Sun, Moon, Skull, Cake } from 'lucide-react'

export const THEMES = [
  { id: 'light', label: 'Claro' },
  { id: 'dark', label: 'Oscuro' },
  { id: 'dracula', label: 'Drácula' },
  { id: 'cupcake', label: 'Cupcake' },
]

// Lucide icon per theme. The ThemeSwitcher trigger renders the icon for
// the currently active theme (changes on switch), and each dropdown row
// renders its own icon next to the label. Add an entry here when adding
// a new theme; the ThemeSwitcher falls back to `Sun` if no icon is set.
export const THEME_ICONS = {
  light: Sun,
  dark: Moon,
  dracula: Skull,
  cupcake: Cake,
}

export const DEFAULT_THEME = 'light'
export const STORAGE_KEY = 'ospinajuanp-ingles:theme'

function readStoredTheme() {
  if (typeof window === 'undefined') return DEFAULT_THEME
  try {
    return window.localStorage.getItem(STORAGE_KEY) ?? DEFAULT_THEME
  } catch {
    return DEFAULT_THEME
  }
}

function isValidTheme(id) {
  return THEMES.some((t) => t.id === id)
}

export function useTheme() {
  const [theme, setThemeState] = useState(() => {
    const stored = readStoredTheme()
    return isValidTheme(stored) ? stored : DEFAULT_THEME
  })

  useEffect(() => {
    if (typeof document === 'undefined') return
    document.documentElement.setAttribute('data-theme', theme)
    try {
      window.localStorage.setItem(STORAGE_KEY, theme)
    } catch {
      // ignore storage failures (private mode, quota, etc.)
    }
  }, [theme])

  const setTheme = useCallback((next) => {
    if (!isValidTheme(next)) return
    setThemeState(next)
  }, [])

  return { theme, setTheme, themes: THEMES, themeIcons: THEME_ICONS }
}
