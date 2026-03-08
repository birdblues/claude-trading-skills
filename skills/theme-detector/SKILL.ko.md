---
name: theme-detector
description: 섹터 전반의 트렌딩 시장 테마를 감지하고 분석합니다. 사용자가 현재 시장 테마, 상승/하락 섹터, 섹터 로테이션, 테마형 투자, 어떤 테마가 과열/냉각 상태인지, 또는 라이프사이클 분석을 포함한 강세/약세 내러티브 식별을 요청할 때 사용하세요.
---

# Theme Detector

## 개요

이 스킬은 섹터 간 모멘텀, 거래량, 브레드스 신호를 분석하여 트렌딩 시장 테마를 탐지하고 순위를 매깁니다. 강세(상승 모멘텀)와 약세(하방 압력) 테마를 모두 식별하고, 라이프사이클 성숙도(초기/중기/후기/소진)를 평가하며, 정량 데이터와 내러티브 분석을 결합한 Confidence 점수를 제공합니다.

**3차원 스코어링 모델:**
1. **Theme Heat** (0-100): 방향 중립적 테마 강도 (모멘텀, 거래량, 상승 추세 비율, 브레드스)
2. **Lifecycle Maturity**: 지속 기간, 극단값 군집, 밸류에이션, ETF 확산도를 기반으로 한 단계 분류 (Early / Mid / Late / Exhaustion)
3. **Confidence** (Low / Medium / High): 정량 브레드스와 내러티브 확인을 결합한 신호 신뢰도

**핵심 기능:**
- FINVIZ industry 데이터를 활용한 섹터 간 테마 탐지
- 방향 인식 스코어링(강세/약세)
- 과밀 테마와 신흥 테마를 구분하기 위한 라이프사이클 성숙도 평가
- ETF 확산도 점수(ETF가 많을수록 더 성숙/과밀한 테마)
- uptrend-dashboard와 통합한 3-point 평가
- 듀얼 모드 동작: FINVIZ Elite(빠름) 또는 public scraping(느림, 제한적)
- 상위 테마에 대한 WebSearch 기반 내러티브 확인

---

## 이 스킬을 사용할 때

**명시적 트리거:**
- "지금 어떤 시장 테마가 트렌딩이야?"
- "어떤 섹터가 뜨고/식고 있어?"
- "현재 시장 테마를 탐지해줘"
- "가장 강한 강세/약세 내러티브가 뭐야?"
- "AI/청정에너지/방산이 아직도 강한 테마야?"
- "섹터 로테이션이 어디로 향하고 있어?"
- "테마 투자 기회를 보여줘"

**암시적 트리거:**
- 사용자가 광범위한 시장 내러티브 변화 파악을 원함
- 테마형 ETF 또는 섹터 배분 아이디어를 찾고 있음
- 과밀 트레이드 또는 후기 사이클 테마를 묻고 있음
- 어떤 테마가 신흥인지 vs 소진됐는지 알고 싶어 함

**사용하지 말아야 할 때:**
- 개별 종목 분석(대신 us-stock-analysis 사용)
- 차트 리딩이 필요한 특정 섹터 심층 분석(대신 sector-analyst 사용)
- 포트폴리오 리밸런싱(대신 portfolio-manager 사용)
- 배당/인컴 투자(대신 value-dividend-screener 사용)

---

## 워크플로

### Step 1: 요구사항 확인

필수 API 키와 의존성을 확인합니다:

```bash
# Check for FINVIZ Elite API key (optional but recommended)
echo $FINVIZ_API_KEY

# Check for FMP API key (optional, used for valuation metrics)
echo $FMP_API_KEY
```

**요구사항:**
- `requests`, `beautifulsoup4`, `lxml`이 설치된 **Python 3.7+**
- **FINVIZ Elite API key** (industry 커버리지와 속도 측면에서 권장)
- **FMP API key** (옵션, P/E ratio 밸류에이션 데이터용)
- FINVIZ Elite가 없으면 public FINVIZ scraping을 사용(산업당 약 20개 종목, 속도 제한으로 느림)

**설치:**
```bash
pip install requests beautifulsoup4 lxml
```

### Step 2: Theme Detection 스크립트 실행

메인 탐지 스크립트를 실행합니다:

```bash
python3 skills/theme-detector/scripts/theme_detector.py \
  --output-dir reports/
```

**스크립트 옵션:**
```bash
# Full run (public FINVIZ mode, no API key required)
python3 skills/theme-detector/scripts/theme_detector.py \
  --output-dir reports/

# With FINVIZ Elite API key
python3 skills/theme-detector/scripts/theme_detector.py \
  --finviz-api-key $FINVIZ_API_KEY \
  --output-dir reports/

# With FMP API key for enhanced stock data
python3 skills/theme-detector/scripts/theme_detector.py \
  --fmp-api-key $FMP_API_KEY \
  --output-dir reports/

# Custom limits
python3 skills/theme-detector/scripts/theme_detector.py \
  --max-themes 5 \
  --max-stocks-per-theme 5 \
  --output-dir reports/

# Explicit FINVIZ mode
python3 skills/theme-detector/scripts/theme_detector.py \
  --finviz-mode public \
  --output-dir reports/
```

**예상 실행 시간:**
- FINVIZ Elite 모드: 약 2-3분 (14개 이상 테마)
- Public FINVIZ 모드: 약 5-8분 (속도 제한 scraping)

### Step 3: 탐지 결과 읽기 및 파싱

스크립트는 두 개의 출력 파일을 생성합니다:
- `theme_detector_YYYY-MM-DD_HHMMSS.json` - 프로그램 처리용 구조화 데이터
- `theme_detector_YYYY-MM-DD_HHMMSS.md` - 사람이 읽기 쉬운 리포트

정량 결과를 이해하려면 JSON 출력을 읽습니다:

```bash
# Find the latest report
ls -lt reports/theme_detector_*.json | head -1

# Read the JSON output
cat reports/theme_detector_YYYY-MM-DD_HHMMSS.json
```

### Step 4: WebSearch로 내러티브 확인 수행

Theme Heat 점수 기준 상위 5개 테마에 대해 WebSearch 질의를 실행하여 내러티브 강도를 확인합니다:

**검색 패턴:**
```
"[theme name] stocks market [current month] [current year]"
"[theme name] sector momentum [current month] [current year]"
```

**내러티브 신호 평가:**
- **Strong narrative**: 주요 매체 다수에서 보도, 애널리스트 상향, 정책 촉매 존재
- **Moderate narrative**: 일부 보도, 혼재된 심리, 뚜렷한 촉매 없음
- **Weak narrative**: 보도량이 적거나, 반대/회의적 톤이 우세

발견 결과에 따라 Confidence 레벨을 업데이트합니다:
- Quantitative High + Narrative Strong = **High** confidence
- Quantitative High + Narrative Weak = **Medium** confidence (모멘텀 다이버전스 가능성)
- Quantitative Low + Narrative Strong = **Medium** confidence (내러티브가 가격을 선행할 수 있음)
- Quantitative Low + Narrative Weak = **Low** confidence

### Step 5: 결과 분석 및 권고 제시

탐지 결과를 지식 베이스와 교차 검증합니다:

**참조 문서:**
1. `references/cross_sector_themes.md` - 테마 정의 및 구성 industry
2. `references/thematic_etf_catalog.md` - 테마별 ETF 노출 옵션
3. `references/theme_detection_methodology.md` - 스코어링 모델 상세
4. `references/finviz_industry_codes.md` - industry 분류 참조

**분석 프레임워크:**

**Hot Bullish Themes** (Heat >= 70, Direction = Bullish)의 경우:
- 라이프사이클 단계 식별(Early = 기회, Late/Exhaustion = 주의)
- 해당 테마 내 상위 성과 industry 나열
- 노출용 proxy ETF 추천
- ETF 확산도 높을 경우 과밀 트레이드 경고 표시

**Hot Bearish Themes** (Heat >= 70, Direction = Bearish)의 경우:
- 압력을 받는 industry 식별
- 약세 모멘텀의 가속/둔화 여부 평가
- 헤징 전략 또는 회피 섹터 제시
- 라이프사이클이 Late/Exhaustion이면 평균회귀 기회 가능성 언급

**Emerging Themes** (Heat 40-69, Lifecycle = Early)의 경우:
- 초기 로테이션 신호일 수 있음
- watchlist 기반 모니터링 권고
- 테마를 가속할 수 있는 촉매 이벤트 식별

**Exhausted Themes** (Heat >= 60, Lifecycle = Exhaustion)의 경우:
- 과밀 트레이드 리스크 경고
- 높은 ETF 수는 과도한 개인투자자 참여를 확인해줌
- 역발상 포지셔닝 또는 익스포저 축소 고려

### Step 6: 최종 리포트 생성

리포트 템플릿 구조를 사용해 사용자에게 최종 리포트를 제시합니다:

```markdown
# Theme Detection Report
**Date:** YYYY-MM-DD
**Mode:** FINVIZ Elite / Public
**Themes Analyzed:** N
**Data Quality:** [note any limitations]

## Theme Dashboard
[Top themes table with Heat, Direction, Lifecycle, Confidence]

## Bullish Themes Detail
[Detailed analysis of bullish themes sorted by Heat]

## Bearish Themes Detail
[Detailed analysis of bearish themes sorted by Heat]

## All Themes Summary
[Complete theme ranking table]

## Industry Rankings
[Top performing and worst performing industries]

## Sector Uptrend Ratios
[Sector-level aggregation if uptrend data available]

## Methodology Notes
[Brief explanation of scoring model]
```

리포트는 `reports/` 디렉터리에 저장합니다.

---

## 리소스

### Scripts 디렉터리 (`scripts/`)

**메인 스크립트:**
- `theme_detector.py` - 메인 오케스트레이션 스크립트
  - industry 데이터 수집, 테마 분류, 스코어링을 조정
  - JSON + Markdown 출력 생성
  - 사용법: `python3 theme_detector.py [options]`

- `theme_classifier.py` - industry를 섹터 간 테마로 매핑
  - `cross_sector_themes.md`에서 테마 정의를 읽음
  - 테마 레벨 집계 점수 계산
  - 구성 industry를 기반으로 방향(강세/약세) 결정

- `finviz_industry_scanner.py` - FINVIZ industry 데이터 수집
  - Elite 모드: industry별 전체 종목 데이터 CSV export
  - Public 모드: 속도 제한이 있는 웹 스크래핑
  - 추출 항목: performance, volume, change%, avg volume, market cap

- `lifecycle_analyzer.py` - 라이프사이클 성숙도 평가
  - 지속 기간 점수, 극단값 군집, 밸류에이션 분석
  - thematic_etf_catalog.md 기반 ETF 확산도 점수
  - 단계 분류: Early / Mid / Late / Exhaustion

- `report_generator.py` - 리포트 출력 생성
  - 템플릿 기반 Markdown 리포트 생성
  - JSON 구조화 출력 생성
  - 테마 대시보드 포맷팅

### References 디렉터리 (`references/`)

**지식 베이스:**
- `cross_sector_themes.md` - industry, ETF, 종목, 매칭 기준을 포함한 테마 정의
- `thematic_etf_catalog.md` - 테마별 ETF 수를 포함한 종합 ETF 카탈로그
- `finviz_industry_codes.md` - FINVIZ industry-to-filter-code 전체 매핑
- `theme_detection_methodology.md` - 3D 스코어링 모델 기술 문서

### Assets 디렉터리 (`assets/`)

- `report_template.md` - 플레이스홀더 포맷이 포함된 리포트 생성용 Markdown 템플릿

---

## 중요 참고사항

### FINVIZ 모드 차이

| Feature | Elite Mode | Public Mode |
|---------|-----------|-------------|
| Industry coverage | All ~145 industries | All ~145 industries |
| Stocks per industry | Full universe | ~20 stocks (page 1) |
| Rate limiting | 0.5s between requests | 2.0s between requests |
| Data freshness | Real-time | 15-min delayed |
| API key required | Yes ($39.99/mo) | No |
| Execution time | ~2-3 minutes | ~5-8 minutes |

### Direction Detection 로직

테마 방향(강세 vs 약세)은 아래를 기반으로 결정됩니다:
1. **가중 industry 성과**: market cap 가중으로 구성 industry의 평균 change% 계산
2. **상승 추세 비율**: 각 industry에서 technical uptrend 상태인 종목 비율(데이터가 있을 때)
3. **거래량 확인**: 거래량이 가격 방향을 지지하는지(accumulation vs. distribution)

테마 분류 기준:
- **Bullish**: Weighted performance > 0 AND (uptrend ratio > 50% OR volume accumulation confirmed)
- **Bearish**: Weighted performance < 0 AND (uptrend ratio < 50% OR volume distribution confirmed)
- **Neutral**: 신호가 혼재되었거나 데이터가 부족한 경우

### 알려진 한계

1. **생존자 편향**: 현재 상장 종목/ETF만 분석
2. **지연**: FINVIZ 데이터는 장중 변동 대비 15분 지연될 수 있음(Public 모드)
3. **테마 경계**: 일부 종목은 여러 테마에 걸치며, 분류는 주 industry 기준
4. **ETF 확산도**: 카탈로그가 정적이라 매우 신규 ETF를 반영하지 못할 수 있음
5. **내러티브 점수**: WebSearch 기반이라 본질적으로 주관성 존재
6. **Public 모드 한계**: 산업당 약 20개 종목만 반영되어 small-cap 신호가 누락될 수 있음

### 면책 조항

**이 분석은 교육 및 정보 제공 목적입니다.**
- 투자 자문이 아닙니다
- 과거 테마 추세는 미래 성과를 보장하지 않습니다
- 테마 탐지는 모멘텀 식별 도구이지, 펀더멘털 가치 평가가 아닙니다
- 투자 결정을 내리기 전에 반드시 본인 조사를 수행하세요

---

**Version:** 1.0
**Last Updated:** 2026-02-16
**API Requirements:** FINVIZ Elite (recommended) or public mode (free); FMP API optional
**Execution Time:** ~2-8 minutes depending on mode
**Output Formats:** JSON + Markdown
**Themes Covered:** 14+ cross-sector themes
