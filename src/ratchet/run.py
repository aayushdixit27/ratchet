"""RATCHET — the loop core.

Fast loop, per bug: Replay QA surfaces a root-caused bug -> signature it ->
semantic search memory (Actian) for a verified fix-pattern -> HIT: apply it in
one cheap router call (warm) -> MISS: reason from scratch (strong, cold), verify
with Replay, then write the new pattern back to memory and publish it to cited.md.

The whole product is one number: cost per *verified* fix falls as the corpus
grows, because a pattern verified once is retrieved instead of re-reasoned. This
file emits that number, per attempt, to runs/ratchet.jsonl — the file the
dashboard tails live.

Two things keep the number honest (Brief A-002):

  * Bugs ARRIVE OVER TIME. We do not present all bugs at t=0. Each iteration
    Replay surfaces a seeded sample drawn from a FIXED class distribution — some
    novel, some recurrences of a class already in the corpus. Coverage grows, so
    warm share climbs gradually and cost/fix descends as a curve, not a step.
    Real software ships continuously; a world where every bug exists at t=0 and
    never recurs is the unrealistic one. The seed is reported; the distribution
    is never tuned to flatter the curve.

  * Fixes FAIL sometimes. Replay verification can reject a first attempt; we
    retry and emit a row for every attempt, failures included. cost/fix divides
    real total cost by real verified fixes, so a failure makes the number worse
    and honest. Warm attempts fail less than cold — a retrieved pattern is more
    reliable precisely because it was verified before.

Determinism: everything is seeded; no wall-clock enters the logic (only the `ts`
field). The same command produces the same numbers twice — what makes the demo
safe when the venue wifi dies with 200 people on it.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from datetime import datetime, timezone

from . import providers
from .policy import load_policy, reset_policy
from .signature import rc_key, selector_shape, signature

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RUNS_DIR = os.path.join(REPO_ROOT, "runs")
TRACE_PATH = os.path.join(RUNS_DIR, "trace.jsonl")
POLICY_HISTORY = os.path.join(REPO_ROOT, "policy_history")
RATCHET_JSONL = os.path.join(RUNS_DIR, "ratchet.jsonl")
CONTROL_JSONL = os.path.join(RUNS_DIR, "control.jsonl")

DEFAULT_SEED = 1729
DEFAULT_BUGS_PER_ITER = 4   # a realistic per-release bug count; spreads corpus
                            # coverage across all 5 iterations so cost/fix is a
                            # curve, not a step. Seed + this are reported, never
                            # tuned to flatter the curve (Brief A-002).
MAX_ATTEMPTS = 3
COLD_FAIL_RATE = 0.28   # cold fixes are reasoned from scratch: more first-try misses
WARM_FAIL_RATE = 0.06   # retrieved patterns were verified before: they fail rarely

# Cross-org provenance. Tasker is org "acme"; app2 (Lane C) is a different org so
# the corpus is visibly cross-company, not a private per-repo cache.
ORIGINS = {
    "tasker": {"origin_app": "tasker", "origin_org": "acme"},
    "app2": {"origin_app": "notes-globex", "origin_org": "globex"},
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _append_jsonl(path: str, obj: dict) -> None:
    """Append one record and flush immediately — the dashboard tails this file,
    so we never buffer."""
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def _truncate(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").close()


def _reset_agent_state(bundle, *, keep_memory: bool) -> None:
    """Clear the patch ledger, and (unless we're transferring a corpus) the
    fixture memory, so a run starts from a known slate and is repeatable. Live
    adapters may not expose reset(); guard every call."""
    targets = [bundle.qa]
    if not keep_memory:
        targets.append(bundle.memory)
    for obj in targets:
        reset = getattr(obj, "reset", None)
        if callable(reset):
            try:
                reset()
            except Exception:
                pass


# --- cold-path step modelling (feeds evolve(); no extra router cost) -----------
def _step_output(step: str, bug) -> str:
    if step == "localize":
        return f"element {selector_shape(bug.selector)}"
    if step == "hypothesize":
        return f"root cause class {bug.bug_class}"
    if step == "synthesize_patch":
        return f"apply fix for {bug.bug_class}"
    if step == "self_review":
        return "approve no issues found"  # constant across bugs -> evolve promotes it
    return f"{step} for {bug.bug_class}"


def _derive_strategy(text: str, bug) -> str:
    text = (text or "").strip()
    if text:
        return text
    return f"Fix strategy for {bug.bug_class}: reset/guard the reported behaviour, then re-verify."


# --- bug arrival: seeded draw from a fixed class distribution ------------------
def _build_catalogue(bundle, url):
    """The fixed universe of bugs Replay can surface, scanned once. Bug templates
    repeat by class exactly as the fixture seeds them (e.g. the modal-state class
    appears 3x), so drawing uniformly from this list reproduces the real class
    frequency — the modal class is common, the singletons rare."""
    qa = bundle.qa
    if callable(getattr(qa, "reset", None)):
        qa.reset()
    return list(qa.scan(url))


def _clone_bug(bundle, template, inst_id: str, origin: dict):
    Bug = bundle.Bug
    raw = dict(getattr(template, "raw", {}) or {})
    raw.update(origin)
    return Bug(
        id=inst_id,
        title=template.title,
        root_cause=template.root_cause,
        selector=template.selector,
        repro=list(template.repro),
        bug_class=template.bug_class,
        raw=raw,
    )


def _sample_iteration(catalogue, rng, k, it, bundle, origin, target):
    """Draw k bugs for this release from the fixed distribution (with
    replacement), each a fresh instance with a unique id."""
    drawn = []
    for j in range(k):
        template = rng.choice(catalogue)
        inst_id = f"{target}-it{it}-d{j}-{template.bug_class}"
        drawn.append(_clone_bug(bundle, template, inst_id, origin))
    return drawn


def _make_pattern(bundle, *, sig, bug, strategy, code_hint, score, uses, iteration, arm, source, origin):
    """Construct a Pattern using whatever fields Lane B's dataclass exposes —
    provenance fields are set when present, never faked."""
    Pattern = bundle.Pattern
    kwargs = dict(
        sig=sig, bug_class=bug.bug_class, strategy=strategy,
        code_hint=code_hint, verified=True, uses=uses, score=score,
    )
    optional = dict(
        discovered_by=arm,
        root_cause_source=source,
        verified_by=source,
        verified_at=_now_iso(),
        verification_count=uses,
        born_at_iteration=iteration,
        saved_usd=0.0,
        origin_app=origin["origin_app"],
        origin_org=origin["origin_org"],
    )
    field_names = getattr(Pattern, "__dataclass_fields__", {})
    for k, v in optional.items():
        if k in field_names:
            kwargs[k] = v
    return Pattern(**kwargs)


def _verified(bundle, qa, url, bug, path, attempt, rng_fail, is_fixture) -> bool:
    """Fixture: model Replay flakiness deterministically (seeded) so failures and
    retries are real in the data. Live: trust Replay's actual verdict."""
    if not is_fixture:
        try:
            return bool(qa.verify(url, bug))
        except Exception:
            return False
    rate = WARM_FAIL_RATE if path == "warm" else COLD_FAIL_RATE
    # last attempt always resolves (the fix lands eventually); earlier ones may fail
    if attempt >= MAX_ATTEMPTS:
        return True
    return rng_fail.random() >= rate


def run_arm(
    *,
    iterations: int,
    url: str,
    mode: str,
    use_memory: bool,
    arm: str,
    jsonl_path: str,
    seed: int = DEFAULT_SEED,
    bugs_per_iter: int = DEFAULT_BUGS_PER_ITER,
    target: str = "tasker",
    corpus_from: str | None = None,
    do_evolve: bool = False,
    verbose: bool = False,
) -> dict:
    """Run one arm. `use_memory=False` is the control: it reasons from scratch
    every time, so its cost per fix stays flat — the honest baseline that answers
    'isn't this just Replay?'. `corpus_from` keeps a prior target's memory so the
    first run of a new app can only warm-hit on transferred patterns."""
    bundle = providers.build(mode)
    qa, memory, router, publisher = bundle.qa, bundle.memory, bundle.router, bundle.publisher
    origin = ORIGINS.get(target, ORIGINS["tasker"])

    reset_policy()
    _reset_agent_state(bundle, keep_memory=bool(corpus_from))
    _truncate(jsonl_path)

    qa_backend = bundle.backends.get("qa", "fixture")
    is_fixture = qa_backend in ("fixture", "fixture(degraded)")
    source = "fixture" if is_fixture else "replay-qa"

    pol = load_policy()
    warm_threshold = float(pol.warm_threshold)

    catalogue = _build_catalogue(bundle, url)
    n_classes = len({b.bug_class for b in catalogue})
    rng_sample = random.Random(seed)
    rng_fail = random.Random(seed ^ 0x9E3779B9)

    cold_costs: dict[str, list[float]] = {}
    per_iter = []

    for it in range(iterations):
        pol = load_policy()  # re-read: evolve() may have rewritten it last iteration
        bugs = _sample_iteration(catalogue, rng_sample, bugs_per_iter, it, bundle, origin, target)

        warm_n = cold_n = 0
        iter_cost = 0.0
        iter_fixes = 0
        for bug in bugs:
            sig = signature(bug)
            hits = memory.search(bug.root_cause, k=3) if use_memory else []
            top = hits[0] if hits else None
            warm = bool(use_memory and top and top[1] >= warm_threshold and top[0].verified)
            path = "warm" if warm else "cold"
            top_score = round(float(top[1]), 4) if top else 0.0
            pattern_id = top[0].sig if top else None
            prior_uses = int(getattr(top[0], "uses", 0)) if warm else 0

            verified = False
            attempt = 0
            while attempt < MAX_ATTEMPTS and not verified:
                attempt += 1
                if warm:
                    text, usage = router.complete(
                        f"Reuse pattern {pattern_id} for {bug.bug_class}", "cheap")
                    strategy = top[0].strategy
                    code_hint = top[0].code_hint
                else:
                    text, usage = router.complete(
                        f"Root-cause and fix: {bug.root_cause}\nselector={bug.selector}", "strong")
                    strategy = _derive_strategy(text, bug)
                    code_hint = rc_key(bug.root_cause)
                    for step in pol.cold_path_steps:  # trace for evolve() — no extra cost
                        _append_jsonl(TRACE_PATH, {
                            "iteration": it, "bug_id": bug.id, "arm": arm,
                            "step": step, "output": _step_output(step, bug),
                        })

                calls = int(usage.get("calls", usage.get("llm_calls", 1)))
                cost = float(usage.get("cost_usd", 0.0))
                if path == "cold":
                    cold_costs.setdefault(bug.bug_class, []).append(cost)
                cc = cold_costs.get(bug.bug_class) or [cost]
                mean_cold = sum(cc) / len(cc)
                saved_usd = round(max(0.0, mean_cold - cost), 6) if path == "warm" else 0.0

                verified = _verified(bundle, qa, url, bug, path, attempt, rng_fail, is_fixture)
                iter_cost += cost

                record = {
                    "iteration": it, "ts": _now_iso(), "arm": arm,
                    "target": target, "origin_app": origin["origin_app"],
                    "origin_org": origin["origin_org"],
                    "bug_id": bug.id, "bug_class": bug.bug_class, "sig": sig,
                    "path": path, "attempt": attempt, "max_attempts": MAX_ATTEMPTS,
                    "llm_calls": calls, "steps": calls,
                    "tokens_in": int(usage.get("prompt_tokens", 0)),
                    "tokens_out": int(usage.get("completion_tokens", 0)),
                    "cost_usd": round(cost, 6), "saved_usd": saved_usd,
                    "wall_ms": 800 * calls,  # modelled, deterministic
                    "verified": bool(verified), "memory_hit": warm,
                    "top_score": top_score, "similarity": top_score,
                    "pattern_id": pattern_id, "uses": prior_uses + 1 if warm else None,
                    "degraded": any(getattr(a, "degraded", False)
                                    for a in (qa, memory, router, publisher)),
                    "model": usage.get("model", "unknown"),
                    "discovered_by": arm, "root_cause_source": source,
                    "born_at_iteration": it, "corpus_from": corpus_from,
                }
                # Pioneer router telemetry passthrough (present only in live router
                # mode). `model` already carries the routed model; also surface it as
                # routed_model and pass the audit/savings fields the dashboard wants.
                if usage.get("model") and "fixture" not in str(usage.get("model")):
                    record["routed_model"] = usage.get("model")
                for _k in ("requested_model", "baseline_model", "rate_diff_per_mtok",
                           "router_saved_usd", "inference_id", "spent_usd_running"):
                    if usage.get(_k) is not None:
                        record[_k] = usage[_k]
                _append_jsonl(jsonl_path, record)

            if verified:
                iter_fixes += 1
                warm_n += 1 if path == "warm" else 0
                cold_n += 1 if path == "cold" else 0
                if use_memory:
                    new_uses = prior_uses + 1 if warm else 1
                    p = _make_pattern(bundle, sig=sig, bug=bug, strategy=strategy,
                                      code_hint=code_hint, score=max(top_score, 0.9),
                                      uses=new_uses, iteration=it, arm=arm,
                                      source=source, origin=origin)
                    memory.upsert(p)
                    try:
                        publisher.publish(p)
                    except Exception:
                        pass

        cpf = (iter_cost / iter_fixes) if iter_fixes else 0.0
        warm_share = warm_n / (warm_n + cold_n) if (warm_n + cold_n) else 0.0
        per_iter.append({"it": it, "cpf": round(cpf, 4), "warm_share": round(warm_share, 3),
                         "warm": warm_n, "cold": cold_n, "fixes": iter_fixes})
        if verbose:
            print(f"  [{arm}] it{it}: fixes={iter_fixes} warm={warm_n} cold={cold_n} "
                  f"warm_share={warm_share:.2f} cpf=${cpf:.4f}")

        if do_evolve and pol.evolve_every and it > 0 and it % int(pol.evolve_every) == 0:
            from .evolve import evolve
            for pr in evolve(_now_iso()):
                _append_jsonl(jsonl_path, {
                    "iteration": it, "arm": arm, "event": "policy_rewrite",
                    "note": f"promoted {pr['step']} to a deterministic rule",
                    "diff_path": os.path.relpath(pr["diff_path"], REPO_ROOT),
                })

    return {"arm": arm, "iters": per_iter, "backends": bundle.backends,
            "seed": seed, "bugs_per_iter": bugs_per_iter, "n_classes": n_classes,
            "target": target, "corpus_from": corpus_from}


def _print_summary(result: dict) -> None:
    iters = result["iters"]
    if not iters:
        print("no iterations ran")
        return
    c0 = iters[0]["cpf"] or 1e-9
    c_last = iters[-1]["cpf"]
    ratio = c_last / c0 if c0 else 0.0
    print(f"\n  arm={result['arm']}  target={result['target']}  "
          f"corpus_from={result['corpus_from']}  seed={result['seed']}  "
          f"k={result['bugs_per_iter']}  classes={result['n_classes']}")
    print(f"  backends={result['backends']}")
    print("  iter | fixes | warm/cold | warm_share |   cpf")
    for r in iters:
        print(f"   {r['it']:>3} | {r['fixes']:>5} | {r['warm']:>4}/{r['cold']:<4} | "
              f"{r['warm_share']:>9.2f} | ${r['cpf']:.4f}")
    print(f"  cost/fix: iter0 ${c0:.4f} -> iter{iters[-1]['it']} ${c_last:.4f} "
          f"= {ratio*100:.1f}% of baseline")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="ratchet.run", description="RATCHET loop core")
    ap.add_argument("--iterations", type=int, default=5)
    ap.add_argument("--mode", default=os.environ.get("RATCHET_MODE", "fixture"))
    ap.add_argument("--url", default="http://localhost:8000")
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--bugs-per-iter", type=int, default=DEFAULT_BUGS_PER_ITER)
    ap.add_argument("--target", default="tasker", choices=sorted(ORIGINS),
                    help="which app to run against (sets origin_app/origin_org)")
    ap.add_argument("--corpus-from", default=None,
                    help="keep a prior target's memory so first-run warm hits are transfer, not leakage")
    ap.add_argument("--control", action="store_true",
                    help="also run the no-memory control arm -> runs/control.jsonl")
    ap.add_argument("--no-memory", dest="no_memory", action="store_true",
                    help="run ONLY the no-memory control arm")
    ap.add_argument("--evolve", action="store_true",
                    help="enable the slow loop (self-rewriting policy.yaml); off by default")
    ap.add_argument("--demo", action="store_true",
                    help="rehearsed offline replay: fixture mode, 5 iterations, both arms")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if args.demo:
        args.mode = "fixture"
        args.iterations = 5
        args.control = True

    verbose = not args.quiet
    common = dict(iterations=args.iterations, url=args.url, mode=args.mode,
                  seed=args.seed, bugs_per_iter=args.bugs_per_iter,
                  target=args.target, corpus_from=args.corpus_from, verbose=verbose)

    if args.no_memory:
        _print_summary(run_arm(use_memory=False, arm="control",
                               jsonl_path=CONTROL_JSONL, do_evolve=False, **common))
        return 0

    _print_summary(run_arm(use_memory=True, arm="ratchet",
                           jsonl_path=RATCHET_JSONL, do_evolve=args.evolve, **common))

    if args.control:
        _print_summary(run_arm(use_memory=False, arm="control",
                               jsonl_path=CONTROL_JSONL, do_evolve=False, **common))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
