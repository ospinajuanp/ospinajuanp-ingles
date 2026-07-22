import type { Metadata } from 'next'
import { z } from 'zod'
import { VerbViewShell } from './_views/VerbViewShell'
import { resolveVerb } from '@/lib/utils/flatten'
import { readVerbsJson } from '@/lib/utils/verbsSource'

const verbSelectorSchema = z.object({
  verbSelector: z
    .string()
    .min(1)
    .max(80)
    .regex(/^[A-Za-z0-9 _\-]+$/, 'slug inválido'),
})

interface PageProps {
  params: Promise<{ verbSelector: string }>
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { verbSelector } = await params
  const parsed = verbSelectorSchema.safeParse({ verbSelector })
  if (!parsed.success) {
    return { title: 'Verbo no encontrado' }
  }
  const flat = await readVerbsJson()
  const resolved = resolveVerb(parsed.data.verbSelector, flat)
  if (!resolved) {
    return { title: 'Verbo no encontrado' }
  }
  const ing = resolved.verb.infinitivo?.ing ?? parsed.data.verbSelector
  return {
    title: `${ing} — conjugaciones en inglés`,
    description: `Conjugaciones y oraciones de ejemplo para "${ing}".`,
    alternates: { canonical: `/v1/verbs/${parsed.data.verbSelector}` },
  }
}

export default async function Page({ params }: PageProps) {
  const { verbSelector } = await params
  const parsed = verbSelectorSchema.safeParse({ verbSelector })
  if (!parsed.success) {
    return (
      <main className="mx-auto max-w-4xl px-4 py-12 text-center">
        <h1 className="text-3xl font-bold">Verbo inválido</h1>
        <p className="mt-2 text-base-content/70">
          El identificador del verbo no tiene un formato válido.
        </p>
      </main>
    )
  }
  const flat = await readVerbsJson()
  const resolved = resolveVerb(parsed.data.verbSelector, flat)
  if (!resolved) {
    return (
      <main className="mx-auto max-w-4xl px-4 py-12 text-center">
        <h1 className="text-3xl font-bold">Verbo no encontrado</h1>
        <p className="mt-2 text-base-content/70">
          No encontramos un verbo con el identificador "{parsed.data.verbSelector}".
        </p>
      </main>
    )
  }
  return <VerbViewShell initialVerb={resolved} />
}
