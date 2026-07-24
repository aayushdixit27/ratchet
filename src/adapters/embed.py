"""Deterministic offline embeddings.

Actian VectorAI DB is model-agnostic — it stores whatever vectors you give it.
That leaves us a choice, and it is a load-bearing one for a live demo:

  * call a hosted embedding API  -> better semantics, but the demo dies with
    the wifi and every retrieval costs money and latency;
  * embed locally with a model   -> a multi-hundred-MB download we do not have
    time for and cannot rely on at a venue;
  * hash-based feature embedding -> deterministic, instant, zero network, zero
    dependencies, and good enough to separate bug classes by root cause.

We take the third. Retrieval quality only has to be good enough to distinguish
"modal keeps state after unmount" from "link points at a dead route", and the
concept axes below do that with a wide margin. The vectors are real vectors and
the similarity search inside Actian is real vector search — nothing is faked,
we have just chosen a cheap embedding function.

Swap `embed()` for a hosted model later and nothing else in the stack changes.
"""

from __future__ import annotations

import hashlib
import math
import re

_STOP = {
    "the", "a", "an", "is", "are", "was", "were", "and", "or", "but", "not",
    "to", "of", "in", "on", "at", "it", "its", "this", "that", "with", "for",
    "from", "by", "as", "be", "been", "has", "have", "had", "does", "do", "did",
    "after", "before", "when", "then", "so", "no", "never", "always",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if w not in _STOP and len(w) > 2}


# A hand-built concept lexicon standing in for an embedding model. Each concept
# is the vocabulary a root cause of that class actually uses. Mapping text onto
# these axes is what lets a pattern learned from bug #1 match bug #7 — the
# "semantic matching on root cause" claim in PRODUCT.md §8 — without shipping a
# model download into a demo that has to survive dead wifi.
_CONCEPTS: dict[str, set[str]] = {
    "state_lifecycle": {
        "state", "unmount", "unmounted", "mount", "mounts", "mounted", "remount",
        "remounts", "reset", "resets", "stale", "retain", "retains", "retained",
        "keeps", "keep", "kept", "persist", "persists", "initialise", "initialised",
        "initialize", "initialized", "local", "draft", "reopen", "reopened",
        "cleared", "clear", "clears", "previous", "previously", "leftover", "copy",
        "working", "dialog", "modal", "drawer", "wizard", "close", "closed",
        "closemodal", "cancelling", "cancel", "cancelled", "prefilled", "between",
        "scratch", "abandoned", "discarded", "dismiss", "dismissal", "resumes",
        "survives", "null", "nulls", "nulling", "seed", "seeds", "seeded",
        "editdraft", "settingsdraft", "pendingdelete", "save", "saved",
    },
    "async_error": {
        "async", "await", "promise", "rejected", "rejection", "swallow",
        "swallows", "swallowed", "catch", "caught", "error", "errors", "fetch",
        "optimistic", "optimistically", "rollback", "silently", "silent",
        "request", "response", "fails", "failed", "failure", "network", "handler",
    },
    "validation": {
        "validate", "validates", "validating", "validation", "required", "empty",
        "blank", "guard", "guards", "guarded", "submit", "submits", "field",
        "fields", "input", "accepts", "accepted", "string", "form", "constraint",
        "trim", "whitespace", "length",
    },
    "a11y": {
        "aria", "label", "labels", "labelled", "unlabelled", "accessible",
        "accessibility", "screen", "reader", "announce", "announces", "announced",
        "placeholder", "assistive", "labelledby", "semantics", "role",
    },
    "concurrency": {
        "race", "races", "racing", "double", "twice", "duplicate", "duplicates",
        "reentry", "entry", "flight", "concurrent", "concurrently", "disabled",
        "enabled", "posts", "post", "queue", "debounce", "idempotent", "second",
    },
    "routing": {
        "route", "routes", "routed", "link", "links", "anchor", "href", "url",
        "path", "prefix", "404", "navigation", "navigate", "registered", "page",
        "redirect", "header", "renders", "reload", "reloads", "submission",
        "preventdefault", "native",
    },
    "binding": {
        "listener", "listeners", "bind", "binds", "bound", "selector", "element",
        "exist", "exists", "missing", "does", "dead", "control", "button",
        "silently", "swallows", "markup", "identifier", "typo",
    },
    "counting": {
        "count", "counter", "counts", "off", "one", "index", "length", "filter",
        "compensated", "arithmetic", "minus", "remaining", "total", "sum",
    },
}

# Small enough to keep Actian's index tiny and fast, big enough that hash
# collisions between our vocabulary terms are rare.
DIM = 256
_N_CONCEPTS = len(_CONCEPTS)
_CONCEPT_INDEX = {name: i for i, name in enumerate(sorted(_CONCEPTS))}

# The first `_N_CONCEPTS` dimensions are reserved for explicit concept axes and
# weighted heavily; the remainder is a hashed bag-of-words that carries the
# lexical detail. The split is what gives same-class root causes a high cosine
# while keeping different-class ones apart.
_CONCEPT_WEIGHT = 3.0


def embed(text: str) -> list[float]:
    """Text -> L2-normalised DIM-dimensional vector. Deterministic."""
    vec = [0.0] * DIM
    toks = _tokens(text)
    if not toks:
        return vec

    # explicit concept axes
    for name, vocab in _CONCEPTS.items():
        hits = len(toks & vocab)
        if hits:
            vec[_CONCEPT_INDEX[name]] += _CONCEPT_WEIGHT * (hits ** 0.7)

    # hashed bag-of-words over the remaining dimensions
    span = DIM - _N_CONCEPTS
    for tok in toks:
        h = hashlib.blake2b(tok.encode(), digest_size=8).digest()
        idx = _N_CONCEPTS + (int.from_bytes(h[:4], "big") % span)
        sign = 1.0 if h[4] & 1 else -1.0     # signed hashing cancels collisions
        vec[idx] += sign

    norm = math.sqrt(sum(v * v for v in vec))
    if norm:
        vec = [v / norm for v in vec]
    return vec


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))     # both are unit vectors
