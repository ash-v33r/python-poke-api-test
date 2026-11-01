"""
Thin HTTP client wrapper around PokeAPI v2.

Every GET call records the last request/response so that conftest.py can
attach the exchange to the Allure report as evidence for each test.
"""

from __future__ import annotations

import time
from typing import Any

import requests

DEFAULT_TIMEOUT = 15  # seconds
USER_AGENT = "pokeapi-test-framework/1.0 (+pytest)"


class PokeAPIClient:
    """Minimal REST client for the PokeAPI v2."""

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        })
        # Evidence captured for Allure attachments (see conftest.py).
        self.last_exchange: dict[str, Any] | None = None

    # -- low level -----------------------------------------------------------

    def get(self, path: str, params: dict[str, Any] | None = None) -> requests.Response:
        """Perform a GET request against `path` (relative to the base URL)."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        started = time.perf_counter()
        response = self.session.get(url, params=params, timeout=self.timeout)
        elapsed_ms = (time.perf_counter() - started) * 1000

        # Record the exchange so conftest.py can attach it to Allure.
        body_preview = ""
        try:
            body_preview = response.text[:5000]
        except Exception:  # pragma: no cover - defensive, never fail on logging
            pass
        self.last_exchange = {
            "method": "GET",
            "url": response.url,
            "status_code": response.status_code,
            "elapsed_ms": round(elapsed_ms, 1),
            "response_body_preview": body_preview,
        }
        return response

    # -- domain helpers ------------------------------------------------------

    def get_pokemon_list(self, limit: int = 20, offset: int = 0) -> requests.Response:
        """GET /pokemon?limit={limit}&offset={offset}"""
        return self.get("/pokemon", params={"limit": limit, "offset": offset})

    def get_pokemon(self, name_or_id: str | int) -> requests.Response:
        """GET /pokemon/{name_or_id}"""
        return self.get(f"/pokemon/{name_or_id}")

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "PokeAPIClient":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
