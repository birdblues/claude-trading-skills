---
name: pead-screener
description: PEAD(Post-Earnings Announcement Drift) 패턴을 찾기 위해 실적 발표 후 gap-up 종목을 스크리닝합니다. 주봉 캔들 형성을 분석해 red candle pullback과 breakout 신호를 감지합니다. 두 가지 입력 모드 지원 - FMP earnings calendar(Mode A) 또는 earnings-trade-analyzer JSON output(Mode B). 사용자가 PEAD 스크리닝, post-earnings drift, 실적 갭 추세 지속, red candle breakout 패턴, 주간 실적 모멘텀 셋업을 요청할 때 사용하세요.
---

# PEAD Screener - Post-Earnings Announcement Drift

주봉 캔들 분석으로 red candle pullback 및 breakout 신호를 감지하여, 실적 발표 후 gap-up 종목에서 PEAD(Post-Earnings Announcement Drift) 패턴을 스크리닝합니다.

## When to Use

- 사용자가 PEAD 스크리닝 또는 post-earnings drift 분석을 요청할 때
- 사용자가 실적 gap-up 후 추세 지속 가능성이 있는 종목을 찾고자 할 때
- 사용자가 실적 이후 red candle breakout 패턴을 요청할 때
- 사용자가 주간 실적 모멘텀 셋업을 요청할 때
- 사용자가 추가 스크리닝을 위해 earnings-trade-analyzer JSON output을 제공할 때

## Prerequisites

- FMP API key (`FMP_API_KEY` 환경 변수 설정 또는 `--api-key` 전달)
- 기본 스크리닝에는 free tier(250 calls/day)로 충분
- Mode B 사용 시: schema_version "1.0"의 earnings-trade-analyzer JSON output 파일 필요

## Workflow

### Step 1: Prepare and Execute Screening

두 가지 모드 중 하나로 PEAD screener script를 실행합니다:

**Mode A (FMP earnings calendar):**
```bash
# Default: last 14 days of earnings, 5-week monitoring window
python3 skills/pead-screener/scripts/screen_pead.py --output-dir reports/

# Custom parameters
python3 skills/pead-screener/scripts/screen_pead.py \
  --lookback-days 21 \
  --watch-weeks 6 \
  --min-gap 5.0 \
  --min-market-cap 1000000000 \
  --output-dir reports/
```

**Mode B (earnings-trade-analyzer JSON input):**
```bash
# From earnings-trade-analyzer output
python3 skills/pead-screener/scripts/screen_pead.py \
  --candidates-json reports/earnings_trade_analyzer_YYYY-MM-DD_HHMMSS.json \
  --min-grade B \
  --output-dir reports/
```

### Step 2: Review Results

1. 생성된 JSON 및 Markdown 리포트를 읽습니다
2. PEAD 이론과 패턴 맥락을 위해 `references/pead_strategy.md`를 로드합니다
3. 트레이드 관리 규칙을 위해 `references/entry_exit_rules.md`를 로드합니다

### Step 3: Present Analysis

각 후보에 대해 다음을 제시합니다:
- Stage 분류 (MONITORING, SIGNAL_READY, BREAKOUT, EXPIRED)
- 주봉 캔들 패턴 세부 정보 (red candle 위치, breakout 상태)
- Composite score 및 rating
- Trade setup: entry, stop-loss, target, risk/reward ratio
- Liquidity metrics (ADV20, average volume)

### Step 4: Provide Actionable Guidance

stage와 rating에 기반해:
- **BREAKOUT + Strong Setup (85+):** 고확신 PEAD 트레이드, full position size
- **BREAKOUT + Good Setup (70-84):** 양호한 PEAD 셋업, standard position size
- **SIGNAL_READY:** red candle 형성 완료, red candle high 상향 돌파 알림 설정
- **MONITORING:** 실적 이후 red candle 미형성, watchlist 편입
- **EXPIRED:** 모니터링 기간 초과, watchlist 제거

## Output

- `pead_screener_YYYY-MM-DD_HHMMSS.json` - stage 분류를 포함한 구조화 결과
- `pead_screener_YYYY-MM-DD_HHMMSS.md` - stage별 그룹의 사람이 읽기 쉬운 리포트

## Resources

- `references/pead_strategy.md` - PEAD 이론 및 주봉 캔들 접근
- `references/entry_exit_rules.md` - 진입, 청산, position sizing 규칙
