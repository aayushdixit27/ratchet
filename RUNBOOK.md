# DEMO RUNBOOK — cold start to three minutes
*Print this. Follow it literally. Do not improvise at 19:00.*

## T-30 min — cold start checklist
```bash
# 1. Docker + Actian must be UP before anything else
open -a Docker                      # if not already running
docker start vectorai               # container persists; it just needs starting
docker ps | grep vectorai           # confirm

# 2. Sanity: the loop runs offline, from golden
python3 -m ratchet.run --demo
```
- `ENGINE_NOT_INITIALIZED` for the first ~10 seconds after the container starts is **expected** — the loop backs off and retries. Don't panic, don't restart it.
- If Docker will not start: run with `RATCHET_MEMORY_MODE=fixture`. Retrieval scores match live to four decimal places, so the curve is identical. **Say so if asked; don't hide it.**

## T-10 min — screens open, in this order
1. Terminal, cleared, big font, in the repo
2. `dashboard/index.html` open in a browser
3. Replay QA project page, logged in, showing the bug list
4. `cited.md` open in an editor
5. Screen recording of the full run, open in a background tab — **the fallback**

## The three minutes
Follow `DEMO.md` exactly. Maya first, 25 seconds, no screen.

## If something breaks
| Breaks | Do this |
|---|---|
| Wifi dies | `python3 -m ratchet.run --demo` — zero network, replays from `runs/golden/` |
| Docker/Actian down | `RATCHET_MEMORY_MODE=fixture`, say it out loud |
| Replay slow or 500s | Skip the live scan beat, use the cached bugs. **Never re-explore live** — it takes minutes |
| Dashboard blank | Check it's reading `runs/golden/`, not a half-written live run |
| Everything dies | Play the screen recording. Narrate over it. Still a demo |
| Live golden run looks wrong | `cp runs/golden-fixture/*.jsonl runs/golden/` — restores the verified zero-network fixture run |

## Never do these
- Never re-run Replay exploration during the demo
- Never overwrite `runs/golden/`
- Never set `RATCHET_MODE=live` globally
- Never claim a sponsor is live if it degraded — the records carry `degraded: true` and a judge can read them

## Honest status to state on stage
- **Live with evidence:** Replay QA (real scan of the deployed app, real bugs, `mark_fixed` written back into their system) · Actian VectorAI (primary memory, real vector search) · Senso (publishing verified patterns)
- **Pioneer:** integrated and working, gated behind their card-on-file requirement
- **Curve:** seeded corpus, so ten Fridays fit in ninety seconds. The scan is live. **Show the seam, don't hide it.**
