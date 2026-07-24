# Handoff log — append-only, newest at the bottom

Format per entry:
```
## [HH:MM] <brief id> — <status: done | partial | blocked>
**Landed:** what actually works now
**Metric:** what runs/ shows
**Deviated:** where I went off-brief and why
**Blocked/next:** what the Architect needs to decide
**Commits:** <sha> <sha>
```

---

## [11:33] C-001 — partial (both deliverables landed; hosting is fragile)
**Landed:**
- **PUBLIC URL IS LIVE — Replay QA can reach it now:**
  `https://frames-heading-institution-catherine.trycloudflare.com`
  Verified 200 on `/`, `/app.js`, `/styles.css` and screenshotted rendering through the tunnel.
- `app/` — vanilla HTML/CSS/JS Tasker. No build step. **8 bugs seeded, exactly 3 sharing
  `modal-state-not-reset`.** The shared three are a genuine single root cause: all three modals
  lazily seed a scratch object (`editDraft` / `settingsDraft` / `pendingDelete`) with the
  `x = x || seed()` idiom, and `closeModal()` only toggles `.hidden` — it never nulls them. One
  fix strategy ("reset modal-owned state on close") resolves all three. Symptoms look completely
  different: stale edit form / discarded settings reappearing / **confirm dialog deleting the
  wrong task**. BUG-04 and BUG-07 are visible on first paint without any interaction, so the
  crawler gets an immediate hit.
- Ground truth in `app/BUGS.md` (human) and `app/bugs.json` (machine: id, class, selectors,
  repro steps, root cause, `fix_strategy`, severity). Lane B is already reading `bugs.json`
  (3f5680d) — that contract is proven working, no action needed.
- `dashboard/index.html` — single file, no framework, polls every 2s. Hero cost-per-verified-fix
  line, warm/cold stacked bars, patterns-learned list, 3 stat tiles, plus a slow-loop
  policy-rewrite strip that appears when it sees a `policy_rewrite` event. Dark, huge type,
  fits one 1440x900 screen with no scrolling. Verified by screenshot in two modes.

**Metric:** **`runs/` is empty — there is no JSONL yet.** I do not own `runs/` and cannot emit
one. So the AMENDMENT-01 §2 join is **unproven end-to-end**: my half is verified only against a
hand-written file. The dashboard reads a real file correctly (aggregation, tiles, warm/cold
shares, pattern first-seen all correct) — but nothing has yet flowed from Lane A's emitter to my
renderer. Treat the join as NOT done until someone runs both.

**Deviated:**
- **Hosting is not what the brief specified.** Plan was GitHub Pages: repo
  `aayushdixit27/tasker-fixture` (public, 3 runtime files only — the answer key is deliberately
  NOT published) created and Pages enabled via API. It has now sat in `status: building` for
  ~15 min and still 404s. I blew the 15-min cap, so per the brief I fell back to a `cloudflared`
  quick tunnel. **This is fragile:** the URL dies if my machine sleeps or the process is killed,
  and a new URL is issued on restart. Two local `python3 -m http.server` processes (8890 for the
  app, 8899 for serving the dashboard) must stay up.
- Swapped one suggested singleton: dropped "delete confirm returns wrong boolean" because it
  would have collided with BUG-03's root cause and blurred the shared class. Replaced with
  `missing-input-validation` (whitespace-only tasks accepted). Still 5 distinct singletons.
- Added two files beyond the brief: `app/bugs.json` (Lane B needed machine-readable ground truth)
  and `dashboard/SCHEMA.sample.jsonl` (the schema contract, below).
- Dashboard has `?demo=1` for labelled synthetic data and `?src=<path>` to point at any JSONL.
  Synthetic mode paints a loud amber "SYNTHETIC DEMO DATA" banner so it can never be mistaken
  for a real run on stage.

**Blocked/next:**
1. **Lane A — schema.** The dashboard accepts field aliases so a rename can't blank the
   projector, but the canonical shape is `dashboard/SCHEMA.sample.jsonl`, one JSON object per
   line: `iteration` (int, 0-based), `bug_id`, `bug_class` (must match `app/bugs.json` classes —
   this is what drives the patterns list), `path` (`"warm"`|`"cold"`), `cost_usd` (float),
   `steps` (int), `verified` (bool). Slow loop emits `{"iteration":N,"event":"policy_rewrite",
   "note":"..."}`. Aliases accepted: cost_usd|cost|usd, path|route|mode, iteration|iter|loop,
   bug_class|class|pattern_id, steps|step_count. Cost-per-fix = total iteration cost / verified
   fixes that iteration, so **emit a row per attempt, including failed ones**, or the curve lies.
2. **Architect decision needed — hosting.** Do we keep waiting on GitHub Pages (it may still
   resolve, and it's far more stable for the demo), or commit to the tunnel and put its URL in
   the submission? If Pages goes green I'll swap and re-handoff the URL. If we stay on the
   tunnel, someone must confirm the URL is alive right before the demo.
3. I did **not** commit the uncommitted work in `src/ratchet/`, `src/adapters/live_*.py`,
   `pyproject.toml`, `EVIDENCE.md`, `PRODUCT.md`, `CLAUDE.md`, `.cowork/` — that is Lane A/B
   in-flight state and committing it mid-edit would be reaching across lanes. Someone who owns
   those trees should commit them.

**Commits:** cdf59ec 0d916df 6d0a93f
