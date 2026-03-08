# Testing Guide

This document describes the testing mechanisms used in this project.

## Overview

The project has four testing layers:

| Layer | Tool | Purpose | When to Run |
|-------|------|---------|-------------|
| **Lint** | ruff, codespell | Code style and spelling | Pre-commit hook, CI |
| **Unit Test** | pytest | Individual skill code correctness | Pre-push hook, CI |
| **Integration Test** | skill-integration-tester | Multi-skill workflow handoff validation | After adding/modifying workflows |
| **Quality Review** | dual-axis-skill-reviewer | Skill structure and quality scoring | Daily automation, manual |
| **Security** | bandit, detect-secrets | SAST and secret detection | CI |

---

## 1. Lint

**Pre-commit hooks** run automatically on `git commit`:

```bash
# Install hooks (one-time setup)
pre-commit install && pre-commit install --hook-type pre-push

# Manual lint
uv run ruff check skills/ scripts/
uv run ruff format skills/ scripts/
uv run codespell --toml pyproject.toml skills/ scripts/
```

Checks: trailing whitespace, end-of-file, YAML/TOML validation, ruff lint + format, codespell.

---

## 2. Unit Tests (pytest)

Each skill with scripts has its own test suite under `skills/<skill-name>/scripts/tests/`.

### Running Tests

```bash
# All skills (isolated per-skill invocations)
bash scripts/run_all_tests.sh

# Single skill
uv run --extra dev pytest skills/<skill-name>/scripts/tests/ -v

# Repo-level tests (orchestrator, pipeline, etc.)
uv run --extra dev pytest scripts/tests/ -v
```

### Module Isolation (Critical)

Multiple skills share identical filenames (`scorer.py`, `calculators/`, `helpers.py`, `fmp_client.py`). To avoid import collisions:

- **Never** run `pytest` from the repo root across all skills at once.
- Use `scripts/run_all_tests.sh` which runs separate pytest invocations per skill.
- `pyproject.toml` uses `--import-mode=importlib` to mitigate collisions, but isolated runs are still the primary mechanism.

### Known Skip List

Defined in `scripts/run_all_tests.sh`:

| Skill | Reason |
|-------|--------|
| `theme-detector` | 27 pre-existing failures |
| `canslim-screener` | Requires `bs4` (not in dev extras) |

These are excluded from the pre-push gate. In CI, `theme-detector` runs with `continue-on-error: true`.

### Test Paths Registered in pyproject.toml

The `[tool.pytest.ini_options]` `testpaths` list defines which skill test directories are discovered. When adding a new skill with tests, register its test path there.

### Pre-push Hook

`scripts/run_all_tests.sh` runs automatically on `git push` via the pre-push hook. A push is blocked if any non-skipped test fails.

---

## 3. Integration Tests (skill-integration-tester)

Located at `skills/skill-integration-tester/`. Validates multi-skill workflows defined in the CLAUDE.md "Multi-Skill Workflows" section.

### What It Validates

| Check | Description |
|-------|-------------|
| Skill existence | Each workflow step's skill directory exists under `skills/` |
| Data contracts | JSON output fields of step N match the input parameters of step N+1 |
| Handoff mechanism | CLI parameters (`--candidates-json`, `--hints`, etc.) are compatible |
| File naming | Output filenames follow the `<prefix>_YYYY-MM-DD_HHMMSS.{json,md}` convention |

### Running

```bash
# Validate all workflows
python3 skills/skill-integration-tester/scripts/test_workflows.py \
  --output-dir reports/

# Validate a specific workflow
python3 skills/skill-integration-tester/scripts/test_workflows.py \
  --workflow "Earnings Momentum" \
  --output-dir reports/

# Dry-run with synthetic fixtures (no real data needed)
python3 skills/skill-integration-tester/scripts/test_workflows.py \
  --dry-run \
  --output-dir reports/
```

### Key Properties

- **No API keys required** -- all validation is local and offline
- **Non-destructive** -- reads SKILL.md and CLAUDE.md only, never modifies files
- **Deterministic** -- same inputs always produce same results

### Contract Definitions

Known handoff contracts are defined in:
- `references/workflow_contracts.md` -- human-readable documentation
- `SKILL_CONTRACTS` and `HANDOFF_CONTRACTS` dicts in `scripts/test_workflows.py` -- machine-readable

### Output

Reports are saved to `reports/`:
- `integration_test_YYYY-MM-DD_HHMMSS.json` -- structured results
- `integration_test_YYYY-MM-DD_HHMMSS.md` -- human-readable summary

Each workflow shows: step existence checks, handoff status (PASS/FAIL/N/A), naming violations, and overall status (valid/broken/warning).

### Integration Test's Own Tests

```bash
uv run --extra dev pytest skills/skill-integration-tester/scripts/tests/ -v
```

---

## 4. Quality Review (dual-axis-skill-reviewer)

Scores skill quality on two axes:
1. **Auto axis (deterministic)** -- structure, scripts, tests, execution safety
2. **LLM axis (optional)** -- deep content review via Claude

### Running

```bash
# Score a specific skill
uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
  --project-root . --skill backtest-expert --output-dir reports/

# Score all skills
uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
  --project-root . --all --output-dir reports/

# Score a random skill (used by automation)
uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
  --project-root . --output-dir reports/
```

### Automated Improvement Loop

`scripts/run_skill_improvement_loop.py` runs daily (via launchd at 05:00):
1. Selects a skill (round-robin)
2. Scores it with the reviewer
3. If below threshold, invokes Claude CLI for improvement
4. Re-scores after improvement; rolls back if score didn't improve
5. Creates a PR if improvements pass

```bash
# Dry-run (score only, no improvements)
python3 scripts/run_skill_improvement_loop.py --dry-run

# Dry-run all skills
python3 scripts/run_skill_improvement_loop.py --dry-run --all

# Full run
python3 scripts/run_skill_improvement_loop.py
```

---

## 5. Security Scanning

### Bandit (SAST)

```bash
uv run bandit -c pyproject.toml -r skills/ --exclude "*/tests/*"
```

Scans Python code for common security issues. Configuration in `pyproject.toml` under `[tool.bandit]`.

### detect-secrets

```bash
# Generate a fresh scan and compare against baseline
detect-secrets scan \
  --exclude-files '\.env$|\.json$|\.csv$|\.md$|\.zip$|\.baseline$' \
  > /tmp/new_scan.json
```

Committed baseline: `.secrets.baseline`. CI fails if new secrets are found that aren't in the baseline.

---

## 6. CI Pipeline (.github/workflows/ci.yml)

Runs on PRs to `main` and pushes to `main`. Three parallel jobs:

```
┌─────────┐  ┌──────────┐  ┌──────────┐
│  Lint   │  │   Test   │  │ Security │
│         │  │          │  │          │
│ ruff    │  │ pytest   │  │ bandit   │
│ codespell│ │ per-skill│  │ detect-  │
│         │  │ coverage │  │ secrets  │
└─────────┘  └──────────┘  └──────────┘
```

- **Lint**: ruff check, ruff format --check, codespell
- **Test**: per-skill pytest with `--cov`, Python 3.9, coverage summary at end
- **Security**: bandit SAST, detect-secrets baseline comparison

---

## Adding Tests for a New Skill

1. Create `skills/<skill-name>/scripts/tests/` directory
2. Add `conftest.py` with necessary fixtures (see existing skills for examples)
3. Add `test_*.py` files
4. Register the test path in `pyproject.toml` under `[tool.pytest.ini_options]` `testpaths`
5. Add a `Test <skill-name>` step in `.github/workflows/ci.yml`
6. Verify with: `uv run --extra dev pytest skills/<skill-name>/scripts/tests/ -v`
7. If the skill has inter-skill data contracts, add entries to `SKILL_CONTRACTS` and `HANDOFF_CONTRACTS` in `skills/skill-integration-tester/scripts/test_workflows.py`

---

## Quick Reference

```bash
# Full local validation (lint + test + security)
uv run ruff check skills/ scripts/ && \
uv run ruff format --check skills/ scripts/ && \
uv run codespell --toml pyproject.toml skills/ scripts/ && \
bash scripts/run_all_tests.sh && \
uv run bandit -c pyproject.toml -r skills/ --exclude "*/tests/*"
```
