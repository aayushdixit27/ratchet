"""Pioneer (Fastino Labs) — the Router adapter.

Pioneer is an OpenAI-compatible inference API with an adaptive model router
that gets cheaper as it sees your traffic. That router is why this is adapter
#1: the cost numbers it returns are the number that drops on stage.

Degrades to FixtureRouter on a missing key, a network failure, or a malformed
response. Never raises.
"""

from __future__ import annotations

import os
from typing import Literal

from .base import Degradable, usage
from .fixtures import FixtureRouter
from .http import env, request_json

DEFAULT_BASE = "https://api.pioneer.ai/v1"

# Published $/1M tokens (input, output). Used only when the API does not return
# a cost itself — Pioneer's adaptive routing can beat these, so a returned cost
# always wins.
PRICE_BOOK: dict[str, tuple[float, float]] = {
    "gemma": (0.25, 0.25),
    "gemma-4-12b-it": (0.25, 0.25),
    "qwen3-32b": (0.90, 0.90),
    "gliner2-large": (0.20, 0.20),
    "nemotron-3-ultra": (0.50, 2.50),
    "claude-sonnet-5": (2.00, 10.00),
    "gpt-5.5": (5.00, 30.00),
}
FALLBACK_PRICE = (1.00, 3.00)


def _price_for(model: str) -> tuple[float, float]:
    key = (model or "").lower()
    if key in PRICE_BOOK:
        return PRICE_BOOK[key]
    for name, price in PRICE_BOOK.items():          # prefix/suffix tolerant
        if name in key or key in name:
            return price
    return FALLBACK_PRICE


class PioneerRouter(Degradable):
    """Two tiers over one OpenAI-compatible endpoint.

    `cheap` is the warm path — a small, adaptively-routed model reusing a
    retrieved fix-pattern. `strong` is the cold path — a frontier model doing
    full root-cause reasoning. The whole thesis is that the warm/cold mix
    shifts toward warm as memory fills, so the two tiers must be genuinely
    different models, not the same model with different prompts.
    """

    def __init__(self):
        self._fixture = FixtureRouter()
        self._base = (env("PIONEER_BASE_URL") or DEFAULT_BASE).rstrip("/")
        self._key = env("PIONEER_API_KEY")
        # Model IDs are namespaced (e.g. "fastino/gliner2-base-v1"). There are
        # no safe defaults — list them with
        #   curl -H "X-API-Key: $PIONEER_API_KEY" https://api.pioneer.ai/v1/models
        # and set both in .env.
        self._cheap = env("PIONEER_CHEAP_MODEL")
        self._strong = env("PIONEER_STRONG_MODEL")
        if not self._key:
            self._degrade("PIONEER_API_KEY not set")
        elif not self._cheap or not self._strong:
            self._degrade("PIONEER_CHEAP_MODEL / PIONEER_STRONG_MODEL not set — "
                          "curl /v1/models with your key and put two real IDs in .env")
        elif self._cheap == self._strong:
            # The one place a wrong config silently produces a lying chart:
            # if warm and cold hit the same model, the cost story is fake.
            self._degrade(f"cheap and strong both resolve to '{self._cheap}' — "
                          "the warm/cold cost gap would be fabricated; refusing")
        else:
            self.backend = "pioneer-live"

    def complete(self, prompt: str, tier: Literal["cheap", "strong"]) -> tuple[str, dict]:
        if self.degraded:
            text, u = self._fixture.complete(prompt, tier)
            u["degraded"] = True
            u["degrade_reason"] = self.degrade_reason
            return text, u

        model = self._cheap if tier == "cheap" else self._strong
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": int(os.getenv("PIONEER_MAX_TOKENS", "1200")),
        }
        try:
            body = self._post(payload)
            return self._parse(body, model, tier)
        except Exception as e:
            self._degrade(f"{type(e).__name__}: {e}")
            text, u = self._fixture.complete(prompt, tier)
            u["degraded"] = True
            u["degrade_reason"] = self.degrade_reason
            return text, u

    # -- internals ---------------------------------------------------------
    def _post(self, payload: dict) -> dict:
        """POST with self-healing auth: console says Bearer, docs say
        X-API-Key (they disagree — observed 12:34). Try Bearer first; on a
        401/403 retry once with the other header before giving up."""
        from .http import HttpError
        url = f"{self._base}/chat/completions"
        try:
            return request_json(url, method="POST", payload=payload,
                                headers={"Authorization": f"Bearer {self._key}"})
        except HttpError as e:
            if e.status not in (401, 403):
                raise
            return request_json(url, method="POST", payload=payload,
                                headers={"X-API-Key": self._key})

    def _parse(self, body: dict, requested_model: str, tier: str) -> tuple[str, dict]:
        choices = body.get("choices") or []
        if not choices:
            raise ValueError(f"no choices in response: {str(body)[:200]}")
        text = (choices[0].get("message") or {}).get("content") or ""

        u = body.get("usage") or {}
        ptok = int(u.get("prompt_tokens") or u.get("input_tokens") or 0)
        ctok = int(u.get("completion_tokens") or u.get("output_tokens") or 0)
        # The router may serve a different (cheaper) model than we asked for —
        # report what actually ran, that's the interesting number.
        served = body.get("model") or requested_model

        cost = u.get("cost") or u.get("total_cost") or body.get("cost")
        if cost is None:
            pin, pout = _price_for(served)
            cost = (ptok * pin + ctok * pout) / 1_000_000
            cost_source = "price_book"
        else:
            cost = float(cost)
            cost_source = "api"

        return text, usage(
            calls=1,
            cost_usd=float(cost),
            tier=tier,
            model=served,
            prompt_tokens=ptok,
            completion_tokens=ctok,
            backend="pioneer-live",
            requested_model=requested_model,
            routed=served != requested_model,
            cost_source=cost_source,
        )
