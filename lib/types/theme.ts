export type ThemeId = 'light' | 'dark' | 'dracula' | 'cupcake'

export interface ThemeDescriptor {
  id: ThemeId
  label: string
}

export type ThemeIconComponent = React.ComponentType<{
  className?: string
  'aria-hidden'?: boolean | 'true' | 'false'
}>

export interface ThemeApi {
  theme: ThemeId
  setTheme: (next: ThemeId) => void
  themes: ThemeDescriptor[]
  themeIcons: Record<ThemeId, ThemeIconComponent>
}
