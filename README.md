# PokeAPI Test Automation Framework

 pytest + requests + jsonschema framework exercising PokeAPI v2
 (https://pokeapi.co/docs/v2), with Allure Report v3 for reporting
 (https://allurereport.org/docs/v3/).

 ## Prerequisites
 - Python 3.10+
 - astral-uv:
       Installation:  https://docs.astral.sh/uv/getting-started/installation/
 - The Allure Report CLI (requires Java):
       macOS:   brew install allure
       Windows: scoop install allure   (or npm i -g allure-commandline)
       Linux:   see https://allurereport.org/docs/install/

 ## Setup
 ```bash
 uv sync
 ```

 Optional: point the suite at another environment
 ```bash
 export POKEAPI_BASE_URL=https://pokeapi.co/api/v2
 ```

 ## Running tests by tag (pytest markers)
 ```bash
 uv run pytest -m smoke        # critical sanity checks only
 uv run pytest -m schema       # JSON-schema / contract validation only
 uv run pytest -m regression   # full regression suite
 ```

 ## Running tests with Allure v3 reporting
 Per the Allure docs, the `allure-pytest` plugin writes raw results to a
 directory via `--alluredir`; the Allure CLI (v3) then renders them:
 ```bash
 # 1. Run tests, writing Allure results (clean old results first)
 uv run pytest --alluredir=./allure-results --clean-alluredir
 allure serve ./allure-results

 # 2b. Or: generate to a fixed folder, then open it
 allure generate ./allure-results -o ./allure-report --clean
 allure open ./allure-report
 ```

 Every test automatically attaches its HTTP exchange (URL, status code,
 latency, response-body preview) and any schema violations to the report.-->

 ## Project layout:
```
   pokeapi-tests/
   ├── pyproject.toml
   ├── conftest.py
   ├── uv.lock
   ├── api/
   │   ├── __init__.py
   │   └── client.py
   ├── schemas/
   │   └── pokemon_schema.json
   ├── tests/
   │   ├── __init__.py
   │   ├── test_pokemon_list.py
   │   └── test_pokemon_detail.py
   └── README.md
```
