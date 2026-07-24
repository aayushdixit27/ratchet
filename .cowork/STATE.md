# STATE — maintained by the Architect (Cowork). Read-only for builders.

**Idea:** RATCHET — self-evolving QA agent whose cost-per-verified-fix declines run over run. See `PRODUCT.md`.
**Sponsor tools committed:** Replay QA · Actian VectorAI DB · Pioneer router · Guild.ai traces · Senso Context OS · Gemini  (6 — need 3)
**Goal metric (the number that drops on stage):** `cost_usd` and `llm_calls` per verified fix, by iteration. Secondary: warm-path share ↑.
**Lanes:** A = loop core · B = adapters · C = fixture app + dashboard
**Loop closed end-to-end:** no
**Demo path rehearsed:** no
**Submitted:** no

## Open risks
1. Replay QA needs a **public URL** for the fixture app — Lane C priority 1, blocks Lane B's QA adapter.
2. Submission portal unconfirmed: Devpost vs tokensand.com/swarmhack vs bit.ly/projects-jul24. Confirm in Discord before 15:30.
3. Any live sponsor API that can't be reached must degrade to fixture without crashing the loop.

## Last checkpoint
11:25 — idea locked, three lane briefs issued, no code yet.
