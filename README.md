# Claude Trading Skills

Curated Claude skills for equity investors and traders. Each skill bundles prompts, knowledge, and optional helper scripts so Claude can assist with systematic backtesting, market environment monitoring, bubble detection, and US stock research. The repository packages skills for both Claude's web app and Claude Code workflows.

日本語版READMEは[`README.ja.md`](README.ja.md)をご覧ください。

## Repository Layout
- `<skill-name>/` – Source folder for each trading skill. Contains `SKILL.md`, reference material, and any helper scripts.
- `zip_packages/` – Pre-built ZIP archives ready to upload to Claude's web app **Skills** tab.

## Getting Started
### Use with Claude Web App
1. Download the ZIP that matches the skill you want from `zip-packages/`.
2. Open Claude in your browser, go to **Settings → Skills**, and upload the ZIP (see Anthropics' [Skills launch post](https://www.anthropic.com/news/skills) for feature overview).
3. Enable the skill inside the conversation where you need it.

### Use with Claude Code (desktop or CLI)
1. Clone or download this repository.
2. Copy the desired skill folder (e.g., `backtest-expert`) into your Claude Code **Skills** directory (open Claude Code → **Settings → Skills → Open Skills Folder**, per the [Claude Code Skills documentation](https://docs.claude.com/en/docs/claude-code/skills)).
3. Restart or reload Claude Code so the new skill is detected.

> Tip: The source folders and ZIPs contain identical content. Edit a source folder if you want to customize a skill, then re-zip it before uploading to the web app.

## Skill Catalog
- **Backtest Expert** (`backtest-expert`)
  - Framework for professional-grade strategy validation: hypothesis definition, parameter robustness checks, slippage modeling, and walk-forward testing.
  - References cover detailed methodology (`references/methodology.md`) and failure post-mortems (`references/failed_tests.md`).
- **Market Environment Analysis** (`market-environment-analysis`)
  - Guides Claude through global macro briefings: equity indices, FX, commodities, yields, and sentiment assessments, with structured reporting templates.
  - Includes indicator cheat sheets (`references/indicators.md`) and analysis patterns, plus a helper script `scripts/market_utils.py` for report formatting.
- **Stanley Druckenmiller Investment Advisor** (`stanley-druckenmiller-investment`)
  - Encodes Druckenmiller’s investment philosophy for macro positioning, liquidity analysis, and risk management coaching (content in Japanese and English).
  - Reference pack provides philosophy deep dives, market analysis workflows, and case studies.
- **US Market Bubble Detector** (`us-market-bubble-detector`)
  - Minsky/Kindleberger-based bubble scoring with an eight-factor “Bubble-O-Meter,” stage diagnostics, and action playbooks for profit taking and hedging.
  - Supplemented by historical case files, quick-reference checklists (JP/EN), and an interactive scorer script `scripts/bubble_scorer.py`.
- **US Stock Analysis** (`us-stock-analysis`)
  - Comprehensive US equity research assistant covering fundamentals, technicals, peer comparisons, and investment memo generation with templated outputs.
  - Reference library documents analytical frameworks (`fundamental-analysis.md`, `technical-analysis.md`, `financial-metrics.md`, `report-template.md`).

## Customization & Contribution
- Update `SKILL.md` files to tweak trigger descriptions or capability notes; ensure the frontmatter name matches the folder name when zipping.
- Extend reference documents or add scripts inside each skill folder to support new workflows.
- When distributing updates, regenerate the matching ZIP in `zip-packages/` so web-app users get the latest version.

## Support & Further Reading
- Claude Skills launch overview: https://www.anthropic.com/news/skills
- Claude Code Skills how-to: https://docs.claude.com/en/docs/claude-code/skills

Questions or suggestions? Open an issue or include guidance alongside the relevant skill folder so future users know how to get the most from these trading assistants.
