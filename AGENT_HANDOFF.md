# Agent Handoff — ospinajuanp-ingles

## Project
React 19 + Vite 8 + Tailwind v4 SPA for learning English verbs in Spanish. On-demand Pexels hero images, Free Dictionary audio (with `SpeechSynthesis` fallback), weighted-random initial verb, progressive-disclosure UX (blur-reveal of Spanish), URL-driven dual routing, MongoDB Atlas lazy+bulk sync.

## Repo
- GitHub: `ospinajuanp/ospinajuanp-ingles`, branch `main`
- Working tree: clean, last commit `593b128 feat(bulk): 1000-verb bulk migration to MongoDB + lazy enrichment`

## Key conventions
- Dataset: `verbos_estructura.json` at repo root (gitignored), copied to `public/` by a Vite plugin (`syncDataPlugin` in `vite.config.js`) on dev start, build start, and on every change. The plugin triggers `full-reload` via WebSocket. **HMR auto-restarts dev server on `api/verbs/sync.js` changes — keep in mind during bulk runs.**
- Routing: **URL is the single source of truth**. React Router v7.14.0. `/` redirects (replace) to `/<slug>` via weighted-random; `/:verbSelector` accepts digits (`verb.id`) or string (`infinitivo.ing` case-insensitive trimmed); unknown selector → `<Navigate to="/" replace />`.
- `useParams()` only works inside `<Route>`. `useVerbos` lives in `<App>` ABOVE `<Routes>`, so reads `useLocation().pathname` and parses with regex `/^\/(.+)$/` + `decodeURIComponent` as `effectiveSelector`. Falls back to `useParams()` value when present.
- Weighted random: buckets A (≤10, 50%), B (10.1–500, 30%), C (500.1–1000, 20%). Lives in `src/utils/weightedRandom.js`.
- Env: `.env` / `.env.*` are gitignored, `.env.example` is force-added via `!.env.example` negation. Two Pexels keys (`VITE_PEXELS_API_KEY` + optional `VITE_PEXELS_API_KEY_2`, automatic fallback on 401/403/429/5xx/network) + `MONGODB_URI` (server-side only).
- ESLint 9 flat config: forbids `setState` in `useEffect` (`react-hooks/set-state-in-effect`). Use derived state pattern with `if (x !== y) setX(y)` during render. New Node-globals block for `scripts/**/*.mjs` and `api/**/*.js` with `no-undef: error`.
- Audio uses imperative `new Audio()` (NOT JSX `<audio>`). `SpeechSynthesis` fallback when API has no phonetics (`draw`, `set`, `run`). Params: `lang: 'en-US', rate: 0.9`.
- Image cache: `Map<word, photo[]>` in `src/utils/imageCache.js`, hydrated from and persisted to `localStorage` under key `verbos:pexelsCache` (~100 KB for ~700 verbs). One JSON blob; refresh button cycles Pexels pages.
- Maximize button (top-left, `data-overlay-control="expand"`, persists to `localStorage['verbos:heroExpanded']`): collapsed = `object-cover h-44 sm:h-52 md:h-56`; expanded = `object-contain h-[min(70vh,560px)] min-h-[280px] bg-slate-900/95`.
- Tips rewritten with Spanish glossing: each English example has Spanish translation + per-word Spanish equivalents. `whitespace-pre-line` rendered in `<p>`.
- Image overlay z-index: blur `z-0`, audio wrapper `z-10`, refresh + ImageCredit + maximize `z-30`.
- Header: sticky. Mobile `flex-col gap-3`; desktop `lg:grid lg:grid-cols-[1fr_2fr_1fr]`.

## Important gotchas
- **Atlas UI defaults to 25 docs per page** — confusing on first check. Use `countDocuments()` or scroll/paginate to confirm full migration.
- **NO `infinitivo.ing` unique index** — dataset has ~95 verbs with duplicate `ing` (`rewrite`, `analyze`, `check`…). Only `id` is uniquely indexed.
- `migrado_desde` is server-managed via `$setOnInsert` only. Bulk passes `'SPA_Bulk_Migration'`, lazy omits it and defaults to `'SPA_Lazy_Migration'`. **Stripped from `$set`** so updates never overwrite the marker.
- `src/hooks/useVerbos.js` weighted-pick guards against the old `isFirstEffectRun` bug using a `cameFromEmpty` flag (check it when touching shuffle/init logic).
- `AudioButton.jsx` is a `forwardRef` so `VerbImageOverlay` can trigger play on image click. Has `isMountedRef` guarding `setState` after fetch await.
- `SpeechSynthesis` cleanup pauses + cancels speech on unmount. Params: `lang: 'en-US'`, `rate: 0.9`.
- `CategoryFilter.jsx` is a dropdown with click-outside + Escape + scroll-close, `w-72 max-w-[calc(100vw-1rem)]` for mobile, container `block w-full sm:inline-block sm:w-auto`.
- `src/utils/tips.js` has 53 short practical English tips with Spanish glossing; `selectTip(seed)` cycles deterministically.
- `src/hooks/useVerbos.js` reads `verbos_estructura.json` via `fetch('/verbos_estructura.json')` (the public copy). **Bulk migration writes to MongoDB but does NOT yet replace the JSON read** — both paths coexist.

## Relevant files
- `src/App.jsx`: `useVerbos()` once at top level (above `<Routes>`), wraps in `VerbProvider`, renders ShellHeader + `<Routes>` (`/`, `/:verbSelector`, `*` catch-all `<Navigate to="/" replace />`).
- `src/main.jsx`: wraps `<App />` in `<BrowserRouter>` + `<StrictMode>`.
- `src/contexts/VerbContext.jsx`: `VerbProvider({value, children})` + `useVerbosContext()` hook. File-level `/* eslint-disable react-hooks/refs */` for the `syncedThisSession` ref. Co-export via `/* eslint-disable react-refresh/only-export-components */`.
- `src/hooks/useVerbos.js`: URL-driven via `useLocation` regex fallback; exposes `current`, `currentVerb`, `currentIndex`, `oraciones`, `conjugationEntries`, `prev/next/shuffle/goTo`, `reportEnrichment`. Two useEffects: root-route redirect or 404 fallback (combined with `initialPickDone` ref), and filter-excludes-verb redirect. `useMemo` for filtered, current, currentIndex.
- `src/utils/mongoSync.js`: fire-and-forget `fetch('/api/verbs/sync', {method:'POST', keepalive:true})` with silent `console.warn`.
- `src/utils/flatten.js`: `flattenVerbos(data)` walks `{generales: {simples, irregulares, …}, tecnologia: {…}}` → flat array of `{verb, category, subcategory}`. `collectCategories(flat)` returns per-category subcategories.
- `src/utils/pexels.js`: dual-key client (`fetchPexelsPhoto`, `checkPexelsStatus`, `hasPexelsKey`, module-level `currentKeyIndex` rotation, `tryFetch` helper, retry once on second key).
- `src/components/VerbCard.jsx`: accepts `onEnriched` callback; tracks `imageInfo`/`audioInfo` state; resets on verb change via `if (trackedVerbKey !== verbKey) { … }`; fires `onEnriched` once per verb via `enrichedForVerb` ref (survives StrictMode double-mount).
- `src/components/VerbImage.jsx`: accepts `onReady({imagen_url, image_source})`. Fires via `useEffect` when `src` is set.
- `src/components/AudioButton.jsx`: `forwardRef`, accepts `onResolved({audio_url, audio_source})`. Fires on mount (cache check) and after every resolution path (cached/TTS/fetched/unavailable).
- `src/components/CategoryFilter.jsx`: dropdown with per-category counts, "Limpiar filtros" reset.
- `src/components/SearchBar.jsx`, `src/components/ConjugationGrid.jsx`, `src/components/SentencePill.jsx`, `src/components/NavButtons.jsx`, `src/components/HeroIllustration.jsx`, `src/components/ImageCredit.jsx`: stable, prop-driven.
- `vite.config.js`: `defineConfig(({mode}) => { const env = loadEnv(mode, process.cwd(), ''); Object.assign(process.env, env); return { plugins: [...] } })`. Middleware at `/api/verbs/sync` lazy-imports handler. `syncDataPlugin` watches root JSON.
- `api/verbs/sync.js`: server-side handler. Validates payload, cached `MongoClient`, idempotent `ensureIndexes` (`id_unique` + `last_seen_desc`), atomic `findOneAndUpdate`. Reads `migrado_desde` from payload (default `'SPA_Lazy_Migration'`), strips from `$set`, puts in `$setOnInsert`.
- `scripts/bulk-direct.mjs`: fast bulk via `MongoClient.bulkWrite()`, ~1s for 1000 verbs. Strip `id` from `$set` to avoid `$set`+`$setOnInsert` conflict. Env: `MONGODB_URI` required.
- `scripts/bulk-migrate.mjs`: bulk via HTTP POSTs, 100ms throttle (~10 req/sec), ~3-5 min for 1000 verbs. Endpoint from `MIGRATE_ENDPOINT` env (default `http://localhost:5173/api/verbs/sync`).
- `eslint.config.js`: default browser config + new block for `scripts/**/*.mjs` and `api/**/*.js` with `globals: ...globals.node`, `no-undef: error`.
- `package.json`: scripts `dev`, `build`, `preview`, `lint`, `bulk:migrate`, `bulk:direct`. Deps: react/react-dom 19.2.7, react-router-dom 7.14.0, mongodb 7.5.0.
- `.env.example`: documents `VITE_PEXELS_API_KEY`, `VITE_PEXELS_API_KEY_2`, `MONGODB_URI=`.
- `.env` (gitignored): both Pexels keys + `MONGODB_URI` with quoted connection string `mongodb+srv://…`.
- `README.md`: setup, architecture, data model, weighted random notes, Pexels rotation.
- `verbos_estructura.json` (root, gitignored): 1000 verbs flattened to 905 unique `infinitivo.ing` (95 duplicates); all 1000 unique `id`.

## Build
`pnpm build` → `dist/` produces ~316 KB JS raw / ~100 KB gzipped (after routing + mongo client wrapper). MongoDB driver NOT in client bundle.

## What works
- **1000/1000 verbs migrated to MongoDB Atlas** in `ingles-db.verbos` via `pnpm bulk:direct`. All `migrado_desde='SPA_Bulk_Migration'`, `audio_source='pending'`, `image_source='picsum'`, `oraciones` populated.
- Idempotency verified: re-running `pnpm bulk:direct` returns `matched: 1000, modified: 1000, upserted: 0, inserted: 0, errors: 0`.
- Lazy sync path ready: VerbCard calls `reportEnrichment` once per verb when both image and audio resolve; existing docs get refreshed URLs, new ones get `migrado_desde='SPA_Lazy_Migration'`.
- Routing fully working: `/`, `/0`, `/accept`, `/feel`, `/tell`, `/know` all render VerbCard. `/xyz-falso` redirects to `/`.
- 190+ verbs have hero image (Pexels or Picsum), audio (API + TTS fallback), 6 conjugations with eye/eye-off reveal, 6 sentences with blur-reveal.
- Header sticky + responsive, category filter, shuffle, keyboard nav, weighted-random initial pick, tips banner, footer.
- README + .env.example + all wiring in place.

## Atlas indices (current)
- `_id_` (default)
- `id_unique` on `{id: 1}` — unique
- `last_seen_desc` on `{ultima_vez_visto: -1}` — for "recently viewed" queries

NO `infinitivo.ing` index. Dataset has ~95 duplicate ing values (e.g. `rewrite`, `analyze`, `check`) which would break `ing_unique` with E11000.

## MongoDB query recipes
```js
// Total
db.verbos.countDocuments({})                                  // 1000

// By migration source
db.verbos.countDocuments({ migrado_desde: 'SPA_Bulk_Migration' })   // 1000
db.verbos.countDocuments({ migrado_desde: 'SPA_Lazy_Migration' })   // 0 (no lazy visits yet)

// Multimedia enrichment state
db.verbos.countDocuments({ audio_source: 'pending' })         // 1000 (need lazy visits)
db.verbos.countDocuments({ audio_source: 'dictionaryapi.dev' }) // grows as users visit
db.verbos.countDocuments({ audio_source: 'tts' })              // TTS fallback
db.verbos.countDocuments({ audio_source: 'none' })             // no phonetics available
db.verbos.countDocuments({ image_source: 'picsum' })           // bulk-seeded
db.verbos.countDocuments({ image_source: 'pexels' })           // enriched by lazy sync

// Most consulted
db.verbos.find({}, {id:1, "infinitivo.ing":1, contador_consultas:1})
  .sort({contador_consultas: -1}).limit(10)

// Recently viewed
db.verbos.find({}, {id:1, "infinitivo.ing":1, ultima_vez_visto:1})
  .sort({ultima_vez_visto: -1}).limit(10)

// Find by id (NOT by infinitivo.ing — duplicates exist)
db.verbos.findOne({ id: 0 })                                  // → accept
db.verbos.findOne({ id: 999 })
```

## How to run
```bash
pnpm install
cp .env.example .env       # paste 1 or 2 Pexels keys + MONGODB_URI
pnpm dev
# or
pnpm build && pnpm preview

# One-shot: migrate all 1000 verbs from verbos_estructura.json
# into MongoDB Atlas (deterministic picsum URLs, audio pending).
# Idempotent: safe to re-run.
pnpm bulk:direct          # ~1s, recommended
pnpm bulk:migrate         # ~3-5min via HTTP, smoke-test only
```

## MongoDB lazy + bulk migration

The collection `ingles-db.verbos` is populated by two paths:

1. **Bulk** (one-shot, manual): two scripts available
   - `pnpm bulk:direct` — **recommended**. Bypasses HTTP, uses
     `MongoClient.bulkWrite()` directly. ~1s for 1000 verbs.
     Requires `MONGODB_URI` in `.env` (loadEnv picks it up).
   - `pnpm bulk:migrate` — POSTs to `/api/verbs/sync`. Slower
     (~3-5 min for 1000 verbs at 10 req/sec) but exercises the
     production endpoint. Useful as a smoke test.
   Both read `verbos_estructura.json` and upsert every verb with
   a deterministic picsum URL, `audio_source: 'pending'`, and
   `migrado_desde: 'SPA_Bulk_Migration'`.

2. **Lazy** (organic, on every verb visit): the SPA fires the
   same endpoint whenever VerbCard resolves both the Pexels image
   and the audio source. New docs get `migrado_desde:
   'SPA_Lazy_Migration'` (default) and `audio_source` set to
   whatever the audio resolver found (`dictionaryapi.dev` / `tts`
   / `none`). Existing docs have their multimedia URLs refreshed
   if Pexels returned a new image or the audio cache updated.

Both paths share:
- Atomic `findOneAndUpdate` with `$set` + `$setOnInsert`
  + `$inc` + `$currentDate`.
- Idempotent unique index on `id` only.
- `contador_consultas` incremented on every hit.
- `ultima_vez_visto` set to server clock on every hit.

`migrado_desde` is server-managed via `$setOnInsert` only — clients
hint the value (bulk passes `'SPA_Bulk_Migration'`, lazy omits it
and defaults to `'SPA_Lazy_Migration'`). Updates never overwrite
the marker.

Re-running bulk is idempotent: existing docs get updated
multimedia URLs (same picsum seed → same URL → no actual change)
and their original `migrado_desde` is preserved. Verified output:

```
[bulk-direct] DONE in 1.0s
  matched:   1000
  modified:  1000
  upserted:  0
  inserted:  0
  errors:    0
```

## Open / parked
- (none) — user-driven; awaiting next instruction.
- Likely next candidates:
  - **Remove static JSON read**: switch `useVerbos` to fetch verbs from MongoDB instead of `/verbos_estructura.json`. Requires adding `GET /api/verbs` (with pagination or full dump).
  - **Proactive enrichment**: background Pexels/Free-Dictionary enrichment of bulk-seeded docs (`audio_source: 'pending'`) so all 1000 are fully enriched before lazy visits.