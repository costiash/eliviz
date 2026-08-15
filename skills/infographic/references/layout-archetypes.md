# Layout archetypes — backbone patterns × content archetypes

Companion to infographic-anatomy.md. The infographic-director agent picks ONE
content archetype and ONE backbone per infographic, driven by the data shape
in the parser output. Never mix backbones on a single canvas.

## Backbones (from the CHI 2020 Visual Information Flow taxonomy [3])

Linear (explicit order, best for narratives):

- **portrait** — vertical spine, groups stacked on one side. The default for
  data stories; strongest single-path readability. Number chips ride the spine.
- **spiral (zigzag)** — vertical flow, groups alternate left/right of a center
  spine. Adds rhythm for 4–6 sections; connector line must snake visibly.
- **pulse** — horizontal flow, groups alternate above/below a center line.
  Wide canvases (presentation headers, banners) only.
- **up-ladder / down-ladder** — diagonal steps; use for ranked or cumulative
  stories ("from smallest to biggest").

Circular (use only when data is cyclic or radiates from one concept):

- **clock** — groups around a full circle; cyclical processes, "a day/season of".
- **star** — groups radiating from a central object; one-concept-many-facets.

Rule of thumb: portrait unless the data argues otherwise; zigzag when eli5
(rhythm keeps young/novice readers moving); ladder for rankings; clock/star
only with genuinely cyclic/radial content.

## Content archetypes (pick by data shape) [4]

| Archetype | Data signal (from parse output) | Core devices |
|-----------|--------------------------------|--------------|
| **Statistical (hero-stat)** | one table, mixed columns, no dominant time axis | hero number, pictogram row, category bars, callout chips |
| **Timeline** | date column spanning months/years; "history of" asks | dated spine as THE backbone, milestone dots, era bands |
| **Process/How-it-works** | ordered steps (docs, logs pipelines, numbered md sections) | numbered arrows, step icons, input→output framing |
| **Comparison** | 2–3 entities dominating a categorical column | side-by-side split canvas, mirrored bars, VS divider |
| **Ranked list** | top-N question, high-cardinality categorical | ladder backbone, position medals/numbers, bar-per-rank |
| **Composition** | parts-of-whole (shares, percentages) | pictogram grid (ISOTYPE), waffle/donut, "1 in N" framing |

A single infographic uses ONE primary archetype; a secondary device may appear
inside one section only (e.g., a mini composition inside a statistical story).

## Section recipe (every evidence section, all archetypes)

```
[number chip]––spine––┐
  [icon 40px]  [HEADER ≤4 words]
               [fact sentence ≤14 words, number in bold accent]
               [micro-visual: one chart OR pictogram row, annotated]
```

Number chips are the explicit flow hint (research: digits + arrows are the
strongest explicit VIF cues [3]); the spine connects them; icon anchors the
group (Gestalt proximity [3]); one micro-visual per section, never two.

## Canvas presets

| Preset | CSS px | Use |
|--------|--------|-----|
| `story` (default) | 1080 × measured (≈1700–2400) | vertical share, chat, print-ish |
| `square` | 1080 × 1080 | social feeds; max 3 sections + hero |
| `wide` | 1920 × 1080 | slides/banners; pulse backbone only |

Always render at MEASURED content height (body.scrollHeight), never a guessed
fixed height; then verify nothing clipped. 2× device scale for the PNG.

## Design-pack integration

The infographic inherits the chosen eliviz design pack's palette variables and
type stack, but NOT its layout CSS: infographic layout comes from this file's
grammar. Accent = hero + number chips; accent2 = secondary series; accent3 =
callout/annotation color. Annotations use an italic/handwritten-feel style
distinct from body text (IPCC AR6 technique [8]).

## Wireframe — portrait/statistical at eli5 (the canonical starter)

```
┌──────────────────────────────┐
│ eyebrow · hook question      │
│ TITLE (display, 2 lines max) │
│ ┌──────────────────────────┐ │
│ │  HERO STAT (giant)       │ │
│ │  one-line gloss          │ │
│ └──────────────────────────┘ │
│ (01)┐ icon HEADER            │
│  │  │ fact + micro-chart     │
│  │  │   ~annotation~         │
│ (02)┤ icon HEADER            │
│  │  │ fact + pictogram row   │
│ (03)┤ icon HEADER            │
│  │  │ fact + category bars   │
│ (04)┘ icon HEADER            │
│     │ fact + micro-chart     │
│ ★ THE TAKEAWAY (distinct bg) │
│   · three plain-words lines  │
│ sources · honesty line       │
└──────────────────────────────┘
```
