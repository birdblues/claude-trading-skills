---
name: options-strategy-advisor
description: 옵션 트레이딩 전략 분석 및 시뮬레이션 도구. Black-Scholes 모델 기반 이론 가격 산출, Greeks 계산, 전략 손익(P/L) 시뮬레이션, 리스크 관리 가이드를 제공합니다. 사용자가 옵션 전략 분석, covered call, protective put, spread, iron condor, earnings 플레이, 또는 옵션 리스크 관리를 요청할 때 사용하세요. 변동성 분석, 포지션 사이징, earnings 기반 전략 추천을 포함합니다. 실전형 trade simulation을 중심으로 한 교육 목적의 스킬입니다.
---

# Options Strategy Advisor

## 개요

이 스킬은 이론 가격 모델을 사용해 포괄적인 옵션 전략 분석과 교육을 제공합니다. 실시간 시장 데이터 구독 없이도 트레이더가 옵션 전략을 이해하고, 분석하고, 시뮬레이션할 수 있도록 돕습니다.

**핵심 기능:**
- **Black-Scholes Pricing**: 이론 옵션 가격 및 Greeks 계산
- **Strategy Simulation**: 주요 옵션 전략의 P/L 분석
- **Earnings Strategies**: Earnings Calendar와 연동된 실적 발표 전 변동성 플레이
- **Risk Management**: 포지션 사이징, Greeks 노출, 최대 손실/수익 분석
- **Educational Focus**: 전략과 리스크 지표에 대한 상세 설명

**데이터 소스:**
- FMP API: 주가, historical volatility, 배당, 실적 발표일
- 사용자 입력: Implied volatility (IV), risk-free rate
- 이론 모델: 가격 및 Greeks 계산용 Black-Scholes

## 이 스킬을 사용할 때

다음 상황에서 이 스킬을 사용하세요:
- 사용자가 옵션 전략을 물을 때 ("What's a covered call?", "How does an iron condor work?")
- 사용자가 전략 P/L 시뮬레이션을 원할 때 ("What's my max profit on a bull call spread?")
- 사용자가 Greeks 분석이 필요할 때 ("What's my delta exposure?")
- 사용자가 earnings 전략을 물을 때 ("Should I buy a straddle before earnings?")
- 사용자가 전략 비교를 원할 때 ("Covered call vs protective put?")
- 사용자가 포지션 사이징 가이드를 원할 때 ("How many contracts should I trade?")
- 사용자가 변동성을 물을 때 ("Is IV high right now?")

요청 예시:
- "Analyze a covered call on AAPL"
- "What's the P/L on a $100/$105 bull call spread on MSFT?"
- "Should I trade a straddle before NVDA earnings?"
- "Calculate Greeks for my iron condor position"
- "Compare protective put vs covered call for downside protection"

## 지원 전략

### Income Strategies
1. **Covered Call** - 주식을 보유하고 call 매도 (수익 창출, 상단 수익 제한)
2. **Cash-Secured Put** - 현금 담보 put 매도 (premium 수취, 주식 매수 의향)
3. **Poor Man's Covered Call** - LEAPS call + 단기 call 매도 (자본 효율적)

### Protection Strategies
4. **Protective Put** - 주식 보유 + put 매수 (보험, 하방 제한)
5. **Collar** - 주식 보유 + call 매도 + put 매수 (상방/하방 제한)

### Directional Strategies
6. **Bull Call Spread** - 낮은 strike call 매수, 높은 strike call 매도 (강세, 제한된 risk/reward)
7. **Bull Put Spread** - 높은 strike put 매도, 낮은 strike put 매수 (credit spread, 강세)
8. **Bear Call Spread** - 낮은 strike call 매도, 높은 strike call 매수 (credit spread, 약세)
9. **Bear Put Spread** - 높은 strike put 매수, 낮은 strike put 매도 (약세, 제한된 risk/reward)

### Volatility Strategies
10. **Long Straddle** - ATM call + ATM put 매수 (양방향 큰 변동 시 수익)
11. **Long Strangle** - OTM call + OTM put 매수 (straddle보다 저렴, 더 큰 변동 필요)
12. **Short Straddle** - ATM call + ATM put 매도 (무변동 시 수익, 무제한 리스크)
13. **Short Strangle** - OTM call + OTM put 매도 (무변동 시 수익, 범위 더 넓음)

### Range-Bound Strategies
14. **Iron Condor** - Bull put spread + bear call spread (박스권 움직임에서 수익)
15. **Iron Butterfly** - ATM straddle 매도, OTM strangle 매수 (좁은 박스권에서 수익)

### Advanced Strategies
16. **Calendar Spread** - 근월물 옵션 매도, 원월물 옵션 매수 (time decay에서 수익)
17. **Diagonal Spread** - strike가 다른 calendar spread (방향성 + time decay)
18. **Ratio Spread** - 비대칭 spread (한쪽 leg 계약 수를 더 많이 사용)

## 분석 워크플로

### 1단계: 입력 데이터 수집

**사용자 필수 입력:**
- 티커 심볼
- 전략 유형
- strike 가격
- 만기일(들)
- 포지션 크기(계약 수)

**사용자 선택 입력:**
- Implied Volatility (IV) - 미입력 시 Historical Volatility (HV) 사용
- Risk-free rate - 기본값은 현재 3개월 T-bill 금리(2025년 기준 약 5.3%)

**FMP API에서 조회:**
- 현재 주가
- 과거 가격(HV 계산용)
- 배당수익률
- 예정된 실적 발표일(earnings 전략용)

**사용자 입력 예시:**
```
Ticker: AAPL
Strategy: Bull Call Spread
Long Strike: $180
Short Strike: $185
Expiration: 30 days
Contracts: 10
IV: 25% (or use HV if not provided)
```

### 2단계: Historical Volatility 계산 (IV 미제공 시)

**목표:** 과거 가격 움직임으로 변동성을 추정합니다.

**방법:**
```python
# Fetch 90 days of price data
prices = get_historical_prices("AAPL", days=90)

# Calculate daily returns
returns = np.log(prices / prices.shift(1))

# Annualized volatility
HV = returns.std() * np.sqrt(252)  # 252 trading days
```

**출력:**
- Historical Volatility (연율 %)
- 사용자 안내: "HV = 24.5%, consider using current market IV for more accuracy"

**사용자 재정의 가능:**
- 브로커 플랫폼(ThinkorSwim, TastyTrade 등)에서 IV 제공
- 스크립트는 `--iv 28.0` 파라미터 지원

### 3단계: Black-Scholes로 옵션 가격 산출

**Black-Scholes 모델:**

유럽형 옵션 기준:
```
Call Price = S * N(d1) - K * e^(-r*T) * N(d2)
Put Price = K * e^(-r*T) * N(-d2) - S * N(-d1)

Where:
d1 = [ln(S/K) + (r + σ²/2) * T] / (σ * √T)
d2 = d1 - σ * √T

S = Current stock price
K = Strike price
r = Risk-free rate
T = Time to expiration (years)
σ = Volatility (IV or HV)
N() = Cumulative standard normal distribution
```

**보정:**
- call 가격 계산 시 S에서 배당의 현재가치 차감
- American 옵션: 근사값을 사용하거나 "European pricing, may undervalue American options"라고 명시

**Python 구현:**
```python
from scipy.stats import norm
import numpy as np

def black_scholes_call(S, K, T, r, sigma, q=0):
    """
    S: Stock price
    K: Strike price
    T: Time to expiration (years)
    r: Risk-free rate
    sigma: Volatility
    q: Dividend yield
    """
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    call_price = S*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    put_price = K*np.exp(-r*T)*norm.cdf(-d2) - S*np.exp(-q*T)*norm.cdf(-d1)
    return put_price
```

**각 옵션 leg 출력:**
- 이론 가격
- 안내: "Market price may differ due to bid-ask spread and American vs European pricing"

### 4단계: Greeks 계산

**Greeks**는 다양한 요인에 대한 옵션 가격 민감도를 측정합니다:

**Delta (Δ):** 주가 $1 변화 시 옵션 가격 변화량
```python
def delta_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * norm.cdf(d1)

def delta_put(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * (norm.cdf(d1) - 1)
```

**Gamma (Γ):** 주가 $1 변화 시 delta 변화량
```python
def gamma(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
```

**Theta (Θ):** 일 단위 옵션 가격 변화량(time decay)
```python
def theta_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    theta = (-S*norm.pdf(d1)*sigma*np.exp(-q*T)/(2*np.sqrt(T))
             - r*K*np.exp(-r*T)*norm.cdf(d2)
             + q*S*norm.cdf(d1)*np.exp(-q*T))

    return theta / 365  # Per day
```

**Vega (ν):** 변동성 1% 변화 시 옵션 가격 변화량
```python
def vega(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return S * np.exp(-q*T) * norm.pdf(d1) * np.sqrt(T) / 100  # Per 1%
```

**Rho (ρ):** 금리 1% 변화 시 옵션 가격 변화량
```python
def rho_call(S, K, T, r, sigma, q=0):
    d2 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T)) - sigma*np.sqrt(T)
    return K * T * np.exp(-r*T) * norm.cdf(d2) / 100  # Per 1%
```

**포지션 Greeks:**

여러 leg로 구성된 전략은 모든 leg의 Greeks를 합산합니다:
```python
# Example: Bull Call Spread
# Long 1x $180 call
# Short 1x $185 call

delta_position = (1 * delta_long) + (-1 * delta_short)
gamma_position = (1 * gamma_long) + (-1 * gamma_short)
theta_position = (1 * theta_long) + (-1 * theta_short)
vega_position = (1 * vega_long) + (-1 * vega_short)
```

**Greeks 해석:**

| Greek | 의미 | 예시 |
|-------|---------|---------|
| **Delta** | 방향성 노출 | Δ = 0.50 → 주가 +$1 시 $50 수익 |
| **Gamma** | Delta 가속도 | Γ = 0.05 → 주가 +$1 시 Delta 0.05 증가 |
| **Theta** | 일일 시간가치 감소 | Θ = -$5 → 시간 경과로 하루 $5 손실 |
| **Vega** | 변동성 민감도 | ν = $10 → IV 1% 증가 시 $10 수익 |
| **Rho** | 금리 민감도 | ρ = $2 → 금리 1% 증가 시 $2 수익 |

### 5단계: 전략 P/L 시뮬레이션

**목표:** 만기 시 다양한 주가에서 손익을 계산합니다.

**방법:**

주가 범위 생성(예: 현재가 기준 ±30%):
```python
current_price = 180
price_range = np.linspace(current_price * 0.7, current_price * 1.3, 100)
```

각 가격 지점별 P/L 계산:
```python
def calculate_pnl(strategy, stock_price_at_expiration):
    pnl = 0

    for leg in strategy.legs:
        if leg.type == 'call':
            intrinsic_value = max(0, stock_price_at_expiration - leg.strike)
        else:  # put
            intrinsic_value = max(0, leg.strike - stock_price_at_expiration)

        if leg.position == 'long':
            pnl += (intrinsic_value - leg.premium_paid) * 100  # Per contract
        else:  # short
            pnl += (leg.premium_received - intrinsic_value) * 100

    return pnl * num_contracts
```

**핵심 지표:**
- **Max Profit**: 가능한 최대 P/L
- **Max Loss**: 가능한 최악 P/L
- **Breakeven Point(s)**: P/L = 0이 되는 주가
- **Profit Probability**: 수익 구간 비율(단순화)

**출력 예시:**
```
Bull Call Spread: $180/$185 on AAPL (30 DTE, 10 contracts)

Current Price: $180.00
Net Debit: $2.50 per spread ($2,500 total)

Max Profit: $2,500 (at $185+)
Max Loss: -$2,500 (at $180-)
Breakeven: $182.50
Risk/Reward: 1:1

Probability Profit: ~55% (if stock stays above $182.50)
```

### 6단계: P/L 다이어그램 생성 (ASCII Art)

**주가별 P/L 시각화:**

```python
def generate_pnl_diagram(price_range, pnl_values, current_price, width=60, height=15):
    """Generate ASCII P/L diagram"""

    # Normalize to chart dimensions
    max_pnl = max(pnl_values)
    min_pnl = min(pnl_values)

    lines = []
    lines.append(f"\nP/L Diagram: {strategy_name}")
    lines.append("-" * width)

    # Y-axis levels
    levels = np.linspace(max_pnl, min_pnl, height)

    for level in levels:
        if abs(level) < (max_pnl - min_pnl) * 0.05:
            label = f"    0 |"  # Zero line
        else:
            label = f"{level:6.0f} |"

        row = label
        for i in range(width - len(label)):
            idx = int(i / (width - len(label)) * len(price_range))
            pnl = pnl_values[idx]
            price = price_range[idx]

            # Determine character
            if abs(pnl - level) < (max_pnl - min_pnl) / height:
                if pnl > 0:
                    char = '█'  # Profit
                elif pnl < 0:
                    char = '░'  # Loss
                else:
                    char = '─'  # Breakeven
            elif abs(level) < (max_pnl - min_pnl) * 0.05:
                char = '─'  # Zero line
            elif abs(price - current_price) < (price_range[-1] - price_range[0]) * 0.02:
                char = '│'  # Current price line
            else:
                char = ' '

            row += char

        lines.append(row)

    lines.append(" " * 6 + "|" + "-" * (width - 6))
    lines.append(" " * 6 + f"${price_range[0]:.0f}" + " " * (width - 20) + f"${price_range[-1]:.0f}")
    lines.append(" " * (width // 2 - 5) + "Stock Price")

    return "\n".join(lines)
```

**출력 예시:**
```
P/L Diagram: Bull Call Spread $180/$185
------------------------------------------------------------
 +2500 |                               ████████████████████
       |                         ██████
       |                   ██████
       |             ██████
     0 |       ──────
       | ░░░░░░
       |░░░░░░
 -2500 |░░░░░
      |____________________________________________________________
       $126                  $180                   $234
                          Stock Price

Legend: █ Profit  ░ Loss  ── Breakeven  │ Current Price
```

### 7단계: 전략별 맞춤 분석

전략 유형에 맞춰 맞춤형 가이드를 제공합니다:

**Covered Call:**
```
Income Strategy: Generate premium while capping upside

Setup:
- Own 100 shares of AAPL @ $180
- Sell 1x $185 call (30 DTE) for $3.50

Max Profit: $850 (Stock at $185+ = $5 stock gain + $3.50 premium)
Max Loss: Unlimited downside (stock ownership)
Breakeven: $176.50 (Cost basis - premium received)

Greeks:
- Delta: -0.30 (reduces stock delta from 1.00 to 0.70)
- Theta: +$8/day (time decay benefit)

Assignment Risk: If AAPL > $185 at expiration, shares called away

When to Use:
- Neutral to slightly bullish
- Want income in sideways market
- Willing to sell stock at $185

Exit Plan:
- Buy back call if stock rallies strongly (preserve upside)
- Let expire if stock stays below $185
- Roll to next month if want to keep shares
```

**Protective Put:**
```
Insurance Strategy: Limit downside while keeping upside

Setup:
- Own 100 shares of AAPL @ $180
- Buy 1x $175 put (30 DTE) for $2.00

Max Profit: Unlimited (stock can rise infinitely)
Max Loss: -$7 per share = ($5 stock loss + $2 premium)
Breakeven: $182 (Cost basis + premium paid)

Greeks:
- Delta: +0.80 (stock delta 1.00 - put delta 0.20)
- Theta: -$6/day (time decay cost)

Protection: Guaranteed to sell at $175, no matter how far stock falls

When to Use:
- Own stock, worried about short-term drop
- Earnings coming up, want protection
- Alternative to stop-loss (can't be stopped out)

Cost: "Insurance premium" - typically 1-3% of stock value

Exit Plan:
- Let expire worthless if stock rises (cost of insurance)
- Exercise put if stock falls below $175
- Sell put if stock drops but want to keep shares
```

**Iron Condor:**
```
Range-Bound Strategy: Profit from low volatility

Setup (example on AAPL @ $180):
- Sell $175 put for $1.50
- Buy $170 put for $0.50
- Sell $185 call for $1.50
- Buy $190 call for $0.50

Net Credit: $2.00 ($200 per iron condor)

Max Profit: $200 (if stock stays between $175-$185)
Max Loss: $300 (if stock moves outside $170-$190)
Breakevens: $173 and $187
Profit Range: $175 to $185 (58% probability)

Greeks:
- Delta: ~0 (market neutral)
- Theta: +$15/day (time decay benefit)
- Vega: -$25 (short volatility)

When to Use:
- Expect low volatility, range-bound movement
- After big move, think consolidation
- High IV environment (sell expensive options)

Risk: Unlimited if one side tested
- Use stop loss at 2x credit received (exit at -$400)

Adjustments:
- If tested on one side, roll that side out in time
- Close early at 50% max profit to reduce tail risk
```

### 8단계: Earnings 전략 분석

**Earnings Calendar 연동:**

사용자가 earnings 전략을 요청하면 earnings date를 조회합니다:
```python
from earnings_calendar import get_next_earnings_date

earnings_date = get_next_earnings_date("AAPL")
days_to_earnings = (earnings_date - today).days
```

**실적 발표 전 전략:**

**Long Straddle/Strangle:**
```
Setup (AAPL @ $180, earnings in 7 days):
- Buy $180 call for $5.00
- Buy $180 put for $4.50
- Total Cost: $9.50

Thesis: Expect big move (>5%) but unsure of direction

Breakevens: $170.50 and $189.50
Profit if: Stock moves >$9.50 in either direction

Greeks:
- Delta: ~0 (neutral)
- Vega: +$50 (long volatility)
- Theta: -$25/day (time decay hurts)

IV Crush Risk: ⚠️ CRITICAL
- Pre-earnings IV: 40% (elevated)
- Post-earnings IV: 25% (typical)
- IV drop: -15 points = -$750 loss even if stock doesn't move!

Analysis:
- Implied Move: √(DTE/365) × IV × Stock Price
  = √(7/365) × 0.40 × 180 = ±$10.50
- Breakeven Move Needed: ±$9.50
- Probability Profit: ~30-40% (implied move > breakeven move)

Recommendation:
✅ Consider if you expect >10% move (larger than implied)
❌ Avoid if expect normal ~5% earnings move (IV crush will hurt)

Alternative: Buy further OTM strikes to reduce cost
- $175/$185 strangle cost $4.00 (need >$8 move, but cheaper)
```

**Short Iron Condor:**
```
Setup (AAPL @ $180, earnings in 7 days):
- Sell $170/$175 put spread for $2.00
- Sell $185/$190 call spread for $2.00
- Net Credit: $4.00

Thesis: Expect stock to stay range-bound ($175-$185)

Profit Zone: $175 to $185
Max Profit: $400
Max Loss: $100

IV Crush Benefit: ✅
- Short high IV before earnings
- IV drops after earnings → profit on vega
- Even if stock moves slightly, IV drop helps

Greeks:
- Delta: ~0 (market neutral)
- Vega: -$40 (short volatility - good here!)
- Theta: +$20/day

Recommendation:
✅ Good if expect normal earnings reaction (<8% move)
✅ Benefit from IV crush regardless of direction
⚠️ Risk if stock gaps outside range (>10% move)

Exit Plan:
- Close next day if IV crushed (capture profit early)
- Use stop loss if one side tested (-2x credit)
```

### 9단계: 리스크 관리 가이드

**포지션 사이징:**

```
Account Size: $50,000
Risk Tolerance: 2% per trade = $1,000 max risk

Iron Condor Example:
- Max loss per spread: $300
- Max contracts: $1,000 / $300 = 3 contracts
- Actual position: 3 iron condors

Bull Call Spread Example:
- Debit paid: $2.50 per spread
- Max contracts: $1,000 / $250 = 4 contracts
- Actual position: 4 spreads
```

**포트폴리오 Greeks 관리:**

```
Portfolio Guidelines:
- Delta: -10 to +10 (mostly neutral)
- Theta: Positive preferred (seller advantage)
- Vega: Monitor if >$500 (IV risk)

Current Portfolio:
- Delta: +5 (slightly bullish)
- Theta: +$150/day (collecting $150 daily)
- Vega: -$300 (short volatility)

Interpretation:
✅ Neutral delta (safe)
✅ Positive theta (time working for you)
⚠️ Short vega: If IV spikes, lose $300 per 1% IV increase
→ Reduce short premium positions if VIX rising
```

**조정 및 청산:**

```
Exit Rules by Strategy:

Covered Call:
- Profit: 50-75% of max profit
- Loss: Stock drops >5%, buy back call to preserve upside
- Time: 7-10 DTE, roll to avoid assignment

Spreads:
- Profit: 50% of max profit (close early, reduce tail risk)
- Loss: 2x debit paid (cut losses early)
- Time: 21 DTE, close or roll (avoid gamma risk)

Iron Condor:
- Profit: 50% of credit (close early common)
- Loss: One side tested, 2x credit lost
- Adjustment: Roll tested side out in time

Straddle/Strangle:
- Profit: Stock moved >breakeven, close immediately
- Loss: Theta eating position, stock not moving
- Time: Day after earnings (if earnings play)
```

## 출력 형식

**전략 분석 보고서 템플릿:**

```markdown
# Options Strategy Analysis: [Strategy Name]

**Symbol:** [TICKER]
**Strategy:** [Strategy Type]
**Expiration:** [Date] ([DTE] days)
**Contracts:** [Number]

---

## Strategy Setup

### Leg Details
| Leg | Type | Strike | Price | Position | Quantity |
|-----|------|--------|-------|----------|----------|
| 1 | Call | $180 | $5.00 | Long | 1 |
| 2 | Call | $185 | $2.50 | Short | 1 |

**Net Debit/Credit:** $2.50 debit ($250 total for 1 spread)

---

## Profit/Loss Analysis

**Max Profit:** $250 (at $185+)
**Max Loss:** -$250 (at $180-)
**Breakeven:** $182.50
**Risk/Reward Ratio:** 1:1

**Probability Analysis:**
- Probability of Profit: ~55% (stock above $182.50)
- Expected Value: $25 (simplified)

---

## P/L Diagram

[ASCII art diagram here]

---

## Greeks Analysis

### Position Greeks (1 spread)
- **Delta:** +0.20 (gains $20 if stock +$1)
- **Gamma:** +0.03 (delta increases by 0.03 if stock +$1)
- **Theta:** -$5/day (loses $5 per day from time decay)
- **Vega:** +$8 (gains $8 if IV increases 1%)

### Interpretation
- **Directional Bias:** Slightly bullish (positive delta)
- **Time Decay:** Working against you (negative theta)
- **Volatility:** Benefits from IV increase (positive vega)

---

## Risk Assessment

### Maximum Risk
**Scenario:** Stock falls below $180
**Max Loss:** -$250 (100% of premium paid)
**% of Account:** 0.5% (if $50k account)

### Assignment Risk
**Early Assignment:** Low (calls have time value)
**At Expiration:** Manage positions if in-the-money

---

## Trade Management

### Entry
✅ Enter if: [Conditions]
- Stock price $178-$182
- IV below 30%
- >21 DTE

### Profit Taking
- **Target 1:** 50% profit ($125) - Close half
- **Target 2:** 75% profit ($187.50) - Close all

### Stop Loss
- **Trigger:** Stock falls below $177 (-$150 loss)
- **Action:** Close position immediately

### Adjustments
- If stock rallies to $184, consider rolling short call higher
- If stock drops to $179, add second spread at $175/$180

---

## Suitability

### When to Use This Strategy
✅ Moderately bullish on AAPL
✅ Expect upside to $185-$190
✅ Want defined risk
✅ 21-45 DTE timeframe

### When to Avoid
❌ Very bullish (buy stock or long call instead)
❌ High IV environment (wait for IV to drop)
❌ Earnings in <7 days (IV crush risk)

---

## Alternatives Comparison

| Strategy | Max Profit | Max Loss | Complexity | When Better |
|----------|-----------|----------|------------|-------------|
| Bull Call Spread | $250 | -$250 | Medium | Moderately bullish |
| Long Call | Unlimited | -$500 | Low | Very bullish |
| Covered Call | $850 | Unlimited | Medium | Own stock already |
| Bull Put Spread | $300 | -$200 | Medium | Want credit spread |

**Recommendation:** Bull call spread is good balance of risk/reward for moderate bullish thesis.

---

*Disclaimer: This is theoretical analysis using Black-Scholes pricing. Actual market prices may differ. Trade at your own risk. Options are complex instruments with significant loss potential.*
```

**파일 네이밍 규칙:**
```
options_analysis_[TICKER]_[STRATEGY]_[DATE].md
```

예시: `options_analysis_AAPL_BullCallSpread_2025-11-08.md`

## 핵심 원칙

### 이론 가격의 한계

**사용자가 알아야 할 점:**
1. **Black-Scholes 가정:**
   - 유럽형 옵션(조기 행사 불가)
   - 변동성 일정(현실에서는 IV가 변함)
   - 거래 비용 없음
   - 연속 거래 가능

2. **실제 가격 vs 이론 가격:**
   - Bid-ask spread: 실제 비용이 이론값보다 높음
   - American 옵션: 조기 행사 가능(특히 ITM put)
   - 유동성: 비유동 옵션은 호가 스프레드가 넓음
   - 배당: Ex-dividend 날짜가 가격에 영향

3. **Best Practices:**
   - 교육용 도구 및 비교 분석 용도로 사용
   - 실제 거래 전 브로커 실시간 호가 확인
   - 이론 가격 ≈ 중간호가(mid-market price)로 이해
   - 수수료와 slippage 반영

### 변동성 가이드

**Historical Volatility vs Implied Volatility:**

```
Historical Volatility (HV): What happened
- Calculated from past price movements
- Objective, based on data
- Available for free (FMP API)

Implied Volatility (IV): What market expects
- Derived from option prices
- Subjective, based on supply/demand
- Requires live options data (user provides)

Comparison:
- IV > HV: Options expensive (consider selling)
- IV < HV: Options cheap (consider buying)
- IV = HV: Fairly priced
```

**IV Percentile:**

사용자가 현재 IV를 제공하면 percentile을 계산합니다:
```python
# Fetch 1-year HV data
historical_hvs = calculate_hv_series(prices_1yr, window=30)

# Calculate IV percentile
iv_percentile = percentileofscore(historical_hvs, current_iv)

if iv_percentile > 75:
    guidance = "High IV - consider selling premium (credit spreads, iron condors)"
elif iv_percentile < 25:
    guidance = "Low IV - consider buying options (long calls/puts, debit spreads)"
else:
    guidance = "Normal IV - any strategy appropriate"
```

## 다른 스킬과의 통합

**Earnings Calendar:**
- earnings date 자동 조회
- earnings 특화 전략 제안
- days to earnings 계산(IV에서 DTE 중요)
- IV crush 리스크 경고

**Technical Analyst:**
- strike 선택에 support/resistance 활용
- 방향성 전략용 추세 분석
- straddle/strangle 타이밍용 breakout 잠재력 평가

**US Stock Analysis:**
- 장기 전략(LEAPS)용 펀더멘털 분석
- covered call/put 분석용 배당수익률
- earnings 플레이용 실적 품질 분석

**Bubble Detector:**
- bubble risk 높음 → protective put 중심
- risk 낮음 → 강세 전략
- risk 임계 수준 → long premium 회피(theta 불리)

**Portfolio Manager:**
- 주식 포지션과 옵션 포지션 통합 추적
- 포트폴리오 Greeks 집계
- 주식 포지션 헤지 도구로 옵션 활용

## 중요 참고사항

- **모든 분석은 English로 제공**
- **교육 중심**: 전략을 명확히 설명
- **이론 가격**: Black-Scholes 근사값
- **사용자 IV 입력**: 선택 사항, 기본값 HV
- **실시간 데이터 불필요**: FMP Free tier로 충분
- **Dependencies**: Python 3.8+, numpy, scipy, pandas

## 일반적인 사용 사례

**Use Case 1: 전략 학습**
```
User: "Explain a covered call"

Workflow:
1. Load strategy reference (references/strategies_guide.md)
2. Explain concept, risk/reward, when to use
3. Simulate example on AAPL
4. Show P/L diagram
5. Compare to alternatives
```

**Use Case 2: 특정 거래 분석**
```
User: "Analyze $180/$185 bull call spread on AAPL, 30 days"

Workflow:
1. Fetch AAPL price from FMP
2. Calculate HV or ask user for IV
3. Price both options (Black-Scholes)
4. Calculate Greeks
5. Simulate P/L
6. Generate analysis report
```

**Use Case 3: Earnings 전략**
```
User: "Should I trade options before NVDA earnings?"

Workflow:
1. Fetch NVDA earnings date (Earnings Calendar)
2. Calculate days to earnings
3. Estimate IV percentile (if user provides IV)
4. Suggest straddle/strangle vs iron condor
5. Warn about IV crush
6. Simulate both strategies
```

**Use Case 4: 포트폴리오 Greeks 점검**
```
User: "What are my total portfolio Greeks?"

Workflow:
1. User provides current positions
2. Calculate Greeks for each position
3. Sum Greeks across portfolio
4. Assess overall exposure
5. Suggest adjustments if needed
```

## 문제 해결

**문제: IV를 사용할 수 없음**
- 해결: HV를 대체값으로 사용하고 사용자에게 명시
- 사용자에게 브로커 플랫폼 IV 제공 요청

**문제: 옵션 가격이 음수로 계산됨**
- 해결: 입력값 점검(strike와 주가 관계)
- Deep ITM 옵션은 수치 계산 이슈 가능

**문제: Greeks가 이상해 보임**
- 해결: 입력값(T, sigma, r) 검증
- 연율값/일일값 혼용 여부 확인

**문제: 전략이 너무 복잡함**
- 해결: leg 단위로 분해해서 개별 분석
- 전략 상세는 references 문서 참조

## 리소스

**참고 문서:**
- `references/strategies_guide.md` - 17개+ 전략 설명
- `references/greeks_explained.md` - Greeks 심화 설명
- `references/volatility_guide.md` - HV vs IV, 트레이드 시점 가이드

**스크립트:**
- `scripts/black_scholes.py` - 가격 엔진 및 Greeks
- `scripts/strategy_analyzer.py` - 전략 시뮬레이션
- `scripts/earnings_strategy.py` - earnings 특화 분석

**외부 리소스:**
- Options Playbook: https://www.optionsplaybook.com/
- CBOE Education: https://www.cboe.com/education/
- Black-Scholes Calculator: Various online tools for verification

---

**Version**: 1.0
**Last Updated**: 2025-11-08
**Dependencies**: Python 3.8+, numpy, scipy, pandas, requests
**API**: FMP API (Free tier sufficient)
