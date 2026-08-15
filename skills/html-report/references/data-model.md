# Data model

Two layers: the **input formats** the parser detects, and the **normalized
model** the HTML template consumes. If you change one side, keep the other in
sync.

## 1. Detection rules (parse_input.py)

By extension first:

| Extension                      | Loader        | Dataset type(s)                    |
|--------------------------------|---------------|------------------------------------|
| `.csv`                         | `load_csv` (`,`) | `table`                         |
| `.tsv`                         | `load_csv` (`\t`) | `table`                        |
| `.jsonl` `.ndjson`             | `load_jsonl`  | `table` (all-dict lines) else `generic` |
| `.json`                        | `load_json`   | `table` (record-shaped) else `generic` |
| `.xlsx` `.xlsm`                | `load_xlsx`   | one `table` per sheet (≤8 sheets)  |
| `.sqlite` `.sqlite3` `.db`     | `load_sqlite` | one `table` per table (≤8 tables, ≤100k rows scanned each) |
| `.md` `.markdown`              | `load_text_like` | `text` (markdown)               |
| `.log`                         | `load_text_like` | `log`                           |

Unknown extension → content sniff, in order:

1. `SQLite format 3` magic bytes → sqlite loader
2. undecodable as UTF-8 → hard error (unsupported binary)
3. leading `{`/`[` and valid JSON → json loader
4. first line has ≥2 commas or tabs and csv parses → csv loader (sniffed delimiter)
5. ≥50% of the first 200 non-blank lines carry a timestamp or level token → `log`
6. markdown headings in the first 4k chars → `text` (markdown), else `text` (plain)

**Record-shaped JSON** (`looks_like_records`): a list of ≥2 items where ≥95% of a
200-item sample are dicts, the key universe is ≤120 keys, ≥40% of keys appear in
≥60% of items, and scalar values outnumber nested ones ≥2:1. Such lists get the
tabular dashboard; everything else stays a `generic` tree.

The strings `""`, `"None"`, `"null"`, `"NULL"`, `"NaN"`, `"nan"` are treated as
missing everywhere (`clean()`).

## 2. Normalized model (what the template reads)

Injected into the template via an inline
`<script type="application/json" id="viz-data">` tag replacing the literal
`/*__VIZ_DATA__*/`. `</` is escaped as `<\/` during injection — keep that if you
re-implement injection.

```jsonc
{
  "meta": {
    "title": "…", "subtitle": "…", "accent": "#7c6cff",
    "generated_at": "ISO date", "sources": ["sales.csv"]
  },
  "datasets": [ { "id": "ds0", "type": "…", "label": "…", … } ]
}
```

### type: "table" dataset

```jsonc
{
  "id": "ds0", "type": "table", "label": "sales.csv",
  "stats": {
    "row_count": 1200, "col_count": 9, "cell_count": 10800,
    "null_cells": 473, "filled_pct": 95.6,
    "numeric_cols": 3, "text_cols": 4, "date_cols": 1, "bool_cols": 1,
    "source_format": "csv" | "tsv" | "json" | "jsonl" | "xlsx" | "sqlite"
  },
  "columns": [
    { "name": "quantity", "type": "number", "nulls": 0, "distinct": 40,
      "min": 1, "max": 40, "sum": 23880, "mean": 19.9, "median": 20,
      "histogram": [ { "label": "1–2.95", "count": 31 } ] },     // 20 bins
    { "name": "region", "type": "string", "nulls": 0, "distinct": 4,
      "top_values": [ { "value": "EMEA", "count": 312 } ],       // top 10
      "avg_len": 4.2 },
    { "name": "date", "type": "date", "nulls": 0, "distinct": 190,
      "min": "2026-01-01T00:00:00", "max": "2026-07-28T00:00:00" },
    { "name": "returned", "type": "boolean", "nulls": 0, "distinct": 2,
      "true_count": 298, "false_count": 902, "true_pct": 24.8 }
  ],
  "timeseries": {                       // null if no date column
    "column": "date", "unit": "hour"|"day"|"month"|"year",
    "points": [ { "label": "2026-01", "count": 171 } ]
  },
  "aggregates": {                       // null if no categorical AND no date col
    "by_category": {                    // string cols with 2–12 distinct values (max 4 cols)
      "region": {
        "counts":    { "EMEA": 312, … },          // rows per value
        "share_pct": { "EMEA": 26.0, … },         // 1 decimal
        "sums":  { "total": { "EMEA": 329170.93, … } },   // per numeric col (max 6), 2 decimals
        "means": { "total": { "EMEA": 1272.19, … } },     // 2 decimals
        "rates_pct": { "returned": { "EMEA": 26.5, … } }  // per boolean col, % true, 1 decimal
      }
    },
    "by_time": {                        // first date column, same bucketing as timeseries
      "column": "date", "unit": "month",
      "counts": { "2026-01": 131, … },
      "sums": { "total": { "2026-01": 158472.26, … } },
      "peak": { "bucket": "2026-07", "count": 153,
                "pct_vs_prev": 28.6,          // vs the previous bucket
                "pct_vs_mean_others": 16.9 }  // vs the mean of all other buckets
    },
    "row_basis": 1200                   // rows the aggregates cover (always ALL rows)
  },
  "rows": [ [ "ORD-1000", "2026-03-05", …, 26, 79.16, false, null ], … ],
  "capped": false, "note": null
}
```

Duplicate header names are uniquified on ingest — the first occurrence keeps
its name, later collisions become `"name (2)"`, `"name (3)"`, … — so every
physical column profiles and aggregates independently.

Column types are inferred over non-null values with a 90% threshold, tested in
the order boolean → number → date → string. Numbers accept thousands separators
and scientific notation; dates accept ISO-8601 plus a handful of common formats.
Cells embedded in `rows` are display-safe: strings capped at 300 chars,
dicts/lists JSON-stringified, NaN/Inf → null. `rows` is capped at `--max-rows`
(default 2000) with `capped: true` and a note; **column stats and the timeseries
always cover ALL rows**. Columns are capped at 60 (noted).

The timeseries buckets by the first date column: hour (≤1 day span), day
(≤120 days, zero-filled), month (≤~10 years), else year.

`aggregates` exists so downstream consumers — the infographic skill's brief, or
any custom section you add — can copy every number verbatim instead of computing
their own. Rounding conventions: sums/means 2 decimals, shares/rates/percent
deltas 1 decimal. It is bounded by design: categorical columns need 2–12
distinct values (first 4 qualify), numeric columns cap at 6.

### type: "text" dataset

```jsonc
{
  "id", "type": "text", "label": "guide.md",
  "format": "markdown" | "plain",
  "stats": { "words": 122, "chars": 1580, "lines": 54, "paragraphs": 22,
             "headings": 9, "code_blocks": 1, "links": 1, "reading_minutes": 1 },
  "outline": [ { "level": 2, "text": "Prerequisites" } ],   // md only, ≤60
  "top_words": [ { "word": "staging", "count": 4 } ],        // top 12, stopword-filtered
  "content": "…",             // capped at --max-text-chars (default 400k)
  "capped": false, "note": null
}
```

### type: "log" dataset

```jsonc
{
  "id", "type": "log", "label": "app.log",
  "stats": {
    "total_lines": 2500, "leveled_lines": 2500, "timestamped_lines": 2500,
    "levels": [ { "level": "INFO", "count": 1743 } ],   // WARN/ERROR normalized
    "error_count": 131, "error_pct": 5.2,
    "by_date": [ { "date": "2026-08-01", "count": 288 } ],  // zero-filled ≤400 days
    "by_hour": [24 ints],
    "date_range": ["ISO", "ISO"] | null, "days_span": 9,
    "top_sources": [ { "name": "db.pool", "count": 497 } ]  // from [bracketed] tokens
  },
  "lines": [ { "raw": "…", "level": "ERROR" | null } ],  // capped at --max-log-lines
  "capped": false, "note": null
}
```

Level aliases are normalized (`WARNING→WARN`, `SEVERE/CRITICAL/FATAL/PANIC→ERROR`,
`NOTICE→INFO`, `TRACE→DEBUG`). Timestamps recognized: ISO-ish, Apache CLF, and
syslog (year assumed current). Individual lines are capped at 600 chars.

### type: "generic" dataset

```jsonc
{
  "id", "type": "generic", "label": "config.json",
  "stats": {
    "root_type": "object" | "array" | "value",
    "total_nodes": 15234, "max_depth": 7,
    "type_counts": { "object": n, "array": n, "string": n, "number": n, "boolean": n, "null": n },
    "top_keys": [ { "key": "uuid", "count": 321 } ]   // top 15
  },
  "data": <the JSON itself>,   // size-capped, see below
  "capped": false, "note": null | "arrays truncated to first 200 items"
}
```

**Size capping (generic only):** if the serialized payload exceeds ~2 MB, arrays
are truncated to their first 200 elements (recursively) and `capped: true` is
set; the template shows the note.

## 3. Gotchas

- Timestamps are parsed leniently and never crash on a bad date — the value is
  simply omitted from date stats.
- CSV sniffing can misfire on exotic delimiters; `load_csv(path, None, …)` falls
  back to `,` if the sniffer fails. Pass an explicit delimiter when patching.
- JSONL lines that fail to parse are skipped and counted in the dataset note —
  never dropped silently.
- Excel loads with `data_only=True`: formulas arrive as their cached values (or
  None if the workbook was never opened by Excel).
- SQLite opens read-only (`mode=ro`); table names are quoted but exotic names
  (embedded quotes) would need extra escaping if you extend this.
- A single-row CSV is treated as data with generated `col_N` headers, not as a
  header-only table.
- Never render an empty heading/label — fall back to a filename or placeholder.
