# LANE C — working state as of 13:55
*Drafted by the Architect from Lane C's handoffs. Lane C should ADD sections 4 and 6 from its own session memory before clearing — the Architect cannot see what you tried and abandoned inside your context.*

## 1. Identity
**Own:** `app/**`, `app2/**`, `dashboard/**`
**Never touch:** anything under `src/`, `runs/` (read-only), `.cowork/**` except appending to `LOG.md` via `/handoff C`
**Model:** Fable 5 (switch to Opus for judgement-heavy design work; Fable for styling/label passes)

## 2. Ground truth right now
- **Tasker fixture app is LIVE:** `https://aayushdixit27.github.io/tasker-fixture/` — GitHub Pages, canonical. The trycloudflare tunnel is a hot spare and must not be quoted anywhere.
- `/BUGS.md` and `/bugs.json` both **404 publicly** — the answer key is not crawlable by Replay or anything else. Keep it that way.
- **App #2 is LIVE:** `https://aayushdixit27.github.io/jotting-fixture/` — a notes app from a "different company". 6 bugs: 2 share Tasker's `modal-state-not-reset` class (wrong-note share invite; resurrecting ghost tag), 4 novel. **All 6 harness-verified in headless Chrome, 6/6 reproduce exactly as documented.**
- `app/bugs.json` and `app2/bugs.json` are the **machine-readable ground truth** Lane B consumes. `BUGS.md` is human-readable only — Lane B's markdown parser was removed because it silently produced garbage rows.
- `dashboard/index.html` is a **single file**, polls `../runs/*.jsonl`, and its data source is **parameterized** — swapping `runs/golden/` requires zero Lane C work.
- **Hero chart is calls per verified fix**, two arms. On the fixture golden: control rises **5 → 8**, Ratchet falls to **1**. Cost lives in a stat tile as a *range*, with Pioneer's routing spread beside it when telemetry is present.
- Memory panel **merges by bug class**; leads with `modal-state-not-reset — 5 uses, 2 patterns, $1.94 saved`, and its dollar sum reconciles exactly with the `$5.07` tile.
- Path-share bars read `N% warm` in green.
- **ACME → GLOBEX banner is built and proven** against a test row. It lights up automatically the moment Lane A's transfer JSONL lands. Required fields on those rows: `corpus_from`, `target`, `origin_org`, `warm` + `verified`. Org names and all numbers derive from the data.
- `$0.000` savings rows render as **"no baseline yet"** — never a computed fallback.
- Render verified against **both** 14:15 outcomes: fixture golden (4-call cold, 4.3 → 1.0) and candidate live (1-call cold, 1.3 → 1.0, visually almost flat).

## 3. Commands that work
```bash
# serve the dashboard locally against golden
python3 -m http.server 8000     # then open /dashboard/index.html

# unstick a wedged GitHub Pages build (this happened once and cost 15 min)
gh api -X POST repos/<owner>/<repo>/pages/builds
```

## 4. REJECTED — do not retry
*(Architect-known items; **Lane C must add its own before clearing**)*
- **trycloudflare tunnel as the canonical URL** — dies when the machine sleeps and reissues a different URL. GitHub Pages survives sleep. Pages is canonical.
- **Parsing `BUGS.md` as machine-readable ground truth** — a lenient parser yielded nonsense rows that passed a naive length check. `bugs.json` only.
- **Hardcoding a data source in the dashboard** — the golden file may be swapped at 14:15; the source stays parameterized.
- **Relabelling a fixture run as live in the renderer** — render exactly what the JSONL says. Model-label problems get fixed at the source by Lane A/B, never in the view.
- Also see `.cowork/state/GLOBAL-REJECTED.md`.

## 5. In flight
Nothing. All of C-001, C-002, C-003, C-004 and ALL-012's four items are complete and verified on screen. **Blocked only on Lane A's `--target app2 --corpus-from tasker` JSONL**, at which point the transfer banner lights with no further work.

## 6. Gotchas
- GitHub Pages' legacy build pipeline can **wedge**; an explicit `POST /pages/builds` unsticks it.
- Everything must render from `runs/golden/` with **zero network** — that is the wifi-dies path.
- Design target is a **dim room, a projector, fifteen feet, tired judges at 19:00**. Contrast and size beat elegance. No animation that delays comprehension.
- *(Lane C: add anything that failed confusingly in your session.)*

## 7. Pointers, not content
Read in this order, and only these: `CLAUDE.md` → this file → `.cowork/state/GLOBAL-REJECTED.md` → `DEMO.md` (**rewritten 13:50, supersedes all earlier drafts**) → `.cowork/briefs/ALL-012.md` → `RUNBOOK.md`.
Do **not** read `MISSION.md`, `PRODUCT.md`, `EVIDENCE.md` or `POSITIONING.md` unless a brief sends you there.
