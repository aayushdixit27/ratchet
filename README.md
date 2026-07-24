# Ratchet

**The QA agent that gets cheaper every time you ship.**

Replay QA finds real bugs in a live app. Ratchet fixes them, and a fix enters memory only once a re-test confirms it worked. The next time that same cause appears, anywhere, it costs one AI call instead of four.

Built in one day at the Self-Evolving Agents Hackathon, DG717 San Francisco, 24 July 2026.

---

## The problem, in someone else's words

We pointed Replay QA at a web app. It filed two bugs hours apart:

> "Remaining-tasks counter displays **one fewer** than actual undone count due to **stale -1 adjustment**."

> "Task counter shows incorrect tasks-remaining count due to **stale -1 adjustment** in render function."

Same cause, filed twice. Replay's own summary asks a human to *"consolidate before fixing."*

That is the problem. Coding agents forget between runs, so somebody pays to solve the same thing twice, forever.

## What it does

1. **Replay QA** crawls the deployed app and returns bugs with root causes. We write none of them.
2. **Ratchet** checks whether it has seen that cause before, by meaning rather than keyword, so one fix matches a bug in a different file with a symptom that looks unrelated.
3. It fixes the bug, **Replay re-tests**, and only a fix that passes enters memory.

We do not remember what a model claimed. We remember what got verified.

| | AI calls | Cost |
|---|---|---|
| First encounter | 4 | $1.65 |
| Next time that cause appears | 1 | $0.03 |

## The proof

Same agent, twice, on identical bugs with identical models. The only difference was memory.

```
                round 1   2     3     4     5
memory on        4.25    3.5   2.75  1.0   1.0     AI calls per verified fix
memory off       5.0     5.0   6.0   5.0   8.0
```

**Not improving is not the failure mode. Getting worse is.** The control arm climbs because it keeps re-failing on causes it has already seen. That matches published work where security flaws rose 37.6% over five rounds of unremembered self-improvement.

## What is actually new

Persisting verified fixes is not novel. [EvoRepair](https://arxiv.org/abs/2605.30105) reports 41.6% lower cost; Meta's Experience Graphs reports 52% lower token cost per valid solution. **Every published version is single-organization.**

So we pointed Ratchet at a second app, from a different team, that it had never seen. On its first run, **two of the first four bugs were fixed straight from memory**, because fixes verified on the first app transferred.

Everyone built the private version. The economics only get interesting when my verified fix makes your first day cheap.

## Sponsors, one job each

| | Role |
|---|---|
| **Replay QA** | Finds the bugs and re-tests the fixes. 17 journeys, 1 exploration, 6 bugs, none planted by us. Its root-cause text is the string we embed. |
| **Actian VectorAI DB** | The memory. Runs in Docker as primary storage, holds every verified fix as a vector so bugs match by cause rather than keyword. |
| **Pioneer** | Routes every call. `pioneer/auto` handles recall; a frontier model is pinned for reasoning. Their response reports what routing saved, which stacks with our deleted calls. |
| **Senso Context OS** | Publishes each verified fix to a public citable page, so the memory can cross company lines instead of staying a private cache. |
| **Guild.ai** | Investigated and **cut**. Their LLM proxy only exists inside a Guild-hosted runtime and coded agents are TypeScript-only, so integrating properly meant hosting our loop on their platform. We would rather name the tradeoff than ship a token integration. |

## Run it

```bash
pip install actian-vectorai-client
docker run -d --name vectorai -p 6573-6575:6573-6575 \
  -e ACTIAN_VECTORAI_ACCEPT_EULA=YES actian/vectorai:latest

cp .env.example .env          # optional: every adapter falls back offline
PYTHONPATH=src python3 -m ratchet.run --demo
```

`--demo` runs both arms with **zero network** in under a second. Every sponsor adapter degrades to a deterministic fixture if its key is missing or the service is unreachable, and marks the record `degraded: true`. Nothing can crash the loop.

Open `dashboard/index.html` for the charts, `deck.html` for the five-screen demo, `explain.html` for the one-page write-up.

## Layout

```
src/ratchet/      the loop, the policy, the metrics
src/adapters/     one adapter per sponsor, each with an offline fixture
app/  app2/       two deliberately buggy web apps (the second is "another company")
runs/             JSONL, one row per attempt, including failures
cited.md          the published corpus of verified fixes
```

## Limits we would rather state than have you find

- The five-round curve uses a **seeded bug sequence** so ten weeks fit in ninety seconds. Bug discovery is live.
- Five rounds is a **small sample**. The raw JSONL is in `runs/`.
- One pattern reports **no baseline yet** because it never paid full price. We only count savings we can prove.
- We built a write-back into Replay's bug status but **did not confirm it landed**, so we do not claim it.
- `runs/golden/` records honestly label their own provenance. Where a record says `fixture`, it means fixture.

## Next

Point it at a real repo and let it open the pull request. Every fix anyone verifies makes everyone else's agent cheaper.
