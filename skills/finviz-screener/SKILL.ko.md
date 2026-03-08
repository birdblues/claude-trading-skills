---
name: finviz-screener
description: 자연어 요청으로 FinViz screener URL을 만들고 열어줍니다. 사용자가 종목 스크리닝, 조건 기반 종목 탐색, 재무/기술적 필터 적용, 특정 조건의 FinViz 열기를 요청할 때 사용하세요. 한국어/영어 입력을 모두 지원합니다(예: "고배당에 성장하는 소형주를 찾고 싶다", "Find oversold large caps with high ROE").
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
| Fallen angel | 급락 후 반등 | `ta_highlow52w_b20to30h,ta_rsi_os40` |
| AI theme | AI 테마 | `theme_artificialintelligence` |
| Cybersecurity theme | 사이버 보안 | `theme_cybersecurity` |
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

## 리소스

- `references/finviz_screener_filters.md` — 자연어 키워드를 포함한 전체 filter code 참고서 (industry code 예시 포함, 전체 142-code 목록은 Industry Codes 섹션 참조)
- `scripts/open_finviz_screener.py` — URL builder 및 Chrome opener
