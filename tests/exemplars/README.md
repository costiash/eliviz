# Exemplar fixtures — the infographic regression targets

These files are **spec, not decoration**. They are the validated exemplars the
v1.1.0 infographic pipeline was built against, and the targets its release
campaign regressed on. Treat any visual or numeric drift against them as a
defect until proven otherwise.

| File | What it pins |
|---|---|
| `sales_pulse.csv` | The canonical demo dataset (seeded, reproducible) every exemplar derives from |
| `brief.json` | The infographic-director's output-contract exemplar — every value is parser-verbatim (regenerate it from `lib/parse_input.py` output if the parser's aggregates ever change) |
| `sunshine.eli5.html` | T4 journey-spine × eli5/sunshine pack |
| `journey-spine.nightglass.junior.html` | T4 × junior/nightglass |
| `broadsheet.pro.html` | T6 broadsheet-brief × pro/broadsheet |
| `verdict-card.eli5.html` | T1 verdict-card (self-skinned light dialect), 1200px canvas |

## Why HTML, not PNG

The HTML is the canonical target; a PNG is derived from it deterministically —
but only within one environment (font rasterization differs across machines).
Committing PNGs would bake one machine's rendering into history. Instead,
regenerate baselines where the regression runs:

```bash
python skills/infographic/scripts/render_png.py tests/exemplars/sunshine.eli5.html --width 1080
python skills/infographic/scripts/render_png.py tests/exemplars/journey-spine.nightglass.junior.html --width 1080
python skills/infographic/scripts/render_png.py tests/exemplars/broadsheet.pro.html --width 1080
python skills/infographic/scripts/render_png.py tests/exemplars/verdict-card.eli5.html --width 1200
```

## How the regression works (validated tolerance)

Rebuild each poster through the pipeline (template skeleton +
`assets/designs/<level>/<id>/components.css` + exemplar content), render both
with `render_png.py` in the same environment, then compare:

- dimensions must match **exactly** (height is measured, never guessed);
- pixels differing by more than 16 gray levels must stay **≤ 2%** of the
  canvas (same-environment antialiasing noise lands well under this).

## Honesty invariants these fixtures encode

- Every number on every canvas traces to `lib/parse_input.py` output for
  `sales_pulse.csv` under the display-formatting rules in
  `skills/infographic/SKILL.md` (separators, precision-rounded abbreviation
  like `$1.49M`/`$5.5k`, whole-unit rounding, the ratio-framing and
  pictogram-scale carve-outs with their exact-value-on-canvas conditions).
- `brief.json` values are byte-identical to parser output — no pre-rounding.
- Color semantics are fixed (green=pass, amber=caution, red=risk, blue=info,
  purple=meta); one icon dialect per canvas; source strip present on all four.

These fixtures are not shipped in the plugin install payload — they exist for
development and regression only.
