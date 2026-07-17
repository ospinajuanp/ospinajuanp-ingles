# Agent Handoff — ospinajuanp-ingles

## Project
React 19 + Vite 8 + Tailwind v4 SPA for learning English verbs in Spanish. On-demand Pexels hero images, Free Dictionary audio (with `SpeechSynthesis` fallback), weighted-random initial verb, progressive-disclosure UX (blur-reveal of Spanish).

## Repo
- GitHub: `ospinajuanp/ospinajuanp-ingles`, branch `main`
- Working tree: clean, last commit `b3cba24`

## Key conventions
- Dataset: `verbos_estructura.json` at repo root (gitignored), copied to `public/` by a Vite plugin (`syncDataPlugin` in `vite.config.js`) on dev start, build start, and on every change. The plugin triggers `full-reload` via WebSocket.
- Weighted random: buckets A (≤10, 60% → **edited to 50%**), B (10.1–500, 25% → **30%**), C (500.1–1000, 15% → **20%**). Lives in `src/utils/weightedRandom.js`.
- Env: `.env` / `.env.*` are gitignored, `.env.example` is force-added via `!.env.example` negation. Two keys: `VITE_PEXELS_API_KEY` + optional `VITE_PEXELS_API_KEY_2` (automatic fallback on 401/403/429/5xx/network).
- ESLint 9 flat config: forbids `setState` in `useEffect` (`react-hooks/set-state-in-effect`). Use derived state or `useState` initializer instead.
- Audio uses imperative `new Audio()` (NOT JSX `<audio>`) because React render-during-await left state stuck on "loading". `SpeechSynthesis` is fallback when API has no phonetics (`draw`, `set`, `run` return empty).
- Image cache is a `Map<word, photo[]>` in `src/utils/imageCache.js`, hydrated from and persisted back to `localStorage` under key `verbos:pexelsCache` (~100 KB for ~700 verbs). Refresh button cycles Pexels pages by appending.
- Image overlay z-index: blur `z-0`, audio wrapper `z-10`, refresh + ImageCredit + maximize `z-30`.
- Maximize button (top-left, persists to `localStorage['verbos:heroExpanded']`): collapsed = `object-cover`; expanded = `object-contain`, `h-[min(70vh,560px)] min-h-[280px]`, `bg-slate-900/95` so full image fits centered.
- Header: sticky. Mobile `flex-col gap-3`; desktop `lg:grid lg:grid-cols-[1fr_2fr_1fr]`.

## Important gotchas
- `src/hooks/useVerbos.js` weighted-pick guards against the old `isFirstEffectRun` bug using a `cameFromEmpty` flag (check it when touching shuffle/init logic).
- `AudioButton.jsx` is a `forwardRef` so `VerbImageOverlay` can trigger play on image click. Has `isMountedRef` guarding `setState` after fetch await.
- `SpeechSynthesis` cleanup pauses + cancels speech on unmount. Params: `lang: 'en-US'`, `rate: 0.9`.
- `CategoryFilter.jsx` is a dropdown with click-outside + Escape + scroll-close, `w-72 max-w-[calc(100vw-1rem)]` for mobile, container `block w-full sm:inline-block sm:w-auto`.
- `src/utils/tips.js` has 53 short practical English tips in Spanish; `selectTip(seed)` cycles deterministically.

## Relevant files
- `src/utils/pexels.js`: dual-key client, `currentKeyIndex` module rotation, `tryFetch` helper, `checkPexelsStatus()` iterates all keys. Exports `fetchPexelsPhoto`, `checkPexelsStatus`, `hasPexelsKey`.
- `src/components/VerbCard.jsx`: owns `heroExpanded` state with localStorage hydration, renders VerbImage + VerbImageOverlay + content sections. Maximize button has `data-overlay-control="expand"`, swaps between `Maximize`/`Minimize` Lucide SVGs.
- `src/components/AudioButton.jsx`: `forwardRef`, Pexels-style API + SpeechSynthesis fallback.
- `src/components/CategoryFilter.jsx`: dropdown with per-category counts, "Limpiar filtros" reset.
- `src/hooks/useVerbos.js`: loads JSON, flattens, filters, weighted-random initial pick, shuffle, keyboard nav, exposes `counts` with `byCategory`, `bySubcategory`, `subForCategory(cat)`.
- `src/utils/weightedRandom.js`: bucket classifier + lottery. Probabilities 50/30/20.
- `src/utils/imageCache.js`: `getCachedImages`, `addCachedImage`, `Map<word, photo[]>`.
- `src/utils/audioCache.js`: tri-state (URL string | `'__tts__'` | `'__none__'`).
- `src/utils/tips.js`: 53 tips, `selectTip(seed)`.
- `src/data/weightedVerbs.js`: ~800 weighted verbs, first-occurrence-wins dedup map.
- `vite.config.js`: `syncDataPlugin` watches root JSON, copies to `public/` on dev start + change.
- `.env.example`: documents both keys.
- `README.md`: setup, architecture, data model, weighted random notes, Pexels rotation.
- `verbos_estructura.json` (root, gitignored) / `public/verbos_estructura.json` (built): canonical dataset, ~700+ verbs currently filled.

## Build
`pnpm build` → `dist/` produces ~265 KB JS + ~40 KB CSS gzipped.

## What works
- 190+ filled verbs with hero image (Pexels or Picsum), audio (API + TTS fallback), 6 conjugations with eye/eye-off reveal, 6 sentences with blur-reveal.
- Header sticky + responsive, category filter, shuffle, keyboard nav, weighted-random initial pick, tips banner, footer.
- README + .env.example + all wiring in place.

## Open / parked
- None right now (working tree clean). Awaiting user instruction.

## How to run
```bash
pnpm install
cp .env.example .env       # optional: paste 1 or 2 Pexels keys
                            # and MONGODB_URI if you want to sync
pnpm dev
# or
pnpm build && pnpm preview

# One-shot: migrate all 1000 verbs from verbos_estructura.json
# into MongoDB Atlas (deterministic picsum URLs, audio pending).
# Requires pnpm dev running in another terminal.
pnpm bulk:migrate
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
- Idempotent unique index on `id` only (`infinitivo.ing` is NOT
  indexed — the dataset has ~95 verbs with duplicate ing, e.g.
  'rewrite', 'analyze', 'check').
- `contador_consultas` incremented on every hit.
- `ultima_vez_visto` set to server clock on every hit.

`migrado_desde` is server-managed via `$setOnInsert` only — clients
hint the value (bulk passes `'SPA_Bulk_Migration'`, lazy omits it
and defaults to `'SPA_Lazy_Migration'`). Updates never overwrite
the marker.

Re-running bulk is idempotent: existing docs get updated
multimedia URLs (same picsum seed → same URL → no actual change)
and their original `migrado_desde` is preserved.

To query by source:
```js
db.verbos.countDocuments({ migrado_desde: 'SPA_Bulk_Migration' })
db.verbos.countDocuments({ migrado_desde: 'SPA_Lazy_Migration' })
db.verbos.countDocuments({ audio_source: 'pending' })      // audio not yet resolved
db.verbos.countDocuments({ image_source: 'pexels' })       // enriched by lazy sync
```
