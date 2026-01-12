---
name: canslim-screener
description: Screen US stocks using William O'Neil's CANSLIM growth stock methodology. Use when user requests CANSLIM stock screening, growth stock analysis, momentum stock identification, or wants to find stocks with strong earnings and price momentum following O'Neil's investment system.
---

# CANSLIM Stock Screener - Phase 1 MVP

## Overview

This skill screens US stocks using William O'Neil's proven CANSLIM methodology, a systematic approach for identifying growth stocks with strong fundamentals and price momentum. CANSLIM analyzes 7 key components: **C**urrent Earnings, **A**nnual Growth, **N**ewness/New Highs, **S**upply/Demand, **L**eadership/RS Rank, **I**nstitutional Sponsorship, and **M**arket Direction.

**Phase 1 MVP** implements the 4 highest-ROI components (C, A, N, M), representing 55% of the full methodology. These components provide the strongest signal-to-noise ratio and can be calculated using the FMP API free tier.

**Two-Stage Approach:**
1. **Stage 1 (FMP API)**: Analyze stock universe with C, A, N, M components
2. **Stage 2 (Reporting)**: Rank by composite score and generate actionable reports

**Key Features:**
- Composite scoring (0-100 scale) with weighted components
- Progressive filtering to optimize API usage
- JSON + Markdown output formats
- Interpretation bands: Exceptional+ (90+), Exceptional (80-89), Strong (70-79), Above Average (60-69)
- Bear market protection (M component gating)

**Phase 1 Component Weights (Renormalized):**
- C (Current Earnings): 27%
- A (Annual Growth): 36%
- N (Newness): 27%
- M (Market Direction): 10%

**Future Phases:**
- Phase 2: Add S (Supply/Demand) and I (Institutional) components → 80% coverage
- Phase 3: Add L (Leadership/RS Rank) → 100% coverage (full CANSLIM)
- Phase 4: FINVIZ Elite integration → 10x faster execution

---

## When to Use This Skill

**Explicit Triggers:**
- "Find CANSLIM stocks"
- "Screen for growth stocks using O'Neil's method"
- "Which stocks have strong earnings and momentum?"
- "Identify stocks near 52-week highs with accelerating earnings"
- "Run a CANSLIM screener on [sector/universe]"

**Implicit Triggers:**
- User wants to identify multi-bagger candidates
- User is looking for growth stocks with proven fundamentals
- User wants systematic stock selection based on historical winners
- User needs a ranked list of stocks meeting O'Neil's criteria

**When NOT to Use:**
- Value investing focus (use value-dividend-screener instead)
- Income/dividend focus (use dividend-growth-pullback-screener instead)
- Bear market conditions (M component will flag - consider raising cash)

---

## Workflow

### Step 1: Verify API Access and Requirements

Check if user has FMP API key configured:

```bash
# Check environment variable
echo $FMP_API_KEY

# If not set, prompt user to provide it
```

**Requirements:**
- FMP API key (free tier: 250 calls/day, sufficient for 40 stocks)
- Python 3.7+ with requests library

If API key is missing, guide user to:
1. Sign up at https://site.financialmodelingprep.com/developer/docs
2. Get free API key (250 calls/day)
3. Set environment variable: `export FMP_API_KEY=your_key_here`

### Step 2: Determine Stock Universe

**Option A: Default Universe (Recommended)**
Use top 40 S&P 500 stocks by market cap (predefined in script):

```bash
python3 skills/canslim-screener/scripts/screen_canslim.py
```

**Option B: Custom Universe**
User provides specific symbols or sector:

```bash
python3 skills/canslim-screener/scripts/screen_canslim.py \
  --universe AAPL MSFT GOOGL AMZN NVDA META TSLA
```

**Option C: Sector-Specific**
User can provide sector-focused list (Technology, Healthcare, etc.)

**API Budget Considerations:**
- 40 stocks × ~3.3 calls/stock = ~133 API calls (within free tier)
- Market data (S&P 500, VIX): 3 calls
- Total: ~136 calls per screening run

### Step 3: Execute CANSLIM Screening Script

Run the main screening script with appropriate parameters:

```bash
cd /Users/takueisaotome/PycharmProjects/claude-trading-skills/skills/canslim-screener/scripts

# Basic run (40 stocks, top 20 in report)
python3 screen_canslim.py --api-key $FMP_API_KEY

# Custom parameters
python3 screen_canslim.py \
  --api-key $FMP_API_KEY \
  --max-candidates 40 \
  --top 20 \
  --output-dir ../../../
```

**Script Workflow:**
1. **Market Direction (M)**: Analyze S&P 500 trend vs 50-day EMA
   - If bear market detected (M=0), warn user to raise cash
2. **Stock Analysis**: For each stock, calculate:
   - C Component: Quarterly EPS/revenue growth (YoY)
   - A Component: 3-year EPS CAGR and stability
   - N Component: Distance from 52-week high, breakout detection
3. **Composite Scoring**: Weighted average with component breakdown
4. **Ranking**: Sort by composite score (highest first)
5. **Reporting**: Generate JSON + Markdown outputs

**Expected Execution Time:**
- FMP-only: 5-10 minutes for 40 stocks (rate limiting)
- Phase 4 with FINVIZ: 1-2 minutes

### Step 4: Read and Parse Screening Results

The script generates two output files:
- `canslim_screener_YYYY-MM-DD_HHMMSS.json` - Structured data
- `canslim_screener_YYYY-MM-DD_HHMMSS.md` - Human-readable report

Read the Markdown report to identify top candidates:

```bash
# Find the latest report
ls -lt canslim_screener_*.md | head -1

# Read the report
cat canslim_screener_YYYY-MM-DD_HHMMSS.md
```

**Report Structure:**
- Market Condition Summary (trend, M score, warnings)
- Top 20 CANSLIM Candidates (ranked)
- For each stock:
  - Composite Score and Rating (Exceptional+/Exceptional/Strong/etc.)
  - Component Breakdown (C, A, N, M scores with details)
  - Interpretation (rating description, guidance, weakest component)
  - Warnings (quality issues, market conditions)
- Summary Statistics (rating distribution)
- Methodology note

### Step 5: Analyze Top Candidates and Provide Recommendations

Review the top-ranked stocks and cross-reference with knowledge bases:

**Reference Documents to Consult:**
1. `references/interpretation_guide.md` - Understand rating bands and portfolio sizing
2. `references/canslim_methodology.md` - Deep dive into component meanings
3. `references/scoring_system.md` - Understand scoring formulas

**Analysis Framework:**

For **Exceptional+ stocks (90-100 points)**:
- All components near-perfect (C≥85, A≥85, N≥85, M≥80)
- Guidance: Immediate buy, aggressive position sizing (15-20% of portfolio)
- Example: "NVDA scores 97.2 - explosive quarterly earnings (100), strong 3-year growth (95), at new highs (98), strong market (100)"

For **Exceptional stocks (80-89 points)**:
- Outstanding fundamentals + strong momentum
- Guidance: Strong buy, standard sizing (10-15% of portfolio)
- Example: "META scores 82.8 - strong earnings (85), solid growth (78), near high (88), uptrend market (80)"

For **Strong stocks (70-79 points)**:
- Solid across all components, minor weaknesses
- Guidance: Buy, standard sizing (8-12% of portfolio)

For **Above Average stocks (60-69 points)**:
- Meets thresholds, one component weak
- Guidance: Buy on pullback, conservative sizing (5-8% of portfolio)

**Bear Market Override:**
- If M component = 0 (bear market detected), **do NOT buy** regardless of other scores
- Guidance: Raise 80-100% cash, wait for market recovery
- CANSLIM does not work in bear markets (3 out of 4 stocks follow market trend)

### Step 6: Generate User-Facing Report

Create a concise, actionable summary for the user:

**Report Format:**

```markdown
# CANSLIM Stock Screening Results
**Date:** YYYY-MM-DD
**Market Condition:** [Trend] - M Score: [X]/100
**Stocks Analyzed:** [N]

## Market Summary
[2-3 sentences on current market environment based on M component]
[If bear market: WARNING - Consider raising cash allocation]

## Top 5 CANSLIM Candidates

### 1. [SYMBOL] - [Company Name] ⭐⭐⭐
**Score:** [X.X]/100 ([Rating])
**Price:** $[XXX.XX] | **Sector:** [Sector]

**Component Breakdown:**
- C (Earnings): [X]/100 - [EPS growth]% QoQ, [Revenue growth]% revenue
- A (Growth): [X]/100 - [CAGR]% 3yr EPS CAGR
- N (Newness): [X]/100 - [Distance]% from 52wk high
- M (Market): [X]/100 - [Trend]

**Interpretation:** [Rating description and guidance]
**Weakest Component:** [X] ([score])

[Repeat for top 5 stocks]

## Investment Recommendations

**Immediate Buy List (90+ score):**
- [List stocks with exceptional+ ratings]
- Position sizing: 15-20% each

**Strong Buy List (80-89 score):**
- [List stocks with exceptional ratings]
- Position sizing: 10-15% each

**Watchlist (70-79 score):**
- [List stocks with strong ratings]
- Buy on pullback

## Risk Factors
- [Identify any quality warnings from components]
- [Market condition warnings]
- [Sector concentration risks if applicable]

## Next Steps
1. Conduct detailed fundamental analysis on top 3 candidates
2. Check earnings calendars for upcoming reports
3. Review technical charts for entry timing
4. [If bear market: Wait for market recovery before deploying capital]

---
**Note:** This is Phase 1 MVP (C, A, N, M components only). Full CANSLIM (Phase 2-3) will add S, L, I components for enhanced accuracy.
```

---

## Resources

### Scripts Directory (`scripts/`)

**Main Scripts:**
- `screen_canslim.py` - Main orchestrator script
  - Entry point for screening workflow
  - Handles argument parsing, API coordination, ranking, reporting
  - Usage: `python3 screen_canslim.py --api-key KEY [options]`

- `fmp_client.py` - FMP API client wrapper
  - Rate limiting (0.3s between calls)
  - 429 error handling with 60s retry
  - Session-based caching
  - Methods: `get_income_statement()`, `get_quote()`, `get_historical_prices()`

**Calculators (`scripts/calculators/`):**
- `earnings_calculator.py` - C component (Current Earnings)
  - Quarterly EPS/revenue growth (YoY)
  - Scoring: 50%+ = 100pts, 30-49% = 80pts, 18-29% = 60pts

- `growth_calculator.py` - A component (Annual Growth)
  - 3-year EPS CAGR calculation
  - Stability check (no negative growth years)
  - Scoring: 40%+ = 90pts, 30-39% = 70pts, 25-29% = 50pts

- `new_highs_calculator.py` - N component (Newness)
  - Distance from 52-week high
  - Volume-confirmed breakout detection
  - Scoring: 5% of high + breakout = 100pts, 10% + breakout = 80pts

- `market_calculator.py` - M component (Market Direction)
  - S&P 500 vs 50-day EMA
  - VIX-adjusted scoring
  - Scoring: Strong uptrend = 100pts, Uptrend = 80pts, Bear market = 0pts

**Supporting Modules:**
- `scorer.py` - Composite score calculation
  - Weighted average: C×27% + A×36% + N×27% + M×10%
  - Rating interpretation (Exceptional+/Exceptional/Strong/etc.)
  - Minimum threshold validation

- `report_generator.py` - Output generation
  - JSON export (programmatic use)
  - Markdown export (human-readable)
  - Summary statistics calculation

### References Directory (`references/`)

**Knowledge Bases:**
- `canslim_methodology.md` (19KB) - Complete CANSLIM explanation
  - All 7 components with O'Neil's original thresholds
  - Historical examples (AAPL 2009, NFLX 2013, TSLA 2019)
  - Phase 1 vs Full CANSLIM comparison

- `scoring_system.md` (17KB) - Technical scoring specification
  - Component weights and formulas
  - Interpretation bands (90-100, 80-89, etc.)
  - Phase 1 renormalization methodology

- `fmp_api_endpoints.md` (14KB) - API integration guide
  - Required endpoints for each component
  - Rate limiting strategy
  - Cost analysis (free tier sufficiency)

- `interpretation_guide.md` (18KB) - User guidance
  - Portfolio construction rules
  - Position sizing by rating
  - Entry/exit strategies
  - Bear market protection rules

**How to Use References:**
- Read `canslim_methodology.md` first to understand O'Neil's system
- Consult `interpretation_guide.md` when analyzing results
- Reference `scoring_system.md` if scores seem unexpected
- Check `fmp_api_endpoints.md` for API troubleshooting

---

## Troubleshooting

### Issue 1: FMP API Rate Limit Exceeded

**Symptoms:**
```
ERROR: 429 Too Many Requests - Rate limit exceeded
Retrying in 60 seconds...
```

**Causes:**
- Running multiple screenings within short time window
- Exceeding 250 calls/day (free tier limit)
- Other applications using same API key

**Solutions:**
1. **Wait and Retry**: Script auto-retries after 60s
2. **Reduce Universe**: Use `--max-candidates 30` to lower API usage
3. **Check Daily Usage**: Free tier resets at midnight UTC
4. **Upgrade Plan**: FMP Starter ($29.99/month) provides 750 calls/day

### Issue 2: Missing API Key

**Symptoms:**
```
ERROR: FMP API key not found. Set FMP_API_KEY environment variable or provide --api-key argument.
```

**Solutions:**
```bash
# Option 1: Set environment variable
export FMP_API_KEY=your_key_here

# Option 2: Provide via argument
python3 screen_canslim.py --api-key your_key_here
```

### Issue 3: No Stocks Meet Minimum Thresholds

**Symptoms:**
```
✓ Successfully analyzed 40 stocks
Top 5 Stocks:
  1. AAPL  -  58.3 (Average)
  2. MSFT  -  55.1 (Average)
  ...
```

**Causes:**
- Bear market conditions (M component low)
- Selected universe lacks growth stocks
- Market rotation away from growth

**Solutions:**
1. **Check M Component**: If M=0 (bear market), raise cash per CANSLIM rules
2. **Expand Universe**: Try different sectors or market cap ranges
3. **Lower Expectations**: Average scores (55-65) may still be actionable in weak markets
4. **Wait for Better Setup**: CANSLIM works best in bull markets

### Issue 4: Data Quality Warnings

**Symptoms:**
```
⚠️ Revenue declining despite EPS growth (possible buyback distortion)
⚠️ Market in choppy/downtrend - defensive posture recommended
```

**Interpretation:**
- These are **not errors** - they are quality flags from calculators
- Revenue warning: EPS growth may be from share buybacks, not organic growth
- Market warning: Proceed with caution, reduce position sizes

**Actions:**
1. Review component details in full report
2. Cross-check with fundamental analysis
3. Adjust position sizing based on risk level

### Issue 5: Slow Execution Time (10+ minutes)

**Causes:**
- FMP rate limiting (0.3s per request)
- Large universe (50+ stocks)
- Network latency

**Solutions:**
1. **Accept Delay**: 5-10 minutes for 40 stocks is normal with free tier
2. **Reduce Universe**: `--max-candidates 30` for faster runs
3. **Upgrade to Phase 4**: FINVIZ Elite integration reduces time to 1-2 minutes

### Issue 6: Empty Historical Data for Some Stocks

**Symptoms:**
```
Analyzing XYZ... ✗ No quarterly data
Analyzing ABC... ✗ Profile unavailable
```

**Causes:**
- Recently IPO'd stocks (< 1 year)
- Delisted or suspended stocks
- API data gaps

**Solutions:**
- These stocks are automatically skipped
- No action required - screener continues with available data
- Final report shows "Successfully analyzed X of Y stocks"

---

## Important Notes

### Phase 1 Limitations

This is **Phase 1 MVP** implementing only 4 of 7 CANSLIM components:
- ✅ **C** (Current Earnings) - Implemented
- ✅ **A** (Annual Growth) - Implemented
- ✅ **N** (Newness) - Implemented
- ❌ **S** (Supply/Demand) - Not implemented (Phase 2)
- ❌ **L** (Leadership/RS Rank) - Not implemented (Phase 3)
- ❌ **I** (Institutional) - Not implemented (Phase 2)
- ✅ **M** (Market Direction) - Implemented

**Implications:**
- Composite scores represent 55% of full CANSLIM methodology
- Top scores typically max out at ~90 (full CANSLIM can reach 200+)
- Missing components: Volume analysis, relative strength rank, institutional sponsorship
- Phase 1 is still highly effective - C, A, N, M are highest-signal components

**Score Conversion:**
- Phase 1 score 85+ ≈ Full CANSLIM 140-160 (Strong to Exceptional)
- Phase 1 score 70-84 ≈ Full CANSLIM 120-139 (Above Average)
- Phase 1 score 60-69 ≈ Full CANSLIM 105-119 (Average)

### Future Enhancements

**Phase 2 (Planned):**
- Add S component: Volume analysis, accumulation/distribution
- Add I component: Institutional ownership changes, 13F filings
- Weight adjustment: C 15%, A 20%, N 15%, S 15%, I 10%, M 5% (L still missing)
- Coverage: 80% of full CANSLIM

**Phase 3 (Planned):**
- Add L component: RS Rank estimation (52-week high proxy, 80% accuracy)
- Full 7-component CANSLIM: C 15%, A 20%, N 15%, S 15%, L 20%, I 10%, M 5%
- Coverage: 100% of full CANSLIM

**Phase 4 (Planned):**
- FINVIZ Elite integration for pre-screening
- Execution time: 10 minutes → 1-2 minutes
- FMP API usage reduction: 90%
- Larger universe possible (100+ stocks)

### Data Source Attribution

- **FMP API**: Income statements, quotes, historical prices, key metrics
- **Methodology**: William O'Neil's "How to Make Money in Stocks" (4th edition)
- **Scoring System**: Adapted from IBD MarketSmith proprietary system

### Disclaimer

**This screener is for educational and informational purposes only.**
- Not investment advice
- Past performance does not guarantee future results
- CANSLIM methodology works best in bull markets (M component confirms)
- Conduct your own research and consult a financial advisor before making investment decisions
- O'Neil's historical winners include AAPL (2009: +1,200%), NFLX (2013: +800%), but many stocks fail to perform

---

**Version:** Phase 1 MVP
**Last Updated:** 2025-01-11
**API Requirements:** FMP API (free tier sufficient)
**Execution Time:** 5-10 minutes for 40 stocks
**Output Formats:** JSON + Markdown
