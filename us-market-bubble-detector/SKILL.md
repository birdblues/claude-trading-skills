---
name: us-market-bubble-detector
description: Evaluates market bubble risk through quantitative data-driven analysis using the revised Minsky/Kindleberger framework v2.0. Prioritizes objective metrics (Put/Call, VIX, margin debt, breadth, IPO data) over subjective impressions. Supports practical investment decisions with mandatory data collection and mechanical scoring. Use when user asks about bubble risk, valuation concerns, or profit-taking timing.
---

# US Market Bubble Detection Skill (Revised v2.0)

## Key Revisions

**Critical Changes:**
1. ✅ **Mandatory Quantitative Data Collection** - Use measured values, not impressions or speculation
2. ✅ **Clear Threshold Settings** - Specific numerical criteria for each indicator
3. ✅ **Two-Phase Evaluation Process** - Quantitative evaluation → Qualitative adjustment (strict order)
4. ✅ **Reduced Weight on Subjective Indicators** - Media coverage as reference only

---

## When to Use This Skill

Use this skill when:

**English:**
- User asks "Is the market in a bubble?" or "Are we in a bubble?"
- User seeks advice on profit-taking, new entry timing, or short-selling decisions
- User reports social phenomena (non-investors entering, media frenzy, IPO flood)
- User mentions narratives like "this time is different" or "revolutionary technology" becoming mainstream
- User consults about risk management for existing positions

**Japanese:**
- ユーザーが「今の相場はバブルか?」と尋ねる
- 投資の利確・新規参入・空売りのタイミング判断を求める
- 社会現象(非投資家の参入、メディア過熱、IPO氾濫)を観察し懸念を表明
- 「今回は違う」「革命的技術」などの物語が主流化している状況を報告
- 保有ポジションのリスク管理方法を相談

---

## Evaluation Process (Strict Order)

### Phase 1: Mandatory Quantitative Data Collection

**CRITICAL: Always collect the following data before starting evaluation**

#### 1.1 Market Structure Data (Highest Priority)
```
□ Put/Call Ratio (CBOE Equity P/C)
  - Source: CBOE DataShop or web_search "CBOE put call ratio"
  - Collect: 5-day moving average

□ VIX (Fear Index)
  - Source: Yahoo Finance ^VIX or web_search "VIX current"
  - Collect: Current value + percentile over past 3 months

□ Volatility Indicators
  - 21-day realized volatility
  - Historical position of VIX (determine if in bottom 10th percentile)
```

#### 1.2 Leverage & Positioning Data
```
□ FINRA Margin Debt Balance
  - Source: web_search "FINRA margin debt latest"
  - Collect: Latest month + Year-over-Year % change

□ Breadth (Market Participation)
  - % of S&P 500 stocks above 50-day MA
  - Source: web_search "S&P 500 breadth 50 day moving average"
```

#### 1.3 IPO & New Issuance Data
```
□ IPO Count & First-Day Performance
  - Source: Renaissance Capital IPO or web_search "IPO market 2025"
  - Collect: Quarterly count + median first-day return
```

**⚠️ CRITICAL: Do NOT proceed with evaluation without Phase 1 data collection**

---

### Phase 2: Quantitative Evaluation (Quantitative Scoring)

Score mechanically based on collected data using the following criteria:

#### Indicator 1: Put/Call Ratio (Market Sentiment)
```
Scoring Criteria:
- 2 points: P/C < 0.70 (excessive optimism, call-heavy)
- 1 point: P/C 0.70-0.85 (slightly optimistic)
- 0 points: P/C > 0.85 (healthy caution)

Rationale: P/C < 0.7 is historically characteristic of bubble periods
```

#### Indicator 2: Volatility Suppression + New Highs
```
Scoring Criteria:
- 2 points: VIX < 12 AND major index within 5% of 52-week high
- 1 point: VIX 12-15 AND near highs
- 0 points: VIX > 15 OR more than 10% from highs

Rationale: Extreme low volatility + highs indicates excessive complacency
```

#### Indicator 3: Leverage (Margin Debt Balance)
```
Scoring Criteria:
- 2 points: YoY +20% or more AND all-time high
- 1 point: YoY +10-20%
- 0 points: YoY +10% or less OR negative

Rationale: Rapid leverage increase is a bubble precursor
```

#### Indicator 4: IPO Market Overheating
```
Scoring Criteria:
- 2 points: Quarterly IPO count > 2x 5-year average AND median first-day return +20%+
- 1 point: Quarterly IPO count > 1.5x 5-year average
- 0 points: Normal levels

Rationale: Poor-quality IPO flood is characteristic of late-stage bubbles
```

#### Indicator 5: Breadth Anomaly (Narrow Leadership)
```
Scoring Criteria:
- 2 points: New high AND < 45% of stocks above 50DMA (narrow leadership)
- 1 point: 45-60% above 50DMA (somewhat narrow)
- 0 points: > 60% above 50DMA (healthy breadth)

Rationale: Rally driven by few stocks is fragile
```

#### Indicator 6: Price Acceleration
```
Scoring Criteria:
- 2 points: Past 3-month return exceeds 95th percentile of past 10 years
- 1 point: Past 3-month return in 85-95th percentile of past 10 years
- 0 points: Below 85th percentile

Rationale: Rapid price acceleration is unsustainable
```

---

### Phase 3: Qualitative Adjustment

**Limit: ±2 points maximum**

Adjust quantitative score based on the following observations (upper limit set to eliminate subjectivity):

#### Adjustment A: Social Penetration (+0 to +2 points)
```
+2 points: Direct recommendation from non-investors (family, taxi drivers, etc.)
+1 point: Observation report of non-investor excitement at workplace
+0 points: No such observations

Important: Only count direct user reports. Do NOT add points based on news articles alone
```

#### Adjustment B: Media & Narrative (+0 to +1 point)
```
+1 point: Google Trends search volume 3x+ year-over-year (verify with actual measurement)
+0 points: Less than 3x

Important: Do not use "many news reports" impressions. Always verify search trend numbers
```

#### Adjustment C: Valuation (-1 to +1 point)
```
+1 point: S&P 500 P/E > 25 AND "this time is different" narrative dominant
 0 points: S&P 500 P/E 18-25
-1 point: S&P 500 P/E < 18

Important: Do not judge based on P/E alone. Combine with narrative dependence
```

---

### Phase 4: Final Judgment

```
Final Score = Phase 2 Total (0-12 points) + Phase 3 Adjustment (-1 to +5 points)
Range: -1 to 17 points (practically converges to 0-16 points)

Judgment Criteria:
- 0-4 points: Normal
- 5-8 points: Caution
- 9-12 points: Euphoria
- 13-16 points: Critical
```

---

## Data Sources (Required)

### US Market
- **Put/Call**: https://www.cboe.com/tradable_products/vix/
- **VIX**: Yahoo Finance (^VIX) or https://www.cboe.com/
- **Margin Debt**: https://www.finra.org/investors/learn-to-invest/advanced-investing/margin-statistics
- **Breadth**: https://www.barchart.com/stocks/indices/sp/sp500?viewName=advanced
- **IPO**: https://www.renaissancecapital.com/IPO-Center/Stats

### Japanese Market
- **Nikkei Futures P/C**: https://www.barchart.com/futures/quotes/NO*0/options
- **JNIVE**: https://www.investing.com/indices/nikkei-volatility-historical-data
- **Margin Debt**: JSF (Japan Securities Finance) Monthly Report
- **Breadth**: https://en.macromicro.me/series/31841/japan-topix-index-200ma-breadth
- **IPO**: https://www.pwc.co.uk/services/audit/insights/global-ipo-watch.html

---

## Implementation Checklist

Verify the following when using:

```
□ Have you collected all Phase 1 data?
□ Did you apply each indicator's threshold mechanically?
□ Did you keep qualitative evaluation within +5 point limit?
□ Are you NOT assigning points based on news article impressions?
□ Does your final score align with other quantitative frameworks?
```

---

## Important Principles (Revised)

### 1. Data > Impressions
Ignore "many news reports" or "experts are cautious" without quantitative data.

### 2. Strict Order: Quantitative → Qualitative
Always evaluate in this order: Phase 1 (Data Collection) → Phase 2 (Quantitative) → Phase 3 (Qualitative Adjustment).

### 3. Upper Limit on Subjective Indicators
Qualitative adjustment has a total limit of +5 points. It cannot override quantitative evaluation.

### 4. "Taxi Driver" is Symbolic
Do not readily acknowledge mass penetration without direct recommendations from non-investors.

---

## Common Failures and Solutions (Revised)

### Failure 1: Evaluating Based on News Articles
❌ "Many reports on Takaichi Trade" → Media saturation 2 points
✅ Verify Google Trends numbers → Evaluate with measured values

### Failure 2: Overreaction to Expert Comments
❌ "Warning of overheating" → Euphoria zone
✅ Judge with measured values of Put/Call, VIX, margin debt

### Failure 3: Emotional Reaction to Price Rise
❌ 4.5% rise in 1 day → Price acceleration 2 points
✅ Verify position in 10-year distribution → Objective evaluation

### Failure 4: Judgment Based on Valuation Alone
❌ P/E 17 → Valuation disconnect 2 points
✅ P/E + narrative dependence + other quantitative indicators for comprehensive judgment

---

## Recommended Actions by Bubble Stage

### Normal (0-4 points)
**Risk Budget: 100%**
- Continue normal investment strategy
- Set ATR 2.0× trailing stop
- Apply stair-step profit-taking rule (+20% take 25%)

**Short-Selling: Not Allowed**
- Composite conditions not met (0/7 items)

### Caution (5-8 points)
**Risk Budget: 70%**
- Begin partial profit-taking (30% reduction)
- Tighten ATR to 1.8×
- Reduce new position sizing

**Short-Selling: Not Recommended**
- Wait for clearer reversal signals

### Euphoria (9-12 points)
**Risk Budget: 40%**
- Accelerate stair-step profit-taking (60% reduction)
- Tighten ATR to 1.5×
- No new long positions

**Short-Selling: Cautious Entry**
- After confirming at least 3/7 composite conditions
- Small position (25% of normal size)

### Critical (13-16 points)
**Risk Budget: 20% or less**
- Major profit-taking or full hedge
- ATR 1.2× or fixed stop-loss
- Consider cash preservation

**Short-Selling: Active Consideration**
- After confirming at least 5/7 composite conditions
- Scale in with small positions
- Tight stop-loss (ATR 1.5× or higher)

---

## Composite Conditions for Short-Selling (7 Items)

Only consider shorts after confirming at least 3 of the following:

```
1. Weekly chart shows lower highs
2. Volume peaks out
3. Leverage indicators drop sharply (margin debt decline)
4. Media/search trends peak out
5. Weak stocks start to break down first
6. VIX surges (spike above 20)
7. Fed/policy shift signals
```

---

## Output Format

### Evaluation Report Structure

```markdown
# [Market Name] Bubble Evaluation Report (Revised v2.0)

## Overall Assessment
- Final Score: X/16 points
- Phase: [Normal/Caution/Euphoria/Critical]
- Risk Level: [Low/Medium/High/Extremely High]
- Evaluation Date: YYYY-MM-DD

## Quantitative Evaluation (Phase 2)

| Indicator | Measured Value | Score | Rationale |
|-----------|----------------|-------|-----------|
| Put/Call | [value] | [0-2] | [reason] |
| VIX + Highs | [value] | [0-2] | [reason] |
| Margin YoY | [value] | [0-2] | [reason] |
| IPO Heat | [value] | [0-2] | [reason] |
| Breadth | [value] | [0-2] | [reason] |
| Price Accel | [value] | [0-2] | [reason] |

**Phase 2 Total: X points**

## Qualitative Adjustment (Phase 3)

- Social Penetration: [details] (+X points)
- Media: [details] (+X points)
- Valuation: [details] (+X points)

**Phase 3 Adjustment: +X points**

## Recommended Actions

**Risk Budget: X%**
- [Specific action 1]
- [Specific action 2]
- [Specific action 3]

**Short-Selling: [Allowed/Not Allowed]**
- Composite conditions: X/7 met
```

---

## Reference Documents

### `references/implementation_guide.md` (English) - **RECOMMENDED FOR FIRST USE**
- Step-by-step evaluation process with mandatory data collection
- NG examples vs OK examples
- Self-check quality criteria (4 levels)
- Red flags during review
- Best practices for objective evaluation

### `references/bubble_framework.md` (Japanese)
- Detailed theoretical framework
- Explanation of Minsky/Kindleberger model
- Behavioral psychology elements

### `references/historical_cases.md` (Japanese)
- Analysis of past bubble cases
- Dotcom, Crypto, Pandemic bubbles
- Common pattern extraction

### `references/quick_reference.md` (Japanese)
### `references/quick_reference_en.md` (English)
- Daily checklist
- Emergency 3-question assessment
- Quick scoring guide
- Key data sources

### When to Load References
- **First use or need detailed guidance:** Load `implementation_guide.md`
- **Need theoretical background:** Load `bubble_framework.md`
- **Need historical context:** Load `historical_cases.md`
- **Daily operations:** Load `quick_reference.md` (Japanese) or `quick_reference_en.md` (English)

---

## Summary: Essence of Revision

**Old Version Problem:**
- "Many media reports" → 2 points (impression)
- "Experts are cautious" → 1 point (hearsay)
- **Result: 10/16 points (overestimation)**

**Revised Version:**
- Put/Call 1.54 → 0 points (measured)
- JNIVE 25.44 → 0 points (measured)
- Margin YoY -2% → 0 points (measured)
- **Result: 3/16 points (objective evaluation)**

**Lesson:**
> "In God we trust; all others must bring data." - W. Edwards Deming

Evaluation without data is no different from fortune-telling.

---

**Last Updated:** October 27, 2025 (Revised v2.0)
**Reason for Revision:** Improved objectivity through mandatory quantitative data collection
