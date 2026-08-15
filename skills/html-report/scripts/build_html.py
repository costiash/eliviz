#!/usr/bin/env python3
"""
build_html.py — one-shot: parse input data file(s) and inject the normalized
model into the HTML template, producing a single self-contained viewer.

Usage:
  python build_html.py input1 [input2 ...] -o viewer.html \
         [--title T] [--subtitle S] [--accent HEX] \
         [--max-rows N] [--max-text-chars N] [--max-log-lines N] \
         [--template path/to/template.html] [--cdn]
"""

import argparse
import html as html_mod
import json
import os
import sys

# the parser is shared plugin-wide: <plugin-root>/lib/parse_input.py
_PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(_PLUGIN_ROOT, "lib"))
from parse_input import build_model  # noqa: E402

DATA_PLACEHOLDER = "/*__VIZ_DATA__*/"
CSS_PLACEHOLDER = "/*__DESIGN_CSS__*/"
FONTS_PLACEHOLDER = "<!--__DESIGN_FONTS__-->"
ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "assets"
)
DEFAULT_TEMPLATE = os.path.join(ASSETS_DIR, "template.html")
VENDOR_DIR = os.path.join(ASSETS_DIR, "vendor")
DESIGNS_DIR = os.path.join(ASSETS_DIR, "designs")


def list_designs():
    out = []
    if os.path.isdir(DESIGNS_DIR):
        for d in sorted(os.listdir(DESIGNS_DIR)):
            meta_path = os.path.join(DESIGNS_DIR, d, "design.json")
            if os.path.isfile(meta_path):
                with open(meta_path, encoding="utf-8") as fh:
                    meta = json.load(fh)
                out.append((d, meta))
    return out


def load_design(ref):
    """ref: a bank id (assets/designs/<id>/) or a path to a custom pack
    directory containing design.json and/or design.css."""
    path = ref if os.path.isdir(ref) else os.path.join(DESIGNS_DIR, ref)
    if not os.path.isdir(path):
        ids = ", ".join(d for d, _ in list_designs()) or "none found"
        raise SystemExit(
            f"Unknown design {ref!r}. Bank designs: {ids}. "
            "Or pass a path to a directory with design.json/design.css.")
    meta, css = {}, ""
    meta_path = os.path.join(path, "design.json")
    css_path = os.path.join(path, "design.css")
    if os.path.isfile(meta_path):
        with open(meta_path, encoding="utf-8") as fh:
            meta = json.load(fh)
    if os.path.isfile(css_path):
        with open(css_path, encoding="utf-8") as fh:
            css = fh.read()
    meta.setdefault("id", os.path.basename(os.path.normpath(path)))
    return meta, css


def inline_vendor_libs(html):
    """Replace <script src=... data-vendor="name"> tags with the library
    source inlined, so the output works fully offline. Falls back to the CDN
    tag for any vendor file that is missing."""
    import re

    def repl(match):
        name = match.group("name")
        path = os.path.join(VENDOR_DIR, name)
        if not os.path.isfile(path):
            return match.group(0)  # keep the CDN tag
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        src = src.replace("</script", "<\\/script")
        return f"<script>/* inlined: {name} */\n{src}\n</script>"

    return re.sub(
        r'<script src="[^"]+" data-vendor="(?P<name>[^"]+)"></script>',
        repl, html)


def inject(template_html, model):
    payload = json.dumps(model, ensure_ascii=False)
    # keep the inline <script> block valid regardless of data content
    payload = payload.replace("</", "<\\/")
    if DATA_PLACEHOLDER not in template_html:
        raise SystemExit(
            f"Template is missing the data placeholder {DATA_PLACEHOLDER!r}"
        )
    return template_html.replace(DATA_PLACEHOLDER, payload, 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="*")
    ap.add_argument("-o", "--output", default="viewer.html")
    ap.add_argument("--title", default=None)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--accent", default=None,
                    help="hex accent (overrides the design's accent)")
    ap.add_argument("--design", default="aurora",
                    help="design id from the bank, or a path to a custom "
                         "design pack directory")
    ap.add_argument("--list-designs", action="store_true")
    ap.add_argument("--max-rows", type=int, default=2000)
    ap.add_argument("--max-text-chars", type=int, default=400_000)
    ap.add_argument("--max-log-lines", type=int, default=5000)
    ap.add_argument("--template", default=DEFAULT_TEMPLATE)
    ap.add_argument("--cdn", action="store_true",
                    help="keep CDN <script> tags instead of inlining the "
                         "vendored libraries (smaller file, needs internet)")
    args = ap.parse_args(argv)

    if args.list_designs:
        for did, meta in list_designs():
            print(f"{did:12s} {meta.get('name','')} — {meta.get('tagline','')}")
        return

    if not args.inputs:
        ap.error("at least one input file is required")

    design_meta, design_css = load_design(args.design)
    accent = args.accent or design_meta.get("accent") or "#7c6cff"

    title = args.title
    if not title:
        names = [os.path.splitext(os.path.basename(p))[0] for p in args.inputs]
        title = " · ".join(names[:2]) or "Data Explorer"

    model = build_model(args.inputs, title, args.subtitle, accent,
                        max_rows=args.max_rows,
                        max_text_chars=args.max_text_chars,
                        max_log_lines=args.max_log_lines)
    model["meta"]["design"] = {
        "id": design_meta.get("id"),
        "name": design_meta.get("name", design_meta.get("id")),
        "hero": design_meta.get("hero", "particles"),
        "accent2": design_meta.get("accent2"),
        "accent3": design_meta.get("accent3"),
    }

    with open(args.template, encoding="utf-8") as fh:
        template_html = fh.read()

    # Static <title> so link previews / crawlers see the real name pre-JS.
    template_html = template_html.replace(
        "<title>Data Explorer</title>",
        f"<title>{html_mod.escape(title)}</title>", 1)

    if not args.cdn:
        template_html = inline_vendor_libs(template_html)
    if CSS_PLACEHOLDER in template_html:
        template_html = template_html.replace(
            CSS_PLACEHOLDER, design_css.replace("</style", "<\\/style"), 1)
    fonts_link = design_meta.get("fonts", {}).get("google", "")
    if FONTS_PLACEHOLDER in template_html:
        template_html = template_html.replace(
            FONTS_PLACEHOLDER,
            f'<link href="{fonts_link}" rel="stylesheet">' if fonts_link else "", 1)
    html = inject(template_html, model)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(html)

    size_mb = os.path.getsize(args.output) / 1e6
    types = ", ".join(d["type"] for d in model["datasets"])
    print(f"Wrote {args.output} ({size_mb:.1f} MB) — datasets: {types}")


if __name__ == "__main__":
    main()
