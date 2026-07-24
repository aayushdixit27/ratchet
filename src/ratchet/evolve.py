"""The slow loop. Every EVOLVE_EVERY iterations the agent reads its OWN traces,
finds an LLM step whose output has been effectively identical across >=3
occurrences, and rewrites its own policy.yaml to replace that step with a
deterministic rule — committing the before/after diff to policy_history/.

This is Guild's 87%-cost-cut story run autonomously. The self-authored diff is
the artifact we `cat` on stage.
"""
from __future__ import annotations

import difflib
import json
import os

from . import policy as policy_mod

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TRACE_PATH = os.path.join(REPO_ROOT, "runs", "trace.jsonl")
HISTORY_DIR = os.path.join(REPO_ROOT, "policy_history")
MIN_OCCURRENCES = 3


def _norm(s: str) -> str:
    return " ".join((s or "").lower().split())


def _read_trace(trace_path: str) -> list[dict]:
    if not os.path.exists(trace_path):
        return []
    out = []
    with open(trace_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def find_promotable(trace: list[dict], cold_steps: list[str]) -> list[str]:
    """A step is promotable if it is still on the cold path, has >=3 recorded
    occurrences, and EVERY occurrence produced the same normalised output."""
    by_step: dict[str, set[str]] = {}
    counts: dict[str, int] = {}
    for rec in trace:
        step = rec.get("step")
        if step is None:
            continue
        by_step.setdefault(step, set()).add(_norm(rec.get("output", "")))
        counts[step] = counts.get(step, 0) + 1
    promotable = []
    for step in cold_steps:  # deterministic order
        if counts.get(step, 0) >= MIN_OCCURRENCES and len(by_step.get(step, set())) == 1:
            promotable.append(step)
    return promotable


def evolve(iso: str, trace_path: str = TRACE_PATH, history_dir: str = HISTORY_DIR) -> list[dict]:
    """Run one slow-loop pass. Returns a list of {step, diff_path, diff} for each
    step promoted this pass (possibly empty)."""
    os.makedirs(history_dir, exist_ok=True)
    pol = policy_mod.load_policy()
    trace = _read_trace(trace_path)
    promoted = []
    for step in find_promotable(trace, pol.cold_path_steps):
        with open(policy_mod.POLICY_PATH, "r", encoding="utf-8") as fh:
            before = fh.read()
        after = policy_mod.promote_step(step)  # writes policy.yaml in place
        if after == before:
            continue
        diff = "".join(
            difflib.unified_diff(
                before.splitlines(keepends=True),
                after.splitlines(keepends=True),
                fromfile="policy.yaml (before)",
                tofile="policy.yaml (after)",
            )
        )
        safe_iso = iso.replace(":", "-")
        diff_path = os.path.join(history_dir, f"{safe_iso}-{step}.diff")
        with open(diff_path, "w", encoding="utf-8") as fh:
            fh.write(diff)
        promoted.append({"step": step, "diff_path": diff_path, "diff": diff})
    return promoted
