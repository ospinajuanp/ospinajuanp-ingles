'use client'

import { useVerbos } from '@/lib/hooks/useVerbos'
import { VerbProvider } from '@/components/providers/VerbContext'

export function VerbShell({ children }: { children: React.ReactNode }) {
  const verbos = useVerbos()
  return <VerbProvider value={verbos}>{children}</VerbProvider>
}
