# STATE — maintained by the Architect (Cowork). Read-only for builders.

**Positioning:** *"Replay finds. We remember."* — we are a consumer of Replay, not a competitor. See `POSITIONING.md`. Demo script locked in `DEMO.md`.
**Idea:** RATCHET — self-evolving QA agent whose cost-per-verified-fix declines run over run. See `PRODUCT.md`.
**Sponsor tools committed:** Replay QA · Actian VectorAI DB · Pioneer router · Guild.ai traces · Senso Context OS · Gemini  (6 — need 3)
**Goal metric (the number that drops on stage):** `cost_usd` and `llm_calls` per verified fix, by iteration. Secondary: warm-path share ↑.
**Lanes:** A = loop core · B = adapters · C = fixture app + dashboard
**Loop closed end-to-end:** no  ·  **Wow #1 (cost curve) clean:** no  ·  **Wow #2 (self-rewrite) — gated, do not start**
**Demo path rehearsed:** no
**Submitted:** no

## Open risks
0. **Prior art is published (EvoRepair −41.58%, Meta Experience Graphs −52% token cost).** Core mechanism is NOT novel. Novel claim is now **cross-organizational** transfer — app #2 (Lane C, building now) is the proof. Never say "nobody does this"; say "everyone built the private version."
0b. **Senso owns "publish verified knowledge agents cite"** — publishing is a byproduct, not the pitch. **Pioneer owns "each call gets cheaper"** — our line is "Pioneer makes every call cheaper, we delete the call."
0c. **Overlap with Replay QA (their CEO is a judge).** Mitigated structurally: live `--no-memory` control arm plotted against us, provenance citing Replay on every pattern, thin QA adapter. Replay adapter must be LIVE — the story is checkable.
1. Replay QA needs a **public URL** for the fixture app — Lane C priority 1, blocks Lane B's QA adapter.
2. Submission portal unconfirmed: Devpost vs tokensand.com/swarmhack vs bit.ly/projects-jul24. Confirm in Discord before 15:30.
3. Any live sponsor API that can't be reached must degrade to fixture without crashing the loop.

## Next hard gate
**12:45 ugly end-to-end** — loop → JSONL → dashboard line moving. Lane A owns the join. Then 45-min "can we demo right now?" from 13:30.

## Last checkpoint
11:45 — idea locked, three lane briefs issued, problem validated in `EVIDENCE.md` (Gartner 2028 cost prediction, CodeRabbit 1.7x defect rate, the 37.6%-vulns-after-5-unmemoried-iterations study, and a named market gap: memory layers and evolution engines exist separately, nobody has fused them for QA). No code yet.
