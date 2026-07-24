# The 3 minutes
*Written now, at 11:50, because per the build rules the demo path is the product. Everything in the briefs exists to make this script true. If a feature isn't in this script, it isn't in the demo.*

**No slides.** Screen only. Rehearse twice; once to someone outside the team.

---

**0:00 – 0:20 · The frame**
> "Gartner published this a month ago: by 2028, AI coding costs per developer will exceed that developer's salary. Pioneer makes every call cheaper. We delete the call."
> "Replay finds the bug and hands us the root cause. That's their job, and they're better at it than anything we'd build in five hours. Ours is the part nobody does: remembering. Watch run one, then watch run five."

**0:20 – 1:10 · Run 1, cold — live**
Replay's actual bug report on screen. Agent reasons from scratch: 4 LLM calls, transcript scrolling, **$0.42, ~90s**. Let it be slow. The slowness is the setup.
> "First time it's ever seen this. Full price."

**1:10 – 2:00 · Run 5, warm — same bug class, a different modal**
`MEMORY HIT — pattern #3 · modal-state-not-reset · similarity 0.91 · learned at iteration 1 · used 4×`
One call. **$0.03, ~8s.** Verified by Replay.
> "Different modal, different selector, same root cause. It didn't think — it remembered. And Replay just confirmed the fix, so the pattern gets stronger."

**2:00 – 2:30 · The counterfactual — the argument**
Both arms on one chart. Control flat (or rising). Ratchet bending down.
> "That flat line is Replay plus a coding agent, used exactly the way you'd use it today. Same bugs, same model, memory switched off. That's not a criticism of Replay — it's their output, and it's our input. The difference between the lines is the entire product."

**2:30 – 2:50 · THE CLOSER — cross-org transfer (this is now the money shot)**
Switch to **app #2 — a notes app, different team, Ratchet has never seen it.** Replay finds a bug. First run, first bug: **MEMORY HIT, $0.03.**
> "This is a different app from a different team. First run it has ever done. It's already cheap — because a fix verified on the other app transferred. Meta published this working inside Meta. EvoRepair published it inside one repo. Everyone built the private version. The economics only get interesting when my verified fix makes *your* first run cheap."

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
