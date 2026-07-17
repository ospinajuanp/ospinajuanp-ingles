import { defineConfig, loadEnv } from 'vite'
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

      // /api/verbs/sync → same handler used in production serverless deploys.
      // Lazy-imported so `mongodb` never reaches the client bundle.
      server.middlewares.use('/api/verbs/sync', async (req, res) => {
        try {
          const mod = await import('./api/verbs/sync.js')
          await mod.default(req, res)
        } catch (err) {
          console.error('[vite:middleware] /api/verbs/sync', err)
          if (!res.headersSent) {
            res.statusCode = 500
            res.setHeader('content-type', 'application/json')
            res.end(JSON.stringify({ ok: false, error: err.message }))
          }
        }
      })
    },
  }
}

export default defineConfig(({ mode }) => {
  // Load .env, .env.local, .env.[mode], .env.[mode].local. The empty
  // string as third arg tells Vite to expose ALL variables (not just
  // VITE_*-prefixed ones) so the dev middleware can read MONGODB_URI,
  // JWT_SECRET, etc. via process.env.X. We merge into process.env so
  // existing shell vars survive unless the .env file explicitly
  // overrides them.
  const env = loadEnv(mode, process.cwd(), '')
  Object.assign(process.env, env)

  return {
    plugins: [react(), tailwindcss(), syncDataPlugin()],
  }
})