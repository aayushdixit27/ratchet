# RATCHET — the 3 minutes
*Rewritten 15:35. One tab. Five screens. Right-arrow only.*

**Concept, and everything hangs off it:**
> ## The QA agent that gets cheaper every time you ship.

**Two rules:** never type a live command you haven't already run in setup · never speak a number you're not looking at.

---
# SETUP (30 min before)
```
open -a Docker                          # wait for the whale to stop moving
cd ~/Downloads/"Self-Evolving Agents Hackathon"
docker start vectorai && docker ps | grep vectorai
PYTHONPATH=src python3 -m ratchet.run --demo
```
Then open **`deck.html` full screen** (Cmd+Ctrl+F) and press `r` to reset the timer.
Second tab: **qa.replay.io**, logged in, on the bug list.
Third tab: your **screen recording**, paused.
Nothing else open. Phone face down.

**Deck controls:** `→` or space forward · `←` back · `r` resets the timer.
Timer top-left goes amber at 2:30, red at 3:00. Progress bar along the bottom.

---
# THE THREE MINUTES

## 0:00–0:25 · Screen 1 — Replay filed the same bug twice
**Don't touch the laptop yet. Look at them.**

> "Somebody on a small team owns quality, and there's no QA team behind them. They ship every week. Every week they re-fix something they already solved. They know they're doing it. They just have no way to make it stop."

**Now gesture at the screen.**

> "This isn't our claim. We pointed Replay QA — a production bug-finding tool — at a web app. It filed these two bugs separately, hours apart. Same cause. And their own summary asks a human to *consolidate before fixing*."

> "**That's the whole problem. Coding agents forget, so somebody pays to solve the same thing twice, forever.**"

`→`

## 0:25–1:10 · Screen 2 — It didn't think. It remembered.
> "First time our agent sees a bug, it reasons from scratch. Find it, work out why, write the fix, check its own work. **Four AI calls. A dollar sixty-five.**"

*(pause, let them read the left column)*

> "Next time that same cause shows up — different file, different button, a symptom that looks nothing like it — **one call. Three cents.**"

> "And it only remembered that fix because **Replay re-tested it and confirmed it worked.** We don't remember what a model said. We remember what got verified."

`→`

## 1:10–1:50 · Screen 3 — Turn memory off and it gets worse
> "Same bugs. Same models. The only thing we changed was memory."

**Trace the orange line with your finger.**

> "Memory off — that's how everyone does this today — starts at five calls per fix and **climbs to eight**, because it keeps re-failing on bugs it has already seen."

**Then the blue line.**

> "Ours goes to one."

> "Not improving isn't the failure mode. **Getting worse is.** There's published work where security flaws rose 37% over five rounds of unremembered self-improvement. We reproduced it by accident."

`→`

## 1:50–2:30 · Screen 4 — Her fix made their first day cheap
> "Then we pointed it at a completely different app. A notes app, different team, **never seen it before.**"

> "On its very first run, **two of the first four bugs were fixed straight from memory** — because fixes verified on the other app carried over."

> "Meta published this working inside Meta. There's a paper called EvoRepair that did it inside one repo. **Everyone built the private version.** The economics only get interesting when *my* verified fix makes *your* first day cheap."

`→`

## 2:30–2:50 · Screen 5 — Runs offline, including the arm that loses
> "All of it runs with no network, same result every time. Bugs from Replay, memory in Actian, routing by Pioneer."

> "And we ship the arm that loses. If we were dressing this up, that second block wouldn't be on the screen."

## 2:50–3:00 · Close
**Look up. Hands off the keyboard.**
> "Next: point it at a real repo and let it open the pull request. Every fix anyone verifies makes everyone else's agent cheaper."

**Stop talking.**

---
# ANSWERS — say these before they ask
- **Who's it for?** The one person on a small team who owns quality and has no QA team.
- **Why AI?** The same bug wears different clothes each time. You can't write a rule for a bug you haven't seen yet.
- **Why different?** Every QA tool costs the same on run 100 as run 1. Ours gets cheaper, and the memory crosses company lines.
- **What did you cut?** Two test apps instead of real repos. Five rounds, not five hundred. An offline fallback behind every integration. Froze features with 90 minutes left.

**Limits — volunteer them:**
- "The five-round curve runs on a seeded set so you see ten weeks in ninety seconds. The bug discovery is live."
- "Five rounds is a small sample. Raw data's in the repo."
- "One pattern shows nothing saved because it never paid full price. We only count savings we can prove."
- **Don't claim the Replay write-back.** It's implemented, not verified. If asked: *"we built it against their endpoint, we haven't confirmed it landed, so I won't claim it."*

**Sponsors, one line each:** Replay finds the bugs · Actian remembers the fixes · Senso publishes them · Pioneer routes every call and reports what it saved. **Guild we investigated and cut** — their proxy only works inside their runtime, their agents are TypeScript-only.

---
# IF IT BREAKS
| Symptom | Do this, out loud |
|---|---|
| Deck won't open | It's one HTML file. Drag it into any browser. |
| Wifi dies | Doesn't matter. The deck is local, the data is on disk. |
| Replay tab dead | Skip it. Screen 1 has their bug text on it already. |
| Docker down | *"Memory's on the local fallback, same match scores."* Keep going. |
| Numbers look wrong | Read what's on screen. Never correct from memory. |
| Total failure | Play the recording. Narrate over it. Still a demo. |

**Rehearse screens 1 and 4 twice out loud.** They carry the rest.
