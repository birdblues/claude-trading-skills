# Instrument Notation Standard

시장 분석 문서 전반에서 일관된 종목 명명을 위한 reference 문서입니다.

## 표준 표기 표

| Asset | Ticker (ETF) | Ticker (Futures) | Full Name (EN) | Japanese | Notes |
|-------|-------------|-------------------|----------------|----------|-------|
| Gold | GLD | GC | Gold | 金 / ゴールド / 金先物 | GLD = SPDR Gold Shares ETF; GC = COMEX Gold Futures |
| Silver | SLV | SI | Silver | 銀 | SLV = iShares Silver Trust; SI = COMEX Silver Futures |
| S&P 500 | SPY | ES | S&P 500 | S&P500 | SPY = SPDR S&P 500 ETF; SPX = index; ES = E-mini Futures |
| S&P 500 Index | -- | SPX | S&P 500 Index | S&P500指数 | Cash index, not tradable directly |
| Volatility | -- | VIX | CBOE VIX | 恐怖指数 / VIX | VIX = index; VXX/UVXY = ETPs |
| US Treasuries | TLT | ZB | 20+ Year Treasury | 米国債 / 10年債 | TLT = iShares 20+ Year; ZB = 30Y futures |
| Crude Oil | USO | CL | WTI Crude Oil | 原油 / WTI | USO = United States Oil Fund; CL = NYMEX WTI Futures |

## 자릿수 힌트 (가격 스케일 검증)

자릿수 힌트 시스템은 보고된 가격이 해당 종목의 올바른 자릿수
order of magnitude에 있는지 검증합니다.
소수점 앞 숫자 개수를 기준으로 판단합니다.

| Instrument | Digit Range | Typical Price Range | Example Valid | Example Invalid |
|------------|------------|---------------------|---------------|-----------------|
| GLD | 2-3 | $100 - $999 | GLD: $268 | GLD: $2,800 (futures price) |
| GC | 3-4 | $1,000 - $9,999 | GC: $2,650 | GC: $265 (ETF price) |
| SPY | 2-3 | $100 - $999 | SPY: $580 | SPY: $5,800 (index price) |
| SPX | 4-5 | $1,000 - $99,999 | SPX: $5,800 | SPX: $580 (ETF price) |
| VIX | 1-2 | $1 - $99 | VIX: $18 | VIX: $180 |
| TLT | 2-3 | $10 - $999 | TLT: $92 | TLT: $9 |
| SLV | 2-2 | $10 - $99 | SLV: $28 | SLV: $280 |
| SI | 2-2 | $10 - $99 | SI: $31 | SI: $3,100 (total contract) |
| USO | 2-2 | $10 - $99 | USO: $72 | USO: $720 |
| CL | 2-3 | $10 - $999 | CL: $78 | CL: $7 |

### 흔한 실수

1. **ETF/Futures 혼동**: 실제로는 GC(gold futures) 가격인데 GLD로 라벨링하거나 그 반대.
   Gold ETF ~$260 vs Gold Futures ~$2,600.
2. **Index/ETF 혼동**: 실제로는 SPX인데 SPY로 라벨링하거나 그 반대.
   SPY ~$580 vs SPX ~$5,800.
3. **주당 가격 vs 계약당 가격**: futures 가격은 보통 단위당
   (예: gold는 트로이온스당), ETF 가격은 주당 가격입니다.

## 통화쌍 표기

| Standard | Alternatives | Avoid |
|----------|-------------|-------|
| USD/JPY | USDJPY, ドル円 | JPY/USD (reversed) |
| EUR/USD | EURUSD, ユーロドル | USD/EUR (reversed) |
| GBP/USD | GBPUSD, ポンドドル | USD/GBP (reversed) |

**관례**: Base currency / Quote currency.
가격은 base currency 1단위를 사기 위해 필요한 quote currency 수량을 의미합니다.

## Index 표기

| Preferred | Alternatives | Context |
|-----------|-------------|---------|
| S&P 500 | S&P500, SP500 | General references |
| SPX | S&P 500 Index | When citing the cash index value |
| SPY | SPDR S&P 500 ETF | When citing the ETF price |
| Dow | DJIA, Dow Jones, DJI | Dow Jones Industrial Average |
| Nasdaq | COMP, QQQ, NDX | Nasdaq Composite (COMP) vs Nasdaq-100 (NDX/QQQ) |
| Russell 2000 | RUT, IWM | RUT = index, IWM = ETF |

## Commodity 표기

| Commodity | Futures Ticker | ETF Ticker | Japanese |
|-----------|---------------|------------|----------|
| Gold | GC | GLD, IAU | 金, ゴールド |
| Silver | SI | SLV | 銀 |
| Crude Oil (WTI) | CL | USO | 原油, WTI |
| Natural Gas | NG | UNG | 天然ガス |
| Copper | HG | COPX | 銅 |

## Best Practices

1. **문서마다 표기 체계를 하나로 정하고** 일관되게 사용하세요.
2. **첫 언급 시** 티커와 함께 전체 이름을 표기하세요:
   "SPDR Gold Shares (GLD) traded at $268."
3. **같은 자산에서 ETF와 futures 티커를 혼용하지 마세요**.
   필요 시 명시적으로 라벨링하세요(예: "GLD (ETF) vs GC (futures)").
4. **일본어 문서**는 일본어 자산명을 써도 되지만,
   첫 언급에는 티커를 포함하세요:
   "金（GLD）は$268で取引。"
