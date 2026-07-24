"""Replay QA — the QA adapter.

Feed it a URL, get back root-caused bug reports. `root_cause` is the field the
whole retrieval thesis depends on, so it is preserved verbatim.

⚠️ UNVERIFIED PATHS. Replay's REST reference is behind signup and was not
reachable before the time-box expired, so the endpoint paths and response field
names below are best guesses. Every one of them is overridable from `.env`
(`REPLAY_SCAN_PATH`, `REPLAY_RESULT_PATH`, …) and the response parser accepts
several field spellings — so correcting this against the real docs should be a
config change, not a code change. Until then it degrades to FixtureQA.

Also note: Replay cannot reach localhost. `RATCHET_TARGET_URL` must be the
public URL of the fixture app.
"""

from __future__ import annotations

import os
import time

from .base import Bug, Degradable
from .fixtures import FixtureQA
from .http import env, request_json

DEFAULT_BASE = "https://api.replay.io/qa/v1"


def _first(d: dict, *names: str, default=None):
    """First present, non-empty key among several candidate spellings."""
    for n in names:
        if n in d and d[n] not in (None, "", [], {}):
            return d[n]
    return default


class ReplayQA(Degradable):
    def __init__(self):
        self._fixture = FixtureQA()
        self._base = (env("REPLAY_BASE_URL") or DEFAULT_BASE).rstrip("/")
        self._key = env("REPLAY_API_KEY")
        self._scan_path = os.getenv("REPLAY_SCAN_PATH", "/scans")
        self._result_path = os.getenv("REPLAY_RESULT_PATH", "/scans/{id}")
        self._poll_seconds = float(os.getenv("REPLAY_POLL_SECONDS", "5"))
        self._poll_max = int(os.getenv("REPLAY_POLL_MAX", "24"))  # ~2 min
        if not self._key:
            self._degrade("REPLAY_API_KEY not set")
        else:
            self.backend = "replay-live"

    # -- Protocol ----------------------------------------------------------
    def scan(self, url: str) -> list[Bug]:
        if self.degraded:
            return self._fixture.scan(url)
        try:
            bugs = self._scan(url)
            if not bugs:
                # A live scan that finds nothing is indistinguishable on stage
                # from a broken integration. Say so loudly rather than showing
                # an empty queue.
                self._degrade("live scan returned zero bugs")
                return self._fixture.scan(url)
            return bugs
        except Exception as e:
            self._degrade(f"scan failed — {type(e).__name__}: {e}")
            return self._fixture.scan(url)

    def verify(self, url: str, bug: Bug) -> bool:
        """A fix is verified when a fresh scan no longer reports this bug."""
        if self.degraded:
            return self._fixture.verify(url, bug)
        try:
            remaining = self._scan(url)
            still_there = any(
                b.id == bug.id or (b.root_cause.strip() == bug.root_cause.strip())
                for b in remaining
            )
            return not still_there
        except Exception as e:
            self._degrade(f"verify failed — {type(e).__name__}: {e}")
            return self._fixture.verify(url, bug)

    def reset(self) -> None:
        """Clean slate between demo runs — available in every mode."""
        self._fixture.reset()

    # -- internals ---------------------------------------------------------
    @property
    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._key}"}

    def _scan(self, url: str) -> list[Bug]:
        target = env("RATCHET_TARGET_URL") or url
        started = request_json(
            f"{self._base}{self._scan_path}",
            method="POST",
            payload={"url": target},
            headers=self._headers,
        )
        # Some APIs return results inline; only poll if we got a job handle.
        bugs = self._extract(started)
        if bugs:
            return bugs
        scan_id = _first(started, "id", "scan_id", "scanId", "job_id")
        if not scan_id:
            raise ValueError(f"no scan id or bugs in response: {str(started)[:200]}")

        path = self._result_path.replace("{id}", str(scan_id))
        for _ in range(self._poll_max):
            time.sleep(self._poll_seconds)
            body = request_json(f"{self._base}{path}", headers=self._headers)
            status = str(_first(body, "status", "state", default="")).lower()
            bugs = self._extract(body)
            if bugs or status in ("complete", "completed", "done", "finished", "succeeded"):
                return bugs
            if status in ("failed", "error", "cancelled"):
                raise RuntimeError(f"scan {scan_id} ended as {status}")
        raise TimeoutError(f"scan {scan_id} still running after "
                           f"{self._poll_max * self._poll_seconds:.0f}s")

    def _extract(self, body: dict) -> list[Bug]:
        raw = _first(body, "bugs", "issues", "findings", "results", "reports", default=[])
        if isinstance(raw, dict):
            raw = raw.get("items") or raw.get("data") or []
        out: list[Bug] = []
        for i, r in enumerate(raw or []):
            if not isinstance(r, dict):
                continue
            selector = _first(r, "selector", "css_selector", "element")
            if isinstance(selector, list):
                selector = selector[0] if selector else None
            repro = _first(r, "repro", "steps", "reproduction", "repro_steps", default=[])
            if isinstance(repro, str):
                repro = [s.strip() for s in repro.splitlines() if s.strip()]
            title = _first(r, "title", "summary", "name", "symptom", default="untitled bug")
            out.append(Bug(
                id=str(_first(r, "id", "bug_id", "key", default=f"REPLAY-{i+1:02d}")),
                title=str(title),
                # verbatim — this is the semantic key for retrieval
                root_cause=str(_first(r, "root_cause", "rootCause", "cause",
                                      "analysis", "explanation", default=title)),
                selector=str(selector) if selector else None,
                repro=[str(s) for s in repro],
                bug_class=str(_first(r, "class", "bug_class", "category", "type",
                                     default="unclassified")),
                raw={**r, "source": "replay-live"},
            ))
        return out
