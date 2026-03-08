---
name: market-top-detector
description: O'Neil Distribution Days, Minervini Leading Stock Deterioration, Monty Defensive Sector Rotation을 결합해 시장 고점 확률을 탐지합니다. 0-100 composite score와 risk zone 분류를 생성합니다. 사용자가 시장 고점 리스크, distribution days, defensive rotation, 리더십 붕괴, 주식 익스포저 축소 여부를 묻는 경우 사용하세요. 10-20% 조정에 선행하는 2-8주 전술 시그널에 초점을 둡니다.
---

# Market Top Detector Skill

## 목적

정량 6-컴포넌트 점수(0-100)를 사용해 시장 고점 형성 확률을 탐지합니다. 검증된 3가지 고점 탐지 방법론을 통합합니다.

1. **O'Neil** - Distribution Day 누적(기관 매도)
2. **Minervini** - Leading stock 악화 패턴
3. **Monty** - Defensive sector rotation 신호

Bubble Detector(거시/수개월 평가)와 달리, 이 스킬은 **10-20% 시장 조정에 선행하는 2-8주 전술 타이밍 신호**에 초점을 둡니다.

## 이 스킬을 사용해야 할 때

**English:**
- User asks "Is the market topping?" or "Are we near a top?"
- User notices distribution days accumulating
- User observes defensive sectors outperforming growth
- User sees leading stocks breaking down while indices hold
- User asks about reducing equity exposure timing
- User wants to assess correction probability for the next 2-8 weeks

**Korean:**
- "천장이 가까운가?" "지금 수익 실현을 해야 하나?"
- 디스트리뷰션 데이 축적에 대한 우려
- 디펜시브 섹터가 그로스 대비 아웃퍼폼
- 선도주는 무너지는데 지수는 버티는 상황
- 익스포저 축소 타이밍 판단
- 향후 2~8주 조정 확률 평가

## Bubble Detector와의 차이

| Aspect | Market Top Detector | Bubble Detector |
|--------|-------------------|-----------------|
| Timeframe | 2-8 weeks | Months to years |
| Target | 10-20% correction | Bubble collapse (30%+) |
| Methodology | O'Neil/Minervini/Monty | Minsky/Kindleberger |
| Data | Price/Volume + Breadth | Valuation + Sentiment + Social |
| Score Range | 0-100 composite | 0-15 points |

---

## 실행 워크플로우

### Phase 1: WebSearch를 통한 데이터 수집

Python 스크립트 실행 전에 아래 데이터를 WebSearch로 수집합니다.
**데이터 최신성 요구:** 모든 데이터는 최근 3영업일 이내여야 합니다. 오래된 데이터는 분석 품질을 떨어뜨립니다.

```
1. S&P 500 Breadth (200DMA above %)
   AUTO-FETCHED from TraderMonty CSV (no WebSearch needed)
   The script fetches this automatically from GitHub Pages CSV data.
   Override: --breadth-200dma [VALUE] to use a manual value instead.
   Disable: --no-auto-breadth to skip auto-fetch entirely.

2. [REQUIRED] S&P 500 Breadth (50DMA above %)
   Valid range: 20-100
   Primary search: "S&P 500 percent stocks above 50 day moving average"
   Fallback: "market breadth 50dma site:barchart.com"
   Record the data date

3. [REQUIRED] CBOE Equity Put/Call Ratio
   Valid range: 0.30-1.50
   Primary search: "CBOE equity put call ratio today"
   Fallback: "CBOE total put call ratio current"
   Fallback: "put call ratio site:cboe.com"
   Record the data date

4. [OPTIONAL] VIX Term Structure
   Values: steep_contango / contango / flat / backwardation
   Primary search: "VIX VIX3M ratio term structure today"
   Fallback: "VIX futures term structure contango backwardation"
   Note: Auto-detected from FMP API if VIX3M quote available.
   CLI --vix-term overrides auto-detection.

5. [OPTIONAL] Margin Debt YoY %
   Primary search: "FINRA margin debt latest year over year percent"
   Fallback: "NYSE margin debt monthly"
   Note: Typically 1-2 months lagged. Record the reporting month.
```

### Phase 2: Python 스크립트 실행

수집한 데이터를 CLI 인자로 전달해 스크립트를 실행합니다.

```bash
python3 skills/market-top-detector/scripts/market_top_detector.py \
  --api-key $FMP_API_KEY \
  --breadth-50dma [VALUE] --breadth-50dma-date [YYYY-MM-DD] \
  --put-call [VALUE] --put-call-date [YYYY-MM-DD] \
  --vix-term [steep_contango|contango|flat|backwardation] \
  --margin-debt-yoy [VALUE] --margin-debt-date [YYYY-MM-DD] \
  --output-dir reports/ \
  --context "Consumer Confidence=[VALUE]" "Gold Price=[VALUE]"
# 200DMA breadth is auto-fetched from TraderMonty CSV.
# Override with --breadth-200dma [VALUE] if needed.
# Disable with --no-auto-breadth to skip auto-fetch.
```

스크립트 동작:
1. FMP API에서 S&P 500, QQQ, VIX 시세 및 히스토리 수집
2. Leading ETF (ARKK, WCLD, IGV, XBI, SOXX, SMH, KWEB, TAN) 데이터 수집
3. Sector ETF (XLU, XLP, XLV, VNQ, XLK, XLC, XLY) 데이터 수집
4. 6개 컴포넌트 계산
5. Composite score와 보고서 생성

### Phase 3: 결과 제시

생성된 Markdown 보고서를 사용자에게 제시할 때 다음을 강조하세요:
- Composite score 및 risk zone
- 데이터 최신성 경고(3일 초과 데이터)
- 최강 경고 신호(가장 높은 컴포넌트 점수)
- 과거 유사 패턴 비교(가장 가까운 historical top)
- What-if 시나리오(핵심 변수 민감도)
- Risk zone별 권장 액션
- Follow-Through Day 상태(해당 시)
- 이전 실행 대비 변화(이전 보고서가 있을 경우)

---

## 6-컴포넌트 점수 체계

| # | Component | Weight | Data Source | Key Signal |
|---|-----------|--------|-------------|------------|
| 1 | Distribution Day Count | **25%** | FMP API | 최근 25거래일 기관 매도 누적 |
| 2 | Leading Stock Health | **20%** | FMP API | 성장 ETF 바스켓 악화 |
| 3 | Defensive Sector Rotation | **15%** | FMP API | Defensive vs Growth 상대성과 |
| 4 | Market Breadth Divergence | **15%** | Auto (CSV) + WebSearch | 지수 레벨 대비 200DMA(자동)/50DMA(수동) breadth |
| 5 | Index Technical Condition | **15%** | FMP API | MA 구조, 실패 반등, lower highs |
| 6 | Sentiment & Speculation | **10%** | FMP + WebSearch | VIX, Put/Call, term structure |

## Risk Zone 매핑

| Score | Zone | Risk Budget | Action |
|-------|------|-------------|--------|
| 0-20 | Green (Normal) | 100% | Normal operations |
| 21-40 | Yellow (Early Warning) | 80-90% | 손절 기준 강화, 신규 진입 축소 |
| 41-60 | Orange (Elevated Risk) | 60-75% | 약한 포지션 차익실현 |
| 61-80 | Red (High Probability Top) | 40-55% | 공격적 차익실현 |
| 81-100 | Critical (Top Formation) | 20-35% | 최대 방어, 헤지 강화 |

---

## API 요구사항

**필수:** FMP API key (free tier로도 충분: 실행당 약 33 calls)
**선택:** WebSearch로 breadth/sentiment 데이터 보강(정확도 향상)

## 출력 파일

- JSON: `market_top_YYYY-MM-DD_HHMMSS.json`
- Markdown: `market_top_YYYY-MM-DD_HHMMSS.md`

## Reference 문서

### `references/market_top_methodology.md`
- O'Neil, Minervini, Monty 프레임워크 전체 방법론
- 컴포넌트 점수 상세 및 임계값
- 과거 검증 노트

### `references/distribution_day_guide.md`
- O'Neil Distribution Day 상세 규칙
- Stalling day 식별
- Follow-Through Day (FTD) 메커니즘

### `references/historical_tops.md`
- 2000, 2007, 2018, 2022 시장 고점 분석
- 과거 고점 시기 컴포넌트 점수 패턴
- 교훈 및 캘리브레이션 데이터

### Reference 로드 시점
- **첫 사용:** `market_top_methodology.md` 로드로 프레임워크 이해
- **Distribution day 질문:** `distribution_day_guide.md` 로드
- **과거 비교 맥락:** `historical_tops.md` 로드
- **정기 실행:** reference 없이도 가능 - 스크립트가 점수 계산 처리
