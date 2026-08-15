#!/usr/bin/env python3
"""
render_png.py — render a composed infographic HTML file to a PNG.

Deterministic and offline: local Chromium via Playwright, no network, no keys.
The canvas height is MEASURED from the document after fonts settle — never
guessed — so nothing is ever clipped. Renders at 2x device scale.

Usage:
  python render_png.py poster.html [-o poster.png] [--width 1080] [--scale 2]

--width must match the canvas preset the HTML was composed for
(story/square: 1080, wide: 1920; T1 verdict-card composes at 1200).

Requires: pip install playwright && python -m playwright install chromium
"""

import argparse
import os
import sys


def render(html_path, out_path, width, scale):
    from playwright.sync_api import sync_playwright

    url = "file://" + os.path.abspath(html_path)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": 800},
            device_scale_factor=scale,
        )
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url)
        page.evaluate("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(400)  # let fonts/layout settle
        height = page.evaluate(
            "Math.max(document.body.scrollHeight, "
            "document.documentElement.scrollHeight)")
        page.set_viewport_size({"width": width, "height": height})
        page.wait_for_timeout(150)
        page.screenshot(path=out_path, full_page=True)
        browser.close()
    return height, errors


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="composed infographic HTML file")
    ap.add_argument("-o", "--output", default=None,
                    help="output PNG path (default: input name with .png)")
    ap.add_argument("--width", type=int, default=1080,
                    help="canvas CSS width in px (default 1080)")
    ap.add_argument("--scale", type=int, default=2,
                    help="device scale factor (default 2)")
    args = ap.parse_args(argv)

    out = args.output or os.path.splitext(args.input)[0] + ".png"
    height, errors = render(args.input, out, args.width, args.scale)

    size_kb = os.path.getsize(out) / 1024
    print(f"Wrote {out} — {args.width}x{height} css px at {args.scale}x "
          f"({size_kb:.0f} KB)")
    if errors:
        print("JS errors during render (fix before delivering):",
              file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
