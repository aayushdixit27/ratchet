---
description: Bootstrap a fresh session as a lane, from disk. Usage: /resume B
argument-hint: [lane letter]
---
You are Lane **$ARGUMENTS**, resuming after a context clear. A previous session wrote your state to disk.

**Read in this exact order and STOP when you have enough. Do not read ahead.**
1. `CLAUDE.md` — the working agreement
2. `.cowork/state/$ARGUMENTS.md` — **your predecessor's working memory. Section 4 (REJECTED) is the most important thing in this repo for you.**
3. `.cowork/state/GLOBAL-REJECTED.md` — dead ends every lane must avoid
4. `.cowork/briefs/` — your most recent brief, plus any `ALL-*` brief newer than it
5. `git log --oneline -15` — what has landed since
6. Last 2 entries of `.cowork/LOG.md`

**Do NOT read:** other lanes' source trees, `MISSION.md`/`PRODUCT.md`/`EVIDENCE.md`/`POSITIONING.md` unless a brief tells you to, or any file "for background". Context is the scarce resource; that is why you were cleared.

Then:
- Restate in 3 bullets: what you own, what state it's in, what your next concrete action is.
- Flag immediately if state and disk disagree — **disk wins**, and say so in your next handoff.
- Execute. Commit every ~15 min. `/handoff $ARGUMENTS` when done.
