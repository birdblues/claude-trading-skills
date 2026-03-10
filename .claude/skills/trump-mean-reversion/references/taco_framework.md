# TACO Framework: Trump Always Chickens Out

## Core Concept

TACO (Trump Always Chickens Out) models Trump as a **bidirectional mean-reversion variable** in financial markets. The administration systematically clips tail risk on both sides:

- **Bear-side clipping:** When markets deteriorate sufficiently (high Pain Index), the administration reverses aggressive policies, makes conciliatory statements, or takes executive action to ease pressure. Markets snap back.
- **Bull-side clipping:** When markets are strong and political capital is high (low Pain Index), the administration pushes aggressive policies (tariff escalation, geopolitical pressure, regulatory changes) that cap further upside.

## Theoretical Basis

### Political Pain Function

The administration's tolerance for market stress is bounded. Unlike a purely ideological actor, Trump's behavior is empirically responsive to:

1. **Energy prices** — Directly affects voter sentiment (gas prices visible daily)
2. **Stock market levels** — Used as a personal scorecard; drawdowns trigger defensive action
3. **Geopolitical escalation** — Military commitments become liabilities when public fatigues
4. **Trade retaliation** — Consumer price increases from tariffs erode approval ratings
5. **Interest rates** — High rates slow housing and business investment, reducing economic growth narrative

### Sigmoid Response Curve

The Pain Index uses a sigmoid (logistic) function for each domain:

```
normalized = 1 / (1 + exp(-steepness * (value - midpoint)))
```

This captures the non-linear nature of political response:
- Below the midpoint: gradual increase in pain
- At the midpoint: inflection — 50% pain level
- Above the midpoint: rapidly approaching maximum pain

### Diminishing Returns

Each successive intervention in the same domain produces less market impact:

```
effectiveness = 1 / (1 + 0.3 * intervention_count)
```

| Intervention # | Effectiveness |
|---------------|---------------|
| 1st | 100% |
| 2nd | 77% |
| 3rd | 63% |
| 4th | 53% |
| 5th | 40% |

**Why diminishing returns?**
- Markets learn to discount verbal threats ("cry wolf" effect)
- Each reversal reduces credibility of future threats
- Institutional actors build hedging strategies around expected reversals

### Words vs Actions Discount

Not all interventions are equal:

| Type | Discount | Examples |
|------|----------|----------|
| Verbal (30%) | Heavy discount | Tweets, press conferences, "considering" statements |
| Executive Order (70%) | Moderate discount | Trade waivers, regulatory pauses, sanctions exemptions |
| Policy Action (100%) | Full impact | Actual tariff removal, treaty signing, legislation |

## Pain Index Interpretation

| Score | Zone | Administration Behavior | Market Implication |
|-------|------|------------------------|-------------------|
| 0-30 | Low | Attack mode — aggressive policies | Bull-side clipping: reduce optimistic scenarios |
| 30-60 | Medium | Oscillation — mixed signals | Minor adjustments only |
| 60-100 | High | TACO mode — expect reversal | Bear-side clipping: reduce pessimistic scenarios |

## Probability Adjustment Mechanics

### High Pain (60-100): Bear Clipping

When Pain Index is high, the Bear scenario probability is reduced because:
- Historical pattern shows policy reversal at high pain levels
- Markets have learned to "buy the Trump dip"
- Administration has direct levers (tariff exemptions, executive orders)

Freed probability is redistributed:
- 60% to Base case (most likely outcome is normalization)
- 40% to Bull case (reversal can trigger sharp relief rallies)

### Low Pain (0-30): Bull Clipping

When Pain Index is low, the Bull scenario probability is reduced because:
- Low pain = political capital to push aggressive agenda
- New tariffs, sanctions, or geopolitical escalation become more likely
- Markets are not pricing in the next policy shock

Freed probability is redistributed:
- 60% to Base case
- 40% to Bear case

### Constraints

All adjustments respect these hard limits:
- **Maximum shift:** ±20 percentage points total (one direction)
- **Floor:** 5% — no scenario probability below 5%
- **Ceiling:** 75% — no scenario probability above 75%
- **Sum invariant:** Base + Bull + Bear = 100%

## Limitations

1. **Model is descriptive, not predictive** — Past behavior may not predict future actions
2. **Black swan events** can overwhelm mean-reversion patterns
3. **Geopolitics and Trade inputs are subjective** — Manual scoring introduces analyst bias
4. **FMP market proxies are imperfect** — USO ≠ WTI, TLT ≠ 10Y yield exactly
5. **Second-term dynamics may differ** from first-term patterns
6. **Intervention timing is unpredictable** — Model estimates probability, not timing
