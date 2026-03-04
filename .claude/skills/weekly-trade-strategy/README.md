# Weekly Trade Strategy Blog Generator

미국주식의 주간 트레이드 전략 블로그를 자동 생성하는 AI 에이전트 시스템

[English](#english) | [한국어](#korean)

---

## <a name="korean"></a>한국어

### 개요

이 프로젝트는 Claude Agents를 활용하여, 미국 주식시장의 주간 트레이드 전략 블로그를 자동 생성하는 시스템입니다. 차트 분석, 시장 환경 평가, 뉴스 분석을 단계적으로 실행하고, 겸업 트레이더를 위한 실전적인 전략 리포트를 생성합니다.

### 주요 기능

- **테크니컬 분석**: VIX, 금리, Breadth 지표, 주요 지수, 원자재의 주봉 차트 분석
- **시장 환경 평가**: 버블 리스크 검출, 센티먼트 분석, 섹터 로테이션 분석
- **뉴스·이벤트 분석**: 과거 10일간의 뉴스 영향 평가, 향후 7일간의 경제 지표·실적 발표 예측
- **주간 전략 블로그 생성**: 3개의 분석 리포트를 통합하여, 실전적인 트레이드 전략을 200-300행의 Markdown 형식으로 출력
- **중장기 전략 리포트** (옵션): Druckenmiller식 18개월 투자 전략을 4시나리오(Base/Bull/Bear/Tail Risk)로 생성

### 사전 요건

- **Claude Code CLI** 또는 **Claude Desktop**
- 아래의 Claude 스킬이 이용 가능할 것:
  - `technical-analyst`
  - `breadth-chart-analyst`
  - `sector-analyst`
  - `market-environment-analysis`
  - `us-market-bubble-detector`
  - `market-news-analyst`
  - `economic-calendar-fetcher`
  - `earnings-calendar`
  - `stanley-druckenmiller-investment` (중장기 전략용)

### 셋업

1. **리포지토리 클론**

```bash
git clone <repository-url>
cd weekly-trade-strategy
```

2. **환경 변수 설정**

`.env` 파일을 생성하고, 필요한 API 키를 설정:

```bash
# Financial Modeling Prep API (실적·경제 캘린더 취득용)
FMP_API_KEY=your_api_key_here
```

3. **폴더 구조 확인**

```
weekly-trade-strategy/
├── charts/              # 차트 이미지 저장 폴더
├── reports/             # 분석 리포트 저장 폴더
├── blogs/               # 최종 블로그 기사 저장 폴더
├── skills/              # Claude 스킬 정의
└── .claude/
    └── agents/          # Claude 에이전트 정의
```

### 사용법

#### 퀵스타트

1. **차트 이미지 준비** (권장 18장)

```bash
# 날짜 폴더 생성
mkdir -p charts/2025-11-03

# 차트 이미지를 배치 (아래 이미지를 권장)
# - VIX (주봉)
# - 미국 10년채 수익률 (주봉)
# - S&P 500 Breadth Index
# - Nasdaq 100, S&P 500, Russell 2000, Dow (주봉)
# - 금, 구리, 원유, 천연가스, 우라늄 (주봉)
# - Uptrend Stock Ratio
# - 섹터·인더스트리 퍼포먼스
# - 실적 발표 캘린더, 히트맵
```

2. **리포트 폴더 생성**

```bash
mkdir -p reports/2025-11-03
```

3. **일괄 실행 프롬프트** (Claude Code/Desktop에서 실행)

```
2025-11-03 주의 트레이드 전략 블로그를 작성해 주세요.

1. technical-market-analyst로 charts/2025-11-03/의 전체 차트를 분석
   → reports/2025-11-03/technical-market-analysis.md

2. us-market-analyst로 시장 환경을 종합 평가
   → reports/2025-11-03/us-market-analysis.md

3. market-news-analyzer로 뉴스/이벤트 분석
   → reports/2025-11-03/market-news-analysis.md

4. weekly-trade-blog-writer로 최종 블로그 기사를 생성
   → blogs/2025-11-03-weekly-strategy.md

각 스텝을 순차 실행하고, 리포트를 확인한 후 다음으로 진행해 주세요.
```

4. **옵션: 중장기 전략 리포트 생성**

주간 블로그와는 별도로, 18개월의 중장기 투자 전략 리포트를 생성할 수 있습니다 (분기별 권장).

```
druckenmiller-strategy-planner 에이전트로 2025년 11월 3일 시점의 18개월 전략을 수립해 주세요.

reports/2025-11-03/ 하위의 3개 리포트를 종합적으로 분석하고,
Druckenmiller식 전략 프레임워크를 적용하여,
reports/2025-11-03/druckenmiller-strategy.md에 저장해 주세요.
```

**특징**:
- 18개월 선행의 중장기 매크로 분석
- 4개의 시나리오(Base/Bull/Bear/Tail Risk)와 확률 평가
- 확신도에 기반한 포지션 사이징 권고
- 매크로 전환점(금융 정책, 경기 사이클)의 식별
- 각 시나리오의 무효화 조건을 명시

#### 스텝별 실행

보다 상세한 절차는 `CLAUDE.md`를 참조해 주세요.

### 프로젝트 구조

```
weekly-trade-strategy/
│
├── charts/                          # 차트 이미지
│   └── YYYY-MM-DD/
│       ├── vix.jpeg
│       ├── 10year_yield.jpeg
│       └── ...
│
├── reports/                         # 분석 리포트
│   └── YYYY-MM-DD/
│       ├── technical-market-analysis.md
│       ├── us-market-analysis.md
│       ├── market-news-analysis.md
│       └── druckenmiller-strategy.md  # (옵션: 중장기 전략)
│
├── blogs/                           # 최종 블로그 기사
│   └── YYYY-MM-DD-weekly-strategy.md
│
├── skills/                          # Claude 스킬 정의
│   ├── technical-analyst/
│   ├── breadth-chart-analyst/
│   ├── sector-analyst/
│   ├── market-news-analyst/
│   ├── us-market-bubble-detector/
│   └── ...
│
├── .claude/
│   └── agents/                      # Claude 에이전트 정의
│       ├── technical-market-analyst.md
│       ├── us-market-analyst.md
│       ├── market-news-analyzer.md
│       ├── weekly-trade-blog-writer.md
│       └── druckenmiller-strategy-planner.md  # (옵션: 중장기 전략)
│
├── CLAUDE.md                        # 상세 실행 절차 가이드
├── README.md                        # 이 파일
├── .env                             # 환경 변수 (생성 필요)
└── .gitignore
```

### 에이전트 목록

| 에이전트 | 역할 | 출력 |
|---------|------|------|
| `technical-market-analyst` | 차트 이미지로부터 테크니컬 분석을 실행 | `technical-market-analysis.md` |
| `us-market-analyst` | 시장 환경과 버블 리스크를 평가 | `us-market-analysis.md` |
| `market-news-analyzer` | 뉴스 영향과 이벤트 예측을 분석 | `market-news-analysis.md` |
| `weekly-trade-blog-writer` | 3개의 리포트를 통합하여 블로그 기사를 생성 | `YYYY-MM-DD-weekly-strategy.md` |
| `druckenmiller-strategy-planner` (옵션) | 중장기(18개월) 전략 플래닝(4시나리오 분석) | `druckenmiller-strategy.md` |

### 트러블슈팅

**Q: 에이전트가 차트를 찾지 못하는 경우**
- `charts/YYYY-MM-DD/` 폴더가 존재하는지 확인
- 이미지 형식이 `.jpeg` 또는 `.png`인지 확인

**Q: 리포트가 생성되지 않는 경우**
- `reports/YYYY-MM-DD/` 폴더가 생성되었는지 확인
- 이전 스텝의 리포트가 정상적으로 생성되었는지 확인

**Q: 블로그 기사의 섹터 배분이 급변하는 경우**
- 전주의 블로그 기사가 `blogs/` 디렉토리에 존재하는지 확인
- 에이전트는 단계적 조정(+-10-15%)을 수행하도록 설계되어 있습니다

**Q: FMP API 에러가 발생하는 경우**
- `.env` 파일에 `FMP_API_KEY`가 올바르게 설정되었는지 확인
- API 키의 유효성을 확인 ([Financial Modeling Prep](https://site.financialmodelingprep.com/))

### 라이선스

이 프로젝트는 MIT 라이선스 하에 공개되어 있습니다.

### 기여

풀 리퀘스트를 환영합니다. 큰 변경의 경우, 먼저 issue를 열어 변경 내용을 논의해 주세요.

---

## <a name="english"></a>English

### Overview

An AI agent system that automatically generates weekly trading strategy blog posts for US stock markets using Claude Agents. The system performs step-by-step chart analysis, market environment evaluation, and news analysis to produce actionable strategy reports for part-time traders.

### Key Features

- **Technical Analysis**: Weekly chart analysis of VIX, yields, breadth indicators, major indices, and commodities
- **Market Environment Assessment**: Bubble risk detection, sentiment analysis, sector rotation analysis
- **News & Event Analysis**: Past 10 days news impact evaluation, upcoming 7 days economic indicators and earnings forecasts
- **Weekly Strategy Blog Generation**: Integrates three analysis reports into a 200-300 line Markdown format trading strategy
- **Medium-Term Strategy Report** (Optional): 18-month Druckenmiller-style investment strategy with 4 scenarios (Base/Bull/Bear/Tail Risk)

### Prerequisites

- **Claude Code CLI** or **Claude Desktop**
- The following Claude skills must be available:
  - `technical-analyst`
  - `breadth-chart-analyst`
  - `sector-analyst`
  - `market-environment-analysis`
  - `us-market-bubble-detector`
  - `market-news-analyst`
  - `economic-calendar-fetcher`
  - `earnings-calendar`
  - `stanley-druckenmiller-investment` (for medium-term strategy)

### Quick Start

1. Clone the repository
2. Create `.env` file with your `FMP_API_KEY`
3. Create date folders: `mkdir -p charts/2025-11-03 reports/2025-11-03`
4. Place chart images in `charts/2025-11-03/`
5. Run the complete workflow via Claude Code/Desktop (see Korean section for detailed prompt)

### Project Structure

See the Korean section above for detailed structure.

### Agents

- **technical-market-analyst**: Chart-based technical analysis
- **us-market-analyst**: Market environment and bubble risk evaluation
- **market-news-analyzer**: News impact and event forecasting
- **weekly-trade-blog-writer**: Final blog post generation
- **druckenmiller-strategy-planner** (Optional): Medium-term (18-month) strategy planning with 4-scenario analysis

### Documentation

For detailed workflow instructions, see `CLAUDE.md`.

### License

This project is licensed under the MIT License.

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## Acknowledgments

This project leverages Claude's advanced AI capabilities for financial market analysis. All trading strategies generated are for educational purposes only and should not be considered as financial advice.

---

**Version**: 1.0
**Last Updated**: 2025-11-02
