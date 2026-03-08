# VCP 스크리너 점수 체계

## 5개 구성요소 복합 점수

| Component | Weight | Source |
|-----------|--------|--------|
| Trend Template (Stage 2) | 25% | 7-point Minervini criteria |
| Contraction Quality | 25% | VCP pattern detection |
| Volume Pattern | 20% | Volume dry-up analysis |
| Pivot Proximity | 15% | Distance from breakout level |
| Relative Strength | 15% | Minervini-weighted RS vs S&P 500 |

## 구성요소별 점수 상세

### 1. Trend Template (0-100)

7개 기준 각각이 14.3점을 기여합니다:

| Criteria Passed | Score | Status |
|-----------------|-------|--------|
| 7/7 | 100 | Perfect Stage 2 |
| 6/7 | 85.8 | Pass (minimum threshold) |
| 5/7 | 71.5 | Borderline |
| <= 4/7 | <= 57 | Fail |

**통과 기준:** VCP 분석으로 진행하려면 Score >= 85 (6개 이상 충족).

### 2. Contraction Quality (0-100)

| # Contractions | Base Score |
|----------------|-----------|
| 4 | 90 |
| 3 | 80 |
| 2 | 60 |
| 1 or invalid | 0-40 |

**가감점:**
- 타이트한 마지막 수축(depth < 5%): +10
- 평균 수축 비율 양호(T1의 0.4 미만): +10
- 깊은 T1(> 30%): -10

### 3. Volume Pattern (0-100)

dry-up ratio(최근 10개 봉 평균 / 50일 평균) 기준:

| Dry-Up Ratio | Base Score |
|-------------|-----------|
| < 0.30 | 90 |
| 0.30-0.50 | 75 |
| 0.50-0.70 | 60 |
| 0.70-1.00 | 40 |
| > 1.00 | 20 |

**가감점:**
- 1.5x+ 거래량 breakout: +10
- 순매집 일수 3일 초과(20일 내): +10
- 순분배 일수 3일 초과(20일 내): -10

### 4. Pivot Proximity (0-100) — Distance-Priority Scoring

점수는 거리 우선(distance-first)입니다. 거래량 확인 보너스는 pivot 상단 0-5% 구간에서만 추가됩니다(Minervini: pivot 상단 5% 초과 추격 매수 금지).

| Distance from Pivot | Base Score | Volume Bonus | Final Score | Trade Status |
|--------------------|-----------|-------------|------------|--------------|
| 0-3% above | 90 | +10 | 100 | BREAKOUT CONFIRMED |
| 3-5% above | 65 | +10 | 75 | EXTENDED - Moderate chase risk (vol confirmed) |
| 5-10% above | 50 | — (none) | 50 | EXTENDED - High chase risk |
| 10-20% above | 35 | — (none) | 35 | EXTENDED - Very high chase risk |
| >20% above | 20 | — (none) | 20 | OVEREXTENDED - Do not chase |
| 0 to -2% below | 90 | — | 90 | AT PIVOT (within 2%) |
| -2% to -5% | 75 | — | 75 | NEAR PIVOT |
| -5% to -8% | 60 | — | 60 | APPROACHING |
| -8% to -10% | 45 | — | 45 | DEVELOPING |
| -10% to -15% | 30 | — | 30 | EARLY |
| < -15% | 10 | — | 10 | FAR FROM PIVOT |

**거래량 보너스 규칙:**
- pivot 상단 0-3% + 거래량: +10점, status = "BREAKOUT CONFIRMED"
- pivot 상단 3-5% + 거래량: +10점, status에 "(vol confirmed)" 추가
- pivot 상단 >5%: 거래량 보너스 없음(Minervini: 확장 breakout 추격 금지)
- pivot 하단: 거래량 보너스 해당 없음

**추격 리스크 규칙(Minervini):** pivot 상단 5% 초과 종목은 매수하지 않습니다. 거리가 base score를 결정하고, 거래량 확인은 보너스일 뿐 override가 아닙니다.

### 5. Relative Strength (0-100)

Minervini 가중치(최근 성과를 더 강조):
- 40%: 최근 3개월(63 거래일)
- 20%: 최근 6개월(126 거래일)
- 20%: 최근 9개월(189 거래일)
- 20%: 최근 12개월(252 거래일)

| Weighted RS vs S&P 500 | Score | RS Rank Estimate |
|-------------------------|-------|------------------|
| >= +50% | 100 | ~99 (top 1%) |
| >= +30% | 95 | ~95 (top 5%) |
| >= +20% | 90 | ~90 (top 10%) |
| >= +10% | 80 | ~80 (top 20%) |
| >= +5% | 70 | ~70 (top 30%) |
| >= 0% | 60 | ~60 (top 40%) |
| >= -5% | 50 | ~50 (average) |
| >= -10% | 40 | ~40 |
| >= -20% | 20 | ~25 |
| < -20% | 0 | ~10 |

## Rating Bands

| Composite Score | Rating | Position Sizing | Action |
|-----------------|--------|-----------------|--------|
| 90-100 | Textbook VCP | 1.5-2x normal | Buy at pivot, aggressive |
| 80-89 | Strong VCP | 1x normal | Buy at pivot, standard |
| 70-79 | Good VCP | 0.75x normal | Buy on volume confirmation |
| 60-69 | Developing VCP | Wait | Watchlist only |
| 50-59 | Weak VCP | Skip | Monitor only |
| < 50 | No VCP | Skip | Not actionable |

### valid_vcp Gate Rule

VCP 패턴 계산기가 `valid_vcp=false`를 반환할 때(예: contraction ratio가 0.75를 초과, 확장형 contraction), composite score와 무관하게 rating 상한이 적용됩니다:

- `valid_vcp=false` AND composite >= 70이면: rating을 **"Developing VCP"**로 강제하고 가이던스를 "Watchlist only - VCP pattern not validated, do not buy"로 설정
- `valid_vcp=false` AND composite < 70이면: override 불필요(이미 실행 불가 임계값 아래)

이 규칙은 확장형 또는 비수축 패턴 종목이 실행 가능한 매수 rating을 받는 것을 방지합니다.

## Entry Ready 조건

다음 조건을 모두 충족할 때 종목은 `entry_ready=True`로 분류됩니다:

| Condition | Default Threshold | CLI Override |
|-----------|-------------------|--------------|
| `valid_vcp` | `True` | `--no-require-valid-vcp` |
| `distance_from_pivot_pct` | -8.0% to +3.0% | `--max-above-pivot` |
| `dry_up_ratio` | <= 1.0 | — |
| `risk_pct` | <= 15.0% | `--max-risk` |

**리포트 섹션:**
- **Section A: Pre-Breakout Watchlist** — `entry_ready=True` 종목, composite score 순 정렬
- **Section B: Extended / Quality VCP** — `entry_ready=False` 종목, composite score 순 정렬

**CLI mode:**
- `--mode all` (default): 두 섹션 모두 출력
- `--mode prebreakout`: `entry_ready=True` 종목만 출력

## Pre-Filter 기준 (Phase 1)

quote 데이터만으로 빠르게 필터링(과거 데이터 불필요):

| Criterion | Threshold | Purpose |
|-----------|-----------|---------|
| Price | > $10 | Penny stock 제외 |
| % above 52w low | > 20% | 대략 상승 추세 구간 |
| % below 52w high | < 30% | 깊은 조정 구간 제외 |
| Average volume | > 200,000 | 충분한 유동성 |
