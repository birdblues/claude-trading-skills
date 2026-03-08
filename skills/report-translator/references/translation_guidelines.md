# Translation Guidelines for Financial Reports

## General Principles

1. **데이터 무결성 우선**: 숫자, 가격, 티커, 기술 지표 데이터는 절대 변경하지 않는다
2. **자연스러운 한국어**: 직역보다 의역을 선호하되, 금융 전문 용어의 정확성을 유지한다
3. **구조 보존**: Markdown 헤더, 테이블, 서식을 원본과 동일하게 유지한다
4. **일관성**: 동일 용어는 문서 전체에서 같은 번역을 사용한다

## Do Not Translate (원본 유지 항목)

| 카테고리 | 예시 |
|---------|------|
| 종목 티커 | AAPL, MSFT, NVDA, SPY, QQQ |
| ETF/지수 이름 | S&P 500, NASDAQ, Russell 2000 |
| 숫자/가격 | $155.00, 3.2%, 1,234,567 |
| 날짜 형식 | 2026-03-08, March 8, 2026 |
| 기술 지표명 | RSI, MACD, EMA, SMA, VWAP, ATR, ADX |
| 패턴명 | VCP, Cup-and-Handle, Head-and-Shoulders |
| 등급/점수 | Grade A+, Score 85/100, PASS/FAIL |
| 시간대 | BMO, AMC, ET, UTC |
| API/기술 용어 | FMP API, JSON, Python, pip |
| URL | https://... |
| 코드 블록 내용 | ```bash ... ``` |

## Section Header Translations (섹션 헤더 번역)

| English | 한국어 |
|---------|--------|
| Executive Summary | 요약 |
| Overview | 개요 |
| Methodology | 방법론 |
| Key Findings | 주요 발견 |
| Analysis | 분석 |
| Results | 결과 |
| Conclusion | 결론 |
| Recommendations | 추천사항 |
| Action Items | 실행 항목 |
| Risk Assessment | 리스크 평가 |
| Disclaimer | 면책 조항 |
| Data Notes | 데이터 참고사항 |
| Additional Resources | 추가 자료 |
| Key Observations | 주요 관찰 |
| Trading Considerations | 트레이딩 고려사항 |
| Output Format | 출력 형식 |
| Timing Reference | 시간 참조 |
| Actionable Guidance | 실행 가이드 |
| Watchlist | 관심종목 |
| Signal Summary | 시그널 요약 |
| Market Context | 시장 맥락 |
| Sector Analysis | 섹터 분석 |
| Technical Setup | 기술적 셋업 |
| Entry/Exit Criteria | 진입/청산 기준 |
| Position Sizing | 포지션 사이징 |
| Stop Loss | 손절 |
| Profit Target | 목표가 |
| Risk/Reward | 리스크/보상 |
| Composite Score | 종합 점수 |
| Current Readings | 현재 수치 |
| Signal Status | 신호 상태 |
| Scenario Analysis | 시나리오 분석 |
| Base Case | 기본 시나리오 |
| Bull Case | 강세 시나리오 |
| Bear Case | 약세 시나리오 |

## Financial Term Dictionary (금융 용어 사전)

### Market & Trading (시장/트레이딩)

| English | 한국어 |
|---------|--------|
| bull market | 강세장 |
| bear market | 약세장 |
| sideways / range-bound | 횡보장 / 박스권 |
| breakout | 돌파 |
| pullback | 조정 / 되돌림 |
| rally | 랠리 / 반등 |
| correction | 조정 |
| consolidation | 횡보 / 조정 구간 |
| reversal | 반전 |
| momentum | 모멘텀 |
| volatility | 변동성 |
| volume | 거래량 |
| liquidity | 유동성 |
| market breadth | 시장 폭 |
| distribution day | 매도 압력일 |
| follow-through day | 추세 확인일 (FTD) |
| uptrend | 상승 추세 |
| downtrend | 하락 추세 |
| resistance | 저항선 |
| support | 지지선 |
| all-time high (ATH) | 사상 최고가 |
| 52-week high/low | 52주 최고/최저 |
| market cap | 시가총액 |
| large cap | 대형주 |
| mid cap | 중형주 |
| small cap | 소형주 |
| sector rotation | 섹터 로테이션 |

### Earnings & Fundamentals (실적/펀더멘털)

| English | 한국어 |
|---------|--------|
| earnings | 실적 / 어닝 |
| revenue | 매출 |
| EPS (earnings per share) | 주당순이익 (EPS) |
| earnings surprise | 어닝 서프라이즈 |
| earnings beat/miss | 실적 상회/하회 |
| guidance | 가이던스 |
| year-over-year (YoY) | 전년 대비 (YoY) |
| quarter-over-quarter (QoQ) | 전분기 대비 (QoQ) |
| forward P/E | 선행 PER |
| trailing P/E | 후행 PER |
| dividend yield | 배당 수익률 |
| payout ratio | 배당 성향 |
| free cash flow | 잉여현금흐름 |
| operating margin | 영업이익률 |
| net margin | 순이익률 |
| debt-to-equity | 부채비율 |

### Options (옵션)

| English | 한국어 |
|---------|--------|
| call option | 콜 옵션 |
| put option | 풋 옵션 |
| strike price | 행사가 |
| expiration date | 만기일 |
| implied volatility (IV) | 내재 변동성 (IV) |
| premium | 프리미엄 |
| open interest | 미결제약정 |
| covered call | 커버드 콜 |
| protective put | 보호적 풋 |
| iron condor | 아이언 콘도르 |
| straddle | 스트래들 |
| strangle | 스트랭글 |

### Macro & Economy (거시경제)

| English | 한국어 |
|---------|--------|
| interest rate | 금리 |
| Fed funds rate | 기준금리 |
| yield curve | 수익률 곡선 |
| inflation | 인플레이션 |
| CPI (Consumer Price Index) | 소비자물가지수 (CPI) |
| GDP (Gross Domestic Product) | 국내총생산 (GDP) |
| unemployment rate | 실업률 |
| quantitative easing (QE) | 양적완화 (QE) |
| quantitative tightening (QT) | 양적긴축 (QT) |
| credit spread | 신용 스프레드 |
| risk-on / risk-off | 위험선호 / 위험회피 |
| safe haven | 안전자산 |
| stagflation | 스태그플레이션 |
| soft landing | 연착륙 |
| hard landing | 경착륙 |

### Risk & Portfolio (리스크/포트폴리오)

| English | 한국어 |
|---------|--------|
| risk management | 리스크 관리 |
| position sizing | 포지션 사이징 |
| stop-loss | 손절 / 스탑로스 |
| take-profit | 익절 / 목표가 |
| risk/reward ratio | 리스크/보상 비율 |
| drawdown | 최대 낙폭 / 드로다운 |
| Sharpe ratio | 샤프 비율 |
| allocation | 배분 / 비중 |
| rebalancing | 리밸런싱 |
| diversification | 분산투자 |
| hedge | 헤지 |
| exposure | 익스포저 / 노출도 |
| Kelly criterion | 켈리 기준 |

### Analysis Types (분석 유형)

| English | 한국어 |
|---------|--------|
| technical analysis | 기술적 분석 |
| fundamental analysis | 기본적 분석 / 펀더멘털 분석 |
| quantitative analysis | 정량 분석 |
| sentiment analysis | 심리 분석 |
| intermarket analysis | 인터마켓 분석 |
| top-down analysis | 탑다운 분석 |
| bottom-up analysis | 바텀업 분석 |
| backtesting | 백테스트 |
| forward testing | 포워드 테스트 |
| screening | 스크리닝 |

## Formatting Rules (서식 규칙)

1. **테이블**: 컬럼 헤더는 기존 `.ko.md` 템플릿 패턴을 따름. 데이터 셀은 원본 유지.
2. **볼드/이탤릭**: 원본과 동일하게 유지. 번역된 텍스트에도 동일한 서식 적용.
3. **리스트**: 불릿 포인트 구조 유지. 내용만 번역.
4. **코드 블록**: 내용을 번역하지 않음. 코드 블록 바로 위/아래 설명만 번역.
5. **주석/면책**: 이탤릭 면책 조항은 한국어로 번역하되, API 출처 정보는 원본 유지.
6. **숫자 범위 표기**: 숫자 범위에 bare `~`(물결표) 사용 금지. Markdown `~~strikethrough~~` 취소선 문법과 충돌하여 텍스트가 의도치 않게 취소선 처리됨. 반드시 `\~`로 이스케이프하여 한국어 관습을 유지하면서 취소선 충돌을 방지.
   - ❌ `7~11`, `$20~40`, `3~5영업일` (bare tilde — 취소선 위험)
   - ✅ `7 \~ 11`, `$20 \~ 40`, `3 \~ 5영업일` (escaped tilde + 앞뒤 공백 — 렌더링 시 `7 ~ 11`로 표시)

## Quality Checklist (품질 체크리스트)

번역 완료 후 다음을 확인한다:

- [ ] 모든 종목 티커가 원본과 동일한가
- [ ] 모든 숫자/가격이 변경 없이 보존되었는가
- [ ] 날짜 형식이 원본과 일치하는가
- [ ] 테이블 구조 (행/열 수)가 동일한가
- [ ] Markdown 헤더 레벨이 일치하는가
- [ ] 코드 블록이 변경되지 않았는가
- [ ] 금융 용어가 사전과 일관되게 번역되었는가
- [ ] data-quality-checker 검증을 통과했는가
