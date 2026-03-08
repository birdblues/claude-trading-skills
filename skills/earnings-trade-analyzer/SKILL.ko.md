---
name: earnings-trade-analyzer
description: 5요인 점수 시스템(갭 크기, 실적 전 추세, 거래량 추세, MA200 위치, MA50 위치)으로 최근 실적 발표 후 종목을 분석합니다. 각 종목을 0-100으로 점수화하고 A/B/C/D 등급을 부여합니다. 사용자가 실적 트레이드 분석, 실적 후 모멘텀 스크리닝, 실적 갭 점수화, 최근 실적 반응 우수 종목 탐색을 요청할 때 사용하세요.
---

# Earnings Trade Analyzer - 실적 발표 후 5요인 점수화

5요인 가중 점수 시스템으로 최근 실적 발표 후 종목을 분석하여, 잠재적 모멘텀 트레이드를 위한 가장 강한 실적 반응을 식별합니다.

## 사용 시점

- 사용자가 실적 발표 후 트레이드 분석 또는 실적 갭 스크리닝을 요청할 때
- 사용자가 최근 실적 반응이 가장 좋은 종목을 찾고자 할 때
- 사용자가 실적 모멘텀 점수화 또는 등급화를 요청할 때
- 사용자가 post-earnings accumulation day (PEAD) 후보를 물을 때

## 사전 요구사항

- FMP API key (`FMP_API_KEY` 환경 변수 설정 또는 `--api-key` 전달)
- 기본 스크리닝(최근 2일, 상위 20개)에는 free tier(250 calls/day)로 충분
- 더 큰 lookback window나 전체 스크리닝에는 paid tier 권장

## 워크플로

### 1단계: Earnings Trade Analyzer 실행

분석기 스크립트를 실행합니다:

```bash
# Default: last 2 days of earnings, top 20 results
python3 skills/earnings-trade-analyzer/scripts/analyze_earnings_trades.py --output-dir reports/

# Custom lookback and market cap filter
python3 skills/earnings-trade-analyzer/scripts/analyze_earnings_trades.py \
  --lookback-days 5 \
  --min-market-cap 1000000000 \
  --top 30 \
  --output-dir reports/

# With entry quality filter
python3 skills/earnings-trade-analyzer/scripts/analyze_earnings_trades.py \
  --apply-entry-filter \
  --output-dir reports/
```

### 2단계: 결과 검토

1. 생성된 JSON 및 Markdown 보고서를 읽습니다.
2. 점수 해석 컨텍스트를 위해 `references/scoring_methodology.md`를 로드합니다.
3. 실행 가능한 셋업은 Grade A/B 종목을 우선 확인합니다.

### 3단계: 분석 제시

각 상위 후보에 대해 다음을 제시합니다:
- 종합 점수와 문자 등급(A/B/C/D)
- 실적 갭 크기와 방향
- 실적 전 20일 추세
- 거래량 비율(20일 vs 60일 평균)
- 200일 및 50일 이동평균 대비 위치
- 가장 약한 점수 구성 요소와 가장 강한 점수 구성 요소

### 4단계: 실행 가능한 가이드 제시

등급 기준:
- **Grade A (85+):** 기관 수급이 동반된 강한 실적 반응 - 진입 고려
- **Grade B (70-84):** 모니터링할 만한 양호한 실적 반응 - 눌림 또는 확인 신호 대기
- **Grade C (55-69):** 신호 혼재 - 주의 필요, 추가 분석 권장
- **Grade D (<55):** 약한 셋업 - 회피 또는 더 나은 조건 대기

## 출력

- `earnings_trade_analyzer_YYYY-MM-DD_HHMMSS.json` - schema_version "1.0"의 구조화 결과
- `earnings_trade_analyzer_YYYY-MM-DD_HHMMSS.md` - 표를 포함한 사람이 읽기 쉬운 보고서

## 리소스

- `references/scoring_methodology.md` - 5요인 점수 시스템, 등급 임계값, entry quality filter 규칙
