# Infographic anatomy — what separates an infographic from a poster

Grounded reference for the infographic skill and the infographic-director agent.
Every rule here traces to published design guidance or peer-reviewed research
(sources at bottom). Read this BEFORE composing any infographic layout.

## The defining distinction

A **poster** (including a styled dashboard) presents a pre-determined message
with data as support; most of it can be absorbed in ~10 seconds and sections
are independent. An **infographic** makes the DATA the star: the narrative
*emerges from* the data, information is encoded at multiple levels (size,
position, color, repetition), and the reader *studies* it — following one
guided path from hook to takeaway. [1]

The four-looks test (Neurath): "At the first look you see the most important
points; at the second, the less important points; at the third, the details;
at the fourth, nothing more — if you see more, the teaching-picture is bad." [6]

If a draft fails ANY of these, it is a poster, not an infographic:

1. There is one **hero stat** — the single number that changes everything —
   and it is the largest data element on the canvas. [4, 5]
2. There is a **single unambiguous reading path** (a "backbone") with explicit
   flow hints: numbered sections, connector lines/arrows, or a visual spine.
   The reader never has to "solve" the layout. [2, 3, 5]
3. Sections are **visual groups** — icon + header + fact + micro-visual bound
   together by proximity — not free-floating panels. [3]
4. It reads as a **story with a beginning, middle, and end**: hook (the
   question/friction) → evidence (3–5 facts) → resolution (the takeaway). [2, 5]
5. At least one quantity is shown **pictorially** (pictograms, repeated units,
   proportional icons) — not only as abstract bars. [6, 7]

## Required components (all of them, in this order)

| # | Component | Rules |
|---|-----------|-------|
| 1 | **Headline + hook** | A descriptive title plus one-line hook framed as the question the data answers. Pub test: if you wouldn't say it to a friend, rewrite it. [5] |
| 2 | **Hero stat** | One number, largest element, immediately under the hook, with a one-line plain-words gloss. [4, 5] |
| 3 | **Numbered evidence sections** | 3–5 (eli5: 3–4; junior: 4–5; pro: 5–7). Each is one visual group: number chip on the backbone + icon + short header + fact + micro-visual. [2, 3, 5] |
| 4 | **Backbone with connectors** | Visible or strongly implied spine linking section numbers in order (line, arrows, or alternating rhythm). See layout-archetypes.md. [2, 3] |
| 5 | **Annotation callouts** | 1–3 handwritten-style asides pointing at chart features non-experts would miss ("this spike = July"). Proven to reduce cognitive load (IPCC AR6 technique). [8] |
| 6 | **Takeaway / resolution** | The "so what" — 2–3 plain-words conclusions, visually distinct (this is the story's ending, not another data section). [2, 5] |
| 7 | **Source strip** | Source file name, date range, and the honesty line ("every number computed from the file"). Non-negotiable. [4] |

## Budgets (hard limits, per canvas)

- **Facts**: 3–5 core statistics beyond the hero stat. More = "data vomit". [5]
- **Colors**: 4–5 plus background/text. Each color has a ROLE (primary data,
  secondary, accent/callout, ground) — never variety for its own sake. [4]
- **Typefaces**: 2–3. Display for title/headers, body face, optional mono for
  data labels. Hierarchy = title ≫ section headers ≫ body ≫ labels ≫ source,
  each level distinct in size AND weight; three text levels max per section. [3, 4]
- **Icon style**: exactly ONE (all line, or all solid, or all filled-outline)
  with uniform stroke weight and corner treatment throughout. Header icons
  ~1.5× body icons. An icon that needs a label to be understood has failed. [4, 7v]
- **Text**: captions ≤ 2 short sentences; body copy supports the visual, never
  the reverse. Roughly 50/50 visual-to-text balance. [4, 9]

## Pictograms (ISOTYPE) — research-backed rules

Pictographic representation is not decoration; controlled studies found
pictographs embedded AS the data improve memory under load and engagement,
with no performance cost — while superfluous background imagery distracts. [7]

- Use repeated unit icons for counts and shares: 1 icon = fixed quantity,
  partial quantities by partial fill/tint. State the unit ("1 box = 300
  orders"). [6, 7]
- Discretize: breaking a magnitude into ≤ 4–5 countable units improves
  estimation; beyond that, revert to bars. [7]
- Never scale icon AREA to encode value (misleading); repeat same-size icons
  instead. [6]
- No decorative imagery unattached to data. If it doesn't encode or anchor a
  fact, cut it. [7]

## Cognitive & accessibility floor

- Preattentive attributes (size, color, position) must pre-answer "where do I
  look first" before conscious reading starts. [5]
- Single-path narrative with explicit directional cues — sequential numbering
  is the strongest. [5]
- Contrast ≥ 4.5:1 body text, ≥ 3:1 large text/graphics; never encode meaning
  by color alone (pair with label, pattern, or position); left-aligned text,
  no justified blocks. [5]
- Breathing zones around dense clusters — whitespace is a navigation device,
  not waste. [4, 5]
- Every element anchored to a grid; floating elements read as amateur. [5]

## Level → tone/density mapping (eliviz complexity levels)

| Level | Sections | Captions | Metaphors | Charts |
|-------|----------|----------|-----------|--------|
| `eli5` | 3–4 | one short sentence, everyday words, one analogy each | required (pictograms first) | max 1 series each, annotated |
| `junior` | 4–5 | ≤ 2 sentences, light domain terms | encouraged | up to 2 series, annotated |
| `pro` | 5–7 | terse, precise, no analogies | only where they compress | full chart vocabulary |

The ELI5 voice mandate (SKILL.md) applies at every level for structure labels;
levels change density and diction, not honesty or clarity.

## Verification checklist (run against the rendered PNG)

1. Four-looks test passes (hero → sections → details → nothing).
2. Reading path provable: cover the numbers — is the order still obvious?
3. Every number on canvas is byte-identical to a brief value.
4. Annotations point at real features; no claim contradicts the data shape.
5. One icon style; one palette with roles; no orphan/floating elements.
6. Source strip present; canvas rendered at measured height (nothing clipped).
7. Legible at 25% zoom (thumbnail test — hero stat + title must survive).

## Sources

1. AbSPORU — "Info-poster or infographic? The differences" (absporu.ca)
2. Univ. of Hull LibGuides — Infographics: Structure / Storytelling (libguides.hull.ac.uk)
3. Lu et al., CHI 2020 — "Exploring Visual Information Flows in Infographics" (visual groups, explicit/Gestalt flow hints)
4. MadeGood, "Infographic Design: Tips, Process, Best Practices" (2026); Marq "Infographic Design Guide" (2026); Venngage "What is an Infographic" (2026)
5. Inkbot Design — "Infographics Design" (2026): hero stat, friction-to-fuel arc, preattentive attributes, neuro-inclusive single-path rules
6. Eye Magazine — "Talking pictures (Isotype)"; Rehkämper, "Some remarks on pictorial statistics" (ISI)
7. Haroz, Kosara, Franconeri — "ISOTYPE Visualization: Working Memory, Performance, and Engagement with Pictographs" (CHI 2015)
8. Information is Beautiful Awards 2023 — IPCC AR6 figures (axis icons, handwritten annotations to reduce cognitive load)
9. Common Ninja — "Designing Infographics That Tell a Compelling Story"
