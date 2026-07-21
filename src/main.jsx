/* eslint-disable react-refresh/only-export-components */
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { SRSProvider } from './contexts/SRSContext'
import { SyncProvider } from './contexts/SyncContext'
import { useSRS } from './hooks/useSRS'
import { useTheme } from './hooks/useTheme'
import { useSyncEngine } from './hooks/useSyncEngine'

function Root() {
  // SRS + Theme are the two stateful inputs the sync engine needs to
  // observe. Both are loaded here (above <App>) so the engine can read
  // them on its very first effect run — no race against <App> mount.
  const srs = useSRS()
  const themeApi = useTheme()
  const sync = useSyncEngine({ srs, themeApi })

  return (
    <SRSProvider value={srs}>
      <SyncProvider value={sync}>
        <App />
      </SyncProvider>
    </SRSProvider>
  )
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Root />
    </BrowserRouter>
  </StrictMode>,
)