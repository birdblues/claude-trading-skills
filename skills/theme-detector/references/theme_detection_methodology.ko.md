# Theme Detection 방법론

## 개요

Theme Detector는 시장 테마를 식별하고 순위를 매기며 상태를 평가하기 위해 **3차원 스코어링 모델**을 사용합니다. 단일 점수 랭킹과 달리, 이 접근법은 테마의 강도(heat), 성숙도 단계(lifecycle), 신호 신뢰도(confidence)를 독립 차원으로 분리합니다.

---

## 차원 1: Theme Heat (0-100)

Theme Heat는 테마의 **방향 중립적 강도**를 측정합니다. Heat 점수가 높다는 것은 강세/약세와 무관하게 해당 테마의 시장 활동이 크다는 뜻입니다.

### 구성 요소

#### 1.1 Momentum Score (가중치: 35%)

구성 industry의 다중 기간 가중 수익률(1W 10%, 1M 25%, 3M 35%, 6M 30%)에 log-sigmoid 함수를 적용해 방향 중립 모멘텀 강도를 측정합니다.

**수식:**
```
weighted_return = perf_1w * 0.10 + perf_1m * 0.25 + perf_3m * 0.35 + perf_6m * 0.30
momentum_score = 100 / (1 + exp(-2.0 * (ln(1 + |weighted_return|) - ln(16))))
```

중간점은 |15%| 가중 수익률이며, 로그 변환으로 극단값을 압축해 중간 구간 분해능을 높입니다.

**데이터 소스:** FINVIZ industry 성과(1W, 1M, 3M, 6M change %)

**스코어링 구간:**
| Absolute Change % | Score |
|-------------------|-------|
| >= 5%             | 100   |
| 3-5%              | 80    |
| 1-3%              | 60    |
| 0.5-1%            | 40    |
| < 0.5%            | 20    |

참고: 절대값을 사용하므로 강한 상승/하락 모두 높은 heat를 생성합니다.

#### 1.2 Volume Score (가중치: 20%)

테마 전반의 비정상 거래량 활동을 측정합니다.

**수식:**
```
volume_score = normalize(avg_relative_volume, scale=[0.5, 3.0] -> [0, 100])

avg_relative_volume = MEAN(stock_volume / stock_avg_volume) for all stocks in theme
```

**데이터 소스:** FINVIZ relative volume (volume / avg volume 비율)

**스코어링 구간:**
| Relative Volume | Score |
|-----------------|-------|
| >= 3.0          | 100   |
| 2.0-3.0         | 80    |
| 1.5-2.0         | 60    |
| 1.0-1.5         | 40    |
| < 1.0           | 20    |

#### 1.3 Uptrend Ratio Score (가중치: 25%)

테마 내 technical uptrend 상태인 종목 비율을 측정합니다.

**수식:**
```
uptrend_score = normalize(uptrend_ratio, scale=[0%, 100%] -> [0, 100])

uptrend_ratio = count(stocks_in_uptrend) / count(total_stocks)
```

**데이터 소스:** uptrend-dashboard 출력(3-point 평가: price > 50-day SMA, 50-day SMA > 200-day SMA, 200-day SMA rising)

**uptrend 데이터가 없을 때:** FINVIZ의 price-above-SMA200을 대체 지표로 사용합니다. Confidence에는 20% 페널티를 적용합니다.

**스코어링 구간:**
| Uptrend Ratio | Score |
|---------------|-------|
| >= 80%        | 100   |
| 60-80%        | 80    |
| 40-60%        | 60    |
| 20-40%        | 40    |
| < 20%         | 20    |

참고: 약세 테마는 비율을 반전해 downtrend ratio를 사용합니다.

#### 1.4 Breadth Score (가중치: 20%)

테마 참여가 얼마나 폭넓은지(대형주 소수 쏠림 여부)를 측정합니다.

**수식:**
```
breadth_score = normalize(participation_rate, scale=[0%, 100%] -> [0, 100])

participation_rate = count(stocks_moving_in_direction > 1%) / count(total_stocks)
```

**데이터 소스:** FINVIZ 종목 레벨 성과 데이터

**스코어링 구간:**
| Participation Rate | Score |
|-------------------|-------|
| >= 80%            | 100   |
| 60-80%            | 80    |
| 40-60%            | 60    |
| 20-40%            | 40    |
| < 20%             | 20    |

### Theme Heat 종합식

```
theme_heat = (momentum_score * 0.35) + (volume_score * 0.20) + (uptrend_score * 0.25) + (breadth_score * 0.20)
```

---

## 차원 2: Lifecycle Maturity

Lifecycle 평가는 테마를 **Emerging**, **Accelerating**, **Trending**, **Mature**, **Exhausting**의 5단계 중 하나로 분류합니다. 이는 신흥 기회와 과밀 트레이드를 구분하는 핵심 요소입니다.

### 구성 요소

#### 2.1 Duration Score (가중치: 25%)

테마가 얼마나 오래 활성 상태였는지(heat 고점 구간의 연속 주차)를 측정합니다.

**측정 방식:** theme_heat >= 40인 주차 수를 집계.

| Duration | Stage Signal |
|----------|-------------|
| 1-3 weeks | Early |
| 4-8 weeks | Mid |
| 9-16 weeks | Late |
| > 16 weeks | Exhaustion |

**제약:** Duration 추적은 히스토리 데이터가 필요합니다. 첫 실행에서는 duration을 "Unknown"으로 두고 다른 요인만으로 lifecycle을 산출합니다.

#### 2.2 Extremity Clustering Score (가중치: 25%)

테마 내 종목 중 52주 고점/저점 부근에 있는 종목 비율을 측정합니다.

**수식:**
```
extremity_pct = count(within_5pct_of_52wk_high_or_low) / count(total_stocks)
```

| Extremity % | Stage Signal |
|-------------|-------------|
| < 20%       | Early |
| 20-40%      | Mid |
| 40-60%      | Late |
| > 60%       | Exhaustion |

**데이터 소스:** FINVIZ 52-week high/low 데이터

#### 2.3 Price Extreme Saturation Score (가중치: 25%)

52주 극단값(5% 이내) 부근 종목 비중을 측정합니다.

**수식:**
```
bullish: pct = count(dist_from_52w_high <= 0.05) / total
bearish: pct = count(dist_from_52w_low <= 0.05) / total
score = min(100, pct * 200)
```

#### 2.4 Valuation Score (가중치: 15%)

테마 구성 종목의 평균 P/E를 S&P 500 P/E 대비 상대값으로 평가합니다.

**수식:**
```
relative_pe = avg_theme_pe / sp500_pe
```

| Relative P/E | Stage Signal |
|---------------|-------------|
| < 0.8         | Early (undervalued) |
| 0.8-1.2       | Mid (fair value) |
| 1.2-2.0       | Late (overvalued) |
| > 2.0         | Exhaustion (extreme) |

**데이터 소스:** FMP API의 P/E (옵션; fallback으로 FINVIZ forward P/E 사용)

#### 2.5 ETF Proliferation Score (가중치: 10%)

해당 테마를 추종하는 ETF 개수입니다. ETF가 많을수록 개인/기관의 주목도가 높습니다.

**소스:** `thematic_etf_catalog.md` (정적 레퍼런스)

| ETF Count | Score | Stage Signal |
|-----------|-------|-------------|
| 0         | 0     | Very Early |
| 1         | 20    | Early |
| 2-3       | 40    | Mid |
| 4-6       | 60    | Mid-Late |
| 7-10      | 80    | Late |
| > 10      | 100   | Exhaustion |

### Lifecycle Maturity 종합식

```
maturity = (duration * 0.25) + (extremity * 0.25) + (price_extreme * 0.25) + (valuation * 0.15) + (etf_proliferation * 0.10)
```

### Lifecycle 단계 분류

maturity 점수 기반 분류:

| Maturity Score | Stage |
|----------------|-------|
| 0-20 | Emerging |
| 20-40 | Accelerating |
| 40-60 | Trending |
| 60-80 | Mature |
| 80-100 | Exhausting |

**참고:** Media/Narrative Saturation은 자동 maturity 계산에 포함되지 않습니다. Claude의 WebSearch 내러티브 확인으로 lifecycle 평가를 정성적으로 보정할 수 있습니다.

---

## 차원 3: Confidence (Low / Medium / High)

Confidence는 데이터 품질과 확인 신호를 바탕으로 테마 탐지의 **신뢰도**를 측정합니다.

### 레이어

#### 3.1 Quantitative Layer (기본값)

데이터 폭과 일관성 기준:

| Condition | Level |
|-----------|-------|
| >= 4 industries matching, >= 20 stocks analyzed | High |
| 2-3 industries matching, >= 10 stocks analyzed | Medium |
| 1 industry matching or < 10 stocks | Low |

#### 3.2 Breadth Layer (modifier)

섹터 간 참여도가 높을수록 Confidence를 가산합니다.

| Condition | Modifier |
|-----------|----------|
| Theme spans 3+ sectors | +1 level (cap at High) |
| Theme spans 2 sectors | No change |
| Theme in 1 sector only | -1 level (floor at Low) |

#### 3.3 Narrative Layer (modifier, Step 4 적용)

WebSearch 확인 결과로 Confidence를 조정합니다.

| Narrative Finding | Modifier |
|-------------------|----------|
| Strong confirmation (multiple sources, clear catalysts) | +1 level |
| Mixed signals | No change |
| Contradictory narrative (bearish articles for bullish theme) | -1 level |

### 최종 Confidence

```
confidence = apply_modifiers(quantitative_base, breadth_modifier, narrative_modifier)
confidence = clamp(confidence, Low, High)
```

---

## Direction Detection

테마 방향(**leading** vs. **lagging**)은 절대 수익률이 아니라 상대 순위로 결정됩니다.

### 알고리즘

1. 각 industry는 모멘텀 순위 리스트에서의 위치로 `rank_direction`을 받습니다: 상위 절반 = "bullish"(leading), 하위 절반 = "bearish"(lagging).
2. 테마 방향은 구성 industry의 `rank_direction` 다수결로 정합니다.

```python
# Industry-level (industry_ranker.py)
rank_direction = "bullish" if rank <= len(industries) // 2 else "bearish"

# Theme-level (theme_classifier.py)
direction = majority_vote([ind.rank_direction for ind in theme.industries])
```

### 중요: 절대값이 아닌 상대값

**LEAD/LAG 방향은 상대 개념입니다.** "lagging" 테마도 절대 수익률은 플러스일 수 있으며, 다른 테마 대비 상대적으로 약할 뿐입니다. 따라서:
- **LEAD** 테마: 비중 확대/신규 포지션 후보
- **LAG** 테마: 비중 축소 후보(언더웨이트), **숏 시그널은 아님**

---

## 데이터 소스

### Primary: FINVIZ

**Elite Mode (권장):**
- CSV export endpoint: `https://elite.finviz.com/export.ashx?v=151&f=ind_{code},cap_smallover,...&auth=KEY`
- 제공 필드: ticker, company, sector, industry, market cap, P/E, change%, volume, avg volume, 52wk high/low, RSI, SMA20/50/200
- Rate limit: 요청 간 0.5초
- Coverage: industry별 전체 종목 유니버스

**Public Mode (fallback):**
- HTML scraping: `https://finviz.com/screener.ashx?v=151&f=ind_{code},cap_smallover`
- 제공 필드: 유사하지만 page 1에 한정(산업당 약 20종목)
- Rate limit: 요청 간 2.0초(과도한 scraping은 차단 가능)
- Coverage: industry별 시가총액 상위 20종목

### Secondary: FMP API (옵션)

- 밸류에이션 분석용 P/E 비율
- 필수 아님; fallback으로 FINVIZ forward P/E 사용
- 더 세밀한 밸류에이션 지표에 유용

### Tertiary: uptrend-dashboard (옵션)

- uptrend-dashboard 스킬의 CSV 출력
- 종목별 3-point technical evaluation 제공
- uptrend ratio 정확도를 크게 개선
- 미사용 시 FINVIZ price-vs-SMA200을 대체 사용

### Quaternary: WebSearch (narrative layer)

- Step 4의 내러티브 확인에 사용
- 자동화되지 않음; 워크플로 중 Claude가 검색 수행
- 매체 보도량/애널리스트 심리에 대한 정성 평가

---

## uptrend-dashboard 통합

uptrend-dashboard 데이터가 있으면 테마 탐지기는 강화된 3-point 평가를 사용합니다.

**3-Point 평가 기준:**
1. Price > 50-day SMA (단기 추세)
2. 50-day SMA > 200-day SMA (중기 추세, golden/death cross)
3. 200-day SMA 상승 중 (장기 추세 확인)

**3개 조건 모두 충족** = 확정 uptrend
**0개 충족** = 확정 downtrend

단순한 price-above-SMA200 대체 지표보다 uptrend ratio를 더 정확하게 제공합니다.

---

## 출력 스키마

### JSON 출력 구조

```json
{
  "metadata": {
    "date": "2026-02-16",
    "mode": "elite",
    "themes_analyzed": 14,
    "industries_scanned": 145,
    "total_stocks": 5200,
    "uptrend_data_available": true,
    "execution_time_seconds": 150
  },
  "themes": [
    {
      "name": "AI & Semiconductors",
      "direction": "Bullish",
      "direction_strength": "Strong",
      "theme_heat": 82,
      "heat_components": {
        "momentum": 90,
        "volume": 75,
        "uptrend": 85,
        "breadth": 70
      },
      "lifecycle": {
        "stage": "Late",
        "duration_weeks": 12,
        "extremity_pct": 45,
        "relative_pe": 1.8,
        "etf_proliferation_score": 100,
        "etf_count": 11
      },
      "confidence": "High",
      "confidence_components": {
        "quantitative": "High",
        "breadth_modifier": "+1",
        "narrative_modifier": "pending"
      },
      "industries": [
        {
          "name": "Semiconductors",
          "change_pct": 4.2,
          "avg_relative_volume": 1.8,
          "uptrend_ratio": 0.75,
          "stock_count": 35
        }
      ],
      "top_stocks": [
        {"ticker": "NVDA", "change_pct": 6.5, "relative_volume": 2.1},
        {"ticker": "AVGO", "change_pct": 4.8, "relative_volume": 1.9}
      ],
      "proxy_etfs": ["SMH", "SOXX", "AIQ", "BOTZ"]
    }
  ],
  "industry_rankings": {
    "top_10": [...],
    "bottom_10": [...]
  },
  "sector_summary": {
    "Technology": {"uptrend_ratio": 0.65, "avg_change_pct": 2.1},
    "Energy": {"uptrend_ratio": 0.40, "avg_change_pct": -1.5}
  }
}
```

---

## 알려진 한계

1. **정적 테마 정의**: 섹터 간 테마는 `cross_sector_themes.md`에 사전 정의되어 있습니다. 갑작스러운 신규 테마(예: 밈주 테마)는 자동 탐지되지 않습니다.

2. **Industry 세분화 한계**: FINVIZ industry 분류가 투자 테마와 완전히 일치하지 않을 수 있습니다. 일부 industry는 여러 테마에 걸칩니다.

3. **단일 종목 지배 효과**: 대형주(예: AI에서 NVDA)가 테마 지표를 왜곡할 수 있습니다. 시가총액 가중은 이를 더 증폭합니다.

4. **시간 지연**: 주간 성과 데이터는 장중/당일 모멘텀 변화를 반영하지 못합니다.

5. **ETF 카탈로그 노후화**: 테마 ETF 카탈로그는 수동 관리되어 최근 ETF 상장/폐지를 즉시 반영하지 못할 수 있습니다.

6. **Public 모드 데이터 한계**: 산업당 약 20개 종목만 반영되어 small/mid-cap 참여가 과소추정될 수 있습니다.

7. **Duration 추적 한계**: 첫 실행 분석에서는 히스토리 베이스라인이 없어 duration을 평가할 수 없습니다.

8. **내러티브 주관성**: WebSearch 기반 Confidence 조정은 본질적으로 주관적이며 검색 결과 품질에 좌우됩니다.

9. **생존자 편향**: 현재 상장/활성 상태 종목과 ETF만 분석하므로 상장폐지·청산 자산은 반영되지 않습니다.

10. **FINVIZ 지연 데이터**: Public FINVIZ 데이터는 15분 지연되며, Elite는 장중 실시간을 제공합니다.
