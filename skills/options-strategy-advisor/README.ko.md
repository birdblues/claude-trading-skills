# Options Strategy Advisor

Black-Scholes 모델을 사용해 이론 가격, 전략 분석, 리스크 관리 가이드를 제공하는 교육용 옵션 트레이딩 도구입니다.

## 개요

Options Strategy Advisor는 고가의 실시간 옵션 데이터 없이도 트레이더가 옵션 전략을 이해하고 분석할 수 있도록 돕습니다. 이론 가격 모델(Black-Scholes)과 무료 주식 시장 데이터(FMP API)를 결합해 전략 시뮬레이션과 Greeks 계산을 수행합니다.

**주요 기능:**
- ✅ Black-Scholes pricing engine
- ✅ 전체 Greeks 계산 (Delta, Gamma, Theta, Vega, Rho)
- ✅ 17개+ 옵션 전략 지원
- ✅ P/L 시뮬레이션 및 시각화
- ✅ Earnings 전략 연동
- ✅ Historical volatility 계산
- ✅ 리스크 관리 가이드

## 왜 이 접근인가?

**비싼 데이터 구독이 필요 없음:**
- 실시간 옵션 데이터: $99-$500/month (Polygon.io, Intrinio)
- FMP API Free tier: $0/month (250 requests/day)

**교육 중심:**
- 전략이 어떻게 동작하는지 학습
- Greeks와 리스크 지표 이해
- 전략을 나란히 비교

**실전 적용:**
- 이론 가격 ≈ 시장 중간호가
- 사용자가 브로커의 실제 IV 입력 가능
- 전략 기획 및 학습에 적합

## 지원 전략

### Income Strategies
1. **Covered Call** - 주식 보유분으로 수익 창출
2. **Cash-Secured Put** - 주식 매수 의향으로 premium 수취
3. **Poor Man's Covered Call** - 자본 효율적인 covered call

### Protection Strategies
4. **Protective Put** - 주식 포지션 보험
5. **Collar** - 제한된 risk/reward 보호

### Directional Strategies
6. **Bull Call Spread** - 제한 리스크의 강세 전략
7. **Bull Put Spread** - 강세 관점의 credit spread
8. **Bear Call Spread** - 약세 관점의 credit spread
9. **Bear Put Spread** - 제한 리스크의 약세 전략

### Volatility Strategies
10. **Long Straddle** - 큰 움직임에서 수익
11. **Long Strangle** - 더 저렴한 straddle, 더 큰 움직임 필요
12. **Short Straddle** - 무변동에서 수익 (고위험)
13. **Short Strangle** - 범위를 넓힌 straddle

### Range-Bound Strategies
14. **Iron Condor** - 박스권 트레이딩에서 수익
15. **Iron Butterfly** - 좁은 박스권에서 수익

### Advanced Strategies
16. **Calendar Spread** - time decay 플레이
17. **Diagonal Spread** - 방향성 + time decay

## 설치

### 사전 요구사항
- Python 3.8+
- FMP API key (free tier로 충분)

### 의존성 설치
```bash
pip install numpy scipy requests pandas
```

### FMP API Key 받기
1. https://financialmodelingprep.com/developer/docs 방문
2. 무료 계정 가입
3. API key 복사
4. 환경 변수 설정:
```bash
export FMP_API_KEY="your_key_here"
```

## 빠른 시작

### Black-Scholes Pricer 테스트

```bash
python scripts/black_scholes.py
```

**출력 예시:**
```
BLACK-SCHOLES OPTIONS PRICER - EXAMPLE
======================================================================

Input Parameters:
  Stock Price: $180.00
  Strike Price: $185.00
  Days to Expiration: 30
  Volatility: 25.0%
  Risk-Free Rate: 5.30%
  Dividend Yield: 1.0%

======================================================================
CALL OPTION
======================================================================
Price: $2.45
Intrinsic Value: $0.00
Time Value: $2.45

Greeks:
  Delta: 0.3654 ($36.54 per $1 move)
  Gamma: 0.0234 (delta changes by 0.0234)
  Theta: -$0.18/day (loses $0.18 per day)
  Vega: $0.25 per 1% IV (gains $0.25 if IV +1%)
  Rho: $0.12 per 1% rate (gains $0.12 if rate +1%)
```

### 코드에서 사용하기

```python
from scripts.black_scholes import OptionPricer

# Initialize pricer
pricer = OptionPricer(
    S=180,          # Stock price
    K=185,          # Strike price
    T=30/365,       # Time to expiration (years)
    r=0.053,        # Risk-free rate (5.3%)
    sigma=0.25,     # Volatility (25%)
    q=0.01          # Dividend yield (1%)
)

# Get call option price
call_price = pricer.call_price()
print(f"Call Price: ${call_price:.2f}")

# Get all Greeks for call
call_greeks = pricer.get_all_greeks('call')
print(f"Delta: {call_greeks['delta']:.4f}")
print(f"Gamma: {call_greeks['gamma']:.4f}")
print(f"Theta: ${call_greeks['theta']:.2f}/day")
print(f"Vega: ${call_greeks['vega']:.2f} per 1%")
```

### Historical Volatility 계산

```python
from scripts.black_scholes import (
    calculate_historical_volatility,
    fetch_historical_prices_for_hv
)

# Fetch prices from FMP
api_key = "your_key"
prices = fetch_historical_prices_for_hv("AAPL", api_key, days=90)

# Calculate 30-day HV
hv = calculate_historical_volatility(prices, window=30)
print(f"30-Day HV: {hv*100:.2f}%")
```

## 지표 이해하기

### 옵션 가격 구성요소

**내재가치 (Intrinsic Value):**
- Call: max(0, Stock Price - Strike Price)
- Put: max(0, Strike Price - Stock Price)

**시간가치 (Time Value):**
- Option Price - Intrinsic Value
- 만기에 $0으로 감소

### Greeks

**Delta (Δ)** - 방향성 노출
```
Range: 0 to 1 (calls), -1 to 0 (puts)
Meaning: Change in option price per $1 stock move

Example: Δ = 0.50
→ If stock +$1, option +$0.50
→ If stock -$1, option -$0.50
```

**Gamma (Γ)** - Delta 가속도
```
Meaning: Change in delta per $1 stock move
Peak: ATM options
Low: Deep ITM or OTM

Example: Γ = 0.05, Δ currently = 0.50
→ If stock +$1, delta becomes 0.55
```

**Theta (Θ)** - 시간가치 감소
```
Meaning: Change in option price per day
Sign: Usually negative (options lose value over time)
Peak: Last 30 days before expiration

Example: Θ = -$0.15/day
→ Tomorrow, option loses $0.15 if nothing else changes
```

**Vega (ν)** - 변동성 민감도
```
Meaning: Change in option price per 1% IV change
Sign: Always positive (options gain value when vol increases)

Example: ν = $0.25 per 1%
→ If IV increases from 25% to 26%, option +$0.25
```

**Rho (ρ)** - 금리 민감도
```
Meaning: Change in option price per 1% rate change
Sign: Positive for calls, negative for puts
Impact: Usually small unless long-dated options

Example: ρ = $0.10 per 1%
→ If interest rate increases 1%, option +$0.10
```

### 변동성: HV vs IV

**Historical Volatility (HV):**
- 과거 가격 움직임으로 계산
- 실제 데이터 기반의 객관적 수치
- 무료 사용 가능(가격 데이터 기반)

**Implied Volatility (IV):**
- 옵션 시장 가격에서 역산
- 수급 기반의 주관적 수치
- 실시간 옵션 데이터 필요(또는 사용자 입력)

**비교:**
```
IV > HV: Options expensive → Consider selling premium
IV < HV: Options cheap → Consider buying options
IV = HV: Fairly priced → Any strategy works
```

## 일반적인 워크플로

### 1. 전략 분석

```python
from scripts.black_scholes import OptionPricer

# Stock: AAPL @ $180
# Strategy: Bull Call Spread $180/$185 (30 DTE)

# Price long call ($180 strike)
long_call = OptionPricer(S=180, K=180, T=30/365, r=0.053, sigma=0.25)
long_price = long_call.call_price()
long_delta = long_call.call_delta()

# Price short call ($185 strike)
short_call = OptionPricer(S=180, K=185, T=30/365, r=0.053, sigma=0.25)
short_price = short_call.call_price()
short_delta = short_call.call_delta()

# Strategy metrics
net_debit = long_price - short_price
max_profit = (185 - 180) - net_debit
max_loss = -net_debit
position_delta = long_delta - short_delta

print(f"Bull Call Spread $180/$185")
print(f"Net Debit: ${net_debit:.2f}")
print(f"Max Profit: ${max_profit:.2f} (at $185+)")
print(f"Max Loss: ${max_loss:.2f} (at $180-)")
print(f"Position Delta: {position_delta:.4f}")
```

### 2. IV와 HV 비교

```python
# Get HV
prices = fetch_historical_prices_for_hv("AAPL", api_key, days=90)
hv = calculate_historical_volatility(prices, window=30)

# User provides IV (from broker platform)
iv = 0.28  # 28% from ThinkorSwim

print(f"Historical Volatility: {hv*100:.2f}%")
print(f"Implied Volatility: {iv*100:.1f}%")

if iv > hv * 1.1:
    print("→ Options expensive (IV > HV) - Consider selling premium")
elif iv < hv * 0.9:
    print("→ Options cheap (IV < HV) - Consider buying options")
else:
    print("→ Fairly priced")
```

### 3. Earnings 전략

earnings가 임박했는지 확인 (Earnings Calendar skill 사용):
```python
# If earnings in 7 days:
# - IV typically elevated (30-50% higher)
# - Consider straddle/strangle (profit from big move)
# - Or sell iron condor (profit from IV crush)

# Example: Long Straddle
straddle_cost = call_price + put_price
breakeven_up = stock_price + straddle_cost
breakeven_down = stock_price - straddle_cost

print(f"Straddle Cost: ${straddle_cost:.2f}")
print(f"Breakevens: ${breakeven_down:.2f} / ${breakeven_up:.2f}")
print(f"Need {abs(breakeven_up - stock_price)/stock_price*100:.1f}% move to profit")
```

## 제한사항 및 Best Practices

### 이론 가격 vs 시장 가격

**Black-Scholes 가정:**
- 유럽형 옵션 (조기 행사 불가)
- 변동성 일정 (현실에서는 변함)
- 거래 비용 없음
- 연속 거래 가능

**실무 차이점:**
- American 옵션(대부분의 주식 옵션)은 조기 행사 가능
- Bid-ask spread: 실제 체결 비용이 이론 중간값보다 큼
- 수수료 및 slippage
- 유동성: 비유동 옵션은 스프레드가 넓음

### Best Practices

**1. 교육 및 계획 용도로 사용:**
- 전략의 동작 원리 학습
- 다양한 접근법 비교
- 거래 전 risk/reward 이해

**2. 거래 전 검증:**
- 브로커에서 실시간 호가 확인
- bid-ask spread 점검
- 옵션 유동성 확인(open interest, volume)

**3. 실제 IV 입력:**
- 이론 가격은 변동성 일정 가정을 사용
- 정확도를 위해 현재 시장 IV 사용
- IV percentile 확인(과열/저점)

**4. 배당 반영:**
- Ex-dividend 날짜가 옵션 가격에 영향
- Ex-div일에 calls는 가치 하락, puts는 가치 상승
- 스크립트는 dividend yield 입력 지원

**5. Greeks 모니터링:**
- Delta: 전체 방향성 노출
- Theta: 일일 time decay (seller에게 유리)
- Vega: 변동성 리스크 (earnings 기간 주의)
- Gamma: delta 변화 리스크 (만기 근접 구간 회피)

## 다른 스킬과 통합

**Earnings Calendar:**
- earnings date 조회
- IV crush 기회 식별
- earnings 전략 타이밍 결정

**Technical Analyst:**
- strike 선택에 support/resistance 활용
- 방향성 전략용 추세 분석
- straddle 타이밍용 breakout 잠재력

**US Stock Analysis:**
- LEAPS용 펀더멘털 분석
- covered call/put용 배당수익률
- earnings 플레이용 실적 품질

**Bubble Detector:**
- 고위험 → protective puts
- 저위험 → bullish strategies
- 임계 위험 → long premium 회피

**Portfolio Manager:**
- 주식 포지션과 옵션 포지션 통합 추적
- 포트폴리오 Greeks 집계
- 헤지 도구로서 옵션 활용

## API 사용량 및 비용

**Free Tier로 충분:**
- 주가: 심볼당 1 request
- 과거 가격(HV): 심볼당 1 request
- 배당 데이터: 심볼당 1 request

**분석 예시 비용:**
```
Covered Call on AAPL:
- Current price: 1 request
- HV calculation: 1 request (90 days data)
- Dividend yield: 1 request
Total: 3 requests

Daily budget: 250 requests / day
→ Can analyze ~80 strategies per day
```

## 문제 해결

### 옵션 가격이 음수
**원인:** 입력값 오류 (strike와 주가 관계)
**해결:** 입력값의 타당성 점검

### Greeks가 이상함
**원인:** 단위 오류 (annual vs daily)
**해결:** T는 year 단위, theta는 day 단위인지 확인

### HV와 IV 차이가 큼
**정상:** IV는 미래 기대, HV는 과거 데이터
**대응:** 정확도를 위해 브로커 IV 사용

### 옵션 가격이 너무 높거나 낮음
**원인:** 변동성 입력값 오류
**해결:** sigma가 annual 기준인지 확인 (예: 25%는 0.25)

## 리소스

### 문서
- `SKILL.md` - 전체 워크플로 및 전략
- `references/strategies_guide.md` - 모든 전략 설명 (TBD)
- `references/greeks_explained.md` - Greeks 심화 설명 (TBD)

### 외부 리소스
- Options Playbook: https://www.optionsplaybook.com/
- CBOE Education: https://www.cboe.com/education/
- Black-Scholes Calculator: https://www.option-price.com/

### 실제 IV 확인
- ThinkorSwim (TD Ameritrade): Free
- TastyTrade: Free
- Barchart: https://www.barchart.com/options
- CBOE: http://www.cboe.com/delayedquote/

## 향후 개선

**계획:**
- Strategy simulation script (완전한 P/L 분석)
- P/L diagram generator (ASCII art)
- Earnings strategy advisor (Earnings Calendar와 연동)
- 완전한 전략 레퍼런스 가이드

**기여 환영:**
- 추가 전략
- 개선된 변동성 모델
- 더 나은 시각화 도구

## 라이선스

교육용 사용 목적입니다. 거래는 본인 책임이며, 옵션은 큰 리스크를 수반하고 모든 투자자에게 적합하지 않을 수 있습니다.

---

**Version:** 1.0
**Last Updated:** 2025-11-08
**Dependencies:** Python 3.8+, numpy, scipy, requests
**API:** FMP API (Free tier sufficient)
**Model:** Black-Scholes (European options pricing)
