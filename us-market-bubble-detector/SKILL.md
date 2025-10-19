---
name: us-market-bubble-detector
description: Evaluates US stock market bubble risk through crowd psychology and social contagion using the Minsky/Kindleberger framework. Supports practical investment decisions (profit-taking, risk management, short timing). Use when user asks about market euphoria, bubble risk, valuation concerns, profit-taking timing, or observes social phenomena like "taxi drivers giving stock tips" or "everyone talking about stocks".
---

# US Market Bubble Detection Skill

## Overview

This skill evaluates the degree of bubble in the US stock market based on **the phase of crowd psychology rather than price levels**, and proposes practical investment actions.

### Core Concept

A true bubble is complete when these 3 conditions are met:

1. **Critical Information Cascade** - Spread to all layers (including non-investors) is complete
2. **Social Norm Inversion** - "Pain of non-conformity > Value of independent judgment"
3. **Institutionalized FOMO** - Social cost of skepticism is maximized

**Iconic Signal:** When taxi drivers or family members start recommending investments, it signals the "last buyer" cohort has entered—bubble completion is near.

## When to Use This Skill

Use this skill when:

**English:**
- User asks "Is the market in a bubble?" or "Are we in a bubble?"
- User seeks advice on profit-taking, new entry timing, or short-selling decisions
- User reports social phenomena (non-investors entering, media frenzy, IPO flood)
- User mentions narratives like "this time is different" or "revolutionary technology" becoming mainstream
- User consults about risk management for existing positions
- User observes taxi drivers, family members, or other non-investors recommending stocks

**Japanese:**
- ユーザーが「今の相場はバブルか?」と尋ねる
- 投資の利確・新規参入・空売りのタイミング判断を求める
- 社会現象(非投資家の参入、メディア過熱、IPO氾濫)を観察し懸念を表明
- 「今回は違う」「革命的技術」などの物語が主流化している状況を報告
- 保有ポジションのリスク管理方法を相談

## Workflow

### Step 1: Quantitative Evaluation with Bubble-O-Meter

Evaluate 8 indicators on a scale of 0-2 points, and determine the bubble degree by total score (0-16 points).

#### The 8 Indicators

1. **Mass Penetration** - Recommendations/mentions from non-investor layers (taxi drivers, hairdressers, family)
2. **Media Saturation** - Surge in search trends, social media, TV coverage
3. **New Entrants** - Acceleration of account openings, fund inflows
4. **Issuance Flood** - Proliferation of IPOs/SPACs/related ETFs
5. **Leverage** - Margin balances, mark-to-market P&L, funding rate bias
6. **Price Acceleration** - Returns reach upper percentiles of historical distribution
7. **Valuation Disconnect** - Fundamental explanation becomes purely "narrative"-driven
8. **Correlation & Breadth** - Even low-quality stocks rally (sign of last buyer entry)

#### Scoring Method

Evaluate each indicator through dialogue or based on market observation information provided by the user.

```bash
# Script-based evaluation (interactive)
python scripts/bubble_scorer.py --manual

# Specify scores directly
python scripts/bubble_scorer.py --scores '{"mass_penetration":2,"media_saturation":1,...}'
```

#### Judgment Criteria

| Score Range | Phase | Risk Level | Recommended Action |
|------------|-------|-----------|-------------------|
| 0-4 points | Normal | Low | Continue normal investment strategy |
| 5-8 points | Caution | Medium | Begin partial profit-taking, reduce new positions |
| 9-12 points | Euphoria | High | Accelerate stair-step profit-taking, reduce total risk budget 30-50% |
| 13-16 points | Critical | Extremely High | Major profit-taking or full hedge, consider shorts after reversal |

### Step 2: Identify Minsky/Kindleberger Phase

From the score and market observations, identify the bubble progression stage:

1. **Displacement** - New technology, institutional change, monetary easing
2. **Boom** - Self-reinforcing loop of price rises
3. **Euphoria** - FOMO becomes social norm, leverage increases
4. **Profit Taking** - Smart money begins to exit
5. **Panic** - Chain of liquidations

For detailed stage-specific characteristics, refer to `references/bubble_framework.md`.

### Step 3: Propose Practical Actions

Propose specific investment actions based on bubble stage.

#### Offense: Profit-Taking Strategy

**Stair-Step Profit-Taking (Recommended):**
```
Target Return    Profit-Taking %
+20%             25%
+40%             25%
+60%             25%
+80%             25%
```

**ATR Trailing Stop (Aggressive):**
```python
stop_price = current_price - (ATR_20day × coefficient)
# Coefficient: 2.0 (normal), 1.8 (caution), 1.5 (euphoria), 1.2 (critical)
```

#### Defense: Risk Management

**Risk Budget by Bubble Stage:**
- Normal: 100% (full position allowed)
- Caution: 70% (30% reduction)
- Euphoria: 40% (60% reduction)
- Critical: 20% or less (major reduction)

**Short-Selling Timing (Important):**

❌ Absolutely NG: Early contrarian (subjective "too high" judgment)

✅ Recommended: After confirming composite conditions (at least 3 met)
1. Weekly chart shows lower highs
2. Volume peaks out
3. Leverage indicator drops sharply
4. Media/search trends peak out
5. Weak stocks start to break down first
6. VIX surges
7. Fed/policy shift signals

### Step 4: Design Continuous Monitoring

Provide daily checklist:

**Morning Routine (5 minutes):**
1. Update Bubble-O-Meter (score 8 indicators)
2. Update ATR trailing stops
3. Check signals (Google Trends, VIX, Put/Call ratio)

For details, refer to `references/quick_reference.md` (Japanese) or `references/quick_reference_en.md` (English).

## Resource Usage Guide

### Scripts

**`scripts/bubble_scorer.py`**
- Bubble-O-Meter calculation script
- Supports interactive evaluation or JSON input
- Outputs total score, Minsky phase, recommended actions

### References

**`references/bubble_framework.md`** (Japanese) / **English version TBD**
- Detailed theoretical framework
- Explanation of Minsky/Kindleberger model
- Behavioral psychology elements
- Quantitative indicators for detection
- Detailed practical response strategies

**`references/historical_cases.md`** (Japanese) / **English version TBD**
- Analysis of past bubble cases
  - 1990s Dotcom Bubble
  - 2017 Crypto Bubble
  - 2020-21 Pandemic Bubble
- Extraction of common patterns
- Case studies and lessons

**`references/quick_reference.md`** (Japanese)
- Daily checklist
- Emergency 3-question assessment
- Quick scoring guide
- Key data sources
- Common failure patterns & solutions

**`references/quick_reference_en.md`** (English)
- Daily checklist
- Emergency 3-question assessment
- Quick scoring guide
- Key data sources
- Common failure patterns & solutions

### When to Load References

- **First use:** Load `bubble_framework.md` to understand theory
- **Need historical context:** Load `historical_cases.md` for case studies
- **Daily operations:**
  - Japanese: `quick_reference.md`
  - English: `quick_reference_en.md`
- **Need detailed criteria:** Load relevant reference sections

## Output Format

### Evaluation Report Structure

```markdown
# US Market Bubble Evaluation Report

## Overall Assessment
- Total Score: X/16 points (Y%)
- Market Phase: [Normal/Caution/Euphoria/Critical]
- Minsky Phase: [Applicable phase]
- Risk Level: [Low/Medium/High/Extremely High]

## Indicator Details
[8 indicators with scores and rationale]

## Recommended Actions

### Immediate Actions
[Specific actions]

### Risk Management
[Position sizing, stop setting]

### Short-Selling Consideration
[Condition verification and judgment]

## Continuous Monitoring
[Daily checklist items]

## Warning Signals
[Signs to watch]
```

## Important Principles

### 1. See Process, Not Price Level

Evaluate objective phase transitions of crowd psychology (information cascade, social norm inversion, institutionalized FOMO) rather than subjective "too high" judgments.

### 2. Mechanical Rules Protect Psychology

During bubbles, conformity pressure maximizes and rational judgment becomes difficult. Strict adherence to pre-determined rules (stair-step profit-taking, ATR trailing) enables investment that doesn't succumb to psychological pressure.

### 3. Abandon Perfection, Aim for Satisfaction

Selling at the peak is impossible. Prioritize "secure profit capture" with stair-step profit-taking, and manage the regret of "could have made more."

### 4. Early Contrarian Shorts Are Dangerous

It's normal for prices to rise another 2-3x after feeling "obviously too high." Only consider shorts after objective confirmation of composite conditions.

## Frequently Asked Questions

**Q: Score is in caution zone but seems likely to rise further?**
A: Bubbles "last longer than expected" is the norm. In caution zone, begin partial profit-taking and position reduction, and manage risk on the remainder with ATR trailing while following the upside.

**Q: Are comparisons to past bubbles valid?**
A: Yes. The Minsky/Kindleberger model is a pattern common to many bubbles. Refer to `references/historical_cases.md` for comparison with past cases.

**Q: Should I overreact to daily small fluctuations?**
A: No. Bubble-O-Meter updates are sufficient weekly or after important events. Daily, only update price ATR trailing stops and check major signals (VIX, trends).

**Q: What about "this time is different" for AI, crypto, and other new technologies?**
A: Even if technological innovation is real, bubble formation is a separate issue. Prices overshoot even for revolutionary technologies. The internet during the Dotcom bubble was a real revolution, but year 2000 prices were clearly excessive.

## Usage Examples

### Example 1: User Reports Social Phenomena

**Japanese:**
**User:** "最近、職場の同僚全員がNVIDIA株の話をしていて、投資経験のない人まで『絶対買うべき』と言っています。これってバブルですか?"

**English:**
**User:** "Recently, everyone at work is talking about NVIDIA stock, and even people with no investment experience are saying 'you absolutely must buy.' Is this a bubble?"

**Response:**
1. Evaluate "Mass Penetration" indicator of Bubble-O-Meter (likely score 1-2)
2. Confirm other 7 indicators through dialogue
3. Provide judgment and action recommendations based on total score
4. Explain in context of "Taxi Driver Rule"

### Example 2: User Seeks Profit-Taking Advice

**Japanese:**
**User:** "ポジションが+60%になりましたが、まだ上がりそうです。売るべきでしょうか?"

**English:**
**User:** "My position is up 60%, but it seems like it will go higher. Should I sell?"

**Response:**
1. Evaluate current Bubble-O-Meter score
2. Suggest based on stair-step profit-taking rule (25% at +60%)
3. Set ATR trailing stop for remaining position
4. Explain "aim for satisfaction" principle

### Example 3: User Considers Short Selling

**Japanese:**
**User:** "明らかに高すぎる気がします。空売りすべきですか?"

**English:**
**User:** "It seems obviously too high. Should I short?"

**Response:**
1. Warn of early contrarian risks
2. Check short-selling composite conditions (7 items)
3. Recommend waiting until at least 3 conditions are met
4. If conditions met, suggest small position (25% of normal) test entry

## Conclusion

**English:**
This skill evaluates bubbles through "crowd psychology phase" rather than "price level," supporting practical investment decisions through mechanical rules.

**Japanese:**
このスキルは、バブルを「価格水準」ではなく「群集心理の位相」で判定し、機械的ルールによる実務的な投資判断を支援します。

**Key Messages:**
- When taxi drivers talk stocks, exit
- Mechanical rules protect psychology
- Short after confirmation, take profits early
- When skepticism hurts, the end begins
