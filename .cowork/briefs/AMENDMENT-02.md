# AMENDMENT 02 — positioning, made structural
**Issued 11:50. Read `POSITIONING.md` and `DEMO.md` first — this brief just makes them true in code.**

## ⚠️ Nothing here comes before the 12:45 ugly-end-to-end gate.
Land the join first — loop → JSONL → moving line. *Then* apply this. Do not let a positioning change cost us the demo path. That mistake is how teams die at 16:00.

## Why
Replay QA already finds bugs, root-causes them and suggests fixes. Their CEO is judging. We do not compete with that — we consume it. Our claim is the one thing they demonstrably don't do: **remember across runs.** These changes make that claim an artifact instead of a sentence.

---

## Lane A — the loop core

**1. `--no-memory` control arm. This is the single most valuable thing you will build today.**
Same bugs, same model, same seed — memory disabled, reasons from scratch every iteration. Emit to `runs/control.jsonl` with identical schema plus `"arm": "control" | "ratchet"`.
A full run should execute **both arms** so the chart has two lines. Control flat; Ratchet bending. It's a flag around an if-statement — cheap — and it is the entire answer to "isn't this just Replay?"

**2. `saved_usd` accounting.** On every warm hit, record `saved_usd = mean_cold_cost(bug_class) - actual_cost`. Accumulate per pattern. The dashboard sorts on it. "This one pattern has saved $3.71" is the fundability line.

**3. Provenance on every pattern** (Lane B is adding the fields):
`discovered_by`, `root_cause_source`, `verified_by`, `verified_at`, `verification_count`, `born_at_iteration`.
Set them honestly — `"replay-qa"` when live, `"fixture"` when not. **Never label fixture data as Replay-sourced.** Judges score the gap between demo and build, and a mislabelled provenance field is exactly the kind of thing that gets found.

**4. `evolve()` stays gated** behind wow #1 running clean twice unattended. It also overlaps Guild's existing optimize feature more than we'd like, so it is now clearly our *second* claim.

## Lane B — adapters

**Priority order changes. Replay moves up; the story is fake without it.**

| new # | adapter | why |
|---|---|---|
| 1 | **Memory (Actian)** | the thesis |
| 2 | **QA (Replay)** | ⬆ was #3. If Replay is fixture-only, "Replay finds, we remember" is a lie a judge can check. **Must be live.** |
| 3 | Router (Pioneer) | fixture cost numbers are good enough to demo if this slips |
| 4 | Publisher (Senso) | ⬆ was #5 — `cited.md` carries the "public corpus, not a private cache" argument |
| 5 | Tracer (Guild) | nice, not load-bearing |

**Extend `Pattern`** with: `discovered_by: str`, `root_cause_source: str`, `verified_by: str`, `verified_at: str | None`, `verification_count: int = 0`, `born_at_iteration: int = 0`, `saved_usd: float = 0.0`. Tell Lane A the moment it's committed.

**`FixturePublisher` must write a genuinely readable `cited.md`** at repo root — human-legible entries, each citing its source. That file gets opened on stage at 2:30. It is not a stub.

**Keep `replay.py` thin and don't apologise for it.** "Our Replay adapter is forty lines because Replay does the hard part" is a line we're saying out loud. A thin QA adapter next to a thick `memory/` module argues the positioning to anyone who opens the repo.

## Lane C — the demo surface

**1. Two lines on the hero chart** — `control` flat, `ratchet` bending. Label them **"Replay + coding agent (today)"** and **"Ratchet"**. This chart *is* the argument; give it the most pixels.

**2. Memory panel** — every pattern with `born_at_iteration`, `uses`, `saved_usd`, and its `discovered_by` source badge. Sorted by `saved_usd` descending.

**3. Cold/warm split pane — mandatory.** Two columns, same bug class. Left: the cold reasoning transcript, call count, cost. Right: one line — `MEMORY HIT · pattern #3 · similarity 0.91 · learned at iteration 1` — then cost. The chart is the proof; **this is the feeling**. It runs 1:10–2:00, the longest single beat of the demo.

Read `DEMO.md`. Every screen in that script must exist and be legible from 15 feet in a dim room. Anything not in that script is not in scope.
