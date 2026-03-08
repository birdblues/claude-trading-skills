# Conviction Matrix - 시그널→액션 매핑

멀티 스킬 시그널 조합을 구체적인 익스포저 및 액션 권고로 변환하기 위한 정량 교차 참조 테이블입니다.

## 1. Market Top Zone x Macro Regime 매트릭스

top risk와 regime의 교차점에 따른 권장 **equity exposure %**:

| Market Top Zone → | Green (0-20) | Yellow (21-40) | Orange (41-60) | Red (61-80) | Critical (81-100) |
|-------------------|:---:|:---:|:---:|:---:|:---:|
| **Broadening** | 95-100% | 80-90% | 65-75% | 45-55% | 25-35% |
| **Concentration** | 85-95% | 70-80% | 55-65% | 35-45% | 15-25% |
| **Transitional** | 80-90% | 65-75% | 50-60% | 30-40% | 10-20% |
| **Inflationary** | 70-80% | 55-65% | 40-50% | 25-35% | 5-15% |
| **Contraction** | 60-70% | 45-55% | 30-40% | 15-25% | 0-10% |

**사용법:** 현재 Market Top 점수 zone과 Macro Regime의 교차 셀을 찾으면 권장 equity allocation 범위를 얻을 수 있습니다.

## 2. Breadth Zone x VCP Availability 매트릭스

권장 **new position entry** 공격성:

| Breadth Zone → | Healthy (60+) | Recovering (40-59) | Weak (20-39) | Critical (<20) |
|----------------|:---:|:---:|:---:|:---:|
| **Textbook VCP (90+)** | Full size, aggressive | 75% size | 50% size, pilot only | No new entries |
| **Strong VCP (80-89)** | Full size | 75% size | 25% size, pilot | No new entries |
| **Good VCP (70-79)** | 75% size | 50% size | Watchlist only | No new entries |
| **Developing (60-69)** | Watchlist | Watchlist | Pass | Pass |

## 3. FTD State x Market Top Risk 매트릭스

조정 이후 권장 **re-entry behavior**:

| FTD State → | FTD Confirmed | Rally Attempt | No Signal | Rally Failed |
|-------------|:---:|:---:|:---:|:---:|
| **Top < 30 (Low Risk)** | Aggressive re-entry, 80%+ | Moderate entry, 60% | Normal operations | Monitor only |
| **Top 30-50 (Moderate)** | Measured re-entry, 60% | Small pilot, 30% | Stay cautious | Stay defensive |
| **Top 50-70 (Elevated)** | Selective entry, 40% | Watchlist only | Reduce exposure | Maximum defense |
| **Top > 70 (High Risk)** | Contrarian pilot, 25% | No new entries | Sell rallies | Full cash/hedge |

**핵심 인사이트:** FTD Confirmed + Top > 70 = Pattern 3 (Extreme Sentiment Contrarian). 이는 Druckenmiller의 "가장 큰 돈은 베어마켓에서 벌린다" 셋업입니다.

## 4. Macro Regime x Theme Quality 매트릭스

권장 **sector/theme tilt**:

| Regime → | Broadening | Concentration | Transitional | Inflationary | Contraction |
|----------|:---:|:---:|:---:|:---:|:---:|
| **Hot themes (70+)** | Ride themes, broad | Ride themes in mega-caps | Selective theme plays | Commodity themes only | Avoid, preserve cash |
| **Moderate themes (40-69)** | Diversified across themes | Index-weighted | Wait for clarity | Real assets focus | Defensive only |
| **Cold themes (<40)** | Value/cyclical rotate | Mega-cap safety | Cash heavy | Gold/commodities | Full defensive |

## 5. Signal Convergence 해석

| Convergence Score | Meaning | Action |
|-------------------|---------|--------|
| 80-100 | All ducks in a row | Maximum conviction sizing |
| 60-79 | Most signals agree | Standard conviction sizing |
| 40-59 | Mixed signals | Reduced sizing, selective |
| 20-39 | Conflicting signals | Minimal positions, high cash |
| 0-19 | Complete disagreement | Sit out entirely |

## 6. 종합 Conviction 의사결정 트리

```
Conviction >= 80 AND Convergence >= 70
  → Maximum exposure, concentrated positions
  → "Go for the jugular" - Druckenmiller

Conviction 60-79 AND Pattern = Policy Pivot
  → Overweight equity, lean into regime transition
  → "Focus on central banks and liquidity"

Conviction 40-59 AND Pattern = Unsustainable Distortion
  → Reduce to 40-50% equity, tighten all stops
  → "It's how much you lose when wrong"

Conviction < 40 AND FTD = Confirmed
  → Contrarian pilot positions (25-40% equity)
  → "Most money made in bear markets"

Conviction < 40 AND FTD != Confirmed
  → Capital preservation mode (10-30% equity)
  → "When you don't see it, don't swing"
```

## 7. Position Sizing Quick Reference

| Conviction Zone | Max Single | Max Positions | Daily Vol Target |
|----------------|:---:|:---:|:---:|
| Maximum (80-100) | 25% | 8 | 0.40% |
| High (60-79) | 15% | 12 | 0.30% |
| Moderate (40-59) | 10% | 15 | 0.25% |
| Low (20-39) | 5% | 20 | 0.15% |
| Preservation (0-19) | 3% | 25 | 0.10% |
