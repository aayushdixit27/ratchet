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

## [11:34] B-001 — partial
**Landed:** All five adapters exist behind one contract and the loop cannot be crashed by any of them.
- `src/adapters/base.py` — contract shipped verbatim as briefed (committed 10 min in, Lane A unblocked). Added `Degradable` mixin + `usage()` helper so every router reports cost in one shape.
- Five deterministic fixtures. `RATCHET_MODE=fixture` (default) = **zero network**. Per-adapter override (`RATCHET_MEMORY_MODE=live`) so we can demo one live integration at a time.
- Five live adapters written: Pioneer, Actian, Replay, Guild, Senso. Every one try/excepts, degrades to its fixture, sets `degraded: true`, never re-raises.
- **Verified: `RATCHET_MODE=live` with zero API keys behaves byte-identically to fixture mode.** warm=2 cold=1 over 3 iterations in both. That is the wifi-dies insurance and it is real.
- `FixtureQA` reads Lane C's `app/bugs.json` (their canonical ground truth), seed only as backstop. `Bug.raw` passes their `fix_strategy`/`severity`/`file`/`symbol` through to Lane A.
- `.env.example` covers all five sponsors with signup instructions per key.

**Metric:** `runs/` is **empty — no JSONL exists yet.** That is Lane A's tree and my brief emitted no metric, so this is not a miss on my part, but nothing is measuring anything yet as of 11:34. What I can evidence instead, from a real run on Lane C's actual bug data: retrieval separation is same-class **0.78–0.80** vs nearest non-match **0.42**. **Lane A: use threshold 0.60.** Cost per fix on the shared class drops **$0.41 cold → $0.03 warm (13x)**.

**Deviated:**
1. Brief said `FixtureQA` reads `app/BUGS.md`. It now reads **`app/bugs.json`** instead — Lane C wrote both and explicitly names the JSON as machine-readable ground truth. My markdown parser silently returned 3 garbage rows that passed a naive length check; a lenient parser that yields nonsense is worse than falling back, so it's gone and replaced with a structural sanity gate.
2. Fixture memory scoring was rewritten to use the **same `embed()`+cosine as the live Actian path**. They scored differently before, which would have meant Lane A's threshold silently meant two different things in fixture vs live — we'd have found out on stage.
3. Fixture `strong` tier reports `calls: 4` per the brief; the live Pioneer path reports actual calls (1 per `complete()`). **Flagging for Lane A:** call-count is not comparable across modes, cost is. If the demo counts calls, decide which one is truth.

**Blocked/next:**
1. **ZERO live integrations are actually verified, because there are no API keys on this machine — there is no `.env` at all.** This is the single biggest threat to the Tool Use criterion (judges want 3+ working). Nothing I can do in code fixes it. **Needs a human, now:** sign up and paste keys into `.env` for Pioneer (`agent.pioneer.ai` → Billing → Get Pro → event promo code), Guild (`guild.ai`, 50M free tokens), Senso (`docs.senso.ai`, $100 credit), Replay (ask Brian/Discord). The moment a key lands, that adapter goes live with no code change.
2. **Actian is the thesis and it is the least live.** `pip install actian-vectorai` — the package is **not on public PyPI** (docs are ahead of release); needs Community Edition from actian.com. Also **Docker daemon is down** on this machine and the server is `docker run -p 6574:6574 vectoraidb`. Two human actions: start Docker Desktop, download Community Edition. Adapter is written and waiting.
3. **Replay + Senso endpoint paths are unverified guesses.** Their REST references are behind signup; doc time-box blew. All paths/fields are `.env`-overridable and parsers accept multiple spellings, so this is a config fix not a code fix — but someone should grab the real paths from the sponsor Discord channels. Senso *auth* is confirmed (`X-API-Key`, `https://apiv2.senso.ai/api/v1`).
4. **From Lane C:** public URL for the fixture app. Replay cannot reach localhost. Set it as `RATCHET_TARGET_URL`.
5. **Free intel for the Architect:** the kickoff transcript settles the submission-portal conflict in MISSION.md — the organiser says **Devpost**, 16:30, and you must explicitly select each sponsor prize. Worth confirming in Discord but the ambiguity is probably resolved.

**Commits:** 87deb31 2ac5d1d 66b4b8c 3f5680d 54fa6ee

## [11:40] C-001 — URL correction, hosting risk closed
**Landed:** GitHub Pages came up after an explicit rebuild request (`POST /pages/builds`) —
the legacy build had wedged. **The canonical public URL is now:**

  `https://aayushdixit27.github.io/tasker-fixture/`

Verified 200 on `/`, `/app.js`, `/styles.css`; renders correctly; and `/BUGS.md` + `/bugs.json`
both 404, so the answer key is not reachable by anything crawling the app.

**This supersedes the trycloudflare URL in my 11:33 entry — use the Pages one everywhere**
(submission copy, Lane B's Replay adapter target, DEMO.md). The tunnel is still up as a hot
spare but is no longer canonical and should not be quoted anywhere.

**Metric:** `runs/` still empty. Nothing has changed on the join since 11:33.

**Deviated:** none.

**Blocked/next:**
- Hosting decision from my last entry is **closed** — no Architect input needed. Pages is stable
  and survives my machine sleeping, which the tunnel did not.
- AMENDMENT-02 read and understood; **not applied**, per its own gate and Yoshi's instruction —
  it waits until the 12:45 end-to-end join is green. Flagging early so Lane A/B can emit the
  fields while they're already in that code: the post-gate Lane C work needs `arm`
  (`"control"`|`"ratchet"`) for the two-line chart, `saved_usd` + `discovered_by` +
  `born_at_iteration` for the memory panel, and for the split pane at DEMO.md 1:10–2:00 I need
  the **similarity score and pattern id on warm hits** (`similarity`, `pattern_id`, `uses`) —
  DEMO.md quotes "similarity 0.91 · learned at iteration 1 · used 4×" verbatim, and I cannot
  render any of that unless it is in the JSONL. Cheapest possible time to add these is now,
  while the emitter is being written.
