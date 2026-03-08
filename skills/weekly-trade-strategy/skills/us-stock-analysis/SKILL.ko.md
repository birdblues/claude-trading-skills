---
name: us-stock-analysis
description: "재무(Fundamental), 기술적(Technical), 종목 비교, 투자 리포트 생성을 포함한 미국 주식 종합 분석 스킬입니다. 사용자가 미국 주식 티커 분석(예: \"analyze AAPL\", \"compare TSLA vs NVDA\", \"give me a report on Microsoft\"), 재무 지표 평가, 차트 기술적 분석, 또는 미국 주식 투자 제안을 요청할 때 사용합니다."
---

# 미국 주식 분석

## 개요

Fundamental analysis(재무, 비즈니스 품질, 밸류에이션), technical analysis(지표, 추세, 패턴), peer comparison을 포함해 미국 주식을 종합적으로 분석하고 상세 투자 리포트를 생성합니다. 웹 검색 도구로 최신 시장 데이터를 수집하고 구조화된 분석 프레임워크를 적용합니다.

## 데이터 소스

항상 웹 검색 도구를 사용해 최신 시장 데이터를 수집합니다:

**우선 수집 데이터:**
1. **현재 주가 및 거래 데이터** (price, volume, 52-week range)
2. **재무제표** (income statement, balance sheet, cash flow)
3. **핵심 지표** (P/E, EPS, revenue, margins, debt ratios)
4. **애널리스트 평가 및 목표가**
5. **최근 뉴스 및 주요 이슈**
6. **Peer/경쟁사 데이터** (비교 분석용)
7. **기술적 데이터** (가능한 경우 moving averages, RSI, MACD)

**검색 전략:**
- 티커 + 필요한 데이터 조합으로 검색(예: "AAPL financial metrics 2024")
- 종합 데이터는 실적 발표 자료, investor presentation, SEC filing 중심으로 검색
- 기술적 데이터는 "AAPL technical analysis" 또는 금융 데이터 사이트 활용
- 데이터 최신성은 항상 검증(최근 분기 데이터 우선)

**신뢰 가능한 소스:**
- Yahoo Finance, Google Finance, MarketWatch, Seeking Alpha, Bloomberg, CNBC
- 기업 IR 페이지
- 상세 재무 확인용 SEC filings (10-K, 10-Q)
- 기술적 데이터용 TradingView, StockCharts

## 분석 유형

이 스킬은 4가지 분석 유형을 지원합니다. 사용자 요청에 맞는 유형을 결정합니다:

1. **Basic Stock Info** - 핵심 지표 중심의 빠른 개요
2. **Fundamental Analysis** - 비즈니스/재무/밸류에이션 심층 분석
3. **Technical Analysis** - 차트 패턴, 지표, 추세 분석
4. **Comprehensive Report** - 모든 접근을 결합한 전체 리포트

## 분석 워크플로

### 1. Basic Stock Information

**사용 시점:** 사용자가 빠른 개요 또는 기본 정보를 요청할 때

**단계:**
1. 현재 주가 데이터(price, volume, market cap) 검색
2. 핵심 지표(P/E, EPS, revenue growth, margins) 수집
3. 52-week range와 연초 이후(YTD) 성과 확인
4. 최근 뉴스 또는 주요 이슈 확인
5. 간결한 요약 형식으로 제시

**출력 형식:**
- 회사 설명(1-2문장)
- 현재 주가 및 거래 지표
- 핵심 밸류에이션 지표(표)
- 최근 성과
- 최근 주요 뉴스(있는 경우)

### 2. Fundamental Analysis

**사용 시점:** 사용자가 재무 분석, 밸류에이션 평가, 비즈니스 평가를 원할 때

**단계:**
1. **종합 재무 데이터 수집:**
   - Revenue, earnings, cash flow (3-5년 추세)
   - Balance sheet 지표(debt, cash, working capital)
   - 수익성 지표(margins, ROE, ROIC)

2. 분석 프레임워크를 위해 **`references/fundamental-analysis.md`**를 읽습니다

3. 지표 정의/계산식을 위해 **`references/financial-metrics.md`**를 읽습니다

4. **비즈니스 품질 분석:**
   - 경쟁우위
   - 경영진 track record
   - 산업 내 포지션

5. **밸류에이션 분석 수행:**
   - 핵심 비율 계산(P/E, PEG, P/B, EV/EBITDA)
   - 과거 평균과 비교
   - peer group과 비교
   - 적정가치 범위 추정

6. **리스크 식별:**
   - 기업 고유 리스크
   - 시장/거시 리스크
   - 재무 데이터상 red flag

7. **출력 생성:** `references/report-template.md` 구조 준수

**핵심 분석 항목:**
- 수익성 추세(마진 개선/악화)
- 현금흐름 품질(FCF vs earnings)
- 재무건전성(debt 수준, liquidity)
- 성장 지속 가능성
- peers 및 과거 평균 대비 밸류에이션

### 3. Technical Analysis

**사용 시점:** 사용자가 technical analysis, 차트 패턴, 매매 시그널을 요청할 때

**단계:**
1. **기술적 데이터 수집:**
   - 현재 주가와 최근 price action
   - 거래량 추세
   - Moving averages(20-day, 50-day, 200-day)
   - Technical indicators(RSI, MACD, Bollinger Bands)

2. 지표 정의와 패턴을 위해 **`references/technical-analysis.md`**를 읽습니다

3. **추세 식별:**
   - 상승, 하락, 횡보
   - 추세 강도

4. **지지/저항 레벨 도출:**
   - 최근 고점/저점
   - 이동평균 레벨
   - 라운드 넘버

5. **지표 분석:**
   - RSI: 과매수(>70) 또는 과매도(<30)
   - MACD: crossover 및 divergence
   - Volume: 확인 또는 divergence
   - Bollinger Bands: squeeze 또는 expansion

6. **차트 패턴 식별:**
   - 반전 패턴(head and shoulders, double top/bottom)
   - 지속 패턴(flags, triangles)

7. **기술적 전망 생성:**
   - 현재 추세 평가
   - 관찰해야 할 핵심 레벨
   - Risk/reward 분석
   - 단기 및 중기 전망

**해석 가이드라인:**
- 단일 지표가 아닌 다중 지표로 신호 확인
- 거래량으로 신호 유효성 검증
- 가격과 지표 간 divergence 명시
- 항상 리스크 레벨(stop-loss) 식별

### 4. Comprehensive Investment Report

**사용 시점:** 사용자가 상세 리포트, 투자 추천, 완전한 분석을 요청할 때

**단계:**
1. **데이터 수집 수행** (Basic Info와 동일)

2. **Fundamental analysis 수행** (상기 워크플로 준수)

3. **Technical analysis 수행** (상기 워크플로 준수)

4. 전체 리포트 구조를 위해 **`references/report-template.md`**를 읽습니다

5. **결과 통합:**
   - Fundamental/Technical 인사이트 통합
   - Bull/Bear case 구성
   - Risk/reward 평가

6. **추천 생성:**
   - Buy/Hold/Sell rating
   - 시간축이 있는 target price
   - Conviction level
   - Entry strategy

7. **포맷된 리포트 생성:** 템플릿 구조 준수

**리포트 필수 포함 항목:**
- 추천을 포함한 Executive summary
- 회사 개요
- 투자 논리(Bull/Bear case)
- Fundamental analysis 섹션
- Technical analysis 섹션
- 밸류에이션 분석
- 리스크 평가
- 촉매와 타임라인
- 결론

## 종목 비교 분석

**사용 시점:** 사용자가 2개 이상 종목 비교를 요청할 때(예: "compare AAPL vs MSFT")

**단계:**
1. **모든 종목 데이터 수집:**
   - 각 티커에 대해 동일한 데이터 수집 절차 수행
   - 비교 가능한 기간으로 정렬

2. **`references/fundamental-analysis.md`** 및 `references/financial-metrics.md` 읽기

3. **나란히 비교표 작성:**
   - 비즈니스 모델 비교
   - 재무 지표 테이블(핵심 비율 전체)
   - 밸류에이션 지표 테이블
   - 성장률 비교
   - 수익성 비교
   - 재무건전성 비교

4. **상대 강점 식별:**
   - 각 회사가 우위인 영역
   - 수치화된 강점

5. **기술적 비교:**
   - 상대강도
   - 모멘텀 비교
   - 기술적으로 더 우수한 포지션 판단

6. **추천 생성:**
   - 어떤 종목이 더 매력적인지와 그 이유
   - Fundamental/Technical 요인 동시 고려
   - 포트폴리오 배분 제안
   - 리스크 조정 수익률 관점 평가

**출력 형식:** `references/report-template.md`의 "Comparison Report Structure"를 따릅니다.

## 출력 가이드라인

**일반 원칙:**
- 재무 데이터와 비교는 표로 제시(스캔 용이성)
- 핵심 지표와 결론은 굵게 표시
- 데이터 소스와 날짜 포함
- 가능한 한 수치화
- Bull/Bear 관점 모두 제시
- 가정과 불확실성을 명확히 표기

**포맷:**
- 섹션 구분을 위한 **Headers**
- 지표/비교/과거 데이터용 **Tables**
- 목록/요인/리스크용 **Bullet points**
- 핵심 지표/중요 발견 강조용 **Bold text**
- 성장률/수익률/마진은 **Percentages**
- 통화 형식 일관성 유지(`$B` billions, `$M` millions)

**톤:**
- 객관적이고 균형 있게
- 불확실성을 인정
- 주장에는 데이터 근거 제시
- 과장 표현 지양
- 리스크를 명확히 제시

## 레퍼런스 파일

분석 중 필요할 때 다음 레퍼런스를 로드합니다:

**references/technical-analysis.md**
- 사용 시점: technical analysis 수행 또는 지표 해석 시
- 포함 내용: 지표 정의, 차트 패턴, 지지/저항 개념, 분석 워크플로

**references/fundamental-analysis.md**
- 사용 시점: fundamental analysis 또는 비즈니스 평가 수행 시
- 포함 내용: 비즈니스 품질 평가, 재무건전성 분석, 밸류에이션 프레임워크, 리스크 평가, red flags

**references/financial-metrics.md**
- 사용 시점: 재무 비율 정의 또는 계산 방법이 필요할 때
- 포함 내용: 수익성/밸류에이션/성장성/유동성/레버리지/효율성/현금흐름 등 핵심 지표 공식

**references/report-template.md**
- 사용 시점: 종합 리포트 또는 비교 리포트 작성 시
- 포함 내용: 전체 리포트 구조, 포맷 가이드, 섹션 템플릿, 비교 형식

## 예시 질의

**Basic Info:**
- "What's the current price of AAPL?"
- "Give me key metrics for Tesla"
- "Quick overview of Microsoft stock"

**Fundamental:**
- "Analyze NVDA's financials"
- "Is Amazon overvalued?"
- "Evaluate Apple's business quality"
- "What's Google's debt situation?"

**Technical:**
- "Technical analysis of TSLA"
- "Is Netflix oversold?"
- "Show me support levels for AAPL"
- "What's the trend for AMD?"

**Comprehensive:**
- "Complete analysis of Microsoft"
- "Give me a full report on AAPL"
- "Should I invest in Tesla? Give me detailed analysis"

**Comparison:**
- "Compare AAPL vs MSFT"
- "Tesla vs Nvidia - which is better?"
- "Analyze Meta vs Google"
