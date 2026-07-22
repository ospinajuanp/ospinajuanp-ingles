'use client'

import { SRSProvider } from '@/components/providers/SRSContext'
import { SyncProvider } from '@/components/providers/SyncContext'
import { VerbProvider } from '@/components/providers/VerbContext'
import { useSRS } from '@/lib/hooks/useSRS'
import { useTheme } from '@/lib/hooks/useTheme'
import { useSyncEngine } from '@/lib/hooks/useSyncEngine'
import { useVerbos } from '@/lib/hooks/useVerbos'
import Header from '@/components/Header'

function SyncProviderWithEngine({ children }: { children: React.ReactNode }) {
  const srs = useSRS()
  const themeApi = useTheme()
  const sync = useSyncEngine({ srs, themeApi })
  return (
    <SyncProvider value={sync}>
      <SRSProvider value={srs}>{children}</SRSProvider>
    </SyncProvider>
  )
}

function VerbProviderWithHook({ children }: { children: React.ReactNode }) {
  const verbos = useVerbos()
  return <VerbProvider value={verbos}>{children}</VerbProvider>
}

interface ProvidersProps {
  children: React.ReactNode
}

export function Providers({ children }: ProvidersProps) {
  return (
    <SyncProviderWithEngine>
      <VerbProviderWithHook>
        <Header />
        {children}
      </VerbProviderWithHook>
    </SyncProviderWithEngine>
  )
}
