# Claude Trading Skills

이 리포지토리는 주식 투자 및 트레이딩에 유용한 Claude 스킬을 모아놓은 것입니다. 각 스킬에는 프롬프트 설계, 참조 자료, 보조 스크립트가 포함되어 있으며, 체계적인 백테스트, 마켓 분석, 기술적 차트 분석, 경제 캘린더 모니터링, 미국 주식 리서치를 Claude에게 맡길 수 있습니다. Claude 웹앱과 Claude Code 양쪽 환경에서 활용할 수 있습니다.

📖 **문서 사이트:** <https://tradermonty.github.io/claude-trading-skills/>

영문 README는 [`README.md`](README.md)에서 확인할 수 있습니다.

## 리포지토리 구성
- `<skill-name>/` – 각 스킬의 소스 폴더. `SKILL.md`, 참조 자료, 보조 스크립트가 포함됩니다.
- `skill-packages/` – Claude 웹앱의 **Skills** 탭에 바로 업로드할 수 있는 `.skill` 패키지 저장소.

## 시작하기
### Claude 웹앱에서 사용하는 경우
1. 사용하려는 스킬에 해당하는 `.skill` 파일을 `skill-packages/`에서 다운로드합니다.
2. 브라우저에서 Claude를 열고 **Settings → Skills**로 이동하여 ZIP을 업로드합니다(자세한 내용은 Anthropic의 [Skills 출시 게시글](https://www.anthropic.com/news/skills)을 참조).
3. 필요한 대화에서 스킬을 활성화합니다.

### Claude Code(데스크톱/CLI)에서 사용하는 경우
1. 이 리포지토리를 클론하거나 다운로드합니다.
2. 사용하려는 스킬 폴더(예: `backtest-expert`)를 Claude Code의 **Skills** 디렉토리에 복사합니다(Claude Code → **Settings → Skills → Open Skills Folder**. 자세한 내용은 [Claude Code Skills 문서](https://docs.claude.com/en/docs/claude-code/skills)를 참조).
3. Claude Code를 재시작하거나 리로드하면 새로운 스킬이 인식됩니다.

> 팁: 소스 폴더와 ZIP의 내용은 동일합니다. 스킬을 커스터마이징하려면 소스 폴더를 편집하고, 웹앱용으로 배포할 때는 다시 ZIP으로 압축하세요.

## 스킬 목록

### 마켓 분석 및 리서치

- **섹터 애널리스트** (`sector-analyst`)
  - CSV에서 섹터 업트렌드 비율 데이터를 가져오고(API 키 불필요), 마켓 사이클 이론에 기반한 섹터 로테이션 패턴을 분석.
  - 순환주 vs 방어주 리스크 레짐 스코어를 계산하고, 과매수/과매도 섹터를 식별하며, 현재 마켓 사이클 페이즈(Early/Mid/Late Cycle 또는 Recession)를 추정.
  - 차트 이미지를 선택적으로 수신하여 보조적인 업종별 분석을 수행.
  - 섹터 로테이션 전략을 위한 시나리오 기반 확률 평가를 생성.

- **브레드(시장 폭) 차트 애널리스트** (`breadth-chart-analyst`)
  - S&P 500 브레드 인덱스와 미국 주식 상승 추세 종목 비율 차트를 분석하여 시장 건전성과 포지셔닝을 평가.
  - 시장 폭 지표에 기반한 중기적 전략과 단기적 전술적 시장 전망을 제공.
  - 강세장 페이즈(건전한 시장 폭, 시장 폭 축소, 분배)와 약세장 시그널을 식별.
  - 상세한 시장 폭 해석 프레임워크와 역사적 패턴 참조를 포함.

- **테크니컬 애널리스트** (`technical-analyst`)
  - 주식, 지수, 암호화폐, 환율 페어의 주봉 차트를 순수한 기술적 분석으로 평가.
  - 펀더멘탈 편향 없이 추세, 지지/저항 레벨, 차트 패턴, 모멘텀 지표를 식별.
  - 추세 변화의 구체적인 트리거 레벨을 포함한 시나리오 기반 확률 평가를 생성.
  - 엘리어트 파동, 다우 이론, 일본 캔들스틱, 기술적 지표 해석을 참조 자료로 수록.

- **마켓 뉴스 애널리스트** (`market-news-analyst`)
  - WebSearch/WebFetch를 사용한 자동 수집을 통해 지난 10일간의 시장 동향 뉴스 이벤트를 분석.
  - FOMC 결정, 중앙은행 정책, 메가캡 실적, 지정학 이벤트, 원자재 시장 요인에 집중.
  - 정량적 스코어링 프레임워크(가격 임팩트 × 범위 × 미래 중요성)를 사용한 임팩트 순위 리포트를 생성.
  - 신뢰할 수 있는 뉴스 소스 가이드, 이벤트 패턴 분석, 지정학-원자재 상관관계를 참조 자료로 수록.

- **미국 주식 분석** (`us-stock-analysis`)
  - 펀더멘탈, 테크니컬, 동종 업체 비교, 투자 메모 생성을 망라한 포괄적인 미국 주식 리서치 어시스턴트.
  - 재무 지표, 밸류에이션 비율, 성장 궤적, 경쟁력 포지셔닝을 분석.
  - 강세/약세 케이스와 리스크 평가를 포함한 구조화된 투자 메모를 생성.
  - 분석 프레임워크(`fundamental-analysis.md`, `technical-analysis.md`, `financial-metrics.md`, `report-template.md`)를 참조 라이브러리에 수록.

- **마켓 환경 분석** (`market-environment-analysis`)
  - 주식 지수, 환율, 원자재, 금리, 시장 센티먼트를 포함한 글로벌 매크로 브리핑을 가이드.
  - 지표 기반 평가를 포함한 일간/주간 마켓 리뷰용 구조화된 리포트 템플릿을 제공.
  - 인디케이터 해설(`references/indicators.md`)과 분석 패턴을 포함.
  - 리포트 정리와 데이터 시각화를 지원하는 보조 스크립트 `scripts/market_utils.py`를 동봉.

- **마켓 브레드 애널라이저** (`market-breadth-analyzer`)
  - TraderMonty의 공개 CSV 데이터를 사용하여 데이터 기반 6컴포넌트 스코어링 시스템(0-100)으로 시장 폭의 건전성을 정량화.
  - 컴포넌트: 전체 브레드, 섹터 참여, 섹터 로테이션, 모멘텀, 평균 회귀 리스크, 히스토리컬 컨텍스트.
  - 시장이 상승 또는 하락에 얼마나 광범위하게 참여하는지를 측정 (100 = 최대 건전성, 0 = 심각한 취약성).
  - API 키 불필요 - GitHub의 무료 CSV 데이터를 사용.

- **업트렌드 애널라이저** (`uptrend-analyzer`)
  - Monty's Uptrend Ratio Dashboard를 사용하여 약 2,800개의 미국 주식을 11개 섹터에 걸쳐 추적하고 시장 폭의 건전성을 진단.
  - 5컴포넌트 복합 스코어링(0-100): 마켓 브레드, 섹터 참여, 섹터 로테이션, 모멘텀, 히스토리컬 컨텍스트.
  - 경고 오버레이 시스템: Late Cycle과 High Selectivity 플래그가 익스포저 가이던스를 강화하고 주의 액션을 추가.
  - 섹터 레벨 폴백: sector_summary.csv가 없으면 타임시리즈 데이터에서 섹터 서머리를 자동 구성.
  - API 키 불필요 - GitHub의 무료 CSV 데이터를 사용.

- **매크로 레짐 검출기** (`macro-regime-detector`)
  - 크로스 에셋 비율 분석을 통해 구조적인 매크로 레짐 전환(1-2년 호라이즌)을 검출.
  - 6컴포넌트 분석: RSP/SPY 집중도, 일드 커브, 크레딧 환경, 사이즈 팩터, 주식-채권 관계, 섹터 로테이션.
  - 레짐 식별: Concentration, Broadening, Contraction, Inflationary, Transitional.
  - 크로스 에셋 ETF 데이터(RSP, SPY, IWM, HYG, LQD, TLT, XLE, XLU 등)에 FMP API가 필요.

- **기관 투자자 플로우 트래커** (`institutional-flow-tracker`)
  - 13F SEC 제출 서류 데이터를 사용하여 기관 투자자의 보유 변동을 추적하고, "스마트 머니"의 매집/분배 패턴을 식별.
  - 상당한 기관 보유 변동(QoQ 10-15% 이상)을 보이는 종목을 스크리닝하고 다분기 추세를 분석.
  - 티어 기반 품질 프레임워크: 슈퍼인베스터(Berkshire, Baupost)를 3.0-3.5배, 인덱스 펀드를 0.0-0.5배로 가중.
  - 개별 종목 딥 다이브: 분기별 보유 추세, 상위 보유자, 신규/증가/감소/청산 포지션.
  - 집중 리스크 분석과 포지션 변동 카테고리 분류(신규 매수, 증가, 감소, 청산).
  - FMP API 통합. 무료 티어로 분기 포트폴리오 리뷰에 충분(250 calls/일).
  - Warren Buffett(Berkshire), Cathie Wood(ARK), Bill Ackman(Pershing Square) 등 특정 기관 추적 가능.
  - 포괄적 참조 가이드: 13F 제출 서류, 기관 투자자 유형, 시그널 강도 매트릭스를 포함한 해석 프레임워크.

- **테마 검출기** (`theme-detector`)
  - FINVIZ의 업종 및 섹터 퍼포먼스 데이터를 복수 타임프레임에서 분석하여 상승 및 하락 양쪽 트렌드 테마를 검출.
  - 3차원 스코어링: Theme Heat (0-100: 모멘텀/볼륨/업트렌드/브레드), Lifecycle Maturity (0-100: 지속 기간/RSI 극단치/가격 극단치/밸류에이션/ETF 수), Confidence (Low/Medium/High).
  - Direction-aware 분석: 베어 테마도 불 테마와 동등한 감도로 스코어링(반전 지표 사용).
  - 크로스 섹터 테마 검출(AI/반도체, 클린 에너지, 금, 사이버 보안 등)과 섹터 내 수직 집중 검출.
  - 라이프사이클 스테이지: Emerging, Accelerating, Trending, Mature, Exhausting -- 테마별로 대표 종목과 프록시 ETF를 표시.
  - Monty's Uptrend Ratio Dashboard를 보조 브레드 시그널로 통합(3점 평가: ratio + MA10 + slope).
  - 핵심 기능에 API 키 불필요(FINVIZ Public + yfinance). FMP/FINVIZ Elite는 옵션으로 종목 선정을 강화.

### 경제 및 실적 캘린더

- **경제 캘린더 조회** (`economic-calendar-fetcher`)
  - Financial Modeling Prep (FMP) API를 사용하여 향후 7-90일간의 경제 이벤트를 조회.
  - 중앙은행 결정, 고용 통계(NFP), 인플레이션 데이터(CPI/PPI), GDP 발표 및 기타 시장을 움직이는 지표를 수집.
  - 임팩트 평가(High/Medium/Low)와 시장 영향 분석을 포함한 시계열 마크다운 리포트를 생성.
  - 포괄적인 에러 처리를 갖춘 유연한 API 키 관리(환경 변수 또는 사용자 입력)를 지원.

- **실적 캘린더** (`earnings-calendar`)
  - FMP API를 사용하여 시가총액 2B 달러 이상의 중형주 이상 기업에 초점을 맞춘 미국 주식의 향후 실적 발표를 조회.
  - 날짜와 타이밍(장 시작 전, 장 마감 후, 장중)별로 실적을 정리.
  - 주간 실적 리뷰와 포트폴리오 모니터링을 위한 깔끔한 마크다운 테이블 형식을 제공.
  - CLI, 데스크톱, Web 환경을 지원하는 유연한 API 키 관리.

### 전략 및 리스크 관리

- **시나리오 애널라이저** (`scenario-analyzer`)
  - 뉴스 헤드라인을 입력으로 18개월 시나리오를 분석. 1차/2차/3차 영향, 추천 종목, 리뷰를 포함한 포괄적 리포트를 생성.
  - 듀얼 에이전트 구성: scenario-analyst로 주분석, strategy-reviewer로 세컨드 오피니언을 획득.
  - API 키 불필요 - WebSearch로 뉴스 수집.

- **백테스트 엑스퍼트** (`backtest-expert`)
  - 전략 가설 정의, 파라미터 견고성 검증, 워크포워드 검증을 포함한 프로페셔널 등급의 전략 검증 프레임워크.
  - 현실적인 전제 조건을 중시: 슬리피지 모델링, 거래 비용, 생존 편향 제거, 아웃오브샘플 검증.
  - 상세한 방법론(`references/methodology.md`)과 실패 사례집(`references/failed_tests.md`)을 참조 자료로 수록.
  - 아이디어 생성부터 프로덕션 배포까지 품질 게이트가 있는 체계적 접근 방식을 가이드.

- **스탠리 드러켄밀러 투자 어드바이저** (`stanley-druckenmiller-investment`)
  - 매크로 포지셔닝, 유동성 분석, 비대칭적 리스크/리턴 평가를 위한 드러켄밀러의 투자 철학을 인코딩.
  - "높은 확신도일 때 크게 베팅하라" 접근 방식과 엄격한 손절 규율에 집중.
  - 투자 철학 상세, 시장 분석 워크플로우, 역사적 케이스 스터디를 포함한 레퍼런스 팩(일본어/영어).
  - 매크로 테마 식별, 테크니컬 확인, 포지션 사이징 전략을 중시.

- **미국 시장 버블 검출기** (`us-market-bubble-detector`) - **v2.1 업데이트**
  - 필수 정량 지표(Put/Call, VIX, 마진 부채, 브레드, IPO 데이터)를 사용한 개정 민스키/킨들버거 프레임워크에 의한 데이터 기반 버블 리스크 평가.
  - 2단계 평가: 정량적 스코어링(0-12점) → 엄격한 정성적 조정(0-3점, v2.0의 +5에서 축소).
  - 모든 정성적 조정에 대해 측정 가능한 증거 요구 사항을 통한 확인 편향 방지.
  - 세분화된 리스크 페이즈: Normal (0-4) → Caution (5-7) → Elevated Risk (8-9) → Euphoria (10-12) → Critical (13-15).
  - 각 페이즈별 실행 가능한 리스크 버짓과 이익 실현 전략, 구체적인 숏셀링 기준 포함.
  - 역사적 케이스 파일, 퀵 레퍼런스 체크리스트(일영), 엄격한 스코어링 기준의 구현 가이드를 보충.

- **옵션 전략 어드바이저** (`options-strategy-advisor`)
  - Black-Scholes 모델을 사용한 이론적 가격 산출, 전략 분석, 리스크 관리 가이던스를 제공하는 교육적 옵션 트레이딩 도구.
  - 전체 Greeks(Delta, Gamma, Theta, Vega, Rho) 계산과 17개 이상의 옵션 전략(커버드 콜, 스프레드, 아이언 콘도르, 스트래들 등)을 지원.
  - FMP API를 사용한 무료 주가 데이터 + Black-Scholes 가격 산출로 고가의 실시간 옵션 데이터($99-500/월) 없이 전략을 시뮬레이션.
  - P/L 시뮬레이션과 시각화로 전략 간 비교, 실적 시즌 전략 통합 가능.
  - 이론 가격은 시장 중간 가격에 근사; 더 정확한 결과를 위해 브로커에서 실제 IV를 입력 가능.
  - 옵션 메커니즘 학습, Greeks 이해, 라이브 트레이딩 전 전략 플래닝에 최적.

- **포트폴리오 매니저** (`portfolio-manager`)
  - Alpaca MCP Server 연동을 통한 실시간 보유 데이터를 활용한 포괄적 포트폴리오 분석 및 관리.
  - 다차원 분석: 자산 배분, 섹터 분산, 리스크 지표(베타, 변동성, 드로다운), 퍼포먼스 리뷰.
  - 테제 검증과 밸류에이션에 기반한 HOLD/ADD/TRIM/SELL의 포지션 레벨 추천.
  - 목표 모델을 향한 포트폴리오 배분 최적화를 위한 구체적 액션이 포함된 상세한 리밸런싱 계획을 생성.
  - 모델 포트폴리오(Conservative/Moderate/Growth/Aggressive) 벤치마크 비교를 지원.
  - Alpaca 증권 계좌(페이퍼 또는 라이브)와 Alpaca MCP Server 설정이 필요; 수동 데이터 입력도 지원.

- **포지션 사이저** (`position-sizer`)
  - Fixed Fractional, ATR 기반, Kelly Criterion 방식으로 롱 주식 매매의 리스크 기반 포지션 사이즈를 계산.
  - 포트폴리오 제약(최대 포지션 %, 최대 섹터 %)을 적용하고 바인딩 제약을 식별.
  - 2가지 출력 모드: "shares" 모드(진입/스톱 포함)는 최종 추천 주식 수를 반환; "budget" 모드(Kelly만)는 추천 리스크 버짓을 반환.
  - 계산 상세, 제약 분석, 최종 추천이 포함된 JSON + 마크다운 리포트를 생성.
  - API 키 불필요 — 순수 계산, 오프라인 동작.

- **엣지 후보 에이전트** (`edge-candidate-agent`)
  - 일일 마켓 관찰을 재현 가능한 리서치 티켓으로 변환하고, `trade-strategy-pipeline` Phase I 호환 후보 스펙을 내보냄.
  - 구조화된 리서치 티켓에서 `strategy.yaml` + `metadata.json` 아티팩트를 생성. 인터페이스 계약(`edge-finder-candidate/v1`) 검증 포함.
  - 2개의 엔트리 패밀리 지원: `pivot_breakout`(VCP 검출 포함), `gap_up_continuation`(갭 검출 포함).
  - 파이프라인 스키마에 대한 사전 검증과 `uv run` 서브프로세스 폴백을 통한 크로스 환경 호환성 제공.
  - 가드레일: 스키마 바운드(리스크 한도, 이탈 규칙, 비어있지 않은 조건)와 인터페이스 버전 관리를 통한 결정론적 메타데이터를 적용.
  - API 키 불필요 — 로컬 YAML 파일로 동작하며, 로컬 파이프라인 리포지토리에 대해 검증.

- **트레이드 가설 아이디에이터** (`trade-hypothesis-ideator`)
  - 구조화된 전략 컨텍스트, 마켓 컨텍스트, 트레이드 로그, 저널 증거에서 1-5개의 반증 가능한 가설 카드를 생성.
  - 2패스 워크플로우: Pass 1은 `evidence_summary.json`을 구축; Pass 2는 원시 가설을 검증하고, 카드를 랭킹하며, JSON + 마크다운 리포트를 출력.
  - 가드레일: 필드 완전성, 금지 문구 감지, 중복 감지, 제약 위반 체크를 적용.
  - `pursue` 가설을 `edge-finder-candidate/v1` 호환 `strategy.yaml` + `metadata.json`으로 내보냄(`pivot_breakout`, `gap_up_continuation`만).
  - API 키 불필요 — 로컬 JSON/YAML 아티팩트에서 완전히 동작.

- **전략 피벗 디자이너** (`strategy-pivot-designer`)
  - 백테스트 반복 루프의 정체를 감지하고, 파라미터 조정이 국소 최적에 빠졌을 때 구조적으로 다른 전략 피벗 안을 생성.
  - 4개의 결정론적 트리거: 개선 정체, 과적합 프록시, 비용 패배, 테일 리스크 — `evaluate_backtest.py` 출력에서 매핑.
  - 3개의 피벗 기법: 전제 반전, 아키타입 치환, 목적 함수 리프레임. 8개의 정규 전략 아키타입을 커버.
  - Jaccard 거리에 의한 노벨티 스코어링과 결정론적 타이브레이크로 재현 가능한 제안 랭킹을 보장.
  - `strategy_draft` 호환 YAML과 `pivot_metadata` 확장을 출력. 내보내기 가능한 드래프트에는 candidate-agent 티켓 YAML도 동봉.
  - API 키 불필요 — backtest-expert와 edge-strategy-designer의 로컬 JSON/YAML 파일로 동작.

- **엣지 전략 리뷰어** (`edge-strategy-reviewer`)
  - `edge-strategy-designer`가 생성한 전략 드래프트에 대한 결정론적 품질 게이트.
  - 8개 기준(C1-C8) 평가: 엣지 타당성, 과적합 리스크, 샘플 적합성, 레짐 의존성, 이탈 캘리브레이션, 리스크 집중, 실행 현실성, 무효화 품질.
  - 가중 스코어링(0-100)과 PASS/REVISE/REJECT 판정 및 내보내기 적격성 판단.
  - 정밀 임계값 감지로 커브 피팅된 조건에 페널티; 연간 기회 추정으로 지나치게 제한적인 전략을 플래그.
  - REVISE 판정에는 피드백 루프를 위한 구체적 수정 지침 포함.
  - API 키 불필요 — edge-strategy-designer의 로컬 YAML 파일로 동작.

- **엣지 파이프라인 오케스트레이터** (`edge-pipeline-orchestrator`)
  - 엣지 리서치 파이프라인 전체를 엔드투엔드로 오케스트레이션: 자동 감지, 힌트, 콘셉트 합성, 전략 설계, 크리티컬 리뷰, 내보내기.
  - 리뷰-수정 피드백 루프(최대 2회 반복): PASS/REJECT는 반복 간 누적, REVISE 드래프트는 수정 후 재리뷰, 남은 REVISE는 research_probe로 다운그레이드.
  - 내보내기 적격성 게이트: PASS + export_ready_v1 + exportable entry family인 드래프트만 candidate 내보내기로 진행.
  - 모든 업스트림 스킬을 서브프로세스로 호출(크로스 스킬 임포트 없음), 파이프라인 매니페스트로 전체 실행 추적 기록.
  - resume-from-drafts, review-only, dry-run 모드를 지원.
  - API 키 불필요 — 엣지 스킬 전반의 로컬 YAML/JSON 파일을 오케스트레이션.

- **엣지 시그널 애그리게이터** (`edge-signal-aggregator`)
  - edge-candidate-agent, edge-concept-synthesizer, theme-detector, sector-analyst, institutional-flow-tracker, edge-hint-extractor의 출력을 집계.
  - 설정 가능한 가중치, 시그널 중복 제거, 최신성 조정, 모순 처리를 적용하여 랭킹된 확신 대시보드를 생성.
  - 여러 업스트림 스키마 변형(`priority_score`, `support.avg_priority_score`, `themes.all`, `heat/theme_heat` 등)을 지원하여 견고한 크로스 스킬 통합.
  - 출처(`contributing_skills`), 모순 로그, 중복 제거 로그가 포함된 JSON + 마크다운 리포트를 내보냄.
  - API 키 불필요 — 업스트림 엣지 스킬의 로컬 JSON/YAML 출력으로 동작.

### 마켓 타이밍 및 바닥 검출

- **마켓 탑 검출기** (`market-top-detector`)
  - O'Neil의 Distribution Days, Minervini의 Leading Stock Deterioration, Monty의 Defensive Rotation을 사용하여 마켓 탑 확률을 검출.
  - 분배와 천장 형성 패턴을 식별하는 6컴포넌트 전술적 타이밍 시스템.

- **FTD 검출기** (`ftd-detector`)
  - William O'Neil의 방법론을 사용하여 시장 바닥 확인을 위한 Follow-Through Day (FTD) 시그널을 검출.
  - 듀얼 인덱스 추적(S&P 500 + NASDAQ)과 상태 머신에 의한 랠리 시도, FTD 적격, FTD 이후 건전성 모니터링.
  - Market Top Detector의 보완 스킬: Market Top Detector = 디펜시브(분배 검출), FTD Detector = 오펜시브(바닥 확인).
  - 조정 이후 시장 재진입을 위한 익스포저 가이던스 포함 퀄리티 스코어(0-100)를 생성.
  - 인덱스 가격 데이터에 FMP API 키가 필요.

### 실적 모멘텀 스크리닝

- **실적 트레이드 애널라이저** (`earnings-trade-analyzer`)
  - 최근 실적 종목을 5요소 가중 스코어링: 갭 사이즈 (25%), 실적 전 추세 (30%), 거래량 추세 (20%), MA200 포지션 (15%), MA50 포지션 (10%).
  - A/B/C/D 등급 할당(A: 85+, B: 70-84, C: 55-69, D: <55), 복합 스코어 0-100.
  - BMO/AMC 타이밍별 갭 산출 — 실적 발표 타이밍에 따라 다른 기준 가격을 사용.
  - 옵션 엔트리 퀄리티 필터로 낮은 승률 패턴을 제외.
  - API 콜 예산 관리(`--max-api-calls`, 기본값: 200) 및 자동 후보 트리밍.
  - PEAD 스크리너 연계용으로 `schema_version: "1.0"` 포함 JSON 출력.
  - FMP API 키가 필요(무료 티어로 2일 룩백에 충분).

- **PEAD 스크리너** (`pead-screener`)
  - 실적 갭업 종목의 PEAD(Post-Earnings Announcement Drift) 패턴을 주봉 분석으로 스크리닝.
  - 스테이지 기반 모니터링: MONITORING → SIGNAL_READY(레드 캔들 검출) → BREAKOUT(레드 캔들 고가 브레이크) → EXPIRED(5주 초과).
  - 4컴포넌트 스코어링: 셋업 품질 (30%), 브레이크아웃 강도 (25%), 유동성 (25%), 리스크/리워드 (20%).
  - 2개의 입력 모드: 모드A(FMP 실적 캘린더, 단독), 모드B(earnings-trade-analyzer의 JSON 출력, 파이프라인).
  - ISO 주(월요일 시작)에서의 주봉 집계, 실적 주 분할, 부분 주 대응.
  - 유동성 필터: ADV20 >= $25M, 평균 거래량 >= 100만 주, 주가 >= $10.
  - 트레이드 셋업 출력: 진입가, 스톱(레드 캔들 저가), 타겟(2R), 리스크/리워드 비율.
  - FMP API 키가 필요(무료 티어로 14일 룩백에 충분).

### 종목 스크리닝 및 선정

- **VCP 스크리너** (`vcp-screener`)
  - S&P 500 종목에서 Mark Minervini의 Volatility Contraction Pattern (VCP)을 스크리닝.
  - 브레이크아웃 피벗 포인트 부근에서 변동성이 수축하는 Stage 2 상승 추세 종목을 식별.
  - 다단계 필터링: 추세 템플릿 → VCP 베이스 검출 → 수축 분석 → 피벗 포인트 계산.
  - FMP API 키가 필요(무료 티어로 상위 100 후보의 기본 스크리닝에 충분).

- **CANSLIM 주식 스크리너** (`canslim-screener`) - **Phase 2**
  - William O'Neil의 CANSLIM 성장주 방법론을 사용하여 미국 주식을 스크리닝. 멀티배거 후보 발굴에 특화.
  - **Phase 2**에서 7개 컴포넌트 중 6개를 구현(80% 커버리지): C (분기 실적), A (연간 성장), N (신고가), **S (수급)**, **I (기관 투자자)**, M (시장 방향).
  - 복합 스코어링(0-100)과 가중치: C 19%, A 25%, N 19%, **S 19%**, **I 13%**, M 6% (6컴포넌트로 재정규화).
  - **신규**: 볼륨 기반 매집/분배 분석(S 컴포넌트) - 상승일 vs 하락일 거래량 비율로 기관 매수 패턴을 감지.
  - **신규**: 기관 투자자 보유율 추적(I 컴포넌트) - 보유자 수 + 보유율 % 분석, FMP 데이터 불완전 시 **Finviz 자동 폴백**.
  - **Finviz 통합**: 기관 데이터용 무료 웹 스크래핑(beautifulsoup4), I 컴포넌트 정확도를 35/100에서 60-100/100으로 개선.
  - 해석 밴드: Exceptional+ (90-100), Exceptional (80-89), Strong (70-79), Above Average (60-69).
  - 베어마켓 보호: M 컴포넌트가 모든 매수 추천을 게이트(M=0에서 "현금화" 경고).
  - FMP API + Finviz 통합. 무료 티어(250 calls/일)로 40종목 분석 가능(약 1분 40초 실행 시간).
  - 포괄적 지식 베이스: O'Neil의 방법론(S 및 I 포함), 스코어링 공식, 해석 가이드, 포트폴리오 구성 규칙.
  - 향후 Phase 3에서 L (리더십/RS Rank) 컴포넌트를 추가하여 전체 7컴포넌트 완성 예정(100% 커버리지).

- **밸류 배당 스크리너** (`value-dividend-screener`)
  - FMP API를 사용하여 고품질 배당 투자 기회를 스크리닝.
  - 다단계 필터링: 밸류 특성(P/E<=20, P/B<=2) + 수익(수익률 >=3.5%) + 성장성(3년 배당/매출/EPS 상승 추세).
  - 고급 분석: 배당 지속성(배당 성향, FCF 커버리지), 재무 건전성(D/E, 유동성), 퀄리티 스코어(ROE, 마진).
  - 복합 스코어링 시스템으로 밸류, 성장, 퀄리티 요소를 균형있게 반영한 종합 매력도 순위를 매김.
  - 상위 20개 종목을 상세 펀더멘탈 분석 및 포트폴리오 구성 가이던스와 함께 생성.
  - 포괄적인 스크리닝 방법론 문서와 FMP API 사용 가이드를 포함.

- **배당 성장 풀백 스크리너** (`dividend-growth-pullback-screener`)
  - 고품질 배당 성장주(연간 배당 성장 12% 이상, 수익률 1.5% 이상)에서 일시적인 풀백 중인 종목을 검출.
  - 펀더멘탈 배당 분석과 테크니컬 타이밍 지표(RSI<=40 과매도)를 결합.
  - 높은 현재 수익률보다 배당 증가를 통한 복리 부의 축적에 초점을 맞춘 뛰어난 배당 성장률의 종목을 타겟.
  - 2단계 스크리닝 접근: FINVIZ Elite로 빠른 RSI 프리스크리닝 + FMP API로 상세 펀더멘탈 분석.
  - 단기 시장 약세 시 진입 기회를 찾는 장기 배당 성장 투자자에 최적화.
  - 매력적인 기술적 진입 포인트에서의 퀄리티 배당 성장주 랭킹 리스트를 생성.

- **칸치식 배당 SOP** (`kanchi-dividend-sop`)
  - 칸치식 5단계를 미국 주식용 재현 가능한 워크플로우로 변환.
  - 스크리닝, 안전성 정밀 조사, 밸류에이션 판정, 일시적 요인 제외, 풀백 매수 조건을 표준화.
  - 임계값 표, 평가 기준, 1페이지 종목 메모 템플릿을 포함한 운영 기반 스킬.
  - 칸치식 배당 워크플로우 스택의 첫 번째 단계로 설계.

- **칸치식 배당 리뷰 모니터** (`kanchi-dividend-review-monitor`)
  - T1-T5 트리거로 이상 감지를 수행하고, `OK/WARN/REVIEW`로 자동 판정. 자동 매도는 수행하지 않음.
  - 경고와 리뷰 티켓 생성에 집중.
  - 로컬 룰 엔진 스크립트(`build_review_queue.py`)와 트리거 경계값 유닛 테스트를 포함.
  - 후보 선정 이후 지속적 모니터링 레이어로 설계.

- **칸치식 배당 미국 세무/계좌 배치** (`kanchi-dividend-us-tax-accounting`)
  - 인컴 포트폴리오를 위한 미국 배당 세금 분류 및 계좌 배치 워크플로우를 제공.
  - qualified vs ordinary 전제 정리, 보유 기간 체크, 계좌 배치 트레이드오프를 커버.
  - 연간 세무 메모 템플릿과 미확정 전제의 관리를 표준화.
  - 스크리닝 및 모니터링 이후 포트폴리오 구현 레이어로 설계.

- **페어 트레이드 스크리너** (`pair-trade-screener`)
  - 공적분 검정을 사용한 페어 트레이드 기회의 통계적 차익 거래 도구.
  - 동일 섹터 또는 업종 내 주식 페어 간의 장기 균형 관계를 검정.
  - 헤지 비율, 평균 회귀 속도(반감기), z-스코어 기반 진입/이탈 시그널을 산출.
  - 전체 시장 방향과 무관하게 상대적 가격 변동에서 이익을 얻는 마켓 뉴트럴 전략.
  - 섹터 전체 스크리닝과 커스텀 페어 분석을 통계적 엄밀성(ADF 검정, 상관분석)으로 지원.
  - 구조화된 결과와 추가 분석을 위한 JSON 출력이 포함된 FMP API 통합.

- **FinViz 스크리너** (`finviz-screener`)
  - 자연어(일본어/영어)에 의한 스크리닝 지시를 FinViz 필터 코드로 변환하고, Chrome에서 결과를 표시.
  - 펀더멘탈(P/E, 배당, 성장성, 마진), 테크니컬(RSI, SMA, 패턴), 기술적 필터(섹터, 시가총액, 국가) 등 500개 이상의 필터 코드에 대응.
  - `$FINVIZ_API_KEY` 환경 변수에서 FINVIZ Elite를 자동 감지. 미설정 시 퍼블릭 스크리너로 폴백.
  - 고배당 밸류, 소형 성장주, 과매도 대형주, 브레이크아웃 후보, AI/테마 투자 등 14개의 프리셋 레시피를 수록.
  - 기본 사용에 API 키 불필요(퍼블릭 FinViz 스크리너). FINVIZ Elite는 선택 사항으로 확장 기능 이용 가능.

## 워크플로우 예시

### 일일 마켓 모니터링
1. **경제 캘린더 조회**를 사용하여 오늘의 고임팩트 이벤트(FOMC, NFP, CPI 발표)를 확인
2. **실적 캘린더**를 사용하여 오늘 실적 발표하는 주요 기업을 파악
3. **마켓 뉴스 애널리스트**를 사용하여 야간 전개와 시장 영향을 리뷰
4. **브레드 차트 애널리스트**를 사용하여 전체적인 시장 건전성과 포지셔닝을 평가

### 주간 전략 리뷰
1. **섹터 애널리스트**에서 CSV 데이터를 가져와 로테이션 패턴을 식별(선택적으로 차트 제공)
2. **테크니컬 애널리스트**를 주요 지수와 포지션에 사용하여 추세 확인
3. **마켓 환경 분석**을 사용하여 포괄적인 매크로 브리핑을 수행
4. **미국 시장 버블 검출기**를 사용하여 투기적 과열과 리스크 수준을 평가

### 개별 종목 리서치
1. **미국 주식 분석**을 사용하여 포괄적인 펀더멘탈 및 테크니컬 리뷰를 수행
2. **실적 캘린더**를 사용하여 향후 실적 발표일을 확인
3. **마켓 뉴스 애널리스트**를 사용하여 최근 기업별 뉴스와 섹터 전개를 리뷰
4. **백테스트 엑스퍼트**를 사용하여 포지션 사이징 전에 진입/이탈 전략을 검증

### 전략적 포지셔닝
1. **스탠리 드러켄밀러 투자 어드바이저**를 사용하여 매크로 테마를 식별
2. **경제 캘린더 조회**를 사용하여 주요 데이터 릴리스 전후의 진입 타이밍을 설정
3. **브레드 차트 애널리스트**와 **테크니컬 애널리스트**를 사용하여 확인 시그널을 확보
4. **미국 시장 버블 검출기**를 사용하여 리스크 관리와 이익 실현 가이던스를 확보

### 실적 모멘텀 트레이드
1. **실적 트레이드 애널라이저**를 사용하여 최근 실적 리액션(갭 사이즈, 추세, 거래량, MA 포지션)을 스코어링
2. **PEAD 스크리너**(모드B)로 애널라이저 출력을 입력으로 하여, PEAD 셋업(레드 캔들 풀백 → 브레이크아웃 시그널)을 검출
3. **테크니컬 애널리스트**를 사용하여 주봉 차트 패턴과 지지/저항 레벨을 확인
4. PEAD 스크리너의 **유동성** 필터로 포지션 사이징의 실현 가능성을 확인
5. SIGNAL_READY 종목을 모니터링하고, 명확한 스톱로스(레드 캔들 저가)와 2R 타겟으로 브레이크아웃 진입

### 인컴 포트폴리오 구축
1. **밸류 배당 스크리너**를 사용하여 지속 가능한 수익률의 고품질 배당주를 식별
2. **배당 성장 풀백 스크리너**를 사용하여 매력적인 기술적 진입 포인트의 성장 중심 배당주를 검출
3. **미국 주식 분석**을 사용하여 상위 후보에 대한 딥 다이브 펀더멘탈 분석을 수행
4. **실적 캘린더**를 사용하여 포트폴리오 보유 종목의 향후 실적을 추적
5. **마켓 환경 분석**을 사용하여 배당 전략에 대한 매크로 환경을 평가
6. **백테스트 엑스퍼트**를 사용하여 배당 캡처 또는 성장 전략을 검증

### 칸치식 배당 워크플로우(미국 주식)
1. **칸치식 배당 SOP**로 5단계 프로세스를 실행하고 무효화 조건을 포함한 매수 계획을 작성
2. **칸치식 배당 리뷰 모니터**를 일일/주간/분기별 주기로 사용하여 `OK/WARN/REVIEW` 큐를 생성
3. **칸치식 배당 미국 세무/계좌 배치**를 사용하여 보유 종목을 qualified 배당 전제 및 계좌 배치에 맞춤
4. `REVIEW` 판정은 **칸치식 배당 SOP**로 다시 입력하여 포지션 추가 전에 재평가

### 옵션 전략 개발
1. **옵션 전략 어드바이저**를 사용하여 Black-Scholes 가격 산출로 옵션 전략을 시뮬레이션 및 비교
2. **테크니컬 애널리스트**를 사용하여 최적의 진입 타이밍과 지지/저항 레벨을 식별
3. **실적 캘린더**를 사용하여 실적 기반 옵션 전략을 설계
4. **미국 주식 분석**을 사용하여 자본 투입 전 펀더멘탈 테제를 검증
5. Greeks와 P/L 시나리오를 검토하여 최적 전략 선택(커버드 콜, 스프레드, 스트래들 등)

### 포트폴리오 리뷰 및 리밸런싱
1. **포트폴리오 매니저**를 사용하여 Alpaca MCP를 통해 현재 보유 종목을 가져오고 포트폴리오 건전성을 분석
2. 자산 배분, 섹터 분산, 리스크 지표(베타, 변동성, 집중도)를 리뷰
3. 테제 검증에 기반한 포지션별 추천(HOLD/ADD/TRIM/SELL)을 평가
4. **마켓 환경 분석**과 **미국 시장 버블 검출기**를 사용하여 매크로 환경을 평가
5. 배분 최적화를 위한 구체적 매수/매도 액션으로 리밸런싱 계획을 실행

### 통계적 차익 거래 기회
1. **페어 트레이드 스크리너**를 사용하여 섹터 내 공적분된 주식 페어를 식별
2. 평균 회귀 지표(반감기, z-스코어)와 헤지 비율을 분석
3. **테크니컬 애널리스트**를 사용하여 페어 양쪽 레그의 기술적 셋업을 확인
4. z-스코어 임계값에 기반한 진입/이탈 시그널을 모니터링
5. 스프레드 수렴을 추적하고 마켓 뉴트럴 포지션을 관리

### 스킬 품질 및 자동화

- **데이터 퀄리티 체커** (`data-quality-checker`)
  - 마켓 분석 문서와 블로그 기사의 데이터 품질을 발행 전에 검증.
  - 5가지 체크 카테고리: 가격 스케일 불일치(ETF vs 선물 자릿수 힌트), 종목 표기 일관성, 날짜/요일 불일치(영어 + 일본어), 배분 합계 에러(섹션 한정), 단위 불일치.
  - 자문 모드 — 이슈를 경고로 플래그하여 사람이 리뷰, 발견이 있어도 exit 0.
  - 전각 일본어 문자(％, 〜), 범위 표기(50-55%), 명시적 연도가 없는 날짜의 연도 추론을 지원.
  - API 키 불필요 — 로컬 마크다운 파일에서 오프라인 동작.

- **스킬 디자이너** (`skill-designer`)
  - 구조화된 아이디어 사양에서 새로운 스킬을 설계하기 위한 Claude CLI 프롬프트를 생성.
  - 리포지토리 컨벤션(구조 가이드, 품질 체크리스트, SKILL.md 템플릿)을 프롬프트에 임베딩.
  - 기존 스킬 목록을 나열하여 중복 방지. 스킬 자동 생성 파이프라인의 일일 플로우에 사용.
  - API 키 불필요.

- **듀얼 액시스 스킬 리뷰어** (`dual-axis-skill-reviewer`)
  - 듀얼 액시스 방식으로 스킬 품질을 리뷰: 결정론적 오토 스코어링(구조, 워크플로우, 실행 안전성, 아티팩트, 테스트 건전성)과 옵션 LLM 딥 리뷰.
  - 5카테고리 오토 액시스(0-100): 메타데이터 & 유스케이스 (20), 워크플로우 커버리지 (25), 실행 안전성 & 재현성 (25), 지원 아티팩트 (10), 테스트 건전성 (20).
  - `knowledge_only` 스킬(스크립트 없음, 레퍼런스만)을 감지하여 불공정한 페널티를 회피하도록 스코어링 기준을 조정.
  - 옵션 LLM 액시스로 정성적 리뷰(정확성, 리스크, 누락 로직, 유지보수성)를 수행. 가중 블렌드 가능.
  - `--all`로 전체 스킬 일괄 리뷰, `--skip-tests`로 퀵 트리아지, `--project-root`로 타 프로젝트 리뷰에 대응.
  - API 키 불필요.

- **스킬 아이디어 마이너** (`skill-idea-miner`)
  - Claude Code 세션 로그에서 스킬 아이디어 후보를 발굴하고, 참신성/실현가능성/트레이딩 가치로 스코어링하며, 우선순위 백로그를 유지.
  - 주간 스킬 자동 생성 파이프라인에 사용. 수동 실행도 가능.
  - API 키 불필요.

## 스킬 자기 개선 루프

스킬 품질을 지속적으로 리뷰하고 개선하는 자동 파이프라인. 매일 `launchd` 작업이 1개의 스킬을 선택하고, 듀얼 액시스 리뷰어로 스코어링한 뒤, 스코어가 90/100 미만인 경우 `claude -p`로 개선을 적용하고 PR을 생성합니다.

### 작동 원리

1. **라운드 로빈 선택** — 리뷰어 자신을 제외한 모든 스킬을 순번대로 순회. 상태는 `logs/.skill_improvement_state.json`에 영속화.
2. **오토 스코어링** — `run_dual_axis_review.py`를 실행하여 결정론적 스코어(0-100)를 획득.
3. **개선 게이트** — `auto_review.score < 90`인 경우, Claude CLI가 SKILL.md와 레퍼런스를 수정.
4. **품질 게이트** — 개선 후 재스코어링(테스트 활성화). 스코어가 개선되지 않으면 롤백.
5. **PR 생성** — 변경 사항을 피처 브랜치에 커밋하고, 인간 리뷰용으로 GitHub PR을 생성.
6. **일일 서머리** — 결과를 `reports/skill-improvement-log/YYYY-MM-DD_summary.md`에 출력.

### 수동 실행

```bash
# 드라이런: 개선이나 PR 생성 없이 스코어링만
python3 scripts/run_skill_improvement_loop.py --dry-run

# 전체 스킬을 드라이런으로 리뷰
python3 scripts/run_skill_improvement_loop.py --dry-run --all

# 풀 런: 스코어링, 필요 시 개선, PR 생성
python3 scripts/run_skill_improvement_loop.py
```

### launchd 설정 (macOS)

매일 05:00에 macOS `launchd`로 자동 실행:

```bash
# 에이전트 설치
cp launchd/com.trade-analysis.skill-improvement.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.trade-analysis.skill-improvement.plist

# 확인
launchctl list | grep skill-improvement

# 수동 트리거
launchctl start com.trade-analysis.skill-improvement
```

### 주요 파일

| 파일 | 용도 |
|------|------|
| `scripts/run_skill_improvement_loop.py` | 오케스트레이션 스크립트(선택, 스코어링, 개선, PR) |
| `scripts/run_skill_improvement.sh` | launchd용 셸 래퍼 |
| `launchd/com.trade-analysis.skill-improvement.plist` | macOS launchd 에이전트 설정 |
| `skills/dual-axis-skill-reviewer/` | 리뷰어 스킬(스코어링 엔진) |
| `logs/.skill_improvement_state.json` | 라운드 로빈 상태 및 이력 |
| `reports/skill-improvement-log/` | 일일 서머리 리포트 |

## 스킬 자동 생성 파이프라인

세션 로그에서 스킬 아이디어를 발굴(주간)하고, 새로운 스킬을 설계, 리뷰, PR로 생성(일간)하는 자동 파이프라인. 자기 개선 루프와 함께 스킬 카탈로그를 지속적으로 확장합니다.

### 작동 원리

1. **주간 마이닝** — Claude Code 세션 로그를 스캔하여 스킬이 될 수 있는 반복 패턴을 찾고, 각 아이디어의 참신성, 실현가능성, 트레이딩 가치를 스코어링.
2. **백로그 스코어링** — 랭킹된 아이디어는 `logs/.skill_generation_backlog.yaml`에 상태 추적(`pending`, `in_progress`, `completed`, `design_failed`, `review_failed`, `pr_failed`)과 함께 저장.
3. **일일 선택** — 가장 높은 스코어의 `pending` 아이디어를 선택; `design_failed` / `pr_failed`는 1회 재시도(`review_failed`는 터미널).
4. **설계 & 리뷰** — Skill Designer가 완전한 스킬(SKILL.md, 레퍼런스, 스크립트)을 구축한 후, Dual-Axis Reviewer가 스코어링. 스코어가 너무 낮으면 `review_failed`로 마킹.
5. **PR 생성** — 새 스킬을 피처 브랜치에 커밋하고, 인간 리뷰용으로 GitHub PR을 생성.

### 수동 실행

```bash
# 주간: 세션 로그에서 아이디어를 발굴하고 스코어링
python3 scripts/run_skill_generation_pipeline.py --mode weekly --dry-run

# 일간: 백로그에서 가장 높은 스코어의 아이디어로 스킬 설계
python3 scripts/run_skill_generation_pipeline.py --mode daily --dry-run

# 풀 일간 실행(브랜치 생성, 스킬 설계, PR 생성)
python3 scripts/run_skill_generation_pipeline.py --mode daily
```

### launchd 설정 (macOS)

2개의 `launchd` 에이전트가 주간/일간 스케줄을 처리:

```bash
# 양쪽 에이전트 설치
cp launchd/com.trade-analysis.skill-generation-weekly.plist ~/Library/LaunchAgents/
cp launchd/com.trade-analysis.skill-generation-daily.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.trade-analysis.skill-generation-weekly.plist
launchctl load ~/Library/LaunchAgents/com.trade-analysis.skill-generation-daily.plist

# 확인
launchctl list | grep skill-generation

# 수동 트리거
launchctl start com.trade-analysis.skill-generation-weekly
launchctl start com.trade-analysis.skill-generation-daily
```

### 주요 파일

| 파일 | 용도 |
|------|------|
| `scripts/run_skill_generation_pipeline.py` | 오케스트레이션 스크립트(마이닝, 선택, 설계, 리뷰, PR) |
| `scripts/run_skill_generation.sh` | launchd용 셸 래퍼 |
| `launchd/com.trade-analysis.skill-generation-weekly.plist` | 주간 마이닝 스케줄 (토요일 06:00) |
| `launchd/com.trade-analysis.skill-generation-daily.plist` | 일간 생성 스케줄 (07:00) |
| `skills/skill-idea-miner/` | 마이닝 및 스코어링 스킬 |
| `skills/skill-designer/` | 스킬 설계 프롬프트 빌더 |
| `logs/.skill_generation_backlog.yaml` | 상태 추적이 포함된 스코어링된 아이디어 백로그 |
| `logs/.skill_generation_state.json` | 실행 이력 및 상태 |
| `reports/skill-generation-log/` | 일간 생성 서머리 리포트 |

## 커스터마이징 및 기여
- 트리거 설명이나 기능 메모를 조정하려면 각 폴더 내의 `SKILL.md`를 업데이트하세요. ZIP으로 만들 때는 frontmatter `name`이 폴더명과 일치하는지 확인하세요.
- 참조 자료 추가나 새로운 스크립트 추가로 워크플로우를 확장할 수 있습니다.
- 변경 사항을 배포하려면 최신 내용을 반영한 `.skill` 파일을 `skill-packages/`에 재생성하세요.

## API 요구사항

일부 스킬은 데이터 접근을 위해 API 키가 필요합니다:

### API가 필요한 스킬

| 스킬 | FMP API | FINVIZ Elite | Alpaca | 비고 |
|------|---------|--------------|--------|------|
| **경제 캘린더 조회** | ✅ 필수 | ❌ 미사용 | ❌ 미사용 | 경제 이벤트 조회 |
| **실적 캘린더** | ✅ 필수 | ❌ 미사용 | ❌ 미사용 | 실적 발표일 조회 |
| **기관 투자자 플로우 트래커** | ✅ 필수 | ❌ 미사용 | ❌ 미사용 | 13F 제출 서류 분석, 무료 티어 충분 |
| **밸류 배당 스크리너** | ✅ 필수 | 🟡 옵션 | ❌ 미사용 | FINVIZ로 실행 시간 70-80% 단축 |
| **배당 성장 풀백 스크리너** | ✅ 필수 | 🟡 옵션 | ❌ 미사용 | RSI 프리스크리닝용 FINVIZ |
| **칸치식 배당 SOP** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 지식 워크플로우; 다른 스킬 출력 또는 수동 리스트를 사용 |
| **칸치식 배당 리뷰 모니터** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 로컬 룰 엔진; 정규화된 입력 JSON을 소비 |
| **칸치식 배당 미국 세무/계좌** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 분류/계좌 배치용 지식 워크플로우 |
| **페어 트레이드 스크리너** | ✅ 필수 | ❌ 미사용 | ❌ 미사용 | 통계적 차익 거래 분석 |
| **옵션 전략 어드바이저** | 🟡 옵션 | ❌ 미사용 | ❌ 미사용 | 주가 데이터용 FMP; 이론적 가격 산출은 API 없이 동작 |
| **포트폴리오 매니저** | ❌ 미사용 | ❌ 미사용 | ✅ 필수 | Alpaca MCP를 통한 실시간 보유 데이터 |
| **CANSLIM 주식 스크리너** | ✅ 필수 | ❌ 미사용 | ❌ 미사용 | Phase 2 (6컴포넌트); 무료 티어 충분; Finviz 웹 스크래핑으로 기관 데이터 |
| **VCP 스크리너** | ✅ 필수 | ❌ 미사용 | ❌ 미사용 | Stage 2 + VCP 패턴 스크리닝; 무료 티어 충분 |
| **FTD 검출기** | ✅ 필수 | ❌ 미사용 | ❌ 미사용 | 랠리/FTD 검출을 위한 인덱스 가격 데이터 |
| **매크로 레짐 검출기** | ✅ 필수 | ❌ 미사용 | ❌ 미사용 | 크로스 에셋 ETF 비율 분석 |
| **마켓 브레드 애널라이저** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 무료 GitHub CSV 데이터 사용 |
| **업트렌드 애널라이저** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 무료 GitHub CSV 데이터 사용 |
| **섹터 애널리스트** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 무료 GitHub CSV 데이터 사용; 선택적 차트 이미지 |
| **테마 검출기** | 🟡 옵션 | 🟡 옵션 | ❌ 미사용 | 핵심: FINVIZ public + yfinance (무료). FMP는 ETF 보유, FINVIZ Elite는 종목 리스트 |
| **FinViz 스크리너** | ❌ 미사용 | 🟡 옵션 | ❌ 미사용 | 퍼블릭 스크리너 무료; FINVIZ Elite는 `$FINVIZ_API_KEY`에서 자동 감지 |
| **엣지 후보 에이전트** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 로컬 YAML 생성; 로컬 파이프라인 리포에 대해 검증 |
| **트레이드 가설 아이디에이터** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 로컬 JSON 가설 파이프라인 + 선택적 전략 내보내기 |
| **엣지 전략 리뷰어** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 로컬 YAML 드래프트에 대한 결정론적 스코어링 |
| **엣지 파이프라인 오케스트레이터** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 서브프로세스를 통한 로컬 엣지 스킬 오케스트레이션 |
| **엣지 시그널 애그리게이터** | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 로컬 엣지 스킬 JSON/YAML 출력을 가중 랭킹 시그널로 집계 |
| 듀얼 액시스 스킬 리뷰어 | ❌ 미사용 | ❌ 미사용 | ❌ 미사용 | 결정론적 스코어링 + 옵션 LLM 리뷰 |

### API 설정

**Financial Modeling Prep (FMP) API:**
- 무료 티어: 250 요청/일 (대부분의 유스케이스에 충분)
- 가입: https://financialmodelingprep.com/developer/docs
- 환경 변수 설정: `export FMP_API_KEY=your_key_here`
- 또는 프롬프트 시 커맨드라인 인수로 키를 제공

**FINVIZ Elite API:**
- 구독: $39.99/월 또는 $329.99/년
- 가입: https://elite.finviz.com/
- 환경 변수 설정: `export FINVIZ_API_KEY=your_key_here`
- 배당 스크리너의 빠른 프리스크리닝을 제공

**Alpaca Trading API:**
- 무료 페이퍼 트레이딩 계좌 이용 가능
- 가입: https://alpaca.markets/
- Alpaca MCP Server 설정이 필요
- 환경 변수 설정:
  ```bash
  export ALPACA_API_KEY="your_api_key_id"
  export ALPACA_SECRET_KEY="your_secret_key"
  export ALPACA_PAPER="true"  # 또는 라이브 트레이딩의 경우 "false"
  ```

## 참고 링크
- Claude Skills 출시 개요: https://www.anthropic.com/news/skills
- Claude Code Skills 가이드: https://docs.claude.com/en/docs/claude-code/skills
- Financial Modeling Prep API: https://financialmodelingprep.com/developer/docs

질문이나 개선 제안이 있으면 issue를 생성하거나, 각 스킬 폴더에 메모를 남겨주시면 나중에 이용하는 사용자에게도 도움이 됩니다.

## 라이선스

이 리포지토리의 모든 스킬과 참조 자료는 교육 및 연구 목적으로 제공됩니다.
