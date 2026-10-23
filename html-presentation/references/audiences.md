# Audience profiles

Pick the profile, then let it drive structure, density, theme and motion. Each section ends with the anti-patterns that most often sink that audience.

Contents: Stakeholder · Technical · Architecture · Product · Mixed · Timing guide

---

## Stakeholder / executive
**They want:** the decision, the risk, the money, the date. They will read titles and numbers, not bullets.
**Theme:** `executive`. **Motion:** low — builds for pacing, count-ups for key numbers, one architecture flow at most, shown at the "boxes and value" level.

**Arc (SCQA / pyramid):**
1. Title with the outcome in it
2. Statement — the problem in one sentence with one number
3. KPIs — 2–4 outcomes committed to (count-up)
4. What changes — compare (before/after) or a simple 5–7 node flow
5. Cost / value — bars or table, payback stated in words
6. Risks & mitigations — 3 cards, tone-coded
7. Roadmap — 3–5 milestones, each a business outcome
8. The ask — numbered decisions with owners/dates

**Density:** ≤ 3 points per slide, ≤ ~25 body words, one number per KPI. Lead with the conclusion, put evidence in notes or appendix.
**Vocabulary:** outcomes, customers, cost, risk, time. Translate tech: "Kafka topic" → "event stream"; "p99 latency" → "status within 2 seconds for 99% of orders".
**Diagrams:** labels are business capabilities; hide infra (registries, caches) unless they're the point. Captions carry the "so what".

**Anti-patterns:** agenda slides; architecture with 15 boxes; bullets that are sentences of jargon; ending on "Questions?" instead of the ask; numbers without a comparison ("38%" vs "38% fewer contacts").

---

## Technical (engineering teams)
**They want:** how it works, why this design over alternatives, failure modes, what they'll build or change.
**Theme:** `technical`. **Motion:** medium-high — stepped diagrams with packets, sequence diagrams one message per click, code line-focus.

**Arc:**
1. Title + context (one line on the problem and constraints)
2. Requirements / constraints as cards (throughput, latency, consistency, compliance)
3. Design overview — stepped flow diagram
4. Deep dives — sequence diagram for the tricky interaction, code walkthrough for the contract
5. Failure modes — swimlane/flowchart of retries, DLQ, idempotency
6. Alternatives considered — table with the decision criteria
7. Rollout / migration plan, observability
8. Open questions — what you want feedback on

**Density:** one diagram *or* one code block (≤ 15 lines, ≤ ~55 chars) per slide plus ≤ 3 annotations. Real names (services, topics, tables) build trust.
**Diagrams:** show sync vs async (`style: "dashed"`), data stores (`db`), queues/topics (`queue`), trust boundaries (`groups`). Use `badge` for versions/new.

**Anti-patterns:** screenshots of IDE code; walls of YAML; hand-waving failure handling; diagrams without a legend when line styles carry meaning.

---

## Architecture (architecture review board, principal engineers)
**They want:** boundaries, responsibilities, data ownership, coupling, NFRs, and the trade-offs you made deliberately.
**Theme:** `blueprint`. **Motion:** medium — assemble the system layer by layer, flow critical paths, focus on the decision points.

**Arc (C4-flavoured zoom):**
1. Context — system + actors + external systems (5–7 nodes)
2. Containers — services, stores, streams grouped by boundary (`groups`), stepped reveal
3. Key flows — 2–3 critical paths as packet flows (write path, read path, failure path)
4. Data ownership — which service owns which store; table or diagram with groups
5. NFR mapping — cards or table: availability, latency, scale, security, compliance, with the mechanism for each
6. Decisions & trade-offs — ADR-style: context → decision → consequences (compare or table)
7. Risks, evolution path, what's deliberately out of scope

**Density:** moderate; diagrams up to ~10 nodes if grouped. One zoom level per slide — never mix context and component level on one canvas.
**Diagrams:** `groups` for regions/VPCs/domains/trust zones, `external` for third parties, `lanes` for ownership. Use `focus` steps to put each decision in context.

**Anti-patterns:** one giant "everything" diagram; arrows without direction semantics; NFRs listed without mechanisms; no explicit trade-offs.

---

## Product (PMs, design, business partners)
**They want:** the user problem, the experience, the value, what ships when, how success is measured.
**Theme:** `product`. **Motion:** expressive but purposeful — journey flows, before/after wipes, count-ups, roadmap builds.

**Arc:**
1. Title framed as user outcome
2. The user & pain — statement or quote, a number
3. Journey today vs tomorrow — compare with `wipe`, or a flow of user steps (`actor` → steps → outcome)
4. How it works (lightly) — a 4–6 node flow where nodes are capabilities, not services
5. Success metrics — KPIs
6. Roadmap — milestones as user-visible releases
7. Dependencies & asks

**Density:** low-moderate; big type, generous whitespace. Use language of jobs-to-be-done.
**Diagrams:** flows of user steps or capabilities, `decision` for key branches, `tone: "good"` for the happy outcome.

**Anti-patterns:** internal service names; feature lists without the user problem; metrics without baselines.

---

## Mixed audience (exec + engineering in one room) — layering strategy
Don't average the tones — **layer** them. The spine is executive; depth is opt-in.

1. **Executive spine** in `executive` theme: title → problem → outcomes → simple architecture (capability level) → value → roadmap → ask. A non-technical attendee can follow these slides alone.
2. **Technical inserts** marked visually: set `data-theme="technical"` (or `blueprint`) on deep-dive slides and use an eyebrow like `Deep dive · exactly-once`. The theme shift itself tells executives "this part is for the engineers" and tells engineers "here's the substance".
3. **Bridge every insert**: the slide before it states the business claim; the deep-dive proves it; the caption of its last step restates the claim in plain words.
4. **Same diagram, two depths**: show the capability-level flow on the spine; reuse node ids and positions in the deep-dive with infra revealed via extra `show` steps, so the room sees the same picture getting richer instead of a new one.
5. **Appendix** after the ask (section divider `Appendix`) for details you'll only show if asked — keeps the ask from being buried.

`assets/example.src.html` is a mixed deck built this way.

---

## Timing guide
| Slot | Slides (excluding appendix) | Diagram slides |
|---|---|---|
| 5 min | 4–6 | 0–1 |
| 15 min | 8–12 | 1–2 |
| 30 min | 12–18 | 2–4 |
| 60 min | 20–30 | 4–8 |

Each build step costs ~10–20 s of talk; a 6-step diagram is a 2-minute slide.
