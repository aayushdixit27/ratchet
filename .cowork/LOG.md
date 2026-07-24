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

## [11:49] A-001 + A-002 + AMD-01/02/03 — partial (loop core DONE & joined; cross-org run blocked on B/C)
**Landed:**
- **Loop core green on Lane B's real adapters, zero network, deterministic.** `python -m ratchet.run --iterations 5 --mode fixture` runs end-to-end. Fast loop: scan → signature → memory.search → warm(cheap)/cold(strong) → verify → upsert → publish. Imports only from `src.adapters` (get_qa/get_memory/…); my local fixtures deleted — Lane B's are canonical.
- **The 12:45 ugly-end-to-end gate was met at ~11:35, an hour early.** JSONL flows to `runs/ratchet.jsonl`; verified the dashboard fetches it (HTTP 200 at `../runs/ratchet.jsonl`) and its own aggregation reproduces the hero line. **Join proven over HTTP.**
- **Two-arm proof (AMD-02):** `--control`/`--no-memory` runs the no-memory baseline to `runs/control.jsonl` (every record tagged `arm`). Control never improves; Ratchet bends. This is the "isn't this just Replay?" answer.
- **Curve, not step (A-002 #1):** bugs now ARRIVE OVER TIME — each iteration draws k=4 bugs (seed 1729) from the fixed class distribution, so corpus coverage grows and cost/fix descends across all 5 points. Seed + k reported in the summary; distribution not tuned.
- **Honest failures (A-002 #2):** fixes can fail Replay verification and retry (max 3), one row per attempt; cost/fix = real cost / real verified fixes. Warm fails rarer (6%) than cold (28%). Nothing is 8/8 perfect anymore.
- **Every field Lane C asked for (11:40 entry) is now in the JSONL:** `arm`, `saved_usd`, `discovered_by`, `born_at_iteration`, and on warm hits `similarity`, `pattern_id`, `uses`. Plus `origin_app`/`origin_org` (tasker=acme) per AMD-03, `attempt`/`max_attempts`, `degraded`, `root_cause_source`.
- **`--demo`:** fixture, 5 iters, both arms, offline, <1s. Rehearsed replay for dead-wifi.
- **evolve() (slow loop) built + verified** — it genuinely rewrites `policy.yaml` (promotes `self_review` → deterministic rule) and writes a clean unified diff to `policy_history/`. **Gated behind `--evolve`, parked** per AMD-01 (curve is wow #1). policy.yaml resets to baseline each run so the diff re-derives live.
- **Cross-org transfer plumbing:** `--target app2 --corpus-from tasker` keeps Tasker's memory and never pre-seeds app2's own corpus. Verified app2's *first* run warm-hits at $0.03 from transferred patterns (mechanism proven).

**Metric:** `runs/ratchet.jsonl` (real, this round):
`ratchet: it0 $0.426 → it1 $0.239 → it2 $0.234 → it3 $0.030 → it4 $0.029` (= 6.9% of baseline, curve).
`control: it0 $0.522 → … → it4 $0.864` (flat-to-worse, never learns). $11+ saved across warm hits. Deterministic across two runs (byte-identical modulo timestamps).

**Deviated:**
- **`warm_threshold` 0.82 → 0.55.** Probed same-class similarity on the real bug data: 0.62–0.90 same-class, cross-class far below; 0.55 reuses a pattern only for its own class, zero cross-class hits observed. (Lane B suggested 0.60 in their 11:34 entry — within noise; either is safe. Say the word and I'll match 0.60 exactly.)
- **Router usage keys:** my brief's schema said `llm_calls`/`tokens_in`; Lane B's actual `usage()` returns `calls`/`prompt_tokens`. I mapped to Lane B's real shape and emit BOTH names. Per Lane B's 11:34 flag, cost is comparable across modes, call-count is not — the demo should quote **cost**, not calls.
- **k=4, seed=1729** chosen for a realistic release size that spreads coverage over all 5 iters. Not seed-shopped; reported in every run summary.
- Committed other lanes'/Architect's in-flight docs (STATE, DEMO, POSITIONING, briefs A-002/AMD-03, cited.md) because builders own 100% of git writes and they were dangling — content untouched.

**Blocked/next (Architect + lanes):**
1. **Lane C — dashboard must be SERVED OVER HTTP**, not opened as `file://` (browser blocks `fetch()`). `python3 -m http.server` from repo root; dashboard at `/dashboard/`, data at `/runs/`. Flagging because it's a silent demo-killer.
2. **Lane C — two-line chart + split pane can be built now:** `runs/control.jsonl` exists with `arm`; warm rows carry `similarity`/`pattern_id`/`uses`; memory panel has `saved_usd`/`born_at_iteration`/`origin_org`. Everything DEMO.md quotes verbatim is in the data.
3. **Lane C — `app2/bugs.json` needed for AMD-03's closing beat** (notes app, 2 shared modal-class + 4 novel). Until it lands, `--target app2` reuses Tasker's catalogue — transfer mechanism works but symptoms aren't distinct yet.
4. **Lane B — two asks:** (a) extend `Pattern` with provenance fields (`discovered_by`, `root_cause_source`, `verified_by`, `verified_at`, `verification_count`, `born_at_iteration`, `saved_usd`, `origin_app`, `origin_org`); my code sets them the moment they exist, currently skipped (honest). (b) Serve `app2/bugs.json` as a selectable QA source so `--target app2` gets distinct symptoms.
5. **Lane A next (me):** route app2 output to its own `runs/app2.jsonl` so the closing beat has separate data; wire the real transfer demo once B/C land; unpark `evolve()` as wow #2 on your call (it's proven, curve is proven twice).
6. **Architect decision:** live sponsor integrations are still fixture-only (no `.env`/keys per Lane B 11:34). Tool-Use criterion wants 3+ live — that's a human/keys blocker, not code.

**Commits:** 7e66ae9 6d19079 4a3cfb5 9ea27f3 bd36a6d

## [12:01] B-002 + AMD-02/03 (Lane B parts) — done
**Landed:**
- **Replay rewritten against the real spec** (qa.replay.io, Bearer `lqa_`, project-scoped async flow, field mapping per B-002 — `root_cause <- analysis`, padded with expected/actual when thin, selector never invented). Polling budgeted ~3min then degrades; the loop can never block on Replay.
- **⭐ `QA.mark_fixed(bug, ok)` on the protocol** — writes our verdict back INTO Replay (PATCH fixed/reopened). `verify()` reads Replay's own status; `reopened` → False so Lane A can demote pattern confidence. Fixture mode: local ledger, un-record supported. Reverse-proxy fallback wired (`REPLAY_USE_REVERSE_PROXY=true`).
- **Pioneer per real docs:** auth fixed to `X-API-Key`; invented model defaults deleted — cheap/strong must come from a real `/v1/models` listing (curl one-liner in `.env.example`). **If cheap == strong the adapter refuses to go live** — that misconfig fabricates the warm/cold gap, the one lying-chart risk. `PIONEER_ADAPTIVE` flagged as an unverified guess: verify at agent.pioneer.ai/routers or ask Kelton before claiming adaptive routing on stage.
- **`Pattern` extended** with all AMD-02/03 provenance fields (discovered_by, root_cause_source, verified_by, verified_at, verification_count, born_at_iteration, saved_usd, origin_app, origin_org) — all defaulted + appended, so Lane A's existing construction and persisted `.ratchet` state load unchanged (tested both). ReplayQA stamps `raw.provenance="replay-qa"` so Lane A copies, never guesses.
- **`get_qa('app2')` / `RATCHET_TARGET_APP=app2`** selects `app2/bugs.json` with a per-app patch ledger (no bleed between apps). Falls back to seed until Lane C lands the file.
- **`cited.md` now human-legible** (AMD-02): provenance + economics as prose ("has saved $1.17 in avoided reasoning"), JSON folded into `<details>`. Actian round-trips the full dataclass so provenance survives the live DB.

**Metric:** `runs/ratchet.jsonl` fresh at 11:48 (Lane A's round): it0 $0.418 cold → it4 $0.030 warm, sim 0.62 on last row. My changes are upstream of the numbers; nothing in this round regenerated runs/.

**Deviated:**
- B-002 says `Bug.bug_class <- ours, derived`. Live Replay bugs currently get `bug_class = polish_category or "unclassified"` (prior kept in raw as specified). True derivation belongs to Lane A's signature module, which already keys on root_cause — flag if you want the field left strictly "unclassified" for live bugs.
- Restored `cited.md` after my test transiently deleted Lane A's committed copy (caught in handoff review, `git checkout` restored — zero content lost).

**Blocked/next:**
1. **Keys, still.** Everything above is written and tested in degraded mode; ZERO live calls have been made. Replay needs an `lqa_` token, Pioneer needs a key + two real model IDs from `/v1/models`, Senso needs a key, Guild needs a key, Actian needs Docker Desktop started + Community Edition download. Every one is a human errand; every one is a no-code-change flip.
2. **From Lane C:** `app2/bugs.json` (AMD-03) — my selector is wired and waiting; currently falls back to seed so `--target app2` has non-distinct symptoms. Also still need the public URL for `RATCHET_TARGET_URL`.
3. **For Lane A:** `reopened` → pattern-confidence demotion is plumbed on my side (verify returns False, status in raw); wiring the demotion into memory scoring is yours if there's time.
4. `.obsidian/` appeared untracked (someone's editor) — left alone, suggest a gitignore line from whoever owns the root .gitignore.

**Commits:** 66d4d2c 8fdff42 7c7445d 5b0e0d1

## [12:28] B-006 — partial (2 sponsors GENUINELY LIVE, 1 billing-blocked, 1 waiting on human)
**Landed:**
- **Step 0 done first:** golden fixture run archived to `runs/golden/` (5d010ba) before any live call. `--demo` insurance is committed and will not be overwritten.
- **REPLAY: GENUINELY LIVE, evidence on disk.** Project `proj-ratchet-mrzbmsos` explored Lane C's deployed app and found **2 real bugs we never seeded** — a toast z-index occlusion and a WCAG `aria-selected` violation — both approved by Replay's own judge. Raw JSON cached at `src/adapters/seeds/replay_bugs_live.json`. `mark_fixed` write-back **verified round-trip live** (PATCH→fixed, GET confirms, reverted to open so the on-stage flip is still available). `REPLAY_PROJECT_ID` pinned in `.env` — the demo never re-explores. Live-shape parse fixes landed: `analysis` arrives as a `{'chain':[{text}]}` dict, `reproduction_steps` can be null, project id is `id` not `exploration_id` — none of that was in the spec summary; all learned from real responses.
- **SENSO: GENUINELY LIVE, in the loop.** CLI path (v0.11.1), org "ScoutAI", draft mode. Created geo-question prompts programmatically — **one per bug class** after observing live that a shared question id makes every pattern overwrite one document. Two distinct content_ids on file. Full loop ran with `publisher: senso-live(draft)`: **curve identical, $0.4258 → $0.0293** — B-006's regression gate passes.
- **PIONEER: blocked at billing, code fully verified.** Key authenticates; `/v1/models` returns the real catalogue; real IDs configured (`LiquidAI/LFM2-24B-A2B` cheap at $0.03/M, `claude-sonnet-5` strong); same-model guard armed. Inference returns **403 `card_required`** — the event promo was never applied. **agent.pioneer.ai/billing → "Get Pro" → promo code, 2 minutes, then `RATCHET_ROUTER_MODE=live` just works.** Mid-run degradation fired exactly as designed when the 403 hit.
- Guild: cancelled per B-005, untouched.

**Metric:** `runs/ratchet.jsonl` regenerated this round with live publisher: it0 $0.4258 → it4 $0.0293 (6.9% of baseline), warm_share 0.25→1.00. Golden copy preserved separately.

**Deviated:**
- B-006 step 0 said `git add -A`; I staged `runs/golden` targeted — the tree had other lanes' and editor junk that must not ride along.
- Senso geo-question: brief said "get one from the dashboard"; I created them via `senso prompts create` instead (faster, and scriptable per class). `SENSO_GEO_QUESTION_ID` in `.env` is now only the fallback.

**Blocked/next:**
1. **⚠️ ARCHITECT DECISION — QA live would flatten the curve today.** Replay has found 2 live bugs so far; they are singletons (glitches, accessibility) with no shared class, so a live-QA loop run has no warm path and the chart goes flat. Exploration is still running (17 test runs in flight) and may yet surface the seeded modal-state family. Options: (a) demo = live Replay scan beat + fixture curve, stated plainly; (b) wait for exploration to find the modal family, re-check at 13:30; (c) hybrid — live bugs merged with fixture catalogue. I recommend (a) with (b) as upside. **Do not flip `RATCHET_QA_MODE=live` for the demo run without choosing.**
2. **Pioneer promo code** — the 2-minute human errand above unlocks real cost numbers.
3. **Actian** — still with Yoshi (Docker daemon down, SDK not on PyPI). Adapter ready.
4. mark_fixed flip on stage: use `bug-mrzbq4us-w9k6` (toast) — currently `open`, one PATCH away.

**Commits:** 5d010ba 095df42 9c41f77 e56ab88

## [12:38] B-007 ⭐ test + B-008 — done, with one diagnosis overturned
**Landed:**
- **B-008's premise is falsified by direct test.** `Authorization: Bearer` returns the IDENTICAL `403 card_required` as `X-API-Key` — ran the exact console cURL verbatim. Identification is fine either way (`/v1/models` is 200 with both); the missing thing is *entitlement on this key's account*. Console showing Pro + $40 with the API saying card_required means **the key in `.env` was almost certainly minted under a different workspace than the one that was upgraded. Fix: mint a fresh key from the workspace whose billing page shows Pro, paste into `.env`. Two minutes, zero code.** Adapter is now header-agnostic anyway (Bearer first, X-API-Key retry on 401/403) so the docs/console contradiction can never bite again. `cheap=pioneer/auto` (their router, per B-008), `strong=claude-sonnet-5` pinned, same-model guard armed on resolved model.
- **B-007 ⭐ test run, result honest: no warm hit yet.** All 3 live Replay bugs score below threshold against the seeded corpus (0.50, 0.29, 0.41). The near-miss (0.504) is a modal *visibility* bug, not the state-reset family. Notably the embedding correctly refused to conflate Replay's toast **z-index occlusion** with our seeded toast **listener-binding** pattern — same DOM element, different root cause. A false warm hit on stage would have been worse than none.
- **Live bug count: 2 → 3** (exploration completed; 9 deeper test runs still in flight). Cache refreshed on disk. The seeded modal-state family needs multi-step journeys (open→edit→cancel→reopen), which is exactly what's still running — **the fully-live money shot is still in play, re-check bugs count at ~13:00.**

**Metric:** no loop run this round; curve state unchanged (golden intact, last verified $0.4258→$0.0293 with Senso live).

**Deviated:** B-008 said "change the header and the 403 clears" — implemented the header change AND kept the correction visible rather than silently claiming success. Do not tell the room Pioneer is live until a fresh key actually completes a call.

**Blocked/next:**
1. **Pioneer: fresh API key from the Pro workspace** (agent.pioneer.ai → the workspace whose billing shows Pro/$40 → API Keys → create). The moment it lands: `RATCHET_ROUTER_MODE=live` smoke test, then full curve re-run with real prices (B-008's report-both rule).
2. **Replay: poll `bugs` count at 13:00.** If the modal-state family lands, re-run the B-007 similarity test — a live warm hit collapses both demo beats into one.
3. Architect: B-007's seeded-corpus framing is adopted on my side; nothing in the adapters labels fixture data as live.

**Commits:** e87921a 709077e

## [12:48] B-009 — done. ACTIAN IS LIVE. Three sponsors genuinely live.
**Landed:**
- **Actian VectorAI DB running and primary.** `actian-vectorai-client` + `actian/vectorai:latest` container (gRPC 6574, data in gitignored `local_data/`). Beyond the guide: sync client needs explicit `connect()` (the `with` form hid it), no `PayloadSchema` in this SDK build → schema via `extra_params_json` with plain fallback, protobuf runtime bump, ENGINE_NOT_INITIALIZED backoff per gotcha #1, and one live-discovered fix: **HNSW `limit=1` returns empty for low-similarity queries that `limit=10` finds** — adapter over-fetches to 10 and truncates.
- **Score parity with the fixture to four decimals** on every test query — same `embed()` vectors, same cosine, so the 0.55 warm threshold provably means the same thing in fixture and live mode. Provenance fields survive the DB round-trip. Seeded modal root cause warm-hits at **0.842 through the real gRPC search**.
- **Full curve run with `memory=actian-live` + `publisher=senso-live`: $0.4258 → $0.0293, shape unchanged.** `RATCHET_MEMORY_MODE=live` is on in `.env`. Golden untouched.
- **Anti-disqualifier on record:** Memory protocol exists since 87deb31 (11:21), fixture documented as wifi-fallback from the start — the "swapped in a vector DB at the last hour" rule does not apply to us and git proves it.
- Replay live count now **4 open + 1 judge-rejected** (their own judge filters!). 🆕 bug is seeded BUG-04 (counter) discovered live at **0.4912 — 0.06 under the warm threshold.** Modal-state family not yet surfaced; 3 test runs still in flight.

**Metric:** curve verified this round with two live backends in the loop: it0 $0.4258 → it4 $0.0293 (6.9%), warm 0.25→1.00.

**Deviated:** nothing material. Filterable-payload schema is best-effort (unknown server support in this build) — loop filters client-side anyway.

**Blocked/next:**
1. **Live count: Replay ✅ Senso ✅ Actian ✅ = 3, Tool Use criterion cleared with evidence.** Pioneer would make 4 — still needs a fresh key from the Pro workspace (12:38 entry).
2. **0.4912 near-miss decision for the Architect:** Replay's live re-discovery of the seeded counter bug scores 0.06 under threshold. Options: leave it (honest cold, still a good beat), or Lane A lowers threshold to 0.45 (re-probe cross-class margin first — nearest non-mate was 0.42 on seeded data, that's tight). My take: DON'T touch the threshold for one bug; a false warm hit on stage is fatal, a cold near-miss is a good story about honesty.
3. **Demo op note:** Docker Desktop + vectorai container must be running before the demo; add `docker start vectorai` to the demo runbook cold-start (Lane C/Architect).
4. Replay deeper journeys: 3 still running — last poll before 13:30 worth doing.

**Commits:** 636c32c be1963d

## [13:00] C-003 item 1 — done (split pane + memory panel + two-arm chart, all from golden JSONL)
**Landed:** `dashboard/index.html` rewritten for the AMENDMENT-02 surface, commit 581a7ea.
Verified by headless-Chrome screenshot against `runs/golden/` at each step.
- **Two-arm hero chart.** One shared y-scale so control's climb is never cropped: control
  ends at **$0.864** (labeled), ratchet **$0.426 → $0.029**. Arms labeled exactly as briefed:
  "Replay + coding agent (today) — memory off" / "Ratchet — memory on".
- **Split pane.** Left: cold first encounter (`tasker-it0-d0`, 4 stacked LLM-call rows,
  $0.418, 6,890 tokens, 3.2s). Right: `MEMORY HIT · pattern b7a3887a7811 · similarity
  0.8565 · used 2×`, $0.030, 1 call. Footer derives "**14× cheaper**". These are the exact
  values the corrected DEMO.md quotes — and they are *selected*, not typed: rule is
  "bug class with most warm reuse → earliest cross-bug hit → paired with the cold row that
  actually learned the pattern (sig == pattern_id, path == cold, different bug_id)".
- **Memory panel.** Patterns sorted by cumulative `saved_usd` desc (top: missing-preventdefault
  $1.21, 4×), each with uses, born-iteration, `discovered_by` badge. Badge styling keys on
  "replay" substring so it lights up blue automatically if Lane A re-runs with live Replay.
- Tiles now: total saved by memory **$5.07** across 15 hits / LLM calls per verified fix
  **3.3 → 1.0** / patterns **6**, reused 22×.
- **Zero-network path:** `?golden=1` reads `runs/golden/*.jsonl`; default tails `runs/`.
  Nothing on screen is hardcoded — every number derives from the JSONL at render time,
  including the 14× factor and the caption ("same root cause (modal-state-not-reset),
  different bug" comes from the row's own class field).

**Metric:** golden run renders: ratchet $0.4258→$0.0293/fix, control $0.5219→$0.8643,
warm share 20%→100% by iter 3. Independently recomputed in Python before rendering — chart
and recomputation agree.

**Deviated:**
- Split-pane row selection needed judgment the brief didn't specify: highest-similarity warm
  hit was iter1-d0 (0.9024) but that's the *same bug recurring* and its pattern was born from
  a warm fix — "1× cheaper", story dead. The rule above picks the genuine generalisation.
  Flagging because if Lane A regenerates golden data, the pane re-derives from the new file —
  presenter should re-check the quoted numbers in DEMO.md after any regen.
- Cold pane shows call-count blocks + aggregate tokens/time from the JSONL, not a scrolling
  reasoning transcript — per-call text isn't in the data and I won't invent it (C-002: "don't
  invent them"). If we want the transcript beat, Lane A would need to emit transcript lines.

**Blocked/next:**
- Starting C-003 item 2 / AMENDMENT-03 now: `app2/` notes app (org "globex"), 6 bugs, 2 sharing
  `modal-state-not-reset` with genuinely different symptoms, novel singletons, `app2/bugs.json`
  in Lane B's schema, second GitHub Pages URL. Cut line if time runs short, per brief.
- Nothing needed from other lanes for item 2. For the demo: whoever presents should load
  `dashboard/index.html?golden=1` served locally (e.g. `python3 -m http.server` from repo
  root) — file:// won't fetch; a local server is required. RUNBOOK.md should say this.

**Commits:** 581a7ea
