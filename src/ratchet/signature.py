"""Stable bug signatures. Same root cause + same selector *shape* -> same sig,
so a fix-pattern learned on bug b3 retrieves for the structurally-identical b7.

This is the crux of the retention story: signatures are what let semantic memory
generalise one fix across bugs it has never literally seen before.
"""
from __future__ import annotations

import hashlib
import re

_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^a-z0-9 ]+")
_DIGITS = re.compile(r"\d+")
_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*")


def rc_key(root_cause: str) -> str:
    """Normalise a root-cause string: lowercase, strip punctuation, collapse
    whitespace. Two root causes that differ only in casing/spacing/punctuation
    map to the same key."""
    s = root_cause.lower().strip()
    s = _PUNCT.sub(" ", s)
    s = _WS.sub(" ", s).strip()
    return s


def selector_shape(selector: str | None) -> str:
    """Reduce a CSS/DOM selector to its *shape* — structure without the volatile
    bits. `#modal-42 .btn` and `#modal-99 .btn` share a shape."""
    if not selector:
        return "-"
    s = _DIGITS.sub("N", selector)
    s = _WS.sub(" ", s).strip()
    return s


def signature(bug) -> str:
    """A stable 12-hex-char signature for a bug: hash of normalised root cause
    plus selector shape. Deterministic across runs (no salt, no randomness)."""
    payload = f"{rc_key(bug.root_cause)}|{selector_shape(bug.selector)}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]
