---
description: Close out the current brief — append to .cowork/LOG.md and commit. Usage: /handoff A
argument-hint: [lane letter]
---
You are closing out Lane **$ARGUMENTS**. Do all of the following, in order:

1. `git status --short` and `git log --oneline -10`. Stage and commit anything uncommitted with a meaningful message.
2. Check `runs/` for fresh JSONL from this round. If the brief required a metric and none exists, **say so plainly** in the entry rather than glossing over it.
3. Append one entry to `.cowork/LOG.md` in exactly the format at the top of that file, prefixed with the lane letter. Timestamp with real local time (`date +%H:%M`). Be blunt — if something is half-working, write half-working. The Architect makes scope cuts from this and cannot see your terminal.
4. If you need something from another lane's file tree, state it under **Blocked/next**. Do not reach across and edit it yourself.
5. `git add .cowork/LOG.md && git commit -m "chore: handoff $ARGUMENTS"`
6. Print a 2-line summary for the human to read aloud, then the exact string `catch up` so they know what to say in Cowork.

Never edit `.cowork/briefs/**`, `.cowork/STATE.md`, `MISSION.md`, or `PRODUCT.md`.
