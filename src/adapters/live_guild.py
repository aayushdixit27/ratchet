"""Guild.ai — the Tracer adapter.

Guild is the control plane: govern, run and trace agents. Traces matter here
for two reasons beyond observability:

  1. per-run cost attribution shown next to the JSONL metric;
  2. the slow loop reads its own traces to find LLM steps whose output has been
     effectively deterministic, and rewrites them into code.

So spans are always recorded locally (via FixtureTracer) even when the live
export fails — the self-improvement path must not depend on the network.

⚠️ UNVERIFIED PATHS — Guild's REST reference is behind login. Endpoint and
field names are overridable from `.env`. Degrades silently to local-only.
"""

from __future__ import annotations

import atexit
import os
from contextlib import contextmanager

from .base import Degradable
from .fixtures import FixtureTracer
from .http import env, request_json

DEFAULT_BASE = "https://api.guild.ai/v1"


class GuildTracer(Degradable):
    def __init__(self):
        self._local = FixtureTracer()          # always-on local recorder
        self._base = (env("GUILD_BASE_URL") or DEFAULT_BASE).rstrip("/")
        self._key = env("GUILD_API_KEY")
        self._project = env("GUILD_PROJECT") or "ratchet"
        self._path = os.getenv("GUILD_TRACE_PATH", "/traces")
        self._batch = int(os.getenv("GUILD_BATCH", "10"))
        self._pending: list[dict] = []
        if not self._key:
            self._degrade("GUILD_API_KEY not set — spans recorded locally only")
        else:
            self.backend = "guild-live"
            atexit.register(self.flush)        # never lose the tail of a run

    @contextmanager
    def span(self, name: str, **meta):
        with self._local.span(name, **meta) as record:
            yield record
        # the local tracer has filled in duration/ok by now
        self._pending.append({**record, "project": self._project})
        if len(self._pending) >= self._batch:
            self.flush()

    def flush(self) -> None:
        if self.degraded:
            self._pending.clear()   # don't grow a buffer nobody will ever send
            return
        if not self._pending:
            return
        batch, self._pending = self._pending, []
        try:
            request_json(
                f"{self._base}{self._path}",
                method="POST",
                payload={"project": self._project, "spans": batch},
                headers={"Authorization": f"Bearer {self._key}"},
            )
        except Exception as e:
            self._degrade(f"trace export failed — {type(e).__name__}: {e}")

    def export(self) -> list[dict]:
        """Local span log — what the slow loop reads. Always populated."""
        return self._local.export()
