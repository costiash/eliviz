---
name: infographic
description: >-
  Turn a data file (CSV/TSV, Excel, SQLite, JSON/JSONL, Markdown, text, logs)
  into a static, shareable infographic IMAGE — a rendered PNG plus its editable
  HTML source. Composes real infographics (hero stat, numbered story spine,
  pictograms, annotations, takeaway), not styled dashboards. Use this skill
  whenever the user asks for an "infographic", "poster image", "one-pager",
  "social card", "an image I can share", "a PNG of this data", or any static
  picture that tells the data's story — as opposed to an interactive
  report/page/dashboard/viewer, which is the html-report skill. Three
  complexity levels (eli5 / junior / pro) with a level-keyed design bank, six
  layout templates, and an infographic-director agent that writes the
  narrative brief from deterministically parsed numbers.
---

# Infographic

Turn one data file into a static infographic: a single PNG (plus its HTML
source) that tells the data's story with a hero stat, a numbered reading path,
pictograms, annotations, and a takeaway — composed as HTML/SVG and rendered
with headless Chromium. No image-generation APIs, no keys, fully offline,
every number deterministic.

**An infographic is not a poster.** A styled dashboard exported as an image
fails this skill's bar. Read `references/infographic-anatomy.md` before
composing anything — it defines the difference, the required components, the
budgets, and the verification checklist. The other three references cover
backbones (`layout-archetypes.md`), the six layout templates
(`infographic-templates.md`), and the level-keyed style packs
(`infographic-design-bank.md`).

## Content voice — ELI5, always

The `[MODE: ELI5_FOR_DUMMIES]` mandate from the html-report skill applies here
at EVERY level: everyday words, simple comparisons, short sentences, zero
fluff, for every word the canvas says. Levels change density and diction — an
eli5 canvas says "1 in 4 boxes came back", a pro canvas says "return rate
25.4%" — but never honesty or clarity. Column names and data values are the
user's data; never rewrite those.

## Complexity levels (chosen FIRST)

| Level | Default when | Sections | Register |
|-------|-------------|----------|----------|
| `eli5` | audience is beginners/kids ("for my kid", "explain simply") | 3–4 | chunky, pictogram-first, one idea per card |
| `junior` | **overall default** | 4–5 | clean modern, light annotations |
| `pro` | analysts/stakeholders ("for the board", "briefing") | 5–7 | dense, terse, tables allowed, findings block |

The level constrains everything downstream: template subset, style pack
subset, section count, chart complexity. If the audience is genuinely unclear
and the user is present, ask — the level changes the artifact more than any
style choice. Selection order is always: **level → template → style pack**.

## The pipeline (run all seven steps, in order)

1. **Parse** — deterministic facts only:
   ```bash
   python <plugin-root>/lib/parse_input.py input.csv -o normalized.json
   ```
   The parser computes everything a brief may cite: per-column stats
   (min/max/sum/mean/median), and for tables an `aggregates` block with
   group-by counts/shares/sums/means/rates plus time buckets and peak deltas
   (see html-report's `references/data-model.md`). **No other number source
   exists.** If a story needs a number the parser didn't emit, the story
   changes — nobody computes numbers downstream.

2. **Brief** — spawn the `infographic-director` agent (ships with this
   plugin; use the Agent tool). Send it: the normalized JSON path, the chosen
   level, the user's ask verbatim, and this skill's directory path. It
   returns the brief: narrative, archetype + backbone + template + style-pack
   choice, and 3–7 facts copied verbatim from parser output. If the Agent
   tool is unavailable, apply `agents/infographic-director.md` yourself and
   say so in one line.

3. **Validate the brief** against the anatomy checklist
   (`references/infographic-anatomy.md`): one hero stat, 3–5 evidence facts
   within the level's budget, every fact value byte-identical to a parser
   value, a takeaway, a source line. Reject and re-brief rather than patch
   silently.

4. **Compose** the poster HTML: template skeleton + the chosen pack's
   `components.css` inlined at `/*__PACK_COMPONENTS_CSS__*/` + your markup.
   Skeletons for the validated templates are in `assets/templates/` (T1
   verdict-card, T4 journey-spine, T6 broadsheet-brief); T2/T3/T5 are
   composed directly from the grammar in `references/infographic-templates.md`.
   Micro-visuals are hand-sized inline SVGs using the pack's `--series-*`
   tokens. Charts show the brief's numbers — display formatting (thousands
   separators, `$1.49M`-style abbreviation, whole-dollar rounding) is the
   only transformation allowed.

5. **Render**:
   ```bash
   python scripts/render_png.py poster.html -o poster.png --width 1080
   ```
   Height is measured from the document, never guessed. `--width` matches
   the canvas preset (story/square 1080, wide 1920, T1 composes at 1200).

6. **Verify visually** — read the PNG and run BOTH checklists: the anatomy
   verification checklist and the template's own additions (semantic-color
   audit, glyph-dialect audit). Check every number on canvas against the
   brief. Nothing clipped, legible at thumbnail size. Iterate until it
   passes; one loop is normal.

7. **Deliver BOTH files** — the PNG and its HTML source, every run. The HTML
   is the editable master; say so when delivering.

## How it works

```
infographic/
├── SKILL.md
├── scripts/
│   └── render_png.py         # HTML → measured full-page PNG at 2x (Playwright)
├── references/
│   ├── infographic-anatomy.md    # what an infographic IS; budgets; checklist
│   ├── layout-archetypes.md      # backbones, section recipe, canvas presets
│   ├── infographic-templates.md  # the six layout grammars + selection matrix
│   └── infographic-design-bank.md # level-keyed packs, token schema, guardrails
└── assets/
    ├── templates/            # skeletons for the validated grammars: T1, T4, T6
    └── designs/<level>/<id>/ # style packs: design.json + components.css
        ├── eli5/sunshine     ├── junior/nightglass     └── pro/broadsheet
```

The parser is shared with the html-report skill: one parser, one source of
truth for numbers, at `<plugin-root>/lib/parse_input.py`.

## Templates and packs

Template selection (after level) follows the matrix in
`references/infographic-templates.md`: statistical stories → T4 (pro: T6),
verdicts/audits → T1, taxonomies → T2/T5, architectures → T3, highlight reels
→ T5. Compatibility is enforced: T1 light packs only, T3 dark packs only,
T6 pro packs only.

The design bank is level-keyed (`assets/designs/<level>/<id>/`): `sunshine`
(eli5), `nightglass` (junior), `broadsheet` (pro) ship validated; the other
six in the bank doc (space-cadet, crayon, cleandeck, warmpaper, briefing,
journal) are specced as roadmap. Custom or blended packs are the
`design-adapter` agent's craft mode — a crafted infographic pack must declare
its `level` and respect that level's `density_ceiling`.

## Locked rules (not style choices)

- **Numbers**: computed only by `lib/parse_input.py`; the brief copies them
  verbatim; every rendered number is byte-traceable to the brief (standard
  display formatting excepted). The director selects and arranges numbers —
  it never computes them. Display formatting means: thousands separators,
  `$1.49M`-style abbreviation rounded to the displayed precision, whole-unit
  rounding, everyday ratio framing ("1 in 4" for a 25.4% rate), and pictogram
  scale declarations ("1 box = 300 orders"). The two framings carry strict
  conditions: ratio framing ONLY when the exact brief value also appears on
  the canvas (fact text, caption, or annotation — the way the exemplars pair
  "1 came back" with "the 25.4% that returned"); a pictogram unit U ONLY when
  U × icon-count exactly equals a brief total that is shown on the canvas AND
  the caption states the unit (ISOTYPE rule: 1 icon = fixed quantity). "Per
  day"-style glosses are NOT display formatting — use the parser's
  `aggregates.by_time.per_day` values.
- **Color semantics**: green=pass, amber=caution, red=risk, blue=info,
  purple=meta. Packs tune hues, never meanings.
- **One icon dialect per canvas** (emoji-glyph OR line OR solid).
- **Canvas**: measured height always; `story` 1080w default, `square`, `wide`.
- **Source strip** on every canvas: file name, date range, honesty line.
- **Both artifacts delivered every run**: PNG + HTML source.
