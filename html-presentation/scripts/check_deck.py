#!/usr/bin/env python3
"""Render a built deck headlessly, screenshot every slide, and lint layout.

Reports:
  - JS console errors
  - elements spilling outside the 1920x1080 slide, or into the footer zone
  - clipped content (scrollHeight > clientHeight on overflow-hidden boxes)
  - diagram problems: overlapping nodes, overlapping edge labels, text that
    renders too small because the diagram is too dense for its box
Writes slide-NN.png (final step of each slide) and contact.png (grid of all).

Usage:
    python check_deck.py deck.html [--out shots/] [--steps]   # --steps: one shot per build step
Requires: playwright (chromium) and Pillow.
"""
import argparse, json, sys
from pathlib import Path

LINT_JS = r"""
(i) => {
  const deck = window.deck, s = deck.slides[i], el = s.el;
  const R = el.getBoundingClientRect(), k = R.width / 1920;
  const issues = [];
  const name = n => (n.tagName.toLowerCase() + (n.className && typeof n.className === 'string' ? '.' + n.className.trim().split(/\s+/).join('.') : '') + (n.textContent ? ` "${n.textContent.trim().slice(0, 40)}"` : ''));
  const footerTop = R.bottom - 78 * k;
  const hasFooter = !!el.querySelector(':scope > .slide-footer');
  el.querySelectorAll('*').forEach(n => {
    if (n.closest('svg') && n.tagName !== 'svg') return;
    if (n.closest('.slide-footer') || n.closest('aside.notes')) return;
    const cs = getComputedStyle(n);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'absolute' && n.matches('.slide::after')) return;
    const r = n.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const tol = 2;
    if (r.right > R.right + tol || r.bottom > R.bottom + tol || r.left < R.left - tol || r.top < R.top - tol)
      issues.push(`OUTSIDE SLIDE: ${name(n)} (${Math.round((r.right - R.left) / k)}x${Math.round((r.bottom - R.top) / k)})`);
    else if (hasFooter && r.bottom > footerTop + tol && n.children.length === 0 && n.textContent.trim())
      issues.push(`INTO FOOTER ZONE: ${name(n)}`);
    const hid = v => v === 'hidden' || v === 'clip';
    if (hid(cs.overflowY) && n.scrollHeight > n.clientHeight + 4 && !n.matches('.slide, .bar-track'))
      issues.push(`CLIPPED: ${name(n)} needs ${Math.round(n.scrollHeight)}px tall, has ${Math.round(n.clientHeight)}px`);
    if (hid(cs.overflowX) && n.scrollWidth > n.clientWidth + 4 && !n.matches('.slide, .bar-track'))
      issues.push(`CLIPPED WIDTH: ${name(n)} needs ${Math.round(n.scrollWidth)}px wide, has ${Math.round(n.clientWidth)}px`);
  });
  // diagrams
  el.querySelectorAll('svg.dg').forEach((svg, di) => {
    const vb = svg.viewBox.baseVal; const sr = svg.getBoundingClientRect();
    const scale = Math.min(sr.width / vb.width, sr.height / vb.height) / k;  // svg units -> 1080p px
    const lbl = svg.querySelector('.node-label, .msg text, .seq-head text');
    if (lbl) {
      const fs = parseFloat(lbl.getAttribute('font-size') || getComputedStyle(lbl).fontSize) * scale;
      if (fs < 17) issues.push(`DIAGRAM ${di}: labels render at ~${fs.toFixed(0)}px — too dense; split the diagram, reduce grid, or give it more room`);
    }
    const boxes = [...svg.querySelectorAll('.node:not(.is-hidden) .node-body')].map(n => ({ n, r: n.getBoundingClientRect() }));
    for (let a = 0; a < boxes.length; a++) for (let b = a + 1; b < boxes.length; b++) {
      const A = boxes[a].r, B = boxes[b].r;
      if (A.left < B.right - 2 && B.left < A.right - 2 && A.top < B.bottom - 2 && B.top < A.bottom - 2)
        issues.push(`DIAGRAM ${di}: nodes overlap: ${boxes[a].n.parentNode.dataset.id} / ${boxes[b].n.parentNode.dataset.id}`);
    }
    const labels = [...svg.querySelectorAll('.edge:not(.is-hidden) .edge-label rect')].map(n => ({ n, r: n.getBoundingClientRect() }));
    for (let a = 0; a < labels.length; a++) {
      for (let b = a + 1; b < labels.length; b++) {
        const A = labels[a].r, B = labels[b].r;
        if (A.left < B.right && B.left < A.right && A.top < B.bottom && B.top < A.bottom)
          issues.push(`DIAGRAM ${di}: edge labels overlap: ${labels[a].n.closest('.edge').dataset.id} / ${labels[b].n.closest('.edge').dataset.id}`);
      }
      boxes.forEach(bx => {
        const A = labels[a].r, B = bx.r;
        if (A.left < B.right - 4 && B.left < A.right - 4 && A.top < B.bottom - 4 && B.top < A.bottom - 4)
          issues.push(`DIAGRAM ${di}: edge label "${labels[a].n.nextSibling?.textContent}" sits on node ${bx.n.parentNode.dataset.id}`);
      });
    }
  });
  return { title: s.title, steps: s.stepCount, issues: [...new Set(issues)] };
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--out", default=None)
    ap.add_argument("--steps", action="store_true", help="screenshot every build step, not just the final one")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright

    deck = Path(a.deck).resolve()
    out = Path(a.out or deck.with_suffix("").as_posix() + "-shots"); out.mkdir(parents=True, exist_ok=True)
    errors, report, shots = [], [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        pg.on("console", lambda m: m.type in ("error", "warning") and errors.append(f"{m.type}: {m.text}"))
        pg.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        pg.goto(deck.as_uri())
        pg.wait_for_function("window.deck && window.deck.slides.length > 0", timeout=10000)
        n = pg.evaluate("window.deck.slides.length")
        for i in range(n):
            total = pg.evaluate(f"window.deck.slides[{i}].stepCount")
            steps = range(total + 1) if a.steps else [total]
            for st in steps:
                pg.evaluate(f"window.deck.go({i}, {st}, {{animate:false}})")
                pg.wait_for_timeout(1300)  # let CSS transitions + packets settle
                f = out / (f"slide-{i+1:02d}" + (f"-s{st}" if a.steps else "") + ".png")
                pg.screenshot(path=str(f)); shots.append(f)
            res = pg.evaluate(LINT_JS, i)
            report.append((i + 1, res))
        b.close()

    try:
        from PIL import Image
        thumbs = [Image.open(s).resize((480, 270)) for s in shots]
        cols = 4; rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 490 + 10, rows * 280 + 10), (30, 30, 34))
        for j, t in enumerate(thumbs):
            sheet.paste(t, (10 + (j % cols) * 490, 10 + (j // cols) * 280))
        sheet.save(out / "contact.png")
    except Exception as e:  # pillow optional
        print(f"(contact sheet skipped: {e})")

    bad = 0
    print(f"\n{deck.name}: {len(report)} slides → screenshots in {out}")
    for num, r in report:
        flag = "✗" if r["issues"] else "✓"
        print(f" {flag} {num:02d} [{r['steps']} steps] {r['title'][:70]}")
        for iss in r["issues"][:8]:
            print(f"      - {iss}")
        bad += bool(r["issues"])
    if errors:
        print("\nConsole:")
        for e in dict.fromkeys(errors):
            print("  ", e)
    print(f"\n{'OK' if not bad and not errors else 'NEEDS FIXES'}: {bad} slide(s) with layout issues, {len(set(errors))} console message(s).")
    print(f"Contact sheet: {out / 'contact.png'}")


if __name__ == "__main__":
    main()
