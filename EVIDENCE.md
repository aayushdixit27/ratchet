# EVIDENCE — is the problem real?
*Checked 24 Jul 2026, before committing to the build. Torres: test the riskiest assumption first, cheaply.*

Our riskiest assumption is not technical. It's that **anyone actually has this problem.** Verdict: yes, loudly, with numbers — and the market gap is named in print.

---

## 1. The economic premise — cost per AI-assisted fix is becoming a CFO line item

- **Gartner, 24 Jun 2026:** by **2028, AI coding costs per developer will surpass the average developer's salary**, driven by token consumption under usage-based pricing. Press release + Register/ComputerWeekly coverage.
- On X, this landed as: *"The tools will cost more than the person using them."* (Russell Fradin)
- *"AI has reintroduced marginal cost into software. Every agent run costs money. Software founders have to think like manufacturing companies with COGS now."* (M Mohan)
- *"Most engineering teams think QA costs what's on the invoice. The real cost is invisible, untracked, and **compounding every sprint**."* (God of Prompt)

**Why this matters to us:** it makes `cost_usd` per verified fix — the exact number on our dashboard — the metric a buyer already cares about. We are not inventing a KPI. We are bending one that is on fire.

## 2. The defect premise — AI-built apps break more, and QA absorbs it

| Finding | Source |
|---|---|
| AI-authored PRs carry **1.7× more issues**, **1.75× more logic errors** (470 PRs) | CodeRabbit |
| **41% increase in bug rates** after AI tool adoption (~800 devs) | Uplevel |
| **30–41% increase in technical debt** post-adoption (8.1M PR study) | GitClear-adjacent |
| Code **duplication 4× higher**; refactoring fell 25% → <10% of changed lines | GitClear |
| Incidents per PR **+23.5% YoY** as AI volume climbed | Cortex |
| By day 90, teams spend **20–30% of sprint capacity** on AI-traced bugs | Keyhole |
| **92% of US devs** use AI coding tools daily; ~41% of 2025 code AI-generated/assisted | GitHub Octoverse 2025 |

The cost didn't vanish, it **moved downstream**: "a feature taking 20 minutes to generate required three additional days for verification."

## 3. The killer datapoint — iterating *without* retention makes things worse

A 2025 study found **critical vulnerabilities rose 37.6% after just five iterations** of AI self-improvement — from 2.1 to 6.2 vulnerabilities per sample by iterations 8–10 — **even when researchers explicitly asked for security improvements.**

That is the control condition for our entire demo. Looping without memory *degrades*. Our thesis is that the missing variable is verified retention, not model quality. We should say this on stage: *"here's what five iterations looks like without memory — it gets worse. Here's ours."*

## 4. The practitioner chorus on X — the memory half is a known, unsolved pain

- *"One of the first things you figure out coding with AI agents: they don't remember anything between sessions. Claude Code has a todo system — it's stuck to one session. Close the tab, it's gone."* — Anurag Arjun
- *"For two years the whole conversation was about context window size. Meanwhile the actual problem never moved: agents don't remember anything between sessions. We kept patching it with RAG and calling that memory."* — Chubby (@kimmonismus)
- *"Everyone is obsessed with AI agents. Almost nobody is talking about the REAL bottleneck: memory. Most agents forget context, forget skills, **forget what worked**."* — shirish
- *"Every agent starts from zero each session. No persistence, no portability, no ownership."* — Rohit Ghumare
- *"Coding agents forgetting basic details mid-thread has been driving me insane."* — nexxel
- **The baseline we're replacing:** *"Coding agents are getting dumber every session and almost nobody is fixing it automatically. They get better through humans noticing patterns and filing issues. Three sprints later someone patches a prompt."* — tetsuo

That last quote is the status quo Ratchet automates away: today the ratchet is a human, and it takes three sprints per click.

## 5. The competitive gap — named in print, and it's exactly our slot

An industry survey of agent self-improvement tooling (Ry Walker, 2026) splits the field into:
- **Memory layers:** Mem0, Letta, Zep, Hindsight, Cognee, Supermemory, LangMem
- **Evolution engines:** ACE, Agentic Context Engine, Microsoft Amplifier

and identifies as unsolved:
1. **"Memory layers and skills frameworks remain separate products. The winning stack will combine them — but it doesn't exist yet."**
2. Multi-agent shared memory is handled well by no one.
3. Evolution engines have research promise but **thin production adoption**.

It also confirms: **nobody is doing QA-specific self-improvement** — no agent that remembers *verified* fixes and drives cost-per-fix down. Closest prior art is Microsoft Amplifier's `DISCOVERIES.md` (agents writing down solutions so they don't repeat mistakes), which is generic, file-based, and unmeasured.

Ratchet = memory layer **fused with** an evolution engine, aimed at one vertical, with the outcome expressed in dollars.

---

## Honest counter-arguments (say these before a judge does)

- **The memory space is crowded.** Half a dozen funded companies sell agent memory. Our differentiation is *not* "we built memory" — it's the vertical (QA), the unit of value (a **verified** fix, not a remembered fact), and the economics (cost per fix falls). Never pitch this as a memory company.
- **Verification is what makes the memory trustworthy, and verification is the hard part.** Replay QA closing the loop — fix, then *prove* the fix — is what separates our corpus from a pile of RAG chunks. Lean on that.
- **Five iterations is a small n.** Say so. Show the curve, name the sample size, and say what a 500-iteration run would need to prove.

## The opening line this evidence buys us

> *"Gartner says that by 2028, AI coding costs per developer will exceed that developer's salary. Every QA tool in this room has a cost curve that goes up with volume. Ours goes down. Here it is going down."*
