# POSITIONING — "Replay finds. We remember — across company lines."
*Rewritten 11:45 after adversarial prior-art research found three collisions. The build barely changes; the pitch changes a lot.*

## The one sentence
> **Everyone is building the private version of agent memory. We're building the one where my verified fix makes *your first run* cheap.**

Replay's unit of output is a bug report and their run count is one. Ours is a verified fix-pattern, and our metric only exists across runs — **and across organizations**, which is the part the published work has not done.

## ⚠️ Three collisions found — read before writing any copy

**1. Prior art on the core mechanism is published, with numbers. Do not claim novelty on "remembering verified fixes."**
- **EvoRepair** (arXiv 2605.30105): verified repair trajectories → markdown + vectors → similarity retrieval → **−41.58% cost**. Our architecture, published.
- **Meta Experience Graphs** (arXiv 2606.29823): executable artifacts with objective rewards, cross-session retrieval, **"10× faster convergence at 52% lower token cost per valid solution."** Our headline, with production numbers.
- **"Compounding engineering"** (Klaassen / Shipper, Every) is an established brand shipped as a Claude Code plugin.

Every one of them is **private and single-org**. That is the gap, and it is the only one we should claim.

**2. Senso collision — do not lead with the corpus.** "Publish verified knowledge that agents cite" is Senso's whole business; `cited.md` is literally their Citeables surface, and `Codeables` is the developer version. Pitching the corpus as our differentiator is pitching a sponsor's product back at them. Publishing is a **byproduct**, not the thesis.

**3. Pioneer collision — do not sell the cost curve on its own.** Pioneer's Adaptive Inference mines production traces, auto-trains specialist small models and promotes them behind the same URL — "cost per task declines" is a claim they can make. The distinction is sharp and you should say it exactly this way:
> **"Pioneer makes every call cheaper. We delete the call."**

**Guild caveat:** the one-button "optimize this workspace" and the 87% figure were demoed on stage but appear nowhere in their public material — their shipped product is measurement (Insights Dashboard: a human reads a chart and edits the agent). Ask Corey or Tamao directly before positioning against it. Either way `evolve()` stays our *second* claim.

Say "QA tool" and you are competing with a sponsor whose CEO is judging, and losing. Say "the memory layer that makes QA compound" and Replay becomes your input, not your rival.

## What we verified (24 Jul 2026)
Replay QA explores an app, writes Playwright tests, records sessions, finds bugs, produces **root cause and suggested fix**, and posts to PRs. They ship a product called **Loop QA**. That is not our idea — it is their product, and Brian Hackett will know it in ten seconds.

What their published material contains **no mention of**: memory across runs, accumulated patterns, or a second run costing less. Loop QA's own page describes a linear pipeline — URL in, tests and bugs out. Every run starts from zero.

That amnesia is the gap. It is the only gap. Everything we build points at it.

---

## Four ways the build makes this structurally true

### 1. Run the counterfactual live — the highest-leverage thing we do
`--no-memory` is a flag, not a feature. Two arms, same Replay input, same model, same bugs:

- **Control arm** — memory off. Reasons from scratch every iteration. *This is literally "Replay + a coding agent" as intended today.*
- **Ratchet arm** — memory on.

Both plotted on the same chart. **Control is flat. Ratchet bends.** That answers "isn't this just Replay?" with a chart instead of a sentence, and it lets us say the generous thing out loud: *"that flat line isn't a criticism of Replay — it's their output, used the normal way."*

And per `EVIDENCE.md`, unmemoried iteration has been measured getting *worse* (vulnerabilities +37.6% over five iterations). If our control arm even trends upward, that's the entire talk.

### 2. Make the corpus a visible asset, not an internal cache
If remembering is the product, the memory must be an object a judge can look at. Every pattern carries `born_at_iteration`, `uses`, and **`saved_usd` cumulative**. Sorted by `saved_usd`, the dashboard says: *"this one pattern has saved $3.71 so far."*

That reframes the artifact from a QA run into **an asset that accrues** — which is the fundability story.

### 3. Attribution as architecture, not manners
Every pattern carries provenance: `discovered_by: replay-qa`, `root_cause_source: replay`, `verified_by: replay`. When it publishes to `cited.md` via Senso, **it cites Replay**.

This satisfies the challenge slide's "grounded in real sources" literally, makes the sponsor relationship structural rather than decorative, and puts Brian's product in the public corpus by design. That isn't flattery — it's the dependency graph, written down.

### 4. Let the thin adapter make the argument
`src/adapters/replay.py` should be short, and we should say so: *"our Replay adapter is forty lines, because Replay does the hard part."* Judges read repos. A thin QA adapter next to a thick `memory/` module states the positioning without a human in the room.

---

## The moat sentence (use this when pushed)
> **We don't remember what the model said. We remember what Replay confirmed.**

Anyone can cache LLM output. What makes the corpus trustworthy is that every pattern was verified by re-running Replay against the live app — so each one carries `verified_by_replay_at` and a verification count. Verification is the expensive, hard, defensible part, and it is Replay-dependent *by design*.

---

## Rehearsed answers

**"Meta's Experience Graphs paper already reports 52% lower token cost from cross-session verified-experience reuse. Aren't you re-implementing a published result?"** *(the strongest objection available — expect it from Paige or the Mercor/Nvidia judges)*
> Yes, and I'd point at EvoRepair too — −41.58% on the same idea. Both are single-org. Meta's graph lives inside Meta; EvoRepair's is per-repo. The economics only get interesting when the corpus crosses company lines — my fix for a common dependency bug should make *your* first run cheap, not just my second. That's a distribution and trust problem: verification gating, provenance, dedup. Not a retrieval problem. That's the part nobody has shipped, and it's what the second app in that demo was showing.

**"Isn't this just Replay QA?"**
> Replay is inside it — we're one of their consumers, and the demo you just watched calls their API live. What they don't do is remember. Every Replay run starts from zero; that's the flat line on the chart. We keep the verified fixes and reuse them, which is why our line bends. Different unit of output, different metric.

**"Couldn't Replay just add memory?"**
> They could, and if they did it would be per-customer — your fixes in your tenant. Ours publishes to a public corpus that any agent can read, which is why the Senso publishing step exists and why we cite the source on every entry. A vendor's private cache and a public compounding corpus are different companies. Honestly, the version where Replay ships memory and points at our corpus is a good outcome.

**"Isn't the self-rewriting policy just Guild's optimize button?"**
> Same idea, different trigger. Guild's is a human pressing a button on a workspace. Ours fires unattended off the agent's own trace analysis, mid-run, per bug class. It's the smaller of our two claims, which is why we showed the cost curve first.

**"Five iterations is a small sample."**
> It is. Here's the n, here's the seed, here's the raw JSONL. What we'd need to prove it properly is a few hundred iterations across several apps — that's the next thing we'd run.

## What we never say
- ❌ "We're building autonomous QA." → that's Replay's sentence.
- ❌ "We built a memory system." → half a dozen funded companies sell agent memory; we'd be the worst one.
- ✅ "We make verified fixes compound, and we publish them."
