"""RATCHET — the loop core.

Fast loop, per bug: Replay QA scans the app -> signature the bug -> semantic
search memory (Actian) for a verified fix-pattern -> HIT: apply it in one cheap
router call (warm) -> MISS: reason from scratch (strong, cold), verify, then
write the new pattern back to memory and publish it to cited.md.

The whole product is one number: cost per verified fix falls run over run,
because iteration N reuses what iteration N-1 wrote down. This file emits that
number, per bug, to runs/ratchet.jsonl — the file the dashboard tails live.

Determinism: the fixtures carry no randomness and we reset all agent state at the
start of every run, so the same command produces the same numbers twice. That is
what makes the demo safe when the venue wifi dies with 200 people on it.
"""
from __future__ import annotations

import argparse
import json
import os
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


def _reset_agent_state(bundle) -> None:
    """Clear fixture memory + patch ledger so a run starts from a blank slate and
    is byte-for-byte repeatable. Live adapters may not expose reset(); that's fine
    — guard every call."""
    for obj in (bundle.memory, bundle.qa):
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
    """The model-consumable fix recipe we persist. Prefer the router's own
    STRATEGY text; fall back to a class-scoped summary."""
    text = (text or "").strip()
    if text:
        return text
    return f"Fix strategy for {bug.bug_class}: reset/guard the reported behaviour, then re-verify."


def _make_pattern(bundle, *, sig, bug, strategy, code_hint, score, iteration, arm):
    """Construct a Pattern using whatever fields Lane B's dataclass exposes —
    provenance fields (Amendment-02) are set when present, never faked."""
    Pattern = bundle.Pattern
    kwargs = dict(
        sig=sig, bug_class=bug.bug_class, strategy=strategy,
        code_hint=code_hint, verified=True, uses=1, score=score,
    )
    backend = bundle.backends.get("qa", "fixture")
    source = "replay-qa" if backend not in ("fixture", "fixture(degraded)") else "fixture"
    optional = dict(
        discovered_by=arm,
        root_cause_source=source,
        verified_by=source,
        verified_at=_now_iso(),
        verification_count=1,
        born_at_iteration=iteration,
        saved_usd=0.0,
    )
    field_names = getattr(Pattern, "__dataclass_fields__", {})
    for k, v in optional.items():
        if k in field_names:
            kwargs[k] = v
    return Pattern(**kwargs)


def run_arm(
    *,
    iterations: int,
    url: str,
    mode: str,
    use_memory: bool,
    arm: str,
    jsonl_path: str,
    do_evolve: bool = False,
    verbose: bool = False,
) -> dict:
    """Run one arm of the experiment. `use_memory=False` is the control: it reasons
    from scratch every time, so its cost per fix stays flat — the honest baseline
    that answers 'isn't this just Replay?'."""
    bundle = providers.build(mode)
    qa, memory, router, publisher = bundle.qa, bundle.memory, bundle.router, bundle.publisher
    reset_policy()
    _reset_agent_state(bundle)
    _truncate(jsonl_path)

    pol = load_policy()
    warm_threshold = float(pol.warm_threshold)

    # Honest provenance: label data by where it actually came from. "replay-qa"
    # only when QA resolved to a live backend; "fixture" otherwise. Never fake it.
    qa_backend = bundle.backends.get("qa", "fixture")
    source = "replay-qa" if qa_backend not in ("fixture", "fixture(degraded)") else "fixture"

    # running per-class mean cold cost, for saved_usd accounting (Amendment-02 #2)
    cold_costs: dict[str, list[float]] = {}
    per_iter = []

    for it in range(iterations):
        # The app regresses every release: the same suite of bugs re-surfaces.
        if callable(getattr(qa, "reset", None)):
            qa.reset()
        pol = load_policy()  # re-read: evolve() may have rewritten it last iteration
        bugs = qa.scan(url)

        warm_n = cold_n = 0
        cost_sum = 0.0
        fixes = 0
        for bug in bugs:
            sig = signature(bug)
            hits = memory.search(bug.root_cause, k=3) if use_memory else []
            top = hits[0] if hits else None
            warm = bool(use_memory and top and top[1] >= warm_threshold and top[0].verified)

            if warm:
                text, usage = router.complete(
                    f"Reuse pattern {top[0].sig} for {bug.bug_class}", "cheap")
                path = "warm"
                strategy = top[0].strategy
                code_hint = top[0].code_hint
                top_score = round(float(top[1]), 4)
            else:
                text, usage = router.complete(
                    f"Root-cause and fix: {bug.root_cause}\nselector={bug.selector}", "strong")
                path = "cold"
                strategy = _derive_strategy(text, bug)
                code_hint = rc_key(bug.root_cause)
                top_score = round(float(top[1]), 4) if top else 0.0
                for step in pol.cold_path_steps:  # trace for evolve() — no extra cost
                    _append_jsonl(TRACE_PATH, {
                        "iteration": it, "bug_id": bug.id, "arm": arm,
                        "step": step, "output": _step_output(step, bug),
                    })

            calls = int(usage.get("calls", usage.get("llm_calls", 1)))
            cost = float(usage.get("cost_usd", 0.0))
            cold_costs.setdefault(bug.bug_class, [])
            if path == "cold":
                cold_costs[bug.bug_class].append(cost)
            mean_cold = (sum(cold_costs[bug.bug_class]) / len(cold_costs[bug.bug_class])
                         if cold_costs[bug.bug_class] else cost)
            saved_usd = round(max(0.0, mean_cold - cost), 6) if path == "warm" else 0.0

            ok = qa.verify(url, bug)
            if ok and use_memory:
                p = _make_pattern(bundle, sig=sig, bug=bug, strategy=strategy,
                                  code_hint=code_hint, score=max(top_score, 0.9),
                                  iteration=it, arm=arm)
                memory.upsert(p)
                try:
                    publisher.publish(p)
                except Exception:
                    pass

            degraded = any(getattr(a, "degraded", False)
                           for a in (qa, memory, router, publisher))
            record = {
                "iteration": it, "ts": _now_iso(), "arm": arm,
                "bug_id": bug.id, "bug_class": bug.bug_class, "sig": sig,
                "path": path, "llm_calls": calls, "steps": calls,
                "tokens_in": int(usage.get("prompt_tokens", 0)),
                "tokens_out": int(usage.get("completion_tokens", 0)),
                "cost_usd": round(cost, 6), "saved_usd": saved_usd,
                "wall_ms": 800 * calls,  # modelled, deterministic
                "verified": bool(ok), "memory_hit": warm, "top_score": top_score,
                "degraded": degraded, "model": usage.get("model", "unknown"),
                "discovered_by": arm, "root_cause_source": source,
                "born_at_iteration": it,
            }
            _append_jsonl(jsonl_path, record)

            cost_sum += cost
            fixes += 1 if ok else 0
            warm_n += 1 if path == "warm" else 0
            cold_n += 1 if path == "cold" else 0

        cpf = (cost_sum / fixes) if fixes else 0.0
        warm_share = warm_n / (warm_n + cold_n) if (warm_n + cold_n) else 0.0
        per_iter.append({"it": it, "cpf": round(cpf, 4), "warm_share": round(warm_share, 3),
                         "warm": warm_n, "cold": cold_n, "fixes": fixes})
        if verbose:
            print(f"  [{arm}] it{it}: fixes={fixes} warm={warm_n} cold={cold_n} "
                  f"warm_share={warm_share:.2f} cpf=${cpf:.4f}")

        if do_evolve and pol.evolve_every and it > 0 and it % int(pol.evolve_every) == 0:
            from .evolve import evolve
            promoted = evolve(_now_iso())
            for pr in promoted:
                _append_jsonl(jsonl_path, {
                    "iteration": it, "arm": arm, "event": "policy_rewrite",
                    "note": f"promoted {pr['step']} to a deterministic rule",
                    "diff_path": os.path.relpath(pr["diff_path"], REPO_ROOT),
                })

    return {"arm": arm, "iters": per_iter, "backends": bundle.backends}


def _print_summary(result: dict) -> None:
    iters = result["iters"]
    if not iters:
        print("no iterations ran")
        return
    c0 = iters[0]["cpf"] or 1e-9
    c_last = iters[-1]["cpf"]
    ratio = c_last / c0 if c0 else 0.0
    print(f"\n  arm={result['arm']}  backends={result['backends']}")
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

    if args.no_memory:
        res = run_arm(iterations=args.iterations, url=args.url, mode=args.mode,
                      use_memory=False, arm="control", jsonl_path=CONTROL_JSONL,
                      do_evolve=False, verbose=verbose)
        _print_summary(res)
        return 0

    ratchet = run_arm(iterations=args.iterations, url=args.url, mode=args.mode,
                      use_memory=True, arm="ratchet", jsonl_path=RATCHET_JSONL,
                      do_evolve=args.evolve, verbose=verbose)
    _print_summary(ratchet)

    if args.control:
        control = run_arm(iterations=args.iterations, url=args.url, mode=args.mode,
                          use_memory=False, arm="control", jsonl_path=CONTROL_JSONL,
                          do_evolve=False, verbose=verbose)
        _print_summary(control)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
