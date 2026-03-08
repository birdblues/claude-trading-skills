# 버블 탐지 Quick Reference (English)

## 일일 체크리스트 (5분)

### 아침 루틴 (장 시작 전)

```
□ Step 1: Update Bubble-O-Meter (2 min)
   - Score 8 indicators (0-2 points each)
   - Check risk budget based on total score

□ Step 2: Position Management (2 min)
   - Update ATR trailing stops
   - Check stair-step profit targets
   - Evaluate new entry eligibility

□ Step 3: Signal Check (1 min)
   - Media/Social trends (Google Trends, Twitter)
   - Major indices distance from 52-week highs
   - VIX & Put/Call ratio
```

---

## 긴급 점검: 3가지 질문

투자 판단이 불확실할 때 다음 3가지를 답하세요:

### Q1: "비투자자도 이걸 추천하는가?"
- YES → 대중 침투 완료, 후기 단계 가능성 높음
- NO → 아직 초기~중기 단계

### Q2: "내러티브가 '상식'이 되었는가?"
- YES → Euphoria 단계, 역행 시각이 사회적으로 용인되지 않음
- NO → 건강한 회의론이 아직 작동

### Q3: "'이번에는 다르다'가 유행어인가?"
- YES → 전형적인 역사적 버블 신호
- NO → 건강한 경계가 남아 있음

**3개 모두 YES → Critical zone, 수익 실현/이탈 우선**

---

## 버블 단계별 액션 매트릭스

| Phase | Score | Risk Budget | Entry | Profit-Taking | Stop | Short |
|-------|-------|------------|-------|---------------|------|-------|
| **Normal** | 0-4 | 100% | Normal | At target | 2.0 ATR | No |
| **Caution** | 5-8 | 70% | 50% reduced | 25% at +20% | 1.8 ATR | No |
| **Euphoria** | 9-12 | 40% | Stopped | 50% at +20% | 1.5 ATR | After confirm |
| **Critical** | 13-16 | 20% | Stopped | 75-100% now | 1.2 ATR | Recommended |

---

## 8개 지표 빠른 점수화

### 1. Mass Penetration
```
0 pts: Investors only
1 pt: General awareness but investment limited
2 pts: Taxi drivers/family recommending
```

### 2. Media Saturation
```
0 pts: Normal coverage
1 pt: Search trends 2-3x normal
2 pts: TV specials/magazine covers, 5x+ search spike
```

### 3. New Accounts & Inflows
```
0 pts: Normal account openings
1 pt: 50-100% YoY increase
2 pts: 200%+ YoY, first-time investor flood
```

### 4. New Issuance Flood
```
0 pts: Normal IPO volume
1 pt: IPO/SPAC/ETFs up 50%+
2 pts: Low-quality IPO flood, "theme" fund proliferation
```

### 5. Leverage Indicators
```
0 pts: Margin debt in normal range
1 pt: Margin debt 1.5x average
2 pts: All-time high margin, funding rates elevated, extreme positioning
```

### 6. Price Acceleration
```
0 pts: Annualized returns near historical median
1 pt: Returns exceed 90th percentile
2 pts: Returns at 95-99th percentile, or positive second derivative
```

### 7. Valuation Disconnect
```
0 pts: Fundamentally explainable
1 pt: High valuation but "growth expectations" provide cover
2 pts: Pure "narrative" dependent, fundamentals ignored
```

### 8. Breadth & Correlation
```
0 pts: Only leader stocks rising
1 pt: Sector-wide participation
2 pts: Low-quality/zombie companies rising (last buyers in)
```

---

## 수익 실현 전략 템플릿

### Template 1: Stair-Step (보수적)

```
Position: $10,000 initial investment
Targets: +20%, +40%, +60%, +80%

+20% ($12,000) → Sell 25% = $3,000 secured
+40% ($14,000) → Sell 25% = $3,500 secured
+60% ($16,000) → Sell 25% = $4,000 secured
+80% ($18,000) → Sell 25% = $4,500 secured

Total profit secured: $15,000 (+50% equivalent)
```

### Template 2: ATR Trailing (공격적)

```python
def calculate_trailing_stop(current_price, atr_20d, bubble_phase):
    """
    Calculate trailing stop based on bubble phase

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
```

### Template 3: Hybrid (권장)

```
Stage 1 (Boom):
  → Stair-step reduces 50% of position

Stage 2 (Euphoria):
  → Apply ATR trailing to remaining 50%, ride upside

Stage 3 (Panic signals):
  → Exit immediately when ATR stop hit
```

---

## 공매도 타이밍 결정 (중요)

### ❌ 절대 피할 것: 조기 역행

```
Reason: Often 2-3x further rise after "obviously too high"
Risk: "Markets can remain irrational longer than you can remain solvent"
```

### ✅ 권장: 복합 조건 충족 후

**고려 전 7개 중 최소 3개 필요:**

1. □ Weekly chart shows clear lower highs
2. □ Volume peaked out (3 weeks declining)
3. □ Leverage metrics drop sharply (margin debt -20%+)
4. □ Media/search trends peaked out
5. □ Weak stocks in sector breaking down first
6. □ VIX spike (+30%+)
7. □ Fed or policy reversal signals

**실행 예시:**

```
Conditions check:
[✓] 1. Weekly lower highs
[✓] 2. Volume declining 3 weeks
[×] 3. Margin debt still elevated
[✓] 4. Google trends -40%
[×] 5. Still broad rally
[✓] 6. VIX +35% spike
[×] 7. No policy change

→ 4/7 met, short consideration OK
→ Small size (25% of normal) test entry
```

---

## 흔한 실패 패턴 및 해결책

### Failure 1: "너무 늦었다" 사고로 계속 대기

**Psychology:** Regret aversion (놓칠까 두려운 FOMO)
**Solution:**
- 너무 늦었다고 느낄 때 Bubble-O-Meter 실행
- 점수 ≤8이면 소규모 진입 가능
- 점수 ≥9이면 대기가 정답

### Failure 2: 수익 실현 후 재진입 (고점 매수)

**Psychology:** Hindsight bias ("오를 줄 알았는데")
**Solution:**
- 수익 실현 후 72시간 재진입 금지
- 재진입은 Bubble-O-Meter 확인 후에만

### Failure 3: "아직 오르는데"로 수익 실현 지연

**Psychology:** Greed + Overconfidence
**Solution:**
- 계단식 수익 실현 자동화(사전 지정가 주문)
- "완벽"이 아니라 "만족"을 목표로

### Failure 4: 성급한 공매도

**Psychology:** 주관적 "이미 너무 비쌈"
**Solution:**
- 복합 조건을 기계적으로 점검
- 최소 3개 조건 충족까지 대기

---

## 비상 대응 플로우차트

```
Market shock detected
    ↓
Q: Have positions?
    ↓YES
Q: Down -5%+ ?
    ↓YES
Q: ATR stop hit?
    ↓YES
→ Sell immediately (no debate)

    ↓NO (stop not hit)
Q: Bubble-O-Meter 13+?
    ↓YES
→ Consider 75%+ profit-taking

    ↓NO (score ≤12)
Q: VIX spike +30%+?
    ↓YES
→ Take 50% profits, tighten stops on rest

    ↓NO
→ Normal monitoring, stay calm
```

---

## Golden Rules (벽에 붙여두기)

1. **Watch the process, not the price**

2. **When taxi drivers talk stocks, exit**

3. **"This time is different" is the same every time**

4. **Mechanical rules protect your psychology**

5. **Short after confirmation, take profits early**

6. **When skepticism hurts socially, the end begins**

7. **Aim for satisfaction, abandon perfection**

8. **Bubbles last longer than expected, crashes faster**

9. **Leverage is an express ticket to ruin**

10. **"Markets can remain irrational longer than you can remain solvent"**

---

## 핵심 데이터 소스

### 즉시 접근 가능한 지표

| Indicator | Source | URL Example |
|-----------|--------|-------------|
| Google Search Trends | Google Trends | trends.google.com |
| VIX (Fear Index) | CBOE | cboe.com/vix |
| Put/Call Ratio | CBOE | cboe.com/data |
| Margin Debt | FINRA | finra.org/data |
| Futures Positioning | CFTC COT | cftc.gov/reports |
| IPO Statistics | Renaissance IPO | renaissancecapital.com |

### 자동화를 위한 API 접근

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

## 추가 학습

### Books
- "Manias, Panics, and Crashes" - Charles Kindleberger
- "Irrational Exuberance" - Robert Shiller
- "The Alchemy of Finance" - George Soros

### Research
- Hyman Minsky's Financial Instability Hypothesis
- Behavioral Finance classics

### Data & Tools
- TradingView: Charts & technical indicators
- FRED (Federal Reserve): Economic time series
- Finviz: Screening & heatmaps
- Google Trends: Social trends

---

**Last Updated:** 2025 Edition
**License:** Educational/personal use only
