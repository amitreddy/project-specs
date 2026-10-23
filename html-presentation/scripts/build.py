#!/usr/bin/env python3
"""Assemble a deck source file into one standalone HTML presentation.

The source holds only slides (<section class="slide">…</section>) plus any
optional <style>/<script> blocks. The engine CSS + JS are inlined so the
output is a single file with zero network dependencies.

Config can live at the top of the source as an HTML comment:
    <!-- deck: {"title": "Payments Modernisation", "theme": "executive", "lang": "en"} -->
CLI flags override the comment.

Usage:
    python build.py deck.src.html -o deck.html [--title T] [--theme executive|technical|blueprint|product]
                    [--footer "Confidential"] [--webfonts]
"""
import argparse, html, json, re, sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
THEMES = {"executive", "technical", "blueprint", "product"}
WEBFONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800'
            '&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("-o", "--out")
    ap.add_argument("--title"); ap.add_argument("--theme"); ap.add_argument("--footer"); ap.add_argument("--lang")
    ap.add_argument("--webfonts", action="store_true", help="add Google Fonts link (falls back to system fonts offline)")
    a = ap.parse_args()

    src = Path(a.source).read_text(encoding="utf-8")
    cfg = {}
    m = re.search(r"<!--\s*deck:\s*(\{.*?\})\s*-->", src, re.S)
    if m:
        try:
            cfg = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            sys.exit(f"Invalid deck config comment: {e}")
        src = src[:m.start()] + src[m.end():]
    for k in ("title", "theme", "footer", "lang"):
        if getattr(a, k):
            cfg[k] = getattr(a, k)
    if a.webfonts:
        cfg["webfonts"] = True

    theme = cfg.get("theme", "executive")
    if theme not in THEMES:
        sys.exit(f"Unknown theme '{theme}'. Choose one of: {', '.join(sorted(THEMES))}")
    title = cfg.get("title") or (re.search(r"<h1[^>]*>(.*?)</h1>", src, re.S) or [None, "Presentation"])[1]
    title = re.sub(r"<[^>]+>", "", title).strip()

    n_slides = len(re.findall(r'<section[^>]*class="[^"]*\bslide\b', src))
    if n_slides == 0:
        sys.exit("No <section class=\"slide\"> elements found in source.")

    css = (ASSETS / "engine.css").read_text(encoding="utf-8")
    js = (ASSETS / "engine.js").read_text(encoding="utf-8")
    out = f"""<!doctype html>
<html lang="{cfg.get('lang', 'en')}" class="no-js" data-theme="{theme}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="deck-title" content="{html.escape(cfg.get('footer', title))}">
{WEBFONTS if cfg.get('webfonts') else ''}
<style>
{css}
</style>
<script>
{js}
</script>
</head>
<body>
<div class="deck"><div class="stage">
{src.strip()}
</div></div>
</body>
</html>
"""
    dest = Path(a.out) if a.out else Path(a.source).with_name(Path(a.source).name.replace(".src", "") if ".src" in a.source else Path(a.source).stem + ".deck.html")
    dest.write_text(out, encoding="utf-8")
    print(f"Built {dest} — {n_slides} slides, theme={theme}, {len(out) // 1024} KB")


if __name__ == "__main__":
    main()
