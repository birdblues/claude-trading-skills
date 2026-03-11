---
name: trump-mean-reversion
description: |
  Post-processing skill that adjusts Base/Bull/Bear scenario probabilities
  using the TACO (Trump Always Chickens Out) framework. Computes a Trump Pain
  Index across 5 domains (Energy, Stock Market, Geopolitics, Trade, Interest Rates)
  and models the probability of policy reversal to clip tail risk in both directions.
  Trigger: after scenario-analyzer or stanley-druckenmiller-investment produces
  scenario probabilities, or when the user asks to apply TACO adjustment,
  Trump mean-reversion correction, or policy intervention probability analysis.
---

## Overview

Model the Trump administration's bidirectional mean-reversion behavior:
- **High Pain** (market stress) → TACO event likely → Bear probability shrinks
- **Low Pain** (market euphoria) → Aggressive policy push → Bull probability shrinks

This skill is a **post-processing step** that adjusts scenario probabilities from
upstream skills (scenario-analyzer, stanley-druckenmiller-investment).

## When to Use

- After scenario-analyzer generates Base/Bull/Bear probabilities
- After stanley-druckenmiller-investment produces a conviction score
- When the user requests TACO adjustment or Trump policy intervention analysis
- When geopolitical or trade tensions change significantly
- TACO 보정, 트럼프 평균회귀 분석, 정책 개입 확률 분석 요청 시

## Prerequisites

- **FMP API Key** (optional): Only needed with `--use-fmp` for real-time market data
- Without FMP: Provide domain values manually via CLI arguments

## Workflow

### Step 1: Load Upstream Scenario Probabilities

Parse scenario probabilities from the upstream skill's output.

```bash
# From scenario-analyzer JSON
uv run python3 skills/trump-mean-reversion/scripts/taco_adjuster.py \
  --scenario-json reports/scenario_analysis.json \
  --geopolitics 7 --trade 5 \
  --output-dir reports/

# From manual input
uv run python3 skills/trump-mean-reversion/scripts/taco_adjuster.py \
  --base 40 --bull 15 --bear 45 \
  --geopolitics 7 --trade 5 \
  --output-dir reports/
```

Supported input formats:
- JSON: `{"base": 40, "bull": 15, "bear": 45}`
- JSON: `{"scenarios": {"base": {"probability": 40}, ...}}`
- JSON: Druckenmiller conviction format (auto-converted)
- Markdown: `### Base Case (50% ...)` header pattern
- CLI: `--base/--bull/--bear` direct arguments

### Step 1.5: Supabase Breaking News Context for Pain Scoring (Optional)

**Prerequisite:** Check if `mcp__supabase__execute_sql` tool is available.
If not available, skip directly to Step 2.

Invoke the `supabase-news-summarizer` agent:

```
Agent tool:
  subagent_type: "supabase-news-summarizer"
  prompt: |
    최근 10일간 Supabase public.news 테이블의 속보를 전량 수집하여
    Trump Pain Index 5개 도메인별 핵심 이벤트를 요약해주세요.

    분석 기간: [현재 날짜 - 10일] ~ [현재 날짜]

    다음 5개 도메인 각각에 대해 관련 뉴스를 정리해주세요:
    1. Energy/Oil — 유가 변동, OPEC 결정, 에너지 정책
    2. Stock Market — S&P 500 급등락, 시장 심리 전환, 금융 위기 신호
    3. Geopolitics — 전쟁/분쟁, 제재, 동맹 관계 변화
    4. Trade/Tariffs — 관세 부과/철회, 무역 협상, 공급망 변화
    5. Interest Rates — 금리 결정, 국채 시장 동향, 연준 발언

    각 도메인별 Pain 수준 평가에 도움이 되는 핵심 팩트를 포함해주세요.
    크로스테마 상호작용과 블라인드 스팟 경보도 포함.
```

**Why agent:** 10일간 중요 속보 800+건 × detail 평균 824자 = ~665K자로 메인 컨텍스트에 직접 로드 불가. 에이전트가 자체 컨텍스트 윈도우에서 전량 처리 후 3,000자 이내 압축 요약을 반환.

**Agent output → Step 2 input:**
- Supabase 컨텍스트가 있으면 Geopolitics/Trade 점수 판단 시 뉴스 기반 근거로 참조
- Energy/Interest Rates 도메인도 최근 정책 변화 반영에 활용

### Step 2: Assess Pain Index Domain Values

**Note:** Step 1.5의 Supabase 컨텍스트가 있으면 Geopolitics(`--geopolitics`)와 Trade(`--trade`) 점수 판단 시 뉴스 기반 근거로 참조하세요. 에이전트 출력에서 각 도메인별 Pain 수준 평가를 참고하여 1-10 점수를 결정합니다.

For each of the 5 domains, determine the current level:

1. **Energy/Oil (30% weight):** WTI price in USD. Use `--energy` or FMP (USO proxy).
2. **Stock Market (25% weight):** S&P 500 drawdown from ATH in %. Use `--stock-drawdown` or FMP.
3. **Geopolitics (20% weight):** Manual 1-10 score via `--geopolitics`.
4. **Trade/Tariffs (15% weight):** Manual 1-10 score via `--trade`.
5. **Interest Rates (10% weight):** 10Y yield in %. Use `--interest-rate` or FMP (TLT proxy).

If using FMP for market data:
```bash
uv run python3 skills/trump-mean-reversion/scripts/taco_adjuster.py \
  --scenario-json reports/scenario_analysis.json \
  --use-fmp --geopolitics 7 --trade 5 \
  --output-dir reports/
```

### Step 3: Calculate Pain Index and Adjust Probabilities

The script automatically:
1. Computes the Trump Pain Index (0-100) via sigmoid normalization
2. Determines the pain zone (Low / Medium / High)
3. Calculates intervention probability with diminishing returns
4. Applies directional probability adjustment:
   - High Pain → clip Bear → redistribute to Base (60%) and Bull (40%)
   - Low Pain → clip Bull → redistribute to Base (60%) and Bear (40%)
   - Medium Pain → minor adjustment only
5. Enforces constraints: floor 5%, ceiling 75%, sum 100%, max shift ±20pp

### Step 4: Generate Reports

Output files saved to `--output-dir`:
- `taco_adjustment_YYYY-MM-DD_HHMMSS.json` — Full structured data
- `taco_adjustment_YYYY-MM-DD_HHMMSS.md` — Human-readable report

### Step 5: Review and Interpret

Review the Markdown report, focusing on:
1. Pain Index dashboard — which domains are driving stress
2. Adjustment magnitude — how much probabilities shifted
3. Diminishing returns — whether repeated interventions are discounted
4. Monitoring levels — key thresholds to watch for regime change

## Output Format

### Markdown Report Structure

1. Trump Pain Index Dashboard (5-domain table)
2. Intervention Probability Analysis
3. Probability Adjustment Results (Before → After table)
4. Adjustment Rationale
5. Key Monitoring Levels
6. Market Data Snapshot (if FMP used)

### JSON Structure

```json
{
  "schema_version": "1.0",
  "metadata": {"generated_at": "...", "skill": "trump-mean-reversion"},
  "pain_index": {"pain_index": 65.3, "zone": "High", ...},
  "intervention": {"effective_impact": 0.85, ...},
  "probability_adjustment": {
    "original": {"base": 40, "bull": 15, "bear": 45},
    "adjusted": {"base": 48, "bull": 19, "bear": 33},
    ...
  }
}
```

## Resources

- `scripts/taco_adjuster.py` — CLI entry point
- `scripts/pain_index.py` — Trump Pain Index calculator (0-100)
- `scripts/intervention_model.py` — Intervention probability + diminishing returns
- `scripts/probability_adjuster.py` — Scenario probability adjustment engine
- `scripts/scenario_parser.py` — Upstream skill output parser
- `scripts/fmp_client.py` — FMP API client for market data
- `scripts/report_generator.py` — Markdown + JSON report output
- `references/taco_framework.md` — TACO theory and methodology
- `references/historical_interventions.md` — Historical intervention case database
- `references/domain_triggers.md` — Domain-specific pain thresholds

## Key Principles

1. **Bidirectional clipping** — Trump is a mean-reversion variable on both tails
2. **Diminishing returns** — Repeated interventions lose market impact
3. **Words vs Actions** — Verbal interventions discounted 70% vs actual policy changes
4. **Conservative adjustment** — Max ±20pp total shift, 5% floor, 75% ceiling
5. **Data quality transparency** — Report missing domains and their weight impact
