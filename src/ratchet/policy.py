"""policy.yaml is the agent's editable brain-stem. The loop *reads* it every
iteration; evolve() *rewrites* it. We deliberately avoid PyYAML so the loop has
zero runtime dependencies and cannot fail to start on a cold offline demo box.

The reader understands exactly the restricted schema we author:
  key: scalar
  cold_path_steps:
    - item
  deterministic_rules: {}   |   deterministic_rules:\n  key: value

evolve() edits the file surgically (line-level) rather than load->dump, so the
unified diff we `cat` on stage is minimal and human-readable — that diff is the
single most surprising artifact we show a technical judge.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

POLICY_PATH = os.path.join(os.path.dirname(__file__), "policy.yaml")

_LIST_KEYS = {"cold_path_steps", "warm_path_steps"}
_MAP_KEYS = {"deterministic_rules"}

# The pristine iteration-0 policy. run.py restores this at the start of every run
# so the demo re-derives the agent's self-authored diff live and reproducibly.
BASELINE_YAML = """\
# RATCHET policy — THE AGENT EDITS THIS FILE.
# evolve() (the slow loop) rewrites it in place when it finds an LLM step whose
# output has been effectively deterministic across >=3 occurrences. The before/
# after diff lands in policy_history/. This file's drift from its it-0 state is
# the evidence that the agent improved itself, unattended.
# warm_threshold 0.55: same-class root causes score 0.62-0.90, cross-class well
# below, so a pattern is reused only for its own bug class, never a wrong one.
warm_threshold: 0.55
evolve_every: 2
cold_path_steps:
  - localize
  - hypothesize
  - synthesize_patch
  - self_review
warm_path_steps:
  - apply_known
deterministic_rules: {}
"""


def reset_policy(path: str = POLICY_PATH) -> None:
    """Restore policy.yaml to its pristine iteration-0 baseline."""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(BASELINE_YAML)


@dataclass
class Policy:
    warm_threshold: float = 0.55
    evolve_every: int = 2
    cold_path_steps: list[str] = field(default_factory=list)
    warm_path_steps: list[str] = field(default_factory=list)
    deterministic_rules: dict[str, str] = field(default_factory=dict)


def _coerce(v: str):
    v = v.strip()
    if v == "{}":
        return {}
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


def load_policy(path: str = POLICY_PATH) -> Policy:
    p = Policy(cold_path_steps=[], warm_path_steps=[])
    cur_list: str | None = None
    cur_map: str | None = None
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            indented = line[0] in (" ", "\t")
            stripped = line.strip()
            if not indented:
                cur_list = cur_map = None
                if ":" not in stripped:
                    continue
                key, _, val = stripped.partition(":")
                key, val = key.strip(), val.strip()
                if key in _LIST_KEYS:
                    cur_list = key
                    setattr(p, key, [])
                elif key in _MAP_KEYS:
                    if val == "{}" or val == "":
                        setattr(p, key, {})
                        cur_map = None if val == "{}" else key
                    else:
                        setattr(p, key, _coerce(val))
                    if val == "":
                        cur_map = key
                elif hasattr(p, key):
                    setattr(p, key, _coerce(val))
            else:
                if cur_list and stripped.startswith("- "):
                    getattr(p, cur_list).append(stripped[2:].strip())
                elif cur_map and ":" in stripped:
                    k, _, v = stripped.partition(":")
                    getattr(p, cur_map)[k.strip()] = _coerce(v)
    return p


def promote_step(step: str, rule: str = "approve", path: str = POLICY_PATH) -> str:
    """Surgically rewrite policy.yaml to (1) drop `step` from cold_path_steps and
    (2) record it under deterministic_rules. Returns the NEW full file text.
    Idempotent: promoting an already-promoted step returns the text unchanged."""
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    out: list[str] = []
    in_cold = False
    in_det = False
    det_had_entries = False
    det_insert_idx: int | None = None
    already = False

    for line in lines:
        stripped = line.strip()
        indented = line[:1] in (" ", "\t")

        # track section context on non-indented header lines
        if not indented and stripped.endswith(":") or (not indented and ":" in stripped):
            in_cold = stripped.startswith("cold_path_steps:")
            in_det = stripped.startswith("deterministic_rules:")
            if in_det:
                # normalise `deterministic_rules: {}` -> `deterministic_rules:`
                if stripped.endswith("{}"):
                    line = "deterministic_rules:\n"
                out.append(line)
                det_insert_idx = len(out)  # rules get appended right after header
                continue

        if in_cold and indented and stripped == f"- {step}":
            continue  # drop the promoted step from the cold path

        if in_det and indented and stripped.startswith(f"{step}:"):
            already = True

        if in_det and indented and ":" in stripped:
            det_had_entries = True

        out.append(line)

    if not already:
        new_rule = f"  {step}: {rule}\n"
        if det_insert_idx is not None:
            out.insert(det_insert_idx, new_rule)
        else:
            out.append("deterministic_rules:\n")
            out.append(new_rule)

    text = "".join(out)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text
