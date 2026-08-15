---
name: html-report
description: >-
  Parse data files of many formats — CSV/TSV, Excel (.xlsx), SQLite, JSONL/NDJSON,
  JSON, Markdown, plain text, and log files — and generate a stunning,
  self-contained, single-file HTML experience that visualizes the data: a Three.js
  animated hero, GSAP scroll animations, Tailwind styling, column-profiled data
  tables with search/sort/pagination, histograms and time-series charts, a
  markdown reading view with outline navigation, a filterable log viewer, and a
  collapsible tree explorer for arbitrary JSON. Use this skill whenever the user
  uploads or points at a data file (spreadsheet, export, database, document, log)
  and wants to "visualize", "explore", "browse", "display", or "turn into a
  webpage" that data, or asks for an interactive "report", "page", "dashboard",
  "viewer", or "UI" for it — even if they don't say "HTML" explicitly. Not for
  static image asks ("infographic", "poster image", "PNG I can share") — that is
  the separate infographic skill. Ships a five-style design bank (dark glass,
  editorial light, brutalist, terminal CRT, neon cyberpunk) that is auto-picked
  per dataset, and pairs with the design-adapter agent for custom branding,
  new moods, or blended styles.
---

# Visualizer

Turn almost any data file into a single, self-contained HTML page with an
award-caliber UI: a Three.js particle hero, GSAP-driven scroll storytelling,
animated stat counters, SVG charts, and a per-format interactive experience —
profiled sortable tables for tabular data, an outline-navigated reading view for
markdown, a level-filterable viewer for logs, and a lazy tree explorer for
arbitrary JSON.

The heavy lifting is deterministic and lives in bundled scripts — run them rather
than re-implementing parsing or hand-writing the whole page from scratch. Your
judgment goes into tailoring: titles, accent colors, and any bespoke sections the
user asks for.

## Content voice — ELI5, always

Every word a generated page says to its reader follows this mode. It is not
optional and it is independent of the visual design (a brutalist page and an
editorial page speak the same way):

```
[MODE: ELI5_FOR_DUMMIES]
- Target Audience: A smart 10-year-old or absolute beginner.
- Vocabulary Level: Basic, everyday words only. No industry jargon.
- Rule 1: Explain complex terms using a simple real-world comparison
          (like toys, cooking, or driving).
- Rule 2: Keep sentences short and punchy.
- Rule 3: Use bullet points for steps.
- Rule 4: Zero fluff. Skip long intros.
```

The template's built-in copy already speaks this way ("a column is like a
labeled jar", "a log is a diary your software writes") — keep it that way. The
mode applies to EVERYTHING you add on top:

- `--title` and `--subtitle` values you write
- any custom sections, labels, or chart captions added via a template copy
- the note chips explaining caps and truncation
- the chat message delivering the page

Column names, cell values, and log lines are the user's DATA — never rewrite
those. The rule covers the page's own words, not the data it displays. When
editing the template, jargon in code comments is fine; jargon in rendered text
is a bug.

## Quick start (the 90% case)

One command parses the input(s), detects the format, normalizes the data, injects
it into the template, and writes the final HTML:

```bash
python scripts/build_html.py <input1> [input2 ...] -o viewer.html --title "My Data"
```

- Accepted inputs: `.csv` `.tsv` `.jsonl` `.ndjson` `.json` `.xlsx` `.xlsm`
  `.sqlite` `.sqlite3` `.db` `.md` `.markdown` `.txt` `.log` — plus unknown
  extensions, which are content-sniffed (JSON → tree/table, delimited → table,
  log-shaped → log viewer, otherwise → text).
- Multiple inputs become switchable datasets (tabs) in one page. Multi-sheet
  Excel files and multi-table SQLite databases automatically expand into one tab
  per sheet/table.
- JSON arrays of flat records are **promoted to the tabular dashboard** (column
  profiling, charts, sortable table) instead of the raw tree — the tree explorer
  remains the fallback for nested/irregular JSON.
- Useful flags: `--design` (design pack — see "The design bank" below),
  `--title` (hero title), `--subtitle` (hero subtitle), `--accent` (hex color,
  overrides the design's accent), `--max-rows` (rows embedded in the page,
  default 2000 — stats always cover ALL rows), `--max-text-chars` (default
  400k), `--max-log-lines` (default 5000).
- The output is a single file with all three JS libraries inlined (fully
  offline-capable). Pass `--cdn` for a much smaller file that loads Tailwind,
  GSAP, and Three.js from CDNs instead.
- Excel input needs `openpyxl` (`pip install openpyxl --break-system-packages`
  if missing); everything else is stdlib.

Then ALWAYS open-verify before delivering: render the file headless and look at a
screenshot (see "Verify" below). Deliver the HTML file to the user.

## How it works

```
<plugin-root>/lib/
└── parse_input.py        # SHARED parser: format detection + normalization →
                          # normalized JSON (both eliviz skills call this one file)
html-report/
├── SKILL.md
├── scripts/
│   └── build_html.py     # parse (via ../../lib) + inject data into the template → final HTML
├── references/
│   ├── data-model.md     # detection rules + exact normalized dataset schemas
│   ├── design-spec.md    # the visual language, animation specs, extension guide
│   └── design-bank.md    # design pack anatomy, override hooks, blending rules
└── assets/
    ├── template.html     # the full viewer template (data placeholder inside)
    ├── designs/          # the design bank: aurora, editorial, brutalist, terminal, neon
    └── vendor/           # tailwind, gsap, ScrollTrigger, three (for inlining)
```

`parse_input.py` detects each input as one of four dataset types:

| Dataset type | Sources                                              | Experience                                                        |
|--------------|------------------------------------------------------|-------------------------------------------------------------------|
| `table`      | csv, tsv, jsonl, xlsx sheets, sqlite tables, record-shaped JSON | stat cards, time-series, column-type donut, per-column profile cards (histograms / top values / ranges), searchable + sortable + paginated table, column drill-down modal |
| `text`       | md, txt (non-log)                                    | word/reading stats, top-words chart, outline sidebar, rendered markdown or plain-text reading view |
| `log`        | .log, or text that sniffs as a log                   | level donut, lines-per-day and hour-of-day charts, top sources, level-filterable searchable line viewer |
| `generic`    | any other JSON shape                                 | node/depth/type stats, type donut, top-keys chart, lazy collapsible tree explorer |

Column types (number / text / date / boolean) are inferred with a 90% threshold
over non-null values; numeric columns get precomputed 20-bin histograms, date
columns drive the rows-over-time chart, so the template's charts and counters are
driven by real numbers. Run the parser standalone
(`python <plugin-root>/lib/parse_input.py input.csv -o normalized.json`) only
when you need to inspect or post-process the normalized model; otherwise
`build_html.py` does everything. Numeric columns also carry a `sum`, and table
datasets carry a deterministic `aggregates` block (group-by counts/sums/means/
rates and time buckets) — see `references/data-model.md`.

## The design bank

Five complete visual identities ship in `assets/designs/`; each is a
`design.json` + `design.css` pack applied with `--design <id>`
(`--list-designs` prints them):

| id          | Look                                                        | Reach for it when |
|-------------|-------------------------------------------------------------|-------------------|
| `aurora`    | dark glassmorphism, violet/cyan/pink, particle hero         | default — mixed data, dashboards |
| `editorial` | warm paper, italic serif display, hairline rules            | reports, documents, stakeholder/print audiences |
| `brutalist` | stark ground, 2px black borders, hard offset shadows        | portfolios, launches, "bold/loud" asks |
| `terminal`  | phosphor-green CRT, scanlines, all-mono, cursor blink       | logs, dev data, sqlite dumps, ops |
| `neon`      | violet night, magenta/cyan glow, techno display type        | gaming/social/marketing data, "flashy" asks |

**The `design-adapter` agent chooses, always.** Design selection is the
agent's job, not yours. For every build, spawn `design-adapter` (ships with
this plugin — use the Agent tool) in **pick mode**: send it a short profile —
dataset types and sizes, what the data is about, who will read it, and the
user's request verbatim, plus the skill directory path — and build with the
design id it returns, quoting its one-line rationale when delivering. The only
exception: the user explicitly named a bank design ("use neon", "the editorial
one") — then just use it, no agent needed.

The same agent handles **craft mode** whenever the request implies a design
the bank doesn't hold verbatim: brand colors or "match our site", a mood
outside the bank's range, or a blend ("editorial but dark", "terminal but
softer"). Give it: the original input files, the built page's title, the skill
directory path, and the user's styling brief, verbatim. It authors a custom
pack, rebuilds, screenshot-verifies, and returns the pack + page — deliver its
page as usual. Small tweaks (just a different accent) don't need craft mode:
`--accent` handles that.

If the Agent tool is unavailable in the session, fall back to applying the
pick-mode rubric from `references/design-bank.md` yourself and say so in one
line.

## When to customize vs. when to just run it

- User wants a viewer for their data → just run `build_html.py` with the
  auto-picked design. Do not hand-roll a new page; the template already handles
  all four dataset types.
- User wants different branding/mood → `--design`, then `--accent`; beyond
  that, spawn the `design-adapter` agent (above). Custom packs it produces are
  passed as `--design <pack-dir>`.
- Structural changes (new sections, different charts, layout changes — things
  no design pack can express) → copy `assets/template.html` to the working
  directory, edit the copy, and pass `--template <copy>`. Read
  `references/design-spec.md` first — it documents the template's section
  anatomy, CSS variables, JS entry points, and the safe extension seams.
- Input is huge, unusual, or a format the parser mis-detects → read
  `references/data-model.md` for the normalized model, the detection order, and
  the size-capping rules before changing anything.

## Verify (always)

The page must actually render — a blank hero or a JS error is a failed delivery.
After building:

```bash
python - <<'EOF'
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1440,'height':900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file:///ABS/PATH/viewer.html')
        await pg.wait_for_timeout(3500)
        await pg.screenshot(path='shot_hero.png')
        await pg.evaluate('window.scrollTo(0, document.body.scrollHeight*0.45)')
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path='shot_mid.png')
        print('JS errors:', errs or 'none')
        await b.close()
asyncio.run(main())
EOF
```

Read the screenshots. Check: hero text visible over the particle canvas, stat
counters populated (not zeros unless truly zero — mid-animation values are fine),
charts drawn, cards/table/log lines present. If a CDN is unreachable in your
sandbox (only relevant with `--cdn`) the page degrades gracefully (the template
has a no-WebGL/no-lib fallback) — note that to the user rather than treating it
as a bug, and spot-check the DOM contains the data instead.

## Output expectations

- Exactly one `.html` file is the deliverable; deliver it to the user directly.
- Never leak absolute container paths into the page.
- The page is responsive (mobile → wide desktop), respects
  `prefers-reduced-motion`, and — with the default inlined libraries — works
  fully offline.
- Nothing is silently dropped: capped tables/logs/documents say so in an amber
  note chip, and stats always cover the full input even when the embedded rows
  or lines are capped.
- Every word the page says to its reader passes the ELI5_FOR_DUMMIES check
  (see "Content voice" above): a smart 10-year-old could read any label,
  subtitle, or note on the page and get it.
