# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains Claude Skills for equity investors and traders. Each skill packages domain-specific prompts, knowledge bases, and helper scripts to assist with market analysis, technical charting, economic calendar monitoring, and trading strategy development. Skills are designed to work in both Claude's web app and Claude Code environments.

⚠️ **Important:** Some skills require paid API subscriptions (FMP API and/or FINVIZ Elite) to function. See the [API Key Management](#api-key-management) section for detailed requirements by skill.

## Development Commands

**Package manager:** `uv` (with `pyproject.toml`; scripts-only project, not an installable package)

```bash
# Install dependencies
uv sync --extra dev

# Lint and format
uv run ruff check skills/ scripts/
uv run ruff format skills/ scripts/
uv run codespell --toml pyproject.toml skills/ scripts/

# Run ALL tests (per-skill isolation — see Module Isolation below)
bash scripts/run_all_tests.sh

# Run a single skill's tests
uv run --extra dev pytest skills/<skill-name>/scripts/tests/ -v

# Run repo-level tests (orchestrator, etc.)
uv run --extra dev pytest scripts/tests/ -v

# Security scan
uv run bandit -c pyproject.toml -r skills/ --exclude "*/tests/*"

# Set up pre-commit and pre-push hooks
pre-commit install && pre-commit install --hook-type pre-push
```

**Pre-commit hooks:** trailing-whitespace, end-of-file, YAML/TOML check, ruff lint+format, codespell, detect-secrets.
**Pre-push hook:** runs `scripts/run_all_tests.sh` (all skill tests).

### Module Isolation (Critical)

Multiple skills have identically-named files (`scorer.py`, `calculators/`, `helpers.py`, `fmp_client.py`). Tests **must** run per-skill in separate pytest invocations to avoid import collisions. Never run `pytest` from the repo root across all skills at once — use `scripts/run_all_tests.sh` instead.

Known test skip list (in `run_all_tests.sh`): `theme-detector` (27 pre-existing failures), `canslim-screener` (requires `bs4`, not in dev extras).

### CI Pipeline (`.github/workflows/ci.yml`)

Three parallel jobs on PR/push to `main`:
1. **Lint** — ruff check, ruff format, codespell
2. **Test** — per-skill pytest with coverage (Python 3.9), 40% coverage threshold
3. **Security** — bandit SAST, detect-secrets baseline comparison

## Repository Architecture

### Skill Structure

All skills live under `skills/`. Each follows this structure:

```
skills/<skill-name>/
├── SKILL.md              # Required: YAML frontmatter (name, description) + workflow body
├── references/           # Knowledge bases loaded into Claude's context
├── scripts/              # Executable Python scripts (not auto-loaded)
│   ├── tests/            # Pytest tests for this skill
│   └── calculators/      # Optional: modular scoring components
└── assets/               # Templates and resources for output generation
```

**Skill type categories:**
1. **Knowledge-only** (no scripts): technical-analyst, sector-analyst, us-stock-analysis — just SKILL.md + references
2. **Simple scripts** (1-3 files): earnings-calendar, economic-calendar-fetcher — FMP API wrappers
3. **Complex modular** (calculators subdir): macro-regime-detector, earnings-trade-analyzer — multiple calculator modules + scorer + report_generator

**SKILL.md Format:**
- YAML frontmatter with `name` and `description` fields
- `name` must match the directory name for proper skill detection
- Description defines when the skill should be triggered
- Body contains workflow instructions written in imperative/infinitive form
- All instructions assume Claude will execute them, not the user

**Progressive Loading:**
1. Metadata (YAML frontmatter) loads first for skill detection
2. SKILL.md body loads when skill is invoked
3. References load conditionally based on analysis needs
4. Scripts execute on demand, never auto-loaded into context

### Key Design Patterns

**Knowledge Base Organization:**
- `references/` contains markdown files with domain knowledge (sector rotation patterns, technical analysis frameworks, news source credibility guides)
- Knowledge bases provide context without requiring Claude to have specialized training
- References are read selectively during skill execution to minimize token usage

**Script vs. Reference Division:**
- Scripts (`scripts/`) are executable code for API calls, data fetching, report generation
- References (`references/`) are documentation for Claude to read and apply
- Scripts handle I/O; references handle knowledge

**Output Generation:**
- Skills generate reports (markdown + JSON) saved to `reports/` directory
- Filename convention: `<skill>_<analysis-type>_<date>.md` (and `.json`)
- Reports use structured templates from `assets/` directories
- Scripts should default `--output-dir` to `reports/` (or pass `--output-dir reports/` when invoking)

## Common Development Tasks

### Creating a New Skill

Use the skill-creator plugin (available in Claude Code):

```bash
# This invokes the skill-creator to guide you through setup
# Follow the 6-step process: Understanding → Planning → Initializing → Editing → Packaging → Iterating
```

The skill-creator will:
1. Ask clarification questions about the skill's purpose
2. Create the directory structure
3. Generate SKILL.md template
4. Set up references and scripts directories
5. Package the skill into a .skill file

**MANDATORY: After creating or committing a new skill, update both READMEs:**
1. Add skill description to the appropriate category in `README.md` (English)
2. Add skill description to the matching category in `README.ko.md` (Korean)
3. If the skill requires API keys, add it to the API Requirements table in `README.md` and the API 요구사항 section in `README.ko.md`
4. If a new category is needed, create it in both files

### Packaging Skills for Distribution

Skills are packaged as ZIP files for Claude web app users:

```bash
# Use the skill-creator's packaging script
python3 ~/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/package_skill.py <skill-name>
```

The packaged .skill files are stored in `skill-packages/` and should be regenerated after any skill modifications.

### Testing Skills

Skills are tested by invoking them in Claude Code conversations:

1. Copy skill folder to Claude Code Skills directory
2. Restart Claude Code to detect the skill
3. Trigger the skill by providing input that matches the skill's description
4. Verify that:
   - Skill loads correctly (check YAML frontmatter)
   - References load when needed
   - Scripts execute with proper error handling
   - Output matches expected format

### Code Generation (TDD)

When generating or modifying code in this repository, use a TDD-first workflow:

1. Write or update tests first (expected to fail initially).
2. Implement the minimal code change needed to pass tests.
3. Refactor while keeping tests green.
4. Run the relevant test suite before finishing.

If no test exists for the changed behavior, add one whenever practical.

### API Key Management

⚠️ **IMPORTANT:** Several skills require paid API subscriptions to function. Review the requirements below before using these skills.

#### API Requirements by Skill

| Skill | FMP API | FINVIZ Elite | Alpaca | Notes |
|-------|---------|--------------|--------|-------|
| **Economic Calendar Fetcher** | ✅ Required | ❌ | ❌ | Fetches economic events |
| **Earnings Calendar** | ✅ Required | ❌ | ❌ | Fetches earnings dates |
| **Institutional Flow Tracker** | ✅ Required | ❌ | ❌ | 13F filings; free tier sufficient |
| **Value Dividend Screener** | ✅ Required | 🟡 Optional | ❌ | FINVIZ reduces runtime 70-80% |
| **Dividend Growth Pullback Screener** | ✅ Required | 🟡 Optional | ❌ | FINVIZ for RSI pre-screening |
| **Pair Trade Screener** | ✅ Required | ❌ | ❌ | Statistical arbitrage |
| **Earnings Trade Analyzer** | ✅ Required | ❌ | ❌ | 5-factor scoring; free tier sufficient |
| **PEAD Screener** | ✅ Required | ❌ | ❌ | Weekly candle PEAD; free tier sufficient |
| **Options Strategy Advisor** | 🟡 Optional | ❌ | ❌ | Black-Scholes works without |
| **Portfolio Manager** | ❌ | ❌ | ✅ Required | Real-time holdings via Alpaca MCP |
| **Theme Detector** | 🟡 Optional | 🟡 Optional | ❌ | FINVIZ for dynamic stocks |
| **FinViz Screener** | ❌ | 🟡 Optional | ❌ | Public screener free; Elite auto-detected |
| Chart/News/Analysis skills | ❌ | ❌ | ❌ | Image-based or WebSearch; no API needed |

#### API Key Setup

**Financial Modeling Prep (FMP) API:**
```bash
# Set environment variable (preferred method)
export FMP_API_KEY=your_key_here

# Or provide via command-line argument when script runs
python3 scripts/get_economic_calendar.py --api-key YOUR_KEY
```

**FINVIZ Elite API:**
```bash
# Set environment variable
export FINVIZ_API_KEY=your_key_here

# Or provide via command-line argument
python3 value-dividend-screener/scripts/screen_dividend_stocks.py \
  --use-finviz \
  --finviz-api-key YOUR_KEY
```

**Alpaca Trading API:**
```bash
# Set environment variables
export ALPACA_API_KEY="your_api_key_id"
export ALPACA_SECRET_KEY="your_secret_key"
export ALPACA_PAPER="true"  # or "false" for live trading

# Configure Alpaca MCP Server in Claude Code settings
# See portfolio-manager/references/alpaca-mcp-setup.md for detailed setup guide
```

All API scripts follow a consistent pattern: check env var first → fall back to CLI arg → clear error if missing. See README.md for detailed pricing and sign-up links.

### Running Helper Scripts

All scripts support `--help` for full usage. Scripts live under `skills/<skill-name>/scripts/`. Common invocation pattern:

```bash
# Run any skill script (always pass --output-dir reports/)
python3 skills/<skill-name>/scripts/<script>.py --output-dir reports/

# Example: earnings trade analyzer
python3 skills/earnings-trade-analyzer/scripts/analyze_earnings_trades.py --output-dir reports/

# Example: PEAD screener (pipeline from analyzer output)
python3 skills/pead-screener/scripts/screen_pead.py \
  --candidates-json reports/earnings_trade_*.json --min-grade B --output-dir reports/

# Example: skill reviewer
uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
  --project-root . --skill backtest-expert --output-dir reports/
```

### Skill Self-Improvement Loop

An automated pipeline reviews and improves skill quality on a daily cadence.

**Architecture:**
- `scripts/run_skill_improvement_loop.py` — orchestrator (round-robin selection, auto scoring, Claude CLI improvement, quality gate, PR creation)
- `skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py` — scoring engine (5-category deterministic auto axis, optional LLM axis)
- `scripts/run_skill_improvement.sh` — thin shell wrapper for launchd
- `launchd/com.trade-analysis.skill-improvement.plist` — macOS launchd agent (daily 05:00)

**Key design decisions:**
- Improvement trigger uses `auto_review.score` (deterministic) instead of `final_review.score` (LLM-influenced) for reproducibility
- Quality gate re-scores after improvement with tests enabled; rolls back if score didn't improve
- PID-based lock file with stale detection prevents concurrent runs
- Git safety checks (clean tree, main branch, `git pull --ff-only`) before any operations
- `knowledge_only` skills (no scripts, references only) get adjusted scoring to avoid unfair penalties

**Running manually:**
```bash
# Dry-run: score one skill without improvements or PRs
python3 scripts/run_skill_improvement_loop.py --dry-run

# Dry-run all skills
python3 scripts/run_skill_improvement_loop.py --dry-run --all

# Full run
python3 scripts/run_skill_improvement_loop.py
```

**Running the reviewer standalone:**
```bash
# Score a random skill
uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
  --project-root . --output-dir reports/

# Score a specific skill
uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
  --project-root . --skill backtest-expert --output-dir reports/

# Score all skills
uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
  --project-root . --all --output-dir reports/
```

**State and output files:**
- `logs/.skill_improvement_state.json` — round-robin state and 60-entry history
- `logs/skill_improvement.log` — execution log (30-day rotation)
- `reports/skill-improvement-log/YYYY-MM-DD_summary.md` — daily summary

**Tests:**
```bash
# Reviewer tests (21 tests)
python3 -m pytest skills/dual-axis-skill-reviewer/scripts/tests/ -v

# Orchestrator tests (20 tests)
python3 -m pytest scripts/tests/test_skill_improvement_loop.py -v
```

## Multi-Skill Workflows

Skills are designed to be combined for comprehensive analysis:

- **Daily Monitoring:** Economic Calendar → Earnings Calendar → Market News → Breadth Chart
- **Weekly Review:** Sector Analyst → Technical Analyst → Market Environment → Bubble Detector
- **Stock Research:** US Stock Analysis → Earnings Calendar → Market News → Backtest Expert
- **Options Development:** Options Strategy Advisor → Technical Analyst → Earnings Calendar → US Stock Analysis
- **Portfolio Review:** Portfolio Manager (Alpaca MCP) → Risk Metrics → Market Environment → Rebalance
- **Earnings Momentum:** Earnings Trade Analyzer → PEAD Screener (Mode B) → Technical Analyst → Monitor breakouts
- **Statistical Arbitrage:** Pair Trade Screener → Technical Analyst → Monitor z-score convergence
- **Income Portfolio:** Value Dividend Screener → Dividend Growth Pullback → US Stock Analysis → Portfolio Manager
- **Kanchi Dividend:** kanchi-dividend-sop → kanchi-dividend-review-monitor → kanchi-dividend-us-tax-accounting

## Important Conventions

### SKILL.md Writing Style

- Use imperative/infinitive verb forms (e.g., "Analyze the chart", "Generate report")
- Write instructions for Claude to execute, not user instructions
- Avoid phrases like "You should..." or "Claude will..." - just state actions directly
- Structure: Overview → When to Use → Workflow → Output Format → Resources

### Reference Document Patterns

- Knowledge bases use declarative statements of fact
- Include historical examples and case studies
- Provide decision frameworks and checklists
- Organize hierarchically (H2 for major sections, H3 for subsections)

### Analysis Output Requirements

All analysis outputs must:
- Be saved to the `reports/` directory (create if it does not exist)
- Include date/time stamps
- Use English language
- Provide probability assessments where applicable
- Include specific trigger levels for actionable scenarios
- Cite references to knowledge base sources

## Language Considerations

- All SKILL.md files are in English
- Analysis outputs are in English
- Some reference materials (Stanley Druckenmiller Investment) include Japanese content
- README files available in both English (README.md) and Korean (README.ko.md)
- User interactions may be in Korean or Japanese; analysis outputs remain in English

## Distribution Workflow

1. Test skill thoroughly in Claude Code
2. Package with skill-creator (see [Packaging Skills](#packaging-skills-for-distribution))
3. Move `.skill` file to `skill-packages/`
4. Update `README.md` and `README.ko.md` (include API requirements if applicable)
5. Commit changes
