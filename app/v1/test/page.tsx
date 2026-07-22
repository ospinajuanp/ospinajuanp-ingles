import type { Metadata } from 'next'
import { SRSStudyPage } from './_views/SRSStudyPage'

export const metadata: Metadata = {
  title: 'Repaso espaciado',
  description:
    'Sesión de tarjetas con SM-2 de 4 niveles: mezcla tus oraciones personalizadas con los verbos que ya visitaste.',
  alternates: { canonical: '/v1/test' },
}

export default function Page() {
  return <SRSStudyPage />
}
