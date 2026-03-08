---
name: earnings-trade-analyzer
description: Analyze recent post-earnings stocks using a 5-factor scoring system (Gap Size, Pre-Earnings Trend, Volume Trend, MA200 Position, MA50 Position). Scores each stock 0-100 and assigns A/B/C/D grades. Use when user asks about earnings trade analysis, post-earnings momentum screening, earnings gap scoring, or finding best recent earnings reactions.
---

# Earnings Trade Analyzer - Post-Earnings 5-Factor Scoring

Analyze recent post-earnings stocks using a 5-factor weighted scoring system to identify the strongest earnings reactions for potential momentum trades.

## When to Use

- User asks for post-earnings trade analysis or earnings gap screening
- User wants to find the best recent earnings reactions
- User requests earnings momentum scoring or grading
- User asks about post-earnings accumulation day (PEAD) candidates

## Prerequisites

- FMP API key (set `FMP_API_KEY` environment variable or pass `--api-key`)
- Free tier (250 calls/day) is sufficient for default screening (lookback 2 days, top 20)
- Paid tier recommended for larger lookback windows or full screening

## Workflow

### Step 1: Run the Earnings Trade Analyzer

Execute the analyzer script:

```bash
# Default: last 2 days of earnings, top 20 results
python3 skills/earnings-trade-analyzer/scripts/analyze_earnings_trades.py --output-dir reports/

# Custom lookback and market cap filter
python3 skills/earnings-trade-analyzer/scripts/analyze_earnings_trades.py \
  --lookback-days 5 \
  --min-market-cap 1000000000 \
  --top 30 \
  --output-dir reports/

# With entry quality filter
python3 skills/earnings-trade-analyzer/scripts/analyze_earnings_trades.py \
  --apply-entry-filter \
  --output-dir reports/
```

### Step 2: Review Results

1. Read the generated JSON and Markdown reports
2. Load `references/scoring_methodology.md` for scoring interpretation context
3. Focus on Grade A and B stocks for actionable setups

### Step 3: Present Analysis

For each top candidate, present:
- Composite score and letter grade (A/B/C/D)
- Earnings gap size and direction
- Pre-earnings 20-day trend
- Volume ratio (20-day vs 60-day average)
- Position relative to 200-day and 50-day moving averages
- Weakest and strongest scoring components

### Step 4: Provide Actionable Guidance

Based on grades:
- **Grade A (85+):** Strong earnings reaction with institutional accumulation - consider entry
- **Grade B (70-84):** Good earnings reaction worth monitoring - wait for pullback or confirmation
- **Grade C (55-69):** Mixed signals - use caution, additional analysis needed
- **Grade D (<55):** Weak setup - avoid or wait for better conditions

## Output

- `earnings_trade_analyzer_YYYY-MM-DD_HHMMSS.json` - Structured results with schema_version "1.0"
- `earnings_trade_analyzer_YYYY-MM-DD_HHMMSS.md` - Human-readable report with tables

### Step 5: 한글 리포트 생성

생성된 영어 리포트를 한국어로 번역한다.

1. `skills/report-translator/references/translation_guidelines.md`를 읽어 번역 가이드라인 확인
2. 생성된 마크다운 리포트를 한국어로 번역
   - 종목 티커, 숫자, 기술 지표명은 원본 유지
   - 섹션 헤더, 설명, 가이던스를 한국어로 변환
   - Markdown 구조(테이블, 볼드 등) 보존
3. 번역본을 `*_ko.md`로 저장
4. data-quality-checker로 번역본 검증:
   ```bash
   python3 skills/data-quality-checker/scripts/check_data_quality.py \
     --file reports/<translated_file>_ko.md --output-dir reports/
   ```
5. 검증 결과에 ERROR가 있으면 해당 부분 수정 후 재저장

## Resources

- `references/scoring_methodology.md` - 5-factor scoring system, grade thresholds, and entry quality filter rules
