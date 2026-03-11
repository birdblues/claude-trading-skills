---
name: market-news-analyst
description: This skill should be used when analyzing recent market-moving news events and their impact on equity markets and commodities. Use this skill when the user requests analysis of major financial news from the past 10 days, wants to understand market reactions to monetary policy decisions (FOMC, ECB, BOJ), needs assessment of geopolitical events' impact on commodities, or requires comprehensive review of earnings announcements from mega-cap stocks. The skill automatically collects news using Supabase breaking news (when available) and WebSearch/WebFetch tools and produces impact-ranked analysis reports.
---

# Market News Analyst

## Overview

This skill enables comprehensive analysis of market-moving news events from the past 10 days, focusing on their impact on US equity markets and commodities. When Supabase MCP is available, the skill first queries the breaking news database (Valley.town crawler) to identify dominant themes and high-signal events, then uses WebSearch/WebFetch to fill gaps and verify details. Without Supabase, the skill falls back to WebSearch/WebFetch-only collection. The skill evaluates market impact magnitude, analyzes actual market reactions, and produces structured reports ranked by market impact significance.

## When to Use This Skill

Use this skill when:
- User requests analysis of recent major market news (past 10 days)
- User wants to understand market reactions to specific events (FOMC decisions, earnings, geopolitical)
- User needs comprehensive market news summary with impact assessment
- User asks about correlations between news events and commodity price movements
- User requests analysis of how central bank policy announcements affected markets

Example user requests:
- "Analyze the major market news from the past 10 days"
- "How did the latest FOMC decision impact the market?"
- "What were the most important market-moving events this week?"
- "Analyze recent geopolitical news and commodity price reactions"
- "Review mega-cap tech earnings and their market impact"

## Analysis Workflow

Follow this structured 6-step workflow when analyzing market news:

### Step 0.5: Supabase Breaking News Collection (Optional)

**Prerequisite:** Check if `mcp__supabase__execute_sql` tool is available. If not available, skip directly to Step 1.

Invoke the `supabase-news-summarizer` agent to collect and summarize the full 10-day breaking news corpus:

```
Agent tool:
  subagent_type: "supabase-news-summarizer"
  prompt: |
    최근 10일간 Supabase public.news 테이블의 속보를 전량 수집하여
    내러티브별 요약을 생성해주세요.

    분석 기간: [현재 날짜 - 10일] ~ [현재 날짜]

    다음을 반환해주세요:
    1. 내러티브 그룹별 요약 (건수, 핵심 이벤트, 현재 상태)
    2. 크로스테마 상호작용
    3. WebSearch 갭 리스트
    4. 블라인드 스팟 경보 (사모/크레딧/시스템 리스크)
```

**Why agent:** 10일간 중요 속보 800+건 × detail 평균 824자 = ~665K자로 메인 컨텍스트에 직접 로드 불가. 에이전트가 자체 컨텍스트 윈도우에서 전량 처리 후 3,000자 이내 압축 요약을 반환.

**Agent output → Step 1 input:**
- 내러티브 그룹별 요약 (건수, 핵심 이벤트, 시장 영향)
- 크로스테마 상호작용 (인과 체인)
- WebSearch 갭 리스트 (Step 1에서 우선 검색할 항목)
- 블라인드 스팟 경보 (is_important=false에서 발견된 크레딧/시스템 리스크 신호)

---

### Step 1: News Collection via WebSearch/WebFetch

**Objective:** Gather comprehensive news from the past 10 days covering major market-moving events. If Step 0.5 was executed, focus on filling gaps identified in the WebSearch gap list and verifying key Supabase findings. If Step 0.5 was skipped (no Supabase MCP), execute all searches below as primary collection.

**Search Strategy:**

Execute parallel WebSearch queries covering different news categories:

**Monetary Policy:**
- Search: "FOMC meeting past 10 days", "Federal Reserve interest rate", "ECB policy decision", "Bank of Japan"
- Target: Central bank decisions, forward guidance changes, inflation commentary

**Inflation/Economic Data:**
- Search: "CPI inflation report [current month]", "jobs report NFP", "GDP data", "PPI producer prices"
- Target: Major economic data releases and surprises

**Mega-Cap Earnings:**
- Search: "Apple earnings [current quarter]", "Microsoft earnings", "NVIDIA earnings", "Amazon earnings", "Tesla earnings", "Meta earnings", "Google earnings"
- Target: Results, guidance, market reactions for largest companies

**Geopolitical Events:**
- Search: "Middle East conflict oil prices", "Ukraine war", "US China tensions", "trade war tariffs"
- Target: Conflicts, sanctions, trade disputes affecting markets

**Commodity Markets:**
- Search: "oil prices news past week", "gold prices", "OPEC meeting", "natural gas prices", "copper prices"
- Target: Supply disruptions, demand shifts, price movements

**Corporate News:**
- Search: "major M&A announcement", "bank earnings", "tech sector news", "bankruptcy", "credit rating downgrade"
- Target: Large corporate events beyond mega-caps

**Credit & Alternative Investments:**
- Search: "private credit fund redemption", "hedge fund liquidation",
  "BlackRock BXPE gating", "alternative investment outflows"
- Target: Private credit stress, fund gating/redemption events,
  systemic credit risk signals

**Recommended News Sources (Priority Order):**
1. Official sources: FederalReserve.gov, SEC.gov (EDGAR), Treasury.gov, BLS.gov
2. Tier 1 financial news: Bloomberg, Reuters, Wall Street Journal, Financial Times
3. Specialized: CNBC (real-time), MarketWatch (summaries), S&P Global Platts (commodities)

**Search Execution:**
- Use WebSearch for broad topic searches
- Use WebFetch for specific URLs from official sources or major news outlets
- Collect publication dates to ensure news is within 10-day window
- Capture: Event date, source, headline, key details, market context (pre-market, trading hours, after-hours)

**Filtering Criteria:**
- Focus on Tier 1 market-moving events (see references/market_event_patterns.md)
- Prioritize news with clear market impact (price moves, volume spikes)
- Exclude: Stock-specific small-cap news, minor product updates, routine filings

Think in English throughout collection process. Document each significant news item with:
- Date and time
- Event type (monetary policy, earnings, geopolitical, etc.)
- Source reliability tier
- Initial market reaction (if observable)

### Step 1.5: Price & Data Fact-Check

**Objective:** Verify extreme price claims before they propagate into the report.

**When to Trigger:**

Scan all collected news items from Step 1 for any of the following superlative keywords:
- "all-time high", "record high", "highest ever", "사상 최고"
- "all-time low", "record low", "lowest ever", "사상 최저"
- "biggest gain/loss since [year]", "worst/best since [year]"
- "first time since [year]", "broke through [round number]"

**Verification Procedure:**

For each superlative claim found:

1. **Dedicated verification search:** Execute a separate WebSearch query specifically to verify the claim
   - Example: If a news article says "gold hits record high at $5,097" → search "gold all-time high 2026 record price"
   - Example: If a news article says "oil biggest weekly gain ever" → search "crude oil largest weekly gain history"

2. **Cross-reference with at least 2 sources:** Do not rely on a single search result. Confirm with official data sources (FRED, BLS, exchange data) or Tier 1 financial news

3. **Record verified facts:** For each verified price point, document:
   - Actual ATH/ATL value and date
   - Current price and % distance from ATH/ATL
   - Whether the superlative claim is accurate, exaggerated, or false

4. **Correct or contextualize:**
   - If claim is **accurate**: Use with verified ATH value and date
   - If claim is **exaggerated**: Replace with accurate context (e.g., "$5,097/oz (ATH $5,589 on 1/28, -8.8%)")
   - If claim is **false**: Discard and use factual description only

**Output:** A verified price fact table to be referenced in Steps 3-6:

| Asset | Claimed | Verified ATH/ATL | Date | Current | Distance |
|-------|---------|-------------------|------|---------|----------|

**Rule:** No superlative price language may appear in the final report (Step 6) without passing through this verification step.

### Step 2: Load Knowledge Base References

**Objective:** Access domain expertise to inform impact assessment.

Load relevant reference files based on collected news types:

**Always Load:**
- `references/market_event_patterns.md` - Comprehensive patterns for all major event types
- `references/trusted_news_sources.md` - Source credibility assessment

**Conditionally Load (Based on News Collected):**

If **monetary policy news** found:
- Focus on: market_event_patterns.md → Central Bank Monetary Policy Events section
- Key frameworks: Interest rate hike/cut reactions, QE/QT impacts, hawkish/dovish tone

If **geopolitical events** found:
- Load: `references/geopolitical_commodity_correlations.md`
- Focus on: Energy Commodities, Precious Metals, regional frameworks matching event

If **mega-cap earnings** found:
- Load: `references/corporate_news_impact.md`
- Focus on: Specific company sections, sector contagion patterns

If **commodity news** found:
- Load: `references/geopolitical_commodity_correlations.md`
- Focus on: Specific commodity sections (Oil, Gold, Copper, etc.)

**Knowledge Integration:**
Compare collected news against historical patterns to:
- Predict expected market reactions
- Identify anomalies (market reacted differently than historical pattern)
- Assess whether reaction was typical magnitude or outsized
- Determine if contagion occurred as expected

### Step 3: Impact Magnitude Assessment

**Objective:** Rank each news event by market impact significance.

**Impact Assessment Framework:**

For each news item, evaluate across three dimensions:

**1. Asset Price Impact (Primary Factor):**

Measure actual or estimated price movements:

**Equity Markets:**
- Index-level: S&P 500, Nasdaq 100, Dow Jones
  - Severe: ±2%+ in day
  - Major: ±1-2%
  - Moderate: ±0.5-1%
  - Minor: ±0.2-0.5%
  - Negligible: <0.2%

- Sector-level: Specific sector ETFs
  - Severe: ±5%+
  - Major: ±3-5%
  - Moderate: ±1-3%
  - Minor: <1%

- Stock-specific: Individual mega-caps
  - Severe: ±10%+ (and index weight causes index move)
  - Major: ±5-10%
  - Moderate: ±2-5%

**Commodity Markets:**
- Oil (WTI/Brent):
  - Severe: ±5%+
  - Major: ±3-5%
  - Moderate: ±1-3%

- Gold:
  - Severe: ±3%+
  - Major: ±1.5-3%
  - Moderate: ±0.5-1.5%

- Base Metals (Copper, etc.):
  - Severe: ±4%+
  - Major: ±2-4%
  - Moderate: ±1-2%

**Bond Markets:**
- 10-Year Treasury Yield:
  - Severe: ±20bps+ in day
  - Major: ±10-20bps
  - Moderate: ±5-10bps

**Currency Markets:**
- USD Index (DXY):
  - Severe: ±1.5%+
  - Major: ±0.75-1.5%
  - Moderate: ±0.3-0.75%

**2. Breadth of Impact (Multiplier):**

Assess how many markets/sectors affected:

- **Systemic (3x multiplier):** Multiple asset classes, global markets
  - Examples: FOMC surprise, banking crisis, major war outbreak

- **Cross-Asset (2x multiplier):** Equities + commodities, or equities + bonds
  - Examples: Inflation surprise, geopolitical supply shock

- **Sector-Wide (1.5x multiplier):** Entire sector or related sectors
  - Examples: Tech earnings cluster, energy policy announcement

- **Stock-Specific (1x multiplier):** Single company (unless mega-cap with index impact)
  - Examples: Individual company earnings, M&A

**3. Forward-Looking Significance (Modifier):**

Consider future implications:

- **Regime Change (+50%):** Fundamental market structure shift
  - Examples: Fed pivot from hiking to cutting, major geopolitical realignment

- **Trend Confirmation (+25%):** Reinforces existing trajectory
  - Examples: Consecutive strong inflation prints, sustained earnings beats

- **Isolated Event (0%):** One-off with limited forward signal
  - Examples: Single data point within range, company-specific issue

- **Contrary Signal (-25%):** Contradicts prevailing narrative
  - Examples: Good news ignored by market, bad news rallied

**Impact Score Calculation:**

```
Impact Score = (Price Impact Score × Breadth Multiplier) + Forward-Looking Modifier

Price Impact Score:
- Severe: 10 points
- Major: 7 points
- Moderate: 4 points
- Minor: 2 points
- Negligible: 1 point
```

**Example Calculations:**

**FOMC 75bps Rate Hike (hawkish tone):**
- Price Impact: S&P 500 -2.5% (Severe = 10 points)
- Breadth: Systemic (equities, bonds, USD, commodities all moved) = 3x
- Forward: Trend confirmation (ongoing tightening) = +25%
- **Score: (10 × 3) × 1.25 = 37.5**

**NVIDIA Earnings Beat:**
- Price Impact: NVDA +15%, Nasdaq +1.5% (Severe = 10 points)
- Breadth: Sector-wide (semis, tech broadly) = 1.5x
- Forward: Trend confirmation (AI demand) = +25%
- **Score: (10 × 1.5) × 1.25 = 18.75**

**Geopolitical Flare-up (Middle East):**
- Price Impact: Oil +8%, S&P -1.2% (Severe = 10 points)
- Breadth: Cross-asset (oil, equities, gold) = 2x
- Forward: Isolated event (no escalation) = 0%
- **Score: (10 × 2) × 1.0 = 20**

**Single Stock Earnings (Non-Mega-Cap):**
- Price Impact: Stock +12%, no index impact (Major = 7 points)
- Breadth: Stock-specific = 1x
- Forward: Isolated = 0%
- **Score: (7 × 1) × 1.0 = 7**

**Ranking:**
After scoring all news items, rank from highest to lowest impact score. This determines report ordering.

### Step 4: Market Reaction Analysis

**Objective:** Analyze how markets actually responded to each event.

For each significant news item (Impact Score >5), conduct detailed reaction analysis:

**Immediate Reaction (Intraday):**
- Direction: Positive, negative, mixed
- Magnitude: Align with price impact categories
- Timing: Pre-market, during trading, after-hours
- Volatility: VIX movement, bid-ask spreads

**Multi-Asset Response:**

**Equities:**
- Index performance (S&P 500, Nasdaq, Dow, Russell 2000)
- Sector rotation (which sectors outperformed/underperformed)
- Individual stock moves (mega-caps, relevant companies)
- Growth vs Value, Large vs Small Cap divergences

**Fixed Income:**
- Treasury yields (2Y, 10Y, 30Y)
- Yield curve shape (steepening, flattening, inversion)
- Credit spreads (IG, HY)
- TIPS breakevens (inflation expectations)

**Commodities:**
- Energy: Oil (WTI, Brent), Natural Gas
- Precious Metals: Gold, Silver
- Base Metals: Copper, Aluminum (if relevant)
- Agricultural: Wheat, Corn, Soybeans (if relevant)

**Currencies:**
- USD Index (DXY)
- EUR/USD, USD/JPY, GBP/USD
- Emerging market currencies
- Safe havens (JPY, CHF)

**Derivatives:**
- VIX (volatility index)
- Options activity (put/call ratio, unusual volume)
- Futures positioning

**Pattern Comparison:**

Compare observed reaction against expected pattern from knowledge base:

- **Consistent:** Reaction matched historical pattern
  - Example: Fed hike → Tech stocks down, USD up (as expected)

- **Amplified:** Reaction exceeded typical pattern
  - Example: Inflation print +0.3% above consensus → Selloff 2x typical
  - Investigate: Positioning, sentiment, cumulative factors

- **Dampened:** Reaction less than historical pattern
  - Example: Geopolitical event → Oil barely moved
  - Investigate: Already priced in, other offsetting factors

- **Inverse:** Reaction opposite of historical pattern
  - Example: Good news ignored, bad news rallied
  - Investigate: "Good news is bad news" dynamics, Fed pivot hopes

**Anomaly Identification:**

Flag reactions that deviate significantly from patterns:
- Market shrugged off typically market-moving news
- Overreaction to typically minor news
- Contagion failed to spread as expected
- Safe havens didn't work (correlations broke)

**Sentiment Indicators:**

- Risk-On vs Risk-Off: Which regime dominated
- Positioning: Evidence of crowded trades unwinding
- Momentum: Follow-through in subsequent sessions or reversal

### Step 4.5: Structural Implication Analysis (Deep Layer)

**Objective:** Go beyond surface-level market reactions to analyze the underlying structural meaning, data quality, political economy, and second/third-order effects of each event. This is the layer that separates useful analysis from headline regurgitation.

**For each significant news item (Impact Score >10), perform all five sub-analyses below. For items scoring 5-10, perform at minimum sub-analyses A and D.**

#### A. Data Noise Decomposition

**Objective:** Separate signal from noise. Determine what portion of a data point reflects genuine economic reality vs temporary distortions.

**Procedure:**

1. **Identify potential distortion factors** for each economic data release:
   - **Weather:** Extreme cold/heat, hurricanes, snowstorms that suppress economic activity temporarily (e.g., construction, retail foot traffic, outdoor work)
   - **Strikes/Labor Actions:** Large strikes (>10,000 workers) that temporarily depress payrolls in specific industries. BLS counts striking workers as "employed but not at work" only if they receive pay; unpaid strikers show as job losses
   - **Calendar Effects:** Seasonal adjustment anomalies, holiday timing shifts, survey week placement
   - **Government Shutdowns/Policy:** Federal hiring freezes, DOGE-driven layoffs, census hiring/unwinding
   - **One-Time Events:** Natural disasters, pandemic aftereffects, large company bankruptcy affecting a single metro area
   - **Revisions Context:** How much were prior months revised? Persistent downward revisions signal systematic overcount, not noise

2. **Quantify the distortion** where possible:
   - Search for analyst estimates of temporary factors (e.g., "Kaiser strike impact on NFP estimated at -28K to -32K")
   - Calculate "adjusted" headline number removing identified noise (e.g., NFP -92K + Kaiser strike +28K = adjusted -64K, still weak but less alarming)
   - Note confidence level in the adjustment (High/Medium/Low)

3. **Assess underlying trend:**
   - Compare against 3-month and 6-month moving averages
   - Look at diffusion index (breadth of job gains/losses across industries)
   - Check if "noise" explanation is consistent across multiple data points or cherry-picked

**Output format for report:**

```
**Noise Decomposition:**
- Headline: [raw number]
- Identified distortions: [factor 1: ±X], [factor 2: ±X]
- Adjusted estimate: [number] (confidence: High/Medium/Low)
- Underlying trend: [assessment]
- Verdict: [Genuine deterioration / Temporary distortion / Mixed signal]
```

**Example:**
```
**Noise Decomposition:**
- Headline: NFP -92,000
- Identified distortions: Kaiser Permanente strike +28K, unusually cold February weather +15K (est.)
- Adjusted estimate: -49,000 (confidence: Medium)
- Underlying trend: 3-month avg declining from +180K to +20K; diffusion index narrowing
- Verdict: Mixed signal — headline exaggerated by temp factors, but underlying trend genuinely weakening
```

#### B. Political Economy Analysis

**Objective:** Analyze who benefits, who loses, and what policy responses are likely. Markets move not just on what happened but on what policymakers will do next.

**Framework — "Cui Bono" (Who Benefits):**

1. **Identify key stakeholders** affected by each event:
   - White House / Administration (election cycle, approval ratings)
   - Federal Reserve (dual mandate constraints)
   - Congress (legislative agenda, fiscal policy)
   - Foreign governments (trade partners, adversaries)
   - Corporate sector (specific industries, lobbying power)
   - Consumers / Voters (inflation pain, employment)

2. **Assess policy response incentives:**
   - **What does the administration want?** (e.g., lower oil prices before midterms → SPR release likely; strong jobs → no urgency on stimulus)
   - **What can the Fed do?** (e.g., stagflation = no good options → likely to wait; clear recession = cut aggressively)
   - **What is Congress likely to approve?** (e.g., bipartisan support for energy independence spending; partisan gridlock on fiscal stimulus)
   - **What will foreign actors do?** (e.g., OPEC response to war premium; China's tariff retaliation calibrated to maximize pain vs minimize self-harm)

3. **Evaluate credibility of official statements:**
   - Does the statement match incentive structure? (e.g., Trump saying "war ending soon" when oil at $119 and approval dropping → high incentive to say this regardless of military reality)
   - Track record of follow-through on similar statements
   - Gap between rhetoric and policy action
   - Reference TACO framework for Trump-specific policy reversal patterns when applicable

4. **Historical policy analogs:**
   - Similar situations in the past → what did policymakers actually do?
   - Time lag between event and policy response
   - Effectiveness of past interventions

**Output format for report:**

```
**Political Economy:**
- Key stakeholders: [list with interests]
- Most likely policy response: [action, timeline, probability]
- Statement credibility: [High/Medium/Low] — [reasoning]
- Historical analog: [past event → policy response → outcome]
- Market implication: [what the policy response means for positioning]
```

#### C. Second and Third-Order Effects

**Objective:** Trace causal chains beyond the immediate market reaction. The real money is made anticipating effects that are 2-3 steps downstream.

**Causal Chain Mapping:**

For each event, map at least 2 levels of downstream effects:

```
1st Order (immediate): [Event] → [Direct market reaction]
2nd Order (weeks): [Direct reaction] → [Economic/policy consequence]
3rd Order (months): [Consequence] → [Structural shift or reversal]
```

**Example — Oil at $100:**
```
1st Order: Hormuz closure → Oil +50%, energy stocks rally
2nd Order: $100 oil → Gasoline $5+/gal → Consumer spending compression → Retail/restaurant earnings miss → Discretionary sector selloff
3rd Order: Sustained high oil → SPR depletion / US shale ramp-up / Iran peace pressure → Oil supply normalizes → Energy sector gives back gains, but inflation stickiness remains
```

**Example — NFP -92K:**
```
1st Order: Weak NFP → Recession fears → Equities sell, bonds bid
2nd Order: If noise-adjusted NFP is -49K → Less alarming → March rebound likely → "False alarm" narrative → Relief rally
3rd Order: But if trend is genuinely weakening → Q2 earnings downgrades → Revenue misses cascade → Correction deepens regardless of March bounce
```

**Key questions to ask:**
- What breaks if this situation persists for 3 more months?
- Who is forced to act (margin calls, policy intervention, corporate restructuring)?
- What secondary markets are affected that headlines ignore? (e.g., shipping insurance, agricultural inputs, EM debt)
- Is there a reflexivity loop? (e.g., oil high → recession fear → oil demand drops → oil price self-corrects)

#### D. Narrative Stress Test

**Objective:** Test whether the dominant market narrative is supported by evidence or is an oversimplification that markets will eventually correct.

**Procedure:**

1. **State the prevailing narrative** clearly (e.g., "Stagflation is here — high inflation + weak jobs")

2. **Gather supporting evidence:**
   - Data points that support the narrative
   - Market positioning consistent with narrative (flows, options, surveys)

3. **Gather contradicting evidence:**
   - Data points that undermine the narrative
   - Structural factors the narrative ignores
   - Historical episodes where similar narratives proved wrong

4. **Assess narrative durability:**
   - **Strong:** Multiple independent data points confirm; structural factors support; no contradicting evidence of comparable weight
   - **Moderate:** Some supporting data but key caveats; narrative could survive 1-2 contrary data points
   - **Fragile:** Depends on 1-2 data points that have known distortions; one contrary release could shatter it
   - **Premature:** Insufficient data to confirm; market is extrapolating from too few observations

**Example — "Stagflation" narrative stress test:**
```
Supporting: NFP -92K, wages +3.8%, oil $100+, CPI expected to rise
Contradicting: Kaiser strike distorted NFP by -28K; oil spike is geopolitical (temporary if war ends); Jan CPI was 2.4% (within range); unemployment 4.4% (not crisis level)
Assessment: **Fragile** — narrative depends on (a) war continuing and (b) March NFP also being weak. One positive surprise could collapse it. However, if 3/11 CPI confirms upward pressure, narrative strengthens to Moderate.
```

5. **Identify the "narrative break" catalyst:** What single data point or event would invalidate the current narrative? This is the highest-information event to watch for.

#### E. Structural vs Transitory Assessment

**Objective:** Determine whether each event represents a permanent structural shift or a temporary disruption that will mean-revert.

**Classification Framework:**

| Factor | Structural (Permanent) | Transitory (Temporary) |
|--------|----------------------|----------------------|
| **Cause** | Policy change, demographic shift, technology disruption | Weather, strike, one-time shock, supply disruption |
| **Duration** | Persists after initial cause removed | Reverses when cause removed |
| **Precedent** | No close historical analog, or analog led to permanent change | Multiple past episodes that mean-reverted |
| **Policy response** | Requires structural reform | Can be addressed with temporary measures (SPR, emergency rates) |
| **Market pricing** | Should be priced into long-term valuations (DCF changes) | Should be faded after initial shock (mean-reversion trade) |

**For each event, assign:**
- **Classification:** Structural / Transitory / Uncertain
- **Confidence:** High / Medium / Low
- **Mean-reversion timeline:** If transitory, estimated duration (days / weeks / months)
- **Trading implication:** Fade the move vs position for continuation

**Key principle:** Markets systematically overweight dramatic headlines and underweight base rates. Most "regime changes" are actually temporary disruptions. But occasionally the market is right — the skill is distinguishing which.

---

### Step 5: Correlation and Causation Assessment

**Objective:** Distinguish direct impacts from coincidental timing.

**Multi-Event Analysis:**

When multiple significant events occurred in the 10-day period, assess interactions:

**Reinforcing Events:**
- Same directional impact
- Example: Hawkish FOMC + hot CPI → Both bearish for equities, amplified move
- Combined impact often non-linear (greater than sum of parts)

**Offsetting Events:**
- Opposite directional impacts
- Example: Strong earnings (positive) + geopolitical tensions (negative) → Muted net reaction
- Identify which factor dominated

**Sequential Events:**
- One event set up reaction to next
- Example: First rate hike modest reaction, second rate hike severe (cumulative tightening concerns)
- Path dependence matters

**Coincidental Timing:**
- Events unrelated but occurred simultaneously
- Difficult to isolate individual impacts
- Note uncertainty in attribution

**Geopolitical-Commodity Correlations:**

For geopolitical events, specifically analyze commodity market reactions using geopolitical_commodity_correlations.md:

**Energy:**
- Map conflict/sanction to supply disruption risk
- Assess actual vs feared supply impact
- Duration: Temporary spike vs sustained elevation

**Precious Metals:**
- Safe-haven flows vs real rate drivers
- Gold response to risk-off events
- Central bank buying implications

**Industrial Metals:**
- Demand destruction from economic slowdown fears
- Supply chain disruptions
- China factor in copper, aluminum

**Agriculture:**
- Black Sea grain exports (Russia-Ukraine)
- Weather overlays
- Food security policy responses

**Transmission Mechanisms:**

Trace how news impacts flowed through markets:

**Direct Channel:**
- News → Immediate asset price reaction
- Example: OPEC cuts → Oil prices up immediately

**Indirect Channels:**
- News → Economic impact → Asset prices
- Example: Rate hike → Mortgage rates up → Housing slows → Homebuilder stocks down

**Sentiment Channel:**
- News → Risk appetite shift → Broad asset reallocation
- Example: Banking crisis → Flight to quality → Treasuries rally, stocks sell

**Feedback Loops:**
- Initial reaction creates secondary effects
- Example: Stock selloff → Margin calls → Forced selling → Deeper selloff

### Step 6: Report Generation

**Objective:** Create structured English Markdown report ranked by market impact.

**Report Structure:**

```markdown
# Market News Analysis Report - [Date Range]

## Executive Summary

[3-4 sentences covering:]
- Period analyzed (specific dates)
- Number of significant events identified
- Dominant market theme/regime (risk-on/risk-off, sector rotation)
- Top 1-2 highest-impact events

## Market Impact Rankings

[Table format, sorted by Impact Score descending]

| Rank | Event | Date | Impact Score | Asset Classes Affected | Market Reaction |
|------|-------|------|--------------|------------------------|-----------------|
| 1 | [Event] | [Date] | [Score] | [Equities, Commodities, etc.] | [Brief reaction] |
| 2 | ... | ... | ... | ... | ... |

---

## Detailed Event Analysis

[For each event in rank order, provide comprehensive analysis]

### [Rank]. [Event Name] (Impact Score: [X])

**Event Date:** [Date, Time]
**Event Type:** [Monetary Policy / Earnings / Geopolitical / Economic Data / Corporate]
**News Source:** [Source, with credibility tier]

#### Event Summary
[3-4 sentences describing what happened]
- Key details (e.g., rate decision, earnings beat/miss magnitude, conflict developments)
- Context (was this expected, surprise factor)
- Forward guidance or implications stated

#### Market Reaction

**Immediate (Day-of):**
- **Equities:** S&P 500 [+/-X%], Nasdaq [+/-X%], Sector rotation [details]
- **Bonds:** 10Y yield [change], credit spreads [movement]
- **Commodities:** Oil [+/-X%], Gold [+/-X%], Copper [+/-X%] (if relevant)
- **Currencies:** USD [+/-X%], [other relevant pairs]
- **Volatility:** VIX [level/change]

**Follow-Through (Subsequent Sessions):**
- [Direction: sustained, reversed, or consolidated]
- [Additional price action details if significant]

**Pattern Comparison:**
- **Expected Reaction:** [Based on historical patterns from knowledge base]
- **Actual vs Expected:** [Consistent / Amplified / Dampened / Inverse]
- **Explanation of Deviation:** [If applicable, why reaction differed]

#### Impact Assessment Detail

**Asset Price Impact:** [Severe/Major/Moderate/Minor] - [Justification]
**Breadth:** [Systemic/Cross-Asset/Sector/Stock-Specific] - [Affected markets]
**Forward Significance:** [Regime Change/Trend Confirmation/Isolated/Contrary] - [Rationale]

**Calculated Score:** ([Price Score] × [Breadth Multiplier]) × [Forward Modifier] = [Total]

#### Sector-Specific Impacts

[If relevant, detail which sectors/industries were most affected]
- [Sector 1]: [Impact and reason]
- [Sector 2]: [Impact and reason]
- [Example: Technology -3% (rate sensitivity), Energy +5% (oil price spillover)]

#### Structural Implications (Deep Analysis)

**Noise Decomposition:** [For economic data events]
- Headline: [raw number]
- Identified distortions: [factor 1: ±X], [factor 2: ±X]
- Adjusted estimate: [number] (confidence: High/Medium/Low)
- Underlying trend: [assessment]
- Verdict: [Genuine deterioration / Temporary distortion / Mixed signal]

**Political Economy:**
- Key stakeholders: [list with interests]
- Most likely policy response: [action, timeline, probability]
- Statement credibility: [High/Medium/Low] — [reasoning]
- Historical analog: [past event → policy response → outcome]

**Causal Chain (2nd/3rd Order Effects):**
```
1st Order: [immediate reaction]
2nd Order: [downstream consequence in weeks]
3rd Order: [structural implication in months]
```

**Narrative Stress Test:**
- Prevailing narrative: [state clearly]
- Supporting evidence: [list]
- Contradicting evidence: [list]
- Durability: [Strong/Moderate/Fragile/Premature]
- Narrative break catalyst: [what would invalidate this]

**Structural vs Transitory:** [Classification] (Confidence: [H/M/L])
- Mean-reversion timeline: [if transitory]
- Trading implication: [fade vs continuation]

#### Geopolitical-Commodity Correlation Analysis

[Include this section only for geopolitical events]
- [Specific commodity affected]: [Price movement]
- [Supply/demand mechanism]: [Explanation]
- [Historical precedent]: [Comparison to similar past events]
- [Expected duration]: [Temporary shock vs sustained impact]

[Repeat detailed analysis for each ranked event]

---

## Thematic Synthesis

### Dominant Market Narrative
[Identify overarching theme across the 10-day period]
- [E.g., "Persistent inflation concerns dominated despite mixed economic data"]
- [E.g., "Tech sector strength drove markets higher despite geopolitical headwinds"]

### Interconnected Events
[Analyze how events related or compounded]
- [Event A] + [Event B] → [Combined impact analysis]
- [Sequential causation if applicable]

### Market Regime Assessment
**Risk Appetite:** [Risk-On / Risk-Off / Mixed]
**Evidence:**
- [Supporting indicators: sector performance, safe haven flows, credit spreads, VIX]

**Sector Rotation Trends:**
- [Growth vs Value]
- [Cyclicals vs Defensives]
- [Outperformers and underperformers]

### Anomalies and Surprises
[Highlight unexpected market reactions]
1. [Event]: Market reacted [unexpectedly] because [explanation]
2. [Continue for significant anomalies]

### Narrative vs Reality Assessment

[For each dominant market narrative, provide structured stress test]

#### Narrative 1: "[State the prevailing narrative]"

**Supporting Evidence:**
- [Data point 1]
- [Data point 2]

**Contradicting Evidence:**
- [Counter-data 1 — why headline may be misleading]
- [Counter-data 2 — structural factors ignored]

**Noise-Adjusted Reality:**
- [What the data actually says after removing temporary distortions]

**Durability Assessment:** [Strong / Moderate / Fragile / Premature]

**Narrative Break Catalyst:** [The single event/data point that would invalidate this narrative — this is the highest-information item to monitor]

**Investment Implication:** [If narrative is correct → positioning A. If narrative breaks → positioning B. Probability-weight accordingly.]

[Repeat for each major narrative, typically 1-3]

### Political Economy Outlook

[Synthesize political economy analysis across all events]
- **Administration priorities:** [What does the White House need most right now?]
- **Fed constraints:** [What can/can't the Fed do given current conditions?]
- **Policy response probability matrix:**
  - [Policy action 1]: [probability, timeline, market impact]
  - [Policy action 2]: [probability, timeline, market impact]
- **Key stakeholder to watch:** [Whose next move matters most?]

---

## Commodity Market Deep Dive

[Dedicated section for commodity movements]

### Energy
- **Crude Oil (WTI/Brent):** [Price level, % change over period, key drivers]
- **Natural Gas:** [If significant movement]
- **Key Events:** [Specific news impacting energy: OPEC, geopolitics, inventory data]

### Precious Metals
- **Gold:** [Price level, % change, safe-haven flows vs real rate dynamics]
- **Silver:** [If significant divergence from gold]
- **Drivers:** [Geopolitical risk premium, inflation hedging, USD strength]

### Base Metals
- **Copper:** [As economic barometer - demand signals]
- **Aluminum, Nickel:** [If relevant supply/demand news]
- **China Factor:** [Impact of Chinese economic data/policy]

### Agricultural (If Relevant)
- **Grains:** [Wheat, Corn, Soybeans - weather, Ukraine conflict impacts]

[For each commodity, reference geopolitical events from main analysis and draw correlations]

---

## Forward-Looking Implications

### Market Positioning Insights
[What the news suggests for current market positioning]
- [Trend continuation or reversal signals]
- [Overvaluation or undervaluation indications]
- [Sentiment extremes (complacency or panic)]

### Upcoming Catalysts
[Events on horizon that may be set up by recent news]
- [Next FOMC meeting expectations post-recent decision]
- [Upcoming earnings seasons based on guidance]
- [Geopolitical developments to monitor]

### Risk Scenarios
[Based on recent news, identify key risks]
1. **[Risk Name]:** [Description, probability, potential impact]
2. **[Risk Name]:** [Description, probability, potential impact]
3. [Continue for 3-5 key risks]

---

## Data Sources and Methodology

### News Sources Consulted
[List primary sources used, organized by tier]
- **Supabase Breaking News Feed:** [Valley.town crawler — if used, note item count and date range]
- **Official Sources:** [e.g., FederalReserve.gov, SEC.gov]
- **Tier 1 Financial News:** [e.g., Bloomberg, Reuters, WSJ]
- **Specialized:** [e.g., S&P Global Platts for commodities]

### Analysis Period
- **Start Date:** [Specific date]
- **End Date:** [Specific date]
- **Total Days:** 10

### Market Data
- Equity indices: [Data sources]
- Commodity prices: [Data sources]
- Economic data: [Government sources]

### Knowledge Base References
- `market_event_patterns.md` - Historical reaction patterns
- `geopolitical_commodity_correlations.md` - Geopolitical-commodity frameworks
- `corporate_news_impact.md` - Mega-cap impact analysis
- `trusted_news_sources.md` - Source credibility assessment

---

*Analysis Date: [Date report generated]*
*Language: English*
*Analysis Thinking: English*

```

**File Naming Convention:**
`market_news_analysis_[START_DATE]_to_[END_DATE].md`

Example: `market_news_analysis_2024-10-25_to_2024-11-03.md`

**Report Quality Standards:**
- Objective, fact-based analysis (no speculation beyond probability-weighted scenarios)
- Quantify price movements with specific percentages
- Cite sources for major claims
- Distinguish between correlation and causation
- Acknowledge uncertainty when attributing market moves to specific news
- Use proper financial terminology
- Maintain consistent English throughout

## Key Analysis Principles

When conducting market news analysis:

1. **Impact Over Noise:** Focus on truly market-moving news, filter out minor events
2. **Multi-Asset Perspective:** Analyze across equities, bonds, commodities, currencies to understand full impact
3. **Pattern Recognition:** Compare against historical precedents while noting unique aspects
4. **Causation Discipline:** Be rigorous about attributing market moves to specific news vs coincidental timing
5. **Forward-Looking:** Emphasize implications for future market behavior, not just backward-looking description
6. **Objectivity:** Separate market reaction (what happened) from personal market view (what should happen)
7. **Quantification:** Use specific numbers (%, bps) rather than vague terms ("significant," "large")
8. **Source Credibility:** Weight official sources and Tier 1 news over rumors and unverified reports
9. **Breadth Analysis:** Individual stock moves only significant if mega-cap or systemic signal
10. **English Consistency:** All thinking, analysis, and output in English for consistency
11. **Signal vs Noise:** Always decompose economic data into structural signal and temporary noise (weather, strikes, calendar effects, revisions). The headline number is the starting point, not the conclusion
12. **Political Economy Lens:** Every major event triggers a policy response. Analyze who benefits, who is incentivized to act, and what policymakers are most likely to do — the policy response often matters more than the event itself
13. **Narrative Skepticism:** Market narratives simplify complex reality. Actively stress-test dominant narratives by gathering contradicting evidence. Identify the "narrative break" catalyst — the single data point that would invalidate the consensus story
14. **Second-Order Thinking:** The obvious first-order effect is already priced in. Focus analytical effort on second and third-order consequences that markets haven't fully discounted
15. **Structural vs Transitory Discipline:** Most dramatic headlines are transitory disruptions that mean-revert. Reserve "regime change" designation for events with genuine structural permanence. When in doubt, assume transitory

## Common Pitfalls to Avoid

**Over-Attribution:**
- Not every market move is news-driven (technicals, flows, month-end rebalancing exist)
- Acknowledge when attribution is uncertain

**Recency Bias:**
- Latest news isn't always most important
- Rank by actual impact, not chronological order

**Hindsight Bias:**
- Distinguish "obvious in retrospect" from "surprising at the time"
- Note consensus expectations vs actual outcomes

**Single-Factor Analysis:**
- Markets respond to multiple factors simultaneously
- Acknowledge interaction effects

**Ignoring Magnitude:**
- A "hot" CPI that's 0.1% above consensus is different from 0.5% above
- Quantify surprise factor

**Headline Literalism:**
- Taking economic data at face value without decomposing noise factors
- Example: NFP -92K looks catastrophic but may include -28K from a strike that already ended + weather effects
- Always search for "what distorted this number?" before concluding "the economy is collapsing"
- Check prior month revisions — persistent downward revisions ARE signal, but a single miss can be noise

**Narrative Capture:**
- Adopting the dominant market narrative without stress-testing it
- Markets are frequently wrong about narratives (e.g., "transitory inflation" in 2021, "hard landing certain" in 2023)
- Always present both the bull and bear case for any narrative
- Ask: "What would change my mind?" — if nothing, the analysis is biased

**Ignoring Policy Response:**
- Analyzing events in a vacuum without considering how policymakers will respond
- Events are temporary; policy responses can be permanent
- Example: Oil at $100 is bearish for consumers, but SPR release + shale production increase + diplomatic pressure are all likely responses that partially offset the impact

**Confusing Correlation with Causation in Political Statements:**
- A president saying "the war is ending" does not mean the war is ending
- Evaluate statements against the speaker's incentive structure, track record, and concrete actions
- Political statements move markets intraday; follow-through (or lack thereof) moves markets over weeks

## Resources

### references/

**market_event_patterns.md** - Comprehensive knowledge base covering:
- Central bank monetary policy events (FOMC, ECB, BOJ, PBOC)
- Inflation data releases (CPI, PPI, PCE)
- Employment data (NFP, unemployment, wages)
- GDP reports
- Geopolitical events (conflicts, trade wars, sanctions)
- Corporate earnings (mega-cap technology, banks, energy)
- Credit events and rating changes
- Commodity-specific events (OPEC, weather, supply disruptions)
- Recession indicators
- Historical case studies (2008 crisis, COVID-19, 2022 inflation)
- Pattern recognition framework and sentiment analysis

**geopolitical_commodity_correlations.md** - Detailed correlations covering:
- Energy commodities (crude oil, natural gas, coal) and geopolitical conflicts
- Precious metals (gold, silver, platinum, palladium) safe-haven dynamics
- Base metals (copper, aluminum, nickel, zinc) and economic/political risks
- Agricultural commodities (wheat, corn, soybeans) and weather/policy
- Rare earth elements and critical minerals (China dominance, supply security)
- Regional geopolitical frameworks (Middle East, Russia-Europe, Asia-Pacific, Latin America)
- Correlation summary tables
- Time horizon considerations

**corporate_news_impact.md** - Mega-cap analysis framework:
- "Magnificent 7" technology stocks (NVIDIA, Apple, Microsoft, Amazon, Meta, Google, Tesla)
- Financial sector mega-caps (JPMorgan, Bank of America, etc.)
- Healthcare mega-caps (UnitedHealth, Pfizer, J&J, Merck)
- Energy mega-caps (Exxon Mobil, Chevron)
- Consumer staples mega-caps (P&G, Coca-Cola, PepsiCo)
- Industrial mega-caps (Boeing, Caterpillar)
- Earnings impact frameworks, product launches, M&A, regulatory issues
- Sector contagion patterns
- Impact magnitude framework

**trusted_news_sources.md** - Source credibility guide:
- Tier 1 primary sources (central banks, government agencies, SEC)
- Tier 2 major financial news (Bloomberg, Reuters, WSJ, FT, CNBC)
- Tier 3 specialized sources (energy, tech, emerging markets, China-specific, crypto)
- Tier 4 analysis and research (independent research, central bank publications, think tanks)
- Search and aggregation tools
- Source quality assessment criteria
- Speed vs accuracy trade-offs
- Recommended search strategies for 10-day analysis
- Source credibility framework
- Red flag sources to avoid

## Important Notes

- 리포트를 한국어로 작성한다. 종목 티커, 기술 지표명, 숫자 데이터는 영어/원본 유지.
- When Supabase MCP is available, query breaking news DB first (Step 0.5) before WebSearch
- Use WebSearch and WebFetch tools to collect news automatically (as primary source or gap-filler)
- Focus on trusted news sources as defined in references
- Rank events by impact score (price impact × breadth × forward significance)
- Target analysis period: Past 10 days from current date
- Emphasize US equity markets and commodities as primary analysis subjects
- FOMC and other central bank policy decisions receive highest priority analysis
- Distinguish between correlation and causation rigorously
- Quantify all market reactions with specific percentages
- Load appropriate reference files based on news types collected
- Generate comprehensive reports ranked by market impact (highest impact first)
