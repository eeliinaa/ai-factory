# AI Product Factory

Lean AI-assisted system for turning a high-level topic into an Etsy-ready digital product draft package.

## Status
MVP pipeline with batch runs, run history, comparison views, refinement tracking, and packaging outputs.

## What it does
The pipeline can:
- load topic + context,
- research and evaluate candidate opportunities,
- select one viable direction,
- create a structured product draft,
- run QA,
- attempt refinement after QA failures,
- package outputs,
- prepare listing materials.

## Project structure
- `src/ai_product_factory/` — application package
- `config/` — app configuration files
- `data/sqlite/` — SQLite database files
- `data/runs/` — generated run outputs
- `tests/` — test suite

## Requirements
- Python 3.11+
- Optional: OpenAI API key for live mode
- Git (recommended)

## Manual setup on macOS / Linux
1. Open Terminal.
2. Go to the project folder:
   - `cd /path/to/ISO/mix/context/ai-project-factory`
3. Create a virtual environment:
   - `python3 -m venv .venv`
4. Activate it:
   - `source .venv/bin/activate`
5. Install the project:
   - `python -m pip install --upgrade pip`
   - `pip install -e .[dev]`

## Manual setup on Windows (PowerShell)
1. Open PowerShell.
2. Go to the project folder:
   - `cd C:\path\to\ISO\mix\context\ai-project-factory`
3. Create a virtual environment:
   - `py -3 -m venv .venv`
4. Activate it:
   - `.\.venv\Scripts\Activate.ps1`
5. Install the project:
   - `python -m pip install --upgrade pip`
   - `pip install -e .[dev]`

## Environment variables
For placeholder mode, no API key is required if placeholder fallback is enabled.

For live mode, set your OpenAI API key.

macOS / Linux:
- `export OPENAI_API_KEY="your_key_here"`

Windows PowerShell:
- `$env:OPENAI_API_KEY="your_key_here"`

## Quickstart
Run from inside `mix/context/ai-project-factory`.

1. Run a single topic in placeholder mode:
   - `python -m ai_product_factory.main --topic "etsy planners" --placeholder`
2. Run multiple topics:
   - `python -m ai_product_factory.main --topic "etsy planners" --topic "wedding checklists" --placeholder`
3. Run from a file:
   - `python -m ai_product_factory.main --topic-file topics.txt --placeholder`
4. Run in live mode:
   - `python -m ai_product_factory.main --topic "etsy planners" --live`

## History and comparison
- List runs:
  - `python -m ai_product_factory.main --list-runs`
- Show a run:
  - `python -m ai_product_factory.main --run-id <run_id>`
- Compare runs:
  - `python -m ai_product_factory.main --compare-run <run_id> --compare-run <run_id>`
- Show best runs:
  - `python -m ai_product_factory.main --best-runs --sort-by score`

## Modes
- `--placeholder` — allow placeholder fallback mode
- `--live` — force live model mode
- `--allow-placeholder-fallback true|false` — backward-compatible override

## Developer workflow
- Install dev dependencies:
  - `pip install -e .[dev]`
- Run tests:
  - `pytest`
- Run lint:
  - `ruff check src tests`
- Run compile check:
  - `python -m compileall src`
- CI runs on every push and pull request via `.github/workflows/ci.yml`

## Outputs
Each run writes outputs under the configured runs directory, including:
- generated artifacts
- `run-report.json`
- `manifest.json`
- `package-ready/PACKAGE_SUMMARY.md`
- optional `batch-summary.json`

## Context documents
See:
- `../AI_PRODUCT_FACTORY_PROJECT_SPEC.md`
- `../IMPLEMENTATION_PLAN.md`
- `../crew-ai-context`
