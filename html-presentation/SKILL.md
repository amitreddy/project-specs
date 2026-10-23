---
name: html-presentation
description: Build polished, standalone single-file HTML presentations with modern design and purposeful JavaScript animation — animated dataflows, architecture diagrams, flowcharts, swimlanes, sequence diagrams, code walkthroughs, KPI count-ups, roadmaps — tuned to the audience (stakeholder/executive, technical, architecture, product, or mixed). Use this skill whenever the user asks for a presentation, deck, slides, pitch, walkthrough, architecture review, design review, explainer, or "something to present", especially as HTML or when they want animation, flows, diagrams, or to show how data moves through a system — even if they don't say "HTML". Also use it to turn a design doc, spec, or system description into a talk, or to add animated diagrams to an existing deck. Not for .pptx files (use the pptx skill) unless the user wants an HTML alternative.
---

# HTML Presentation

Produce a single `.html` file that opens anywhere (offline, no CDN, no build step for the viewer), presents at 1920×1080 scaled to any screen, and uses motion to *explain* — data visibly moving along edges, systems assembling in the order the story needs, the current idea in focus.

Everything heavy is already built: a zero-dependency engine (`assets/engine.js` + `engine.css`) that you never edit per deck. Your job is the story and the slide markup.

## Why it's built this way

- **Zero dependencies.** Corporate networks block CDNs and decks get emailed. Animation uses the native Web Animations API, CSS transitions and a small rAF loop — no GSAP/Reveal needed, works from `file://`.
- **Declarative diagrams.** You describe nodes on a grid and edges by id in JSON; the engine routes orthogonal edges, spreads ports, sizes groups, fits labels and stretches the grid to the slot. Hand-placing SVG coordinates is where LLM-authored diagrams go wrong, so don't.
- **Object model.** `Deck → Slide → Build | Component`, where `Component` is subclassed by `FlowDiagram`, `SequenceDiagram`, `CodeBlock`, `CountUp`. Every step is applied idempotently from a step index, so forward, back, deep-link (`#/4/2`), overview and print all agree. New behaviours are new `Component` subclasses (see `references/components.md` → Extending).

## Workflow

### 1. Pin down the brief (infer first, ask only what's missing)
Get four things: **audience/tone** (stakeholder · tech · architecture · product · mixed), **the one thing they should leave with** (a decision, an understanding, buy-in), **time slot** (sets slide count), and **source material** (docs, diagrams, code the user has). If the request makes these obvious, don't ask — state your reading in one line and proceed. If the tone is unclear and the deck is substantial, ask that single question.

### 2. Read the audience profile
Open `references/audiences.md` and read the section for the tone. It sets narrative arc, density, vocabulary, theme, diagram depth and motion intensity. Mixed audiences have a specific layering strategy there — read it rather than averaging the tones.

### 3. Storyboard before markup
Write the deck as a list of **action titles** — one sentence per slide stating the takeaway ("One event, four consumers, zero polling", not "Architecture"). Read the titles alone top to bottom: they should tell the whole story. For every diagram slide, also write its step script — what appears, what flows, what gets focus at each click. This is where good decks are made; markup is mechanical afterwards. Show the storyboard to the user first only for long decks (>12 slides) or when the brief was thin.

### 4. Author the source
Create `<name>.src.html` containing only `<section class="slide">` elements (plus optional `<style>`). Use `references/components.md` for every layout, build attribute and the diagram JSON schema. `assets/example.src.html` is a complete 11-slide mixed-audience deck exercising every component — skim it before your first deck; copying its patterns is faster than reading the reference cold.

Put config in the first line:
```html
<!-- deck: {"title": "Payments Modernisation", "theme": "executive", "footer": "Payments · Confidential"} -->
```
Themes: `executive` (warm paper, serif — stakeholders), `technical` (dark, mono accents), `blueprint` (navy grid — architecture), `product` (bright, bold). Any slide can override with `data-theme="…"`, which is how mixed decks drop into a dark deep-dive and back.

Write speaker notes (`<aside class="notes">`) on any slide where the presenter needs a talk track — they show in the presenter window (P) and notes overlay (N), never on the slide.

### 5. Build
```bash
python <skill>/scripts/build.py deck.src.html -o deck.html
```
Inlines the engine → one self-contained file (~100 KB). Add `--webfonts` only if the user wants Inter/JetBrains Mono and will be online; system fonts are the default fallback.

### 6. Verify — always, before delivering
```bash
python <skill>/scripts/check_deck.py deck.html          # add --steps to shoot every build step
```
It renders headless Chromium, screenshots each slide's final step, writes `contact.png`, and reports console errors, overflow, clipped text, overlapping diagram nodes/labels, and diagrams too dense to read. **Look at `contact.png`**, then open individual slides that look off. Fix and rebuild until clean. For diagram-heavy slides, also check a middle step with `--steps` — the final state can hide story problems (e.g. a flow arriving at a node that isn't shown yet).

Typical fixes: label overlaps → give the edge room (spread `at` columns, or move the label with `labelAt`); too dense → split into two slides or drop to the 5–7 nodes that matter; text into footer → cut words, not font size.

### 7. Deliver
Publish as an artifact when the person will present or share it; otherwise send the `.html` file. Tell them in one line how to drive it: **→/Space** next, **←** back, **O** overview, **P** presenter window with notes + timer, **F** fullscreen, **Ctrl/⌘+P** prints one slide per page (diagrams in their complete state). Keep the `.src.html` too in case they want edits.

## Design principles (the "why" behind good output)

- **One idea per slide; the title is the idea.** Supporting content proves the title. If you need two titles, you need two slides.
- **Motion has a job.** Every animation either reveals sequence (what happens first), shows causality (data moving from A to B), or directs attention (focus/dim). Decoration-only motion reads as noise to executives and as gimmick to engineers. Default slide transition is a quiet slide-fade; reserve `zoom` for a statement moment.
- **Diagrams tell a story in steps.** Build systems in the order of the narrative: actors → core path → dependencies → failure/new capability. A good diagram step does one of: *show* new parts, *flow* a packet along a path, or *focus* one area. Caption each step with the sentence the presenter would say.
- **Density follows the audience.** Executives: ≤ 3 points, ≤ ~25 words of body per slide, numbers big. Engineers tolerate more but still one diagram or one code block per slide.
- **Contrast and restraint.** One accent colour carries meaning (current, new, important); semantic tones (good/warn/bad) only for state. Don't colour every node.
- **Text is authored at 1080p.** Body ≥ 24px, diagram labels render ≥ ~17px (the checker enforces this). Never shrink fonts to make content fit — cut content.
- **Accessible by default.** The engine honours `prefers-reduced-motion` (packets off, builds instant, active paths still highlighted) and keeps real text in the DOM/SVG. Don't put meaning in colour alone — pair with labels or line style.

## Complexity ladder

Match the build to the ask; don't over-engineer a 5-minute update.
- **Simple** (status update, 5–8 slides): title, statement, KPIs with count-up, points with builds, ask. No diagrams beyond a small flow.
- **Medium** (design review, 10–15 slides): one or two stepped flow diagrams, a compare, a roadmap, notes on key slides.
- **Complex** (architecture deep-dive, mixed board): stepped architecture with groups and packets, swimlane failure flow, sequence diagram, code walkthrough with line focus, per-slide theme switching, full speaker notes, appendix section.

## Files

- `scripts/build.py` — source → standalone HTML (inlines engine)
- `scripts/check_deck.py` — headless render, screenshots, contact sheet, layout lint
- `assets/engine.js`, `assets/engine.css` — runtime and themes (don't fork per deck; extend via `<style>` or `DeckKit.Deck.register`)
- `assets/example.src.html` — full worked example of every component
- `references/audiences.md` — tone profiles: arcs, density, theme, motion per audience; mixed-audience strategy
- `references/components.md` — authoring reference: layouts, builds, diagram JSON (flow + sequence), code, KPIs, extending
- `references/motion.md` — motion language, step-scripting patterns for dataflows, timing, anti-patterns
