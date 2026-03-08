---
name: uptrend-analyzer
description: Monty의 Uptrend Ratio Dashboard 데이터를 사용해 시장 breadth를 진단합니다. 5개 구성요소(브레드스, 섹터 참여도, 로테이션, 모멘텀, 히스토리컬 컨텍스트)로 0-100 복합 점수를 생성합니다. 시장 breadth, uptrend ratio, 혹은 현재 시장 환경이 주식 익스포저를 지지하는지 묻는 경우 사용하세요. API 키는 필요하지 않습니다.
---

# Uptrend Analyzer 스킬

## 목적

Monty의 Uptrend Ratio Dashboard를 사용해 시장 breadth 건전성을 진단합니다. 이 대시보드는 11개 섹터 전반의 미국 주식 약 2,800개를 추적합니다. 0-100 복합 점수(높을수록 건전)를 생성하고 익스포저 가이던스를 제공합니다.

Market Top Detector(API 기반 리스크 점수기)와 달리, 이 스킬은 무료 CSV 데이터를 사용해 "참여 breadth"(시장 상승이 광범위한지, 좁은지)를 평가합니다.

## 이 스킬을 사용할 때

**영어:**
- 사용자가 "시장 breadth는 건강한가?" 또는 "랠리의 폭은 얼마나 넓은가?"라고 묻는 경우
- 사용자가 섹터별 uptrend ratio 평가를 원하는 경우
- 사용자가 시장 참여도 또는 breadth 상황에 대해 묻는 경우
- 사용자가 breadth 분석 기반 익스포저 가이던스를 필요로 하는 경우
- 사용자가 Monty의 Uptrend Dashboard 또는 uptrend ratio를 언급하는 경우

**한국어:**
- "시장 브레드스는 건전한가?" "상승의 저변은 넓은가?"
- 섹터별 업트렌드 비율을 확인하고 싶다
- 시장 참가율·브레드스 상황을 진단하고 싶다
- 브레드스 분석에 기반한 익스포저 가이던스가 필요하다
- Monty의 업트렌드 대시보드에 대한 질문

## Market Top Detector와의 차이

| 항목 | Uptrend Analyzer | Market Top Detector |
|--------|-----------------|-------------------|
| 점수 방향 | 높을수록 건전 | 높을수록 위험 |
| 데이터 소스 | 무료 GitHub CSV | FMP API (유료) |
| 초점 | breadth 참여도 | 천장 형성 위험 |
| API 키 | 불필요 | 필요 (FMP) |
| 방법론 | Monty Uptrend Ratios | O'Neil/Minervini/Monty |

---

## 실행 워크플로

### Phase 1: Python 스크립트 실행

분석 스크립트를 실행합니다(API 키 불필요):

```bash
python3 skills/uptrend-analyzer/scripts/uptrend_analyzer.py
```

스크립트는 다음을 수행합니다:
1. Monty의 GitHub 저장소에서 CSV 데이터를 다운로드
2. 5개 구성요소 점수 계산
3. 복합 점수 및 리포트 생성

### Phase 2: 결과 제시

생성된 Markdown 리포트를 사용자에게 제시하며 다음을 강조합니다:
- 복합 점수와 zone 분류
- 익스포저 가이던스(Full/Normal/Reduced/Defensive/Preservation)
- 가장 강한/약한 섹터를 보여주는 섹터 heatmap
- 핵심 모멘텀 및 로테이션 시그널

---

## 5-구성요소 점수 체계

| # | 구성요소 | 가중치 | 핵심 신호 |
|---|-----------|--------|------------|
| 1 | Market Breadth (Overall) | **30%** | ratio 수준 + 추세 방향 |
| 2 | Sector Participation | **25%** | uptrend 섹터 수 + ratio spread |
| 3 | Sector Rotation | **15%** | Cyclical vs Defensive 균형 |
| 4 | Momentum | **20%** | slope 방향 + 가속도 |
| 5 | Historical Context | **10%** | 히스토리 내 percentile 순위 |

## 점수 구간(Scoring Zones)

| 점수 | Zone | 익스포저 가이던스 |
|-------|------|-------------------|
| 80-100 | Strong Bull | Full Exposure (100%) |
| 60-79 | Bull | Normal Exposure (80-100%) |
| 40-59 | Neutral | Reduced Exposure (60-80%) |
| 20-39 | Cautious | Defensive (30-60%) |
| 0-19 | Bear | Capital Preservation (0-30%) |

### 7-레벨 Zone 상세

각 점수 구간은 더 정밀한 평가를 위해 하위 구간으로 세분화됩니다:

| 점수 | Zone Detail | 색상 |
|-------|-------------|-------|
| 80-100 | Strong Bull | Green |
| 70-79 | Bull-Upper | Light Green |
| 60-69 | Bull-Lower | Light Green |
| 40-59 | Neutral | Yellow |
| 30-39 | Cautious-Upper | Orange |
| 20-29 | Cautious-Lower | Orange |
| 0-19 | Bear | Red |

### Warning 시스템

활성 warning은 복합 점수가 높아도 익스포저 가이던스를 더 보수적으로 만들기 위해 penalty를 적용합니다:

| Warning | 조건 | Penalty |
|---------|-----------|---------|
| **Late Cycle** | Commodity 평균 > Cyclical, Defensive 둘 다 | -5 |
| **High Spread** | 섹터 ratio max-min spread > 40pp | -3 |
| **Divergence** | 그룹 내 std > 8pp, spread > 20pp, 또는 추세 이탈 섹터 존재 | -3 |

Penalty는 누적(최대 -10)되며, 2개 이상 활성 시 multi-warning discount(+1)를 적용합니다. 복합 점수 산출 후 적용됩니다.

### 모멘텀 스무딩

slope 값은 점수화 전에 EMA(3)(지수이동평균, span=3)으로 스무딩합니다. 가속도는 스무딩 slope의 최근 10포인트 평균과 이전 10포인트 평균(10v10 윈도우)을 비교해 계산하며, 데이터가 20포인트 미만이면 5v5를 사용합니다.

### 히스토리컬 신뢰도 지표

Historical Context 구성요소는 다음 기준의 신뢰도 평가를 포함합니다:
- **샘플 크기:** 사용 가능한 과거 데이터 포인트 수
- **Regime coverage:** 관측된 시장 국면(강세/약세/중립) 다양성
- **Recency:** 최신 데이터 포인트의 최근성

신뢰도 레벨: High, Medium, Low.

---

## API 요구사항

**필수:** 없음(무료 GitHub CSV 데이터 사용)

## 출력 파일

- JSON: `uptrend_analysis_YYYY-MM-DD_HHMMSS.json`
- Markdown: `uptrend_analysis_YYYY-MM-DD_HHMMSS.md`

## 참고 문서

### `references/uptrend_methodology.md`
- Uptrend Ratio 정의 및 threshold
- 5-구성요소 점수 방법론
- 섹터 분류(Cyclical/Defensive/Commodity)
- 히스토리컬 캘리브레이션 노트

### 참고 문서를 불러올 때
- **최초 사용:** 전체 프레임워크 이해를 위해 `uptrend_methodology.md` 로드
- **일반 실행:** 참고 문서 불필요 - 스크립트가 점수 계산 처리
