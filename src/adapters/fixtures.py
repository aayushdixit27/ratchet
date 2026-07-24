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

def _bugs_from_json(data: dict, source: str) -> list[Bug]:
    """Load Lane C's canonical `app/bugs.json`.

    Schema (theirs, v1): each bug has id, class, severity, selectors[], symptom,
    repro[], root_cause, fix_strategy, file, symbol. Everything beyond the
    contract's fields is preserved in `Bug.raw` — Lane A gets `fix_strategy`
    and `severity` for free, and nothing is lost in translation.

    `root_cause` is copied verbatim: it is the semantic key the whole retrieval
    thesis rests on.
    """
    out: list[Bug] = []
    for b in data.get("bugs", []):
        selectors = b.get("selectors") or ([b["selector"]] if b.get("selector") else [])
        symptom = b.get("symptom") or b.get("title") or b.get("id", "")
        out.append(Bug(
            id=b["id"],
            # first sentence of the symptom reads as a title without duplicating it
            title=symptom.split(". ")[0].strip().rstrip(".") or b["id"],
            root_cause=b["root_cause"],
            selector=selectors[0] if selectors else None,
            repro=list(b.get("repro", [])),
            bug_class=b.get("class") or b.get("bug_class") or "unclassified",
            raw={**b, "source": source, "selectors": selectors},
        ))
    return out


def _looks_usable(bugs: list[Bug]) -> bool:
    """Reject a parse that produced structurally wrong data.

    Learned the hard way: a lenient loader that returns three garbage rows is
    worse than one that falls back to the seed, because the loop runs happily
    on nonsense and nobody notices until the demo.
    """
    if len(bugs) < 3:
        return False
    if any(not b.id or not b.root_cause for b in bugs):
        return False
    if sum(1 for b in bugs if b.bug_class == "unclassified") > len(bugs) // 2:
        return False
    from collections import Counter
    # the whole demo needs at least one class with repeats
    return Counter(b.bug_class for b in bugs).most_common(1)[0][1] >= 2


class FixtureQA:
    """Replay QA stand-in.

    Reads Lane C's canonical `app/bugs.json` if present, otherwise the local
    seed. Either way: 8 bugs, 3 of which share one class — that shared class is
    what makes memory retention visible by iteration 3.
    """

    backend = "fixture"
    degraded = False
    degrade_reason: str | None = None

    def __init__(self, bugs_json: Path | None = None, seed: Path | None = None):
        # Lane C owns app/bugs.json and declares it the machine-readable ground
        # truth; prefer it, and keep our own seed purely as an offline backstop
        # for when app/ is missing.
        self._bugs_json = bugs_json or (REPO_ROOT / "app" / "bugs.json")
        self._seed = seed or (SEED_DIR / "bugs.json")
        self._ledger = state_dir() / "patches.json"
        self.source = "unloaded"

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
        if self._bugs_json.exists():
            try:
                parsed = _bugs_from_json(
                    json.loads(self._bugs_json.read_text()), "app/bugs.json")
                if _looks_usable(parsed):
                    self.source = "app/bugs.json"
                    return parsed
            except Exception:
                pass  # fall through to the seed — never crash the loop
        self.source = "seed"
        return _bugs_from_json(json.loads(self._seed.read_text()), "seed")


# ----------------------------------------------------------------------- Memory

def _similarity(a: str, b: str) -> float:
    """Cosine over the same vectors Actian indexes.

    Deliberately identical to the live path: FixtureMemory and ActianMemory
    must score the same pair the same way, or Lane A's retrieval threshold
    would silently mean two different things in fixture vs live mode — and we
    would only find out on stage.
    """
    from .embed import cosine, embed
    return round(max(0.0, cosine(embed(a), embed(b))), 4)


class FixtureMemory:
    """Actian VectorAI stand-in — same embedding + cosine, JSON-backed.

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
