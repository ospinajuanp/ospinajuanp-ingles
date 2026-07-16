const CATEGORIES = [
  { name: 'A', max: 10.0, prob: 0.5 },
  { name: 'B', max: 500.0, prob: 0.30 },
  { name: 'C', max: 1000.0, prob: 0.20 },
]

export function bucketOf(weight) {
  if (weight <= 10.0) return 'A'
  if (weight <= 500.0) return 'B'
  return 'C'
}

export function pickCategory(rng = Math.random) {
  const r = rng()
  let acc = 0
  for (const { name, prob } of CATEGORIES) {
    acc += prob
    if (r < acc) return name
  }
  return 'C'
}

function lookupWeight(verb, weightMap) {
  const ing = verb?.infinitivo?.ing?.toLowerCase()?.trim?.()
  if (!ing) return undefined
  return weightMap.get(ing)
}

export function pickWeightedIndex(verbs, weightMap, rng = Math.random) {
  const buckets = { A: [], B: [], C: [] }
  verbs.forEach((item, idx) => {
    const w = lookupWeight(item?.verb, weightMap)
    if (w === undefined) return
    buckets[bucketOf(w)].push(idx)
  })

  const wanted = pickCategory(rng)
  const fallbackOrder = [wanted, 'A', 'B', 'C'].filter(
    (c, i, a) => a.indexOf(c) === i,
  )
  for (const cat of fallbackOrder) {
    const bucket = buckets[cat]
    if (bucket.length > 0) {
      return bucket[Math.floor(rng() * bucket.length)]
    }
  }
  return 0
}