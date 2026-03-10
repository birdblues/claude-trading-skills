# Domain Trigger Levels and Normalization Parameters

## Domain Configuration

### Energy / Oil (Weight: 30%)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Proxy | USO ETF (WTI tracking) | Liquid, accessible via FMP |
| Midpoint | $90 WTI | Gas price complaints escalate above $3.50/gal |
| Steepness | 0.08 | Gradual — price changes take weeks to reach consumers |
| Low Pain | < $70 | Comfortable — no political pressure |
| High Pain | > $110 | Crisis — "do something" headline territory |
| Extreme Pain | > $130 | Emergency intervention almost certain |

**Market Response Speed:** Immediate (WTI drops on intervention announcement)

**Executive Levers:**
- Strategic Petroleum Reserve (SPR) releases
- OPEC+ diplomatic pressure
- Sanctions waivers for oil-producing nations
- Pipeline/drilling permit acceleration

### Stock Market (Weight: 25%)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Proxy | ^GSPC (S&P 500) | Benchmark index, politically visible |
| Metric | Drawdown from 52-week high (%) | ATH-relative performance |
| Midpoint | -10% | Correction territory triggers "concern" |
| Steepness | 0.30 | Sharp — political sensitivity is binary (headlines) |
| Low Pain | < -3% | Normal volatility, no concern |
| High Pain | > -15% | Bear market narrative begins |
| Extreme Pain | > -20% | Full crisis mode |

**Market Response Speed:** Fast (verbal intervention moves futures)

**Executive Levers:**
- Verbal ("market is great", "buying opportunity")
- Trade de-escalation (remove tariff overhang)
- Tax/regulatory announcements
- Pressure on Fed (indirect)

### Geopolitics (Weight: 20%)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Input | Manual 1-10 scale | Complex domain, not reducible to single metric |
| Midpoint | 5 | Moderate tension (normal diplomatic friction) |
| Steepness | 0.60 | Moderate — escalation is non-linear but somewhat gradual |

**Scoring Guide:**
| Score | Description |
|-------|-------------|
| 1-2 | Peace / active diplomacy / summits |
| 3-4 | Normal tensions / sanctions in place |
| 5-6 | Elevated tensions / military posturing |
| 7-8 | Active conflict / alliance stress / refugee crisis |
| 9-10 | Full-scale war / nuclear threat / global crisis |

**Market Response Speed:** Variable (days to weeks depending on escalation type)

**Executive Levers:**
- "Mission accomplished" declarations
- Summit announcements
- Troop withdrawal signals
- Diplomatic channel openings

### Trade / Tariffs (Weight: 15%)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Input | Manual 1-10 scale | Multi-dimensional (tariff rates, retaliation, supply chains) |
| Midpoint | 5 | Moderate trade friction |
| Steepness | 0.60 | Moderate — tariff impacts accumulate over weeks |

**Scoring Guide:**
| Score | Description |
|-------|-------------|
| 1-2 | Free trade / deals signed / tariffs removed |
| 3-4 | Targeted tariffs / ongoing negotiations |
| 5-6 | Broad tariffs / retaliation announced |
| 7-8 | Trade war escalation / supply chain disruption |
| 9-10 | Full decoupling / consumer price crisis / stagflation fears |

**Market Response Speed:** 1-3 weeks (supply chain effects take time)

**Executive Levers:**
- Tariff exemptions (most direct)
- "Pause" announcements
- Bilateral deal frameworks
- Section 122 waivers

### Interest Rates (Weight: 10%)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Proxy | TLT ETF (inverse yield proxy) | 20Y Treasury bond ETF |
| Metric | Estimated 10Y yield (%) | Core rate that drives mortgages/business lending |
| Midpoint | 5.0% | Psychological threshold for "rates too high" |
| Steepness | 1.00 | Sharp — small yield changes have large economic impact |
| Low Pain | < 4.0% | Comfortable — accommodative environment |
| High Pain | > 5.5% | Economic drag headlines |
| Extreme Pain | > 6.0% | Housing/credit crisis territory |

**Market Response Speed:** Months (rate effects are slow-moving)

**Executive Levers (limited):**
- Verbal Fed criticism (low effectiveness)
- Treasury issuance changes (indirect)
- Regulatory easing to offset rate drag
- Deficit reduction signals (theoretical only)

**Note:** This domain has the lowest weight because the administration has the fewest direct levers. Fed independence limits intervention effectiveness.

## Cross-Domain Interactions

| Trigger | Secondary Effects |
|---------|-------------------|
| Geopolitical de-escalation | Energy relief (WTI drops), risk-on for stocks |
| Trade deal announcement | Consumer stocks rally, USD/CNY stabilizes |
| Energy price spike | Consumer spending pressure, trade retaliation risk |
| Stock market crash | All domains activate — full TACO probability spikes |
| Rate spike | Housing slowdown → stock market pressure (lagged) |

## Normalization Function Reference

All domains use the same sigmoid function with domain-specific parameters:

```python
def sigmoid_normalize(value, midpoint, steepness):
    x = steepness * (value - midpoint)
    return 1 / (1 + exp(-x))
```

The output is a 0-1 score where:
- 0.0 = no pain (below threshold)
- 0.5 = at midpoint (50% pain)
- 1.0 = maximum pain (well above threshold)

The composite Pain Index is the weighted sum of all domain scores × 100.
