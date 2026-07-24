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
        # Budget guard (B-010): auto-recharge exists on this account, so a
        # runaway loop against real inference can charge a card. Hard-cap live
        # calls per process; past the cap we degrade to fixture, loudly.
        self._max_calls = int(os.getenv("PIONEER_MAX_CALLS", "400"))
        self._max_spend = float(os.getenv("PIONEER_MAX_SPEND_USD", "5.0"))
        self._calls_made = 0
        self.spent_usd = 0.0
        self._live_prices: dict[str, tuple[float, float]] = {}
        if not self.degraded:
            self._load_prices()

    def _load_prices(self) -> None:
        """Price book from their live /v1/models — exact cost for whatever
        model the router resolves to, instead of a stale hand-copied table."""
        try:
            body = request_json(f"{self._base}/models",
                                headers={"Authorization": f"Bearer {self._key}"})
            for m in body.get("data", []):
                pin = m.get("input_price_per_million")
                pout = m.get("output_price_per_million")
                if m.get("id") and pin is not None and pout is not None:
                    self._live_prices[m["id"].lower()] = (float(pin), float(pout))
        except Exception:
            pass  # static book still covers the common models

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
        # Budget guard. Dollar cap is primary (that's what the card feels);
        # call cap is the belt-and-braces backstop. Tripping mid-run mixes
        # fixture and live prices into one curve — a lying chart — so the cap
        # exists to be high enough to never trip on a planned run, and the
        # degrade_reason makes any trip impossible to miss in the JSONL.
        if self.spent_usd >= self._max_spend or self._calls_made >= self._max_calls:
            text, u = self._fixture.complete(prompt, tier)
            u["degraded"] = True
            u["degrade_reason"] = (f"budget cap: spent ${self.spent_usd:.4f}/"
                                   f"{self._max_spend}, calls {self._calls_made}/"
                                   f"{self._max_calls}")
            return text, u
        # Transient failures (429s, timeouts when auto routes the warm prompt
        # to an opus-class model whose 1200-token generation outlives a short
        # socket timeout) must cost ONE call, not the rest of the run — a
        # permanent flip mid-run stitches fixture prices onto live ones and
        # the curve lies. So: up to 4 attempts with 1/2/4/8s backoff, all
        # inside ONE hard wall-clock deadline (PIONEER_DEADLINE_S, default
        # 90s — a hang during the live demo beat is unrecoverable, so the
        # deadline is per completion, not per attempt). Past the deadline we
        # fixture-price this call, flagged degraded, and degrade permanently
        # only after 3 consecutive failures.
        import time as _t
        deadline = float(os.getenv("PIONEER_DEADLINE_S", "90"))
        t0 = _t.monotonic()
        last_err: Exception | None = None
        for attempt in range(4):
            remaining = deadline - (_t.monotonic() - t0)
            if remaining <= 0:
                break
            try:
                body = self._post(payload, timeout=remaining)
                self._calls_made += 1
                self._consec_failures = 0
                return self._parse(body, model, tier)
            except Exception as e:
                last_err = e
                backoff = 1.0 * 2 ** attempt   # 1, 2, 4, 8s
                if (_t.monotonic() - t0) + backoff >= deadline:
                    break
                _t.sleep(backoff)
        self._consec_failures = getattr(self, "_consec_failures", 0) + 1
        if self._consec_failures >= 3:
            self._degrade(f"3 consecutive failures, last: "
                          f"{type(last_err).__name__}: {last_err}")
        self._log_router_error(tier, model, last_err)
        text, u = self._fixture.complete(prompt, tier)
        u["degraded"] = True
        u["requested_model"] = model
        u["degrade_reason"] = (f"transient ({self._consec_failures} consec): "
                               f"{type(last_err).__name__}: {str(last_err)[:160]}")
        return text, u

    def _log_router_error(self, tier: str, model: str, err: Exception | None) -> None:
        """Every fixture fallback appends WHY to runs/router_errors.jsonl.
        The run JSONL drops the usage-dict degrade_reason today, so without
        this line a fixture-priced row is undiagnosable after the fact."""
        try:
            import datetime
            import json as _json
            import pathlib
            path = pathlib.Path(__file__).resolve().parents[2] / "runs" / "router_errors.jsonl"
            with open(path, "a") as f:
                f.write(_json.dumps({
                    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "tier": tier,
                    "requested_model": model,
                    "consec_failures": self._consec_failures,
                    "error": f"{type(err).__name__}: {str(err)[:300]}" if err else None,
                }) + "\n")
        except Exception:
            pass  # diagnostics must never take down the call path

    # -- internals ---------------------------------------------------------
    def _post(self, payload: dict, timeout: float | None = None) -> dict:
        """POST with self-healing auth: console says Bearer, docs say
        X-API-Key (they disagree — observed 12:34). Try Bearer first; on a
        401/403 retry once with the other header before giving up."""
        from .http import HttpError
        url = f"{self._base}/chat/completions"
        # Inference outlives the 20s default when auto routes to an opus-class
        # model: give completions their own ceiling, further clamped to the
        # caller's remaining deadline budget.
        timeout = min(float(os.getenv("PIONEER_TIMEOUT", "75")), timeout or 75.0)
        try:
            return request_json(url, method="POST", payload=payload,
                                timeout=timeout,
                                headers={"Authorization": f"Bearer {self._key}"})
        except HttpError as e:
            if e.status not in (401, 403):
                raise
            return request_json(url, method="POST", payload=payload,
                                timeout=timeout,
                                headers={"X-API-Key": self._key})

    def _parse(self, body: dict, requested_model: str, tier: str) -> tuple[str, dict]:
        choices = body.get("choices") or []
        if not choices:
            raise ValueError(f"no choices in response: {str(body)[:200]}")
        text = (choices[0].get("message") or {}).get("content") or ""

        u = body.get("usage") or {}
        ptok = int(u.get("prompt_tokens") or u.get("input_tokens") or 0)
        ctok = int(u.get("completion_tokens") or u.get("output_tokens") or 0)

        # x_pioneer: their router's own telemetry — routed model, the baseline
        # it avoided, and the rate difference. This is a sponsor's API
        # validating our cost claim; inference_id is the audit trail.
        xp = body.get("x_pioneer") or {}
        savings = xp.get("savings") or {}
        rate_diff = savings.get("rate_diff_per_mtok") or {}
        served = (xp.get("routed_model") or body.get("model") or requested_model)

        cost = u.get("cost") or u.get("total_cost") or body.get("cost")
        if cost is None:
            pin, pout = self._live_prices.get(served.lower()) or _price_for(served)
            cost = (ptok * pin + ctok * pout) / 1_000_000
            cost_source = "live_price_book" if served.lower() in self._live_prices else "static_price_book"
        else:
            cost = float(cost)
            cost_source = "api"
        self.spent_usd += float(cost)

        # Pioneer's saving on THIS call: rate difference × actual tokens.
        # Kept separate from calls_eliminated_saved_usd (Lane A computes that
        # from warm hits) — the two savings stack, they don't compete.
        router_saved_usd = round(
            (ptok * float(rate_diff.get("input") or 0)
             + ctok * float(rate_diff.get("output") or 0)) / 1_000_000, 6)

        return text, usage(
            calls=1,
            cost_usd=float(cost),
            tier=tier,
            model=served,                       # what ACTUALLY ran (B-010 #2)
            prompt_tokens=ptok,
            completion_tokens=ctok,
            backend="pioneer-live",
            requested_model=requested_model,
            routed=served != requested_model,
            cost_source=cost_source,
            # A-003 names these fields verbatim — keep both spellings so Lane A
            # reads them without guessing ('model' stays the canonical one).
            routed_model=served,
            inference_id=xp.get("inference_id"),
            baseline_model=savings.get("baseline_model"),
            rate_diff_per_mtok=rate_diff or None,
            router_saved_usd=router_saved_usd,
            spent_usd_running=round(self.spent_usd, 6),
        )
