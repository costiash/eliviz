# Infographic design bank — level-keyed, separate from the HTML-report bank

The plugin ships TWO design banks that never mix:

| Bank | Serves | Organized by | Location |
|------|--------|--------------|----------|
| Report bank (existing) | `/eliviz:html-report` | mood / audience (aurora, editorial, brutalist, terminal, neon) | `skills/html-report/assets/designs/<id>/` |
| **Infographic bank (this)** | `/eliviz:infographic` | **complexity level → styles within it** | `skills/infographic/assets/designs/<level>/<id>/` |

The report bank restyles one fixed page template. The infographic bank works
differently: the composer builds fresh HTML per run from the section recipe
(layout-archetypes.md), so a pack here supplies the **component styles** for
that recipe — hero card, number chip, spine, section card, annotation,
pictogram, takeaway, source strip — plus tokens. Layout grammar always comes
from the anatomy/archetype references; packs decide only how it *looks*.

## Why level-keyed

A complexity level is not just word choice — it is a visual register. The
research base (infographic-anatomy.md sources) shows audience determines
density, metaphor load, and formality *simultaneously*; a phosphor-CRT skin on
a 10-year-old's explainer or pastel stickers on a data briefing fails the
audience either way. So the level is chosen FIRST and constrains the design
subset; style choice happens inside the level.

## The bank (3 levels × 3 packs = 9)

Validated exemplars marked ✦ (rendered and verified on the Sales Pulse brief).

### `eli5/` — friendly, chunky, pictogram-first
Register: warm grounds or playful darks, fully rounded shapes, offset "sticker"
shadows, solid/thick icons, ≤3 sections, one idea per card, exclamation energy.

- ✦ `sunshine` — cream ground, coral/amber/teal, ink-navy hero card, podium
  and pictogram devices. The default eli5.
- `space-cadet` — playful dark: deep navy, big glowing dots, rocket/star icon set.
- `crayon` — white ground, saturated primaries, hand-drawn-feel rules and arrows.

### `junior/` — clean modern, approachable-professional
Register: soft cards, gradient or flat accents, line icons (2.2px), 4–5
sections, light annotations, "team meeting" energy.

- ✦ `nightglass` — aurora-descended dark glass adapted to infographic grammar
  (the v2 exemplar). The default junior.
- `cleandeck` — white ground, single blue/teal accent family, corporate-safe.
- `warmpaper` — light editorial ground, friendly serif headers, sans body.

### `pro/` — data-journalism / briefing register
Register: restrained 2-accent palettes, hairline rules, serif display or
grotesk caps, dense annotation, tables allowed, 5–7 sections, formal findings
block, "publication" energy.

- ✦ `broadsheet` — warm paper, Georgia display, ink + one red + one blue,
  numbered squares, kicker + standfirst + findings. The default pro.
- `briefing` — dark terminal-adjacent: near-black, tabular numerals, amber/red
  signal colors, monospace labels.
- `journal` — white scientific: IPCC-style light ground, annotation-heavy,
  muted categorical palette, figure-caption conventions.

## design.json schema (per pack)

```jsonc
{
  "id": "sunshine", "level": "eli5", "name": "Sunshine",
  "tagline": "…", "mood": ["warm","playful","kids","friendly"],
  "ground": "#fff8ec", "dark": false,
  "roles": {                       // anatomy doc: every color has a ROLE
    "ink": "#2b2140", "muted": "#6b5d6e",
    "hero": "#ffb02e",             // hero stat + emphasis
    "chip": "#ff6b57",             // number chips + spine accents
    "annotation": "#ff6b57",       // callouts/asides
    "series": ["#00b8a9","#ffb02e","#b7a6ff","#ffd9a0"]  // chart palette, ≤4
  },
  "type": { "display": "Inter", "body": "Inter", "data": "Inter",
            "display_weight": 900, "google": "" },
  "icons": { "style": "line|solid", "stroke": 2.6, "corner": "round" },
  "shape": { "radius": 28, "shadow": "offset|soft|hairline|none",
             "card_border": "none|hairline" },
  "spine": { "style": "band|line|rule", "chip": "circle|square" },
  "density_ceiling": { "sections": 3, "series_per_chart": 1 }  // level guardrail
}
```

Plus `components.css` implementing the section-recipe classes (`.hero-card`,
`.chip`, `.spine`, `.sec-card`, `.ann`, `.picto-cap`, `.takeaway`, `.src`) in
the pack's register. The composer imports exactly one pack's css per run.

## Selection flow

1. **Level first.** From the user's ask/audience ("for my kid/the team/the
   board" → eli5/junior/pro); when absent and the user is present, ask — the
   level changes the artifact more than any style choice. Default: `junior`.
2. **Pack second**, within the level's subset only: design-adapter agent in
   pick mode, same rubric style as the report bank (mood/best_for matching,
   content over surface keywords). Defaults per level: sunshine / nightglass /
   broadsheet.
3. **Custom/blends** stay design-adapter craft-mode territory — but a crafted
   pack must declare its `level` and respect that level's `density_ceiling`;
   the anatomy checklist is validated against the LEVEL, not the pack.

## Guardrails

- A pack may never override level density ceilings, the anatomy checklist, or
  the honesty rules (numbers verbatim from the brief; source strip mandatory).
- One icon style, ≤5 role colors, per pack — enforced at pack-validation time,
  not per run.
- Cross-bank borrowing is allowed one way only: an infographic pack may cite a
  report pack as its palette ancestor (nightglass ← aurora) so users get a
  consistent family look across both outputs of the same dataset.
