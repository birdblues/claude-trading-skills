# 버블 탐지 Quick Reference

## 일일 체크리스트 (5분 완료)

### 아침 루틴 (장 시작 전)

```
□ Step 1: Update Bubble-O-Meter (2 minutes)
   - Score 8 indicators on 0-2 scale
   - Confirm risk budget based on total score

□ Step 2: Position Management (2 minutes)
   - Update ATR trailing stops
   - Check if stair-step profit-taking targets reached
   - Determine new entry eligibility

□ Step 3: Signal Confirmation (1 minute)
   - Media/social media trends (Google Trends, Twitter)
   - Major indices' distance from 52-week highs
   - VIX & Put/Call ratio
```

---

## 긴급 점검: 3가지 질문

투자 결정이 불확실할 때 아래 3가지를 답하세요:

### Q1: "비투자자가 추천하고 있는가?"
- YES → 대중 침투 완료, 후기 단계일 가능성 높음
- NO → 아직 초기~중기 단계

### Q2: "내러티브가 '상식'이 되었는가?"
- YES → Euphoria 단계, 반대 의견이 사회적으로 수용되지 않음
- NO → 회의적 시각이 아직 허용되는 건강한 상태

### Q3: "'이번에는 다르다'가 주문처럼 반복되는가?"
- YES → 역사적으로 전형적인 버블 신호
- NO → 건강한 경계심이 작동 중

**3개 모두 YES → Critical zone, 수익 실현/이탈 우선**

---

## 버블 단계별 액션 매트릭스 (REVISED v2.1)

| Phase | Score | Risk Budget | Entry | Profit-Taking | Stop | Shorts |
|-------|-------|------------|-------|--------------|------|--------|
| **Normal** | 0-4 | 100% | Normal | At target | 2.0 ATR | No |
| **Caution** | 5-7 | 70-80% | 50% reduced | 25% at +20% | 1.8 ATR | No |
| **Elevated Risk** | 8-9 | 50-70% | Selective | 40% at +20% | 1.6 ATR | Consider |
| **Euphoria** | 10-12 | 40-50% | Stop | 50% at +20% | 1.5 ATR | After conditions |
| **Critical** | 13-15 | 20-30% | Stop | 75-100% immediate | 1.2 ATR | Recommended |

**참고**: 최대 점수는 16점에서 15점으로 축소됨 (Phase 2: 최대 12, Phase 3: 최대 3)

---

## 8개 지표 빠른 점수화

### 1. Mass Penetration
```
0 points: Investors only
1 point: General awareness but investment still limited
2 points: Taxi drivers/family recommending
```

### 2. Media Saturation
```
0 points: Normal coverage level
1 point: Search trends 2-3x
2 points: TV specials/magazine covers, searches 5x+
```

### 3. New Entrants
```
0 points: Normal account opening pace
1 point: 50-100% YoY increase
2 points: 200%+ YoY, beginner flood
```

### 4. Issuance Flood
```
0 points: Normal IPO count
1 point: 50% increase in IPOs/related products
2 points: Low-quality IPOs, theme ETF proliferation
```

### 5. Leverage
```
0 points: Normal range
1 point: Margin balance 1.5x
2 points: All-time high, funding rates elevated
```

### 6. Price Acceleration
```
0 points: Near historical median
1 point: Exceeds 90th percentile
2 points: 95-99th percentile or accelerating
```

### 7. Valuation Disconnect
```
0 points: Explainable by fundamentals
1 point: High valuation but explained by growth expectations
2 points: Completely "narrative"-dependent, fundamentals ignored
```

### 8. Correlation & Breadth
```
0 points: Only some leaders rising
1 point: Sector-wide spread
2 points: Even low-quality/zombie companies rallying
```

---

## 핵심 데이터 소스

### 즉시 확인 가능한 지표

| Indicator | Source | Example URL |
|-----------|--------|------------|
| Google Search Trends | Google Trends | trends.google.com |
| VIX (Fear Index) | CBOE | cboe.com/vix |
| Put/Call Ratio | CBOE | cboe.com/data |
| Margin Balance | FINRA | finra.org/data |
| Futures Positions | CFTC COT | cftc.gov/reports |
| IPO Statistics | Renaissance IPO | renaissancecapital.com |

### API 접근 기반 자동 수집

```python
# Example: Google Trends (pytrends)
from pytrends.request import TrendReq
pytrends = TrendReq()
pytrends.build_payload(['SPY', 'stock market'])
data = pytrends.interest_over_time()

# Example: VIX (yfinance)
import yfinance as yf
vix = yf.Ticker('^VIX')
current_vix = vix.history(period='1d')['Close'].iloc[-1]
```

---

## 수익 실현 전략 템플릿

### Template 1: Stair-Step Profit-Taking (보수적)

```
Position: $10,000 initial investment
Targets:  +20%, +40%, +60%, +80%

+20% ($12,000) → Sell 25% = $3,000 secured
+40% ($14,000) → Sell 25% = $3,500 secured
+60% ($16,000) → Sell 25% = $4,000 secured
+80% ($18,000) → Sell 25% = $4,500 secured

Total profits: $15,000 (+50% equivalent)
```

### Template 2: ATR Trailing (공격적)

```python
def calculate_trailing_stop(current_price, atr_20d, bubble_phase):
    """
    Calculate trailing stop based on bubble stage

    bubble_phase: 'normal', 'caution', 'euphoria', 'critical'
    """
    multipliers = {
        'normal': 2.0,
        'caution': 1.8,
        'euphoria': 1.5,
        'critical': 1.2
    }
    multiplier = multipliers.get(bubble_phase, 2.0)
    stop_price = current_price - (atr_20d * multiplier)
    return stop_price

# Usage example
current_price = 450.0
atr_20d = 10.0  # Average True Range over 20 days
bubble_phase = 'euphoria'

stop = calculate_trailing_stop(current_price, atr_20d, bubble_phase)
print(f"Trailing Stop: ${stop:.2f}")
# Output: Trailing Stop: $435.00
```

### Template 3: Hybrid (권장)

```
Stage 1 (Boom period):
  → Reduce 50% of position via stair-step profit-taking

Stage 2 (Euphoria period):
  → Apply ATR trailing to remaining 50%, follow upside

Stage 3 (Panic signs):
  → Exit immediately when ATR stop hit
```

---

## 공매도 타이밍 점검 (중요)

### ❌ 절대 NG: 조기 역행

```
Reason: Normal for prices to rise 2-3x more after feeling "too high"
Risk: "Markets can remain irrational longer than you can remain solvent"
```

### ✅ 권장: 복합 조건 확인 후

**아래 최소 3개 충족 시 시작 고려:**

1. □ Weekly chart shows clear lower highs
2. □ Volume peaks out (3 consecutive weeks declining)
3. □ Sharp drop in leverage indicators (margin balance -20%+)
4. □ Media/search trends peak out
5. □ Weak stocks within sector start breaking down first
6. □ VIX surges (+30%+)
7. □ Fed/policy shift signals

**실행 예시:**

```
Condition Check:
[✓] 1. Weekly lower highs forming
[✓] 2. Volume declining 3 weeks straight
[×] 3. Margin balance still elevated
[✓] 4. Google search trends -40%
[×] 5. Still broad rally continuing
[✓] 6. VIX +35% surge
[×] 7. No policy changes

→ 4/7 met, shorts consideration OK
→ Small position (25% of normal) for test entry
```

---

## 흔한 실패 패턴 및 해결책

### Failure 1: "너무 늦었다" 마비로 기회 상실

**Psychology:** Regret aversion (늦었다는 두려움)
**Solution:**
- "너무 늦었다"는 느낌이 들 때 Bubble-O-Meter 수행
- 점수 ≤8: 소규모 진입 가능
- 점수 ≥9: 관망이 정답

### Failure 2: 수익 실현 후 재진입 (고점 매수)

**Psychology:** Hindsight bias ("더 갈 줄 알았는데")
**Solution:**
- 수익 실현 후 72시간 재진입 금지
- 재진입은 Bubble-O-Meter 점검 후에만

### Failure 3: "아직 오르는데"로 수익 실현 실패

**Psychology:** Greed + Overconfidence
**Solution:**
- 계단식 수익 실현 자동화(사전 지정가 주문)
- "완벽" 대신 "만족" 목표

### Failure 4: 너무 이른 공매도

**Psychology:** 주관적 "너무 많이 올랐다"
**Solution:**
- 복합 조건을 기계적으로 확인
- 최소 3개 충족까지 대기

---

## 비상 대응 플로우차트

```
Detect market volatility
    ↓
Q: Have positions?
    ↓YES
Q: Down -5% or more?
    ↓YES
Q: ATR stop reached?
    ↓YES
→ Sell immediately (no debate)

    ↓NO (Stop not reached)
Q: Bubble-O-Meter score 13+?
    ↓YES
→ Consider 75%+ profit-taking

    ↓NO (Score ≤12)
Q: VIX surge +30%+?
    ↓YES
→ 50% profit-taking, tighten remaining stops

    ↓NO
→ Business as usual, continue calm observation
```

---

## Golden Rules (벽에 붙여둘 10계명)

1. **See process, not price**

2. **When taxi drivers talk stocks, exit**

3. **"This time is different" is always the same**

4. **Mechanical rules protect psychology**

5. **Short after confirmation, take profits early**

6. **When skepticism hurts, the end begins**

7. **Aim for satisfaction, abandon perfection**

8. **Bubbles last longer than expected, collapses are faster**

9. **Leverage is an express ticket to ruin**

10. **"Markets can remain irrational longer than you can remain solvent"**

---

## 추가 학습 리소스

### Books
- **"Manias, Panics, and Crashes"** - Charles Kindleberger
- **"Irrational Exuberance"** - Robert Shiller
- **"The Alchemy of Finance"** - George Soros

### Research
- Hyman Minsky's Financial Instability Hypothesis
- Classic papers in Behavioral Finance

### Data & Tools
- **TradingView**: Charts and technical indicators
- **FRED (Federal Reserve)**: Economic indicator time series
- **Finviz**: Screening and heatmaps
- **Google Trends**: Social trends

---

**Last Updated:** 2025 Edition
**License:** Educational and personal use only, redistribution prohibited
