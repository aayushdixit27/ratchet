# POSITIONING — "Replay finds. We remember."

## The one sentence
> **Replay's unit of output is a bug report, and their run count is one. Ours is a verified fix-pattern, and our metric only exists across runs.**

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
