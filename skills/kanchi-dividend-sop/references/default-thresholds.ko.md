# 기본 임계값

사용자가 커스텀 risk 설정을 제공하지 않을 때 아래 기본값을 사용합니다.

## Baseline (US Stock-Focused)

| 카테고리 | 지표 | 기본값 | 해석 |
|---|---|---:|---|
| Yield | Forward dividend yield | >= 3.5% | Kanchi Step 1 핵심 필터 |
| Yield trap | Extreme yield flag | >= 8.0% | 통과 전에 deep dive 강제 |
| Growth | Revenue CAGR (5y) | > 0% | 기본 business expansion 점검 |
| Growth | EPS CAGR (5y) | > 0% | earnings trend 건전성 |
| Dividend trend | Dividend growth (5y) | Non-declining | 강한 safety가 있을 때만 flat 허용 |
| Safety | EPS payout ratio | <= 70% | `70-85%` = 주의 |
| Safety | FCF payout ratio | <= 80% | `>100%` = high risk |
| Balance sheet | Net debt trend | Not persistently rising | 3개 기간 연속 상승 = 경고 |
| Balance sheet | Interest coverage | >= 3.0x | `<2.5x` = 주의 |
| Entry trigger | Yield alpha vs 5y average | +0.5pp | 기본 Kanchi Step 5 pullback 임계값 |

## Instrument별 참고

coverage check에는 아래 denominator 대체값을 사용합니다:

| Instrument type | Primary denominator | 참고 |
|---|---|---|
| Stock | FCF | `CFO - CapEx` 사용 |
| REIT | FFO/AFFO | 가능하면 AFFO 우선 |
| BDC | NII | distribution 대비 NII 비교 |
| ETF | 많은 경우 fund-level distribution coverage 확인 불가 | methodology 및 holdings quality 중심 점검 |

## 목표별 튜닝

profile별 조정값을 적용합니다:

| Profile | Yield floor | Safety bias | 참고 |
|---|---:|---|---|
| Income now | 4.0% | Tight safety checks | 단일 high-yield sector 과집중 회피 |
| Balanced | 3.0-3.5% | Medium | current income과 dividend growth를 혼합 |
| Growth first | 1.5-2.5% | High quality first | 더 높은 dividend CAGR을 위해 초기 yield 하향 허용 |

## Step 5 Alpha 튜닝

yield-trigger alpha는 아래 범위를 사용합니다:
- Stable mega-cap compounders: `+0.3pp`.
- 기본 baseline: `+0.5pp`.
- Higher-volatility 종목: `+0.8pp` to `+1.0pp`.

## 포트폴리오 제약

실무 기본값으로 아래를 사용합니다:
- 최대 종목 수: `15-30`.
- 단일 종목 최대 매입 비중: `<= 8%`.
- 최대 섹터 비중: `<= 25%`.
- High-yield bucket(REIT/telecom/utilities 합산): `<= 35%`.

사용자가 명시적으로 다른 정책을 선택한 경우에만 override하세요.
