# Motion language

Motion in a presentation is a pointer: it tells the room where to look and what caused what. Use it to make the presenter's sentence visible.

## The three jobs (if it does none, cut it)
1. **Sequence** — the order things happen or were built (builds, stepped diagram reveals, timeline).
2. **Causality** — this thing causes / sends / triggers that (packets along edges, sequence messages drawing in).
3. **Attention** — this matters now (focus + dim, pulse, accent highlight, line focus in code).

## Tokens (already in the engine)
| Token | Value | Use |
|---|---|---|
| ease-out | `cubic-bezier(.16,1,.3,1)` (expo-out) | entrances — fast start, soft landing |
| ease-in-out | `cubic-bezier(.65,0,.35,1)` | exits, edge draw-in, things moving between states |
| spring | `cubic-bezier(.34,1.45,.64,1)` | node pop-in only (slight overshoot) |
| durations | 220 fast · 560 base · 900 slow | UI · builds · draw-ins |
| stagger | 80ms per sibling | items revealed in the same step |
| packet speed | 520 units/s × `speed` | flows; `count` 2–3 for "stream", 1 for "a request" |

Exits are faster than entrances (420 vs 700ms slide transition) — the audience cares about what's arriving.

## Scripting a dataflow
Write the step script as the presenter's lines first, then map each line to one verb:

| Presenter says | Step |
|---|---|
| "A customer places an order…" | `show` actor + service, `flow` actor>service |
| "…which publishes one event…" | `show` topic, `flow` with `label: "OrderPlaced"` |
| "…and every consumer reacts independently." | `show` consumers group, parallel `flow`s |
| "Adding fraud scoring changes nothing upstream." | `focus` [topic, fraud], `pulse` fraud, flow end-to-end in `warn` tone |

Rules of thumb:
- **One new idea per click.** If a step both reveals 4 nodes and runs a failure path, split it.
- **Flow what you just revealed.** A packet arriving at a newly shown node is the strongest "this is how it connects" signal.
- **Name packets** (`label`) when the payload matters (event type, token, file) — engineers love it, executives understand it.
- **End on focus.** The last step of a diagram should isolate the punchline; the caption states it in plain words.
- **Colour = semantics:** accent for the path under discussion, `bad` for failure paths, `warn` for degraded/new-risk, `good` for success/commit, `muted` for analytics/side paths.
- **Loops are fine** for flows (default) — the room needs a few seconds to read the path. Use `loop: false` only for one-shot "a request happens" moments.

## Builds on text slides
- Reveal list items one per click only when you'll talk to each; otherwise reveal the list together and let stagger do the work.
- `data-dim-after` keeps earlier points visible but receded as you move on — better than hiding them.
- `wipe` for before → after reveals; `scale` / `pop` for a single big number; `blur` sparingly for a reveal moment (one per deck).
- KPI count-ups: 1.2–1.6s. Never count up more than three numbers on one slide.

## Slide transitions
Default `slide` (horizontal, direction-aware) gives a sense of progress. Use `fade` for section changes within a theme, `zoom` for the one statement slide you want to land, `none` for rapid-fire comparisons. Don't mix many transition types.

## Reduced motion & print
The engine handles both: with `prefers-reduced-motion`, builds are instant, packets are off, active paths still show (marching dashes off, accent on). In print/overview, diagrams render complete with no focus/dim. Never encode information *only* in motion — the static state of every step should still read correctly.

## Anti-patterns
- Everything fades up one-by-one: pacing becomes tedious; group related items into one step.
- Packets on every edge at once: nothing stands out; flow one path, focus one area.
- Spinning/bouncing/parallax decoration.
- Animating layout (things changing size/position between steps) on text slides — reads as jitter.
- Long diagram scripts (> 6 steps): split into two slides with the same layout.
