# The three words

Spoken by Yoshi in the **Cowork** session. Everything else is conversation.

### "brief"  → hand off to Claude Code
The Architect writes `.cowork/BRIEF.md` and hands back one line to paste into Claude Code:
> `Read .cowork/BRIEF.md and execute it.`

A brief always contains: goal, done-criteria, files to touch, files NOT to touch, the metric it must emit, and a time-box.

### "catch up"  → hand back to Cowork
The Architect reads, in this order:
1. `git log --oneline` since last checkpoint
2. `git diff <last-checkpoint>..HEAD --stat`, then the interesting hunks
3. `.cowork/LOG.md` new entries
4. `runs/*.jsonl` — is the metric actually moving?

Then returns: what landed, what's off-spec, what's now the biggest risk to the 16:30 deadline, and the next brief.

### "ship"  → produce submission artifacts
From actual repo state, not from intent: submission copy, README, the 3-minute demo script with exact clicks and the moment the number drops, and the sponsor-prize checklist.

---
## Why this shape
- One writer per file. The Architect owns `.cowork/` + `MISSION.md`; the Builder owns everything else. No merge conflicts, no clobbering.
- Git is the source of truth about *what happened*; the log is the source of truth about *why*. Cheap for the Architect to re-read both after any gap.
- You never re-explain context. Both sessions bootstrap from files on disk.

## Checkpoints — Architect's job, unprompted where possible
- **13:00** — is the loop closed end-to-end (even if fake data)? If not, cut scope now.
- **15:00** — feature freeze. Demo path only.
- **15:30** — submission draft ready; portal confirmed.
- **16:00** — submitted. Rehearse the 3 minutes twice.
