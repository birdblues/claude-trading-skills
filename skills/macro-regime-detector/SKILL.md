---
name: macro-regime-detector
description: Detect structural macro regime transitions (1-2 year horizon) using cross-asset ratio analysis. Analyze RSP/SPY concentration, yield curve, credit conditions, size factor, equity-bond relationship, and sector rotation to identify regime shifts between Concentration, Broadening, Contraction, Inflationary, and Transitional states. Run when user asks about macro regime, market regime change, structural rotation, or long-term market positioning.
---

# Macro Regime Detector

Detect structural macro regime transitions using monthly-frequency cross-asset ratio analysis. This skill identifies 1-2 year regime shifts that inform strategic portfolio positioning.

## When to Use

- User asks about current macro regime or regime transitions
- User wants to understand structural market rotations (concentration vs broadening)
- User asks about long-term positioning based on yield curve, credit, or cross-asset signals
- User references RSP/SPY ratio, IWM/SPY, HYG/LQD, or other cross-asset ratios
- User wants to assess whether a regime change is underway

## Workflow

1. Load reference documents for methodology context:
   - `references/regime_detection_methodology.md`
   - `references/indicator_interpretation_guide.md`

2. Execute the main analysis script:
   ```bash
   python3 skills/macro-regime-detector/scripts/macro_regime_detector.py
   ```
   This fetches 600 days of data for 9 ETFs + Treasury rates (10 API calls total).

3. Read the generated Markdown report and present findings to user. 탐지 결과와 뉴스 내러티브의 수렴/발산을 비교하세요 (Step 3.5의 Supabase 컨텍스트가 있는 경우).

#### Step 3.5: Supabase Breaking News Narrative Overlay (Optional)

**Prerequisite:** Check if `mcp__supabase__execute_sql` tool is available.
If not available, skip directly to Step 4.

Invoke the `supabase-news-summarizer` agent:

```
Agent tool:
  subagent_type: "supabase-news-summarizer"
  prompt: |
    최근 10일간 Supabase public.news 테이블의 속보를 전량 수집하여
    매크로 레짐 전환 감지에 특화된 요약을 생성해주세요.

    분석 기간: [현재 날짜 - 10일] ~ [현재 날짜]

    다음을 반환해주세요:
    1. 중앙은행 정책 전환 신호 (금리, QE/QT, 포워드 가이던스)
    2. 크레딧 사이클 변화 (하이일드 스프레드, 신용 긴축/완화)
    3. 대형주/소형주 로테이션 신호 (집중도 변화, 브로드닝)
    4. 인플레이션/디플레이션 내러티브 변화
    5. 주식-채권 상관관계 변화 관련 이벤트
    6. 크로스테마 상호작용
    7. 블라인드 스팟 경보 (사모/크레딧/시스템 리스크)
```

**Why agent:** 10일간 중요 속보 800+건 × detail 평균 824자 = ~665K자로 메인 컨텍스트에 직접 로드 불가. 에이전트가 자체 컨텍스트 윈도우에서 전량 처리 후 3,000자 이내 압축 요약을 반환.

**Agent output → Step 4 input:**
- 정량 탐지 결과와 뉴스 내러티브의 수렴/발산을 비교하여 레짐 전환 확신도를 조정
- 크레딧/정책 관련 블라인드 스팟은 레짐 전환 선행 지표로 활용

4. Provide additional context using `references/historical_regimes.md` when user asks about historical parallels.

## Prerequisites

- **FMP API Key** (required): Set `FMP_API_KEY` environment variable or pass `--api-key`
- Free tier (250 calls/day) is sufficient (script uses ~10 calls)

## 6 Components

| # | Component | Ratio/Data | Weight | What It Detects |
|---|-----------|------------|--------|-----------------|
| 1 | Market Concentration | RSP/SPY | 25% | Mega-cap concentration vs market broadening |
| 2 | Yield Curve | 10Y-2Y spread | 20% | Interest rate cycle transitions |
| 3 | Credit Conditions | HYG/LQD | 15% | Credit cycle risk appetite |
| 4 | Size Factor | IWM/SPY | 15% | Small vs large cap rotation |
| 5 | Equity-Bond | SPY/TLT + correlation | 15% | Stock-bond relationship regime |
| 6 | Sector Rotation | XLY/XLP | 10% | Cyclical vs defensive appetite |

## 5 Regime Classifications

- **Concentration**: Mega-cap leadership, narrow market
- **Broadening**: Expanding participation, small-cap/value rotation
- **Contraction**: Credit tightening, defensive rotation, risk-off
- **Inflationary**: Positive stock-bond correlation, traditional hedging fails
- **Transitional**: Multiple signals but unclear pattern

## Output

- `macro_regime_YYYY-MM-DD_HHMMSS.json` — Structured data for programmatic use
- `macro_regime_YYYY-MM-DD_HHMMSS.md` — Human-readable report with:
  1. Current Regime Assessment
  2. Transition Signal Dashboard
  3. Component Details
  4. Regime Classification Evidence
  5. Portfolio Posture Recommendations

## Relationship to Other Skills

| Aspect | Macro Regime Detector | Market Top Detector | Market Breadth Analyzer |
|--------|----------------------|--------------------|-----------------------|
| Time Horizon | 1-2 years (structural) | 2-8 weeks (tactical) | Current snapshot |
| Data Granularity | Monthly (6M/12M SMA) | Daily (25 business days) | Daily CSV |
| Detection Target | Regime transitions | 10-20% corrections | Breadth health score |
| API Calls | ~10 | ~33 | 0 (Free CSV) |

## Script Arguments

```bash
python3 macro_regime_detector.py [options]

Options:
  --api-key KEY       FMP API key (default: $FMP_API_KEY)
  --output-dir DIR    Output directory (default: current directory)
  --days N            Days of history to fetch (default: 600)
```

## Resources

- `references/regime_detection_methodology.md` — Detection methodology and signal interpretation
- `references/indicator_interpretation_guide.md` — Guide for interpreting cross-asset ratios
- `references/historical_regimes.md` — Historical regime examples for context

## 한글 리포트 생성

생성된 영어 리포트를 한국어로 번역한다.

1. `skills/report-translator/references/translation_guidelines.md`를 읽어 번역 가이드라인 확인
2. 생성된 마크다운 리포트를 한국어로 번역
   - 종목 티커, 숫자, 기술 지표명은 원본 유지
   - 섹션 헤더, 설명, 가이던스를 한국어로 변환
   - Markdown 구조(테이블, 볼드 등) 보존
3. 번역본을 `*_ko.md`로 저장
4. data-quality-checker로 번역본 검증:
   ```bash
   python3 skills/data-quality-checker/scripts/check_data_quality.py \
     --file reports/<translated_file>_ko.md --output-dir reports/
   ```
5. 검증 결과에 ERROR가 있으면 해당 부분 수정 후 재저장
