"""Deterministic fixture implementations of every adapter.

These are not throwaway. If the wifi dies on stage, these carry the demo — so
they are seeded, deterministic, and produce realistic numbers. Every live
adapter falls back to the corresponding class here.

No randomness anywhere: same inputs -> same bugs, same costs, same scores.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

from .base import Bug, Pattern, usage

REPO_ROOT = Path(__file__).resolve().parents[2]
SEED_DIR = Path(__file__).resolve().parent / "seeds"


def state_dir() -> Path:
    """Adapter-owned scratch state (fixture memory, patch ledger).

    Self-ignoring directory so it never lands in a commit and never touches
    another lane's .gitignore.
    """
    d = Path(os.getenv("RATCHET_STATE_DIR") or (REPO_ROOT / ".ratchet"))
    d.mkdir(parents=True, exist_ok=True)
    gi = d / ".gitignore"
    if not gi.exists():
        gi.write_text("*\n")
    return d


def _stable_unit(*parts: str) -> float:
    """Deterministic float in [0, 1) from the given strings."""
    h = hashlib.sha256("|".join(parts).encode()).hexdigest()
    return int(h[:12], 16) / float(1 << 48)


# --------------------------------------------------------------------------- QA

_BUGS_MD_FIELDS = {
    "root_cause": "root_cause",
    "root cause": "root_cause",
    "class": "bug_class",
    "bug_class": "bug_class",
    "selector": "selector",
    "repro": "repro",
}


def _parse_bugs_md(text: str) -> list[Bug]:
    """Forgiving parser for Lane C's `app/BUGS.md`.

    Expects blocks like:

        ## BUG-01 — Title of the bug
        - class: state-not-reset-on-unmount
        - selector: #edit-task-modal
        - root_cause: Modal keeps local form state after unmount...
        - repro:
          1. Open task and click Edit
          2. Close without saving

    Anything it cannot understand is skipped rather than raised.
    """
    bugs: list[Bug] = []
    blocks = re.split(r"^##\s+", text, flags=re.M)[1:]
    for block in blocks:
        lines = block.splitlines()
        header = lines[0].strip()
        m = re.match(r"([A-Za-z]+[-_]?\d+)\s*[—\-:–]\s*(.+)", header)
        if m:
            bug_id, title = m.group(1).strip(), m.group(2).strip()
        else:
            bug_id, title = header.split()[0] if header else "BUG-?", header
        fields: dict[str, object] = {}
        repro: list[str] = []
        collecting_repro = False
        for line in lines[1:]:
            stripped = line.strip().lstrip("-*").strip()
            if not stripped:
                continue
            kv = re.match(r"([A-Za-z_ ]+):\s*(.*)$", stripped)
            key = kv.group(1).strip().lower() if kv else None
            if key in _BUGS_MD_FIELDS:
                collecting_repro = _BUGS_MD_FIELDS[key] == "repro"
                if collecting_repro:
                    val = kv.group(2).strip()
                    if val:
                        repro.append(val)
                else:
                    fields[_BUGS_MD_FIELDS[key]] = kv.group(2).strip()
            elif collecting_repro:
                repro.append(re.sub(r"^\d+[.)]\s*", "", stripped))
        root_cause = str(fields.get("root_cause") or title)
        bug_class = str(fields.get("bug_class") or "unclassified")
        selector = fields.get("selector") or None
        bugs.append(Bug(
            id=bug_id,
            title=title,
            root_cause=root_cause,
            selector=str(selector) if selector else None,
            repro=repro,
            bug_class=bug_class,
            raw={"source": "app/BUGS.md"},
        ))
    return bugs


class FixtureQA:
    """Replay QA stand-in.

    Reads `app/BUGS.md` if Lane C has written one, otherwise the local seed.
    Always yields 8 bugs, 3 of which share `state-not-reset-on-unmount` — that
    shared class is what makes memory retention visible by iteration 3.
    """

    backend = "fixture"
    degraded = False
    degrade_reason: str | None = None

    def __init__(self, bugs_md: Path | None = None, seed: Path | None = None):
        self._bugs_md = bugs_md or (REPO_ROOT / "app" / "BUGS.md")
        self._seed = seed or (SEED_DIR / "bugs.json")
        self._ledger = state_dir() / "patches.json"

    # -- Protocol ----------------------------------------------------------
    def scan(self, url: str) -> list[Bug]:
        bugs = self._load()
        fixed = self._patched()
        return [b for b in bugs if b.id not in fixed]

    def verify(self, url: str, bug: Bug) -> bool:
        """True once a patch has been recorded for this bug.

        The loop calls `verify()` after attempting a fix, so the first call for
        a given bug records the patch and returns True. Deterministic, and it
        makes `scan()` on the next iteration return a shorter list — the bug
        actually leaves the queue, which is what the dashboard shows.
        """
        self.record_patch(bug.id)
        return True

    # -- Fixture-only extras (Lane A may ignore these) ----------------------
    def record_patch(self, bug_id: str) -> None:
        fixed = self._patched()
        fixed.add(bug_id)
        self._ledger.write_text(json.dumps(sorted(fixed), indent=2))

    def reset(self) -> None:
        """Clear the patch ledger — call between demo runs for a clean slate."""
        if self._ledger.exists():
            self._ledger.unlink()

    # -- internals ---------------------------------------------------------
    def _patched(self) -> set[str]:
        try:
            return set(json.loads(self._ledger.read_text()))
        except Exception:
            return set()

    def _load(self) -> list[Bug]:
        if self._bugs_md.exists():
            try:
                parsed = _parse_bugs_md(self._bugs_md.read_text())
                if len(parsed) >= 3:
                    return parsed
            except Exception:
                pass  # fall through to the seed — never crash the loop
        data = json.loads(self._seed.read_text())
        return [
            Bug(
                id=b["id"],
                title=b["title"],
                root_cause=b["root_cause"],
                selector=b.get("selector"),
                repro=list(b.get("repro", [])),
                bug_class=b["bug_class"],
                raw={"source": "seed"},
            )
            for b in data["bugs"]
        ]


# ----------------------------------------------------------------------- Memory

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
        "cleared", "clear", "previous", "previously", "leftover", "copy",
        "working", "dialog", "modal", "drawer", "wizard", "close", "closed",
        "cancelling", "cancel", "prefilled", "between",
    },
    "async_error": {
        "async", "await", "promise", "rejected", "rejection", "swallow",
        "swallows", "swallowed", "catch", "caught", "error", "errors", "fetch",
        "optimistic", "optimistically", "rollback", "silently", "silent",
        "request", "response", "fails", "failed", "failure", "network", "handler",
    },
    "validation": {
        "validate", "validates", "validating", "validation", "required", "empty",
        "blank", "guard", "guards", "submit", "submits", "field", "fields",
        "input", "accepts", "accepted", "string", "form", "constraint",
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
        "redirect", "header", "renders",
    },
}


def _concept_vector(tokens: set[str]) -> dict[str, float]:
    vec: dict[str, float] = {}
    for concept, vocab in _CONCEPTS.items():
        hits = len(tokens & vocab)
        if hits:
            # sub-linear: three strong signals shouldn't triple-count
            vec[concept] = hits ** 0.7
    return vec


def _cosine(va: dict[str, float], vb: dict[str, float]) -> float:
    shared = set(va) & set(vb)
    if not shared:
        return 0.0
    dot = sum(va[k] * vb[k] for k in shared)
    na = sum(v * v for v in va.values()) ** 0.5
    nb = sum(v * v for v in vb.values()) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def _similarity(a: str, b: str) -> float:
    """Concept-vector cosine blended with literal token overlap.

    Not a real embedding, but it separates 'modal keeps state after unmount'
    from 'link points at the wrong route' with the margin a real embedding
    gives — same-class root causes land ~0.7-0.9, cross-class below ~0.35 —
    so Lane A's threshold logic is exercised against realistic scores.
    """
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    concept = _cosine(_concept_vector(ta), _concept_vector(tb))
    inter = ta & tb
    coverage = len(inter) / min(len(ta), len(tb)) if inter else 0.0
    return round(min(1.0, 0.72 * concept + 0.28 * coverage), 4)


class FixtureMemory:
    """Actian VectorAI stand-in — token-overlap similarity, JSON-backed.

    Persists across process boundaries so retention survives a restart mid-demo.
    """

    backend = "fixture"
    degraded = False
    degrade_reason: str | None = None

    def __init__(self, path: Path | None = None):
        self._path = path or (state_dir() / "memory_fixture.json")
        self._patterns: dict[str, Pattern] = {}
        self._load()

    # -- Protocol ----------------------------------------------------------
    def search(self, text: str, k: int = 3) -> list[tuple[Pattern, float]]:
        scored = [
            (p, _similarity(text, f"{p.bug_class} {p.strategy} {p.code_hint or ''}"))
            for p in self._patterns.values()
        ]
        scored = [s for s in scored if s[1] > 0.0]
        scored.sort(key=lambda s: (-s[1], -s[0].uses, s[0].sig))
        return scored[:k]

    def upsert(self, p: Pattern) -> None:
        existing = self._patterns.get(p.sig)
        if existing:
            p.uses = max(p.uses, existing.uses)
        self._patterns[p.sig] = p
        self._flush()

    # -- Fixture-only extras -----------------------------------------------
    def all(self) -> list[Pattern]:
        return list(self._patterns.values())

    def reset(self) -> None:
        self._patterns = {}
        self._flush()

    # -- internals ---------------------------------------------------------
    def _load(self) -> None:
        try:
            raw = json.loads(self._path.read_text())
            self._patterns = {k: Pattern(**v) for k, v in raw.items()}
        except Exception:
            self._patterns = {}

    def _flush(self) -> None:
        try:
            self._path.write_text(json.dumps(
                {k: vars(v) for k, v in self._patterns.items()}, indent=2))
        except Exception:
            pass  # memory is best-effort; never crash the loop


# ----------------------------------------------------------------------- Router

# Fixture price book. `strong` is deliberately ~14x `cheap` per call-set so the
# warm/cold gap is unmistakable on the dashboard.
CHEAP_BASE_USD = 0.030
STRONG_BASE_USD = 0.420


class FixtureRouter:
    """Pioneer router stand-in. Canned text, realistic deterministic usage."""

    backend = "fixture"
    degraded = False
    degrade_reason: str | None = None

    def complete(self, prompt: str, tier: Literal["cheap", "strong"]) -> tuple[str, dict]:
        jitter = _stable_unit(tier, prompt)
        if tier == "cheap":
            calls = 1
            cost = CHEAP_BASE_USD * (0.92 + 0.16 * jitter)
            model = "pioneer/fixture-fast"
            ptok, ctok = 850 + int(300 * jitter), 160 + int(80 * jitter)
            text = self._warm_text(prompt)
        else:
            calls = 4
            cost = STRONG_BASE_USD * (0.93 + 0.14 * jitter)
            model = "pioneer/fixture-strong"
            ptok, ctok = 4900 + int(1200 * jitter), 1250 + int(400 * jitter)
            text = self._cold_text(prompt)
        return text, usage(calls, cost, tier, model, ptok, ctok, backend="fixture")

    # -- canned generations -------------------------------------------------
    @staticmethod
    def _warm_text(prompt: str) -> str:
        return (
            "Reusing the retrieved fix-pattern. Apply the stored strategy verbatim "
            "to the reported selector, then re-run the reproduction steps to confirm.\n"
            "CONFIDENCE: high (pattern matched on root cause, not on symptom)."
        )

    @staticmethod
    def _cold_text(prompt: str) -> str:
        return (
            "STRATEGY: Reset the component's local state on every open rather than "
            "initialising it once. Derive the form values from the record passed in, "
            "key the component on the record id so a different record forces a fresh "
            "mount, and clear any module-level draft object in the close handler.\n"
            "CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), "
            "[record.id]); onClose(() => draft.clear())\n"
            "VERIFY: reopen with a second record and assert the fields are empty."
        )


# -------------------------------------------------------------------- Publisher

CITED_HEADER = """# cited.md — RATCHET's verified fix-pattern corpus

Every entry below was written by the agent after a fix was **verified** by QA.
Iteration N is cheaper than N-1 because of the rows on this page.

<!-- machine-readable: each pattern is one `## sig` block with a JSON payload -->
"""


class FixturePublisher:
    """Senso stand-in — appends verified patterns to `cited.md` at repo root."""

    backend = "fixture"
    degraded = False
    degrade_reason: str | None = None

    def __init__(self, path: Path | None = None):
        self._path = path or (REPO_ROOT / "cited.md")

    def publish(self, p: Pattern) -> str:
        try:
            if not self._path.exists():
                self._path.write_text(CITED_HEADER)
            body = self._path.read_text()
            marker = f"<!-- pattern:{p.sig} -->"
            entry = self._render(p, marker)
            if marker in body:
                body = re.sub(
                    rf"{re.escape(marker)}.*?(?=\n<!-- pattern:|\Z)",
                    entry.strip(),
                    body,
                    flags=re.S,
                )
            else:
                body = body.rstrip() + "\n\n" + entry
            self._path.write_text(body)
        except Exception:
            pass  # publishing is never allowed to break the loop
        return f"file://{self._path}#{p.sig}"

    @staticmethod
    def _render(p: Pattern, marker: str) -> str:
        payload = json.dumps({
            "sig": p.sig,
            "bug_class": p.bug_class,
            "strategy": p.strategy,
            "code_hint": p.code_hint,
            "verified": p.verified,
            "uses": p.uses,
            "score": p.score,
        }, indent=2)
        return (
            f"{marker}\n"
            f"## `{p.sig}` — {p.bug_class}\n\n"
            f"**Verified:** {'yes' if p.verified else 'no'} · **Reused:** {p.uses}x\n\n"
            f"{p.strategy}\n\n"
            f"```json\n{payload}\n```\n"
        )


# ----------------------------------------------------------------------- Tracer

class FixtureTracer:
    """Guild stand-in — no-op span that keeps an in-process trace list.

    The trace list is what the slow loop reads to spot deterministic steps, so
    it is recorded even in fixture mode.
    """

    backend = "fixture"
    degraded = False
    degrade_reason: str | None = None

    def __init__(self):
        self.spans: list[dict] = []

    @contextmanager
    def span(self, name: str, **meta):
        started = time.time()
        record = {"name": name, "meta": dict(meta), "ok": True}
        try:
            yield record
        except Exception as e:  # record then re-raise — this is Lane A's error, not ours
            record["ok"] = False
            record["error"] = repr(e)
            raise
        finally:
            record["duration_ms"] = round((time.time() - started) * 1000, 2)
            self.spans.append(record)

    def export(self) -> list[dict]:
        return list(self.spans)
