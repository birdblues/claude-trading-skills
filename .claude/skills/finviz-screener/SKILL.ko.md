---
name: finviz-screener
description: "자연어 요청으로 FinViz screener URL을 만들고 열어줍니다. 사용자가 종목 스크리닝, 조건 기반 종목 탐색, 재무/기술적 필터 적용, 특정 조건의 FinViz 열기를 요청할 때 사용하세요. 한국어/영어 입력을 모두 지원합니다(예: \"고배당에 성장하는 소형주를 찾고 싶다\", \"Find oversold large caps with high ROE\")."
---

# FinViz Screener

## 개요

자연어 기반 종목 스크리닝 요청을 FinViz screener filter code로 변환하고, URL을 구성해 Chrome에서 엽니다. 공개 screener는 API key가 필요 없고, 향상 기능을 위해 `$FINVIZ_API_KEY`를 통해 FINVIZ Elite를 자동 감지합니다.

**주요 기능:**
- 자연어 -> filter code 매핑 (Korean + English)
- view type 및 sort order를 포함한 URL 구성
- Elite/Public 자동 감지 (환경 변수 또는 명시적 플래그)
- Chrome 우선 브라우저 실행 + OS별 fallback
- URL injection 방지를 위한 엄격한 filter 검증

---

## 이 스킬을 사용할 때

**명시적 트리거:**
- "고배당에 성장하는 소형주를 찾고 싶다"
- "Find oversold large caps near 52-week lows"
- "테크놀로지 섹터의 저평가 주식을 스크리닝하고 싶다"
- "Screen for stocks with insider buying"
- "FinViz에서 브레이크아웃 후보를 표시해줘"
- "Show me high-growth small caps on FinViz"
- "배당 수익률 5% 이상에 ROE 15% 이상 종목을 찾아줘"

**암시적 트리거:**
- 사용자가 재무/기술 지표로 스크리닝 기준을 설명할 때
- 사용자가 FinViz screener 또는 종목 필터링을 언급할 때
- 사용자가 특정 재무 특성을 만족하는 종목 탐색을 요청할 때

**사용하지 말아야 할 경우:**
- 특정 종목의 심층 재무 분석 (use us-stock-analysis)
- 보유 자산 기반 포트폴리오 리뷰 (use portfolio-manager)
- 이미지 기반 차트 패턴 분석 (use technical-analyst)
- 실적 이벤트 중심 스크리닝 (use earnings-trade-analyzer or pead-screener)

---

## 워크플로

### 1단계: 필터 참고 자료 로드

필터 지식 베이스를 읽습니다:

```bash
cat references/finviz_screener_filters.md
```

### 2단계: 사용자 요청 해석

사용자의 자연어 요청을 FinViz filter code로 매핑합니다. 빠른 매핑을 위해 아래 Common Concept Mapping 표를 사용하고, 정확한 코드 선택은 전체 filter 목록을 참조합니다.

**참고:** 범위 기준(예: "배당 3-8%", "PER 10-20")의 경우, `_o`와 `_u` 필터를 조합하지 말고 `{from}to{to}` 범위 구문을 단일 필터 토큰으로 사용합니다(예: `fa_div_3to8`, `fa_pe_10to20`).

**Common Concept Mapping:**

| User Concept (EN) | User Concept (KR) | Filter Codes |
|---|---|---|
| High dividend | 고배당 | `fa_div_o3` or `fa_div_o5` |
| Small cap | 소형주 | `cap_small` |
| Mid cap | 중형주 | `cap_mid` |
| Large cap | 대형주 | `cap_large` |
| Mega cap | 초대형주 | `cap_mega` |
| Value / cheap | 저평가 | `fa_pe_u20,fa_pb_u2` |
| Growth stock | 성장주 | `fa_epsqoq_o25,fa_salesqoq_o15` |
| Oversold | 과매도 | `ta_rsi_os30` |
| Overbought | 과매수 | `ta_rsi_ob70` |
| Near 52W high | 52주 고가 부근 | `ta_highlow52w_b0to5h` |
| Near 52W low | 52주 저가 부근 | `ta_highlow52w_a0to5l` |
| Breakout | 브레이크아웃 | `ta_highlow52w_b0to5h,sh_relvol_o1.5` |
| Technology | 테크놀로지 | `sec_technology` |
| Healthcare | 헬스케어 | `sec_healthcare` |
| Energy | 에너지 | `sec_energy` |
| Financial | 금융 | `sec_financial` |
| Semiconductors | 반도체 | `ind_semiconductors` |
| Biotechnology | 바이오테크 | `ind_biotechnology` |
| US stocks | 미국 주식 | `geo_usa` |
| Profitable | 흑자 | `fa_pe_profitable` |
| High ROE | 고ROE | `fa_roe_o15` or `fa_roe_o20` |
| Low debt | 저부채 | `fa_debteq_u0.5` |
| Insider buying | 인사이더 매수 | `sh_insidertrans_verypos` |
| Short squeeze | 숏 스퀴즈 | `sh_short_o20,sh_relvol_o2` |
| Dividend growth | 배당 증가 | `fa_divgrowth_3yo10` |
| Deep value | 딥 밸류 | `fa_pb_u1,fa_pe_u10` |
| Momentum | 모멘텀 | `ta_perf_13wup,ta_sma50_pa,ta_sma200_pa` |
| Defensive | 디펜시브 | `ta_beta_u0.5` or `sec_utilities,sec_consumerdefensive` |
| Liquid / high volume | 고거래량 | `sh_avgvol_o500` or `sh_avgvol_o1000` |
| Pullback from high | 고점 대비 눌림목 | `ta_highlow52w_10to30-bhx` |
| Near 52W low reversal | 저가권 리버설 | `ta_highlow52w_10to30-alx` |
| Fallen angel | 급락 후 반등 | `ta_highlow52w_b20to30h,ta_rsi_os40` |
| AI theme | AI 테마 | `theme_artificialintelligence` |
| Cybersecurity theme | 사이버 보안 | `theme_cybersecurity` |
| Yield 3-8% (trap excluded) | 배당 3-8% (함정 제외) | `fa_div_3to8` |
| Mid-range P/E | 적정 PER대 | `fa_pe_10to20` |
| EV undervalued | EV 저평가 | `fa_evebitda_u10` |
| Earnings next week | 다음 주 실적 발표 | `earningsdate_nextweek` |
| IPO recent | 최근 IPO | `ipodate_thismonth` |
| Target price above | 목표 주가 이상 | `targetprice_a20` |
| Recent news | 최신 뉴스 있음 | `news_date_today` |
| High institutional | 기관 보유율 높음 | `sh_instown_o60` |
| Low float | 유동 주식 수 적음 | `sh_float_u20` |
| Near all-time high | 사상 최고가 부근 | `ta_alltime_b0to5h` |
| High ATR | 고변동성 | `ta_averagetruerange_o1.5` |

### 3단계: 필터 선택 제시

실행 전에 선택된 필터를 표로 먼저 보여주고 사용자 확인을 받습니다:

```markdown
| Filter Code | Meaning |
|---|---|
| cap_small | Small Cap ($300M–$2B) |
| fa_div_o3 | Dividend Yield > 3% |
| fa_pe_u20 | P/E < 20 |
| geo_usa | USA |

View: Overview (v=111)
Mode: Public / Elite (auto-detected)
```

진행 전에 사용자에게 확인 또는 조정을 요청합니다.

### 4단계: 스크립트 실행

screener script를 실행해 URL을 만들고 Chrome을 엽니다:

```bash
python3 scripts/open_finviz_screener.py \
  --filters "cap_small,fa_div_o3,fa_pe_u20,geo_usa" \
  --view overview
```

**스크립트 인자:**
- `--filters` (required): 쉼표로 구분된 filter code
- `--elite`: Elite 모드 강제 (설정하지 않으면 `$FINVIZ_API_KEY`로 auto-detected)
- `--view`: View type — overview, valuation, financial, technical, ownership, performance, custom
- `--order`: Sort order (예: `-marketcap`, `dividendyield`, `-change`)
- `--url-only`: 브라우저를 열지 않고 URL만 출력

### 5단계: 결과 보고

screener를 연 뒤 다음을 보고합니다:
1. 구성된 URL
2. 사용된 Elite/Public 모드
3. 적용된 필터 요약
4. 다음 단계 제안 (예: "Sort by dividend yield", "Switch to Financial view for detailed ratios")

---

## 사용 레시피

반복적인 사용에서 도출한 실전 스크리닝 패턴입니다. 각 레시피에는 시작 필터 세트, 추천 view, 반복적 정제 팁이 포함됩니다.

### 레시피 1: 고배당 성장주 (칸치 스타일)

**목표:** 고수익률 + 배당 증가 + 이익 증가, 수익률 함정 제외.

```
--filters "fa_div_3to8,fa_sales5years_pos,fa_eps5years_pos,fa_divgrowth_5ypos,fa_payoutratio_u60,geo_usa"
--view financial
```

| Filter Code | 용도 |
|---|---|
| `fa_div_3to8` | 수익률 3-8% (고수익률 함정 제한) |
| `fa_sales5years_pos` | 5년 매출 성장률 양수 |
| `fa_eps5years_pos` | 5년 EPS 성장률 양수 |
| `fa_divgrowth_5ypos` | 5년 배당 성장률 양수 |
| `fa_payoutratio_u60` | 배당성향 < 60% (지속가능성) |
| `geo_usa` | 미국 상장 주식 |

**반복 정제:** `fa_div_o3`로 넓게 시작 → 결과 검토 → `fa_div_3to8`로 수익률 상한 설정 → `fa_payoutratio_u60`으로 함정 제외 → `financial` view로 전환하여 배당성향 및 성장 컬럼 확인.

### 레시피 2: 미너비니 추세 템플릿 + VCP

**목표:** Stage 2 상승 추세에 있는 변동성 수축(VCP 셋업) 종목.

```
--filters "ta_sma50_pa,ta_sma200_pa,ta_sma200_sb50,ta_highlow52w_0to25-bhx,ta_perf_26wup,sh_avgvol_o300,cap_midover"
--view technical
```

| Filter Code | 용도 |
|---|---|
| `ta_sma50_pa` | 50일 이동평균 위 |
| `ta_sma200_pa` | 200일 이동평균 위 |
| `ta_sma200_sb50` | 200 SMA가 50 SMA 아래 (상승 추세) |
| `ta_highlow52w_0to25-bhx` | 52주 고가 대비 25% 이내 |
| `ta_perf_26wup` | 26주 수익률 양수 |
| `sh_avgvol_o300` | 평균 거래량 > 300K |
| `cap_midover` | 중형주 이상 |

**VCP 압축 필터 (추가 좁히기):** `ta_volatility_wo3,ta_highlow20d_b0to5h,sh_relvol_u1` — 낮은 주간 변동성, 20일 고가 부근, 평균 이하 상대 거래량 (수축 신호).

### 레시피 3: 부당하게 매도된 성장주

**목표:** 펀더멘털이 강한 기업 중 최근 급락한 종목 — 평균 회귀 후보.

```
--filters "fa_sales5years_o5,fa_eps5years_o10,fa_roe_o15,fa_salesqoq_pos,fa_epsqoq_pos,ta_perf_13wdown,ta_highlow52w_10to30-bhx,cap_large,sh_avgvol_o200"
--view overview
```

| Filter Code | 용도 |
|---|---|
| `fa_sales5years_o5` | 5년 매출 성장률 > 5% |
| `fa_eps5years_o10` | 5년 EPS 성장률 > 10% |
| `fa_roe_o15` | ROE > 15% |
| `fa_salesqoq_pos` | QoQ 매출 성장률 양수 |
| `fa_epsqoq_pos` | QoQ EPS 성장률 양수 |
| `ta_perf_13wdown` | 13주 수익률 음수 |
| `ta_highlow52w_10to30-bhx` | 52주 고가 대비 10-30% 하락 |
| `cap_large` | 대형주 |
| `sh_avgvol_o200` | 평균 거래량 > 200K |

**검토 후:** `valuation` view로 전환하여 P/E와 P/S로 진입 매력도를 확인.

### 레시피 4: 턴어라운드 주식

**목표:** 이전에 이익이 감소했으나 현재 회복 조짐을 보이는 기업 — 펀더멘털 확인 바텀 피싱.

```
--filters "fa_eps5years_neg,fa_epsqoq_pos,fa_salesqoq_pos,ta_highlow52w_b30h,ta_perf_13wup,cap_smallover,sh_avgvol_o200"
--view performance
```

| Filter Code | 용도 |
|---|---|
| `fa_eps5years_neg` | 5년 EPS 성장률 음수 (이전 하락) |
| `fa_epsqoq_pos` | QoQ EPS 성장률 양수 (회복) |
| `fa_salesqoq_pos` | QoQ 매출 성장률 양수 (회복) |
| `ta_highlow52w_b30h` | 52주 고가 대비 30% 이내 (바닥 아님) |
| `ta_perf_13wup` | 13주 수익률 양수 |
| `cap_smallover` | 소형주 이상 |
| `sh_avgvol_o200` | 평균 거래량 > 200K |

### 레시피 5: 모멘텀 매매 후보

**목표:** 거래량 증가와 함께 52주 고가 부근의 단기 모멘텀 리더.

```
--filters "ta_sma50_pa,ta_sma200_pa,ta_highlow52w_b0to3h,ta_perf_4wup,sh_relvol_o1.5,sh_avgvol_o1000,cap_midover"
--view technical
```

| Filter Code | 용도 |
|---|---|
| `ta_sma50_pa` | 50일 이동평균 위 |
| `ta_sma200_pa` | 200일 이동평균 위 |
| `ta_highlow52w_b0to3h` | 52주 고가 대비 3% 이내 |
| `ta_perf_4wup` | 4주 수익률 양수 |
| `sh_relvol_o1.5` | 상대 거래량 > 1.5배 |
| `sh_avgvol_o1000` | 평균 거래량 > 1M |
| `cap_midover` | 중형주 이상 |

### 팁: 반복적 정제 패턴

스크리닝은 단발 쿼리가 아니라 대화 형태로 진행할 때 가장 효과적입니다:

1. **넓게 시작** — 3-4개 핵심 필터로 초기 결과 세트 확보
2. **결과 수 검토** — 너무 많으면 (>100) 필터 추가로 좁히기; 너무 적으면 (<5) 조건 완화
3. **view 전환** — `overview`로 빠른 스캔 후, `financial` 또는 `valuation`으로 심층 검토
4. **기술적 필터 추가** — 펀더멘털 품질 확인 후, `ta_` 필터로 진입 타이밍 조절
5. **저장 후 반복** — URL을 북마크하고, 한 번에 하나씩 필터를 조정하여 영향 파악

---

## 리소스

- `references/finviz_screener_filters.md` — 자연어 키워드를 포함한 전체 filter code 참고서 (industry code 예시 포함, 전체 142-code 목록은 Industry Codes 섹션 참조)
- `scripts/open_finviz_screener.py` — URL builder 및 Chrome opener
