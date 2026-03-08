# Pair Trade Screener

cointegration 테스트와 mean-reversion 분석을 사용해 pair trading 기회를 식별하고 분석하는 Statistical arbitrage 도구입니다.

## Overview

Pair Trade Screener는 통계적으로 유의미한 pair trading 기회를 다음 방식으로 찾습니다:
- cointegration(장기 균형 관계) 테스트
- hedge ratio(beta 값) 계산
- mean-reversion 속도(half-life) 측정
- z-score 임계값 기반 진입/청산 신호 생성

**Market Neutral Strategy:** 전체 시장 방향과 무관하게 상대 가격 움직임에서 수익을 추구합니다.

## Features

✅ **Sector-wide screening** - 섹터 내 모든 종목 분석
✅ **Custom pair analysis** - 특정 종목 조합 테스트
✅ **Statistical rigor** - cointegration 테스트(ADF), correlation 분석
✅ **Mean-reversion metrics** - half-life 계산, z-score 추적
✅ **Trade signals** - 자동 진입/청산 추천
✅ **FMP API integration** - 무료 티어로도 스크리닝 가능
✅ **JSON output** - 후속 분석을 위한 구조화 결과

## Installation

### Prerequisites

- Python 3.8+
- FMP API key (free tier: 250 requests/day)

### Install Dependencies

```bash
pip install pandas numpy scipy statsmodels requests
```

### Get FMP API Key

1. 방문: https://financialmodelingprep.com/developer/docs
2. 무료 계정 가입
3. API key 복사
4. 환경 변수 설정:

```bash
export FMP_API_KEY="your_key_here"
```

또는 영구 적용을 위해 `~/.bashrc` / `~/.zshrc`에 추가하세요.

## Usage

### Quick Start

```bash
# Screen Technology sector for pairs
python scripts/find_pairs.py --sector Technology

# Analyze specific pair
python scripts/analyze_spread.py --stock-a AAPL --stock-b MSFT
```

### Screening for Pairs

**Sector-Based Screening:**

```bash
# Screen entire sector
python scripts/find_pairs.py --sector Financials

# Adjust correlation threshold
python scripts/find_pairs.py --sector Energy --min-correlation 0.75

# Longer lookback period
python scripts/find_pairs.py --sector Healthcare --lookback-days 1095
```

**Custom Stock List:**

```bash
# Test specific stocks
python scripts/find_pairs.py --symbols AAPL,MSFT,GOOGL,META,NVDA

# Tech giants pair screening
python scripts/find_pairs.py --symbols JPM,BAC,WFC,C,GS,MS
```

**Full Options:**

```bash
python scripts/find_pairs.py \
  --sector Technology \
  --min-correlation 0.70 \
  --min-market-cap 10000000000 \
  --lookback-days 730 \
  --output tech_pairs.json \
  --api-key YOUR_KEY
```

### Analyzing Individual Pairs

**Basic Analysis:**

```bash
python scripts/analyze_spread.py --stock-a AAPL --stock-b MSFT
```

**Custom Parameters:**

```bash
python scripts/analyze_spread.py \
  --stock-a JPM \
  --stock-b BAC \
  --lookback-days 365 \
  --entry-zscore 2.0 \
  --exit-zscore 0.5 \
  --api-key YOUR_KEY
```

## Example Output

### Pair Screening Results

```
PAIR TRADING SCREEN SUMMARY
==========================================================================

Total pairs analyzed: 45
Cointegrated pairs: 12
Pairs with trade signals: 5

==========================================================================
ACTIVE TRADE SIGNALS
==========================================================================

Pair: XOM/CVX
  Signal: LONG
  Z-Score: -2.35
  Correlation: 0.9421
  P-Value: 0.0012
  Half-Life: 28.3 days
  Strength: ★★★
```

### Individual Pair Analysis

```
PAIR TRADE ANALYSIS: AAPL / MSFT
==========================================================================

[ PAIR STATISTICS ]
  Correlation: 0.8732
  Hedge Ratio (Beta): 1.1523
  Data Points: 365

[ COINTEGRATION TEST ]
  ADF Statistic: -3.8542
  P-value: 0.0028
  Result: ✅ COINTEGRATED (p < 0.05)
  Strength: ★★★ Very Strong

[ MEAN REVERSION ]
  Half-Life: 42.1 days
  Speed: Moderate (suitable for pair trading)

[ Z-SCORE ]
  Current Z-Score: -2.13
  Historical Range: [-3.45, 3.12]

[ TRADE SIGNAL ]
  Signal: 🔺 LONG SPREAD
  Action: Long AAPL, Short MSFT
  Rationale: Z-score = -2.13 → AAPL cheap relative to MSFT

[ POSITION SIZING ]
  Example Allocation: $10,000
  LONG AAPL: $5,000 (27 shares @ $185.50)
  SHORT MSFT: $5,762 (14 shares @ $411.25)

  Exit Conditions:
    - Primary: Z-score crosses 0 (mean reversion)
    - Stop Loss: Z-score > ±3.0
    - Time-based: No reversion after 90 days
```

## Understanding the Metrics

### Correlation
- **Range:** -1 to +1
- **Threshold:** ≥ 0.70 required
- **Interpretation:** 높을수록 동행성이 강함

### Cointegration P-Value
- **Range:** 0 to 1
- **Threshold:** < 0.05 required (통계적으로 유의)
- **Interpretation:** 낮을수록 cointegration이 강함
  - p < 0.01: ★★★ Very strong
  - p 0.01-0.05: ★★ Moderate
  - p > 0.05: ☆ Not cointegrated (reject)

### Half-Life
- **Meaning:** 스프레드가 평균으로 절반 되돌아오는 데 걸리는 시간
- **Fast:** < 30 days (단기 트레이딩에 이상적)
- **Moderate:** 30-60 days (표준 pair trading)
- **Slow:** > 60 days (장기 포지션)

### Z-Score
- **Calculation:** (Current Spread - Mean) / Std Dev
- **Entry Signals:**
  - Z > +2.0: Short spread (Short A, Long B)
  - Z < -2.0: Long spread (Long A, Short B)
- **Exit:** Z가 0을 통과(평균회귀)
- **Stop:** |Z| > 3.0 (극단적 괴리)

### Hedge Ratio (Beta)
- **Meaning:** Stock A $1당 필요한 Stock B 달러 금액
- **Example:** Beta = 1.2 → A를 $1,000 long할 때 B를 $1,200 short
- **Purpose:** Market-neutral 포지셔닝(net beta ≈ 0)

## Common Workflows

### 1. Weekly Pair Screening

```bash
# Monday: Screen for new opportunities
python scripts/find_pairs.py --sector Technology --output tech_pairs.json

# Review top pairs in JSON output
cat tech_pairs.json | jq '.pairs[] | select(.signal != "NONE")'

# Detailed analysis on top candidates
python scripts/analyze_spread.py --stock-a AAPL --stock-b MSFT
```

### 2. Sector Rotation Pairs

```bash
# Screen multiple sectors
for sector in Technology Financials Healthcare Energy; do
  python scripts/find_pairs.py --sector $sector --output ${sector}_pairs.json
  sleep 5
done

# Find pairs with strongest signals
cat *_pairs.json | jq '.pairs[] | select(.current_zscore | . > 2 or . < -2)'
```

### 3. Monitor Existing Pairs

```bash
# Update z-scores for current positions
python scripts/analyze_spread.py --stock-a XOM --stock-b CVX
python scripts/analyze_spread.py --stock-a JPM --stock-b BAC
python scripts/analyze_spread.py --stock-a GOOGL --stock-b META
```

## API Usage & Rate Limits

**Free Tier:**
- 250 API requests/day
- 가격 데이터 기준 종목당 약 2 requests
- 약 60개 종목/일 스크리닝 가능 (= 1,770 pairs)

**Screening Costs:**
```
Sector screening (30 stocks):
  - Fetch 30 stock prices = 30 requests
  - Analyze 435 pairs (30 choose 2) = 0 additional requests
  - Total: 30 requests

Individual pair analysis:
  - Fetch 2 stock prices = 2 requests
```

**Tips:**
- 섹터 스크린은 일일이 아닌 주 1회 실행
- JSON 파일로 결과 캐시
- 특정 pair는 매일 모니터링(각 2 requests)
- 여러 섹터를 매일 스크리닝한다면 유료 플랜 업그레이드 고려

## Interpretation Guide

### When to Trade

✅ **Strong Pair (Enter):**
- Correlation > 0.80
- P-value < 0.03
- Half-life 20-60 days
- |Z-score| > 2.0
- Economic linkage (same sector/industry)

⚠️ **Marginal Pair (Caution):**
- Correlation 0.70-0.80
- P-value 0.03-0.05
- Half-life > 60 days
- |Z-score| 1.5-2.0

❌ **Weak Pair (Avoid):**
- Correlation < 0.70
- P-value > 0.05
- Half-life > 90 days or undefined
- Economic linkage 부재

### Exit Conditions

**Primary Exit:**
- Z-score가 0을 통과(스프레드 평균회귀)
- 양쪽 레그를 동시에 청산

**Stop Loss:**
- |Z-score| > 3.0 (극단적 괴리, 구조적 붕괴 가능성)
- -5% loss on spread
- 즉시 청산

**Time-Based:**
- 90일(또는 3× half-life) 내 mean reversion이 없으면 청산
- 더 좋은 기회를 위해 자본 회수

## Troubleshooting

### No pairs found

**Solutions:**
- `--min-correlation`을 0.65로 낮춤
- 종목 유니버스 확대(다른 섹터 시도)
- `--lookback-days`를 1095(3년)로 증가

### API rate limit exceeded

**Solutions:**
- 24시간 대기(무료 티어는 매일 리셋)
- 스크리닝 결과를 JSON으로 캐시
- 유료 플랜(Starter tier $14/mo) 업그레이드

### All z-scores near zero

**Normal:** pair들이 균형 구간에 있어 신호가 없음
**Action:** 나중에 재확인하거나 유니버스 확대

### Pair correlation broke down

**Causes:** 기업 이벤트, M&A, 비즈니스 모델 변화
**Detection:** 최근 correlation << 과거 correlation
**Action:** pair 청산 후 watchlist에서 제거

## Integration with Other Skills

**Backtest Expert:**
- pair trading 전략 백테스트
- entry/exit 임계값 최적화
- 견고성 검증

**Sector Analyst:**
- 순환 중인 섹터 식별
- 주도 섹터 내부 pair 스크리닝

**Technical Analyst:**
- 개별 종목 추세 확인
- 진입 전 support/resistance 확인

**Portfolio Manager:**
- 다수 pair 포지션 추적
- 전체 market-neutral 익스포저 모니터링

## Resources

**Documentation:**
- `references/methodology.md` - Statistical arbitrage 이론
- `references/cointegration_guide.md` - cointegration 테스트 가이드

**FMP API:**
- API Docs: https://financialmodelingprep.com/developer/docs
- Historical Price API: `/v3/historical-price-full/{symbol}`
- Stock Screener API: `/v3/stock-screener`

**Academic Papers:**
- Engle & Granger (1987): "Co-Integration and Error Correction"
- Gatev et al. (2006): "Pairs Trading: Performance of a Relative-Value Arbitrage Rule"

## License

교육 및 연구 목적용입니다. 거래 책임은 본인에게 있습니다. 과거 성과는 미래 수익을 보장하지 않습니다.

---

**Version:** 1.0
**Last Updated:** 2025-11-08
**Dependencies:** Python 3.8+, pandas, numpy, scipy, statsmodels, requests
**API:** FMP API (free tier sufficient)
