# Design bank

The visual identity of a generated page is a **design pack**: a directory with
`design.json` (tokens + metadata) and `design.css` (an override stylesheet
injected into the template's `<style id="design-css">` slot, after the base
styles). The base template IS the `aurora` design; every other pack restyles it
by overriding CSS custom properties and the small, stable set of component
classes below. Packs never touch markup or JS.

## The bank

| id          | Name            | Ground | Hero     | Signature |
|-------------|-----------------|--------|----------|-----------|
| `aurora`    | Aurora Glass    | dark   | `wave`   | glassmorphism, violet/cyan/pink gradient family, ocean-of-light hero |
| `editorial` | Editorial Light | light  | `static` | warm paper, Fraunces italic serif, hairline rules |
| `brutalist` | Brutalist       | light  | `static` | 2px black borders, hard offset shadows, zero radius, highlight-block title |
| `terminal`  | Terminal CRT    | dark   | `rain`   | phosphor green mono, scanlines, code-rain hero, blinking cursor |
| `neon`      | Neon Cyberpunk  | dark   | `grid`   | violet night, magenta/cyan glow, synthwave grid + striped-sun hero |

Build with `--design <id>`, or `--design <path>` for a custom pack directory.
`--list-designs` prints the bank. An explicit `--accent` flag beats the pack's
accent.

## Selection rubric (the design-adapter agent's pick-mode guide)

Design choice belongs to the `design-adapter` agent (pick mode) — the skill
sends it a data profile and builds with what it returns. This is its rubric.
Choose by dominant dataset + audience cues, then confirm by mood words in the
user's request:

- log-heavy or sqlite/dev data → `terminal`
- reports, documents, business/finance tables, "for stakeholders/print" → `editorial`
- gaming/social/event/marketing data, "flashy", "wow" → `neon`
- creative portfolios, launches, "bold", "loud" → `brutalist`
- mixed or unknown → `aurora` (default)

Tie-breakers: content beats surface keywords (a dev experiment that is mostly
long-form REPORTS reads better in a quiet ground than a CRT novelty); the
dataset the reader will spend the most time in dominates; audience overrides
aesthetics. Each pack's `design.json` carries `mood` and `best_for` arrays —
match request keywords against them rather than hardcoding beyond these
defaults.

## design.json schema

```jsonc
{
  "id": "editorial",            // = directory name
  "name": "Editorial Light",
  "tagline": "…",
  "mood": ["light", "corporate", …],      // matching keywords for auto-pick
  "best_for": ["reports", …],
  "hero": "wave" | "rain" | "grid" | "static",
  // Each animated value is a DIFFERENT Three.js figure — no two designs need
  // to share one. wave = ocean-of-light + motes (aurora's). rain = falling
  // code columns (terminal's). grid = synthwave floor + striped sun (neon's).
  // static = no WebGL at all; --hero-static-bg paints the canvas.
  // "particles" is accepted as a legacy alias for "wave".
  // All figures auto-color from --accent/--accent2/--accent3 and --hero-fog,
  // so a custom pack can claim any figure and it will wear the pack's palette.
  "dark": false,                          // ground polarity (adapter hint)
  "accent": "#9a3412",                    // seeds --accent (CLI --accent wins)
  "accent2": "#0f766e", "accent3": "#9d174d",   // seed --accent2/--accent3
  "fonts": { "display": "…", "body": "…", "mono": "…",
             "google": "https://fonts.googleapis.com/css2?…" }  // one link, injected in <head>
}
```

`accent` drives gradients, hbar fills, chart gradient bottom stop, hover glows.
`accent2` is the chart gradient top stop, date-column color, donut secondary.
`accent3` is the boolean-column color and gradient tail. The hero particle wave
lerps accent → accent2 → accent3, so the three together ARE the hero palette.

## Override surface (what design.css may target)

**Semantic variables** (set on `:root`) — always set all of these coherently:

| Var | Drives |
|-----|--------|
| `--hero-fog` | Three.js fog color (all animated figures) — MUST match the page ground |
| `--hero-static-bg` | canvas background when `hero: "static"` (or WebGL fails) |
| `--ct-number`, `--ct-string` | number/text column colors (cards, donut, chips) |
| `--lvl-error/-warn/-info/-debug` | log level badges + donut |
| `--track` | donut/bar track color |
| `--donut-text`, `--donut-text-dim` | donut center label |
| `--muted` | null/neutral tokens |

**Component classes** — the stable seams, in the order the packs organize them:
`body` + scrollbar + `::selection`; the white-alpha utility mappings (below);
`.glass` / `.glass-strong` / `.chip` / `.card-hover`; `.font-display` /
`.grad-text` / `.grad-line`; `#hero > div[style*="radial-gradient"]` (the
vignette overlay — retint or disable); `.dtable th/td/tr` + `.cell-num` /
`.cell-null` + `.tab-btn.active`; `.logtext` / `.logline` / `.loglvl` /
`.lvl-chip.active`; `.prose-msg` elements + `.prose-doc` borders; `.jk .js_
.jn .jb .jz .jm` JSON tree tokens.

**The light-ground recipe.** The template's text/border/background utilities
are white-alpha (`text-white/60` etc.). A light pack MUST remap every one of
them to ink. Define `--tx` as a bare RGB triplet (e.g. `--tx: 28 25 23;`) and
copy the mapping block from `editorial/design.css` (the `.text-white…` through
`.hover\:bg-white\/5:hover` run), adjusting alphas to taste — light grounds
need HIGHER alphas than the white originals to keep contrast. Dark packs must
NOT include this block. Also on light grounds: disable or retint the hero
vignette overlay, give `.glass` an opaque background, and darken the four
`--lvl-*` colors (the dark-theme defaults are pastels that fail on white).

**Radii and shadows** are fair game (`border-radius` overrides on the
`.rounded-*` utilities — see brutalist). Blur is `.glass`'s
`backdrop-filter`; flat designs should set it to `none`.

**Never**: hide data, remove hover states, add un-guarded looping animation
(guard with `@media (prefers-reduced-motion: reduce)`), reference external
images or fonts beyond the single `fonts.google` link, or use element IDs from
render functions (they're per-dataset and unstable).

## Blending packs

Every pack's CSS uses the same labeled sections, so blends are section grafts:
take the ground + text mappings from one pack, the surface language from
another, the type block from either, then re-derive the semantic vars for the
resulting ground. Blend rules of thumb: exactly one surface signature (blur XOR
offset-shadow XOR glow XOR hairline); tokens (`--ct-*`, `--lvl-*`) always
follow the GROUND, not the source pack; `--hero-fog` always equals the final
background; if either parent is light, follow the full light-ground recipe.

For custom brands: put the brand color in `--accent`, derive `accent2` (a
60–120° hue shift, similar lightness) and `accent3` (between them or a
deepened accent), and check body-text contrast ≥ 4.5:1 before committing.

## Verifying a pack (non-negotiable)

Build against a mixed input set (a table + a text doc + a log, so every render
path is exercised), then headless-screenshot hero + mid-scroll at 1440px and
390px. Read the screenshots and check: title legible over the hero, every text
tier readable (chips, table header, log lines, tree tokens), charts visible
against the ground, no leftover base-design colors, zero JS errors, no
horizontal overflow at 390px.
