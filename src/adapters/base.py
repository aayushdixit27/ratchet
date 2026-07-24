"""RATCHET adapter contract.

This file is the interface between Lane A (loop core) and Lane B (sponsor
integrations). Lane A codes against the Protocols and dataclasses below and
must never import anything else from `src.adapters` internals.

One-way dependency: nothing here may import from `src/ratchet/**`.
"""

from dataclasses import dataclass, field
from typing import Protocol, Literal
from contextlib import contextmanager


@dataclass
class Bug:
    id: str
    title: str
    root_cause: str            # Replay returns this — it is the semantic key, preserve it verbatim
    selector: str | None
    repro: list[str]
    bug_class: str
    raw: dict = field(default_factory=dict)


@dataclass
class Pattern:
    sig: str
    bug_class: str
    strategy: str              # natural-language fix recipe, model-consumable
    code_hint: str | None
    verified: bool
    uses: int = 0
    score: float = 0.0


class QA(Protocol):
    def scan(self, url: str) -> list[Bug]: ...
    def verify(self, url: str, bug: Bug) -> bool: ...


class Memory(Protocol):
    def search(self, text: str, k: int = 3) -> list[tuple[Pattern, float]]: ...
    def upsert(self, p: Pattern) -> None: ...


class Router(Protocol):
    def complete(self, prompt: str, tier: Literal["cheap", "strong"]) -> tuple[str, dict]: ...


class Publisher(Protocol):
    def publish(self, p: Pattern) -> str: ...


class Tracer(Protocol):
    @contextmanager
    def span(self, name: str, **meta): ...


# --- Additions below are Lane B implementation support. -----------------------
# They do not change the contract above; Lane A may ignore them entirely, or
# read `.degraded` / `.backend` off any adapter instance for the dashboard.

class Degradable:
    """Mixin for live adapters that silently fall back to a fixture.

    A live adapter NEVER re-raises. On any failure it flips `degraded` to True,
    records why, and serves the fixture for the rest of the run. Lane A can
    surface `degraded: true` in the JSONL without special-casing anything.
    """

    degraded: bool = False
    backend: str = "fixture"
    degrade_reason: str | None = None

    def _degrade(self, reason: str) -> None:
        if not self.degraded:
            self.degraded = True
            self.degrade_reason = reason
            self.backend = "fixture(degraded)"
            import sys
            print(f"[ratchet:adapter] {type(self).__name__} degraded -> fixture: {reason}",
                  file=sys.stderr)


def usage(calls: int, cost_usd: float, tier: str, model: str,
          prompt_tokens: int = 0, completion_tokens: int = 0, **extra) -> dict:
    """Canonical shape of the second element of `Router.complete`.

    Lane A sums `cost_usd` and `calls` per iteration — this is the number that
    drops on stage, so the keys are fixed here rather than per-adapter.
    """
    d = {
        "calls": calls,
        "cost_usd": round(cost_usd, 6),
        "tier": tier,
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
    }
    d.update(extra)
    return d
