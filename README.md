# Verbos en Inglés

A modern single-page web app for learning English verbs in Spanish.
Browse 1,000 weighted verbs with full conjugations (past, participle,
gerund, future, conditional), six contextualized example sentences
per verb, and on-demand pronunciation audio pulled from the free
[Dictionary API](https://dictionaryapi.dev/).

![Verbos en Inglés](public/icon.ico)

## Features

- **Smart initial pick** — On every page load the app lands on a verb
  chosen by a weighted random lottery (60 % high-frequency,
  25 % mid-frequency, 15 % low-frequency) from a curated list of
  1,000 verbs.
- **On-demand re-roll** — A dice button next to the pager rerolls
  the lottery without reloading the page.
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
  the inline SVG forest illustration.
- **Real-time search + filters** — Filter by category
  (Generales / Tecnología) and subcategory (Simples / Irregulares
  / Compuestos). Search matches both English infinitives and
  Spanish meanings.
- **Mobile-first** — Responsive from 320 px up. Swipe horizontally
  on the card to navigate between verbs. Touch targets stay in the
  thumb zone. `<kbd>←</kbd> / <kbd>→</kbd>` on desktop.
- **Accessibility** — Honors `prefers-reduced-motion`, full keyboard
  navigation, ARIA labels on every interactive element, semantic
  roles for the conjugation/sentence cards.
- **Live data sync** — Edit `verbos_estructura.json` at the repo
  root and Vite hot-reloads the running dev server automatically
  (no manual copy into `public/`).

## Tech stack

- **React 19** with strict mode + concurrent rendering
- **Vite 8** for dev server and production build
- **Tailwind CSS v4** via `@tailwindcss/vite` (no config file, CSS-first
  theme via `@theme` in `src/index.css`)
- **Free Dictionary API** for pronunciation audio
- ESLint 9 with flat config + `eslint-plugin-react` /
  `eslint-plugin-react-hooks` / `eslint-plugin-react-refresh`

No state-management library, no router, no backend, no API keys.
Everything runs from a static `dist/` directory.

## Requirements

- **Node.js ≥ 20** (the project is built and tested on v24).
- **pnpm** (recommended). npm or yarn also work.
- **Pexels API key** (optional, for curated photos per verb). Free tier:
  200 requests/hour, 20,000/month. Without a key the app falls
  back to Picsum + inline SVG.

## Installation

```bash
git clone https://github.com/ospinajuanp/ospinajuanp-ingles.git
cd ospinajuanp-ingles
pnpm install
cp .env.example .env       # then paste your Pexels key (optional)
```

### Optional: configure Pexels for verb hero images

1. Sign up for a free key at <https://www.pexels.com/api/>.
2. Open `.env` and paste it after `VITE_PEXELS_API_KEY=`.
3. Restart `pnpm dev`. The first time you visit a verb, the app
   fetches a curated photo from Pexels and caches it in memory
   (see `src/utils/imageCache.js`). Subsequent visits are
   instant.

Without a key, verbs show Picsum images (deterministic per word)
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
├── index.html                       # Vite entry, sets the favicon
├── vite.config.js                   # Plugins: react + tailwind + sync-data
├── eslint.config.js                 # Flat config (react, hooks, refresh)
├── package.json
├── pnpm-lock.yaml
├── public/
│   ├── icon.ico                     # Favicon + brand logo (256×256)
│   └── verbos_estructura.json      # Copied from root at build/dev time
├── verbos_estructura.json           # Authoritative dataset (gitignored)
├── src/
│   ├── main.jsx                     # React root
│   ├── App.jsx                      # Shell: header + skeleton/error/card
│   ├── index.css                    # Tailwind import + @theme + keyframes
│   ├── components/
│   │   ├── AudioButton.jsx          # Free Dictionary API audio player
│   │   ├── CategoryFilter.jsx       # Pills for category / subcategory
│   │   ├── ConjugationGrid.jsx      # 3-col grid with reveal-on-hover
│   │   ├── HeroIllustration.jsx     # Inline-SVG forest-path fallback
│   │   ├── ImageCredit.jsx          # Pill attribution for Pexels photos
│   │   ├── NavButtons.jsx           # Prev / counter / next / shuffle
│   │   ├── SearchBar.jsx            # Live filter input
│   │   ├── SentencePill.jsx         # Sentence card with blur reveal
│   │   └── VerbCard.jsx             # The main flashcard + swipe gesture
│   ├── hooks/
│   │   └── useVerbos.js             # Loads JSON, filters, weighted pick
│   ├── data/
│   │   └── weightedVerbs.js         # 1,000 verbs with weights + dedup map
│   └── utils/
│       ├── audioCache.js            # In-memory cache of resolved audio URLs
│       ├── flatten.js               # Walk nested JSON → flat array
│       ├── imageCache.js            # In-memory cache of Pexels photos
│       ├── pexels.js                # fetchPexelsPhoto() with auth header
│       ├── tips.js                  # Rotating conjugation tips
│       └── weightedRandom.js        # 60 / 25 / 15 lottery
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

- **Image flow** in `VerbImage`: starts with the inline SVG as the
  base layer so the user never sees a blank frame. State initializer
  reads `imageCache` synchronously and seeds the URL from there if
  it's a hit; otherwise the effect fires the async Pexels fetch
  (when `VITE_PEXELS_API_KEY` is set). Any failure cascades to
  Picsum, then to the SVG alone. Attribution lives in the
  `ImageCredit` overlay, linked to the photographer's Pexels
  profile.
- **No global state** — everything lives in `useVerbos` or local
  component state.
- **Audio playback** uses an imperative `new Audio()` instance per
  button rather than a JSX `<audio>` element. This avoids a race
  where the React render hadn't committed yet when `play()` was
  called, which previously left the button stuck on its loading
  spinner.
- **Verb transitions** play a 480 ms fade-up + scale keyframe
  (`@theme --animate-verb-enter` in `index.css`) on the inner
  content block, triggered by a `key={verbKey}` remount. The hero
  image stays mounted so it doesn't reload.
- **Swipe gesture** is implemented via direct DOM mutation in
  `VerbCard.handleTouchMove` for 60 fps feedback without re-renders.
  A 70 px horizontal threshold (with `|dx| > 1.5·|dy|`) distinguishes
  a swipe from a vertical scroll.
- **Live data sync** is a tiny Vite plugin (`vite.config.js →
  syncDataPlugin`) that watches `verbos_estructura.json` and copies
  it into `public/` on dev start, build start, and on every change.

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