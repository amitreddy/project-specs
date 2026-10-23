# html-presentation

A Claude skill (and a small standalone toolkit) for building single-file HTML presentations with animated dataflows, architecture diagrams, flowcharts, sequence diagrams and code walkthroughs — tuned to stakeholder, technical, architecture, product or mixed audiences.

Output decks have zero dependencies: one `.html` file that works offline, from `file://`, and on networks that block CDNs.

## Project layout

```
html-presentation/
├── SKILL.md                    # Skill entry point: workflow + design principles (what Claude reads first)
├── README.md                   # This file
├── assets/
│   ├── engine.js               # Runtime: Deck, Slide, Build, Component, FlowDiagram, SequenceDiagram,
│   │                           #          CodeBlock, CountUp, FlowAnimator, PresenterView, Motion
│   ├── engine.css              # Themes (executive, technical, blueprint, product), layouts, diagram styles, print
│   └── example.src.html        # Worked example source exercising every component
├── scripts/
│   ├── build.py                # deck.src.html -> standalone deck.html (inlines the engine)
│   └── check_deck.py           # headless render: screenshots, contact sheet, layout + diagram lint
├── references/
│   ├── audiences.md            # Tone profiles: narrative arc, density, theme, motion; mixed-audience layering
│   ├── components.md           # Authoring reference: layouts, builds, diagram JSON schema, extending
│   └── motion.md               # Motion language, step-scripting dataflows, timing tokens, anti-patterns
└── examples/
    ├── order-events.html               # Built 11-slide mixed-audience deck (from assets/example.src.html)
    ├── order-events-contact.png        # Contact sheet of every slide
    ├── instant-refunds.src.html        # Product-theme source incl. a custom Component extension
    ├── instant-refunds.html            # Built 4-slide product deck
    └── instant-refunds-contact.png
```

## Using it without Claude

```bash
# 1. write slides
cp assets/example.src.html my-deck.src.html        # edit sections, diagram JSON, notes

# 2. build a standalone file
python scripts/build.py my-deck.src.html -o my-deck.html

# 3. verify (needs: pip install playwright pillow && playwright install chromium)
python scripts/check_deck.py my-deck.html            # --steps for one screenshot per build step
```

Open `my-deck.html` in a browser. Keys: **→ / Space** next · **←** back · **O** overview · **P** presenter window · **N** notes overlay · **F** fullscreen · **B** blackout · **number + Enter** jump · **Ctrl/⌘+P** print to PDF (one slide per page, diagrams complete).

## Object model

```
Deck ──owns──▶ Slide ──owns──▶ Build        (element with data-step; CSS-driven reveal)
                         └──▶ Component    (base class: stepCount, setStep(k, ctx), leave())
                                ├── FlowDiagram      nodes/edges/groups/lanes + packets (FlowAnimator)
                                ├── SequenceDiagram  participants/messages, one message per step
                                ├── CodeBlock        line-range focus per step
                                └── CountUp          animated numbers
Deck ──uses──▶ PresenterView, Motion (easing/duration tokens, reduced-motion aware)
```

Every `setStep` derives state from the step index alone, so forward, back, deep links (`#/4/2`), overview and print always agree. Add behaviour by subclassing `DeckKit.Component` and calling `DeckKit.Deck.register(selector, Class)` — see `references/components.md` §9.

## Installing as a Claude skill

Zip this folder (or use the packaged `.skill` file) and add it under Settings → Capabilities → Skills, or drop the folder into your Claude Code skills directory (`~/.claude/skills/html-presentation`).
