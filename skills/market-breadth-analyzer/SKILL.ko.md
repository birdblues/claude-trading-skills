---
name: market-breadth-analyzer
description: TraderMonty의 공개 CSV 데이터를 활용하여 시장 브레드스 건강도를 정량화합니다. 6개 구성 요소에 걸쳐 0-100 복합 점수를 생성합니다 (100 = 건강). API 키 불필요. 시장 브레드스, 참가율, 등락 건강도, 랠리가 광범위한지 여부, 또는 전반적인 시장 건강도 평가를 요청할 때 사용합니다.
---

# Market Breadth Analyzer 스킬

## 목적

데이터 기반 6-구성요소 스코어링 시스템(0-100)을 사용하여 시장 브레드스 건강도를 정량화합니다. TraderMonty의 공개 CSV 데이터를 사용하여 랠리 또는 하락에 시장이 얼마나 광범위하게 참여하고 있는지 측정합니다.

**점수 방향:** 100 = 최고 건강도 (광범위한 참가), 0 = 심각한 약세.

**API 키 불필요** - GitHub Pages에서 무료로 제공되는 CSV 데이터를 사용합니다.

## 이 스킬을 사용하는 경우

**English:**
- User asks "Is the market rally broad-based?" or "How healthy is market breadth?"
- User wants to assess market participation rate
- User asks about advance-decline indicators or breadth thrust
- User wants to know if the market is narrowing (fewer stocks participating)
- User asks about equity exposure levels based on breadth conditions

**Korean:**
- "마켓 브레드스는 어떤가요?" "시장 참가율은?"
- "상승이 확산되고 있나?" "일부 종목만의 상승인가?"
- 브레드스 지표에 기반한 익스포저 판단
- 시장의 건강도를 데이터로 확인하고 싶다

## Breadth Chart Analyst와의 차이점

| 항목 | Market Breadth Analyzer | Breadth Chart Analyst |
|------|------------------------|----------------------|
| 데이터 소스 | CSV (자동) | 차트 이미지 (수동) |
| API 필요 여부 | 없음 | 없음 |
| 출력 | 정량적 0-100 점수 | 정성적 차트 분석 |
| 구성 요소 | 6개 채점 차원 | 시각적 패턴 인식 |
| 재현성 | 완전 재현 가능 | 분석가 의존적 |

---

## 실행 워크플로우

### Phase 1: Python 스크립트 실행

분석 스크립트를 실행합니다:

```bash
python3 skills/market-breadth-analyzer/scripts/market_breadth_analyzer.py \
  --detail-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv" \
  --summary-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv"
```

스크립트가 수행하는 작업:
1. 상세 CSV (~2,500행, 2016-현재) 및 요약 CSV (8개 지표) 가져오기
2. 데이터 최신성 검증 (5일 이상 오래된 경우 경고)
3. 6개 구성 요소 점수 계산 (데이터 부족 시 자동 가중치 재분배)
4. 구간 분류를 포함한 복합 점수 생성
5. 점수 이력 추적 및 추세 계산 (개선 중/악화 중/안정)
6. JSON 및 Markdown 리포트 출력

### Phase 2: 결과 제시

생성된 Markdown 리포트를 사용자에게 제시하며, 다음 항목을 강조합니다:
- 복합 점수 및 건강 구간
- 가장 강한/약한 구성 요소
- 권장 주식 비중
- 주목해야 할 주요 브레드스 수준
- 데이터 최신성 경고 (있는 경우)

---

## 6-구성요소 스코어링 시스템

| # | 구성 요소 | 가중치 | 핵심 신호 |
|---|-----------|--------|------------|
| 1 | 브레드스 수준 & 추세 | **25%** | 현재 8MA 수준 + 200MA 추세 방향 + 8MA 방향 조정자 |
| 2 | 8MA vs 200MA 크로스오버 | **20%** | MA 갭과 방향을 통한 모멘텀 |
| 3 | 고점/저점 사이클 | **20%** | 브레드스 사이클 내 위치 |
| 4 | 베어리시 신호 | **15%** | 백테스트된 약세 신호 플래그 |
| 5 | 역사적 백분위 | **10%** | 현재 vs 전체 이력 분포 |
| 6 | S&P 500 다이버전스 | **10%** | 멀티 윈도우 (20일 + 60일) 가격 vs 브레드스 다이버전스 |

**가중치 재분배:** 구성 요소에 충분한 데이터가 없는 경우(예: 고점/저점 마커 미탐지), 해당 구성 요소는 제외되고 가중치는 나머지 구성 요소에 비례하여 재분배됩니다. 리포트에는 원래 가중치와 실효 가중치가 모두 표시됩니다.

**점수 이력:** 복합 점수는 실행 간에 유지됩니다 (데이터 날짜 기준 키). 리포트에는 여러 관측값이 있는 경우 추세 요약 (개선 중/악화 중/안정)이 포함됩니다.

## 건강 구간 매핑 (100 = 건강)

| 점수 | 구간 | 주식 비중 | 행동 |
|-------|------|-----------------|--------|
| 80-100 | 강세 | 90-100% | 풀 포지션, 성장/모멘텀 선호 |
| 60-79 | 건강 | 75-90% | 정상 운용 |
| 40-59 | 중립 | 60-75% | 선택적 포지셔닝, 손절가 조임 |
| 20-39 | 약화 | 40-60% | 수익 실현, 현금 비중 확대 |
| 0-19 | 심각 | 25-40% | 자본 보전, 저점 형성 대기 |

---

## 데이터 소스

**상세 CSV:** `market_breadth_data.csv`
- 2016-02부터 현재까지 ~2,500행
- 컬럼: Date, S&P500_Price, Breadth_Index_Raw, Breadth_Index_200MA, Breadth_Index_8MA, Breadth_200MA_Trend, Bearish_Signal, Is_Peak, Is_Trough, Is_Trough_8MA_Below_04

**요약 CSV:** `market_breadth_summary.csv`
- 8개 집계 지표 (평균 고점, 평균 저점, 횟수, 분석 기간)

두 파일 모두 GitHub Pages에 공개 호스팅되어 있으며, 인증이 필요하지 않습니다.

## 출력 파일

- JSON: `market_breadth_YYYY-MM-DD_HHMMSS.json`
- Markdown: `market_breadth_YYYY-MM-DD_HHMMSS.md`
- 이력: `market_breadth_history.json` (실행 간 유지, 최대 20개 항목)

## 참고 문서

### `references/breadth_analysis_methodology.md`
- 구성 요소 채점 세부 사항이 포함된 전체 방법론
- 임계값 설명 및 구간 정의
- 역사적 맥락 및 해석 가이드

### 참고 문서 로드 시점
- **첫 사용 시:** 프레임워크 이해를 위해 방법론 참고 문서 로드
- **정기 실행 시:** 스크립트가 채점을 처리하므로 참고 문서 불필요
