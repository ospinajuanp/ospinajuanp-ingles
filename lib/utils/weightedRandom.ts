import type { FlatVerb, Verb } from '@/lib/types/verbs'

const CATEGORIES: ReadonlyArray<{ name: WeightBucket; max: number; prob: number }> = [
  { name: 'A', max: 10.0, prob: 0.5 },
  { name: 'B', max: 500.0, prob: 0.3 },
  { name: 'C', max: 1000.0, prob: 0.2 },
]

export type WeightBucket = 'A' | 'B' | 'C'

export function bucketOf(weight: number): WeightBucket {
  if (weight <= 10.0) return 'A'
  if (weight <= 500.0) return 'B'
  return 'C'
}

export function pickCategory(rng: () => number = Math.random): WeightBucket {
  const r = rng()
  let acc = 0
  for (const { name, prob } of CATEGORIES) {
    acc += prob
    if (r < acc) return name
  }
  return 'C'
}

function lookupWeight(verb: Verb | undefined, weightMap: Map<string, number>): number | undefined {
  const ing = verb?.infinitivo?.ing?.toLowerCase()?.trim?.()
  if (!ing) return undefined
  return weightMap.get(ing)
}

export function pickWeightedIndex(
  verbs: readonly FlatVerb[],
  weightMap: Map<string, number>,
  rng: () => number = Math.random,
): number {
  const buckets: Record<WeightBucket, number[]> = { A: [], B: [], C: [] }
  verbs.forEach((item, idx) => {
    const w = lookupWeight(item?.verb, weightMap)
    if (w === undefined) return
    buckets[bucketOf(w)].push(idx)
  })

  const wanted = pickCategory(rng)
  const fallbackOrder = [wanted, 'A', 'B', 'C'].filter((c, i, a) => a.indexOf(c) === i) as WeightBucket[]
  for (const cat of fallbackOrder) {
    const bucket = buckets[cat]
    if (bucket.length > 0) {
      const idx = Math.floor(rng() * bucket.length)
      const value = bucket[idx]
      return value ?? 0
    }
  }
  return 0
}
