"""Adapter factories.

Lane A imports only this module and `base`:

    from src.adapters import get_qa, get_memory, get_router, get_publisher, get_tracer
    from src.adapters.base import Bug, Pattern

`RATCHET_MODE=fixture` (the default) returns deterministic fixtures with zero
network. `RATCHET_MODE=live` returns the sponsor-backed adapters, each of which
falls back to its fixture on any failure and flips `.degraded = True` instead of
raising. A missing API key is treated as a failure, not an error — so `live`
mode is always safe to run.

Per-adapter override, useful for demoing one live integration at a time:

    RATCHET_MODE=fixture RATCHET_MEMORY_MODE=live python -m ratchet.loop
"""

from __future__ import annotations

import os

from .base import Bug, Pattern, QA, Memory, Router, Publisher, Tracer, usage
from .fixtures import (
    FixtureQA,
    FixtureMemory,
    FixtureRouter,
    FixturePublisher,
    FixtureTracer,
)

__all__ = [
    "get_qa", "get_memory", "get_router", "get_publisher", "get_tracer",
    "get_all", "Bug", "Pattern", "QA", "Memory", "Router", "Publisher",
    "Tracer", "usage",
]


def _mode(which: str) -> str:
    """Resolve mode for one adapter: per-adapter env wins over RATCHET_MODE."""
    specific = os.getenv(f"RATCHET_{which.upper()}_MODE")
    if specific:
        return specific.strip().lower()
    return (os.getenv("RATCHET_MODE") or "fixture").strip().lower()


def get_qa() -> QA:
    if _mode("qa") == "live":
        from .live_replay import ReplayQA
        return ReplayQA()
    return FixtureQA()


def get_memory() -> Memory:
    if _mode("memory") == "live":
        from .live_actian import ActianMemory
        return ActianMemory()
    return FixtureMemory()


def get_router() -> Router:
    if _mode("router") == "live":
        from .live_pioneer import PioneerRouter
        return PioneerRouter()
    return FixtureRouter()


def get_publisher() -> Publisher:
    if _mode("publisher") == "live":
        from .live_senso import SensoPublisher
        return SensoPublisher()
    return FixturePublisher()


def get_tracer() -> Tracer:
    if _mode("tracer") == "live":
        from .live_guild import GuildTracer
        return GuildTracer()
    return FixtureTracer()


def get_all() -> dict:
    """Everything at once, plus the backend each one resolved to.

    Handy for the dashboard header and for Lane A's per-run JSONL provenance
    block — `{"backends": {"qa": "replay-live", "memory": "fixture", ...}}`.
    """
    qa, mem, router = get_qa(), get_memory(), get_router()
    pub, tracer = get_publisher(), get_tracer()
    return {
        "qa": qa,
        "memory": mem,
        "router": router,
        "publisher": pub,
        "tracer": tracer,
        "backends": {
            "qa": getattr(qa, "backend", "unknown"),
            "memory": getattr(mem, "backend", "unknown"),
            "router": getattr(router, "backend", "unknown"),
            "publisher": getattr(pub, "backend", "unknown"),
            "tracer": getattr(tracer, "backend", "unknown"),
        },
    }
