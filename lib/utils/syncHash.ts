import type { SrsStore } from '@/lib/types/srs'
import type { ThemeId } from '@/lib/types/theme'

const FNV_OFFSET_BASIS = 0x811c9dc5
const FNV_PRIME = 0x01000193

function fnv1a(input: string): string {
  let hash = FNV_OFFSET_BASIS
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i)
    hash = Math.imul(hash, FNV_PRIME)
  }
  return (hash >>> 0).toString(16).padStart(8, '0')
}

function stableStringify(value: unknown): string {
  if (value === null || value === undefined) return 'null'
  if (typeof value === 'boolean') return value ? '1' : '0'
  if (typeof value === 'number') {
    return Number.isFinite(value) ? JSON.stringify(value) : 'null'
  }
  if (typeof value === 'string') return JSON.stringify(value)
  if (Array.isArray(value)) {
    let out = '['
    for (let i = 0; i < value.length; i++) {
      if (i > 0) out += ','
      out += stableStringify(value[i])
    }
    return out + ']'
  }
  if (typeof value === 'object') {
    const obj = value as Record<string, unknown>
    const keys = Object.keys(obj).sort()
    let out = '{'
    for (let i = 0; i < keys.length; i++) {
      const k = keys[i] as string
      if (i > 0) out += ','
      out += JSON.stringify(k) + ':' + stableStringify(obj[k])
    }
    return out + '}'
  }
  return 'null'
}

const THEME_LOCAL_STORAGE_KEY = 'ospinajuanp-ingles:theme'

export function readThemeFromLocalStorage(): string | null {
  if (typeof window === 'undefined') return null
  try {
    return window.localStorage.getItem(THEME_LOCAL_STORAGE_KEY)
  } catch {
    return null
  }
}

interface CardLike {
  id?: string
  type?: string
  verbKey?: string
  front?: unknown
  infinitivo?: unknown
  srs?: unknown
  createdAt?: number
  [key: string]: unknown
}

export function calculateCardHash(card: unknown): string {
  if (!card || typeof card !== 'object') return fnv1a('null')
  const cardObj = card as CardLike
  const { id: _ignored, ...rest } = cardObj
  void _ignored
  return fnv1a(stableStringify(rest))
}

export function calculateStoreHash(
  srsStore: SrsStore | null | undefined,
  theme: ThemeId | string | null | undefined,
): string {
  const cards = (srsStore && typeof srsStore === 'object' && srsStore.cards) || {}
  const order = (srsStore && Array.isArray(srsStore.order)) ? srsStore.order : []
  const cardIds = Object.keys(cards).sort()
  const cardsPart = fnv1a(
    cardIds
      .map((id) => `${id}:${calculateCardHash((cards as Record<string, unknown>)[id])}`)
      .join('|'),
  )
  const orderPart = fnv1a(order.join(','))
  const themePart = fnv1a(typeof theme === 'string' ? theme : '')
  return fnv1a(`s=${cardsPart}|o=${orderPart}|t=${themePart}`)
}
