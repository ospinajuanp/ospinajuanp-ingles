export function flattenVerbos(data) {
  const out = []
  walk(data, [], out)
  return out
}

function isVerbArray(node) {
  return (
    Array.isArray(node) &&
    node.length > 0 &&
    typeof node[0] === 'object' &&
    node[0] !== null &&
    'infinitivo' in node[0]
  )
}

function isFilled(verb) {
  return Boolean(verb?.infinitivo?.ing?.trim?.())
}

function walk(node, path, out) {
  if (Array.isArray(node)) {
    if (isVerbArray(node)) {
      const [category, subcategory = null] = path
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

export function collectCategories(flat) {
  const cats = new Map()
  for (const item of flat) {
    if (!cats.has(item.category)) cats.set(item.category, new Set())
    if (item.subcategory) cats.get(item.category).add(item.subcategory)
  }
  const result = []
  for (const [category, subs] of cats.entries()) {
    result.push({
      category,
      subcategories: [...subs].sort(),
    })
  }
  return result
}
