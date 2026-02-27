# Weekly Trade Strategy Blog - 프로젝트 가이드

이 프로젝트는 미국주식의 주간 트레이드 전략 블로그를 자동 생성하기 위한 시스템입니다.

## 프로젝트 구조

```
weekly-trade-strategy/
├── charts/              # 차트 이미지 저장 폴더
│   └── YYYY-MM-DD/     # 날짜별 폴더
│       ├── chart1.jpeg
│       └── chart2.jpeg
│
├── reports/            # 분석 리포트 저장 폴더
│   └── YYYY-MM-DD/    # 날짜별 폴더
│       ├── technical-market-analysis.md
│       ├── us-market-analysis.md
│       └── market-news-analysis.md
│
├── blogs/              # 최종 블로그 기사 저장 폴더
│   └── YYYY-MM-DD-weekly-strategy.md
│
└── .claude/
    ├── agents/         # 에이전트 정의
    └── skills/         # 스킬 정의
```

## 주간 블로그 작성의 표준 절차

### 스텝 0: 준비

1. **차트 이미지 배치**
   ```bash
   # 이번 주 날짜로 폴더 생성
   mkdir -p charts/2025-11-03

   # 차트 이미지를 배치 (18장 권장)
   # - VIX (주봉)
   # - 미국 10년채 수익률 (주봉)
   # - S&P 500 Breadth Index (200일 MA + 8일 MA)
   # - Nasdaq 100 (주봉)
   # - S&P 500 (주봉)
   # - Russell 2000 (주봉)
   # - Dow Jones (주봉)
   # - 금 선물 (주봉)
   # - 구리 선물 (주봉)
   # - 원유 (주봉)
   # - 천연가스 (주봉)
   # - 우라늄 ETF (URA, 주봉)
   # - Uptrend Stock Ratio (전체 시장)
   # - 섹터 퍼포먼스 (1주간)
   # - 섹터 퍼포먼스 (1개월)
   # - 인더스트리 퍼포먼스 (상위/하위)
   # - 실적 발표 캘린더
   # - 주요 종목 히트맵
   ```

2. **리포트 출력 폴더 생성**
   ```bash
   mkdir -p reports/2025-11-03
   ```

### 스텝 1: Technical Market Analysis

**목적**: 차트 이미지를 분석하고, 테크니컬 지표로부터 시장 환경을 평가

**에이전트**: `technical-market-analyst`

**입력**:
- `charts/YYYY-MM-DD/*.jpeg` (전체 차트 이미지)

**출력**:
- `reports/YYYY-MM-DD/technical-market-analysis.md`

**실행 커맨드 예**:
```
이번 주(2025-11-03)의 차트 분석을 technical-market-analyst 에이전트로 실행해 주세요.
charts/2025-11-03/에 있는 모든 차트를 분석하고, 리포트를 reports/2025-11-03/technical-market-analysis.md에 저장해 주세요.
```

**분석 내용**:
- VIX, 10년채 수익률, Breadth 지표의 현재값과 평가
- 주요 지수(Nasdaq, S&P500, Russell2000, Dow)의 테크니컬 분석
- 원자재(금, 구리, 원유, 우라늄)의 트렌드 분석
- 섹터 로테이션 분석
- 시나리오별 확률 평가

---

### 스텝 2: US Market Analysis

**목적**: 시장 환경의 종합 평가와 버블 리스크 검출

**에이전트**: `us-market-analyst`

**입력**:
- `reports/YYYY-MM-DD/technical-market-analysis.md` (스텝 1의 결과)
- 시장 데이터(VIX, Breadth, 금리 등)

**출력**:
- `reports/YYYY-MM-DD/us-market-analysis.md`

**실행 커맨드 예**:
```
us-market-analyst 에이전트로 미국 시장의 종합 분석을 실행해 주세요.
reports/2025-11-03/technical-market-analysis.md를 참조하고,
시장 환경과 버블 리스크를 평가하여 reports/2025-11-03/us-market-analysis.md에 저장해 주세요.
```

**분석 내용**:
- 현재 시장 페이즈 (Risk-On / Base / Caution / Stress)
- 버블 검출 스코어 (0-16 스케일)
- 섹터 로테이션 패턴
- 변동성 레짐
- 리스크 요인과 카탈리스트

---

### 스텝 3: Market News Analysis

**목적**: 과거 10일간의 뉴스 영향 분석과 향후 7일간의 이벤트 예측

**에이전트**: `market-news-analyzer`

**입력**:
- `reports/YYYY-MM-DD/technical-market-analysis.md` (스텝 1의 결과)
- `reports/YYYY-MM-DD/us-market-analysis.md` (스텝 2의 결과)
- 경제 캘린더, 실적 발표 캘린더

**출력**:
- `reports/YYYY-MM-DD/market-news-analysis.md`

**실행 커맨드 예**:
```
market-news-analyzer 에이전트로 뉴스와 이벤트 분석을 실행해 주세요.
과거 10일간의 뉴스 영향과 향후 7일간의 중요 이벤트를 분석하고,
reports/2025-11-03/market-news-analysis.md에 저장해 주세요.
```

**분석 내용**:
- 과거 10일간의 주요 뉴스와 시장에 대한 영향
- 향후 7일간의 경제 지표 스케줄
- 주요 실적 발표 (시가총액 $2B 이상)
- 이벤트별 시나리오 분석 (확률 포함)
- 리스크 이벤트의 우선순위 부여

---

### 스텝 4: Weekly Blog Generation

**목적**: 3개의 리포트를 통합하여, 겸업 트레이더를 위한 주간 전략 블로그를 생성

**에이전트**: `weekly-trade-blog-writer`

**입력**:
- `reports/YYYY-MM-DD/technical-market-analysis.md`
- `reports/YYYY-MM-DD/us-market-analysis.md`
- `reports/YYYY-MM-DD/market-news-analysis.md`
- `blogs/` (전주 블로그 기사, 연속성 체크용)

**출력**:
- `blogs/YYYY-MM-DD-weekly-strategy.md`

**실행 커맨드 예**:
```
weekly-trade-blog-writer 에이전트로 2025년 11월 3일 주의 블로그 기사를 작성해 주세요.
reports/2025-11-03/ 하위의 3개 리포트를 통합하고,
전주의 섹터 배분과의 연속성을 유지하면서,
blogs/2025-11-03-weekly-strategy.md에 저장해 주세요.
```

**기사 구성** (200-300행):
1. **3줄 요약** - 시장 환경·초점·전략
2. **이번 주 액션** - 로트 관리, 매매 레벨, 섹터 배분, 중요 이벤트
3. **시나리오별 플랜** - Base/Risk-On/Caution의 3시나리오
4. **마켓 상황** - 통합 트리거(10Y/VIX/Breadth)
5. **원자재·섹터 전술** - 금/구리/우라늄/원유
6. **겸업 운용 가이드** - 아침/저녁 체크리스트
7. **리스크 관리** - 이번 주 고유의 리스크
8. **정리** - 3-5문장

**중요한 제약**:
- 전주로부터의 섹터 배분 변경은 **+-10-15% 이내** (단계적 조정)
- 사상 최고치 경신 중+Base 트리거의 경우, 급격한 포지션 축소는 피함
- 현금 배분은 단계적으로 증가 (예: 10% -> 20-25% -> 30-35%)

---

### 스텝 5 (옵션): Druckenmiller Strategy Planning

**목적**: 3개의 분석 리포트를 통합하여, 18개월의 중장기 투자 전략을 수립

**에이전트**: `druckenmiller-strategy-planner`

**입력**:
- `reports/YYYY-MM-DD/technical-market-analysis.md` (스텝 1의 결과)
- `reports/YYYY-MM-DD/us-market-analysis.md` (스텝 2의 결과)
- `reports/YYYY-MM-DD/market-news-analysis.md` (스텝 3의 결과)
- 전회의 Druckenmiller 전략 리포트 (존재하는 경우)

**출력**:
- `reports/YYYY-MM-DD/druckenmiller-strategy.md`

**실행 커맨드 예**:
```
druckenmiller-strategy-planner 에이전트로 2025년 11월 3일 시점의 18개월 전략을 수립해 주세요.
reports/2025-11-03/ 하위의 3개 리포트를 종합적으로 분석하고,
Druckenmiller식 전략 프레임워크를 적용하여,
reports/2025-11-03/druckenmiller-strategy.md에 저장해 주세요.
```

**분석 프레임워크**:

1. **Druckenmiller의 투자 철학**
   - 매크로 중시의 18개월 선행 분석
   - 확신도에 기반한 포지션 사이징
   - 복수 요인이 갖추어졌을 때의 집중 투자
   - 신속한 손절과 유연성

2. **4개의 시나리오 분석** (확률 포함)
   - **Base Case** (최고 확률 시나리오)
   - **Bull Case** (낙관 시나리오)
   - **Bear Case** (리스크 시나리오)
   - **Tail Risk** (저확률 극단 시나리오)

3. **각 시나리오의 구성 요소**
   - 주요 카탈리스트 (정책, 경기, 지정학)
   - 타임라인 (Q1-Q2, Q3-Q4의 전개)
   - 자산 클래스별 영향
   - 최적 포지셔닝 전략
   - 무효화 시그널 (전략 전환의 트리거)

**리포트 구성** (약 150-200행):
```markdown
# Strategic Investment Outlook - [Date]

## Executive Summary
[2-3단락: 지배적 테마와 전략적 포지셔닝의 요약]

## Market Context & Current Environment
### Macroeconomic Backdrop
[금융 정책, 경기 사이클, 매크로 지표의 현황]

### Technical Market Structure
[주요 테크니컬 레벨, 트렌드, 패턴]

### Sentiment & Positioning
[시장 센티먼트, 기관투자자 포지션, 역발상 기회]

## 18-Month Scenario Analysis

### Base Case Scenario (XX% probability)
**Narrative:** [가장 가능성 높은 시장의 경로]
**Key Catalysts:**
- [카탈리스트 1]
- [카탈리스트 2]
**Timeline Markers:**
- [Q1-Q2의 예상 전개]
- [Q3-Q4의 예상 전개]
**Strategic Positioning:**
- [자산 배분 권고]
- [구체적인 트레이드 아이디어와 확신도]
**Risk Management:**
- [무효화 시그널]
- [스톱로스/철수 기준]

### Bull Case Scenario (XX% probability)
[Base Case와 동일한 구성]

### Bear Case Scenario (XX% probability)
[Base Case와 동일한 구성]

### Tail Risk Scenario (XX% probability)
[Base Case와 동일한 구성]

## Recommended Strategic Actions

### High Conviction Trades
[테크니컬, 펀더멘털, 센티먼트가 갖추어진 트레이드]

### Medium Conviction Positions
[양호한 리스크/리워드이나 요인의 정합성이 낮은 포지션]

### Hedges & Protective Strategies
[리스크 관리 포지션과 포트폴리오 보험]

### Watchlist & Contingent Trades
[확인 대기 또는 특정 트리거 대기의 셋업]

## Key Monitoring Indicators
[시나리오 검증/무효화를 위한 추적 지표]

## Conclusion & Next Review Date
[최종적인 전략 권고와 다음 재검토 시기]
```

**중요한 특징**:
- 주간 블로그(단기 전술)와는 달리, **18개월의 중장기 전략**
- 매크로 경제의 구조 변화나 정책 전환점을 중시
- 확신도에 따른 포지션 사이징 (High/Medium/Low)
- 각 시나리오에 명확한 무효화 조건을 설정
- stanley-druckenmiller-investment 스킬을 활용

**실행 타이밍**:
- 주간 블로그와 동시 (분기별 권장)
- FOMC 등 중대 이벤트 후
- 시장 구조의 큰 전환점

**부족 리포트의 자동 생성**:
상류 리포트(스텝 1-3)가 존재하지 않는 경우, druckenmiller-strategy-planner는 자동으로 부족 에이전트를 호출합니다.

---

## 일괄 실행 스크립트 (권장)

```bash
# 날짜 설정
DATE="2025-11-03"

# 스텝 0: 폴더 준비
mkdir -p charts/$DATE reports/$DATE

# 스텝 1-4를 일괄 실행하는 프롬프트 예:
「$DATE 주의 트레이드 전략 블로그를 작성해 주세요.

1. technical-market-analyst로 charts/$DATE/의 전체 차트를 분석
   → reports/$DATE/technical-market-analysis.md

2. us-market-analyst로 시장 환경을 종합 평가
   → reports/$DATE/us-market-analysis.md

3. market-news-analyzer로 뉴스/이벤트 분석
   → reports/$DATE/market-news-analysis.md

4. weekly-trade-blog-writer로 최종 블로그 기사를 생성
   → blogs/$DATE-weekly-strategy.md

각 스텝을 순차 실행하고, 리포트를 확인한 후 다음으로 진행해 주세요.」
```

---

## 에이전트 간의 데이터 플로우

### 주간 블로그 생성 플로우

```
charts/YYYY-MM-DD/
  ├─> [technical-market-analyst]
  │      └─> reports/YYYY-MM-DD/technical-market-analysis.md
  │            │
  │            ├─> [us-market-analyst]
  │            │      └─> reports/YYYY-MM-DD/us-market-analysis.md
  │            │            │
  │            │            ├─> [market-news-analyzer]
  │            │            │      └─> reports/YYYY-MM-DD/market-news-analysis.md
  │            │            │            │
  │            └────────────┴────────────┴─> [weekly-trade-blog-writer]
  │                                                └─> blogs/YYYY-MM-DD-weekly-strategy.md
  │
  └─> (전주의 블로그 기사도 참조)
       blogs/YYYY-MM-DD-weekly-strategy.md (지난주)
```

### 중장기 전략 리포트 생성 플로우 (옵션)

```
reports/YYYY-MM-DD/
  ├─> technical-market-analysis.md ────┐
  ├─> us-market-analysis.md ───────────┼─> [druckenmiller-strategy-planner]
  └─> market-news-analysis.md ─────────┘      └─> reports/YYYY-MM-DD/druckenmiller-strategy.md
                                                       (18개월 투자 전략)
```

---

## 트러블슈팅

### 에이전트가 차트를 찾지 못하는 경우
- `charts/YYYY-MM-DD/` 폴더가 존재하는지 확인
- 차트 이미지의 파일 형식이 `.jpeg` 또는 `.png`인지 확인

### 리포트가 생성되지 않는 경우
- `reports/YYYY-MM-DD/` 폴더가 존재하는지 확인
- 이전 스텝의 리포트가 정상적으로 생성되었는지 확인

### 블로그 기사의 섹터 배분이 급변하는 경우
- 전주의 블로그 기사가 `blogs/`에 존재하는지 확인
- weekly-trade-blog-writer 에이전트의 연속성 체크 기능이 유효한지 확인

### 블로그 기사가 너무 긴 경우 (300행 초과)
- weekly-trade-blog-writer 에이전트 정의의 길이 제한을 확인
- 기사 생성 후, 행수를 확인: `wc -l blogs/YYYY-MM-DD-weekly-strategy.md`

---

## 권장 워크플로우

### 일요일 밤 (한국 시간) 또는 금요일 밤 (미국 시간)
1. 주말에 차트를 준비
2. technical-market-analyst를 실행
3. 결과를 확인한 후 다음 스텝으로

### 월요일 아침
4. us-market-analyst, market-news-analyzer를 실행
5. 3개의 리포트를 리뷰
6. weekly-trade-blog-writer로 블로그 생성
7. 최종 리뷰 및 공개

---

## 각 에이전트의 상세 사양

### technical-market-analyst
- **스킬**: technical-analyst, breadth-chart-analyst, sector-analyst
- **분석 대상**: 주봉 차트, Breadth 지표, 섹터 퍼포먼스
- **출력 형식**: Markdown, 시나리오별 확률 포함

### us-market-analyst
- **스킬**: market-environment-analysis, us-market-bubble-detector
- **분석 대상**: 시장 페이즈, 버블 스코어, 센티먼트
- **출력 형식**: Markdown, 리스크 평가

### market-news-analyzer
- **스킬**: market-news-analyst, economic-calendar-fetcher, earnings-calendar
- **분석 대상**: 과거 10일 뉴스, 향후 7일 이벤트
- **출력 형식**: Markdown, 이벤트별 시나리오

### weekly-trade-blog-writer
- **입력**: 상기 3개 리포트 + 전주 블로그
- **제약**: 200-300행, 단계적 조정(+-10-15%)
- **출력 형식**: 겸업 트레이더 대상 Markdown (5-10분 독해)

### druckenmiller-strategy-planner (옵션)
- **스킬**: stanley-druckenmiller-investment
- **분석 대상**: 18개월 중장기 매크로 전략, 시나리오 분석
- **입력**: 상기 3개 리포트 (technical, us-market, market-news)
- **출력 형식**: Markdown, 4시나리오(Base/Bull/Bear/Tail Risk), 확률·확신도 포함
- **특징**: Druckenmiller식 집중 투자와 신속한 손절, 매크로 전환점의 식별
- **실행 빈도**: 분기별, 또는 FOMC 등 중대 이벤트 후

---

## 버전 관리

- **프로젝트 버전**: 1.0
- **최종 업데이트일**: 2025-11-02
- **유지보수**: 이 문서는 정기적으로 업데이트해 주세요

---

## 연락처·피드백

이 워크플로우에 관한 개선 제안이나 문제 보고는 프로젝트의 Issue 트래커에 보고해 주세요.
