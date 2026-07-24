# AMENDMENT 01 — all lanes, read now, mid-flight
**Issued 11:35. Supersedes any conflicting instruction in your -001 brief.**

Source: a 15x-hackathon veteran's build system (`.cowork/BUILD-RULES.md`). Two things we were getting wrong.

## 1. One wow at a time — and it isn't the one you think

**Lane A:** your brief told you to prioritise `evolve()` (the self-rewriting `policy.yaml`) above live APIs. **That is now demoted.** New order:

1. **Wow #1 — the cost curve.** Cold path vs warm path, cost and call-count per verified fix falling across iterations, written to `runs/ratchet.jsonl`. Clean, deterministic, repeatable twice in a row unattended.
2. **Only then, wow #2 — `evolve()`** and the self-authored diff.

Do not start `evolve()` until wow #1 has run end-to-end twice with nobody touching it. If you're already deep in `evolve()`, commit what you have, park it, and go make the curve clean.

## 2. Ugly end-to-end by 12:45 — this is a joint deliverable

Right now three correct pieces are being built and **nobody owns the join**. That's the classic way to be at 90% at 16:00 with nothing to show.

By **12:45** this must be true: `python -m ratchet.run --iterations 5 --mode fixture` writes JSONL, and `dashboard/index.html` opened in a browser shows a line that moves. Fake numbers are fine. Ugly is fine. Broken styling is fine. **Joined is not optional.**

- **Lane A owns the join.** If Lane C's dashboard isn't reading your file, say so in a handoff immediately — don't work around it, and don't edit their files.
- **Lane C:** the dashboard moves ahead of the fixture app polish. A public URL and a chart that renders beat a beautiful broken app.
- **Lane B:** by 12:45 the fixtures must be good enough for A to run offline. Live integrations continue *after* the join, in the priority order you already have.

## 3. Demo mode is a rehearsed artifact, not a flag you wrote once

`--demo` must replay a full 5-iteration run from cache with **zero network**, deterministically, in under ~90 seconds. Lane A owns it. It gets *run* at every checkpoint, not just written. If the venue wifi dies at 19:00 with 200 people on `717Guest`, this is the entire demo.

## 4. Cadence
Commit every 15 minutes. From 13:30, every 45 minutes, answer one question honestly from what is on disk: **"Can we demo right now?"** If no, we cut scope before anyone writes another line. No rewrites of another lane's landed work after 14:00.
