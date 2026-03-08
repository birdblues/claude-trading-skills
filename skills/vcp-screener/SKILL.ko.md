---
name: vcp-screener
description: S&P 500 종목을 대상으로 Mark Minervini의 Volatility Contraction Pattern(VCP)을 스크리닝합니다. Stage 2 상승 추세에서 변동성이 축소되는 타이트한 베이스를 형성하며 breakout pivot 근처에 있는 종목을 식별합니다. 사용자가 VCP 스크리닝, Minervini 스타일 셋업, 타이트 베이스 패턴, 변동성 축소 breakout 후보, 또는 Stage 2 모멘텀 스캔을 요청할 때 사용합니다.
---

# VCP 스크리너 - Minervini Volatility Contraction Pattern

S&P 500 종목에서 Mark Minervini의 Volatility Contraction Pattern(VCP)을 스크리닝하여, breakout pivot 근처에서 변동성이 수축하는 Stage 2 상승 추세 종목을 식별합니다.

## 사용 시점

- 사용자가 VCP 스크리닝 또는 Minervini 스타일 셋업을 요청할 때
- 사용자가 타이트 베이스 / 변동성 축소 패턴 종목을 찾고 싶을 때
- 사용자가 Stage 2 모멘텀 종목 스캔을 요청할 때
- 사용자가 리스크가 정의된 breakout 후보를 요청할 때

## 사전 준비

- FMP API 키 (`FMP_API_KEY` 환경 변수 설정 또는 `--api-key` 전달)
- Free tier(일 250콜)로 기본 스크리닝(상위 100개 후보)에 충분
- 전체 S&P 500 스크리닝(`--full-sp500`)은 Paid tier 권장

## 워크플로

### Step 1: 스크리닝 준비 및 실행

VCP 스크리너 스크립트를 실행합니다:

```bash
# Default: S&P 500, top 100 candidates
python3 skills/vcp-screener/scripts/screen_vcp.py --output-dir skills/vcp-screener/scripts

# Custom universe
python3 skills/vcp-screener/scripts/screen_vcp.py --universe AAPL NVDA MSFT AMZN META --output-dir skills/vcp-screener/scripts

# Full S&P 500 (paid API tier)
python3 skills/vcp-screener/scripts/screen_vcp.py --full-sp500 --output-dir skills/vcp-screener/scripts
```

### 고급 튜닝 (백테스트용)

리서치와 백테스트를 위해 VCP 탐지 파라미터를 조정합니다:

```bash
python3 skills/vcp-screener/scripts/screen_vcp.py \
  --min-contractions 3 \
  --t1-depth-min 12.0 \
  --breakout-volume-ratio 2.0 \
  --trend-min-score 90 \
  --atr-multiplier 1.5 \
  --output-dir reports/
```

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `--min-contractions` | 2 | 2-4 | 높일수록 패턴 수는 줄고 품질은 높아짐 |
| `--t1-depth-min` | 8.0% | 1-50 | 높일수록 얕은 첫 조정을 제외 |
| `--breakout-volume-ratio` | 1.5x | 0.5-10 | 높일수록 거래량 확인이 엄격해짐 |
| `--trend-min-score` | 85 | 0-100 | 높일수록 Stage 2 필터가 엄격해짐 |
| `--atr-multiplier` | 1.5 | 0.5-5 | 낮출수록 스윙 탐지가 민감해짐 |
| `--contraction-ratio` | 0.75 | 0.1-1 | 낮출수록 더 타이트한 수축을 요구 |
| `--min-contraction-days` | 5 | 1-30 | 높일수록 최소 수축 기간이 길어짐 |
| `--lookback-days` | 120 | 30-365 | 길수록 오래된 패턴까지 탐지 |

### Step 2: 결과 검토

1. 생성된 JSON 및 Markdown 리포트를 읽습니다
2. 패턴 해석 컨텍스트를 위해 `references/vcp_methodology.md`를 로드합니다
3. 점수 임계값 가이드를 위해 `references/scoring_system.md`를 로드합니다

### Step 3: 분석 제시

각 상위 후보에 대해 다음을 제시합니다:
- VCP composite score 및 rating
- 수축 상세(T1/T2/T3 depth와 ratio)
- 트레이드 셋업: pivot price, stop-loss, risk percentage
- Volume dry-up ratio
- Relative strength rank

### Step 4: 실행 가능한 가이드 제공

rating 기준:
- **Textbook VCP (90+):** pivot에서 공격적 비중으로 매수
- **Strong VCP (80-89):** pivot에서 표준 비중으로 매수
- **Good VCP (70-79):** pivot 상단에서 거래량 확인 후 매수
- **Developing (60-69):** watchlist에 추가, 더 타이트한 수축 대기
- **Weak/No VCP (<60):** 모니터링만 하거나 제외

## 3단계 파이프라인

1. **Pre-Filter** - Quote 기반 스크리닝(price, volume, 52w position) 약 101 API calls
2. **Trend Template** - 7개 항목 Stage 2 필터 + 260일 히스토리 약 100 API calls
3. **VCP Detection** - 패턴 분석, 스코어링, 리포트 생성(API 추가 호출 없음)

## 출력물

- `vcp_screener_YYYY-MM-DD_HHMMSS.json` - 구조화된 결과
- `vcp_screener_YYYY-MM-DD_HHMMSS.md` - 사람이 읽기 쉬운 리포트

## 리소스

- `references/vcp_methodology.md` - VCP 이론 및 Trend Template 설명
- `references/scoring_system.md` - 점수 임계값 및 구성요소 가중치
- `references/fmp_api_endpoints.md` - API 엔드포인트 및 rate limit
