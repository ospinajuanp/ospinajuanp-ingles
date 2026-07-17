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
- Image cache is `Map<word, photo[]>` in `src/utils/imageCache.js`; refresh button cycles Pexels pages by popping the head.
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
pnpm dev
# or
pnpm build && pnpm preview
```
