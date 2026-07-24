---
description: Close out the current brief — append to .cowork/LOG.md and commit
---
Do all of the following, in order:

1. Run `git status --short` and `git log --oneline -10`. Stage and commit anything uncommitted with a meaningful message.
2. Check `runs/` — is there fresh JSONL metric data from this round? If the brief required a metric and none exists, say so plainly in the entry rather than glossing over it.
3. Append one entry to `.cowork/LOG.md` in exactly the format documented at the top of that file. Timestamp with the real local time (`date +%H:%M`). Be blunt: if something is half-working, say half-working. The Architect makes scope cuts based on this and cannot see your terminal.
4. Commit the log entry: `git add .cowork/LOG.md && git commit -m "chore: handoff <brief id>"`.
5. Print a 2-line summary for the human to read aloud, plus the exact string `catch up` so they know what to say in Cowork.

Never edit `.cowork/BRIEF.md`, `.cowork/STATE.md`, or `MISSION.md`.
