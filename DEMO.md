# The 3 minutes
*Rewritten 13:50. Supersedes all earlier drafts (previous version kept at `.cowork/DEMO-prev.md`).*
**No slides. Screen only. Rehearse twice, once to someone outside the team.**

## ⚠️ Two rules that override everything in this script
1. **Never speak a number this file quotes without checking it against the live render.** Every figure below is marked either `[FIXED]` (verified, stable) or `[READ]` (read it off the screen in the moment). The corpus changes what scores what; a script quoting a stale number is the exact demo-versus-build gap judges hunt for.
2. **For the memory-hit beat, say "watch the score" — never a specific number.** The counter bug scored 0.49 at 12:30 and 0.76 at 13:30, and the difference was mostly the corpus rebuilding on real model text, not anything we changed. Let the screen say it.

---

**0:00 – 0:25 · Maya** (no screen, just talk)
> "Maya is the only person on a four-person team who cares about QA. There's no QA hire. She ships an AI-built internal tool most Fridays."
> "She points Replay at the deploy, gets root-caused bugs back, pastes them into her coding agent, ships."
> "Next Friday: more bugs, and some are the same *kind* she fixed last week, in different places, wearing different symptoms. She pays full price to rediscover something she already solved."
> "And she knows. She's thinking *we've fixed this three times now*. Eventually she writes a lint rule, three sprints late."
> **"Maya is the ratchet. She's doing it by hand, from memory, on top of her actual job. We automated her instinct, and we verify it."**

**0:25 – 0:35 · The turn**
> "Every team has a Maya. Gartner says by 2028 AI coding cost per developer will exceed that developer's salary. Pioneer makes every call cheaper. **We delete the call.**"

**0:35 – 1:15 · The live beat — Replay, for real**
Replay's project page on screen.
> "This is Replay QA against our deployed app. Their crawler, their exploration, their root-cause analysis. It found bugs **we never planted**."
Run the loop. One of Replay's own bugs comes in and hits memory.
> "Watch the similarity score. That's a bug Replay discovered on its own, matching a pattern we verified earlier. One call instead of a full reasoning pass."
Then flip to Replay's UI and show the bug status change.
> "And we write the confirmation back into Replay's own system. That's not us marking our own homework."

**1:15 – 1:55 · Cold versus warm, side by side**
Split pane. Left: the cold path reasoning, call count, cost. Right: `MEMORY HIT`, one call, cost. `[READ]` both figures off the screen.
> "Same root cause, different bug, different selector, different file. It didn't think. It remembered."

**1:55 – 2:25 · The counterfactual — and it gets worse**
Hero chart: **calls per verified fix**, two arms.
> "That top line is Maya's Friday: Replay plus a coding agent, memory off. Same bugs, same models. Not a criticism of Replay — that's their output, and it's our input."
> "It doesn't flatten. It **climbs**, from five calls per fix to eight `[READ]`, because it keeps re-failing on classes it has already seen. There's a published result where vulnerabilities rose 37.6% over five unmemoried iterations. We reproduced it by accident."
> "Ours goes to one."
Then the cost tile:
> "In dollars that's a range rather than a clean curve, because at real Pioneer prices the numbers are cents and the variance is bigger than the signal. So we report the invariant: **calls**. Pioneer's own telemetry shows what their routing saved on top `[READ]`. Those stack."

**2:25 – 2:50 · THE CLOSER — cross-org transfer**
Switch to **app #2, `jotting-fixture`** — a notes app from a different company, never seen before.
Banner: **ACME → GLOBEX**.
> "Different app, different company, first run it has ever done. Already cheap, because a fix verified on the other app transferred."
> "Meta published this working inside Meta. EvoRepair published it inside one repo. **Everyone built the private version.** The economics only get interesting when *my* verified fix makes *your* first Friday cheap."

**2:50 – 3:00 · Trajectory**
> "Next: point it at a real repo and let it open the PR. Every fix anyone verifies makes everyone else's agent cheaper."

---
## Honesty beats — say these before anyone asks
- **The corpus is seeded** from a controlled replay of the app's bug history, so you see ten Fridays in ninety seconds. The scan is live. *"We'd rather show you the seam than hide it."*
- **The "no baseline yet" row** in the memory panel: *"that pattern shows nothing saved because it never paid full price to begin with. We only claim savings we can prove."*
- **What's live:** Replay, Actian, Senso, Pioneer — four, with evidence on disk. **Guild we investigated and cut**: their LLM proxy only exists inside a Guild-hosted runtime and coded agents are TypeScript-only, so integrating properly meant hosting our loop on their platform. Naming that beats a token integration.
- **Small n.** Five iterations. Say the number, show the seed, offer the raw JSONL.

## Tradeoffs, volunteered
One target app plus one transfer app, not arbitrary repos. Fixture fallbacks behind every integration so the demo cannot die. Feature freeze at 15:00 so the last ninety minutes went to making this bulletproof instead of adding things.

## If asked how you built it in five hours
Product first, code second. Problem statement and non-goals before any code. A pre-mortem naming five failure modes with an owned mitigation each. Then the check most teams skip: *is the problem real*, answered with Gartner, CodeRabbit and GitClear data. Then three parallel build lanes with strict file ownership, and a separate session holding the plan and reviewing every diff against the judging criteria.

## Failure drill
Wifi dies → `python -m ratchet.run --demo`, zero network, replays from `runs/golden/`. Docker down → `RATCHET_MEMORY_MODE=fixture`, say so. Everything dies → play the screen recording and narrate. See `RUNBOOK.md`.
