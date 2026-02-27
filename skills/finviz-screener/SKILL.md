---
name: finviz-screener
description: Build and open FinViz screener URLs from natural language requests. Use when user wants to screen stocks, find stocks matching criteria, filter by fundamentals or technicals, or asks to open FinViz with specific conditions. Supports both Korean and English input (e.g., "고배당에 성장하는 소형주를 찾고 싶다", "Find oversold large caps with high ROE").
---

# FinViz Screener

## Overview

Translate natural-language stock screening requests into FinViz screener filter codes, build the URL, and open it in Chrome. No API key required for public screener; FINVIZ Elite is auto-detected from `$FINVIZ_API_KEY` for enhanced functionality.

**Key Features:**
- Natural language → filter code mapping (Korean + English)
- URL construction with view type and sort order selection
- Elite/Public auto-detection (environment variable or explicit flag)
- Chrome-first browser opening with OS-appropriate fallbacks
- Strict filter validation to prevent URL injection

---

## When to Use This Skill

**Explicit Triggers:**
- "고배당에 성장하는 소형주를 찾고 싶다"
- "Find oversold large caps near 52-week lows"
- "테크놀로지 섹터의 저평가 주식을 스크리닝하고 싶다"
- "Screen for stocks with insider buying"
- "FinViz에서 브레이크아웃 후보를 표시해줘"
- "Show me high-growth small caps on FinViz"
- "배당 수익률 5% 이상에 ROE 15% 이상 종목을 찾아줘"

**Implicit Triggers:**
- User describes stock screening criteria using fundamental or technical terms
- User mentions FinViz screener or stock filtering
- User asks to find stocks matching specific financial characteristics

**When NOT to Use:**
- Deep fundamental analysis of a specific stock (use us-stock-analysis)
- Portfolio review with holdings (use portfolio-manager)
- Chart pattern analysis on images (use technical-analyst)
- Earnings-based screening (use earnings-trade-analyzer or pead-screener)

---

## Workflow

### Step 1: Load Filter Reference

Read the filter knowledge base:

```bash
cat references/finviz_screener_filters.md
```

### Step 2: Interpret User Request

Map the user's natural-language request to FinViz filter codes. Use the Common Concept Mapping table below for quick translation, and reference the full filter list for precise code selection.

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

### Step 3: Present Filter Selection

Before executing, present the selected filters in a table for user confirmation:

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

Ask the user to confirm or adjust before proceeding.

### Step 4: Execute Script

Run the screener script to build the URL and open Chrome:

```bash
python3 scripts/open_finviz_screener.py \
  --filters "cap_small,fa_div_o3,fa_pe_u20,geo_usa" \
  --view overview
```

**Script arguments:**
- `--filters` (required): Comma-separated filter codes
- `--elite`: Force Elite mode (auto-detected from `$FINVIZ_API_KEY` if not set)
- `--view`: View type — overview, valuation, financial, technical, ownership, performance, custom
- `--order`: Sort order (e.g., `-marketcap`, `dividendyield`, `-change`)
- `--url-only`: Print URL without opening browser

### Step 5: Report Results

After opening the screener, report:
1. The constructed URL
2. Elite or Public mode used
3. Summary of applied filters
4. Suggested next steps (e.g., "Sort by dividend yield", "Switch to Financial view for detailed ratios")

---

## Resources

- `references/finviz_screener_filters.md` — Complete filter code reference with natural language keywords (includes industry code examples; full 142-code list is in the Industry Codes section)
- `scripts/open_finviz_screener.py` — URL builder and Chrome opener
