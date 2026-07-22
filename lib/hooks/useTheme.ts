import { useCallback, useEffect, useState } from 'react'
import { Sun, Moon, Skull, Cake } from 'lucide-react'
import type { ThemeApi, ThemeId, ThemeIconComponent } from '@/lib/types/theme'

export const THEMES: ReadonlyArray<{ id: ThemeId; label: string }> = [
  { id: 'light', label: 'Claro' },
  { id: 'dark', label: 'Oscuro' },
  { id: 'dracula', label: 'Drácula' },
  { id: 'cupcake', label: 'Cupcake' },
]

export const THEME_ICONS: Record<ThemeId, ThemeIconComponent> = {
  light: Sun as ThemeIconComponent,
  dark: Moon as ThemeIconComponent,
  dracula: Skull as ThemeIconComponent,
  cupcake: Cake as ThemeIconComponent,
}

export const DEFAULT_THEME: ThemeId = 'light'
export const STORAGE_KEY = 'ospinajuanp-ingles:theme'

function prefersDark(): boolean {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

function detectInitialTheme(): ThemeId {
  if (typeof window === 'undefined') return DEFAULT_THEME
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (raw && isValidTheme(raw as ThemeId)) return raw as ThemeId
  } catch {
    // ignore — fall through to system preference
  }
  return prefersDark() ? 'dark' : DEFAULT_THEME
}

function readStoredTheme(): ThemeId {
  return detectInitialTheme()
}

function isValidTheme(id: ThemeId): boolean {
  return THEMES.some((t) => t.id === id)
}

export function useTheme(): ThemeApi {
  const [theme, setThemeState] = useState<ThemeId>(() => {
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

  const setTheme = useCallback((next: ThemeId): void => {
    if (!isValidTheme(next)) return
    setThemeState(next)
  }, [])

  return { theme, setTheme, themes: [...THEMES], themeIcons: THEME_ICONS }
}
