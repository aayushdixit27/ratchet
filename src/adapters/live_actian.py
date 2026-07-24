"""Actian VectorAI DB — the Memory adapter.

This is the thesis. "The failure mode is state, not intelligence" — the agent
gets cheaper run over run because verified fix-patterns persist here as vectors
and are retrieved by *root cause*, not by symptom. That semantic hop is what
makes a pattern learned from bug #1 apply to bug #7.

Vectors come from `embed.py` (deterministic, offline). Actian does the real
vector search. Degrades to FixtureMemory if the SDK or the server is absent.

Server:  docker run -p 6574:6574 vectoraidb
SDK:     pip install actian-vectorai   (Community Edition)
"""

from __future__ import annotations

import hashlib
import os

from .base import Degradable, Pattern
from .embed import DIM, embed
from .fixtures import FixtureMemory
from .http import env

DEFAULT_ENDPOINT = "localhost:6574"
DEFAULT_COLLECTION = "ratchet_fix_patterns"


def _point_id(sig: str) -> int:
    """Stable positive 63-bit int id from a pattern signature."""
    return int.from_bytes(hashlib.blake2b(sig.encode(), digest_size=8).digest(), "big") >> 1


class ActianMemory(Degradable):
    def __init__(self):
        self._fixture = FixtureMemory()
        self._endpoint = env("ACTIAN_ENDPOINT") or DEFAULT_ENDPOINT
        self._collection = env("ACTIAN_COLLECTION") or DEFAULT_COLLECTION
        self._client = None
        self._sdk = None
        self._connect()

    # -- Protocol ----------------------------------------------------------
    def search(self, text: str, k: int = 3) -> list[tuple[Pattern, float]]:
        if self.degraded:
            return self._fixture.search(text, k)
        try:
            results = self._client.points.search(
                self._collection, vector=embed(text), limit=k)
            out: list[tuple[Pattern, float]] = []
            for r in results:
                payload = getattr(r, "payload", None) or {}
                p = self._to_pattern(payload)
                if p is not None:
                    out.append((p, round(float(getattr(r, "score", 0.0)), 4)))
            return out
        except Exception as e:
            self._degrade(f"search failed — {type(e).__name__}: {e}")
            return self._fixture.search(text, k)

    def upsert(self, p: Pattern) -> None:
        # Always mirror into the fixture store. If Actian drops out mid-run the
        # loop keeps its memory and retention stays visible on stage.
        self._fixture.upsert(p)
        if self.degraded:
            return
        try:
            PointStruct = self._sdk["PointStruct"]
            # vars(p) carries the whole dataclass — including provenance —
            # so nothing is lost round-tripping through the live DB.
            self._client.points.upsert(self._collection, [PointStruct(
                id=_point_id(p.sig),
                vector=embed(f"{p.bug_class} {p.strategy} {p.code_hint or ''}"),
                payload=dict(vars(p)),
            )])
        except Exception as e:
            self._degrade(f"upsert failed — {type(e).__name__}: {e}")

    def all(self) -> list[Pattern]:
        """Everything remembered — the mirror is authoritative for display."""
        return self._fixture.all()

    def reset(self) -> None:
        """Clean slate between demo runs — available in every mode."""
        self._fixture.reset()
        if self.degraded:
            return
        try:
            self._client.collections.delete(self._collection)
        except Exception:
            pass  # best-effort; the mirror is already clear
        self._connect()

    # -- internals ---------------------------------------------------------
    def _connect(self) -> None:
        try:
            from actian_vectorai import (  # type: ignore
                VectorAIClient, VectorParams, Distance, PointStruct,
            )
        except Exception as e:
            self._degrade(f"actian_vectorai SDK not importable ({e}); "
                          "install Community Edition to go live")
            return
        self._sdk = {"PointStruct": PointStruct}
        try:
            client = VectorAIClient(self._endpoint)
            client.health_check()
            try:
                client.collections.create(
                    self._collection,
                    vectors_config=VectorParams(size=DIM, distance=Distance.Cosine),
                )
            except Exception:
                pass  # already exists — the common case on re-runs
            self._client = client
            self.backend = "actian-live"
        except Exception as e:
            self._degrade(f"cannot reach VectorAI DB at {self._endpoint} "
                          f"({type(e).__name__}: {e}); is `docker run -p 6574:6574 vectoraidb` up?")

    @staticmethod
    def _to_pattern(payload: dict) -> Pattern | None:
        try:
            known = {f for f in Pattern.__dataclass_fields__}
            kwargs = {k: v for k, v in payload.items() if k in known}
            kwargs.setdefault("sig", payload["sig"])
            kwargs["code_hint"] = payload.get("code_hint") or None
            return Pattern(**kwargs)
        except Exception:
            return None
