"""
Shared fixtures and Allure evidence plumbing.

- `api_client`     : session-scoped PokeAPIClient (connection reuse).
- `_api_evidence`  : autouse fixture that attaches the last HTTP exchange
                     of every test to the Allure report.
- BASE URL override: set POKEAPI_BASE_URL env var (useful for mocks/proxies).
"""

from __future__ import annotations

import json
import os

import allure
import pytest

from api.client import PokeAPIClient

BASE_URL = os.getenv("POKEAPI_BASE_URL", "https://pokeapi.co/api/v2")


@pytest.fixture(scope="session")
def api_client() -> PokeAPIClient:
    """Session-scoped HTTP client so connections are reused across tests."""
    client = PokeAPIClient(BASE_URL)
    yield client
    client.close()


@pytest.fixture(autouse=True)
def _api_evidence(request: pytest.FixtureRequest) -> None:
    """
    Attach the last HTTP exchange performed during the test to the Allure
    report, so every result carries request/response evidence.
    """
    yield
    if "api_client" not in request.fixturenames:
        return
    client: PokeAPIClient = request.getfixturevalue("api_client")
    if client.last_exchange is None:
        return
    evidence = dict(client.last_exchange)
    body = evidence.pop("response_body_preview", "")
    allure.attach(
        json.dumps(evidence, indent=2),
        name="HTTP exchange (meta)",
        attachment_type=allure.attachment_type.JSON,
    )
    if body:
        allure.attach(
            body,
            name="Response body (preview)",
            attachment_type=allure.attachment_type.JSON,
        )
