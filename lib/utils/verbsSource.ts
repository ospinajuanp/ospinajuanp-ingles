import { promises as fs } from 'node:fs'
import path from 'node:path'
import { flattenVerbos } from './flatten'
import type { FlatVerb } from '@/lib/types/verbs'

const VERBS_JSON_PATH = path.join(process.cwd(), 'public', 'verbos_estructura.json')

let cached: Promise<FlatVerb[]> | null = null

export async function readVerbsJson(): Promise<FlatVerb[]> {
  if (cached) return cached
  cached = (async () => {
    try {
      const raw = await fs.readFile(VERBS_JSON_PATH, 'utf-8')
      const parsed: unknown = JSON.parse(raw)
      return flattenVerbos(parsed)
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err)
      console.error('[verbsSource] failed to read verbos_estructura.json:', message)
      return []
    }
  })()
  return cached
}
