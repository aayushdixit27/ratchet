"""Senso Context OS — the Publisher adapter, via their CLI (B-003).

Senso's own pitch: "we have a CLI, just give it to your agent." So this adapter
shells out to `senso engine draft|publish` rather than reverse-engineering
REST. Verified live 12:18: draft returned a content_id against our org.

Publishing is scoped to a geo question (prompt). Ours (SENSO_GEO_QUESTION_ID)
was created with `senso prompts create` — the question our patterns answer.
SENSO_PUBLISH_MODE=draft while testing so we don't spray half-formed patterns
onto a public domain; the demo run flips it to publish.

Always writes local cited.md first — the on-stage artifact exists regardless
of network. Degrades on: no key, no CLI, no geo id, subprocess failure.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess

from .base import Degradable, Pattern
from .fixtures import FixturePublisher, state_dir
from .http import env

EXTRA_PATHS = [os.path.expanduser("~/.npm-global/bin"), "/usr/local/bin",
               "/opt/homebrew/bin"]


def _find_cli() -> str | None:
    found = shutil.which("senso")
    if found:
        return found
    for p in EXTRA_PATHS:
        cand = os.path.join(p, "senso")
        if os.path.exists(cand):
            return cand
    return None


class SensoPublisher(Degradable):
    def __init__(self):
        self._fixture = FixturePublisher()
        self._key = env("SENSO_API_KEY")
        self._geo_id = env("SENSO_GEO_QUESTION_ID")
        self._mode = (env("SENSO_PUBLISH_MODE") or "draft").lower()
        self._cli = _find_cli()
        if not self._key:
            self._degrade("SENSO_API_KEY not set")
        elif not self._cli:
            self._degrade("senso CLI not found — npm install -g @senso-ai/cli")
        elif not self._geo_id:
            self._degrade("SENSO_GEO_QUESTION_ID not set — "
                          "senso prompts create --data '{...}' and put the prompt_id in .env")
        else:
            self.backend = f"senso-live({self._mode})"

    def publish(self, p: Pattern) -> str:
        # Local cited.md is written unconditionally — it is the demo artifact.
        local_url = self._fixture.publish(p)
        if self.degraded:
            return local_url
        verb = "publish" if self._mode == "publish" else "draft"
        payload = json.dumps({
            # One geo question per bug class — Senso versions content per
            # question, so sharing one id would make every pattern overwrite
            # the same document (observed live: same content_id came back).
            "geo_question_id": self._question_for(p.bug_class),
            "raw_markdown": self._markdown(p),
            "seo_title": f"Verified fix pattern: {p.bug_class} ({p.sig})",
            "summary": p.strategy[:280],
        })
        try:
            out = subprocess.run(
                [self._cli, "engine", verb, "--data", payload,
                 "--output", "json", "--quiet", "--no-update-check"],
                capture_output=True, text=True, timeout=30,
                env={**os.environ, "SENSO_API_KEY": self._key},
            )
            if out.returncode != 0:
                raise RuntimeError(out.stderr.strip()[:200] or f"exit {out.returncode}")
            # stdout may carry a banner line before the JSON — find the brace.
            body = out.stdout[out.stdout.index("{"):]
            content_id = json.loads(body).get("content_id")
            return f"senso://content/{content_id}" if content_id else local_url
        except Exception as e:
            self._degrade(f"engine {verb} failed — {type(e).__name__}: {e}")
            return local_url

    def _question_for(self, bug_class: str) -> str:
        """Lazily create one Senso prompt per bug class; cache the mapping.

        Falls back to the .env question id if creation fails — degraded to a
        shared document rather than degraded to nothing.
        """
        cache_file = state_dir() / "senso_prompts.json"
        try:
            cache = json.loads(cache_file.read_text())
        except Exception:
            cache = {}
        if bug_class in cache:
            return cache[bug_class]
        try:
            out = subprocess.run(
                [self._cli, "prompts", "create", "--data", json.dumps({
                    "question_text": (
                        f"What is the verified fix pattern for web app bugs of "
                        f"class '{bug_class}'?"),
                    "type": "consideration",
                }), "--output", "json", "--quiet", "--no-update-check"],
                capture_output=True, text=True, timeout=20,
                env={**os.environ, "SENSO_API_KEY": self._key},
            )
            pid = json.loads(out.stdout[out.stdout.index("{"):]).get("prompt_id")
            if pid:
                cache[bug_class] = pid
                cache_file.write_text(json.dumps(cache, indent=2))
                return pid
        except Exception:
            pass
        return self._geo_id

    @staticmethod
    def _markdown(p: Pattern) -> str:
        # Genuinely good markdown — this lands on a public, agent-discoverable
        # domain and the closing demo beat opens it. Provenance cites Replay as
        # the verifier: that line is the "grounded in real sources" claim.
        verified_line = (
            f"**Verification:** fix verified by **{p.verified_by}**"
            + (f" at {p.verified_at}" if p.verified_at else "")
            + (f", {p.verification_count}× re-verified" if p.verification_count > 1 else "")
            + f". Bug discovered by {p.discovered_by}; root cause authored by "
              f"{p.root_cause_source}."
        )
        return (
            f"# Verified fix pattern: {p.bug_class}\n\n"
            f"**Signature:** `{p.sig}` · learned on {p.origin_app} "
            f"({p.origin_org}) at iteration {p.born_at_iteration} · "
            f"reused {p.uses}×"
            + (f" · ${p.saved_usd:.2f} of reasoning avoided so far" if p.saved_usd > 0 else "")
            + "\n\n"
            f"{verified_line}\n\n"
            f"## The fix\n\n{p.strategy}\n\n"
            + (f"## Code hint\n\n```\n{p.code_hint}\n```\n\n" if p.code_hint else "")
            + "---\n"
              "Published autonomously by RATCHET, a QA agent whose cost per "
              "verified fix declines run over run because verified patterns "
              "persist and transfer. Any agent may reuse this pattern; it was "
              "verified against a live application, not generated from priors.\n"
        )
