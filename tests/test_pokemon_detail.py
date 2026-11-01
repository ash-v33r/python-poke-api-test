"""
Test suite for the single-Pokemon endpoint:
    GET https://pokeapi.co/api/v2/pokemon/pikachu

Validates the response body against the JSON Schema in
schemas/pokemon_schema.json using `jsonschema`.
"""

import json
from pathlib import Path

import allure
import jsonschema
import pytest

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "pokemon_schema.json"


@pytest.fixture(scope="module")
def pokemon_schema() -> dict:
    """Load the Pokemon JSON Schema from disk once per module."""
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@allure.feature("Pokemon")
@allure.story("Pokemon detail endpoint (/pokemon/{name})")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("pokeapi", "pikachu", "contract")
@allure.link("https://pokeapi.co/docs/v2", name="PokeAPI v2 documentation")
@allure.description(
    "Fetches /pokemon/pikachu and validates the response body against the "
    "contract defined in schemas/pokemon_schema.json (JSON Schema draft-07)."
)
@pytest.mark.schema
@pytest.mark.regression
@pytest.mark.api
def test_pikachu_response_matches_contract_schema(api_client, pokemon_schema):
    with allure.step("GET /pokemon/pikachu"):
        response = api_client.get_pokemon("pikachu")
        assert response.status_code == 200, (
            f"Expected HTTP 200 but got {response.status_code}: {response.text[:300]}"
        )

    body = response.json()

    with allure.step("Sanity-check known Pikachu identifiers"):
        assert body["name"] == "pikachu"
        assert isinstance(body["id"], int)

    with allure.step("Validate response body against JSON Schema"):
        validator = jsonschema.Draft7Validator(pokemon_schema)
        errors = sorted(validator.iter_errors(body), key=lambda e: list(e.absolute_path))

        if errors:
            failures = "\n".join(
                f"- {'/'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}"
                for err in errors
            )
            allure.attach(failures, name="Schema violations", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(
                f"Response for /pokemon/pikachu violates the schema "
                f"({len(errors)} violation(s)):\n{failures}"
            )


# NOTE: register the 'schema' marker in pytest.ini (already included above).
# Run this suite alone with:  pytest -m schema
