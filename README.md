# Verbos en Inglés

A modern single-page web app for learning English verbs in Spanish.
Browse 1,000 weighted verbs with full conjugations (past, participle,
gerund, future, conditional), six contextualized example sentences
per verb, on-demand pronunciation audio pulled from the free
[Dictionary API](https://dictionaryapi.dev/), a **SM-2 spaced
repetition** module with 3D-flip flashcards at `/v1/test`, a
**multi-theme** UI (light / dark / dracula / cupcake), and lazy
sync of every visit to **MongoDB Atlas**.

![Verbos en Inglés](public/icon.ico)

## Features

- **Landing page + namespaced routes** — `/` shows a hero with two
  cards (Explorar Verbos / Repasar). Verbs live under `/v1/verbs/:verbSelector`
  (digits or slug, case-insensitive). Spaced-repetition study is at
  `/v1/test`. Old `/repaso` and `/<slug>` URLs still work as legacy
  redirects so bookmarks don't break.
- **Weighted-random verb exploration** — A dice button (and a
  landing-page CTA) rerolls the lottery without reloading. Buckets:
  ≤ 10 (50 %), 10.1–500 (30 %), 500.1–1000 (20 %).
- **Six full conjugations** — Pasado, Participio, Gerundio, Futuro,
  Condicional for every verb in the dataset.
- **Contextual sentences** — Each verb ships with one example
  sentence per tense slot (infinitivo, pasadoSimple, participio,
  gerundio, futuro, condicional) across six pronouns (yo, tu,
  él/ella, ellos, nosotros, eso).
- **Progressive disclosure** — Spanish translations are blurred by
  default and revealed on hover (desktop) or tap (mobile), forcing
  the learner to try translating the English first.
- **Pronunciation audio** — A centered play button on the hero image
  fetches the first audio URL from the Free Dictionary API and
  plays it. Falls back to the browser's `SpeechSynthesis` API when
  the Free Dictionary entry has no recording. Results are cached in
  memory; the whole image area is the touch target.
- **Hero images** — Curated photos from the [Pexels API](https://www.pexels.com/api/)
  land on each verb with proper photographer attribution. Optional:
  set `VITE_PEXELS_API_KEY` in `.env`. Without a key the app uses
  deterministic [Picsum](https://picsum.photos) images and finally
  the inline SVG forest illustration. Dual-key rotation
  (`VITE_PEXELS_API_KEY` + `VITE_PEXELS_API_KEY_2`) handles rate
  limits automatically.
- **Real-time search + filters** — Filter by category
  (Generales / Tecnología) and subcategory (Simples / Irregulares
  / Compuestos). Search matches both English infinitives and
  Spanish meanings.
- **SM-2 spaced repetition at `/v1/test`** — Two decks coexist in a
  single study queue: **Mazo Personalizado** (user-added sentences
  via `AddFlashcardForm`) and **Mazo de Verbos Vistos** (verbs
  auto-registered when visited). 3D-flip flashcards, 4-level
  grading (Otra vez / Difícil / Bien / Fácil). Schedule persisted
  to `localStorage` under `ospinajuanp-ingles:srs:v1` — fully
  offline, no backend. Re-visits never duplicate a card.
- **Deck Manager** — A `ModeToggle` join group on `/v1/test` switches
  between Estudiar and Gestionar Mazo. The manager is a DaisyUI
  table with real-time search across both languages, 10/page
  pagination with numeric shortcuts + ellipsis gaps, edit (custom
  cards via a native `<dialog>`) and delete (any card, with
  confirm). Editing a custom prompt preserves the SRS schedule.
- **Multi-theme UI** — Light / dark / dracula / cupcake via DaisyUI 5.
  Theme persists to `localStorage['ospinajuanp-ingles:theme']`; an
  inline `<script>` in `index.html` applies the persisted theme to
  `<html data-theme>` before React mounts, so dark-mode users see no
  flash of light theme on reload.
- **MongoDB Atlas sync** — A tiny serverless endpoint at
  `/api/verbs/sync` upserts every visited verb into
  `ingles-db.verbos` (atomic `findOneAndUpdate` with `$set` +
  `$setOnInsert` + `$inc` + `$currentDate`). One-shot bulk scripts
  (`pnpm bulk:direct` / `pnpm bulk:migrate`) seed all 1,000 verbs.
- **Mobile-first** — Responsive from 320 px up. Swipe horizontally
  on the card to navigate between verbs. Touch targets stay in
  the thumb zone. `<kbd>←</kbd> / <kbd>→</kbd>` on desktop.
- **Accessibility** — Honors `prefers-reduced-motion`, full keyboard
  navigation, ARIA labels on every interactive element, semantic
  roles for the conjugation/sentence cards.
- **Live data sync** — Edit `verbos_estructura.json` at the repo
  root and Vite hot-reloads the running dev server automatically
  (no manual copy into `public/`).

## Tech stack

- **React 19** with strict mode + concurrent rendering
- **Vite 8** for dev server and production build
- **React Router DOM 7** for namespaced `/v1` routing + legacy redirects
- **Tailwind CSS v4** via `@tailwindcss/vite` (no config file, CSS-first
  theme via `@theme` in `src/index.css`)
- **DaisyUI 5** for theme tokens (`bg-base-100`, `text-base-content`,
  `btn-primary`, `dropdown`, `modal`, `table`, `join` …)
- **lucide-react** for every UI icon (28 hand-rolled SVGs retired)
- **Free Dictionary API** for pronunciation audio
- **MongoDB Atlas** via the official `mongodb` driver — lazy sync on
  every visit + bulk-migration scripts
- ESLint 9 with flat config + `eslint-plugin-react` /
  `eslint-plugin-react-hooks` / `eslint-plugin-react-refresh` (forbids
  `setState` inside `useEffect` — use derived-state pattern instead)

State is split across two React contexts: `VerbProvider` (verb list,
filters, navigation) and `SRSProvider` (spaced-repetition store, one
instance at the app root). Everything else is local component state.

## Requirements

- **Node.js ≥ 20** (the project is built and tested on v24).
- **pnpm** (recommended). npm or yarn also work.
- **Pexels API key(s)** (optional, for curated photos per verb).
  Free tier: 200 requests/hour, 20,000/month. The app supports up to
  two keys — `VITE_PEXELS_API_KEY` and `VITE_PEXELS_API_KEY_2` —
  and automatically rotates to the second when the first returns
  401 / 403 / 429 / 5xx or a network error. Set up two free Pexels
  accounts for higher volume. Without any key the app falls back to
  Picsum + inline SVG.
- **MongoDB Atlas connection string** (`MONGODB_URI`, server-side
  only) for the `/api/verbs/sync` lazy endpoint and the bulk
  migration scripts. Without it the app still works — it just won't
  persist visits to the database.

## Installation

```bash
git clone https://github.com/ospinajuanp/ospinajuanp-ingles.git
cd ospinajuanp-ingles
pnpm install
cp .env.example .env       # then paste your Pexels key(s) (optional)
```

### Optional: configure Pexels for verb hero images

1. Sign up for a free key at <https://www.pexels.com/api/>.
2. Open `.env` and paste your key after `VITE_PEXELS_API_KEY=`.
3. (Optional) For higher volume, create a second Pexels account and
   paste its key after `VITE_PEXELS_API_KEY_2=`. The app will use the
   primary and fall back to the secondary automatically.
4. Restart `pnpm dev`. The first time you visit a verb, the app
   fetches a curated photo from Pexels and caches it in memory
   (see `src/utils/imageCache.js`). Subsequent visits are
   instant.

Without any key, verbs show Picsum images (deterministic per word)
or the inline forest-path SVG.

## Usage

### Development server

```bash
pnpm dev
```

Opens on `http://localhost:5173` (Vite default). Edits to
`src/**` hot-reload instantly. Edits to `verbos_estructura.json`
trigger a full reload so the new data appears immediately.

### Production build

```bash
pnpm build
```

Outputs static assets to `dist/`. The Vite `syncDataPlugin`
ensures the latest `verbos_estructura.json` is copied into
`dist/` at build time, and `public/icon.ico` is also copied.

### Preview the build

```bash
pnpm preview
```

Serves `dist/` for a quick local sanity check.

### Lint

```bash
pnpm lint
```

## Project structure

```
.
├── index.html                       # Vite entry + FOUC-prevention theme script
├── vite.config.js                   # Plugins: react + tailwind + sync-data
├── eslint.config.js                 # Flat config (react, hooks, refresh + node)
├── vercel.json                      # SPA fallback rewrite for /(?!api/)
├── package.json
├── pnpm-lock.yaml
├── public/
│   ├── icon.ico                     # Favicon + brand logo (256×256)
│   └── verbos_estructura.json      # Copied from root at build/dev time
├── verbos_estructura.json           # Authoritative dataset (gitignored)
├── api/
│   └── verbs/
│       └── sync.js                  # Serverless /api/verbs/sync handler (MongoDB upsert)
├── scripts/
│   ├── bulk-direct.mjs              # MongoClient.bulkWrite() — 1s for 1000 verbs
│   └── bulk-migrate.mjs             # HTTP POSTs to /api/verbs/sync — smoke test only
├── src/
│   ├── main.jsx                     # React root + Root component (single useSRS)
│   ├── App.jsx                      # Shell + ShellHeader + Routes + verb filter
│   ├── index.css                    # Tailwind import + DaisyUI plugin + @theme
│   ├── contexts/
│   │   ├── VerbContext.jsx          # VerbProvider + useVerbosContext()
│   │   └── SRSContext.jsx           # SRSProvider + useSRSContext()
│   ├── pages/
│   │   ├── HomePage.jsx             # Landing page (/): DaisyUI hero + 2 cards
│   │   ├── VerbView.jsx             # /v1/verbs/:verbSelector (the verb flashcard)
│   │   └── SRSStudyPage.jsx         # /v1/test — SRS session + ModeToggle + DeckManager
│   ├── components/
│   │   ├── AddFlashcardForm.jsx     # ES/EN form for custom SRS cards
│   │   ├── AudioButton.jsx          # Free Dictionary API audio player (forwardRef)
│   │   ├── CategoryFilter.jsx       # Dropdown for category / subcategory filters
│   │   ├── ConjugationGrid.jsx      # 3-col grid with reveal-on-hover
│   │   ├── DeckManager.jsx          # Table + search + pagination + edit dialog
│   │   ├── Flashcard.jsx            # 3D-flip card + 4 grade buttons
│   │   ├── HeroIllustration.jsx     # Inline-SVG forest-path fallback
│   │   ├── ImageCredit.jsx          # Pill attribution for Pexels photos
│   │   ├── LegacyVerbRedirect.jsx   # /:verbSelector → /v1/verbs/<slug>
│   │   ├── NavButtons.jsx           # Prev / counter / next / shuffle
│   │   ├── ReviewNavButton.jsx      # Header pill → /v1/test with due-count badge
│   │   ├── SearchBar.jsx            # Live filter input
│   │   ├── SentencePill.jsx         # Sentence card with blur reveal
│   │   ├── ThemeSwitcher.jsx        # DaisyUI dropdown for the 4 themes
│   │   └── VerbCard.jsx             # The main flashcard + swipe gesture
│   ├── hooks/
│   │   ├── useSRS.js                # Single-instance SRS store (localStorage)
│   │   ├── useTheme.js              # Theme persistence + DaisyUI THEME_ICONS map
│   │   └── useVerbos.js             # URL-driven verb list, filters, navigation
│   └── utils/
│       ├── audioCache.js            # In-memory cache of resolved audio URLs
│       ├── flatten.js               # Walk nested JSON → flat array
│       ├── imageCache.js            # In-memory cache of Pexels photos (localStorage)
│       ├── mongoSync.js             # Fire-and-forget fetch to /api/verbs/sync
│       ├── pexels.js                # fetchPexelsPhoto() with dual-key rotation
│       ├── srs.js                   # Pure SM-2 functions (calculateNextReview, isDue, …)
│       ├── tips.js                  # Rotating conjugation tips (Spanish glossing)
│       └── weightedRandom.js        # 50 / 30 / 20 lottery
└── GUIA_ESTILO.md                   # Spanish guide for filling the JSON
```

## Data model

`verbos_estructura.json` is the source of truth. It looks like:

```json
{
  "generales": {
    "simples":     [ /* verb objects */ ],
    "irregulares": [ /* verb objects */ ],
    "compuestos":  [ /* verb objects */ ]
  },
  "tecnologia":   [ /* verb objects */ ]
}
```

Each verb:

```json
{
  "id": 0,
  "imagen": "https://example.com/forest.jpg",
  "infinitivo":   { "esp": "aceptar",  "ing": "accept" },
  "pasadoSimple": { "esp": "aceptó",   "ing": "accepted" },
  "participio":   { "esp": "aceptado", "ing": "accepted" },
  "gerundio":     { "esp": "aceptando","ing": "accepting" },
  "futuro":       { "esp": "aceptará", "ing": "will accept" },
  "condicional":  { "esp": "aceptaría","ing": "would accept" },
  "oraciones": {
    "infinitivo":   { "pronombre": "yo",       "ing": "I accept the proposal.",         "esp": "Yo acepto la propuesta." },
    "pasadoSimple": { "pronombre": "tu",       "ing": "You accepted the challenge.",     "esp": "Tú aceptaste el desafío." },
    "participio":   { "pronombre": "el_ella",  "ing": "She has accepted the invitation.", "esp": "Ella ha aceptado la invitación." },
    "gerundio":     { "pronombre": "ellos",    "ing": "They are accepting the terms.",    "esp": "Ellos están aceptando los términos." },
    "futuro":       { "pronombre": "nosotros", "ing": "We will accept the decision.",     "esp": "Nosotros aceptaremos la decisión." },
    "condicional":  { "pronombre": "eso",      "ing": "It would accept the configuration.","esp": "Eso aceptaría la configuración." }
  }
}
```

### Adding or updating verbs

1. Edit `verbos_estructura.json` directly **or** run `python3
   llenar_verbos.py` to generate it (the script in this repo builds
   the dataset semi-automatically).
2. If `imagen` is empty, the app falls back to an inline SVG
   forest illustration, and on `<img onError>` to a deterministic
   Picsum URL seeded with the verb's English name.
3. Verbs whose `infinitivo.ing` is empty are silently ignored — no
   error, no broken UI.
4. The dev server auto-syncs the file into `public/` and reloads.

See [`GUIA_ESTILO.md`](./GUIA_ESTILO.md) for content-writing
conventions (pronoun per slot, translation naturalness, etc.).

## Weighted random selection

`src/data/weightedVerbs.js` is the weighted list. Each entry is
`{ verb: 'be', weight: 0.0 }`. The first occurrence of each base
form wins, so `run` (21.8) takes precedence over `run` (142.1),
`work` (7.3) over `work` (757.0), etc.

`src/utils/weightedRandom.js` implements the lottery:

| Bucket | Weight range | Probability |
|---|---|---|
| **A** | `≤ 10.0`  | 60 % |
| **B** | `10.1 – 500.0`  | 25 % |
| **C** | `500.1 – 1000.0` | 15 % |

1. Pick a category via accumulated-probability draw.
2. Bucket the JSON's flattened verbs by category (using each verb's
   weight).
3. Pick a uniform random index from the winning bucket.
4. If the bucket is empty, fall through to the next non-empty
   category.

Empirically validated: 5 000 picks yield ~61 / 24.5 / 14.5 %
distribution.

The same `pickWeightedIndex` is exposed to the user via the
**shuffle / dice button** in the card header — click it for another
random verb without reloading.

## Architecture notes

- **Routing** is namespaced under `/v1`. `<App>` calls `useVerbos()`
  once at the top level (above `<Routes>`) so verb filters work
  regardless of the route. `useVerbos` reads `useLocation().pathname`
  with a regex scoped to `/v1/verbs/<slug>` and falls back to
  `useParams()` value when present. Legacy redirects (`/repaso` →
  `/v1/test`, `/<slug>` → `/v1/verbs/<slug>`) keep old bookmarks
  working. Unknown URLs land on `/`.
- **Two React contexts** (`VerbContext` + `SRSContext`) live
  symmetrically: `useVerbos()` runs once in `<App>`'s body, and
  `useSRS()` runs once in `Root` (a small wrapper in `src/main.jsx`)
  so that `useVerbos`'s auto-register effect can call
  `useSRSContext()` — the provider has to exist by the time
  `useVerbos` renders. Never call `useSRS()` twice.
- **Image flow** in `VerbImage`: starts with the inline SVG as the
  base layer so the user never sees a blank frame. State initializer
  reads `imageCache` synchronously and seeds the URL from there if
  it's a hit; otherwise the effect fires the async Pexels fetch
  (when `VITE_PEXELS_API_KEY` is set). Any failure cascades to
  Picsum, then to the SVG alone. Attribution lives in the
  `ImageCredit` overlay, linked to the photographer's Pexels
  profile. The composite-key pattern `${verbKey}-${renderId}` on the
  wrapper `<div>` plus a derived-state fallback inside `VerbImage`
  defends against stacked mounts when navigating fast.
- **Audio playback** uses an imperative `new Audio()` instance per
  button rather than a JSX `<audio>` element. This avoids a race
  where the React render hadn't committed yet when `play()` was
  called, which previously left the button stuck on its loading
  spinner. `AudioButton` is a `forwardRef` so `VerbImageOverlay` can
  trigger play on image click.
- **Verb transitions** play a 480 ms fade-up + scale keyframe
  (`@theme --animate-verb-enter` in `index.css`) on the inner
  content block, triggered by a `key={verbKey}` remount. The hero
  image stays mounted so it doesn't reload.
- **Swipe gesture** is implemented via direct DOM mutation in
  `VerbCard.handleTouchMove` for 60 fps feedback without re-renders.
  A 70 px horizontal threshold (with `|dx| > 1.5·|dy|`) distinguishes
  a swipe from a vertical scroll.
- **Theme application** lives at `<html data-theme="...">`. Tailwind v4
  has no config file — DaisyUI is registered as a CSS plugin in
  `src/index.css`:
  `@plugin "daisyui" { themes: light --default, dark, dracula, cupcake; }`.
  `useTheme()` persists to `localStorage['ospinajuanp-ingles:theme']`
  and re-applies on every change. A tiny inline `<script>` in
  `index.html` mirrors the same key BEFORE React mounts so dark-mode
  users see no flash of light on reload.
- **Live data sync** is a tiny Vite plugin (`vite.config.js →
  syncDataPlugin`) that watches `verbos_estructura.json` and copies
  it into `public/` on dev start, build start, and on every change.
- **MongoDB sync** fires from `src/utils/mongoSync.js` on every
  successful verb visit (image + audio resolved). `api/verbs/sync.js`
  uses an atomic `findOneAndUpdate` with `$set` + `$setOnInsert` +
  `$inc` + `$currentDate`. `migrado_desde` is server-managed via
  `$setOnInsert` only (bulk passes `'SPA_Bulk_Migration'`, lazy
  defaults to `'SPA_Lazy_Migration'`) so updates never overwrite the
  marker.

## Spaced Repetition (SM-2)

Pure-function math lives in `src/utils/srs.js`:

```text
SRS_MIN_EF   = 1.3          // EF floor
SRS_INITIAL_EF = 2.5         // fresh-card EF

calculateNextReview(interval, ef, grade)
  fail  → interval = 1, repetitions = 0, ef = max(1.3, ef - 0.20)
  hard  → interval grows by EF,           ef = max(1.3, ef - 0.10)
  good  → interval grows by EF,           ef unchanged
  easy  → interval grows by EF,           ef += 0.15
  (successes share: 0 → 1, 1 → 3, then round(prev * ef))
```

State lives in `localStorage['ospinajuanp-ingles:srs:v1']` under a
versioned schema. The hook (`useSRS`) is the single owner; everything
else reads via `useSRSContext()`. The cross-tab `storage` event keeps
multiple tabs in sync.

Two decks coexist in one queue:

- **Mazo Personalizado** — user-added sentences via `AddFlashcardForm`
  on `/v1/test` (front = Spanish, back = English).
- **Mazo de Verbos Vistos** — auto-populated. Every time the user
  lands on a verb in the main app, `useVerbos` calls
  `srs.registerVerb(currentVerb)`, which is idempotent per `verbKey`
  (`id:${id}` preferred, `slug:<ing>` fallback). Re-visits do not
  duplicate.

**4-level grading UI** on every card: Otra vez (fail / `error`),
Difícil (hard / `warning`), Bien (good / `success`), Fácil (easy /
`info`). Cards are 3D-flip Tailwind arbitrary values
(`[perspective:1200px]` / `[transform-style:preserve-3d]` /
`[backface-visibility:hidden]` / `[transform:rotateY(180deg)]`).

**Deck Manager** is the second tab of the `/v1/test` page
(`ModeToggle` join group). DaisyUI table with real-time search
across both languages, 10/page pagination (numeric shortcuts + first/
last + ellipsis gaps), edit (custom only, via a native `<dialog>`)
and delete (any card, with `window.confirm`). Editing a custom
prompt **preserves the SRS schedule** — only the prompt text
changes.

## Conventions

- Spanish-language UI copy, English-language code/comments.
- 2-space indent, single quotes, no semicolons, JSX attribute
  wrappers on their own lines for multi-attribute elements.
- Tailwind classes ordered: layout → sizing → spacing → color →
  typography → effects.

## License

This project is licensed under the [Polyform Noncommercial License 1.0.0](LICENSE.md).

You are free to view, fork, and modify the code for personal, educational, or portfolio purposes.
**Commercial use is not permitted** without a separate written agreement from the author.

(c) 2026 Juan Pablo Ospina Restrepo.