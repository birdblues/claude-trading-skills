---
name: portfolio-manager
description: Alpaca MCP Server 통합으로 보유 종목/포지션 데이터를 조회하고 자산 배분, 리스크 지표, 개별 종목 포지션, 분산도 분석 및 리밸런싱 권고를 제공하는 종합 포트폴리오 분석 스킬. 사용자가 브로커리지 계좌 기준 포트폴리오 리뷰, 포지션 분석, 리스크 평가, 성과 평가, 리밸런싱 제안을 요청할 때 사용.
---

# Portfolio Manager

## 개요

Alpaca MCP Server와 연동해 실시간 포트폴리오 데이터를 조회하고, 자산 배분/분산도/리스크 지표/개별 포지션 평가/리밸런싱 권고를 포함한 종합 분석을 수행합니다. 실행 가능한 인사이트가 담긴 상세 포트폴리오 보고서를 생성합니다.

이 스킬은 MCP (Model Context Protocol)를 통해 Alpaca 브로커리지 API를 사용하므로, 수동 입력 데이터가 아닌 실제 최신 포지션 기준으로 분석할 수 있습니다.

## 사용 시점

사용자가 다음과 같이 요청하면 호출합니다:
- "Analyze my portfolio"
- "Review my current positions"
- "What's my asset allocation?"
- "Check my portfolio risk"
- "Should I rebalance my portfolio?"
- "Evaluate my holdings"
- "Portfolio performance review"
- "What stocks should I buy or sell?"
- 포트폴리오 단위 분석/관리 전반 요청

## 사전 준비

### Alpaca MCP Server 설정

이 스킬은 Alpaca MCP Server가 구성/연결되어 있어야 하며, 다음 데이터에 접근합니다:
- 현재 포트폴리오 포지션
- 계정 Equity/Buying Power
- 과거 포지션 및 거래 내역
- 보유 종목 시장 데이터

**사용 MCP Server Tools:**
- `get_account_info` - 계정 equity, buying power, 현금 잔고
- `get_positions` - 현재 포지션(수량, 원가, 시가) 조회
- `get_portfolio_history` - 과거 포트폴리오 성과 데이터
- 시세/펀더멘털용 시장 데이터 도구

Alpaca MCP Server가 연결되어 있지 않으면 사용자에게 알리고 `references/alpaca_mcp_setup.md`의 설정 안내를 제공합니다.

## 워크플로

### Step 1: Alpaca MCP로 포트폴리오 데이터 조회

Alpaca MCP Server 도구로 현재 포트폴리오 정보를 수집합니다.

**1.1 계정 정보 조회:**
```
Use mcp__alpaca__get_account_info to fetch:
- Account equity (total portfolio value)
- Cash balance
- Buying power
- Account status
```

**1.2 현재 포지션 조회:**
```
Use mcp__alpaca__get_positions to fetch all holdings:
- Symbol ticker
- Quantity held
- Average entry price (cost basis)
- Current market price
- Current market value
- Unrealized P&L ($ and %)
- Position size as % of portfolio
```

**1.3 포트폴리오 히스토리 조회 (선택):**
```
Use mcp__alpaca__get_portfolio_history for performance analysis:
- Historical equity values
- Time-weighted return calculation
- Drawdown analysis
```

**데이터 검증:**
- 모든 포지션의 ticker 유효성 확인
- 포지션 시가 합계와 account equity 대략 일치 여부 확인
- 오래되었거나 비활성 포지션 점검
- 예외 케이스 처리(소수점 주식, 옵션, crypto 지원 시)

### Step 2: 포지션 데이터 보강

포트폴리오의 각 포지션에 대해 추가 시세/펀더멘털 데이터를 수집합니다.

**2.1 현재 시장 데이터:**
- 실시간 또는 지연 시세
- 일일 거래량/유동성 지표
- 52주 범위
- 시가총액

**2.2 펀더멘털 데이터:**
WebSearch 또는 사용 가능한 API로 조회:
- 섹터/산업 분류
- 핵심 밸류에이션 지표 (P/E, P/B, 배당수익률)
- 최근 실적 및 재무 건전성 지표
- 애널리스트 평점/목표가
- 최근 뉴스/중요 이벤트

**2.3 기술적 분석:**
- 가격 추세 (20일/50일/200일 이평)
- Relative strength
- 지지/저항
- 모멘텀 지표 (RSI, MACD 가능 시)

### Step 3: 포트폴리오 레벨 분석

레퍼런스 파일 프레임워크를 사용해 종합 분석을 수행합니다.

#### 3.1 자산 배분 분석

**배분 프레임워크는 references/asset-allocation.md 참조**

다중 차원 배분 분석:

**자산군 기준:**
- 주식 vs 채권 vs 현금 vs 대체자산
- 사용자 위험 성향 기준 목표 배분과 비교
- 투자 목표와의 정합성 점검

**섹터 기준:**
- Technology, Healthcare, Financials, Consumer 등
- 섹터 집중 리스크 식별
- 벤치마크 섹터 비중(S&P 500 등)과 비교

**시가총액 기준:**
- Large/Mid/Small-cap 분포
- 메가캡 집중 여부
- 시총 분산 점수

**지역 기준:**
- US / International / Emerging Markets
- 국내 편중 리스크 평가

**출력 형식:**
```markdown
## Asset Allocation

### Current Allocation vs Target
| Asset Class | Current | Target | Variance |
|-------------|---------|--------|----------|
| US Equities | XX.X% | YY.Y% | +/- Z.Z% |
| ... |

### Sector Breakdown
[Pie chart description or table with sector percentages]

### Top 10 Holdings
| Rank | Symbol | % of Portfolio | Sector |
|------|--------|----------------|--------|
| 1 | AAPL | X.X% | Technology |
| ... |
```

#### 3.2 분산 투자 분석

**분산 이론은 references/diversification-principles.md 참조**

포트폴리오 분산 품질 평가:

**포지션 집중도:**
- 상위 보유 종목과 합산 비중 파악
- 단일 포지션 10-15% 초과 시 경고
- HHI(Herfindahl-Hirschman Index) 계산

**섹터 집중도:**
- 지배적 섹터 식별
- 단일 섹터 30-40% 초과 시 경고
- 벤치마크 대비 섹터 분산 비교

**상관관계 분석:**
- 주요 포지션 간 상관 추정
- 고상관 포지션(중복 노출) 식별
- 실질 분산 효과 평가

**포지션 개수:**
- 개인 포트폴리오 적정 범위: 15-30종목
- 과소 분산(<10) / 과다 분산(>50) 표시

**출력:**
```markdown
## Diversification Assessment

**Concentration Risk:** [Low / Medium / High]
- Top 5 holdings represent XX% of portfolio
- Largest single position: [SYMBOL] at XX%

**Sector Diversification:** [Excellent / Good / Fair / Poor]
- Dominant sector: [Sector Name] at XX%
- [Assessment of balance across sectors]

**Position Count:** [Optimal / Under-diversified / Over-diversified]
- Total positions: XX stocks
- [Recommendation]

**Correlation Concerns:**
- [List any highly correlated position pairs]
- [Diversification improvement suggestions]
```

#### 3.3 리스크 분석

**리스크 측정 프레임워크는 references/portfolio-risk-metrics.md 참조**

핵심 리스크 지표 계산 및 해석:

**변동성 지표:**
- 추정 포트폴리오 beta (가중 평균)
- 개별 포지션 변동성
- 포트폴리오 표준편차(히스토리 데이터 가능 시)

**하방 리스크:**
- 최대 낙폭 (portfolio history)
- 고점 대비 현재 낙폭
- 미실현 손실이 큰 포지션

**리스크 집중:**
- 고변동성 종목(beta > 1.5) 비중
- 투기적/비수익 기업 비중
- 레버리지 사용(해당 시)

**꼬리 리스크:**
- 블랙스완 이벤트 노출
- 단일 종목 집중 리스크
- 섹터 특화 이벤트 리스크

**출력:**
```markdown
## Risk Assessment

**Overall Risk Profile:** [Conservative / Moderate / Aggressive]

**Portfolio Beta:** X.XX (vs market at 1.00)
- Interpretation: Portfolio is [more/less] volatile than market

**Maximum Drawdown:** -XX.X% (from $XXX,XXX to $XXX,XXX)
- Current drawdown from peak: -XX.X%

**High-Risk Positions:**
| Symbol | % of Portfolio | Beta | Risk Factor |
|--------|----------------|------|-------------|
| [TICKER] | XX% | X.XX | [High volatility / Recent loss / etc] |

**Risk Concentrations:**
- XX% in single sector ([Sector])
- XX% in stocks with beta > 1.5
- [Other concentration risks]

**Risk Score:** XX/100 ([Low/Medium/High] risk)
```

#### 3.4 성과 분석

사용 가능한 데이터로 포트폴리오 성과를 평가합니다.

**절대 수익:**
- 포트폴리오 총 미실현 P&L ($ / %)
- 수익률 상위 포지션 Top 5
- 손실률 상위 포지션 Bottom 5

**Time-Weighted Returns (히스토리 가능 시):**
- YTD 수익률
- 1년/3년/5년 연환산 수익률
- 벤치마크(S&P 500 등) 비교

**포지션 단위 성과:**
- Winners vs Losers 비율
- 수익 포지션 평균 수익률
- 손실 포지션 평균 손실률
- 52주 고점/저점 인접 포지션

**출력:**
```markdown
## Performance Review

**Total Portfolio Value:** $XXX,XXX
**Total Unrealized P&L:** $XX,XXX (+XX.X%)
**Cash Balance:** $XX,XXX (XX% of portfolio)

**Best Performers:**
| Symbol | Gain | Position Value |
|--------|------|----------------|
| [TICKER] | +XX.X% | $XX,XXX |
| ... |

**Worst Performers:**
| Symbol | Loss | Position Value |
|--------|------|----------------|
| [TICKER] | -XX.X% | $XX,XXX |
| ... |

**Performance vs Benchmark (if available):**
- Portfolio return: +X.X%
- S&P 500 return: +Y.Y%
- Alpha: +/- Z.Z%
```

### Step 4: 개별 포지션 분석

상위 10-15개 핵심 포지션(포트폴리오 비중 기준)을 상세 분석합니다.

**포지션 분석 프레임워크는 references/position-evaluation.md 참조**

각 중요 포지션에 대해:

**4.1 Thesis Validation:**
- 이 포지션을 왜 진입했는가? (사용자 컨텍스트가 있는 경우)
- 투자 가설이 유효한가/훼손되었는가
- 최근 기업 이벤트/뉴스

**4.2 Valuation Assessment:**
- 현재 밸류에이션 지표 (P/E, P/B 등)
- 과거 밸류 범위 대비 비교
- 섹터 피어 대비 비교
- Overvalued / Fair / Undervalued 판단

**4.3 Technical Health:**
- 가격 추세 (uptrend/downtrend/sideways)
- 이평선 대비 위치
- 지지/저항 레벨
- 모멘텀 상태

**4.4 Position Sizing:**
- 현재 포트폴리오 비중
- 확신도/리스크 대비 적정 크기 여부
- 최적 비중 대비 과대/과소

**4.5 액션 권고:**
- **HOLD** - 비중 적정 + thesis 유지
- **ADD** - 기회 대비 과소비중 + thesis 강화
- **TRIM** - 과대비중 또는 밸류 부담
- **SELL** - thesis 훼손, 더 나은 대안 존재

**포지션별 출력:**
```markdown
### [SYMBOL] - [Company Name] (XX.X% of portfolio)

**Position Details:**
- Shares: XXX
- Avg Cost: $XX.XX
- Current Price: $XX.XX
- Market Value: $XX,XXX
- Unrealized P/L: $X,XXX (+XX.X%)

**Fundamental Snapshot:**
- Sector: [Sector]
- Market Cap: $XX.XB
- P/E: XX.X | Dividend Yield: X.X%
- Recent developments: [Key news or earnings]

**Technical Status:**
- Trend: [Uptrend / Downtrend / Sideways]
- Price vs 50-day MA: [Above/Below by XX%]
- Support: $XX.XX | Resistance: $XX.XX

**Position Assessment:**
- **Thesis Status:** [Intact / Weakening / Broken / Strengthening]
- **Valuation:** [Undervalued / Fair / Overvalued]
- **Position Sizing:** [Optimal / Overweight / Underweight]

**Recommendation:** [HOLD / ADD / TRIM / SELL]
**Rationale:** [1-2 sentence explanation]
```

### Step 5: 리밸런싱 권고

**리밸런싱 접근은 references/rebalancing-strategies.md 참조**

구체적인 리밸런싱 권고를 생성합니다.

**5.1 리밸런싱 트리거 식별:**
- 목표 비중 대비 크게 이탈한 포지션
- 조정이 필요한 섹터/자산군 배분
- 축소 대상 과대 비중 포지션
- 확대 대상 과소 비중 영역
- 세금 이슈(자본이득세 영향)

**5.2 리밸런싱 계획 수립:**

**TRIM 대상:**
- 목표 대비 과대 비중 포지션
- 과도한 상승으로 밸류 부담이 커진 종목
- 포트폴리오 15-20%를 초과한 집중 포지션
- thesis 훼손 포지션

**ADD 대상:**
- 과소 비중 섹터/자산군
- 확신도 높지만 현재 비중이 낮은 포지션
- 분산도 개선에 기여하는 신규 기회

**현금 배치:**
- 과도한 현금(>10%) 시 배치 제안
- 기회와 배분 갭 기준 우선순위 제시

**5.3 우선순위:**
1. **Immediate** - 리스크 축소(집중 포지션 trim)
2. **High Priority** - 큰 배분 이탈(목표 대비 >10%)
3. **Medium Priority** - 중간 배분 이탈(5-10%)
4. **Low Priority** - 미세 조정/기회 대응

**출력:**
```markdown
## Rebalancing Recommendations

### Summary
- **Rebalancing Needed:** [Yes / No / Optional]
- **Primary Reason:** [Concentration risk / Sector drift / Cash deployment / etc]
- **Estimated Trades:** X sell orders, Y buy orders

### Recommended Actions

#### HIGH PRIORITY: Risk Reduction
**TRIM [SYMBOL]** from XX% to YY% of portfolio
- **Shares to Sell:** XX shares (~$XX,XXX)
- **Rationale:** [Overweight / Valuation extended / etc]
- **Tax Impact:** $X,XXX capital gain (est)

#### MEDIUM PRIORITY: Asset Allocation
**ADD [Sector/Asset Class]** exposure
- **Target:** Increase from XX% to YY%
- **Suggested Stocks:** [SYMBOL1, SYMBOL2, SYMBOL3]
- **Amount to Invest:** ~$XX,XXX

#### CASH DEPLOYMENT
**Current Cash:** $XX,XXX (XX% of portfolio)
- **Recommendation:** [Deploy / Keep for opportunities / Reduce to X%]
- **Suggested Allocation:** [Distribution across sectors/stocks]

### Implementation Plan
1. [First action - highest priority]
2. [Second action]
3. [Third action]
...

**Timing Considerations:**
- [Tax year-end planning / Earnings season / Market conditions]
- [Suggested phasing if applicable]
```

### Step 6: 포트폴리오 보고서 생성

저장소 루트에 종합 Markdown 보고서를 생성합니다.

**Filename:** `portfolio_analysis_YYYY-MM-DD.md`

**Report Structure:**

```markdown
# Portfolio Analysis Report

**Account:** [Account type if available]
**Report Date:** YYYY-MM-DD
**Portfolio Value:** $XXX,XXX
**Total P&L:** $XX,XXX (+XX.X%)

---

## Executive Summary

[3-5 bullet points summarizing key findings]
- Overall portfolio health assessment
- Major strengths
- Key risks or concerns
- Primary recommendations

---

## Holdings Overview

[Summary table of all positions]

---

## Asset Allocation
[Section from Step 3.1]

---

## Diversification Analysis
[Section from Step 3.2]

---

## Risk Assessment
[Section from Step 3.3]

---

## Performance Review
[Section from Step 3.4]

---

## Position Analysis
[Detailed analysis of top 10-15 positions from Step 4]

---

## Rebalancing Recommendations
[Section from Step 5]

---

## Action Items

**Immediate Actions:**
- [ ] [Action 1]
- [ ] [Action 2]

**Medium-Term Actions:**
- [ ] [Action 3]
- [ ] [Action 4]

**Monitoring Priorities:**
- [ ] [Watch list item 1]
- [ ] [Watch list item 2]

---

## Appendix: Full Holdings

[Complete table with all positions and metrics]
```

### Step 7: 인터랙티브 후속 대응

다음과 같은 후속 질문에 답할 수 있어야 합니다.

**자주 나오는 질문:**

**"Why should I sell [SYMBOL]?"**
- 구체적 우려(밸류, thesis 훼손, 집중도) 설명
- 근거 데이터 제시
- 필요 시 대체 포지션 제안

**"What should I buy instead?"**
- 배분 개선에 유효한 구체 종목 제시
- 포트폴리오 공백을 어떻게 메우는지 설명
- 간단한 투자 논리 제시

**"What's my biggest risk?"**
- 핵심 리스크 요인(집중/섹터 노출/변동성) 특정
- 리스크 정량화
- 완화 전략 제시

**"How does my portfolio compare to [benchmark]?"**
- 배분, 섹터 비중, 리스크 지표 비교
- 핵심 차이점 설명
- 해당 차이가 정당한지 평가

**"Should I rebalance now or wait?"**
- 시장 환경, 세금, 거래비용 고려
- 근거와 함께 타이밍 제안

**"Can you analyze [specific position] in more detail?"**
- 필요 시 us-stock-analysis 스킬로 심층 분석
- 결과를 포트폴리오 맥락에 재통합

## 분석 프레임워크

### 목표 배분 템플릿

위험 성향별 레퍼런스 배분 모델을 포함합니다.

**상세 모델은 references/target-allocations.md 참조:**

- **Conservative** (원금 보전/인컴 중심)
- **Moderate** (성장+인컴 균형)
- **Growth** (장기 자본 성장)
- **Aggressive** (최대 성장, 고위험 허용)

각 모델에는 다음이 포함됩니다:
- 자산군 목표(Stocks/Bonds/Cash/Alternatives)
- 섹터 가이드라인
- 시가총액 분포
- 지역 배분
- 포지션 크기 규칙

사용자가 명시 전략이 없으면 비교 기준 벤치마크로 사용합니다.

### 위험 성향 평가

사용자의 목표 배분이 불명확할 때 다음을 바탕으로 적정 위험 성향을 추정합니다:
- 나이(언급된 경우)
- 투자 기간(언급된 경우)
- 현재 배분(선호 반영)
- 보유 종목 성격(보수 vs 투기)

**평가 프레임워크는 references/risk-profile-questionnaire.md 참조**

## 출력 가이드라인

**톤/스타일:**
- 객관적이고 분석적
- 근거가 명확한 실행형 권고
- 시장 예측 불확실성 인정
- 낙관과 리스크 인식의 균형
- 가능한 한 수치화

**데이터 제시:**
- 비교/지표는 표 사용
- 배분/수익률은 퍼센트
- 절대값은 달러 금액
- 보고서 전체 포맷 일관성 유지

**권고 명확성:**
- 동사 중심 액션(TRIM, ADD, HOLD, SELL)
- 구체 수량(XX주 매도, $X,XXX 매수)
- 우선순위(Immediate, High, Medium, Low)
- 각 권고의 근거 명시

**시각 설명:**
- 배분은 파이차트처럼 설명
- 섹터 비중은 바차트 형태로 설명
- 성과 추세는 방향 기호(↑ ↓ →) 활용

## Reference Files

분석 중 필요 시 다음 참고 문서를 로드합니다.

**references/alpaca-mcp-setup.md**
- When: 사용자에게 Alpaca MCP Server 설정 안내가 필요할 때
- Contains: 설치 절차, API 키 구성, MCP 연결 단계, 트러블슈팅

**references/asset-allocation.md**
- When: 배분 분석 또는 리밸런싱 계획 수립 시
- Contains: 자산배분 이론, 위험 성향별 배분, 섹터 가이드, 리밸런싱 트리거

**references/diversification-principles.md**
- When: 분산 품질 평가 시
- Contains: MPT 기초, 상관관계, 적정 종목 수, 집중 리스크 임계값, 분산 지표

**references/portfolio-risk-metrics.md**
- When: 리스크 점수 계산/변동성 해석 시
- Contains: Beta, 표준편차, Sharpe, 최대낙폭, VaR, 위험조정수익

**references/position-evaluation.md**
- When: 개별 포지션 매수/보유/매도 의사결정 시
- Contains: 분석 프레임워크, thesis 검증 체크리스트, 비중 가이드, 매도 규율

**references/rebalancing-strategies.md**
- When: 리밸런싱 권고 수립 시
- Contains: 캘린더/임계값/전술 리밸런싱, 세금 최적화, 거래비용, 실행 타이밍

**references/target-allocations.md**
- When: 비교용 목표 배분 필요 시
- Contains: 보수/중립/성장/공격 모델 포트폴리오, 섹터 범위, 시총 분포

**references/risk-profile-questionnaire.md**
- When: 위험 성향 또는 목표 배분 미제시 시
- Contains: 위험 성향 질문, 점수화 방법, 프로파일 분류

## 오류 처리

**Alpaca MCP Server 미연결 시:**
1. Alpaca 통합이 필요함을 안내
2. references/alpaca-mcp-setup.md 기반 설정 방법 제공
3. 대안 제시: 수동 CSV 입력(권장도 낮음)

**API 데이터가 불완전할 때:**
- 사용 가능한 데이터로 분석 진행
- 보고서에 한계 명시
- 누락 포지션 수동 검증 권고

**포지션 데이터가 stale로 보일 때:**
- 문제를 명시
- 연결 갱신/Alpaca 상태 확인 권고
- 단서(caveat)를 달고 분석 진행

**포지션이 없는 계정일 때:**
- 빈 포트폴리오 상태를 명확히 안내
- 분석 대신 포트폴리오 구성 가이드 제공
- value-dividend-screener 또는 us-stock-analysis 활용 제안

## 고급 기능

### Tax-Loss Harvesting 기회

미실현 손실 포지션 중 tax-loss harvesting 후보 식별:
- 손실 >5% 포지션
- 보유기간 고려(워시세일 회피)
- 유사하지만 실질동일하지 않은 대체 종목 제안

### 배당 인컴 분석

배당 포트폴리오의 경우:
- 연간 배당 수입 추정
- 배당 성장 경로
- 배당 커버리지/지속가능성
- 장기 보유의 yield on cost

### 상관관계 매트릭스

5-20개 포지션 포트폴리오에 대해:
- 주요 포지션 간 상관 추정
- 중복 포지션(상관 >0.8) 식별
- 분산 개선 제안

### 시나리오 분석

다양한 시나리오에서 포트폴리오 반응 모델링:
- **Bull Market** (+20% equity appreciation)
- **Bear Market** (-20% equity decline)
- **Sector Rotation** (Tech weakness, Value strength)
- **Rising Rates** (성장주/채권 영향)

## Example Queries

**Basic Portfolio Review:**
- "Analyze my portfolio"
- "Review my positions"
- "How's my portfolio doing?"

**Allocation Analysis:**
- "What's my asset allocation?"
- "Am I too concentrated in tech?"
- "Show me my sector breakdown"

**Risk Assessment:**
- "Is my portfolio too risky?"
- "What's my portfolio beta?"
- "What are my biggest risks?"

**Rebalancing:**
- "Should I rebalance?"
- "What should I buy or sell?"
- "How can I improve diversification?"

**Performance:**
- "What are my best and worst positions?"
- "How am I performing vs the market?"
- "Which stocks are winning and losing?"

**Position-Specific:**
- "Should I sell [SYMBOL]?"
- "Is [SYMBOL] overweight in my portfolio?"
- "What should I do with [SYMBOL]?"

## 제한 사항 및 고지

**모든 보고서에 포함:**

*This analysis is for informational purposes only and does not constitute financial advice. Investment decisions should be made based on individual circumstances, risk tolerance, and financial goals. Past performance does not guarantee future results. Consult with a qualified financial advisor before making investment decisions.*

*Data accuracy depends on Alpaca API and third-party market data sources. Verify critical information independently. Tax implications are estimates only; consult a tax professional for specific guidance.*
