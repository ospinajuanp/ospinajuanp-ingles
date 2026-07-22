import { redirect } from 'next/navigation'
import { z } from 'zod'

const slugSchema = z
  .string()
  .min(1)
  .max(80)
  .regex(/^[A-Za-z0-9 _\-]+$/, 'slug inválido')

interface PageProps {
  params: Promise<{ verbSelector: string }>
}

export default async function Page({ params }: PageProps) {
  const { verbSelector } = await params
  const parsed = slugSchema.safeParse(verbSelector)
  const target = parsed.success
    ? `/v1/verbs/${encodeURIComponent(parsed.data)}`
    : '/'
  redirect(target)
}
