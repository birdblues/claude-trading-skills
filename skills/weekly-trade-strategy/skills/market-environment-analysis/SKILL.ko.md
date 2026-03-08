---
name: market-environment-analysis
description: 종합 시장 환경 분석 및 보고서 작성 도구. 미국/유럽/아시아 시장, 외환, 원자재, 경제지표를 포함한 글로벌 시장을 분석합니다. Risk-on/risk-off 평가, 섹터 분석, 기술적 지표 해석을 제공합니다. market analysis, market environment, global markets, trading environment, market conditions, investment climate, market sentiment, forex analysis, stock market analysis, 시장 환경, 시장 분석, 마켓 상황, 투자 환경 같은 키워드에서 트리거됩니다.
---

# Market Environment Analysis

언제든 시장 상황을 이해하고 전문적인 시장 리포트를 작성하기 위한 종합 분석 도구입니다.

## Core Workflow

### 1. 초기 데이터 수집
`web_search` 도구를 사용해 최신 시장 데이터를 수집합니다:
1. 주요 주가지수 (S&P 500, NASDAQ, Dow, Nikkei 225, Shanghai Composite, Hang Seng)
2. 외환 환율 (USD/JPY, EUR/USD, 주요 통화쌍)
3. 원자재 가격 (WTI crude, Gold, Silver)
4. 미국 국채 수익률 (2-year, 10-year, 30-year)
5. VIX 지수 (Fear gauge)
6. 시장 거래 상태 (open/close/current values)

### 2. 시장 환경 평가
수집 데이터로 다음을 평가합니다:
- **추세 방향**: Uptrend/Downtrend/Range-bound
- **리스크 심리**: Risk-on/Risk-off
- **변동성 상태**: VIX 기반 시장 불안 수준
- **섹터 로테이션**: 자금이 이동하는 섹터

### 3. 리포트 구조

#### 표준 리포트 형식:
```
1. Executive Summary (3-5 key points)
2. Global Market Overview
   - US Markets
   - Asian Markets
   - European Markets
3. Forex & Commodities Trends
4. Key Events & Economic Indicators
5. Risk Factor Analysis
6. Investment Strategy Implications
```

## 스크립트 사용

### market_utils.py
리포트 생성 공통 함수를 제공합니다:
```bash
# Generate report header
python scripts/market_utils.py

# Available functions:
- format_market_report_header(): Create header
- get_market_session_times(): Check trading hours
- categorize_volatility(vix): Interpret VIX levels
- format_percentage_change(value): Format price changes
```

## 참고 문서

### 주요 지표 해석 (references/indicators.md)
다음이 필요할 때 참고:
- 각 지수의 중요 레벨
- 기술적 분석 핵심 포인트
- 섹터별 체크 포인트

### 분석 패턴 (references/analysis_patterns.md)
다음을 분석할 때 참고:
- Risk-on/Risk-off 기준
- 경제지표 해석
- 인터마켓 상관관계
- 계절성 및 시장 이상현상

## 출력 예시

### 빠른 요약 버전
```
📊 Market Summary [2025/01/15 14:00]
━━━━━━━━━━━━━━━━━━━━━
【US】S&P 500: 5,123.45 (+0.45%)
【JP】Nikkei 225: 38,456.78 (-0.23%)
【FX】USD/JPY: 149.85 (↑0.15)
【VIX】16.2 (Normal range)

⚡ Key Events
- Japan GDP Flash
- US Employment Report

📈 Environment: Risk-On Continues
```

### 상세 분석 버전
Executive summary로 시작하고, 이후 각 섹션을 상세 분석합니다.
핵심 명확화 항목:
1. 현재 시장 국면 (Bullish/Bearish/Neutral)
2. 단기 방향성 (1-5일 전망)
3. 모니터링할 리스크 이벤트
4. 권장 포지션 조정

## 중요 고려사항

### 타임존 인식
- 주요 시장 타임존을 모두 고려
- 미국 시장: 아시아 시간 기준 저녁~새벽
- 유럽 시장: 아시아 시간 기준 오후~저녁
- 아시아 시장: 현지 시간 기준 오전~오후

### 경제 캘린더 우선순위
중요도별 분류:
- ⭐⭐⭐ Critical (FOMC, NFP, CPI 등)
- ⭐⭐ Important (GDP, Retail Sales 등)
- ⭐ Reference level

### 데이터 소스 우선순위
1. 공식 발표(중앙은행, 정부 통계)
2. 주요 금융 미디어(Bloomberg, Reuters)
3. 브로커 리포트
4. 애널리스트 컨센서스

## 트러블슈팅

### 데이터 수집 노트
- 시장 휴장일 확인(holiday calendars)
- 서머타임 변경 인지
- 속보(flash)와 확정(final) 데이터 구분

### 시장 변동성 대응
1. 사실관계 먼저 정리
2. 유사 과거 사례 참조
3. 복수 소스로 검증
4. 객관적 분석 유지

## 커스터마이징 옵션

사용자 투자 스타일에 맞춰 조정:
- **Day Traders**: Intraday 차트, order flow 중심
- **Swing Traders**: Daily/weekly 기술적 분석 강조
- **Long-term Investors**: 펀더멘털, 거시경제 중심
- **Forex Traders**: 통화 상관관계, 금리차 중심
- **Options Traders**: 변동성 분석, Greeks 모니터링
