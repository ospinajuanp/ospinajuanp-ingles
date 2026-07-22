import type { Metadata } from 'next'
import { HomePage } from './_views/HomePage'

export const metadata: Metadata = {
  title: 'Verbos Inglés — Aprende conjugando',
  description:
    'Aprende verbos en inglés con oraciones contextualizadas, conjugaciones y repetición espaciada.',
  alternates: { canonical: '/' },
}

export default function Page() {
  return <HomePage />
}
