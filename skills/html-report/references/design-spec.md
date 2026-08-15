# Design spec — assets/template.html

Read this before editing the template (custom themes, new sections, different
hero). It documents the visual system and the safe extension seams so changes
stay coherent instead of fighting the existing code.

## Content voice

All rendered copy is ELI5_FOR_DUMMIES (see SKILL.md "Content voice"): everyday
words, real-world comparisons ("a column is like a labeled jar"), short punchy
sentences, zero fluff. Any new section head, panel title, stat label, or note
you add to the template must read the same way. User data (column names, cell
values, log lines, document text) is never rewritten.

## Design language

- **Mood**: dark, luminous, editorial. Near-black ink background (`#0b0b14`),
  glassmorphism panels, one gradient family used everywhere.
- **Palette**: CSS variables on `:root` — `--accent` (set from
  `meta.accent` at boot), `--accent2` (cyan `#22d3ee`), `--accent3`
  (pink `#f472b6`). Every gradient, chart, chip highlight, and hero particle
  color derives from these three. Semantic exceptions: column-type colors
  (`COLTYPE_META`), log-level colors (`LVL_COLORS`), and JSON-token colors are
  fixed hues chosen to read against the ink background. To retheme, change the
  variables — do not scatter new hex values.
- **Type**: Space Grotesk for display headings (`.font-display`), Inter for
  body, JetBrains Mono for code/data. Loaded from Google Fonts with graceful
  system-stack fallback.
- **Surfaces**: `.glass` (4% white + blur + 8% border) for cards,
  `.glass-strong` for nav/modal. Radius scale: `rounded-2xl` cards,
  `rounded-3xl` modal, `rounded-full` chips.
- **Motion philosophy**: entrances are staggered rises (`y: 26 → 0`,
  `power3.out`), numbers count up, bars grow from their baseline. Nothing
  loops except the hero particles and the scroll cue. Everything honors
  `prefers-reduced-motion` (checked once into `reducedMotion`), and every GSAP
  call is guarded by `hasGsap` so a missing library degrades to a static page,
  not a blank one.

## Page anatomy

1. **Hero** (`#hero`) — full-viewport Three.js canvas (`#hero-canvas`): a
   160×90 additive-blended particle wave, color-lerped accent→cyan→pink, plus
   260 drifting motes; mouse parallax on the camera; rendering pauses via
   IntersectionObserver when scrolled past; GSAP scrub fades it out on scroll.
   Overlay: eyebrow chip, `#hero-title` (split into gradient + white halves at
   boot), `#hero-subtitle`, `#hero-chips` (aggregate stats), scroll cue.
   Fallbacks: no THREE → CSS radial-gradient background; WebGL init throw →
   same; reduced motion → single rendered frame.
2. **Nav** (`#topnav`) — sticky glass bar: brand dot, dataset tabs (`#tabs`,
   only when >1 dataset), search field (visible only for `table` and `log`
   datasets — see `SEARCHABLE`).
3. **Content** (`#content`) — re-rendered per active dataset by
   `renderDataset(ds)`, which dispatches on `ds.type`.
4. **Modal** (`#modal`) — one shared overlay, used for column drill-downs.
   `showModal()/hideModal()` handle animation + body scroll lock; Escape and
   backdrop close it.

## Per-type sections

- `table`: stat cards (rows/cols/filled %/cells) → rows-over-time bar chart
  (or top-distinct columns when no date column) + column-type donut → column
  profile card grid (`data-open-col`, mini histogram / top-3 values /
  true-false split / date range per type via `colMiniViz`) → the data table:
  sticky sortable headers (`data-sort-col`, asc → desc → off), top-nav search
  filtering, 100-row pagination (`tableState` per dataset), typed cell
  rendering (`cellHtml`: mono right-aligned numbers, ✓/✗ booleans, dim `∅`
  nulls). Column cards open the modal (`openColumn`): full histogram, top-10
  values, or boolean donut.
- `text`: stat cards → top-words bars + density panel → reading view. Markdown
  renders through `md()` with the `.prose-doc` article styles inside a wide
  glass panel; plain text renders in a `<pre>`. When an outline exists, a
  sticky sidebar links to heading anchors — `wireText` assigns
  `id="hd-{ds.id}-{i}"` to rendered headings by matching outline text (order
  fallback).
- `log`: stat cards (lines/errors/warnings/timestamped) → lines-per-day chart
  (falls back to hour-of-day when a single day) + level donut → optional
  hour-of-day + top-sources row → the log viewer: level filter chips
  (`data-lvl`, `logState` per dataset), top-nav search, chunked rendering
  (400 lines + "load more"), colored level badges (`LVL_COLORS`).
- `generic`: node/depth/type stats, type donut, top-keys bars, lazy
  collapsible JSON tree (`jtreeNode` + `expandLazy`; children render on first
  toggle, 400 per level, so multi-MB payloads stay responsive).

## Data contract

Data is injected as JSON into `<script type="application/json"
id="viz-data">` replacing the literal `/*__VIZ_DATA__*/`. If the placeholder
is left in place, `boot()` shows a friendly "no data" hero rather than
erroring. Schema: see `data-model.md`.

## Charts

Hand-rolled SVG (no chart library): `barChart(data,{height})` for vertical
series with a shared vertical gradient def (also used for histograms at small
heights), `hBars(data,{labelKey})` for labeled horizontal bars, `donut(parts)`
for share-of-total. All emit `<title>` tooltips and animate via
`.bar-anim`/`.hbar-anim` classes picked up by `animateBars()`. Reuse these
instead of adding a chart library.

## Vendored libraries

`build_html.py` inlines `assets/vendor/{tailwind,gsap,ScrollTrigger,three}`
into the output by default (fully offline single file, ~1.2 MB overhead);
`--cdn` keeps the CDN `<script>` tags instead. The `data-vendor` attribute on
those tags is the inlining hook — keep it if you edit the `<head>`.

## Extension seams (safe places to hook in)

- **New section for an existing type**: append HTML inside the relevant
  `render*` function using `sectionHead()`, `panel()`, `statCard()` — then the
  existing `animateReveals/Counters/Bars` calls pick it up automatically
  (anything with `.reveal`, `.counter[data-target]`, `.bar-anim` animates for
  free).
- **New dataset type**: add a normalizer in `parse_input.py`, a `render*` +
  optional `wire*` branch in `renderDataset()`, a hero chip in `heroChips()`,
  and — if it should use the top-nav search — an entry in `SEARCHABLE` plus a
  handler in the search `input` listener. Document the payload in
  `data-model.md`.
- **Retheme**: change `:root` variables + the `body` background; a light
  theme also needs `.glass` backgrounds flipped to dark-on-light, text
  utilities swapped (`text-white/xx` → `text-slate-xxx`), and the `.dtable`
  sticky-header background updated.
- **Different hero**: replace the body of `initHero()` only; keep the canvas
  id, the fallback paths, and the IntersectionObserver pause.

## Quality bar (what "award-worthy" means here)

Check these before delivering: hero text readable over the canvas at 1440px
AND 390px wide; no horizontal overflow at 390px; counters land on exact
formatted values; every interactive element has a hover state; modal scroll
doesn't bleed to the page; long unbroken strings wrap (`overflow-wrap:
anywhere` on `.prose-msg`/`.logtext`, `text-overflow: ellipsis` + `title` on
table cells); every cap (rows, lines, chars, sheets, tables) is labeled in an
amber note chip; JS console clean. If you add imagery, keep it as inline SVG
or data: URLs — the page must remain a single file.
