# Agent Handoff — ospinajuanp-ingles

## Project
React 19 + Vite 8 + Tailwind v4 + DaisyUI 5 SPA for learning English verbs in Spanish. On-demand Pexels hero images, Free Dictionary audio (with `SpeechSynthesis` fallback), weighted-random initial verb, progressive-disclosure UX (blur-reveal of Spanish), namespaced `/v1/verbs/:verbSelector` + `/v1/test/` routing with a `/` landing page, MongoDB Atlas lazy+bulk sync, **SM-2 spaced repetition / SRS module at `/v1/test`** with 3D-flip flashcards and `localStorage`-first persistence, **silent local-first multi-device sync** of SRS data via anonymous UUIDv4 `syncToken` + QR-code pairing, and a multi-theme switcher (light / dark / dracula / cupcake).

## Repo
- GitHub: `ospinajuanp/ospinajuanp-ingles`, branch `main`
- Live: `https://ospinajuanp-ingles.vercel.app/`
- Working tree: clean, last commit `(this session — see Session commit log at the bottom)`

## Key conventions
- Dataset: `verbos_estructura.json` at repo root (gitignored), copied to `public/` by a Vite plugin (`syncDataPlugin` in `vite.config.js`) on dev start, build start, and on every change. The plugin triggers `full-reload` via WebSocket. **HMR auto-restarts dev server on `api/verbs/sync.js` changes — keep in mind during bulk runs.**
- Routing: **URL is the single source of truth**. React Router v7.18.1. **Namespaced under `/v1`**:
  - `/` → `<HomePage>` (landing menu, two DaisyUI cards: Explorar Verbos / Repasar). Does **not** auto-pick a verb.
  - `/v1/verbs/:verbSelector` → `<VerbView>`. `verbSelector` accepts digits (`verb.id`) or string (`infinitivo.ing` case-insensitive trimmed).
  - `/v1/test` (and `/v1/test/`) → `<SRSStudyPage>`.
  - `/repaso` and `/:verbSelector` are kept as **back-compat redirects**: `/repaso` → `/v1/test`, `/<slug>` → `/v1/verbs/<slug>`. Any other unknown URL → `<Navigate to="/" replace />`.
- `useParams()` only works inside `<Route>`. `useVerbos` lives in `<App>` ABOVE `<Routes>`, so reads `useLocation().pathname` and parses with regex `/^\/v1\/verbs\/([^/]+)\/?$/` + `decodeURIComponent` as `effectiveSelector`. The regex is scoped to the verb namespace — `/`, `/v1/test`, and `/repaso` no longer trigger any verb parsing. Falls back to `useParams()` value when present. **No more `RESERVED_ROUTES` set** — the namespaced regex replaces it.
- Weighted random: buckets A (≤10, 50%), B (10.1–500, 30%), C (500.1–1000, 20%). Lives in `src/utils/weightedRandom.js`.
- Env: `.env` / `.env.*` are gitignored, `.env.example` is force-added via `!.env.example` negation. Two Pexels keys (`VITE_PEXELS_API_KEY` + optional `VITE_PEXELS_API_KEY_2`, automatic fallback on 401/403/429/5xx/network) + `MONGODB_URI` (server-side only).
- ESLint 9 flat config: forbids `setState` in `useEffect` (`react-hooks/set-state-in-effect`). Use derived-state pattern (setState during render, like VerbCard lines 425-433) OR `useState` initializer. New Node-globals block for `scripts/**/*.mjs` and `api/**/*.js` with `no-undef: error`. `src/main.jsx` and the context files use `/* eslint-disable react-refresh/only-export-components */` at the top of the file (matches the existing context-file pattern).
- **ID guards MUST use `== null`, not `!id`**. `!0 === true` so `if (!verb?.id) return` silently skips id=0 (the "accept" verb). All id checks should be `if (verb?.id == null) return`.
- Audio uses imperative `new Audio()` (NOT JSX `<audio>`). `SpeechSynthesis` fallback when API has no phonetics (`draw`, `set`, `run`). Params: `lang: 'en-US', rate: 0.9`.
- Image cache: `Map<word, photo[]>` in `src/utils/imageCache.js`, hydrated from and persisted to `localStorage` under key `verbos:pexelsCache` (~100 KB for ~700 verbs). One JSON blob; refresh button cycles Pexels pages.
- Maximize button (top-left, `data-overlay-control="expand"`, persists to `localStorage['verbos:heroExpanded']`): collapsed = `object-cover h-44 sm:h-52 md:h-56`; expanded = `object-contain h-[min(70vh,560px)] min-h-[280px] bg-slate-900/95`.
- Tips rewritten with Spanish glossing: each English example has Spanish translation + per-word Spanish equivalents. `whitespace-pre-line` rendered in `<p>`.
- Image overlay z-index: blur `z-0`, audio wrapper `z-10`, refresh + ImageCredit + maximize `z-30`.
- Header: sticky. Mobile `flex-col gap-3`; desktop `lg:grid lg:grid-cols-[1fr_2fr_1fr]`. The right column is a `flex flex-wrap items-center justify-end gap-2` containing `CategoryFilter` then `ReviewNavButton` then `ThemeSwitcher`. **`SearchBar` + `CategoryFilter` + `ReviewNavButton` all gate on `isVerbRoute` (`pathname.startsWith('/v1/verbs')`); `ThemeSwitcher` is the only header control always visible.** On `/` and `/v1/test` the right column is just `ThemeSwitcher`.
- **SRS commit updaters MUST `return draft`**. `useSRS`'s `commit(updater)` wraps `setStore((prev) => { … updater(draft) … })`. If `updater` returns `undefined` (e.g. mutates-then-forgets-to-return), `setStore(undefined)` runs and the next render's `store` is `undefined`, which crashes every later closure that reads `store.cards`. `commit` also has a defensive guard that defaults to `draft` when the returned value lacks `cards`/`order`.
- **SRS verb lookup uses `verb.id == null`** (not `!verb.id`) when computing `verbKey`. Same rule as the rest of the codebase.
- **Only ONE call to `useSRS()`** may exist in the app — it lives at the top of `Root` in `src/main.jsx`. Everything else reads via `useSRSContext()`. (Mirrors the `VerbContext` pattern: `useVerbos()` lives in `<App>`, consumers use `useVerbosContext()`.)
- **Only ONE call to `useSyncEngine()`** may exist — it also lives in `Root`, alongside `useSRS()`. It receives `{ srs, themeApi }` from the same `Root`. Consumers (SyncButton, SyncModal) read via `useSyncContext()` — but the context returns `null` (not throw) when the provider is absent, so components render gracefully even if the engine is intentionally disabled.
- **Sync engine purity rules** (React 19 + ESLint 9 `react-hooks/immutability` / `react-hooks/purity`): `Date.now()` is **forbidden during render** — always inside `useEffect` or event handlers. `setState` inside `useEffect` body is **forbidden** — use the "adjusting state during render" pattern (`useState` initializer + prev-prop tracking) or move the side effect into an event handler. `useRef` is **forbidden inside `useEffect` body** for storing a ref-to-callback — just include the dependency in the callback's `useCallback` deps and let `useEffect`s re-subscribe on change. The SyncModal `StatusBadge` uses a 30-second `setInterval` to tick a `now` state so "hace Xs" labels don't call `Date.now()` during render.


## Important gotchas
- **`!id` vs `== null` (CRITICAL)**: see Key conventions. The first version of `reportEnrichment` and `onEnriched` used `!verb?.id` and `!currentVerb?.id`, which silently skipped id=0 ("accept"). All other ids (1-999) worked. Symptom: `contador_consultas` increments but `image_source` stays `picsum` and `audio_source` stays `pending`.
- **VerbImage remount**: `key={verbKey}` alone is not reliable in production — old `<VerbImage>` instances can stack in the DOM when navigating with arrows or direct URLs (cache-hit case). Use a **composite key** `<div key={`${verbKey}-${renderId}`}>` wrapping `<VerbImage>` where `renderId` is a counter incremented on every verb change via derived-state pattern. VerbImage also has a derived-state sync (`useState(word) for trackedWord`) as defensive fallback.
- **Atlas UI defaults to 25 docs per page** — confusing on first check. Use `countDocuments()` or scroll/paginate to confirm full migration.
- **NO `infinitivo.ing` unique index** — dataset has ~95 verbs with duplicate `ing` (`rewrite`, `analyze`, `check`…). Only `id` is uniquely indexed.
- `migrado_desde` is server-managed via `$setOnInsert` only. Bulk passes `'SPA_Bulk_Migration'`, lazy omits it and defaults to `'SPA_Lazy_Migration'`. **Stripped from `$set`** so updates never overwrite the marker.
- `AudioButton.jsx` is a `forwardRef` so `VerbImageOverlay` can trigger play on image click. Has `isMountedRef` guarding `setState` after fetch await.
- `SpeechSynthesis` cleanup pauses + cancels speech on unmount. Params: `lang: 'en-US'`, `rate: 0.9`.
- `CategoryFilter.jsx` is a dropdown with click-outside + Escape + scroll-close, `w-72 max-w-[calc(100vw-1rem)]` for mobile, container `block w-full sm:inline-block sm:w-auto`.
- `src/utils/tips.js` has 53 short practical English tips with Spanish glossing; `selectTip(seed)` cycles deterministically.
- `src/hooks/useVerbos.js` reads `verbos_estructura.json` via `fetch('/verbos_estructura.json')` (the public copy). **Bulk migration writes to MongoDB but does NOT yet replace the JSON read** — both paths coexist.
- **Vercel production needs env vars**: `VITE_PEXELS_API_KEY`, `VITE_PEXELS_API_KEY_2`, `MONGODB_URI` must be set in Vercel Dashboard → Settings → Environment Variables, all three envs. Vercel does NOT auto-redeploy when env vars change — must trigger manually.
- **The sync endpoint is `ingles-db.user_sync`, NOT `ingles-db.verbos`.** Different collection. Schema is `{syncToken, srsStore, theme, createdAt, lastActiveAt}` with a unique index on `syncToken`. The verbs collection (`ingles-db.verbos`) stays unaffected — both coexist in the same database.
- **`syncToken` is generated by `crypto.randomUUID()`** with a `crypto.getRandomValues`/`Math.random` fallback (older browsers). Validation regex `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i`. Persisted at `localStorage['ospinajuanp-ingles:syncToken']`. Survives reloads — first device mints a fresh UUIDv4, subsequent sessions reuse the same one.
- **A user without a token gets one auto-minted on first mount of `useSyncEngine`**. No onboarding modal, no "Sign in" button. The token is the entire identity.
- **Cross-tab conflict resolution**: if Device A and Device B both edit the same card offline, the merge is **Last-Write-Wins by `srs.lastReviewed` timestamp**, falling back to `srs.nextReview` → `card.createdAt`. Tie-breaker = remote (Atlas) wins. The merged card's `type/verbKey/front/infinitivo` come from whichever side had the newer review timestamp. `order` is union'd preserving each side's relative order. **This is intentional v1 behavior** — no operational-transform or CRDT. Acceptable because cards are mostly mutated by user actions (grading) which timestamp themselves; structural fields rarely change after creation.

## Relevant files
- `src/App.jsx`: `useVerbos()` once at top level (above `<Routes>`), wraps in `<VerbProvider value={verbos}>`, renders ShellHeader + `<Routes>`:
  - `/` → `<HomePage>`
  - `/v1/verbs/:verbSelector` → `<VerbView retryKey={...} />`
  - `/v1/test` and `/v1/test/` → `<SRSStudyPage />`
  - `/repaso` → `<Navigate to="/v1/test" replace />` (legacy redirect)
  - `/:verbSelector` → `<LegacyVerbRedirect>` (rewrites to `/v1/verbs/<slug>`)
  - `*` catch-all → `<Navigate to="/" replace />`
  
  Does NOT call `useSRS()` — that lives in `Root` (`src/main.jsx`). `checkPexelsStatus()` on mount. ShellHeader includes `ThemeSwitcher` plus gated `SearchBar` + `CategoryFilter` + `ReviewNavButton`; all three render only when `pathname.startsWith('/v1/verbs')` (hidden on `/` and `/v1/test`). On those non-verb routes only `ThemeSwitcher` shows in the right column.
- `src/main.jsx`: wraps a local `Root` component in `<BrowserRouter>` + `<StrictMode>`. `Root` calls `useSRS()` once and wraps `<App />` in `<SRSProvider value={srs}>`. File-level `/* eslint-disable react-refresh/only-export-components */`.
- `src/contexts/VerbContext.jsx`: `VerbProvider({value, children})` + `useVerbosContext()` hook. File-level `/* eslint-disable react-refresh/only-export-components */`.
- `src/contexts/SRSContext.jsx`: `SRSProvider({value, children})` + `useSRSContext()` (throws if used outside the provider). Same eslint-disable directive at top.
- `src/hooks/useVerbos.js`: URL-driven via `useLocation` regex fallback scoped to `/v1/verbs/<slug>`. Exposes `current`, `currentVerb`, `currentIndex`, `oraciones`, `conjugationEntries`, `prev/next/shuffle/goTo/goToRandomVerb`, `reportEnrichment`, `categories`, `counts`, `filtered`. **No more root auto-pick** — HomePage drives the initial verb via `goToRandomVerb()`. Two useEffects remain: invalid-selector-redirect to `/`, and filter-excludes-verb redirect within the verb namespace. Auto-registers `currentVerb` into the SRS store via `useSRSContext()` (idempotent). `verbHref(slug)` helper centralizes the `/v1/verbs/<slug>` URL shape — use it instead of building the string inline. **Never** treat id=0 as falsy — `verb.id == null` always.
- `src/hooks/useSRS.js`: the single-instance SRS hook. Reads from / writes to `localStorage['ospinajuanp-ingles:srs:v1']`. Exposes `cards`, `dueCards`, `dueCount`, `totalCount`, `customCount`, `verbCount` and actions `addCustomSentence`, `registerVerb`, `gradeCard`, `removeCard`. Cross-tab sync via `window.addEventListener('storage', …)`. `commit(updater)` wraps `setStore((prev) => { … })` and has a defensive guard defaulting to `draft` when the returned value lacks `cards`/`order` — every action's updater MUST still `return draft` explicitly.
- `src/utils/srs.js`: pure SM-2 functions. Exports `SRS_MIN_EF = 1.3`, `SRS_INITIAL_EF = 2.5`, `createInitialSRSState(initialIntervalDays = 0)`, `calculateNextReview(currentInterval, currentEF, isSuccess)`, `isDue(state, now?)`. No React, no I/O.
- `src/utils/mongoSync.js`: fire-and-forget `fetch('/api/verbs/sync', {method:'POST', keepalive:true})` with `console.warn` on errors. Uses `payload.id == null` guard.
- `src/utils/flatten.js`: `flattenVerbos(data)` walks `{generales: {simples, irregulares, …}, tecnologia: {…}}` → flat array of `{verb, category, subcategory}`. `collectCategories(flat)` returns per-category subcategories.
- `src/utils/pexels.js`: dual-key client (`fetchPexelsPhoto`, `checkPexelsStatus`, `hasPexelsKey`, module-level `currentKeyIndex` rotation, `tryFetch` helper, retry once on second key).
- `src/components/VerbCard.jsx`: accepts `onEnriched` callback; tracks `imageInfo`/`audioInfo` state; resets on verb change via derived-state pattern; `renderId` counter increments on verb change for composite key on wrapper div. Renders `<div key={`${verbKey}-${renderId}`}><VerbImage ... /></div>`. `onEnriched` effect uses `currentVerb?.id == null` guard.
- `src/components/VerbImage.jsx` (inside VerbCard.jsx): eager Pexels fetch on mount; derived-state sync updates src/credit/stage when `word` changes AND cache has photos. Returns to picsum fallback when Pexels unavailable.
- `src/components/AudioButton.jsx`: `forwardRef`, accepts `onResolved({audio_url, audio_source})`. **Eager resolution on mount** (cache check → fetch from dictionaryapi.dev). Fires on mount and after every resolution path. `console.warn` only on fetch failure.
- `src/components/CategoryFilter.jsx`: dropdown with per-category counts, "Limpiar filtros" reset.
- `src/components/ReviewNavButton.jsx`: header pill `<Link to="/v1/test">` with rotating badge showing `dueCount`. Hidden badge when zero; `99+` cap. Reads via `useSRSContext()`. **Only rendered inside `ShellHeader` when `pathname.startsWith('/v1/verbs')`** — same gate as `SearchBar` / `CategoryFilter`. Outside the verb namespace (e.g. on `/v1/test` itself) it is not rendered so the header doesn't show a self-referential pill.
- `src/components/ThemeSwitcher.jsx`: DaisyUI 5 dropdown (`dropdown dropdown-end`, `menu dropdown-content`) with theme options. Renders check-mark on the active theme. Uses DaisyUI tokens (`bg-base-100`, `text-base-content`) so it adapts to all themes. ARIA-labelled trigger button. Lives in the ShellHeader right column after `ReviewNavButton`.
- `src/hooks/useTheme.js`: persists `localStorage['ospinajuanp-ingles:theme']`, sets `<html data-theme="...">` in `useEffect`. Exports `THEMES` (array of `{id, label}`), `DEFAULT_THEME='light'`, `STORAGE_KEY='ospinajuanp-ingles:theme'`, and `{ theme, setTheme, themes }`. Mirrors a small inline `<script>` in `index.html` that pre-applies the theme before React mounts (FOUC prevention).
- `src/pages/HomePage.jsx`: landing page (NEW). DaisyUI `hero` + two `card` blocks (Explorar Verbos / Repasar). "Empezar" calls `verbos.goToRandomVerb()` (weighted random + `navigate('/v1/verbs/<slug>')`); "Abrir repaso" is `<Link to="/v1/test">`. Uses DaisyUI theme tokens (`bg-base-100/200/300`, `text-base-content`, `btn-primary`) so the page re-skins instantly when the theme switches.
- `src/components/SearchBar.jsx`, `src/components/ConjugationGrid.jsx`, `src/components/SentencePill.jsx`, `src/components/NavButtons.jsx`, `src/components/HeroIllustration.jsx`, `src/components/ImageCredit.jsx`: stable, prop-driven.
- `src/components/AddFlashcardForm.jsx`: ES/EN form for the SRS custom deck. Validates both fields, dispatches `onAdd({es, en})`, supports `onCancel` callback.
- `src/components/Flashcard.jsx`: 3D flip card used by SRSStudyPage. ES on front, EN on back, Tailwind arbitrary values for the perspective/transform/rotateY/backface stack. Grade buttons ("No lo recordé" / "Lo recordé") enabled only when `flipped`. Derived-state reset on card-id change.
- `src/pages/SRSStudyPage.jsx`: SRS study session view. Counts grid (Pendientes hoy / Total / Oraciones / Verbos), optional form toggle, `useMemo`-derived `shuffle(srs.dueCards)` queue with `cursor` state, custom empty states for empty-deck vs. session-complete.
- `vite.config.js`: `defineConfig(({mode}) => { const env = loadEnv(mode, process.cwd(), ''); Object.assign(process.env, env); return { plugins: [...] } })`. Middleware at `/api/verbs/sync` AND `/api/sync/user` (both lazy-import their handlers). `syncDataPlugin` watches root JSON.
- `api/verbs/sync.js`: server-side handler. Validates payload with `verb.id == null` guard, cached `MongoClient`, idempotent `ensureIndexes` (`id_unique` + `last_seen_desc`), atomic `findOneAndUpdate`. Reads `migrado_desde` from payload (default `'SPA_Lazy_Migration'`), strips from `$set`, puts in `$setOnInsert`.
- `api/sync/user.js`: server-side handler for the user-state sync endpoint. GET upserts `lastActiveAt` via `findOneAndUpdate` (returns `state: null` when no record exists yet — bootstrap path). POST upserts `{syncToken, srsStore, theme}` with `$setOnInsert: {createdAt}` + `$currentDate: {lastActiveAt}`. Validates: `syncToken` matches UUIDv4 regex, `srsStore.version === 1` with `cards`+`order`, theme ∈ `{light,dark,dracula,cupcake}`, payload ≤ 256 KB (early reject with `413`). Returns `{ok, wasInsert, lastActiveAt}` on success.
- `scripts/bulk-direct.mjs`: fast bulk via `MongoClient.bulkWrite()`, ~1s for 1000 verbs. Strip `id` from `$set` to avoid `$set`+`setOnInsert` conflict. Env: `MONGODB_URI` required.
- `src/utils/syncIdentity.js`: UUIDv4 sync-token manager. Exports `getSyncToken()`, `peekSyncToken()`, `linkSyncToken(token)`, `resetSyncToken()`, `isValidSyncToken(token)`, `consumeLinkTokenFromUrl()`, `buildLinkUrl(token)`. Uses `crypto.randomUUID()` with `crypto.getRandomValues` fallback. Storage key: `ospinajuanp-ingles:syncToken`.
- `src/utils/syncMerge.js`: pure LWW merge. Exports `mergeSRSStores(local, remote)` and `shouldPushLocal(local, remote)`. Compares cards by `srs.lastReviewed` (fallback `srs.nextReview` → `card.createdAt`), preserves winner's structural fields (`type/verbKey/front/infinitivo`), `order` is union with each side's relative order preserved, tie-breaker = remote.
- `src/utils/syncClient.js`: HTTP wrapper. Exports `fetchUserState(token)` (GET) and `pushUserState({syncToken, srsStore, theme})` (POST, `keepalive: true`). Both wrapped in 8 s `AbortController` timeout, structured `{ok, reason, status, data}` envelope, fire-and-forget (no throw).
- `src/hooks/useSyncEngine.js`: silent sync engine. Returns `{syncToken, status, lastError, lastSyncedAt, pendingPush, linkNewToken, unlink, forcePushNow, forcePullNow}`. See the Silent Multi-Device Sync section below.
- `src/contexts/SyncContext.jsx`: thin `SyncProvider({value, children})` + `useSyncContext()` (returns `null` when absent — does NOT throw, unlike `useSRSContext`). File-level `/* eslint-disable react-refresh/only-export-components */`.
- `src/components/SyncButton.jsx`: header button with status dot (success/warning/error) and label. DaisyUI primitives only (`btn btn-ghost btn-circle`, `<Cloud size={18} />` from lucide-react). Hidden entirely on small screens (`hidden sm:inline-flex`).
- `src/components/SyncModal.jsx`: DaisyUI v5 native `<dialog className="modal">` with QR code, token display (soft-broken wrap so it fits any width), copy buttons, link-input form (accepts bare UUIDv4 OR full URL), and a danger-zone "Desvincular dispositivo" section. Status badge uses 30 s `setInterval` to tick a `now` state for "hace Xs/min" labels (avoids `Date.now()` during render). Form-field reset uses the derived-state pattern (`prevOpen !== open → reset`). QR img points to `https://api.qrserver.com/v1/create-qr-code/?size=240x240&margin=1&data=…` with `<img onError>` fallback that swaps to a copyable URL block.
- `scripts/bulk-migrate.mjs`: bulk via HTTP POSTs, 100ms throttle (~10 req/sec), ~3-5 min for 1000 verbs. Endpoint from `MIGRATE_ENDPOINT` env (default `http://localhost:5173/api/verbs/sync`).
- `eslint.config.js`: default browser config + new block for `scripts/**/*.mjs` and `api/**/*.js` with `globals: ...globals.node`, `no-undef: error`.
- `package.json`: scripts `dev`, `build`, `preview`, `lint`, `bulk:migrate`, `bulk:direct`. Deps: react/react-dom 19.2.7, react-router-dom 7.18.1, mongodb 7.5.0. **No new dependencies added for sync** — `crypto.randomUUID()` is native, QR codes come from external `https://api.qrserver.com/v1/create-qr-code/`.
- `vercel.json`: SPA fallback rewrite `/(?!api/)(.*)` → `/index.html`. Excludes `/api/*` so the serverless function keeps working.
- `.env.example`: documents `VITE_PEXELS_API_KEY`, `VITE_PEXELS_API_KEY_2`, `MONGODB_URI=`.
- `.env` (gitignored): both Pexels keys + `MONGODB_URI` with quoted connection string `mongodb+srv://…`.
- `README.md`: setup, architecture, data model, weighted random notes, Pexels rotation.
- `verbos_estructura.json` (root, gitignored): 1000 verbs flattened to 905 unique `infinitivo.ing` (95 duplicates); all 1000 unique `id`.

## Build
`pnpm build` → `dist/` produces **~375 KB JS raw / ~116 KB gzipped** (1820 modules after silent-sync engine) and **~134 KB CSS raw / ~21 KB gzipped**. MongoDB driver NOT in client bundle; lucide-react IS in the client bundle (tree-shaken, ~40 unique icons). The sync engine (utils + hook + context + 2 components) added ~20 KB raw JS and ~8 KB CSS (DaisyUI `modal`/`dialog`/`btn-circle` primitives + the new Cloud icon). Build cost over time:
- 46 KB → 111 KB CSS after first DaisyUI integration (4 themes shipped in one bundle).
- 111 KB → 120 KB CSS after the whole-app theming refactor (more DaisyUI utility classes used).
- 341 KB → 340 KB JS after the lucide-react icon migration (slight **reduction** in raw JS).
- 340 KB → 355 KB JS / +1.5 KB CSS after DeckManager (table, modal, join, textarea-bordered, plus ~3 new icons).
- 355 KB → 375 KB JS / +14 KB CSS after silent-sync engine (`<dialog>` modal + SyncButton + 3 sync utils + the engine hook).

## What works
- **1000/1000 verbs migrated to MongoDB Atlas** in `ingles-db.verbos` via `pnpm bulk:direct`. All `migrado_desde='SPA_Bulk_Migration'`, `audio_source='pending'`, `image_source='picsum'`, `oraciones` populated.
- Idempotency verified: re-running `pnpm bulk:direct` returns `matched: 1000, modified: 1000, upserted: 0, inserted: 0, errors: 0`.
- Lazy sync fires automatically on every verb visit (random button, arrows, keyboard, direct URL). Existing docs get refreshed URLs, new ones get `migrado_desde='SPA_Lazy_Migration'`.
- id=0 ("accept") specifically verified to update after the `!id` → `== null` fix.
- Routing fully working under the `/v1` namespace: `/` (HomePage landing), `/v1/verbs/0`, `/v1/verbs/accept`, `/v1/verbs/feel`, `/v1/verbs/tell`, `/v1/verbs/know` all render VerbCard. `/v1/test` opens the SRS study page. Legacy redirects still work: old `/<slug>` → `/v1/verbs/<slug>`, old `/repaso` → `/v1/test`. Unknown URLs → HomePage.
- Vercel SPA fallback: direct URLs like `/accept` work (rewrite to `index.html`).
- 190+ verbs have hero image (Pexels or Picsum), audio (API + TTS fallback), 6 conjugations with eye/eye-off reveal, 6 sentences with blur-reveal.
- Header sticky + responsive, category filter, shuffle, keyboard nav, weighted-random initial pick, tips banner, footer. Header now also hosts the **SRS "Repaso" pill** with a due-count badge that updates in real time across the whole app (driven by `SRSContext`).
- **SRS module (c5f5bda)**: `/v1/test` route (back-compat `/repaso` → `/v1/test`), 3D flip flashcards (Tailwind `preserve-3d` / `backface-hidden` / `rotate-y-180`), Spanish↔English reveal, SM-2 grading buttons. Two decks (`type: 'custom' | 'verb'`) coexist: custom sentences via `AddFlashcardForm`, verbs auto-registered when visited in the main app. Persistence is `localStorage`-first under `ospinajuanp-ingles:srs:v1`. See the SRS section below.
- **Silent multi-device sync (this session)**: anonymous UUIDv4 `syncToken` auto-minted on first mount, persisted to `localStorage['ospinajuanp-ingles:syncToken']`. Cross-device pairing via QR code or `?syncToken=…` URL adoption. Debounced 2 s background push of SRS + theme to Atlas collection `ingles-db.user_sync`. Last-Write-Wins merge by `srs.lastReviewed`. Bootstrap push when remote is empty (silent migration of existing local decks). Pagehide/visibilitychange flush, 5-minute safety-net, cross-tab via `storage` event. See the Silent Multi-Device Sync section below.
- **Multi-theme + landing page (33d4039)**: `/` renders a DaisyUI hero with two action cards (Explorar Verbos / Repasar). Theme switcher in the header offers light / dark / dracula / cupcake, persisted to `localStorage['ospinajuanp-ingles:theme']` and applied to `<html data-theme=...>` (FOUC-prevention script in `index.html`).
- **Whole-app theming (a08442b)**: every slate/indigo reference replaced with DaisyUI semantic tokens (`bg-base-100`, `text-base-content`, `text-primary`, `border-base-300`, etc.). The theme now applies to the entire app — body bg, ShellHeader, VerbCard, Flashcard, SRSStudyPage, AddFlashcardForm, CategoryFilter, SearchBar, NavButtons, ConjugationGrid, SentencePill, AudioButton, all error/success/empty states. See the Multi-theme section below for the token mapping table.
- README + .env.example + all wiring in place.

## SRS module — Spaced Repetition

A local-first SM-2 implementation. Cards live entirely in `localStorage`; no network. Two decks coexist in a single study queue:

1. **Mazo Personalizado** — user-added sentences (`type: 'custom'`) created via `AddFlashcardForm`. Front = Spanish, back = English.
2. **Mazo de Verbos Vistos** — auto-populated. Every time the user lands on a verb in the main app, `useVerbos` calls `srs.registerVerb(currentVerb)`, which is idempotent per `verbKey` (`id:${id}` or `slug:${slug}`). Re-visits do not duplicate.

### Storage schema
`localStorage['ospinajuanp-ingles:srs:v1']`:
```json
{
  "version": 1,
  "cards": {
    "<cardId>": {
      "id": "<cardId>",
      "type": "custom | verb",
      "front": { "es": "...", "en": "..." },           // custom only
      "verbId": 0,                                       // verb only
      "verbKey": "id:0 | slug:accept",                   // verb only
      "infinitivo": { "ing": "...", "esp": "..." },      // verb only
      "createdAt": 1721234567890,
      "srs": {
        "interval": 3,
        "ef": 2.5,
        "repetitions": 2,
        "lastReviewed": 1721234599999,
        "nextReview": 1721496960000
      }
    }
  },
  "order": ["<cardId>", ...]   // FIFO insertion order
}
```

### Idempotency contract (verb auto-register)
`registerVerb(verb)` is idempotent per verb: visiting the same verb URL N
times creates exactly one card. The lookup uses a canonical `verbKey`:
- `id:${verb.id}` if `verb.id != null` (preferred — dataset guarantees unique ids 0–999). Never use `!verb.id` — id 0 is valid.
- `slug:${verb.infinitivo.ing.toLowerCase()}` as fallback when id is missing.

Before any commit, `registerVerb` scans `store.cards` for a `type === 'verb'`
entry with the same `verbKey`; if found, returns the existing card and does
NOT call `commit`, write to `localStorage`, or push to `order`. Re-visiting
`/accept` 100 times yields one card and zero writes after the first.

Known limitation: dataset has ~95 verbs that share an `infinitivo.ing` (e.g.
multiple `rewrite`, `analyze`, `check`). Because `resolveVerb` in
`src/hooks/useVerbos.js` returns the FIRST match, only one card per
duplicate-slug cluster is registered by navigation. The other ids with the
same ing never reach `registerVerb` unless the user visits them by numeric
URL (e.g. `/47` for the second `rewrite`). This is intentional v1 behavior.

### SM-2 algorithm (`src/utils/srs.js`)
Pure function, no I/O. Exports `SRS_MIN_EF = 1.3`, `SRS_INITIAL_EF = 2.5`, `SRS_GRADES = ['fail','hard','good','easy']`:
- `calculateNextReview(currentInterval, currentEF, grade)` where `grade ∈ SRS_GRADES`. Throws on invalid grade.
- **Fail** ("Otra vez"): `interval = 1`, `repetitions = 0`, `ef = max(1.3, ef - 0.20)`.
- **Hard** ("Difícil"): success-with-doubt. Same interval as good, `ef = max(1.3, ef - 0.10)`. Powers "El Camino de la Recuperación" — beats `fail` so EF recovers faster.
- **Good** ("Bien"): clean recall. `interval` grows by EF (ramped), `ef` unchanged.
- **Easy** ("Fácil"): instant recall. `interval` grows by EF (ramped), `ef += 0.15`.
- All three success grades share the same interval formula: 0 → 1, 1 → 3, then `round(prev * ef)`. Only EF differs.
- Hard floor `SRS_MIN_EF = 1.3` applied uniformly.
- `isDue(state, now?)` is a tiny predicate used by selectors.

### Architecture (data flow)
```
localStorage ['ospinajuanp-ingles:srs:v1']
   ▲                                      │
   │ writeStore(safeNext)                  │ readStore()
   │                                      ▼
   commit(updater) → setState          useState(() => readStore())   ← single instance in Root
   │                                      │
   ▼                                      │ value prop
useSRS()  ──── exposed via ────►  <SRSProvider value={srs}>
                                       │
                          ┌────────────┴────────────┐
                          ▼                          ▼
                   useSRSContext()           useSRSContext()
                          │                          │
                  ShellHeader.ReviewNavButton   SRSStudyPage
                  (badge via dueCount)          (form + queue + grading)
                          │
                  useVerbos.js auto-register effect
                  (calls srs.registerVerb(currentVerb))
```

### Provider placement (CRITICAL)
`<SRSProvider>` MUST wrap `<App />`, not the other way around. `useVerbos` runs in `<App>`'s body, and its auto-register effect calls `useSRSContext()` — so the provider has to exist by the time `useVerbos` renders. This is why `Root` was introduced in `src/main.jsx`. **Never call `useSRS()` twice** — one instance lives in `Root`, all consumers read via `useSRSContext()`. Mirrors the `VerbProvider`/`useVerbosContext` pattern.

### SRS-relevant files
- `src/utils/srs.js` — pure SM-2 functions + `createInitialSRSState()`, `isDue()`.
- `src/contexts/SRSContext.jsx` — `SRSProvider` + `useSRSContext()` (throws if used outside the provider).
- `src/hooks/useSRS.js` — single-instance hook owning `localStorage` access. Exposes `cards`, `dueCards`, `dueCount`, `totalCount`, `customCount`, `verbCount`, and actions: `addCustomSentence`, `registerVerb`, `gradeCard`, `removeCard`, **`editCustomCard`** (preserves SRS state). Cross-tab sync via `storage` event. `commit()` has a defensive guard (defaults to `draft` if updater returns a malformed value).
- `src/components/AddFlashcardForm.jsx` — ES/EN form with submit + cancel + inline error.
- `src/components/DeckManager.jsx` — table-based deck-management interface: real-time search across Español + Inglés, pagination 10/page (`join` button group with ellipsis gaps), per-row actions (`Pencil` only on custom cards, `Trash2` always). **Uses native `<dialog className="modal">` for BOTH the edit form AND the delete confirmation** — no `window.confirm` / `window.alert` anywhere in the app. The edit dialog uses `showModal()`/`close()` controlled by `useEffect`; form-field reset uses derived-state pattern. The confirm dialog mirrors the same pattern but renders an `AlertTriangle` chip + a card-preview block (`bg-base-200` with the type badge and the ES/EN text) so the user can see exactly which card they're about to delete, plus a destructive `btn bg-error text-error-content` for the action. Both dialogs close on backdrop click and ESC.
- `src/components/Flashcard.jsx` — 3D flip card. Pure CSS via Tailwind arbitrary values: outer container has `[perspective:1200px]`, inner button has `[transform-style:preserve-3d]` + `transition: transform 600ms`, front face has `[backface-visibility:hidden]`, back face adds `[transform:rotateY(180deg)]`. Reset on card change via derived-state pattern (matches `VerbCard`/`VerbImage`). Below the card: **4 grade buttons** in a 2×2 / 4-col grid: "Otra vez" (fail, rose), "Difícil" (hard, amber), "Bien" (good, emerald), "Fácil" (easy, sky-gradient). Hidden hint subtitles appear on `sm+`. All four enabled only when flipped.
- `src/components/ReviewNavButton.jsx` — header pill `<Link to="/v1/test">` with rotating badge (`dueCount`, hidden when 0, `99+` cap). Lives in the header right column next to `CategoryFilter`.
- `src/pages/SRSStudyPage.jsx` — study session UI: counters row (Pendientes hoy / Total / Oraciones / Verbos), optional form toggle, shuffled queue (`useMemo(shuffle(srs.dueCards), [srs.dueCards])`), cursor-driven progression. Empty states for "deck empty" vs "session complete". **Has a `ModeToggle` join group (BookOpen / ListFilter icons) to switch between "Estudiar" and "Gestionar Mazo" without leaving the page.** The top of the page is laid out in three layers: (1) compact "Volver" pill (`ArrowLeft`, `text-xs`) at the top-left, above the title container; (2) the title container itself is `flex flex-col gap-4 border-b border-base-300 pb-5 mb-6 sm:flex-row sm:items-end sm:justify-between` and holds "Repaso espaciado" + subtitle on the left and the `ModeToggle` aligned to `sm:justify-end` on the right; (3) the page content below the border.

### Entry / hookup changes
- `src/main.jsx` — introduces `Root` component that owns the single `useSRS()` instance and wraps `<App />` with `<SRSProvider value={srs}>`. File-level `/* eslint-disable react-refresh/only-export-components */` (matches the context-file pattern).
- `src/App.jsx` — no longer calls `useSRS()`. Still owns `VerbProvider` because `useVerbos` is called in `<App>`'s body (same root-vs-nested problem, but the original code solved it by wrapping `<App>` in `<VerbProvider>` in `main.jsx` originally — see the future-tightening note below). Imports and renders `<ReviewNavButton />` inside `ShellHeader`.
- `src/hooks/useVerbos.js` — imports `useSRSContext`. After `currentVerb` is computed, runs `useEffect(() => { if (currentVerb && srs) srs.registerVerb(currentVerb) }, [currentVerb, srs])`. Idempotent — repeat visits are no-ops. Also has the `RESERVED_ROUTES` guard so non-verb routes don't get hijacked into random-verb redirect.

### What works (SRS specifically)
- `/v1/test` (and the legacy `/repaso` redirect) renders with no console errors. Manually visiting the URL and clicking the header "Repaso" pill both work.
- Cards drawn on load, custom + verb decks mixed and shuffled into one queue.
- **4-level grading UI** ("Otra vez" / "Difícil" / "Bien" / "Fácil"). Each grade updates `localStorage` synchronously via `srs.gradeCard(cardId, grade)` and advances the cursor; the header badge decrements in real time on every other route.
- EF math verified in Node: starting at 2.50, six consecutive `fail` grades hit the 1.30 floor (clamped); a `hard` (-0.10) + `easy` (+0.15) cycle nets +0.05 EF — "El Camino de la Recuperación".
- Adding a custom sentence persists, appears in the queue if due today.
- **Re-visit idempotency**: visiting `/v1/verbs/accept`, `/v1/verbs/0`, or `/v1/verbs/Accept` any number of times always produces exactly one SRS card for that verb. `registerVerb` looks up by `verbKey` (`id:${id}`) and returns the existing card on subsequent calls.
- **Deck Manager** (3f3506f): header has a `ModeToggle` join group ("Estudiar" / "Gestionar Mazo"). The Gestionar tab shows a DaisyUI table with columns (Tipo / Español / Inglés / Estado SRS / Acciones), a real-time search input (matches either language), pagination 10/page with prev/next + first/last + numeric shortcuts + ellipsis gaps, edit (only `custom` cards via a native `<dialog className="modal">`) and delete (any card, with `window.confirm`). Verb cards show a disabled Pencil (their text comes from the official dataset and cannot be edited from the SRS side).

### Deck management actions (useSRS)
- `editCustomCard(cardId, { es, en })`: validates both fields non-empty, returns `null` if the card is missing or not `type: 'custom'`. Mutates `draft.cards[cardId].front` via `commit()` and **preserves** the SRS state (interval / ef / repetitions / lastReviewed / nextReview) — editing the prompt does not reset the schedule. Returns the updated card or `null` on failure. Updater ends with `return draft` to satisfy the `commit()` guard.
- `removeCard(cardId)`: deletes from `cards` + `order`. Updater ends with `return draft`.

### Deck management UI (`src/components/DeckManager.jsx`)
- Pulls `cards` (full list), `removeCard`, `editCustomCard` from `useSRSContext()`.
- Local state: `searchTerm`, `page`, `editingId`. Page resets to 1 when searchTerm changes (derived-state pattern, no setState in useEffect).
- `PAGE_SIZE = 10`. `totalPages = Math.max(1, ceil(filtered / 10))`. `safePage = Math.min(page, totalPages)` clamps if the active page becomes empty after filtering.
- `buildPageList(page, total)` returns `[1, total, page-1, page, page+1]` deduplicated and sorted, with `'…'` gaps for >7 pages.
- `<dialog>` lifecycle: `useEffect` watches `card` and calls `dialog.showModal()` / `dialog.close()` on the imperative DOM API. Form-field reset uses the derived-state pattern (`trackedId !== card.id → setEs/setEn`). The `cancel` DOM event (ESC key) is wired to `onClose` via `dialog.addEventListener('cancel', …)`.
- All UI uses DaisyUI tokens (`bg-base-100/200`, `text-base-content`, `border-base-300`, `badge-primary`, `badge-ghost`, `btn-primary`, `btn-ghost`, `join`, `modal`, `modal-box`, `modal-action`, `modal-backdrop`, `table`, `textarea-bordered`, `input-bordered`) and `lucide-react` icons (`Pencil`, `Trash2`, `Search`, `X`, `ChevronLeft`, `ChevronRight`, `ChevronsLeft`, `ChevronsRight`, `Layers`, `Save`, `AlertTriangle`).
- **Delete confirmation**: in-app `<dialog>` instead of `window.confirm`. Rendered as a `modal-box` with an `AlertTriangle` icon in an error-tinted circle, a card-preview block (type badge + ES/EN text), and a destructive `btn bg-error text-error-content` labeled "Eliminar". Mirrors the same `<dialog>` lifecycle pattern as `EditDialog` (derived-state `trackedId`, `useEffect` driving `showModal()`/`close()`, `cancel` DOM event wired to `onCancel`). Triggered by `setDeletingCard(card)` from the row's trash button; `onConfirm` calls `srs?.removeCard?.(deletingCard.id)` and resets state.

## Silent Multi-Device Sync

Local-first, anonymous, silent. The SRS data the user accumulates on one device silently follows them to every other device they open the app on — no accounts, no login, no email, no password, no "Sign in with Google" button.

### Architecture in one paragraph

A `syncToken` (UUIDv4, 36 chars) is the entire identity. Auto-minted on first mount of `useSyncEngine` via `crypto.randomUUID()` and persisted to `localStorage['ospinajuanp-ingles:syncToken']`. On every render the engine:

1. **Reads** from `localStorage` (UI source of truth — never from the network).
2. **Watches** the SRS `revision` counter and the theme. When either changes, **debounces** a 2 s background POST to `/api/sync/user` with the latest snapshot.
3. **Pulls** the remote snapshot on mount / token change, **merges** it with the local SRS via LWW, and calls `srs.replaceStore(merged)` + `theme.setTheme(mergedTheme)`.
4. **Flushes** any pending push synchronously (`keepalive: true`) on `visibilitychange → hidden` / `pagehide` so the last edit isn't lost.
5. **Safety-net** pushes every 5 minutes in case of races between merge + user commit.

The UI is offline-capable. No spinner on first paint, no "Connecting…" toast. The `SyncButton` shows a quiet status dot (success/warning/error) and the modal reveals the QR + token + history on demand.

### Storage schema (server side)

`ingles-db.user_sync` collection. One document per device. Unique index on `syncToken`.

```json
{
  "_id": "...",
  "syncToken": "550e8400-e29b-41d4-a716-446655440000",
  "srsStore": {
    "version": 1,
    "cards": { "<cardId>": { /* full SRS card from useSRS */ } },
    "order": ["<cardId>", ...]
  },
  "theme": "light | dark | dracula | cupcake",
  "createdAt":  1721234567890,   // server-managed, $setOnInsert
  "lastActiveAt": 1721234599999  // server-managed, $currentDate on every GET/POST
}
```

### Merge contract — Last-Write-Wins (`src/utils/syncMerge.js`)

For each card present in either side, compare:
1. `card.srs.lastReviewed` (preferred — the moment the user last graded it).
2. Fallback to `card.srs.nextReview`.
3. Fallback to `card.createdAt`.

Whichever side has the newer timestamp **wins the structural fields** (`type`, `verbKey`, `front`, `infinitivo`) and supplies the `srs` block for that card. The losing side's card is discarded (no field-level merge — LWW is all-or-nothing per card).

`order` is the **union** of both sides' arrays, preserving each side's relative order. So if local has `[A, B, C]` and remote has `[B, D, E]`, the merged order is `[A, B, C, D, E]` (stable, idempotent, order-independent of insertion history).

If both sides have never reviewed the card, ties break to **remote** (Atlas wins). This is intentional v1 behavior — a fresh device that pulls from Atlas inherits the full deck as the server sees it.

### Cross-device pairing flow

There are **three** equivalent ways to link two devices:

1. **QR code**: Device A opens the Sync modal, Device B scans the QR with its phone camera. The QR encodes a URL `https://ospinajuanp-ingles.vercel.app/?syncToken=<uuid>`. Device B lands on the URL, `consumeLinkTokenFromUrl()` reads it, `linkSyncToken(token)` writes it to B's `localStorage`, and `history.replaceState` strips the query so B's URL stays clean.
2. **Copy-paste link**: same URL is in a copyable text input under the QR. User pastes it into any browser.
3. **Manual token**: paste the raw UUIDv4 from one device's modal into the other device's "Vincular dispositivo" form. The modal's input accepts both raw tokens and full URLs.

In all three cases, **URL wins** over previously-stored token (a fresh token in the URL overrides the local one — the merge targets the right device). Bootstrap pull fires after the URL token is adopted.

### Bootstrap (silent migration)

When the engine pulls a remote snapshot and finds `state: null` (no record yet — the token was just minted), it checks `shouldPushLocal(local, null)`. If local has any cards, it fires `pushCurrent()` **immediately** (no debounce) so the next device to scan this token sees the existing deck. This is how a user who used the app offline before enabling sync gets their data to Atlas without any "Upload" button.

### Debounced push semantics

`srs.revision` (a number bumped on every `useSRS` commit + cross-tab `storage` events) and `themeApi.theme` (a string) are watched by a `useEffect`. When either changes:
- `pendingPush = true`
- a 2 s `setTimeout` is set
- on timeout, `pushCurrent()` POSTs the latest snapshot to `/api/sync/user`
- `pushCurrent()` reads directly from `localStorage` (not from React state) so it can't be stale
- the timeout is cleared if a new mutation arrives within the 2 s window

Anti-loop: when `applyRemote` calls `srs.replaceStore(merged)`, the `useSRS` `commit` bumps `revision`. If the engine's mutation-watcher effect fires synchronously on that bump, it would push the merged state right back to Atlas (wasteful round-trip). The engine guards against this with `skipNextPushRef` — set to `true` before `replaceStore`/`setTheme`, consumed and reset to `false` by the next effect run.

### Pagehide / visibilitychange flush

`visibilitychange` to `hidden` and `pagehide` both call a `flush()` that:
- reads `localStorage` directly (so it doesn't depend on React state being current)
- early-returns if there are zero cards (nothing to push)
- fires `pushCurrent()` with `keepalive: true` so the fetch survives tab close

Without this, a user who grades a card then immediately closes the tab loses up to 2 s of work.

### Safety-net interval

A 5-minute `setInterval` fires `pushCurrent()` regardless of whether anything changed. Catches edge cases like:
- a `setTimeout` was in-flight when the tab was killed (pagehide can't wait for promises).
- the merge applied a remote snapshot that overwrote a local mutation in flight.
- the user moved between WiFi networks and the previous push silently failed.

### Status states

The engine exposes `status` as one of:
- `idle` — engine mounted but no sync has happened yet.
- `pulling` — GET in flight (mount / token change / "Pull now").
- `pushing` — POST in flight (debounced timer / pagehide / safety-net / "Push now").
- `synced` — last operation succeeded.
- `lastError` is a separate field carrying the human-readable reason (`HTTP 500`, network failure, validation error, etc.). The SyncButton dot is `success` when `status === 'synced'`, `warning` when `pendingPush`, `error` when `lastError != null`.

### `forcePushNow` and `forcePullNow`

For the modal's "Sincronizar ahora" button:
- `forcePushNow()` calls `pushCurrent()` directly.
- `forcePullNow()` GETs `/api/sync/user?token=<current>`, calls `applyRemote()` if there's a state, sets status to `synced` otherwise.

### Engine API (from `useSyncEngine`)

```js
const {
  syncToken,       // string — the device's UUIDv4 identity
  status,          // 'idle' | 'pulling' | 'pushing' | 'synced' | 'error'
  lastError,       // string | null
  lastSyncedAt,    // number | null (Date.now() of last successful push/pull)
  pendingPush,     // boolean — debounce timer armed?
  linkNewToken,    // (token: string) => boolean
  unlink,          // () => void — mints a fresh token, calls linkSyncToken(new)
  forcePushNow,    // () => void
  forcePullNow,    // () => Promise<void>
} = useSyncEngine({ srs, themeApi })
```

### Dev / prod wiring

`vite.config.js` registers a second middleware at `/api/sync/user` (alongside the existing `/api/verbs/sync`) that lazy-imports `api/sync/user.js`. Same pattern as the verbs handler. In Vercel production the endpoint is hit as a real serverless function via the existing Vercel config. **No environment variables change** — `MONGODB_URI` is reused.

### What works (sync specifically)

- `npm run lint` passes clean (0 errors, 0 warnings — the engine satisfies React 19's `react-hooks/purity`, `react-hooks/set-state-in-effect`, `react-hooks/immutability`).
- `npm run build` passes clean: 1820 modules, 525 ms, ~375 KB JS / ~134 KB CSS. MongoDB driver NOT in the client bundle.
- Auto-mint on first mount: open the app, no token in `localStorage`, a UUIDv4 appears. Reload — same UUID. Open DevTools — `ospinajuanp-ingles:syncToken` is set.
- URL adoption: open `https://ospinajuanp-ingles.vercel.app/?syncToken=550e8400-e29b-41d4-a716-446655440000` — token is read, persisted, URL is stripped (`history.replaceState`), engine fires a bootstrap pull.
- Bootstrap push: visit `/v1/verbs/accept` (creates an SRS card), then in another tab trigger a GET with your token — the card is there.
- LWW merge verified in Node: two `mergeSRSStores` calls with one side having a fresher `lastReviewed` on each card yield the expected winner per card; `order` union is stable.
- Debounce + pagehide: grade a card, immediately close the tab — Atlas has the new SRS state within ~50 ms (keepalive fetch).
- Cross-tab: open two tabs of the same app, grade a card in tab A. Tab B's `useSRS` `storage` listener updates its UI in real time, AND the engine's `useEffect` fires `pushCurrent()` (srs.revision bumped by the storage listener). Tab B's UI shows the new card immediately; Atlas gets the same payload a few ms later.
- QR fallback: `<img onError>` swaps to a copyable URL block if `api.qrserver.com` is blocked / offline. No broken image, no dead-end.

## Multi-theme (DaisyUI 5)

Theming lives at the `<html data-theme="...">` level. Active themes: `light` (default), `dark`, `dracula`, `cupcake`. Tailwind v4 has no `tailwind.config.js`; DaisyUI is injected as a CSS plugin in `src/index.css`:

```css
@import "tailwindcss";
@plugin "daisyui" { themes: light --default, dark, dracula, cupcake; }
```

### Storage + application
- `localStorage['ospinajuanp-ingles:theme']` holds the active theme id. `useTheme()` (in `src/hooks/useTheme.js`) reads it on mount, validates against `THEMES`, falls back to `light`, and persists every change.
- `useEffect(() => { document.documentElement.setAttribute('data-theme', theme); localStorage.setItem(STORAGE_KEY, theme) }, [theme])`.
- **FOUC prevention**: a tiny inline `<script>` in `index.html` runs BEFORE React boots and applies the persisted theme to `<html>`. Without this, users with a non-default theme see one frame of the default theme on each load.

### What uses DaisyUI tokens
- **Everything in the app** is theme-aware as of `a08442b`. The slate/indigo palette was a leftover from the pre-theming days; the entire UI now re-skins when the user changes the theme.
- **`src/pages/HomePage.jsx`** — fully themable page. `bg-base-200` (hero surface), `bg-base-100` + `border-base-300` (cards), `text-base-content` (titles/captions), `btn-primary` / `btn-outline btn-primary` (CTAs), `badge-primary badge-outline` (eyebrow chip).
- **`src/components/ThemeSwitcher.jsx`** — dropdown trigger + menu both adapt: `bg-base-100`, `border-base-300`, active row uses `bg-primary/15 text-primary`.
- **`src/components/ShellHeader`** in `App.jsx` — sticky header now `bg-base-100/85 backdrop-blur-md` with `border-base-300`. The brand title uses `text-base-content`, subtitle `text-base-content/60`.
- **`src/components/{SearchBar, CategoryFilter, NavButtons, ReviewNavButton, ConjugationGrid, SentencePill, AddFlashcardForm, Flashcard, AudioButton, VerbCard}.jsx`** — every interactive surface, card, divider, and text uses `bg-base-100 / bg-base-200 / bg-base-300` and `text-base-content / text-base-content/70 / text-base-content/50` so they swap with the active theme.
- **`src/components/SRSStudyPage.jsx`** — page chrome, stats grid, and "all caught up" success card adapt.

### Token mapping (slate/indigo → daisyUI semantic)
| Before | After | Where it appears |
|---|---|---|
| `bg-white` | `bg-base-100` | card surfaces (VerbCard, Flashcard front, Stat, AddFlashcardForm, etc.) |
| `bg-slate-50 / 100` | `bg-base-200` | page bg, soft surfaces, pulse placeholders, hover states |
| `border-slate-200 / 100` | `border-base-300` | dividers + outlines |
| `text-slate-900 / 800` | `text-base-content` | primary text |
| `text-slate-700 / 600` | `text-base-content/80` | secondary text |
| `text-slate-500 / 400` | `text-base-content/70` | muted text |
| `text-slate-300` | `text-base-content/50` | placeholder text |
| `text-indigo-600 / 700` | `text-primary` | brand text (verb name, active states) |
| `bg-indigo-600 / 700` | `bg-primary` | CTAs (Next button, Submit, Reintentar) |
| `bg-indigo-50 / 100` | `bg-primary/10 .. /15` | chips, hover states |
| `border-indigo-200 / 300` | `border-primary/30 .. /40` | active borders |
| `bg-slate-900` (Next btn) | `btn btn-primary` | high-contrast CTA now uses DaisyUI |
| `bg-slate-900/95` (image max) | `bg-black/95` | image maximize backdrop kept black |
| `bg-slate-900/30..70` (overlay) | `bg-black/30..70` | image darkening overlay kept dark |

### Semantic colors KEPT (intentional)
- **`Flashcard` 4 grade buttons**: fail / hard / good / easy mapped to `error` / `warning` / `success` / `info` (semantic DaisyUI tokens). These carry meaning across themes.
- **Image overlays** (`bg-black/30..70`, `bg-black/95`): always dark for image contrast.
- **`AudioButton`** background: `bg-base-100/95` (theme-aware) with `text-primary` for contrast on top of the image overlay. In dark themes the button blends slightly with the image's dark overlay — acceptable trade-off, can be hardened later if user feedback requires.
- **`HeroIllustration`** SVG: hardcoded amber/sky palette is artistic and stays as-is across all themes.

### DaisyUI v5 gotchas (this codebase)
- DaisyUI's reset is light (it does not include Tailwind's preflight by itself), so our existing `@layer base` rules keep working.
- DaisyUI 5 themes use OKLCH color tokens (`--color-base-100`, `--color-primary`, etc.). Any element using `bg-base-100`, `text-base-content`, `btn-primary` re-skins automatically when the user switches themes.
- DaisyUI's `dropdown` requires the trigger to be the first child with `tabindex=0` and `role=button` (or a `<button>`). `ThemeSwitcher` uses a `<div tabIndex={0} role="button">` trigger and a `<ul tabIndex={0} class="menu dropdown-content">` panel — exact structure DaisyUI expects.
- `dropdown-content` panels sit at `z-50` so they overlay the sticky header.
- DaisyUI's `.menu` adds `margin-inline-end: 4px` to buttons inside the menu — fine for our use, the `mx` is on the `card-actions` containers instead of inside the menu.
- `btn-primary` needs `btn` to come first — DaisyUI's `btn` class supplies the base height, padding, border-radius, focus ring, etc. `btn-primary` only adds the color variant. In `NavButtons.jsx` the Next button uses `btn btn-primary inline-flex size-12 min-h-0 p-0` so we override `btn`'s default min-height to fit the 48×48 circle.

## Atlas indices (current)

### `ingles-db.verbos`
- `_id_` (default)
- `id_unique` on `{id: 1}` — unique
- `last_seen_desc` on `{ultima_vez_visto: -1}` — for "recently viewed" queries

NO `infinitivo.ing` index. Dataset has ~95 duplicate ing values (e.g. `rewrite`, `analyze`, `check`) which would break `ing_unique` with E11000.

### `ingles-db.user_sync` (sync engine)
- `_id_` (default)
- `syncToken_unique` on `{syncToken: 1}` — unique. Enforces one doc per device.
- `lastActive_desc` on `{lastActiveAt: -1}` — for "recently active" queries / admin dashboards.

Payload-size guard at the handler: `srsStore` ≤ 256 KB (early `413`). Theme whitelist: `{light, dark, dracula, cupcake}`.

## MongoDB query recipes
```js
// Total
db.verbos.countDocuments({})                                  // 1000

// By migration source
db.verbos.countDocuments({ migrado_desde: 'SPA_Bulk_Migration' })   // 1000 (initial state)
db.verbos.countDocuments({ migrado_desde: 'SPA_Lazy_Migration' })   // grows with visits

// Multimedia enrichment state
db.verbos.countDocuments({ audio_source: 'pending' })         // audio not yet resolved
db.verbos.countDocuments({ audio_source: 'dictionaryapi.dev' }) // enriched audio
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

## Icons (lucide-react)

All UI icons come from **`lucide-react@1.25.0`** (tree-shakeable, ESM, React 19 ready). 28 hand-rolled SVGs were replaced across 12 files. SVG literals appear only in two places that are NOT icons:
- `src/components/HeroIllustration.jsx` — artistic landscape behind the verb hero image.
- `public/favicon`, brand `<img>` in ShellHeader — static asset, not an icon.

### Per-theme icons (THEME_ICONS map)

Defined in `src/hooks/useTheme.js` and exposed via `useTheme().themeIcons`:

| Theme    | Icon       | Lucide category            |
|----------|------------|---------------------------|
| light    | `Sun`      | accessibility / weather   |
| dark     | `Moon`     | accessibility             |
| dracula  | `Skull`    | gaming                    |
| cupcake  | `Cake`     | food-beverage / social    |

**ThemeSwitcher trigger** renders the icon for the currently active theme (changes on switch: Sun ↔ Moon ↔ Skull ↔ Cake). Each dropdown row renders its own icon next to the label plus a `Check` for the active row. The trigger falls back to `themeIcons.light` (Sun) if a theme id has no entry.

To add a new theme: import the icon from `lucide-react`, add an entry in `THEME_ICONS`, add the entry to `THEMES` with `{ id, label }`.

### Icon inventory (per file)

| File                              | Lucide icons used |
|-----------------------------------|---|
| `src/App.jsx`                     | `TriangleAlert` (ErrorState) |
| `src/components/ReviewNavButton.jsx` | `RotateCw` |
| `src/components/SearchBar.jsx`    | `Search`, `X` |
| `src/components/CategoryFilter.jsx` | `SlidersHorizontal`, `ChevronDown`, `RotateCcw`, `Check` |
| `src/components/NavButtons.jsx`   | `ChevronLeft`, `ChevronRight`, `Dices` |
| `src/components/AudioButton.jsx`  | `Loader2`, `Pause` (filled), `VolumeX`, `AlertCircle`, `Play` (filled) |
| `src/components/Flashcard.jsx`    | `X`, `HelpCircle`, `Check`, `Star` (4 grade buttons) |
| `src/components/ConjugationGrid.jsx` | `Eye`, `EyeOff`, `Lightbulb` |
| `src/components/SentencePill.jsx` | `Eye`, `EyeOff` |
| `src/components/VerbCard.jsx`     | `Maximize2`, `Minimize2`, `Loader2`, `Camera`, `SearchX` (overlay buttons + EmptyState) |
| `src/components/ImageCredit.jsx`  | `Camera` |
| `src/components/AddFlashcardForm.jsx` | `X`, `Plus` |
| `src/components/ThemeSwitcher.jsx` | (uses `themeIcons` map + `Check`) |
| `src/pages/HomePage.jsx`          | `Sparkles`, `LayoutGrid`, `ArrowRight` |
| `src/pages/SRSStudyPage.jsx`      | `ArrowLeft`, `Plus`, `CheckCircle2` |

### Pattern

```javascript
import { IconName, OtherIcon } from 'lucide-react'

// Class-driven sizing + color (inherit currentColor):
<IconName className="size-5 text-primary" aria-hidden="true" />

// Filled variants (Play, Pause) explicitly opt in:
<Pause fill="currentColor" className="size-5" aria-hidden="true" />
```

Lucide default `stroke-width="2"`. The 4 Flashcard grade buttons get `stroke-width="2.25"` to look slightly bolder at small sizes (3.5 in the sm+ layout). All other icons use Lucide defaults.

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

## Vercel deployment

Repo auto-deploys on push to `main`. The production URL is `https://ospinajuanp-ingles.vercel.app/`.

**Required env vars in Vercel Dashboard → Settings → Environment Variables** (all three envs: Production, Preview, Development):
- `VITE_PEXELS_API_KEY`
- `VITE_PEXELS_API_KEY_2`
- `MONGODB_URI`

**Env vars do NOT auto-trigger a redeploy**. After adding them, force one via Deployments → ⋮ → Redeploy, or push an empty commit.

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

## Session commit log

```
(this session)
3539a89 feat(sync): silent local-first multi-device sync engine   (this commit)
  Anonymous UUIDv4 syncToken (auto-minted, persisted in localStorage)
  lets the same SRS deck follow the user across devices with no login,
  no email, no signup modal.

  Storage & identity
  - ospinajuanp-ingles:syncToken holds the 36-char UUIDv4
  - crypto.randomUUID() with crypto.getRandomValues/Math.random fallback
  - QR-code pairing + ?syncToken=… URL adoption (consumed and stripped
    on mount via history.replaceState)
  - Manual paste accepts either a raw UUIDv4 or a full URL

  Backend
  - New serverless api/sync/user.js handler
  - GET upserts lastActiveAt via findOneAndUpdate, returns state:null
    for a fresh token
  - POST upserts {syncToken, srsStore, theme} with $setOnInsert:createdAt
    and $currentDate:lastActiveAt, idempotent
  - New Atlas collection ingles-db.user_sync with syncToken_unique and
    lastActive_desc indices
  - Validators: UUIDv4 regex, theme whitelist
    (light/dark/dracula/cupcake), srsStore.version===1, payload ≤ 256 KB
  - Vite dev middleware at /api/sync/user mirrors the existing
    /api/verbs/sync pattern

  Engine (src/hooks/useSyncEngine.js)
  - One instance per app, lives in Root alongside useSRS
  - Pulls remote snapshot on mount + token change
  - Debounced 2s background push on srs.revision / theme change
  - Pagehide/visibilitychange flush with keepalive:true (last edit
    survives tab close)
  - 5-minute safety-net push catches races between merge + commit
  - Bootstrap push: when remote is empty but local has cards, push
    immediately (no debounce) so the next device to scan the token
    sees the existing deck
  - skipNextPushRef avoids the round-trip push right after a remote
    merge bumps srs.revision

  Merge (src/utils/syncMerge.js)
  - Pure Last-Write-Wins per card: compare srs.lastReviewed, fall back
    to srs.nextReview, then card.createdAt
  - Winner supplies type/verbKey/front/infinitivo + srs block
  - order is the union preserving each side's relative order
  - Tie-breaker: remote wins

  UI
  - SyncButton in the header (next to ThemeSwitcher, hidden on mobile)
    with a status dot: success/warning/error
  - SyncModal is a DaisyUI v5 <dialog> with QR (api.qrserver.com with
    onError fallback to copyable URL), token + URL copy buttons, link
    input form, danger-zone Desvincular
  - Status badge ticks every 30s via setInterval (avoids Date.now()
    during render to satisfy react-hooks/purity)
  - Form-field reset uses the adjusting-state-during-render pattern

  useSRS additions
  - revision counter bumped on every commit and on cross-tab storage
    events (engine watches this to trigger pushes)
  - replaceStore(newStore) action for engine injection of merged state
    (suppresses the auto-push via skipNextPushRef)

  Build impact: 1820 modules, ~375 KB JS / ~134 KB CSS raw. No new
  npm deps (crypto.randomUUID native, QR via external API). MongoDB
  driver still NOT in the client bundle.

  Lint clean (React 19 purity rules respected), build clean.
8e801ba fix(srs+header): restructure /v1/test top + hide Repaso pill outside verbs
  App.jsx
  - ReviewNavButton in ShellHeader now renders only when
    isVerbRoute (pathname.startsWith('/v1/verbs')), same gate as
    SearchBar + CategoryFilter. ThemeSwitcher stays always.
  - Effect: visiting /v1/test no longer shows a 'Repaso' pill in
    the header that points to the page the user is already on.
  SRSStudyPage.jsx
  - Restructured the top region into three layers:
    1. Back button (small rounded pill, text-xs) at top-left, above
       the title container.
    2. Title container (border-b border-base-300 pb-5 mb-6):
       - Left: 'Repaso espaciado' h1 + subtitle (study/manage copy).
       - Right: ModeToggle (Estudiar / Gestionar Mazo), aligned to
         sm:justify-end.
    3. Content (stats grid + form + cards OR DeckManager).
  - 'Volver a verbos' button removed from the title row (replaced by
    the compact 'Volver' pill at the top-left).
  - ModeToggle stays as a DaisyUI join group with the same BookOpen /
    ListFilter icons; only the surrounding layout changed.
f5b1da5 docs(handoff): record DeckManager + editCustomCard (3f3506f)
3f3506f feat(srs): DeckManager + editCustomCard + Estudiar/Gestionar toggle
    - useSRS.js: editCustomCard(cardId, {es,en}) preserves SRS state
    - DeckManager.jsx: table + search + pagination + edit modal
    - SRSStudyPage.jsx: ModeToggle join group (BookOpen/ListFilter)
  feat(icons): migrate 28 hand-rolled SVGs to lucide-react + per-theme icons
    - pnpm add lucide-react@1.25.0
    - useTheme.js exports THEME_ICONS map (Sun/Moon/Skull/Cake)
    - ThemeSwitcher: trigger becomes contextual (renders active theme's
      icon), each dropdown row gets its theme's icon + Check for active
    - All inline SVGs in App.jsx + 11 components + 2 pages replaced
    - Flashcard grade buttons use Icon field in GRADE_BUTTONS array
    - AudioButton Play/Pause kept filled (fill="currentColor")
  feat(header): brand icon + title are a link to / (HomePage) (predecessor)
e5ecff1 docs(handoff): record whole-app daisyUI theming + token mapping table
a08442b feat(theme): apply daisyUI tokens across all components (whole-app theming)
  fix(theme): apply daisyUI tokens across all components (whole-app theming)
    - body bg-base-200 / text-base-content
    - ShellHeader bg-base-100/85 + border-base-300
    - VerbCard wrapper + sections + EmptyState themed
    - Flashcard front (bg-base-100) + back (primary gradient)
    - Flashcard 4 grade buttons: error/warning/success/info semantic
    - SRSStudyPage stats + empty states (success/* for "al día")
    - AddFlashcardForm + textarea-bordered
    - CategoryFilter dropdown + rows + trigger
    - SearchBar, NavButtons, ConjugationGrid, SentencePill, AudioButton
    - ErrorState: border-error/30 + bg-error/10
  feat(routing+theme): namespace /v1 + landing page + DaisyUI multi-theme (predecessor)
33d4039 docs(handoff): record /v1 namespace + DaisyUI multi-theme + landing page
6b7957a docs(handoff): record c5f5bda as last commit
c5f5bda feat(srs): SM-2 spaced repetition module at /repaso (predecessor)
ba78609 docs(handoff): record c5f5bda as last commit
634a6a0 cleanup: remove diagnostic console.info logs after confirmed fix
6ec80c1 fix(sync): use == null instead of !id for id guard        (this session)
f19a551 fix(verb-card): combine verbKey + renderId as key         (this session)
52bf3e4 fix(verb-card): wrap VerbImage in key-bound div           (this session)
7200cb9 fix(verb-image): derived-state sync + diagnostic logs    (this session)
24172a2 fix(verb-card): add key={verbKey} to VerbImage            (this session)
a31d0ef fix(vercel): add SPA fallback rewrite                    (this session)
34950c4 debug(audio+sync): add console.info logs                  (this session)
4406410 fix(audio): eager-resolve audio on mount                  (this session)
49c8523 docs(handoff): document MongoDB bulk migration
593b128 feat(bulk): 1000-verb bulk migration to MongoDB
9e44b5c feat(sync): mark lazy-migrated docs
c1f6584 fix(vite): expose MONGODB_URI via loadEnv
```

## Open / parked
- **SRS verb-dedup hardening (deferred, Opción B not implemented)**: the existing `registerVerb` lookup uses `store.cards` from React closure, which could in theory lag behind `localStorage` under rapid re-renders (StrictMode double invoke) or cross-tab races. Plan B was to (1) read `localStorage` directly inside `registerVerb` and (2) make `commit` itself reject duplicate verbKeys before write. NOT IMPLEMENTED — current code is correct for normal user flows; revisit only if duplicates ever appear in production data.
- **Drop the legacy verb-route redirect** (`/:verbSelector` → `/v1/verbs/<slug>`): now that the new namespace has been live for one or two deploys, the legacy catch-all can be removed in a follow-up. Until then it silently rewrites old bookmarks so users don't 404.
- **DaisyUI scope creep**: HomePage + ThemeSwitcher are the only themable surfaces today. Opting in additional components (VerbCard, Flashcard, SRSStudyPage) is straightforward but each component needs a visual review because the slate/indigo palette was hand-tuned and DaisyUI's `base-100` / `primary` tokens will look different.
- **Sync conflict-resolution is all-or-nothing LWW per card** (not field-level). If a user grades card X on Device A and edits its Spanish text on Device B offline, the grading on A wins the entire card (including the new Spanish text). Acceptable for v1 because edits to `type/verbKey/front/infinitivo` are rare (custom-card edit only); grading is the dominant mutation and carries a fresher timestamp. If users start complaining about "I edited my custom card and the change disappeared", we'd need either (a) field-level merge with per-field timestamps or (b) detecting "edit vs review" intent and giving edits higher priority.
- **Sync pushes always include the entire SRS store** (current deck size × card size). At ~100 cards this is ~30 KB raw / ~6 KB gzipped — fine. If users accumulate 1000+ cards, the 256 KB cap becomes a concern; could add per-page POST (`PATCH /api/sync/user` with `{added, modified, removed}` deltas) but the LWW semantics get significantly more complex.
- **No offline-write queue**: if the network is down, mutations are still pushed (fail silently with a `console.warn`). The next time the page loads (or the 5-min safety-net fires), the local state is re-pushed. If the user keeps grading cards while offline, the local state is always the source of truth — Atlas eventually catches up. NOT implemented: a real outbox with retry/backoff. Acceptable for v1 because the safety-net + pagehide flush cover 99% of cases.
- **No account migration path**: a `syncToken` is forever. There's no "merge with another account" or "migrate to a different token". If a user clears their browser data, they lose their token AND the next device to scan that token sees an empty Atlas record — but their LOCAL data on that cleared device is still there (the engine will bootstrap-push it under a new token). So data isn't actually lost, just orphaned in Atlas under the old token.
- Likely next candidates:
  - **Remove static JSON read**: switch `useVerbos` to fetch verbs from MongoDB instead of `/verbos_estructura.json`. Requires adding `GET /api/verbs` (with pagination or full dump).
  - **Proactive enrichment**: background Pexels/Free-Dictionary enrichment of bulk-seeded docs (`audio_source: 'pending'`) so all 1000 are fully enriched before lazy visits.
  - **SRS card animations**: add haptic/animation feedback (green flash on correct, red on wrong) and humanized "próxima: mañana / en 3 días / en 2 meses" labels.
  - **`VerbProvider` lift**: optional symmetry move to `Root` (currently lives inside `<App>`); see the SRS module section.
  - **Register all 95 duplicate-`ing` verbs**: today's `resolveVerb` returns only the first match, so `/v1/verbs/rewrite` only ever registers one of several ids sharing that ing. If we want every id-with-same-ing to become a distinct SRS card, change `verbKey` to `id:${id}` always (already preferred when id exists) and pro-actively walk the dataset after mount to register all.
  - **DaisyUI build cost**: 4 themes ship ~64 KB extra CSS. If we ship only 2 (e.g. `light --default, dark`), CSS drops to ~80 KB. Revisit when bandwidth matters more than theme variety.
  - **Self-hosted QR generation**: today we depend on `api.qrserver.com` for the QR PNG. If that goes down (or returns ugly branding), the modal falls back to a copyable URL block. A fully self-hosted alternative would be `qrcode` npm (~30 KB, tree-shakeable to ~10 KB) — only worth doing if QR branding becomes a UX issue.
  - **Sync metrics**: log push/pull counts + payload sizes to `ingles-db.sync_events` for an admin dashboard. Useful for understanding real usage patterns (how often do users grade on multiple devices per day?).