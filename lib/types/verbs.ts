export type TiempoConjugacion =
  | 'infinitivo'
  | 'pasadoSimple'
  | 'participio'
  | 'gerundio'
  | 'futuro'
  | 'condicional'

export type TiempoOracion = TiempoConjugacion

export interface ParBilingue {
  ing: string
  esp: string
}

export interface Conjugaciones {
  infinitivo?: ParBilingue
  pasadoSimple?: ParBilingue
  participio?: ParBilingue
  gerundio?: ParBilingue
  futuro?: ParBilingue
  condicional?: ParBilingue
}

export interface OracionPorTiempo {
  ing?: string
  esp?: string
}

export interface Verb {
  id: number
  infinitivo: ParBilingue
  conjugaciones?: Conjugaciones
  oraciones?: Partial<Record<TiempoConjugacion, OracionPorTiempo>>
  tips?: string
  imagen?: string
  [key: string]: unknown
}

export interface FlatVerb {
  verb: Verb
  category: string | null
  subcategory: string | null
}

export interface CategoryDescriptor {
  category: string
  subcategories: string[]
}

export interface CategoryCounts {
  total: number
  byCategory: Map<string, { total: number; sub: Map<string, number> }>
  bySubcategory: Map<string, number>
  subTotal: (cat: string) => number
  subForCategory: (cat: string) => number
}

export interface ConjugationGridEntry {
  time: string
  value: string | undefined
  valueEsp?: string | undefined
}

export interface OracionFillable {
  timeKey: TiempoConjugacion
  data: ParBilingue
}

export const TIEMPO_LABELS: Record<TiempoConjugacion, string> = {
  infinitivo: 'Infinitivo',
  pasadoSimple: 'Pasado',
  participio: 'Participio',
  gerundio: 'Gerundio',
  futuro: 'Futuro',
  condicional: 'Condicional',
}

export const TIEMPO_KEYS: readonly TiempoConjugacion[] = [
  'infinitivo',
  'pasadoSimple',
  'participio',
  'gerundio',
  'futuro',
  'condicional',
] as const
