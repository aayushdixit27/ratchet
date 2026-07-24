"""Tiny stdlib-only HTTP helper.

Deliberately not `requests`/`httpx`: a hackathon demo should not depend on a
pip install succeeding on conference wifi. urllib is always there.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

DEFAULT_TIMEOUT = float(os.getenv("RATCHET_HTTP_TIMEOUT", "20"))


class HttpError(Exception):
    def __init__(self, status: int, body: str, url: str):
        super().__init__(f"HTTP {status} from {url}: {body[:300]}")
        self.status = status
        self.body = body
        self.url = url


def request_json(
    url: str,
    method: str = "GET",
    payload: dict | None = None,
    headers: dict[str, str] | None = None,
    timeout: float | None = None,
) -> dict:
    """JSON in, JSON out. Raises HttpError/URLError — callers must catch."""
    data = json.dumps(payload).encode() if payload is not None else None
    hdrs = {"Accept": "application/json", "User-Agent": "ratchet/0.1"}
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    hdrs.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout or DEFAULT_TIMEOUT) as r:
            body = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raise HttpError(e.code, e.read().decode("utf-8", "replace"), url) from e
    if not body.strip():
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"_raw": body}


def env(name: str, *fallbacks: str) -> str | None:
    """First non-empty env var among `name` and `fallbacks`."""
    for key in (name, *fallbacks):
        val = os.getenv(key)
        if val and val.strip():
            return val.strip()
    return None
