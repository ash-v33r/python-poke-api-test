"""
Test suite for the paginated Pokemon list endpoint:
    GET https://pokeapi.co/api/v2/pokemon?limit=1
"""

import allure
import pytest

MIN_EXPECTED_POKEMON = 1350
LIST_LIMIT = 1


@allure.feature("Pokemon")
@allure.story("Pokemon list endpoint (/pokemon)")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("pokeapi", "pokemon-list")
@allure.link("https://pokeapi.co/docs/v2", name="PokeAPI v2 documentation")
@allure.description(
    "Calls GET /pokemon?limit=1 and verifies that the API responds with "
    f"HTTP 200 and reports a total Pokemon count of at least {MIN_EXPECTED_POKEMON}."
)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.api
def test_pokemon_list_returns_http_200_and_at_least_1350_pokemon(api_client):
    with allure.step(f"GET /pokemon?limit={LIST_LIMIT}"):
        response = api_client.get_pokemon_list(limit=LIST_LIMIT)
        assert response.status_code == 200, (
            f"Expected HTTP 200 but got {response.status_code}: {response.text[:300]}"
        )

    body = response.json()

    with allure.step(f"Assert reported total count is >= {MIN_EXPECTED_POKEMON}"):
        assert "count" in body, "'count' key missing from response payload"
        actual_count = body["count"]
        assert actual_count >= MIN_EXPECTED_POKEMON, (
            f"Expected at least {MIN_EXPECTED_POKEMON} Pokemon, "
            f"but API reports only {actual_count}"
        )

    with allure.step(f"Assert pagination honoured (limit={LIST_LIMIT})"):
        results = body.get("results", [])
        assert len(results) == LIST_LIMIT, (
            f"Expected {LIST_LIMIT} result(s) but received {len(results)}"
        )
        for entry in results:
            assert {"name", "url"} <= set(entry.keys()), (
                f"List entry is missing required keys: {entry}"
            )


# NOTE: register the extra 'api' marker used above in pytest.ini, e.g.:
#     api: plain API behaviour tests (no schema validation)
