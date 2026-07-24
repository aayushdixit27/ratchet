# Build rules — Ayaan Gazali's hackathon system, audited against ours
*Source: LinkedIn post, 24 Jul 2026 (screenshot in `notes/`). "#1 in YCombinator Hackathon | 15x hackathons."*
*Audited at 11:35, ~1h into build. Three of five were already covered. Two were not. Those two are now binding.*

| # | His rule | Our status | What changed |
|---|---|---|---|
| 1 | **Ship the demo path first, end-to-end.** If you can't demo by halfway, you're cooked. | ⚠️ **partial** | We were building three correct pieces with nobody owning the *join*. New hard milestone: **12:45 UGLY END-TO-END** — loop runs on fixtures → writes JSONL → dashboard draws a line that moves. Ugly is not just allowed, it's the point. Halfway is 13:45; we beat it by an hour or we cut. |
| 2 | **One wow feature at a time.** Pick the one thing that makes judges go "Dayumm?" and execute it clean. | ❌ **violated** | We had two wows racing in parallel. Now ranked and sequenced — see below. |
| 3 | **Small PRs, small merges.** Big merges = last-minute explosions. | ✅ **by other means** | We deliberately don't branch — three lanes own **disjoint file trees** on one branch, which removes merges entirely rather than making them small. Under a 5-hour clock, branch+merge overhead costs more than it saves. His actual goal — no big-bang integration — is met. Reinforced: **commit every 15 minutes, and no rewrites of another lane's landed work after 14:00.** |
| 4 | **Checkpoints every 45 min in the last 3 hours.** Ask "can we demo right now?" If not, cut scope. | ⚠️ **too slack** | Ours were hourly and asked the wrong question ("is the loop closed?"). Replaced with his cadence and his question, below. |
| 5 | **Demo mode + fallbacks.** Seeded data, cached responses, backup flow when an API fails. | ✅ **already core** | It was pre-mortem risk #1: every adapter has a fixture fallback, `RATCHET_MODE=fixture`. Extended: a `--demo` flag must replay a full 5-iteration run from cache with **zero network**, and it gets rehearsed, not just written. |

---

## The one wow — ranked, not parallel

**WOW #1 — the cost curve bends.** Same bug class, cold run vs warm run: 4 calls / $0.42 → 1 call / $0.03, and the chart drops live on the projector. This is the pitch, the metric, the fundability story and the thing a judge repeats to another judge. **Nothing else gets built until this is clean.**

**WOW #2 — the agent rewrites its own `policy.yaml`.** You `cat` a diff the agent wrote to itself. Genuinely surprising to a technical panel — but it is a *second* wow, and it is **gated**: no work on `evolve()` until wow #1 runs end-to-end twice in a row without a human touching anything.

If we only land wow #1, we have a complete, coherent, winnable demo. If we land wow #2 first and wow #1 is shaky, we have a party trick and no pitch. That asymmetry is the whole reason for the ordering.

## Checkpoints — from 13:30, every 45 minutes

**13:30 · 14:15 · 15:00 · 15:45**

One question, asked literally, out loud: **"Can we demo right now?"**

Not "is it nearly working." Not "will it work in twenty minutes." Could you, at this second, stand up and run the three minutes. If the answer is no, **cut scope until it's yes** — before writing another line. The Architect asks it unprompted; builders answer from what's actually on disk.

- **12:45** ugly end-to-end
- **13:45** halfway — demoable, or we're cooked (his words)
- **15:00** feature freeze, start the screen recording
- **15:30** submission draft, portal confirmed in Discord
- **16:00** submitted; rehearse twice, once to a stranger
