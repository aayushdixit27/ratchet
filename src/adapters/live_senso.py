"""Senso Context OS — the Publisher adapter.

Senso is a programmable knowledge base with endpoints that publish content to
the web so *other agents can discover it*. That is the literal ask on the
challenge slide ("publish your agent's output to cited.md") and the second-order
moat in PRODUCT.md §9: a verified fix-pattern corpus that compounds across
teams instead of being relearned in private.

Auth is confirmed (`X-API-Key`, base `https://apiv2.senso.ai/api/v1`); the
ingest path and body fields are ⚠️ UNVERIFIED and overridable from `.env`.

Always writes the local `cited.md` too, via FixturePublisher — the artifact the
judges are pointed at must exist whether or not the network does.
"""

from __future__ import annotations

import os

from .base import Degradable, Pattern
from .fixtures import FixturePublisher
from .http import env, request_json

DEFAULT_BASE = "https://apiv2.senso.ai/api/v1"


class SensoPublisher(Degradable):
    def __init__(self):
        self._fixture = FixturePublisher()
        self._base = (env("SENSO_BASE_URL") or DEFAULT_BASE).rstrip("/")
        self._key = env("SENSO_API_KEY")
        self._path = os.getenv("SENSO_INGEST_PATH", "/content/raw")
        if not self._key:
            self._degrade("SENSO_API_KEY not set")
        else:
            self.backend = "senso-live"

    def publish(self, p: Pattern) -> str:
        # Local cited.md is written unconditionally — it is the demo artifact.
        local_url = self._fixture.publish(p)
        if self.degraded:
            return local_url
        try:
            body = request_json(
                f"{self._base}{self._path}",
                method="POST",
                payload={
                    "title": f"RATCHET fix-pattern: {p.bug_class}",
                    "text": self._markdown(p),
                    "summary": p.strategy[:280],
                    # tags let another agent retrieve this by bug class
                    "tags": ["ratchet", "fix-pattern", p.bug_class,
                             "verified" if p.verified else "unverified"],
                    "external_id": p.sig,
                },
                headers={"X-API-Key": self._key},
            )
            for k in ("url", "public_url", "web_url", "permalink", "link"):
                if body.get(k):
                    return str(body[k])
            return local_url
        except Exception as e:
            self._degrade(f"publish failed — {type(e).__name__}: {e}")
            return local_url

    @staticmethod
    def _markdown(p: Pattern) -> str:
        return (
            f"# Fix-pattern `{p.sig}`\n\n"
            f"**Bug class:** {p.bug_class}\n"
            f"**Verified:** {'yes' if p.verified else 'no'} · "
            f"**Reused:** {p.uses}x · **Score:** {p.score}\n\n"
            f"## Strategy\n\n{p.strategy}\n\n"
            + (f"## Code hint\n\n```\n{p.code_hint}\n```\n" if p.code_hint else "")
            + "\n---\nPublished by RATCHET, an agent whose cost per verified fix "
              "declines run over run. Other agents are free to reuse this pattern.\n"
        )
