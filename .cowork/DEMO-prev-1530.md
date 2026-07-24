# RATCHET — the demo. Follow literally.
*Rewritten 14:45. This file is the single source of truth for the presentation.*

**Two rules that override everything below:**
1. **Never type a live command you have not already run in Part 0.**
2. **Never speak a number you are not looking at.** Every figure here is a reference, not a script line.

**Preflight passed 14:39:** transfer.jsonl ✅ · golden ratchet ✅ · golden control ✅ · restore point ✅ · dashboard ✅ · offline replay ✅

**Numbers currently in golden** (verify on screen anyway):
| | iter 0 → 4 |
|---|---|
| Ratchet calls/fix | **4.25 → 3.5 → 2.75 → 1.0 → 1.0** |
| Control calls/fix | **5 → 5 → 6 → 5 → 8** |
| Split pane | cold **4 calls / $1.65** · warm **1 call / $0.0297** · similarity **0.849** |
| Transfer | **2 of 4 warm on first run**, globex ← tasker |

---

# PART 0 — Setup (30 minutes before)

**1.** Open Docker Desktop. Wait for the whale to stop animating.

**2.** Terminal tab 1:
```
cd ~/Downloads/"Self-Evolving Agents Hackathon"
docker start vectorai
docker ps | grep vectorai
```
Expect a line ending `vectorai`. **If not:** you're fine — say *"memory is on the local fallback"* during the demo and continue.

**3.** Still tab 1:
```
PYTHONPATH=src python3 -m ratchet.run --demo
```
Expect a table ending `iter 4 | 4 | 4/0 | 1.00`.
**Note `PYTHONPATH=src` and `python3`** — plain `python` does not exist on macOS.
`ModuleNotFoundError` → you dropped `PYTHONPATH=src`. Hangs >2 min → Ctrl-C, you don't need it.

**4.** Terminal tab 2 — **new tab, leave running all night**:
```
cd ~/Downloads/"Self-Evolving Agents Hackathon"
python3 -m http.server 8000
```
Expect `Serving HTTP on :: port 8000`. "Address already in use" → it's already up, fine.

**5.** Chrome: `http://localhost:8000/dashboard/index.html`
**Bare URL. No query parameters.** That is what makes it read `runs/golden/` and be immune to anything anyone runs.
Expect: two-line chart, split pane, memory panel, ACME → GLOBEX section.
Blank → tab 2 died. One line only → hard refresh Cmd+Shift+R.

**6.** Record the whole run once with QuickTime. Save it somewhere openable in ten seconds.

# PART 1 — Five minutes before
Five windows, in this order:
1. Terminal tab 1, cleared, font ≥18pt
2. Dashboard
3. `qa.replay.io`, logged in, on your bug list
4. `cited.md`
5. Your screen recording, paused

Phone face down. One breath.

---

# PART 2 — The three minutes

## Beat 1 · 0:00–0:25 · **Hands off the laptop. Look at them.**
> "Maya is the only person on a four-person team who cares about QA. There's no QA hire. She ships an AI-built internal tool most Fridays. She points Replay at the deploy, gets root-caused bugs back, pastes them into her coding agent, ships. Next Friday: more bugs — and some are the same *kind* she fixed last week, in different places, wearing different symptoms. She pays full price to rediscover something she already solved. And she knows. She's thinking *we've fixed this three times now*. Eventually she writes a lint rule, three sprints late. **Maya is the ratchet. She's doing it by hand, from memory, on top of her actual job. We automated her instinct — and we verify it.**"

## Beat 2 · 0:25–0:35 · Still no screen
> "Every team has a Maya. Gartner says by 2028, AI coding cost per developer will exceed that developer's salary. Pioneer makes every call cheaper. **We delete the call.**"

## Beat 3 · 0:35–1:15 · **Go to Replay** — this is now the strongest beat in the demo
*(Corrected 14:50: do NOT claim the fix write-back. All bugs currently read Open. Say only what is on screen.)*

Point at the run summary:
> "This is Replay QA against our deployed app. Their crawler, their journeys, their root-cause analysis. **17 journeys, one exploration, six bugs** — and we planted none of these. This is what our agent receives as input."

Point at the modal bug, then the failed-journey count:
> "One root cause — a modal rendering without its hidden class — took out **12 of 17 journeys**. Editing, filtering, settings, deletion, persistence, all blocked. One cause, many symptoms. That's the shape of the problem."

**Now scroll to the two counter bugs and read them out. This is the moment.**
> "Look at these two. *'Remaining-tasks counter displays one fewer due to a stale minus-one adjustment.'* And: *'Task counter shows incorrect tasks-remaining count due to a stale minus-one adjustment in the render function.'*"
> "**Same root cause. Filed twice.** And Replay's own summary says a near-duplicate was already judge-rejected and asks a human to consolidate before fixing."
> "**That is Maya.** That is the exact problem, happening right now, in a production QA tool, discovered independently of us. Their system can tell these are related. What nobody has is the thing that *remembers the fix* so the second one costs three cents instead of a dollar sixty-five."

*Replay won't load → skip to Beat 4, say "Replay's UI is down, here's what it handed us."*

## Beat 4 · 1:15–1:55 · **Dashboard, split pane**
Left column:
> "First time it has ever seen this root cause. **Four** separate reasoning calls. **$1.65.**"

Right column, green box:
> "Same root cause. Different bug, different selector, different file. **One** call. **Three cents.** It didn't think — it remembered."

*Asked about model names → "that run is the seeded corpus at reference prices; the live runs use gpt-5.5, Opus and DeepSeek through Pioneer's router, and I'll show you the records."*

## Beat 5 · 1:55–2:25 · **Scroll up, hero chart**
Point at red:
> "That's Maya's Friday. Replay plus a coding agent, memory off, same bugs, same models. Not a criticism of Replay — that's their output, and it's our input."

Trace it rising:
> "It doesn't flatten. It **climbs — five calls per fix to eight** — because it keeps re-failing on classes it's already seen. There's a published result where vulnerabilities rose 37.6% over five unmemoried iterations. We reproduced it by accident."

Point at yellow:
> "**Ours goes to one.**"

Cost tile:
> "In dollars it's a range, not a clean curve — at real prices these are cents and the variance beats the signal. So we report the invariant: calls. Pioneer's telemetry shows what their routing saved on top. Those stack."

## Beat 6 · 2:25–2:50 · **Scroll to ACME → GLOBEX**
> "Different app. Different company. A notes app called Jotting. First run it has ever done."

Point at the two warm rows:
> "**Two of four bugs fixed warm on the first run** — patterns verified on the other app transferred."

> "Meta published this working inside Meta. EvoRepair published it inside one repo. **Everyone built the private version.** The economics only get interesting when *my* verified fix makes *your* first Friday cheap."

## Beat 7 · 2:50–3:00 · Look up. Stop clicking.
> "Next: point it at a real repo and let it open the PR. Every fix anyone verifies makes everyone else's agent cheaper."

**Then stop talking.**

---

# PART 3 — Volunteer these before anyone asks
- *"The corpus is seeded from a controlled replay of the app's bug history, so you see ten Fridays in ninety seconds. The scan is live."*
- *"That row shows nothing saved because it never paid full price. We only claim savings we can prove."*
- **Do not claim the Replay fix write-back.** The `mark_fixed` call is implemented but no bug currently shows Fixed in their dashboard. If asked: *"we implemented the write-back against their PATCH endpoint; we have not verified it landed, so I am not going to claim it."*
- *"Four sponsors live: Replay, Actian, Senso, Pioneer. **Guild we investigated and cut** — their LLM proxy only exists inside a Guild-hosted runtime and their coded agents are TypeScript-only, so integrating properly meant hosting our loop on their platform."*
- *"Five iterations. Small n. Here's the seed, and I'll hand you the raw JSONL."*

## The four questions judges ask
- **Who is the user?** Maya. Teams shipping AI-generated code whose QA spend scales linearly with release count.
- **Why AI, not a lint rule?** She can't write a rule for "this modal doesn't reset state" that generalises to a modal she's never seen. Same root cause, different selector, different file. Matching requires understanding the cause.
- **What's different?** Everyone's agent acts. Ours has a cost curve that bends, and the corpus crosses company lines.
- **What did you trade off?** One target app plus one transfer app. Fixture fallbacks behind every integration. Feature freeze at 15:00.

---

# PART 4 — Failure table

| Symptom | Do this, out loud |
|---|---|
| Wifi dies | *"Good, this is the offline path."* → `PYTHONPATH=src python3 -m ratchet.run --demo`. Dashboard unaffected, it reads golden. |
| Dashboard blank | Terminal tab 2 died. Restart the server, reload. |
| Chart shows one line | Hard refresh, Cmd+Shift+R. |
| Docker down | *"Memory's on the local fallback, same retrieval scores."* Keep going. |
| Replay page dead | Skip Beat 3's click-through, use the cold pane. **Never re-run an exploration.** |
| Numbers look wrong | Read what's on screen. **Never correct from memory.** |
| Golden looks corrupted | `cp runs/golden-fixture/*.jsonl runs/golden/` |
| Total failure | Play the recording. Narrate over it. Still a demo. |

---
**Rehearse Beats 1 and 6 twice out loud.** They carry everything else.
