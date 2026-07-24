"""Provider selection — a thin wrapper over Lane B's src.adapters.

Lane A imports ONLY from src.adapters (the contract) and never edits it. Lane B's
adapters already resolve fixture-vs-live per RATCHET_MODE and self-degrade on any
failure, so this module just gathers them and exposes the contract types.
"""
from __future__ import annotations

import os
import sys
from types import SimpleNamespace

# Make `src.adapters` importable no matter how we were launched
# (`python -m ratchet.run` after editable install, or from the repo root).
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)


def _import_adapters():
    try:
        import src.adapters as A  # repo root on path
        from src.adapters.base import Bug, Pattern
        return A, Bug, Pattern
    except Exception:
        import adapters as A  # src on path (editable install)
        from adapters.base import Bug, Pattern
        return A, Bug, Pattern


def build(mode: str | None = None) -> SimpleNamespace:
    if mode:
        os.environ["RATCHET_MODE"] = mode
    A, Bug, Pattern = _import_adapters()
    qa = A.get_qa()
    memory = A.get_memory()
    router = A.get_router()
    publisher = A.get_publisher()
    tracer = A.get_tracer()
    backends = {
        "qa": getattr(qa, "backend", "unknown"),
        "memory": getattr(memory, "backend", "unknown"),
        "router": getattr(router, "backend", "unknown"),
        "publisher": getattr(publisher, "backend", "unknown"),
        "tracer": getattr(tracer, "backend", "unknown"),
    }
    return SimpleNamespace(
        qa=qa, memory=memory, router=router, publisher=publisher, tracer=tracer,
        Bug=Bug, Pattern=Pattern, backends=backends,
    )
