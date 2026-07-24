# RATCHET — product brief
*A ratchet only turns one way. It never slips back.*

Built with the frameworks in `product_findings_july_23_2026.md`, applied in order, **before** any code.

---

## 1. Problem statement (Rachitsky: the highest-leverage artifact of the day)

> **Teams shipping AI-built web apps re-discover and re-fix the same class of bug on every release, because the coding agent has no memory across sessions. Release frequency goes up; QA cost per release stays flat forever.**

The Actian rep said the quiet part on stage this morning: *"every agent, every time, is just reinventing the wheel — and that's very lossy."* The failure mode is **state, not intelligence**. A smarter model does not fix this. Memory does.

## 1b. Is it real? — see `EVIDENCE.md`

Validated before building, not assumed. Headlines: **Gartner (Jun 2026) predicts AI coding cost per developer exceeds developer salary by 2028**; AI-authored PRs carry **1.7× more issues**; teams burn **20–30% of sprint capacity** on AI-traced bugs by day 90; and critically, a study found **vulnerabilities rose 37.6% after five iterations of unmemoried AI self-improvement** — looping without retention makes things *worse*, which is the control condition for our demo. The market gap is named in print: memory layers and evolution engines are separate products and "the winning stack will combine them — but it doesn't exist yet." Nobody is doing it for QA.

## 2. Desired outcome (Torres: behaviour change, not a feature list)

> Cost and steps to reach zero P1 bugs on a release **falls on every run** — and no human ever writes a rule.

Not "an agent that fixes bugs." An agent whose **unit economics improve with use**. That's the whole thesis and the whole demo.

## 3. Opportunity solution tree

```
OUTCOME  cost-per-verified-fix declines run over run, unattended
  └── OPPORTUNITY  coding agents have no cross-session memory
  │     └── SOLUTION  verified fix-patterns persisted as vectors (Actian), retrieved by bug signature
  └── OPPORTUNITY  the same reasoning is re-paid for on every deterministic step
  │     └── SOLUTION  slow loop reads its own traces (Guild) and promotes stable LLM steps into code
  └── OPPORTUNITY  every team on earth re-learns the same fixes in private
        └── SOLUTION  verified patterns published to cited.md (Senso) — agent-discoverable, compounding
```

Every branch traces to a real pain. Anything that doesn't appear on this tree does not get built today.

## 4. The loop

**Fast loop** (per bug): Replay QA scans the deployed app and returns a root-caused bug report → signature it → semantic search Actian for a verified fix-pattern → **hit**: apply the known strategy in one cheap call via the Pioneer router (`warm`) → **miss**: escalate to Gemini for full reasoning (`cold`), verify the fix with Replay, then **write the new pattern back to Actian** and publish it to `cited.md` via Senso.

**Slow loop** (every N iterations): read its own Guild traces, find LLM steps whose output has been effectively deterministic across ≥3 occurrences, and **rewrite its own `policy.yaml`** to replace that step with code. Commit the diff. This is Guild's own 87%-cost-cut story, run autonomously — and it produces a visible artifact: the agent's self-authored diff.

Retention is not claimed, it's **evidenced**: iteration N is cheaper *because* iteration N-1 wrote something down, and you can point at the row it wrote.

## 5. Non-goals (load-bearing — these kill scope creep before it starts)

- ❌ Not a UI framework. One single-file dashboard, no build step.
- ❌ Not fixing arbitrary repos. **One** target app.
- ❌ No auth, no multi-tenancy, no deploy pipeline, no database beyond Actian.
- ❌ Not training or fine-tuning anything.
- ❌ Not integrating a sponsor tool we can't demo. Five is already more than the three required.
- ❌ Not making the fixture app good. It is a prop. It is *supposed* to be broken.

## 6. Pre-mortem (Doshi) — it's 19:00, we lost. Why?

| # | Failure | Mitigation — owned, not aspirational |
|---|---|---|
| 1 | A sponsor SDK ate two hours and the loop never closed | **Every integration sits behind `src/adapters/base.py` with a fixture fallback.** The loop is built and green against fixtures *first*. Live APIs swap in one at a time, 25-min time-box each. A blown box = ship the fixture, log it, move on. |
| 2 | Replay QA can't reach the app (it's on localhost) | Lane C's **priority 1**, before anything else: fixture app on a public URL. Blocking dependency, reported in the first handoff. |
| 3 | The metric doesn't visibly move — 5 iterations is too little signal | Fixture app is seeded so **3 of 8 bugs share one class**. Retention is visible by iteration 3 by construction. Plus a long pre-recorded run as backup evidence. |
| 4 | Live demo dies on stage — 200 people on `717Guest` | Everything runs from a local seeded cache with zero network. Screen recording of the full run captured by 15:30. |
| 5 | Judges smell the gap between demo and build | State plainly on stage what is live vs fixture. Show the Guild trace and the JSONL. The findings doc is explicit: judges punish discovered fakery and reward named tradeoffs. |

## 7. LNO for the day (Doshi) — under a clock, everything is triage

- **Leverage (defend ruthlessly, ~60%)** — the memory hit/miss path, the metric emission, the self-rewritten `policy.yaml`, and the 3-minute demo script.
- **Neutral (do adequately)** — Replay, Guild, Pioneer, Senso adapters.
- **Overhead (fast and sloppy, or cut)** — the buggy fixture app, all styling, the README.

Opportunity-cost test before any new task: *not "is this worth doing?" but "is this the best use of the next 30 minutes?"*

## 8. The four questions judges ask — answers rehearsed

- **Who is the user?** The team shipping AI-generated web apps multiple times a day, whose QA spend scales linearly with release count and whose agent forgets everything between sessions.
- **Why does this need AI?** The retrieval and the reuse are the AI part. A static rules engine can't generalise "this modal doesn't reset state" to a modal it has never seen. Semantic matching on root cause is what makes pattern #1 apply to bug #7.
- **What makes it different?** Everyone here is building an agent that acts. This is an agent whose **cost curve bends**. The artifact isn't the fix, it's the compounding corpus — and we publish it, so the corpus is a public good that gets more valuable as more agents write to it.
- **What did we trade off to ship?** One target app instead of arbitrary repos. Fixture fallbacks behind every integration. No UI beyond a single HTML file. Feature freeze at 15:00.

## 9. Viability (Cagan: value **and** viability)

"The QA agent that gets cheaper the more you ship." Every competitor's margin is flat or worsens with volume; this one improves. The published `cited.md` corpus is a second-order moat — a cross-customer knowledge base that no single-tenant QA tool can replicate. Credible next step, which is what judges score as trajectory: point it at a real repo and let it open the PR.

## 10. The sayable sentence

> *"We didn't build an agent that fixes bugs. We built one whose cost per fix goes down every time it runs — and it publishes what it learns so everyone else's does too."*
