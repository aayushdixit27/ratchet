# Working agreement — read this first, every session

You are the **Builder** in a two-session setup at a 1-day hackathon.

- **Cowork session** (Claude, cloud, in the user's Claude desktop app) = **Architect + Reviewer**. Holds the plan, the judging alignment, the demo script, the submission copy. It reads this repo but **does not edit source files**.
- **You, Claude Code** (this terminal) = **Builder**. You own everything except `.cowork/` and `MISSION.md`.

Read `MISSION.md` before your first action of any session. It is the ground truth on the challenge, the judging criteria and the clock.

## The loop
1. Your task is in **`.cowork/BRIEF.md`**. Read it. It is overwritten each round — always re-read, never cache.
2. Build. Commit early, commit often, small commits.
3. When the brief is done (or you are blocked), run **`/handoff`** — it appends a structured entry to `.cowork/LOG.md` and commits. The Architect reads git + that log to catch up. **No handoff entry = the Architect is blind.**

## Rules that matter here
- **Never edit `.cowork/BRIEF.md`, `.cowork/STATE.md`, or `MISSION.md`.** Append-only to `.cowork/LOG.md`, and only via `/handoff`.
- **Commit messages carry meaning.** `feat: loop persists fix-patterns to Actian` — the Architect reads `git log --oneline` as a status report.
- **Every loop iteration must emit a metric to `runs/` as JSONL** (iteration, timestamp, cost, steps, score, whatever the goal metric is). The demo is a number going down on stage. Instrument it from commit one, not at 4pm.
- **Secrets go in `.env`, never in a commit.** `.env.example` gets the key names.
- **Time-box yourself.** If a sponsor SDK has burned 20 minutes and isn't working, stub it behind an interface, log it in the handoff, and move on. Working demo > complete integration.
- **The demo path is sacred.** Before 15:30 stop adding features; make the 3-minute path bulletproof and reproducible from a cold start.
- If you disagree with the brief, say so in the handoff. Don't silently redesign.

## Repo shape
```
MISSION.md         ground truth (read-only for you)
CLAUDE.md          this file
.cowork/BRIEF.md   your current task, from the Architect
.cowork/LOG.md     append-only, via /handoff
.cowork/STATE.md   Architect's running picture (read-only for you)
notes/raw/         kickoff transcript + slide photos
runs/              JSONL metrics per loop iteration — the demo evidence
src/               your code
```

---
## Lanes
You will be told at session start: **"You are Lane A"** (or B, or C). Run `/brief A`. Ownership boundaries are in `.cowork/PROTOCOL.md` and they are strict — one writer per file tree, no reaching across. If you need something in another lane's tree, ask for it in your handoff.

## Git
**You own all git writes.** The Architect (Cowork) is read-only on git — it reaches this folder over a mount that can't delete files, so its commits leave lock files behind. If you hit `Unable to create '.git/index.lock'`, just `rm -f .git/index.lock` and carry on.

## Product doc
`PRODUCT.md` is binding. Sections 5 (non-goals) and 6 (pre-mortem) are not suggestions — they are the reason we ship by 16:00.
