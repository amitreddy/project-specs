# Authoring reference

Contents: 1 Slide anatomy · 2 Layouts · 3 Builds · 4 Flow diagrams · 5 Sequence diagrams · 6 Code · 7 Numbers & charts · 8 Notes, transitions, themes · 9 Extending · 10 Gotchas

All sizes are px on a 1920×1080 stage. Slide padding is 96/120px; the footer (auto) occupies the bottom ~80px.

---

## 1. Slide anatomy
```html
<section class="slide" data-layout="…" data-theme="…" data-transition="…" data-title="…">
  <header>
    <div class="eyebrow">Section · context</div>
    <h2>Action title stating the takeaway</h2>
    <p class="lead">Optional one-line framing.</p>
  </header>
  …content…
  <aside class="notes">Talk track (presenter only).</aside>
</section>
```
The slide is a flex column (gap 40px). Give the main content `class="grow"` (or use `.diagram`, `.split`, `.compare`, which grow already) so it takes the remaining height.
Slide attributes: `data-footer="off"` or `data-footer="custom text"`; `data-title` overrides the title shown in presenter view.

Text utilities: `.lead` `.muted` `.faint` `.small` `.mono` `.hl` (highlighter), `<em>` = accent colour, `.chip` (+ `.accent .good .warn .bad`), `.callout` (+ `.good .warn .bad`). Helpers: `.row` `.stack` `.center` `.grow`.

## 2. Layouts
**Title** — `data-layout="title"`: eyebrow, `h1`, `.lead`, `.meta` with `<span>`s. No footer.
**Section divider** — `data-layout="section"`: `<div class="section-num">02</div><h2>…</h2>`. No footer.
**Statement** — `data-layout="statement"`: `<p class="statement">… <em>key phrase</em> …</p>` (≤ 20 words).

**Split** — `<div class="split">` two children; variants `.wide-left` `.wide-right`.

**Cards** — `<div class="cards" style="--cols:3">` of
```html
<div class="card [accent]"><span class="kicker">Risk</span><h3>Title</h3><p>One or two lines.</p></div>
```
**Points** — `<ul class="points [numbered]"><li>Point<small>supporting line</small></li></ul>`

**KPIs** — `<div class="kpis grow" style="--cols:3; align-content:center">` of
```html
<div class="kpi accent"><div class="kpi-value"><span class="count" data-to="38" data-suffix="%">38%</span></div>
  <div class="kpi-label">Fewer support contacts</div><div class="delta up">≈ $4.1M / yr</div></div>
```
**Compare** — `<div class="compare"><div class="before"><div class="label">Today</div>…</div><div class="after" data-step="1" data-anim="wipe"><div class="label">Target</div>…</div></div>`

**Timeline** — `<div class="timeline grow" style="--cols:4; align-content:center">` of `<div class="milestone done|now"><span class="when">Q1</span><h3>…</h3><p>…</p></div>`

**Table** — `<table class="table">`; `tr.accent` highlights a row, `td.num` right-aligns numbers.

**Ask** — `<div class="ask">` of `<div><div><h3>Decision</h3><p class="muted">detail</p></div></div>` (auto-numbered 01, 02…).

## 3. Builds (progressive reveal)
Any element with `data-step="N"` is hidden until step N of the slide. Same N → revealed together with an automatic 80ms stagger in DOM order.

| Attribute | Effect |
|---|---|
| `data-step="2"` | appear at step 2 |
| `data-anim="fade-up"` (default) `fade` `fade-down` `slide-left` `slide-right` `scale` `blur` `wipe` `pop` | entrance style |
| `data-until="3"` | visible from step to 3, then hides (temporary callouts) |
| `data-dim-after="3"` | dims to 32% from step 3 (keeps context while focus moves on) |

The slide's step count = max of all builds and components; you never declare it. Builds are pure CSS transitions, so they reverse correctly when going back.

## 4. Flow diagrams (architecture, dataflow, flowchart, swimlane)
```html
<div class="diagram" [data-step-start="2"]>
  <script type="application/json">{ …spec… }</script>
</div>
```
The diagram's own steps map to slide steps starting at `data-step-start` (default 1), so you can put builds before it.

### Spec
```jsonc
{
  "cell": [270, 160],        // grid cell size (default). Bigger = more room for edge labels
  "node": [210, 92],         // default node size
  "direction": "lr",         // "lr" | "tb" — biases which sides edges leave from
  "route": "elbow",          // default edge routing: "elbow" | "curve" | "straight"
  "fit": true,               // stretch cells to fill the slot (never shrinks). false to disable
  "caption": "Initial caption (step 0)",
  "lanes":  [{ "label": "Customer", "row": 0, "span": 1 }],          // swimlanes (full-width rows)
  "groups": [{ "id": "vpc", "label": "us-east-1", "nodes": ["a","b"], "tone": "accent", "style": "solid", "pad": 26 }],
  "nodes":  [{ "id": "a", "label": "Order Service", "sub": "Spring Boot", "kind": "service",
               "at": [col, row], "tone": "accent", "badge": "NEW", "size": [w, h], "tip": "hover text" }],
  "edges":  [{ "id": "e1", "from": "a", "to": "b", "label": "publish", "style": "dashed",
               "tone": "good", "dir": "forward", "route": "curve", "fromSide": "r", "toSide": "l",
               "labelAt": 0.5, "bendAt": 0.5, "offset": 0, "via": [[col,row]] }],
  "steps":  [ { …step… } ],
  "legend": [{ "label": "async", "style": "dashed" }, { "label": "new", "tone": "warn", "style": "box" }]
}
```
**Grid:** `at` is `[column, row]` from 0; fractions are fine (`[3.6, 0.95]`) for tidy spacing. Keep ≤ 5 columns × 4 rows for readable labels; the checker warns when text renders < 17px.
**Node kinds:** `service` (default; also `process`, `box`), `gateway` (pill), `db`, `queue`/`topic`/`stream`, `cache`, `function` (hexagon), `actor`/`user`, `external` (dashed), `decision` (diamond), `start`/`end`/`terminal` (filled pill), `note`.
**Tones:** `default` `accent` `accent2` `good` `warn` `bad` `muted`. Use tone for meaning (new, failing, external-owned), not decoration.
**Edges:** id defaults to `"from>to"`. `style`: `solid` (default) `dashed`/`async` `dotted`. `dir`: `forward` `back` `both` `none`. Multiple edges on one node side are auto-spread. `labelAt` moves the label along the path (0–1) when it collides; `bendAt` moves the elbow. `via` routes through grid points for loops/backtracks.
**Labels** auto-shrink and wrap to two lines to fit the node; keep them ≤ ~22 chars and put tech detail in `sub`.

### Steps — each is one click
```jsonc
{ "show": ["id", …],          // reveal nodes/groups/edges (cumulative). Anything ever "shown" starts hidden.
  "hide": ["id"],             // hide again (cumulative)
  "flow": ["a>b>c",           // animate packets along a node path (edges found in either direction)
           { "path": "a>b", "label": "OrderPlaced", "tone": "warn", "count": 2, "speed": 1.2, "loop": true },
           { "edge": "e1", "reverse": true }],
  "highlight": ["b", "a>b"],  // accent outline / edge emphasis (this step only)
  "focus": ["a", "b"],        // highlight these AND dim everything else (this step only)
  "dim": ["c"],               // dim specific items (this step only)
  "pulse": ["b"],             // gentle breathing scale on nodes (this step only)
  "caption": "Sentence the presenter says. <b>Bold</b> allowed." }
```
Edges appear automatically once both endpoints are visible, unless the edge id itself is listed in a `show` (then it waits for that step and draws itself in). Flows mark their edges active (marching dashes) even under reduced motion.

### Step scripts that work
- **Assemble then animate:** step 1 actors+entry point with a flow; step 2 core; step 3 consumers with parallel flows; step 4 `focus` the punchline.
- **Happy → sad path:** step 1 flow happy path + highlight end; step 2 failure flow in `bad` tone; step 3 `focus` recovery components.
- **Before → after on one canvas:** show legacy nodes, then `hide` them and `show` replacements in the same positions.
- **Zoom (mixed decks):** same ids/positions on the exec slide and the deep-dive slide; the deep-dive adds infra nodes via `show`.

## 5. Sequence diagrams
```jsonc
{ "type": "sequence", "gap": 330, "rowH": 74, "stepwise": true,
  "participants": [{ "id": "api", "label": "Order API", "tone": "accent" }],
  "messages": [
    { "from": "api", "to": "db", "label": "INSERT order + outbox", "caption": "…" },
    { "from": "db", "to": "api", "label": "ok", "kind": "reply" },     // dashed return
    { "from": "relay", "to": "relay", "label": "batch" },              // self-message loop
    { "from": "relay", "to": "db", "label": "mark sent", "with": "prev" }, // same step as previous
    { "from": "a", "to": "b", "label": "produce", "payload": "evt", "tone": "bad", "step": 4 },
    { "note": "Crash here → safe replay", "over": ["db", "kafka"] }
  ] }
```
Each message is its own step (draws in, a packet labelled `payload` travels once, current message in accent). `stepwise: false` shows all at once. Keep ≤ 5 participants and ≤ 9 messages per slide; labels ≤ ~40 chars.

## 6. Code walkthroughs
```html
<pre class="code" data-lang="java" data-lines='["1-3", "5-9", "11"]' [data-step-start="1"]>
…code (escape < as &lt;)…</pre>
```
Each entry in `data-lines` is a step focusing those lines (others dim). Light highlighting for C-family/Java/TS/Python/SQL/YAML; `data-lang="json"` keeps `#`/`//` literal, `data-lang="text"` disables. Keep ≤ 15 lines × ~55 chars — long lines auto-shrink but never below 18px, then get clipped (the checker reports it). Escape `<`, `>`, `&` inside the `pre`.

## 7. Numbers & charts
**Count-up:** `<span class="count" data-to="99.95" data-decimals="2" data-prefix="$" data-suffix="%" data-from="0" data-duration="1400">99.95%</span>` — animates when its slide/build becomes visible; the inner text is the no-JS/print fallback.
**Bars:** 
```html
<div class="bars">
  <div class="bar"><span>Label</span><div class="bar-track"><div class="bar-fill" style="--v:72; --i:0; --bar-color:var(--good)"></div></div><span class="bar-val">$1.9M</span></div>
</div>
```
`--v` is percent of track; `--i` staggers. For real charting needs beyond simple bars, draw an inline SVG in a `.split` and follow the same tokens (`var(--accent)` etc.).

## 8. Notes, transitions, themes
- `<aside class="notes">` → presenter window (P: notes, timer, clock, next slide) and notes overlay (N).
- `data-transition`: `slide` (default) `fade` `zoom` `rise` `none`.
- Theme: deck-level in the config comment; per slide via `data-theme`. Colour tokens available in custom CSS: `--bg --surface --surface-2 --ink --ink-2 --ink-3 --line --accent --accent-2 --accent-soft --good --warn --bad --font-display --font-body --font-mono --radius`.
- Custom CSS: put a `<style>` block at the top of the source. Prefer tokens over hex so per-slide themes keep working.

## 9. Extending (custom components)
Add a `<script>` in the source (runs before the deck boots):
```html
<script>
class Typewriter extends DeckKit.Component {
  constructor(el, slide) { super(el, slide); this.full = el.textContent; }
  get stepCount() { return 1; }                    // internal steps this component consumes
  setStep(k, ctx) {                                // k = slide step; ctx = {animate, static}
    const on = this.localStep(k) >= 1;
    this.el.textContent = on ? this.full : '';
  }
  leave() {}                                       // stop timers/rAF when slide exits
}
DeckKit.Deck.register('.typewriter', Typewriter);
</script>
```
Contract: `setStep` must be idempotent (derive state from `k`, never from history) so back/deep-link/print work; honour `ctx.static` (print/overview → render final, no transient effects) and `DeckKit.Motion.reduced`. Use `DeckKit.Motion.play(el, keyframes, opts)` for WAAPI with the shared easing tokens. Listen to `document.addEventListener('deck:change', e => e.detail)` for global hooks.

## 10. Gotchas
- JSON in diagram specs must be strict: double quotes, no trailing commas, no comments.
- Escape `<` and `&` in `pre.code` and in HTML text; diagram labels are plain text (captions allow inline HTML).
- Don't put `data-step` on elements inside `.diagram` — use diagram `steps`.
- A diagram with a `caption` or `legend` reserves ~50–80px; on dense slides drop the `lead` instead of shrinking the diagram.
- If a flow names nodes with no edge between them, the console warns and that segment is skipped — the checker surfaces console warnings.
