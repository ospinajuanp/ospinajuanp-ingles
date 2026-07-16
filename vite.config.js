import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { copyFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'

const ROOT_JSON = resolve(process.cwd(), 'verbos_estructura.json')
const PUBLIC_JSON = resolve(process.cwd(), 'public/verbos_estructura.json')

function syncVerbosData() {
  if (!existsSync(ROOT_JSON)) return
  copyFileSync(ROOT_JSON, PUBLIC_JSON)
}

function syncDataPlugin() {
  return {
    name: 'sync-verbos-data',
    buildStart() {
      syncVerbosData()
    },
    configureServer(server) {
      syncVerbosData()
      server.watcher.add(ROOT_JSON)
      server.watcher.on('change', (file) => {
        if (file === ROOT_JSON) {
          syncVerbosData()
          server.ws.send({ type: 'full-reload' })
        }
      })
      server.watcher.on('add', (file) => {
        if (file === ROOT_JSON) {
          syncVerbosData()
          server.ws.send({ type: 'full-reload' })
        }
      })
    },
  }
}

export default defineConfig({
  plugins: [react(), tailwindcss(), syncDataPlugin()],
})