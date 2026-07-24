# AMENDMENT 03 — the corpus crosses company lines
**Issued 11:45 after adversarial prior-art research. Read `POSITIONING.md` (rewritten).**

## ⚠️ GATE UNCHANGED. Nothing here touches Lane A or B before the join is green.
`runs/` is still empty. The join is still the only thing that matters. Lane C is idle, so Lane C starts this now; A and B carry on exactly as briefed.

## What the research found
Our core mechanism is **published, with numbers**:
- **EvoRepair** (arXiv 2605.30105) — extracts repair knowledge from *verified* repair trajectories, stores it as markdown + vectors, retrieves by similarity, reports **−41.58% cost**. That is our architecture, in a paper.
- **Meta, Experience Graphs** (arXiv 2606.29823) — executable artifacts with objective rewards, cross-session retrieval, **"10× faster convergence at 52% lower token cost per valid solution."** That is our headline claim, with production numbers.
- **"Compounding engineering"** is an established brand (Kieran Klaassen / Dan Shipper, Every), shipped as a Claude Code plugin.

We cannot say "nobody remembers verified fixes." That is false and a technical judge may know it.

**But every one of those is private.** Meta's graph lives inside Meta. EvoRepair's is per-repo. The interesting economics only appear when the corpus **crosses organizational boundaries** — my verified fix should make *your first run* cheap, not just my second. That is a distribution and trust problem (verification gating, provenance, dedup), not a retrieval problem, and nobody has shipped it.

**The pitch moves from "we remember" to "we remember across company lines."** Cold-start becomes the story, not warm-repeat.

---

## Lane C — start now, in parallel, this is off the critical path

**Build a SECOND fixture app that Ratchet has never seen.**

Different domain, different DOM, different copy, different author voice — a notes app, not a task tracker. But it carries **the same latent root cause**: lazy `x = x || seed()` scratch state that `closeModal()` never nulls. Symptoms must look completely unrelated to Tasker's. Ship it to a second public URL (Pages again — it survives machine sleep; the tunnel doesn't).

Seed ~6 bugs. **Two** share the modal-state class with Tasker. The rest are novel singletons so the run isn't trivially all-warm.

Write `app2/bugs.json` in the same schema Lane B already consumes. Do not touch Tasker, `src/`, or `runs/`.

**Why this is the whole pitch:** the demo's closing beat becomes Ratchet meeting a brand-new app from a "different team" and fixing its first bug for $0.03, because a pattern verified on Tasker transferred. That is the thing the papers did not do.

## Lane A — after the join is green, not before
- Add `origin_app` and `origin_org` to every record and every pattern. Tasker = `org: acme`, app2 = `org: globex`. The corpus must be visibly cross-org or the claim is decorative.
- `--target app2 --corpus-from tasker` must run app2 against a corpus built only from Tasker, so first-run warm hits are provably transfer, not leakage. **Never let app2's own patterns pre-seed its own first run** — that's the fakery a judge will hunt for.

## Lane B — no change to your queue
Keep going: Actian → Replay → Pioneer → Senso → Guild. Note one framing change that affects nothing in code: **Senso is now the publishing rail, not our differentiator** (see below). Still integrate it; just don't build extra on top.

---

## Framing corrections — these are binding on all copy, README and submission text

| Don't say | Because | Say instead |
|---|---|---|
| "We publish verified knowledge that agents cite" | That is **Senso's entire business**, and `cited.md` is literally their Citeables surface. We'd be pitching a sponsor's product back at them. | Publishing is a *byproduct*. Lead with the economics. |
| "Cost per task declines over time" *alone* | **Pioneer's Adaptive Inference** already makes each call cheaper — a judge will call this Pioneer. | **"Pioneer makes every call cheaper. We delete the call."** |
| "Nobody is doing this" | EvoRepair and Meta published it. | **"Everyone is building the private version."** |
