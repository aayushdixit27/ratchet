# The three words

Spoken by Yoshi in the **Cowork** session. Everything else is conversation.

### "brief"  → hand off to Claude Code
The Architect writes `.cowork/briefs/<LANE>-<n>.md` and hands back one line to paste:
> `You are Lane A. Read .cowork/briefs/A-001.md and execute it.`

A brief always contains: goal, done-criteria, files owned, files forbidden, the metric it must emit, and a time-box.

### "catch up"  → hand back to Cowork
The Architect reads, in order: `git log --oneline` since last checkpoint → `git diff --stat` then the interesting hunks → new `.cowork/LOG.md` entries → `runs/*.jsonl` (is the metric *actually* moving?).
Returns: what landed, what's off-spec, the biggest risk to 16:30, and the next brief.

### "ship"  → produce submission artifacts
From real repo state, not intent: submission copy, README, the 3-minute demo script with exact clicks and the moment the number drops, and the sponsor-prize selection checklist.

---
## Lanes — one writer per file tree, no exceptions

| Lane | Owns | Never touches |
|---|---|---|
| **A** loop core | `src/ratchet/**`, `runs/**`, `policy_history/**` | `src/adapters/**` (reads `base.py` only), `app/**`, `dashboard/**` |
| **B** adapters | `src/adapters/**`, `.env.example` | `src/ratchet/**`, `app/**`, `dashboard/**` |
| **C** fixture + demo | `app/**`, `dashboard/**` | everything under `src/` |

Nobody touches `.cowork/**` (except appending to `LOG.md` via `/handoff`), `MISSION.md`, or `PRODUCT.md`.
If a lane needs something from another lane's tree, it says so in the handoff. It does not reach across.

## Checkpoints — Architect drives these, unprompted
See `.cowork/BUILD-RULES.md` for the reasoning.

- **12:45** — **UGLY END-TO-END.** Loop writes JSONL, dashboard draws a moving line. Ugly is the point. Lane A owns the join.
- **13:45** — halfway. Demoable or we cut, no negotiation.
- **13:30 / 14:15 / 15:00 / 15:45** — ask literally, out loud: **"Can we demo right now?"** Not "nearly." If no, cut scope before another line is written.
- **15:00** — feature freeze. Demo path only. Start the screen recording.
- **15:30** — submission draft ready; portal confirmed in Discord.
- **16:00** — submitted. Rehearse the 3 minutes twice, once to a stranger.

**One wow at a time:** wow #1 is the cost curve bending. Wow #2 (`evolve()` rewriting its own policy) is gated until #1 runs clean twice unattended.

---
## Git ownership — important

The Architect reaches this folder over a mount that **cannot delete files**, so any git *write* from the Cowork side leaves `.lock` files behind and breaks the repo for everyone.

**Therefore: builders own 100% of git writes. The Architect is read-only on git** (`git log`, `git diff`, `git show` — never `commit`, `add`, `checkout`, `merge`).

Lane A: on your first action, run `git commit -m "docs: lock RATCHET product brief + three lane briefs"` — there are staged changes from the Architect waiting. Then confirm `git status` is clean.

If you ever see `Unable to create '.git/index.lock': File exists` — it came from the Architect. `rm -f .git/index.lock` works fine from your side (native filesystem); it does not from ours.
