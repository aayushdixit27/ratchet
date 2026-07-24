# The 3 minutes
*Written now, at 11:50, because per the build rules the demo path is the product. Everything in the briefs exists to make this script true. If a feature isn't in this script, it isn't in the demo.*

**No slides.** Screen only. Rehearse twice; once to someone outside the team.

---

**0:00 – 0:25 · Maya** (no screen yet, just talk)
> "Maya is the only person on a four-person team who cares about QA. There's no QA hire. She ships an AI-built internal tool most Fridays."
> "She points Replay at the deploy, gets eight root-caused bugs, pastes them into her coding agent, ships."
> "Next Friday: eight more. Three are the same *kind* of bug she fixed last week, in different modals, wearing different symptoms. She pays full price to rediscover something she already solved."
> "And she knows. She's thinking *we've fixed this three times now*. Eventually she writes a lint rule, three sprints late."
> **"Maya is the ratchet. She's doing it by hand, from memory, on top of her actual job. We automated her instinct, and we verify it."**

**0:25 – 0:35 · The turn**
> "Every team has a Maya, she's the bottleneck, and Gartner says by 2028 AI coding cost per developer will exceed that developer's salary. Pioneer makes every call cheaper. We delete the call."

**0:35 – 1:15 · Run 1, cold — live**
Replay's actual bug report on screen. Agent reasons from scratch: 4 LLM calls, transcript scrolling, **$0.42, ~90s**. Let it be slow. The slowness is the setup.
> "First time it's ever seen this. Full price."

**1:15 – 1:55 · Run 5, warm — same bug class, a different modal**
`MEMORY HIT — pattern b7a3887a7811 · modal-state-not-reset · similarity 0.86 · used 2×`
**⚠ Render these from the JSONL. Do not hardcode.** Real values as of 12:50 are `similarity: 0.8565`, `pattern_id: b7a3887a7811`, `uses: 2`. The 0.91 in an earlier draft of this file was a placeholder I invented before the data existed; if a number on screen doesn't match `runs/golden/ratchet.jsonl`, that is the exact kind of gap judges are told to hunt for.
One call. **$0.03, ~8s.** Verified by Replay.
> "Different modal, different selector, same root cause. It didn't think — it remembered. And Replay just confirmed the fix, so the pattern gets stronger."

**1:55 – 2:25 · The counterfactual — and it gets WORSE**
Both arms on one chart. Ratchet $0.4258 -> $0.0293. Control climbs to $0.8643.
> "That top line is Maya's Friday. Replay plus a coding agent, used exactly the way you'd use it today. Same bugs, same model, memory off. Not a criticism of Replay: that's their output, and it's our input."
> "It doesn't go flat. It goes **up** 66%, because it keeps re-failing on classes it's already seen. There's a published result where vulnerabilities rose 37.6% over five unmemoried iterations. We reproduced it by accident. Looping without memory doesn't plateau, it degrades."

**2:25 – 2:50 · THE CLOSER — cross-org transfer (this is now the money shot)**
Switch to **app #2 — a notes app, different team, Ratchet has never seen it.** Replay finds a bug. First run, first bug: **MEMORY HIT, $0.03.**
> "Different app, different team, first run it has ever done, and it's already cheap: a fix verified on the other app transferred. **This is Maya's fix making someone else's first Friday cheap.** Meta published this working inside Meta. EvoRepair published it inside one repo. Everyone built the private version. The economics only get interesting when my verified fix makes *your* first run cheap."

**2:50 – 2:55 · The asset (fast)**
Open `cited.md`. A pattern entry, citing Replay as the source, with `uses: 4` and `saved: $3.71`.
> "We don't remember what the model said. We remember what Replay confirmed. And we publish it, cited, so any agent on the web can read it. A vendor's private cache doesn't compound across companies. This does."

**2:55 – 3:00 · Trajectory**
> "Next: point it at a real repo and let it open the PR. Every fix anyone verifies makes everyone else's agent cheaper."

**Kicker — only if `evolve()` landed and only if we're under time:**
`cat policy_history/*.diff`
> "Ten seconds: that's a diff the agent wrote to its own policy, unattended, after noticing it was paying a model to do something deterministic."

---
## Failure drill
Wifi dies → `--demo` replays the full run from cache, zero network, under 90s. Screen recording captured by 15:30 as the last resort. **Rehearse the fallback, not just the happy path.**

## Say the tradeoffs before you're asked
One target app, not arbitrary repos. Fixture fallbacks behind every integration. Five iterations, small n. Judges reward named tradeoffs and punish discovered fakery — so name them in the Q&A opener.
