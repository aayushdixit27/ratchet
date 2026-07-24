"""Read-only separation matrix for the embedding + live corpus.

Recomputes the checks behind ALL-011/ALL-012 decision 2 so they can be
re-verified after any corpus regeneration, instead of living in one
session's shell history:

  1. Embed-level matrix (corpus-independent): live Replay bugs and app2
     bugs vs the tasker fixture catalog. Mates must clear the bar with
     margin, non-mates must stay under it. Thresholds: 0.55 same-app,
     0.75 cross-app.
  2. Live-corpus search (corpus-dependent): what the runtime would
     actually retrieve from Actian right now. Scores here move whenever
     the corpus text regenerates — never script them in a demo.

Usage:  python3 -m src.adapters.matrix_check
Never writes anything. Safe against a live collection, but meaningless
while a run is mid-flight (corpus half-built).
"""

from __future__ import annotations

import json
import pathlib

from .embed import cosine, embed

ROOT = pathlib.Path(__file__).resolve().parents[2]
SAME_APP_BAR = 0.55
CROSS_APP_BAR = 0.75

# Live Replay bug id -> the fixture class it instantiates (hand-checked 12:45).
LIVE_CLASS = {
    "bug-mrzceiuz-wr97": "counter-off-by-one",
    "bug-mrzbwnr6-7cmb": "modal-state-not-reset",
    "bug-mrzbq4us-w9k6": "dead-control",
    "bug-mrzbpqy5-cmda": "unclassified",  # aria-selected: no fixture mate exists
}


def _load(path: str) -> list[dict]:
    d = json.load(open(ROOT / path))
    return d["bugs"] if isinstance(d, dict) else d


def _matrix(queries: list[tuple[str, str, str]], refs: list[tuple[str, str, str]],
            bar: float) -> None:
    ref_vecs = [(rid, rcls, embed(txt)) for rid, rcls, txt in refs]
    for qid, qcls, qtxt in queries:
        qv = embed(qtxt)
        scored = sorted(((cosine(qv, rv), rid, rcls) for rid, rcls, rv in ref_vecs),
                        reverse=True)
        mate = max((s for s, _, rcls in scored if rcls == qcls), default=None)
        nonmate = max((s for s, _, rcls in scored if rcls != qcls), default=None)
        top_s, top_id, top_cls = scored[0]
        verdict = "HIT" if top_s >= bar else "miss"
        clean = (mate is None) or (top_cls == qcls)
        print(f"  {qid:22s} [{qcls:24s}] top={top_s:.4f} {top_id:8s} [{top_cls}] "
              f"mate={f'{mate:.4f}' if mate is not None else '  --  '} "
              f"nonmate={f'{nonmate:.4f}' if nonmate is not None else '  --  '} "
              f"{verdict}{'' if clean else '  ** WRONG-CLASS TOP **'}")


def main() -> None:
    tasker = [(b["id"], b["class"], b["root_cause"]) for b in _load("app/bugs.json")]
    app2 = [(b["id"], b["class"], b["root_cause"]) for b in _load("app2/bugs.json")]
    live = [(b["id"], LIVE_CLASS.get(b["id"], "unclassified"), b["root_cause"])
            for b in _load("src/adapters/seeds/replay_bugs_live.json")]

    print(f"== live Replay bugs vs tasker catalog (same-app bar {SAME_APP_BAR}) ==")
    _matrix(live, tasker, SAME_APP_BAR)

    print(f"\n== app2 bugs vs tasker catalog (cross-app bar {CROSS_APP_BAR}) ==")
    _matrix(app2, tasker, CROSS_APP_BAR)

    print("\n== live corpus search (corpus-dependent — do NOT script these) ==")
    from . import get_memory
    mem = get_memory()
    print(f"  adapter={type(mem).__name__} degraded={getattr(mem, 'degraded', '?')}")
    for qid, qcls, qtxt in live + app2:
        hits = mem.search(qtxt, k=3)
        if not hits:
            print(f"  {qid:22s} [{qcls:24s}] (no hits)")
            continue
        p, s = hits[0]
        print(f"  {qid:22s} [{qcls:24s}] top={s:.4f} pattern_class={p.bug_class} "
              f"origin={p.origin_app} uses={p.uses}")


if __name__ == "__main__":
    main()
