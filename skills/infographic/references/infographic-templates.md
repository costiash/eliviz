# Infographic template bank — layout grammars (visually grounded)

This bank holds **templates** (layout grammars — how a popular infographic is
*structured*), orthogonal to **style packs** (palette/typography registers,
infographic-design-bank.md). A run picks: level → template → style. Templates
are grounded three ways: direct visual deconstruction of reference specimens
(the three attached community examples), the pattern literature (CHI'20 VIF,
Excalidraw/Eraser diagram methodology, IBM diagram standards, NotebookLM
structure vocabulary), and a render-and-compare loop — every template ships
with a validated local render before entering the bank.

## Global grammar (applies to every template)

From the diagram-methodology corpus:

- **Shape IS meaning** — diamond = decision/router, ellipse = actor/process
  start-end, rectangle = component/step, hexagon badge = concept, dot = marker.
  Never mix node types without semantic difference (IBM rule).
- **Color IS semantics, with a fixed dialect**: green = pass/positive/confirmed,
  yellow/amber = caution/unresolved, red/rose = fail/negative/risk,
  blue = information/process, purple = meta/identity. Panels carry their
  semantic as a tinted FILL + matching border; content stays ink-on-light or
  silver-on-dark. Any non-obvious coding gets a **legend** (IBM rule).
- **Lines as structure**: spines, arrows, and rules do the organizing;
  containers only when the thing is a "thing" (< ~30% of text boxed).
- **Icons: one dialect per canvas** — emoji-glyph dialect (✅ ⚠️ ❌ ❓ 🔍) OR
  line-icon dialect OR filled-badge dialect. Emoji-glyph is the signature of
  the popular "AI report card" style and costs zero assets.
- **Every arrow earns its place** — if A relates to B, draw it; if not, don't.

## The templates

### T1 · `verdict-card` — the "AI report-card" grid
*Specimen: attached Chaos Haunter OSINT Verdict Report (labeled ELI5).*

Deconstruction of the specimen: white ground; big serif/rounded title +
purple context chip; a **verdict strip** of 3–4 outlined KPI badge cards
(shield/checkmark iconography, each its own semantic color); a dashed-border
**input summary** card with friendly avatars; a **numbered horizontal process
flow** ("what he did", 5 steps, arrow-connected pastel cards); a **findings
grid** (5 cards, tinted tops, ✅/❓ glyphs, per-card `Sources: [n]` footnotes);
a **"baby graph"** micro bar chart with a 0/1/2 coded scale + legend; **TL;DR
checklist** rows (glyph + one-liner); three-column audit panels (credibility /
cui bono / concurrent checks); and a bottom **flowchart verdict strip** —
yes/no chips arrow-chained into an OVERALL verdict card, closed by a 💡
bottom-line banner.
Grammar: Z-pattern macro-flow; panel grid micro-flow; every panel
self-contained (header + glyphs + ≤3 short lines); color semantics do the
scoring; sources cited per-panel.
**Use for**: verdicts, audits, assessments, "what we found" reports, any
brief with pass/fail texture. **Levels**: eli5, junior (its native voice IS
eli5). **Ground**: light.

### T2 · `badge-map` — hub-and-spoke concept map
*Specimen: attached "harness design patterns" figure.*

Deconstruction: central emblem (gear hexagon) with bidirectional arrows
radiating to 10–12 **hexagonal icon badges**, each badge = icon + single-word
label OUTSIDE the badge; muted 3-color palette (navy/orange/sage) rotated
across badges; one badge expanded into a mini-cluster (subagents) to show
depth; academic figure caption beneath.
Grammar: radial VIF (star backbone); badges uniform size (equality of
concepts); labels never inside badges; arrows plain, no labels needed when
the relation is uniform ("is-a-pattern-of").
**Use for**: taxonomies, capability maps, "the N kinds of X", ecosystem
overviews. **Levels**: junior, pro. **Ground**: light or dark.
Caution: no reading order — pair with a numbered list when sequence matters.

### T3 · `neon-blueprint` — dark architecture flow
*Specimen: attached Consumer–Consult Architecture diagram.*

Deconstruction: near-black void ground; semantic node shapes with **neon
stroke + dark fill** (diamond router purple, ellipses orange/red, rounded
rects blue), icon + title + ≤4 bullet lines inside majors; **color-coded
directional arrows with an explicit LEGEND panel**; a monospace evidence
panel (project tree) top-left; numbered "expected behavior" list + intent
panel as bottom footers; one green feedback arrow sweeping back to close the
loop.
Grammar: layered flow VIF; evidence artifacts as dark monospace blocks;
flows distinguished by color not linestyle; footers translate the picture
into ordered words.
**Use for**: system/data architectures, pipelines, agent flows, "how it
works" internals. **Levels**: junior, pro. **Ground**: dark.

### T4 · `journey-spine` — numbered vertical data story
*Specimen: eliviz v2 exemplar (validated).* Portrait VIF: hook → hero stat →
numbered chips on a connector spine → visual-group sections → takeaway →
source strip. **Use for**: statistical stories from one dataset. **Levels**:
all (register shifts with style pack).

### T5 · `bento-grid` — modular tile mosaic
*From the current NotebookLM/social vocabulary.* Uneven tile grid (1 hero
tile 2×2, satellites 1×1), one fact per tile, no connectors — proximity and
scale do the ranking; square-canvas native. **Use for**: highlight reels,
social squares, "N things to know" without sequence. **Levels**: eli5, junior.

### T6 · `broadsheet-brief` — editorial data briefing
*Specimen: eliviz pro exemplar (validated).* Kicker + finding-stating
headline + standfirst; hairline KPI strip; two-column module grid; findings
block; formal source line. **Use for**: analyst/stakeholder briefings.
**Levels**: pro only.

## Selection matrix (director agent, after level is fixed)

| Content shape | eli5 | junior | pro |
|---|---|---|---|
| verdict/audit/assessment | T1 | T1 | T6 (or T1 toned down) |
| one-dataset statistical story | T4 | T4 | T6 |
| taxonomy / kinds-of / ecosystem | T5 | T2 | T2 |
| architecture / pipeline / how-it-works | T4 (simplified) | T3 | T3 |
| highlights, no sequence | T5 | T5 | T6 |
| process / step-by-step | T1's flow strip alone | T4 | T3 |

Template × style-pack compatibility: T1 light packs only; T3 dark packs only;
T2/T4/T5 any; T6 broadsheet/journal. The style pack may never override a
template's color SEMANTICS (green/amber/red dialect) — it tunes the hues,
not their meanings.

## Verification additions (beyond anatomy checklist)

- Semantic-color audit: no green on a negative, no red on a positive; legend
  present if any coding is non-obvious.
- Glyph dialect audit: one icon dialect per canvas.
- T1: every findings panel cites sources; verdict strip readable standalone.
- T2: badges uniform; labels outside; caption present.
- T3: every arrow color appears in the legend; evidence blocks monospace.
