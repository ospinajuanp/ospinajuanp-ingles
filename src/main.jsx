/* eslint-disable react-refresh/only-export-components */
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { SRSProvider } from './contexts/SRSContext'
import { useSRS } from './hooks/useSRS'

function Root() {
  // SRS state lives at the top of the tree so any hook called inside
  // <App> (notably useVerbos, which auto-registers the current verb)
  // can read it via useSRSContext without racing the provider mount.
  const srs = useSRS()
  return (
    <SRSProvider value={srs}>
      <App />
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
