# GLOBAL — dead ends. Do not retry any of these.
*Maintained by the Architect. Every line cost someone real time today.*

## Sponsors
- **Guild.ai — cut entirely.** Their Unified LLM Proxy (`<runtime-base-url>/runtime/services/llm`) only exists **inside a Guild-hosted agent execution**; unreachable from this machine. Coded agents are TypeScript with a runtime permitting only `@guildai/agents-sdk`, `zod`, `@guildai-services/*`. "Self-managed agents" means self-managed *state*, not self-hosted. Do not install their CLI or spike the proxy.
- **Replay auth is Bearer** (`Authorization: Bearer lqa_...`), base `https://qa.replay.io`, paths under `/api/v1/`. Their **docs contradict their console — trust the console.** Our original `api.replay.io/qa/v1` + `X-API-Key` guess was wrong.
- **Pioneer auth is Bearer too**, despite `docs.pioneer.ai/quickstart` saying `X-API-Key`. Base `https://api.pioneer.ai/v1`. Inference requires a **card on file** even on the Pro plan — a bare 403 with `card_required` is billing, not auth.
- **Actian package is `actian-vectorai-client`**, not `actian-vectorai`. Server is `docker pull actian/vectorai:latest`, EULA env var `ACTIAN_VECTORAI_ACCEPT_EULA=YES`, gRPC on **6574**. `ENGINE_NOT_INITIALIZED` for ~10s after container start is expected — back off, don't degrade.
- **Senso:** base `https://apiv2.senso.ai/api/v1`, header `X-API-Key`. Use the **CLI** (`npm i -g @senso-ai/cli`), not REST. `senso engine draft` while testing, `publish` only for the demo run. Publishing needs a `geo_question_id`.

## Loop / data
- **Never set `RATCHET_QA_MODE=live` in a golden candidate run.** Replay's live-discovered bugs are singletons; QA-live means zero warm hits and a completely flat curve. The live scan is a *separate demo beat*.
- **`ratchet.run` has no `--out` flag.** Writes are hardcoded to `runs/ratchet.jsonl` and `runs/control.jsonl`. `runs/golden/` is a separate directory a run cannot touch.
- **`--control` is required** or the control arm goes stale and the two-line chart loses its rising line.
- **Cost-per-fix is NOT the hero metric.** At real Pioneer prices the numbers are cents and per-iteration variance exceeds the signal (`$0.0193 → 0.0063 → 0.0078 → 0.0136 → 0.0085` — non-monotonic). **Hero is calls per verified fix.**
- **An axis cap in `embed.py` was tried and reverted** — it compressed every margin into a 0.55–0.60 band and made separation worse. Sub-linear growth is enough.
- **Never fabricate `llm_calls`.** One `inference_id` per record exposes it instantly.
- **Never compute a fallback baseline** for a class that never paid a cold price. Render `"no baseline yet"`.

## Process
- **Architect (Cowork) is read-only on git.** It reaches the folder over a mount that cannot delete files, so its writes leave `.lock` files behind. Builders own all git writes. `rm -f .git/index.lock` works from the Mac side.
- **One writer per file tree.** Never reach into another lane's paths; request it in a handoff.
- `runs/golden-fixture/` is the permanent restore point: `cp runs/golden-fixture/*.jsonl runs/golden/`.
