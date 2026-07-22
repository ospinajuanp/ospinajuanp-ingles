import type { FlatVerb, Verb } from '@/lib/types/verbs'

export function flattenVerbos(data: unknown): FlatVerb[] {
  const out: FlatVerb[] = []
  walk(data, [], out)
  return out
}

function isVerbArray(node: unknown): node is Verb[] {
  return (
    Array.isArray(node) &&
    node.length > 0 &&
    typeof node[0] === 'object' &&
    node[0] !== null &&
    'infinitivo' in node[0]
  )
}

function isFilled(verb: Verb | undefined): boolean {
  return Boolean(verb?.infinitivo?.ing?.trim?.())
}

function walk(node: unknown, path: string[], out: FlatVerb[]): void {
  if (Array.isArray(node)) {
    if (isVerbArray(node)) {
      const category = path[0] ?? null
      const subcategory = path[1] ?? null
      for (const verb of node) {
        if (isFilled(verb)) {
          out.push({ verb, category, subcategory })
        }
      }
      return
    }
    return
  }

  if (node && typeof node === 'object') {
    for (const [key, value] of Object.entries(node)) {
      walk(value, [...path, key], out)
    }
  }
}

export interface CategoryDescriptor {
  category: string
  subcategories: string[]
}

export function collectCategories(flat: readonly FlatVerb[]): CategoryDescriptor[] {
  const cats = new Map<string, Set<string>>()
  for (const item of flat) {
    if (!item.category) continue
    if (!cats.has(item.category)) cats.set(item.category, new Set())
    if (item.subcategory) cats.get(item.category)?.add(item.subcategory)
  }
  const result: CategoryDescriptor[] = []
  for (const [category, subs] of cats.entries()) {
    result.push({
      category,
      subcategories: [...subs].sort(),
    })
  }
  return result
}

export function resolveVerb(
  selector: string | null | undefined,
  list: readonly FlatVerb[],
): FlatVerb | null {
  if (!selector || !list?.length) return null
  if (/^\d+$/.test(selector)) {
    const id = Number(selector)
    return list.find((i) => i.verb?.id === id) ?? null
  }
  const norm = selector.trim().toLowerCase()
  return (
    list.find(
      (i) => i.verb?.infinitivo?.ing?.trim?.().toLowerCase() === norm,
    ) ?? null
  )
}
