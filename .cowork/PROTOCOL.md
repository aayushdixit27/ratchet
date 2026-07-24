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

## Checkpoints — Architect drives these
- **13:00** — is the loop closed end-to-end on fixtures? If not, cut scope *now*.
- **14:00** — at least 3 live sponsor integrations green. Warm-path share rising.
- **15:00** — **feature freeze.** Demo path only. Start the screen recording.
- **15:30** — submission draft ready; portal confirmed in Discord.
- **16:00** — submitted. Rehearse the 3 minutes twice, once to a stranger.
