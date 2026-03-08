# FinViz Screener 필터 레퍼런스


이 레퍼런스는 FinViz screener filter code를 의미와 자연어 키워드(English + Korean)로 매핑합니다. Claude는 이 문서를 사용해 사용자 의도를 유효한 FinViz filter code로 변환합니다.


---


## URL 형식


**Public (무료):**

```

https://finviz.com/screener.ashx?v={view}&f={filters}&o={order}&s={signal}

```


**Elite (유료 구독):**

```

https://elite.finviz.com/screener.ashx?v={view}&f={filters}&o={order}&s={signal}

```


**파라미터:**

- `v` — View type code (아래 View Types 참조)

- `f` — 쉼표로 구분된 filter code (e.g., `cap_small,fa_div_o3,fa_pe_u20`)

- `o` — Sort order (선택; 내림차순은 `-` prefix 사용, 예: `-marketcap`)

- `t` — Ticker symbol (선택; 쉼표 구분, 예: `AAPL,MSFT`)

- `s` — Signal filter (선택; 아래 Signal Filters 참조)


---


## Signal Filters (`s=` 파라미터)


Signal은 `s=` URL 파라미터로 전달됩니다 (`f=` filter 문자열이 아님).

주요 signal:


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_topgainers` | Top Gainers | gainers, 상승률 상위 |
| `ta_toplosers` | Top Losers | losers, 하락률 상위 |
| `ta_newhigh` | New High | new high, 신고가 |
| `ta_newlow` | New Low | new low, 신저가 |
| `ta_mostvolatile` | Most Volatile | volatile, 고변동성 |
| `ta_mostactive` | Most Active | active, 활발 |
| `ta_unusualvolume` | Unusual Volume | unusual volume, 이상 거래량 |
| `ta_overbought` | Overbought | overbought, 과매수 |
| `ta_oversold` | Oversold | oversold, 과매도 |
| `ta_downgrades` | Downgrades | downgrade, 등급하향 |
| `ta_upgrades` | Upgrades | upgrade, 등급상향 |
| `ta_earnbefore` | Earnings Before | earnings before market |
| `ta_earnafter` | Earnings After | earnings after market |
| `n_majornews` | Major News | major news, 주요뉴스 |
| `ta_p_wedgeup` | Wedge Up |  |
| `ta_p_wedgedown` | Wedge Down |  |
| `ta_p_tri_ascending` | Triangle Ascending |  |
| `ta_p_tri_descending` | Triangle Descending |  |
| `ta_p_channelup` | Channel Up |  |
| `ta_p_channeldown` | Channel Down |  |
| `ta_p_channel` | Channel |  |
| `ta_p_doubletop` | Double Top |  |
| `ta_p_doublebottom` | Double Bottom |  |
| `ta_p_headandshoulders` | Head and Shoulders |  |
| `ta_p_headandshouldersinv` | Head and Shoulders Inverse |  |

---


## View 타입


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `111` | Overview — ticker, company, sector, industry, country, market cap, P/E, price, change, volume | overview, 개요, 목록 |
| `121` | Valuation — market cap, P/E, Forward P/E, PEG, P/S, P/B, P/Cash, P/FCF, EPS, dividend yield | valuation, 밸류에이션, 저평가도 |
| `131` | Ownership — market cap, outstanding shares, float, insider/institutional ownership, short float | ownership, 소유, 주주구성 |
| `141` | Performance — performance periods (day to 10Y), volatility, RSI, SMA | performance, 퍼포먼스, 등락률 |
| `152` | Custom — user-defined columns | custom, 커스텀 |
| `161` | Financial — market cap, dividend yield, ROA, ROE, ROI, ratios, margins | financial, 재무, 파이낸셜 |
| `171` | Technical — RSI, SMA20/50/200, 52W High/Low, pattern, candlestick, beta, ATR | technical, 테크니컬, 차트지표 |

---


## Sort Order 코드


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ticker` | Ticker A→Z | ticker, 티커 |
| `-ticker` | Ticker Z→A |  |
| `company` | Company name A→Z | company, 회사명 |
| `sector` | Sector | sector, 섹터 |
| `industry` | Industry | industry, 업종 |
| `country` | Country | country, 국가 |
| `marketcap` | Market Cap (ascending) | market cap, 시가총액, 작은순 |
| `-marketcap` | Market Cap (descending) | 시가총액 큰순 |
| `pe` | P/E (ascending) | PE, PER |
| `-pe` | P/E (descending) |  |
| `forwardpe` | Forward P/E (ascending) | forward PE |
| `eps` | EPS (ascending) | EPS |
| `dividendyield` | Dividend Yield (ascending) | dividend, 배당, 수익률 |
| `-dividendyield` | Dividend Yield (descending) | 고배당순 |
| `price` | Price (ascending) | price, 주가 |
| `-price` | Price (descending) |  |
| `change` | Change (ascending) | change, 변동률 |
| `-change` | Change (descending) |  |
| `volume` | Volume (ascending) | volume, 거래량 |
| `-volume` | Volume (descending) | 거래량 큰순 |
| `recom` | Analyst Recommendation | recommendation, 애널리스트 추천 |
| `earningsdate` | Earnings Date | earnings date, 결산일 |
| `targetprice` | Target Price | target price, 목표주가 |
| `shortfloat` | Short Float | short float |
| `averagevolume` | Average Volume | average volume |
| `relativevolume` | Relative Volume | relative volume |

---


## 설명형 필터


### 거래소 (`exch_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `exch_amex` | AMEX | AMEX |
| `exch_cboe` | CBOE | CBOE |
| `exch_nasd` | NASDAQ | NASDAQ, 나스닥 |
| `exch_nyse` | NYSE | NYSE, 뉴욕증권거래소 |

### 지수 (`idx_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `idx_sp500` | S&P 500 | S&P 500, S&P500 |
| `idx_dji` | Dow Jones | Dow, 다우, 다우산업 |
| `idx_ndx` | NASDAQ 100 | NASDAQ 100, 나스닥100 |
| `idx_rut` | Russell 2000 | Russell 2000, 러셀2000, 소형주지수 |

### 섹터 (`sec_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sec_basicmaterials` | Basic Materials | basic materials, 소재, 원자재 |
| `sec_communicationservices` | Communication Services | communication, 통신, 미디어 |
| `sec_consumercyclical` | Consumer Cyclical | consumer cyclical, 일반소비재, 경기민감소비 |
| `sec_consumerdefensive` | Consumer Defensive | consumer defensive, 필수소비재, 방어적소비 |
| `sec_energy` | Energy | energy, 에너지, 석유 |
| `sec_financial` | Financial | financial, 금융, 은행 |
| `sec_healthcare` | Healthcare | healthcare, 헬스케어, 의료 |
| `sec_industrials` | Industrials | industrials, 자본재, 산업 |
| `sec_realestate` | Real Estate | real estate, 부동산, REIT |
| `sec_technology` | Technology | technology, 테크놀로지, 하이테크, IT |
| `sec_utilities` | Utilities | utilities, 유틸리티, 전력, 가스 |

### 시가총액 (`cap_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `cap_mega` | Mega ($200B+) | mega cap, 메가캡, 초대형 |
| `cap_large` | Large ($10B–$200B) | large cap, 라지캡, 대형 |
| `cap_mid` | Mid ($2B–$10B) | mid cap, 미드캡, 중형 |
| `cap_small` | Small ($300M–$2B) | small cap, 스몰캡, 소형 |
| `cap_micro` | Micro ($50M–$300M) | micro cap, 마이크로캡, 초소형 |
| `cap_nano` | Nano (under $50M) | nano cap, 나노캡 |
| `cap_largeover` | +Large ($10B+) | large+, 대형이상 |
| `cap_midover` | +Mid ($2B+) | mid+, 중형이상 |
| `cap_smallover` | +Small ($300M+) | small+, 소형이상 |
| `cap_microover` | +Micro ($50M+) | micro+, 초소형이상 |
| `cap_largeunder` | -Large (under $200B) | large이하 |
| `cap_midunder` | -Mid (under $10B) | mid이하 |
| `cap_smallunder` | -Small (under $2B) | small이하 |
| `cap_microunder` | -Micro (under $300M) | micro이하 |

### 국가 (`geo_`)


주요 국가:


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `geo_usa` | USA | USA, 미국 |
| `geo_notusa` | Foreign (ex-USA) | foreign, 외국, 해외, ADR |
| `geo_asia` | Asia | Asia, 아시아 |
| `geo_europe` | Europe | Europe, 유럽 |
| `geo_latinamerica` | Latin America | Latin America, 중남미 |
| `geo_bric` | BRIC | BRIC |
| `geo_china` | China | China, 중국 |
| `geo_chinahongkong` | China & Hong Kong |  |
| `geo_japan` | Japan | Japan, 일본 |
| `geo_india` | India | India, 인도 |
| `geo_unitedkingdom` | United Kingdom | UK, 영국 |
| `geo_canada` | Canada | Canada, 캐나다 |
| `geo_germany` | Germany | Germany, 독일 |
| `geo_france` | France | France, 프랑스 |
| `geo_brazil` | Brazil | Brazil, 브라질 |
| `geo_southkorea` | South Korea | South Korea, 한국 |
| `geo_taiwan` | Taiwan | Taiwan, 대만 |
| `geo_israel` | Israel | Israel, 이스라엘 |
| `geo_australia` | Australia | Australia, 호주 |
| `geo_switzerland` | Switzerland | Switzerland, 스위스 |
| `geo_netherlands` | Netherlands | Netherlands, 네덜란드 |
| `geo_ireland` | Ireland | Ireland, 아일랜드 |
| `geo_singapore` | Singapore | Singapore, 싱가포르 |

추가 국가: Argentina, Bahamas, Belgium, BeNeLux, Bermuda, Cayman Islands, Chile, Colombia, Cyprus, Denmark, Finland, Greece, Hong Kong, Hungary, Iceland, Indonesia, Italy, Jordan, Kazakhstan, Luxembourg, Malaysia, Malta, Mexico, Monaco, New Zealand, Norway, Panama, Peru, Philippines, Portugal, Russia, South Africa, Spain, Sweden, Thailand, Turkey, UAE, Uruguay, Vietnam


### IPO 날짜 (`ipodate_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ipodate_today` | Today | IPO today, 오늘IPO |
| `ipodate_yesterday` | Yesterday |  |
| `ipodate_prevweek` | In the last week | recent IPO, 최근IPO |
| `ipodate_prevmonth` | In the last month |  |
| `ipodate_prevquarter` | In the last quarter |  |
| `ipodate_prevyear` | In the last year |  |
| `ipodate_prev2yrs` | In the last 2 years |  |
| `ipodate_prev3yrs` | In the last 3 years |  |
| `ipodate_prev5yrs` | In the last 5 years |  |
| `ipodate_more1` | More than a year ago |  |
| `ipodate_more5` | More than 5 years ago | established, 안정기업 |
| `ipodate_more10` | More than 10 years ago |  |
| `ipodate_more15` | More than 15 years ago |  |
| `ipodate_more20` | More than 20 years ago |  |
| `ipodate_more25` | More than 25 years ago |  |

### Earnings 날짜 (`earningsdate_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `earningsdate_today` | Today | earnings today, 오늘결산 |
| `earningsdate_todaybefore` | Today Before Market Open | 시가전결산 |
| `earningsdate_todayafter` | Today After Market Close | 마감후결산 |
| `earningsdate_tomorrow` | Tomorrow | earnings tomorrow, 내일결산 |
| `earningsdate_tomorrowbefore` | Tomorrow Before Market Open |  |
| `earningsdate_tomorrowafter` | Tomorrow After Market Close |  |
| `earningsdate_yesterday` | Yesterday | 어제결산 |
| `earningsdate_yesterdaybefore` | Yesterday Before Market Open |  |
| `earningsdate_yesterdayafter` | Yesterday After Market Close |  |
| `earningsdate_thisweek` | This Week | earnings this week, 이번주결산 |
| `earningsdate_nextweek` | Next Week | earnings next week, 다음주결산 |
| `earningsdate_prevweek` | Previous Week | 지난주결산 |
| `earningsdate_nextdays5` | Next 5 Days | 향후5일이내결산 |
| `earningsdate_prevdays5` | Previous 5 Days | 과거5일결산 |
| `earningsdate_thismonth` | This Month | earnings this month, 이번달결산 |

---


## Fundamental 필터 (`fa_`)


### P/E 비율 (`fa_pe_`)


패턴: `fa_pe_u{N}` (N 미만), `fa_pe_o{N}` (N 초과)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_pe_low` | Low (<15) | low PE, 저PER |
| `fa_pe_profitable` | Profitable (>0) | profitable, 흑자 |
| `fa_pe_high` | High (>50) | high PE, 고PER |
| `fa_pe_u5` | Under 5 | PE<5 |
| `fa_pe_u10` | Under 10 | PE<10 |
| `fa_pe_u15` | Under 15 | PE<15 |
| `fa_pe_u20` | Under 20 | PE<20, 저평가 |
| `fa_pe_u25` | Under 25 | PE<25 |
| `fa_pe_u30` | Under 30 | PE<30 |
| `fa_pe_u35` | Under 35 |  |
| `fa_pe_u40` | Under 40 | PE<40 |
| `fa_pe_u45` | Under 45 |  |
| `fa_pe_u50` | Under 50 | PE<50 |
| `fa_pe_o5` | Over 5 | PE>5 |
| `fa_pe_o10` | Over 10 | PE>10 |
| `fa_pe_o15` | Over 15 | PE>15 |
| `fa_pe_o20` | Over 20 | PE>20 |
| `fa_pe_o25` | Over 25 | PE>25 |
| `fa_pe_o30` | Over 30 | PE>30 |
| `fa_pe_o35` | Over 35 |  |
| `fa_pe_o40` | Over 40 | PE>40 |
| `fa_pe_o45` | Over 45 |  |
| `fa_pe_o50` | Over 50 | PE>50 |

### Forward P/E (`fa_fpe_`)


패턴: `fa_fpe_u{N}` (N 미만), `fa_fpe_o{N}` (N 초과). 임계값은 P/E와 동일(5–50)합니다.

특수값: `fa_fpe_low` (Low <15), `fa_fpe_profitable` (>0), `fa_fpe_high` (>50)


### PEG 비율 (`fa_peg_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_peg_low` | Low (<1) | PEG<1, 성장저평가 |
| `fa_peg_high` | High (>2) | PEG>2 |
| `fa_peg_u1` | Under 1 | PEG<1 |
| `fa_peg_u2` | Under 2 | PEG<2 |
| `fa_peg_u3` | Under 3 | PEG<3 |
| `fa_peg_o1` | Over 1 | PEG>1 |
| `fa_peg_o2` | Over 2 | PEG>2 |
| `fa_peg_o3` | Over 3 | PEG>3 |

### P/S 비율 (`fa_ps_`)


패턴: `fa_ps_u{N}` (N 미만), `fa_ps_o{N}` (N 초과). 범위: 1–10.

특수값: `fa_ps_low` (Low <1), `fa_ps_high` (High >10)


### P/B 비율 (`fa_pb_`)


패턴: `fa_pb_u{N}` (N 미만), `fa_pb_o{N}` (N 초과). 범위: 1–10.

특수값: `fa_pb_low` (Low <1, 장부가이하), `fa_pb_high` (High >5)


### P/Cash (`fa_pc_`)


패턴: `fa_pc_u{N}` (N 미만), `fa_pc_o{N}` (N 초과). 범위: 1–50.

특수값: `fa_pc_low` (Low <3), `fa_pc_high` (High >50)


### P/Free Cash Flow (`fa_pfcf_`)


패턴: `fa_pfcf_u{N}` (N 미만), `fa_pfcf_o{N}` (N 초과). 범위: 5–100.

특수값: `fa_pfcf_low` (Low <15, FCF저평가), `fa_pfcf_high` (High >50)


### EV/EBITDA (`fa_evebitda_`)


패턴: `fa_evebitda_u{N}` (N 미만), `fa_evebitda_o{N}` (N 초과). 범위: 5–50.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_evebitda_negative` | Negative (<0) | EV/EBITDA negative |
| `fa_evebitda_low` | Low (<15) | low EV/EBITDA, EV/EBITDA저평가 |
| `fa_evebitda_profitable` | Profitable (>0) | EV/EBITDA profitable |
| `fa_evebitda_high` | High (>50) | high EV/EBITDA |
| `fa_evebitda_u5` | Under 5 | EV/EBITDA<5 |
| `fa_evebitda_u10` | Under 10 | EV/EBITDA<10 |
| `fa_evebitda_u15` | Under 15 | EV/EBITDA<15 |
| `fa_evebitda_u20` | Under 20 | EV/EBITDA<20 |
| `fa_evebitda_u25` | Under 25 |  |
| `fa_evebitda_u30` | Under 30 |  |
| `fa_evebitda_u35` | Under 35 |  |
| `fa_evebitda_u40` | Under 40 |  |
| `fa_evebitda_u45` | Under 45 |  |
| `fa_evebitda_u50` | Under 50 |  |
| `fa_evebitda_o5` | Over 5 |  |
| `fa_evebitda_o10` | Over 10 |  |
| `fa_evebitda_o15` | Over 15 |  |
| `fa_evebitda_o20` | Over 20 |  |
| `fa_evebitda_o25` | Over 25 |  |
| `fa_evebitda_o30` | Over 30 |  |
| `fa_evebitda_o35` | Over 35 |  |
| `fa_evebitda_o40` | Over 40 |  |
| `fa_evebitda_o45` | Over 45 |  |
| `fa_evebitda_o50` | Over 50 |  |

### EV/Sales (`fa_evsales_`)


패턴: `fa_evsales_u{N}` (N 미만), `fa_evsales_o{N}` (N 초과). 범위: 1–10.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_evsales_negative` | Negative (<0) | EV/Sales negative |
| `fa_evsales_low` | Low (<1) | low EV/Sales |
| `fa_evsales_positive` | Positive (>0) | EV/Sales positive |
| `fa_evsales_high` | High (>10) | high EV/Sales |
| `fa_evsales_u1` | Under 1 | EV/Sales<1 |
| `fa_evsales_u2` | Under 2 | EV/Sales<2 |
| `fa_evsales_u3` | Under 3 |  |
| `fa_evsales_u5` | Under 5 |  |
| `fa_evsales_u10` | Under 10 |  |
| `fa_evsales_o1` | Over 1 |  |
| `fa_evsales_o2` | Over 2 |  |
| `fa_evsales_o3` | Over 3 |  |
| `fa_evsales_o5` | Over 5 |  |
| `fa_evsales_o10` | Over 10 |  |

### 배당 수익률 (`fa_div_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_div_none` | None (0%) | no dividend, 무배당 |
| `fa_div_pos` | Positive (>0%) | has dividend, 배당있음 |
| `fa_div_high` | High (>5%) | high dividend, 고배당 |
| `fa_div_veryhigh` | Very High (>10%) | very high dividend, 초고배당 |
| `fa_div_o1` | Over 1% | 배당1%이상 |
| `fa_div_o2` | Over 2% | 배당2%이상 |
| `fa_div_o3` | Over 3% | 배당3%이상 |
| `fa_div_o4` | Over 4% | 배당4%이상 |
| `fa_div_o5` | Over 5% | 배당5%이상 |
| `fa_div_o6` | Over 6% | 배당6%이상 |
| `fa_div_o7` | Over 7% | 배당7%이상 |
| `fa_div_o8` | Over 8% | 배당8%이상 |
| `fa_div_o9` | Over 9% | 배당9%이상 |
| `fa_div_o10` | Over 10% | 배당10%이상 |

### 배당 성장 (`fa_divgrowth_`)


패턴: `fa_divgrowth_{period}o{N}` (period = `1y`/`3y`/`5y`, N = 5/10/15/20/25/30).

양수 조건: `fa_divgrowth_{period}pos`. 연속 증가: `fa_divgrowth_cy{N}` (N = 1–9 years).


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_divgrowth_1ypos` | 1 Year Positive | 1Y배당증배 |
| `fa_divgrowth_1yo5` | 1 Year Over 5% | 1Y DG>5% |
| `fa_divgrowth_1yo10` | 1 Year Over 10% | 1Y DG>10% |
| `fa_divgrowth_3ypos` | 3 Years Positive | 3Y배당증배 |
| `fa_divgrowth_3yo10` | 3 Years Over 10% | 3Y DG>10% |
| `fa_divgrowth_5ypos` | 5 Years Positive | 5Y배당증배 |
| `fa_divgrowth_5yo10` | 5 Years Over 10% | 5Y DG>10% |
| `fa_divgrowth_cy1` | Growing 1+ Year | 1년이상연속증배 |
| `fa_divgrowth_cy3` | Growing 3+ Years | 3년이상연속증배 |
| `fa_divgrowth_cy5` | Growing 5+ Years | 5년이상연속증배, 연속증배주 |
| `fa_divgrowth_cy7` | Growing 7+ Years | 7년이상연속증배 |
| `fa_divgrowth_cy9` | Growing 9+ Years | 9년이상연속증배 |

### Payout Ratio (`fa_payoutratio_`)


패턴: `fa_payoutratio_u{N}` (N% 미만), `fa_payoutratio_o{N}` (N% 초과). 범위: 0–100.

특수값: `fa_payoutratio_none` (0%), `fa_payoutratio_pos` (>0%), `fa_payoutratio_low` (<20%), `fa_payoutratio_high` (>50%)


### EPS 성장


모든 EPS 성장 필터는 동일한 패턴을 따릅니다: `neg` (negative), `pos` (positive), `poslow` (0-10%), `high` (>25%), `o{N}` (N% 초과), `u{N}` (N% 미만). N = 5/10/15/20/25/30.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_epsqoq_*` | EPS Growth Q/Q | EPS QoQ, 분기EPS성장, 증익 |
| `fa_epsyoy_*` | EPS Growth This Year | EPS this year, 올해EPS성장 |
| `fa_epsyoy1_*` | EPS Growth Next Year | EPS next year, 내년EPS성장예상 |
| `fa_epsyoyttm_*` | EPS Growth TTM | EPS TTM, 최근12개월EPS성장 |
| `fa_eps3years_*` | EPS Growth Past 3 Years | 3Y EPS성장 |
| `fa_eps5years_*` | EPS Growth Past 5 Years | 5Y EPS성장 |
| `fa_estltgrowth_*` | EPS Growth Next 5 Years | 5Y EPS성장예상, 장기성장 |

**예시 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_epsqoq_pos` | EPS Q/Q Positive | 증익 |
| `fa_epsqoq_o25` | EPS Q/Q Over 25% | 고성장주 |
| `fa_epsyoy_high` | EPS This Year High (>25%) |  |
| `fa_epsyoy1_pos` | EPS Next Year Positive | 내년증익예상 |
| `fa_epsyoyttm_o10` | EPS TTM Over 10% |  |
| `fa_eps3years_pos` | EPS Past 3Y Positive |  |
| `fa_eps5years_o20` | EPS Past 5Y Over 20% |  |
| `fa_estltgrowth_o15` | EPS Next 5Y Over 15% | 장기고성장 |

### 매출 성장


EPS 성장과 동일한 패턴: `neg`, `pos`, `poslow`, `high`, `o{N}`, `u{N}`.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_salesqoq_*` | Sales Growth Q/Q | 매출QoQ, 증수 |
| `fa_salesyoyttm_*` | Sales Growth TTM | 매출TTM, 최근12개월매출성장 |
| `fa_sales3years_*` | Sales Growth Past 3 Years | 3Y매출성장 |
| `fa_sales5years_*` | Sales Growth Past 5 Years | 5Y매출성장 |

**예시 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_salesqoq_pos` | Sales Q/Q Positive | 증수 |
| `fa_salesqoq_o25` | Sales Q/Q Over 25% | 고성장 |
| `fa_salesyoyttm_o10` | Sales TTM Over 10% |  |
| `fa_sales3years_high` | Sales Past 3Y High (>25%) |  |
| `fa_sales5years_pos` | Sales Past 5Y Positive |  |

### Earnings & Revenue 서프라이즈 (`fa_epsrev_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_epsrev_bp` | Both Positive (>0%) | positive surprise, 긍정적서프라이즈, 실적호조 |
| `fa_epsrev_bm` | Both Met (0%) | met estimates, 예상부합 |
| `fa_epsrev_bn` | Both Negative (<0%) | negative surprise, 부정적서프라이즈, 실적부진 |

### 수익성 — ROE, ROA, ROIC


모든 수익률 지표는 패턴을 따릅니다: `pos` (>0%), `neg` (<0%), `o{N}` (N% 초과), `u-{N}` (-N% 미만).

특수 라벨: `verypos` (ROE >30%, ROA >15%, ROIC >25%), `veryneg` (ROE <-15%, ROA <-15%, ROIC <-10%)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_roe_*` | Return on Equity | ROE, 자기자본이익률 |
| `fa_roa_*` | Return on Assets | ROA, 총자산이익률 |
| `fa_roi_*` | Return on Invested Capital (ROIC) | ROI, ROIC, 투하자본이익률 |

**예시 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_roe_o15` | ROE Over 15% | ROE>15%, 고수익 |
| `fa_roe_o30` | ROE Over 30% | ROE>30% |
| `fa_roa_o10` | ROA Over 10% | ROA>10% |
| `fa_roi_o20` | ROIC Over 20% | ROIC>20% |
| `fa_roi_verypos` | ROIC Very Positive (>25%) | 고ROIC |

### 마진


패턴: `pos` (>0%), `neg` (<0%), `high` (gross >50%, operating >25%, net >20%), `veryneg` (<-20%), `o{N}` (N% 초과), `u{N}` (N% 미만), `u-{N}` (-N% 미만).

N 범위: 0–90 (5-point 간격).


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_grossmargin_*` | Gross Margin | gross margin, 매출총이익률 |
| `fa_opermargin_*` | Operating Margin | operating margin, 영업이익률 |
| `fa_netmargin_*` | Net Profit Margin | net margin, 순이익률 |

**예시 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_grossmargin_o50` | Gross Margin Over 50% | 고매출총이익 |
| `fa_opermargin_o20` | Operating Margin Over 20% | 고영업이익률 |
| `fa_netmargin_pos` | Net Margin Positive | 흑자 |
| `fa_netmargin_o10` | Net Margin Over 10% |  |
| `fa_grossmargin_u-10` | Gross Margin Under -10% | 적자 |

### 부채 및 유동성


**LT Debt/Equity** (`fa_ltdebteq_`): `u{N}` / `o{N}`, N = 0.1–1.0. 특수값: `low` (<0.1), `high` (>0.5)

**Total Debt/Equity** (`fa_debteq_`): 동일 패턴. 특수값: `low` (<0.1), `high` (>0.5)

**Current Ratio** (`fa_curratio_`): `u{N}` / `o{N}`, N = 0.5–10. 특수값: `low` (<1), `high` (>3)

**Quick Ratio** (`fa_quickratio_`): `u{N}` / `o{N}`, N = 0.5–10. 특수값: `low` (<0.5), `high` (>3)


**예시 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `fa_ltdebteq_u0.5` | LT D/E Under 0.5 | 저부채 |
| `fa_debteq_low` | Total D/E Low (<0.1) | 초저부채 |
| `fa_curratio_o2` | Current Ratio Over 2 | 고유동성 |
| `fa_quickratio_o1` | Quick Ratio Over 1 |  |

---


## Technical 필터 (`ta_`)


### RSI 14일 (`ta_rsi_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_rsi_ob90` | Overbought (90) | extremely overbought, 극과열 |
| `ta_rsi_ob80` | Overbought (80) | overbought, 과열 |
| `ta_rsi_ob70` | Overbought (70) | overbought, 과매수 |
| `ta_rsi_ob60` | Overbought (60) |  |
| `ta_rsi_os40` | Oversold (40) | slightly oversold |
| `ta_rsi_os30` | Oversold (30) | oversold, 과매도 |
| `ta_rsi_os20` | Oversold (20) | deeply oversold, 심한과매도 |
| `ta_rsi_os10` | Oversold (10) | extremely oversold |
| `ta_rsi_nob60` | Not Overbought (<60) |  |
| `ta_rsi_nob50` | Not Overbought (<50) |  |
| `ta_rsi_nos40` | Not Oversold (>40) |  |
| `ta_rsi_nos50` | Not Oversold (>50) |  |

### 이동평균 (`ta_sma20_`, `ta_sma50_`, `ta_sma200_`)


각 SMA는 다음 옵션을 가집니다:

- `pa` / `pb` — Price above/below SMA

- `pa{N}` / `pb{N}` — Price N% above/below SMA (N = 10,20,30,40,50 for SMA20/50; up to 100 for SMA200)

- `pc` / `pca` / `pcb` — Price crossed / crossed above / crossed below SMA

- `sa{X}` / `sb{X}` — SMA above/below other SMA (X = 20,50,200)

- `cross{X}` / `cross{X}a` / `cross{X}b` — SMA crossed / crossed above / crossed below other SMA


**주요 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_sma20_pa` | Price Above SMA20 | above 20MA, 20일선위 |
| `ta_sma20_pb` | Price Below SMA20 | below 20MA, 20일선아래 |
| `ta_sma20_pca` | Price Crossed Above SMA20 | break above 20MA, 20일선돌파 |
| `ta_sma20_pcb` | Price Crossed Below SMA20 | break below 20MA, 20일선이탈 |
| `ta_sma50_pa` | Price Above SMA50 | above 50MA, 50일선위 |
| `ta_sma50_pb` | Price Below SMA50 | below 50MA, 50일선아래 |
| `ta_sma50_pca` | Price Crossed Above SMA50 | break above 50MA, 50일선돌파 |
| `ta_sma50_pcb` | Price Crossed Below SMA50 | break below 50MA, 50일선이탈 |
| `ta_sma200_pa` | Price Above SMA200 | above 200MA, 200일선위, 장기상승 |
| `ta_sma200_pb` | Price Below SMA200 | below 200MA, 200일선아래, 장기하락 |
| `ta_sma200_pca` | Price Crossed Above SMA200 | break above 200MA, 골든크로스 |
| `ta_sma200_pcb` | Price Crossed Below SMA200 | break below 200MA, 데드크로스 |
| `ta_sma200_sa50` | SMA200 Above SMA50 | death cross, 데드크로스배치 |
| `ta_sma200_sb50` | SMA200 Below SMA50 | golden cross, 골든크로스배치 |
| `ta_sma50_cross200a` | SMA50 Crossed SMA200 Above | 골든크로스발생 |
| `ta_sma50_cross200b` | SMA50 Crossed SMA200 Below | 데드크로스발생 |

### 당일 변동 (`ta_change_`)


당일 가격 변동. 패턴: `ta_change_u{N}` (N% 상승), `ta_change_d{N}` (N% 하락). N = 1–20.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_change_u` | Up | 오늘상승 |
| `ta_change_d` | Down | 오늘하락 |
| `ta_change_u1` | Up 1% |  |
| `ta_change_u5` | Up 5% | 오늘대폭상승 |
| `ta_change_u10` | Up 10% | 오늘급등 |
| `ta_change_u15` | Up 15% |  |
| `ta_change_u20` | Up 20% |  |
| `ta_change_d1` | Down 1% |  |
| `ta_change_d5` | Down 5% | 오늘대폭하락 |
| `ta_change_d10` | Down 10% | 오늘급락 |
| `ta_change_d15` | Down 15% |  |
| `ta_change_d20` | Down 20% |  |

### 시가 대비 변동 (`ta_changeopen_`)


Change와 동일한 패턴: `ta_changeopen_u{N}` / `ta_changeopen_d{N}`. N = 1–20.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_changeopen_u` | Up from Open | 시가대비상승 |
| `ta_changeopen_d` | Down from Open | 시가대비하락 |
| `ta_changeopen_u5` | Up 5% from Open |  |
| `ta_changeopen_d5` | Down 5% from Open |  |

### 52주 고가/저가 (`ta_highlow52w_`)


패턴: `nh` (new high), `nl` (new low), `b{range}h` (고가 대비 아래), `a{range}h` (저가 대비 위)

고가 대비 범위: `0to3`, `0to5`, `0to10`, `5`, `10`, `15`, `20`, `30`, `40`, `50`, `60`, `70`, `80`, `90`

저가 대비 범위: 동일 패턴


**주요 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_highlow52w_nh` | New High | 52-week high, 52주고가, 신고가 |
| `ta_highlow52w_nl` | New Low | 52-week low, 52주저가, 신저가 |
| `ta_highlow52w_b0to3h` | 0-3% Below High | near high, 고가부근 |
| `ta_highlow52w_b0to5h` | 0-5% Below High | near high |
| `ta_highlow52w_b0to10h` | 0-10% Below High | close to high |
| `ta_highlow52w_b10h` | 10%+ Below High | pullback, 조정중 |
| `ta_highlow52w_b20h` | 20%+ Below High | correction, 조정국면 |
| `ta_highlow52w_b30h` | 30%+ Below High | deep correction |
| `ta_highlow52w_b50h` | 50%+ Below High | bear territory, 폭락 |
| `ta_highlow52w_a0to3h` | 0-3% Above Low | near low, 저가부근 |
| `ta_highlow52w_a0to5h` | 0-5% Above Low | near low |
| `ta_highlow52w_a20h` | 20%+ Above Low | recovering |
| `ta_highlow52w_a50h` | 50%+ Above Low | strong recovery |
| `ta_highlow52w_a100h` | 100%+ Above Low | doubled from low |

### 20일 고가/저가 (`ta_highlow20d_`)


52-Week와 동일 패턴: `nh`, `nl`, `b{range}h` (고가 대비 아래), `a{range}h` (저가 대비 위).

범위: `0to3`, `0to5`, `0to10`, `5`, `10`, `15`, `20`, `30`, `40`, `50`.


**주요 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_highlow20d_nh` | 20-Day New High | 20일신고가 |
| `ta_highlow20d_nl` | 20-Day New Low | 20일신저가 |
| `ta_highlow20d_b0to5h` | 0-5% Below 20D High | 20일고가부근 |

### 50일 고가/저가 (`ta_highlow50d_`)


20-Day High/Low와 동일 패턴. `nh`, `nl`, `b{range}h`, `a{range}h`.


**주요 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_highlow50d_nh` | 50-Day New High | 50일신고가 |
| `ta_highlow50d_nl` | 50-Day New Low | 50일신저가 |

### 사상 최고가/최저가 (`ta_alltime_`)


52-Week High/Low와 동일 구조. 저가 대비 최대 500% 범위까지 지원합니다.


**주요 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_alltime_nh` | All-Time High | all-time high, 사상최고가, ATH |
| `ta_alltime_nl` | All-Time Low | all-time low, 사상최저가 |
| `ta_alltime_b0to3h` | 0-3% Below ATH | ATH부근 |
| `ta_alltime_b0to5h` | 0-5% Below ATH | ATH부근 |
| `ta_alltime_b10h` | 10%+ Below ATH | ATH대비10%하락 |
| `ta_alltime_b20h` | 20%+ Below ATH | ATH대비20%하락 |
| `ta_alltime_b50h` | 50%+ Below ATH | ATH대비반값 |

### 수익률 (`ta_perf_`)


패턴: `ta_perf_{period}{direction}{threshold}`

기간: `d` (today), `1w` (week), `4w` (month), `13w` (quarter), `26w` (half), `52w` (year), `ytd` (YTD), `3y`, `5y`, `10y`

방향: `up`/`down` (any), `{N}o` (+N%), `{N}u` (-N%)


**주요 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_perf_dup` | Today Up | today up, 오늘상승 |
| `ta_perf_ddown` | Today Down | today down, 오늘하락 |
| `ta_perf_d5o` | Today +5% | big up today |
| `ta_perf_d5u` | Today -5% | big down today |
| `ta_perf_1wup` | Week Up | week up, 주간상승 |
| `ta_perf_1wdown` | Week Down | week down, 주간하락 |
| `ta_perf_4wup` | Month Up | month up, 월간상승 |
| `ta_perf_4wdown` | Month Down | month down, 월간하락 |
| `ta_perf_13wup` | Quarter Up | quarter up, 분기상승 |
| `ta_perf_13wdown` | Quarter Down | quarter down |
| `ta_perf_26wup` | Half Year Up | half up, 반기상승 |
| `ta_perf_52wup` | Year Up | year up, 연간상승 |
| `ta_perf_52wdown` | Year Down | year down, 연간하락 |
| `ta_perf_ytdup` | YTD Up | YTD up, 연초대비상승 |
| `ta_perf_ytddown` | YTD Down | YTD down, 연초대비하락 |
| `ta_perf_3yup` | 3 Years Up | 3Y up |
| `ta_perf_5yup` | 5 Years Up | 5Y up |
| `ta_perf_10yup` | 10 Years Up | 10Y up |
| `ta_perf_52w100o` | Year +100% | 연간2배 |
| `ta_perf_52w50u` | Year -50% | 연간반값 |

### 수익률 2 (`ta_perf2_`)


Performance와 구조는 동일하지만 두 번째 독립 성과 필터를 허용합니다.

prefix는 `ta_perf_` 대신 `ta_perf2_`를 사용합니다. 기간/임계값은 동일합니다.

사용 예: 이번 분기 상승 AND 이번 달 하락 종목 동시 필터링.


### 갭 (`ta_gap_`)


패턴: `ta_gap_u{N}` (N% gap up), `ta_gap_d{N}` (N% gap down). N = 0–20.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_gap_u` | Gap Up | gap up, 갭업 |
| `ta_gap_d` | Gap Down | gap down, 갭다운 |
| `ta_gap_u0` | Gap Up 0%+ |  |
| `ta_gap_u3` | Gap Up 3%+ |  |
| `ta_gap_u5` | Gap Up 5%+ | big gap up |
| `ta_gap_u10` | Gap Up 10%+ |  |
| `ta_gap_d0` | Gap Down 0%+ |  |
| `ta_gap_d3` | Gap Down 3%+ |  |
| `ta_gap_d5` | Gap Down 5%+ | big gap down |
| `ta_gap_d10` | Gap Down 10%+ |  |

### Beta (`ta_beta_`)


패턴: `ta_beta_u{N}` (N 미만), `ta_beta_o{N}` (N 초과). 추가 범위: `0to0.5`, `0to1`, `0.5to1`, `0.5to1.5`, `1to1.5`, `1to2`.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_beta_u0` | Beta Under 0 | negative beta |
| `ta_beta_u0.5` | Beta Under 0.5 | low beta, 저베타, 방어적 |
| `ta_beta_u1` | Beta Under 1 | below market |
| `ta_beta_o1` | Beta Over 1 | above market |
| `ta_beta_o1.5` | Beta Over 1.5 | high beta, 고베타 |
| `ta_beta_o2` | Beta Over 2 | very high beta |
| `ta_beta_o3` | Beta Over 3 | extremely high beta |

### 변동성 (`ta_volatility_`)


패턴: `ta_volatility_{period}_{direction}{N}` (period = w/week 또는 m/month, N = 2–15).


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_volatility_mo10` | Month - Over 10% |  |
| `ta_volatility_mo12` | Month - Over 12% |  |
| `ta_volatility_mo15` | Month - Over 15% |  |
| `ta_volatility_mo2` | Month - Over 2% |  |
| `ta_volatility_mo3` | Month - Over 3% |  |
| `ta_volatility_mo4` | Month - Over 4% |  |
| `ta_volatility_mo5` | Month - Over 5% |  |
| `ta_volatility_mo6` | Month - Over 6% |  |
| `ta_volatility_mo7` | Month - Over 7% |  |
| `ta_volatility_mo8` | Month - Over 8% |  |
| `ta_volatility_mo9` | Month - Over 9% |  |
| `ta_volatility_wo10` | Week - Over 10% |  |
| `ta_volatility_wo12` | Week - Over 12% |  |
| `ta_volatility_wo15` | Week - Over 15% |  |
| `ta_volatility_wo2` | Week - Over 2% |  |
| `ta_volatility_wo3` | Week - Over 3% |  |
| `ta_volatility_wo4` | Week - Over 4% |  |
| `ta_volatility_wo5` | Week - Over 5% |  |
| `ta_volatility_wo6` | Week - Over 6% |  |
| `ta_volatility_wo7` | Week - Over 7% |  |
| `ta_volatility_wo8` | Week - Over 8% |  |
| `ta_volatility_wo9` | Week - Over 9% |  |

### Average True Range (`ta_averagetruerange_`)


패턴: `ta_averagetruerange_o{N}` (N 초과), `ta_averagetruerange_u{N}` (N 미만). N = 0.25–5.0.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_averagetruerange_o0.5` | ATR Over 0.5 | ATR>0.5 |
| `ta_averagetruerange_o1` | ATR Over 1 | ATR>1 |
| `ta_averagetruerange_o2` | ATR Over 2 | high ATR, 고ATR |
| `ta_averagetruerange_o3` | ATR Over 3 | very high ATR |
| `ta_averagetruerange_o5` | ATR Over 5 | extreme ATR |
| `ta_averagetruerange_u0.5` | ATR Under 0.5 | low ATR, 저ATR |
| `ta_averagetruerange_u1` | ATR Under 1 |  |
| `ta_averagetruerange_u2` | ATR Under 2 |  |

### 차트 패턴 (`ta_pattern_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_pattern_channel` | Channel |  |
| `ta_pattern_channel2` | Channel (Strong) |  |
| `ta_pattern_channeldown` | Channel Down | falling channel, 하향채널 |
| `ta_pattern_channeldown2` | Channel Down (Strong) |  |
| `ta_pattern_channelup` | Channel Up | rising channel, 상승채널 |
| `ta_pattern_channelup2` | Channel Up (Strong) |  |
| `ta_pattern_doublebottom` | Double Bottom | double bottom, 이중바닥 |
| `ta_pattern_doubletop` | Double Top | double top, 이중천장 |
| `ta_pattern_headandshoulders` | Head & Shoulders | H&S, 헤드앤숄더 |
| `ta_pattern_headandshouldersinv` | Head & Shoulders Inverse | inverse H&S, 역H&S |
| `ta_pattern_horizontal` | Horizontal S/R | horizontal channel, 레인지 |
| `ta_pattern_horizontal2` | Horizontal S/R (Strong) |  |
| `ta_pattern_multiplebottom` | Multiple Bottom | multiple bottom |
| `ta_pattern_multipletop` | Multiple Top | multiple top |
| `ta_pattern_tlresistance` | TL Resistance |  |
| `ta_pattern_tlresistance2` | TL Resistance (Strong) |  |
| `ta_pattern_tlsupport` | TL Support |  |
| `ta_pattern_tlsupport2` | TL Support (Strong) |  |
| `ta_pattern_wedge` | Wedge |  |
| `ta_pattern_wedge2` | Wedge (Strong) |  |
| `ta_pattern_wedgedown` | Wedge Down | falling wedge |
| `ta_pattern_wedgedown2` | Wedge Down (Strong) |  |
| `ta_pattern_wedgeresistance` | Triangle Ascending | ascending triangle |
| `ta_pattern_wedgeresistance2` | Triangle Ascending (Strong) |  |
| `ta_pattern_wedgesupport` | Triangle Descending | descending triangle |
| `ta_pattern_wedgesupport2` | Triangle Descending (Strong) |  |
| `ta_pattern_wedgeup` | Wedge Up | rising wedge |
| `ta_pattern_wedgeup2` | Wedge Up (Strong) |  |

### 캔들스틱 (`ta_candlestick_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ta_candlestick_d` | Doji | doji, 십자선 |
| `ta_candlestick_dd` | Dragonfly Doji | dragonfly doji, 잠자리형 |
| `ta_candlestick_gd` | Gravestone Doji | gravestone doji |
| `ta_candlestick_h` | Hammer | hammer, 해머 |
| `ta_candlestick_ih` | Inverted Hammer | inverted hammer |
| `ta_candlestick_lls` | Long Lower Shadow | long lower shadow, 긴아래꼬리 |
| `ta_candlestick_lus` | Long Upper Shadow | long upper shadow, 긴위꼬리 |
| `ta_candlestick_mb` | Marubozu Black | marubozu black, 음봉마루보즈 |
| `ta_candlestick_mw` | Marubozu White | marubozu white, 양봉마루보즈 |
| `ta_candlestick_stb` | Spinning Top Black | spinning top black |
| `ta_candlestick_stw` | Spinning Top White | spinning top white |

---


## 주식 관련 필터 (`sh_`)


### 평균 거래량 (`sh_avgvol_`)


패턴: `sh_avgvol_o{N}` (NK 초과), `sh_avgvol_u{N}` (NK 미만). 추가 범위: `100to500`, `100to1000`, `500to1000`, `500to10000`.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_avgvol_u50` | Under 50K | very low volume |
| `sh_avgvol_u100` | Under 100K | low volume |
| `sh_avgvol_o100` | Over 100K |  |
| `sh_avgvol_o200` | Over 200K | min volume, 유동성확보 |
| `sh_avgvol_o500` | Over 500K |  |
| `sh_avgvol_o1000` | Over 1M | high volume, 고거래량 |
| `sh_avgvol_o2000` | Over 2M | very high volume |
| `sh_avgvol_100to500` | 100K to 500K |  |
| `sh_avgvol_500to1000` | 500K to 1M |  |

### 상대 거래량 (`sh_relvol_`)


패턴: `sh_relvol_o{N}` (N 초과), `sh_relvol_u{N}` (N 미만). N = 0.1–10.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_relvol_u0.5` | Under 0.5 | low relative volume |
| `sh_relvol_u1` | Under 1 | below avg volume |
| `sh_relvol_o1` | Over 1 | above avg volume |
| `sh_relvol_o1.5` | Over 1.5 | elevated volume |
| `sh_relvol_o2` | Over 2 | volume surge, 거래량급증 |
| `sh_relvol_o3` | Over 3 | very high relative vol |
| `sh_relvol_o5` | Over 5 | extreme volume |
| `sh_relvol_o10` | Over 10 | unusual volume, 이상거래량 |

### 현재 거래량 (`sh_curvol_`)


패턴: `sh_curvol_o{N}`. screener UI의 미리 정의된 dropdown 옵션은 없으며 `f=` 파라미터로 사용합니다.


### 가격 (`sh_price_`)


패턴: `sh_price_u{N}` ($N 미만), `sh_price_o{N}` ($N 초과). 추가 범위: `1to5`, `1to10`, `5to10`, `5to20`, `10to20`, `10to50`, `20to50`, `50to100`.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_price_u1` | Under $1 | penny stock, 페니스톡 |
| `sh_price_u5` | Under $5 | low price, 저가 |
| `sh_price_u10` | Under $10 |  |
| `sh_price_u20` | Under $20 |  |
| `sh_price_u50` | Under $50 | mid price |
| `sh_price_o5` | Over $5 |  |
| `sh_price_o10` | Over $10 |  |
| `sh_price_o20` | Over $20 |  |
| `sh_price_o50` | Over $50 |  |
| `sh_price_o100` | Over $100 | expensive, 고가주 |
| `sh_price_5to50` | $5 to $50 |  |
| `sh_price_10to50` | $10 to $50 | 중가대 |

### 유동주식수 (`sh_float_`)


패턴: `sh_float_u{N}` (NM 미만), `sh_float_o{N}` (NM 초과). 퍼센트 패턴: `sh_float_u{N}p` / `sh_float_o{N}p`.


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_float_u1` | Under 1M | very low float |
| `sh_float_u5` | Under 5M | low float, 저유통주 |
| `sh_float_u10` | Under 10M |  |
| `sh_float_u20` | Under 20M |  |
| `sh_float_o50` | Over 50M |  |
| `sh_float_o100` | Over 100M |  |
| `sh_float_o500` | Over 500M | high float |
| `sh_float_o1000` | Over 1000M |  |
| `sh_float_u10p` | Under 10% of Outstanding | very low float % |
| `sh_float_u20p` | Under 20% |  |
| `sh_float_o50p` | Over 50% |  |
| `sh_float_o80p` | Over 80% | high float % |

### 공매도 비중 (`sh_short_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_short_low` | Low (<5%) | low short interest |
| `sh_short_high` | High (>20%) | heavily shorted, 대량공매도 |
| `sh_short_u5` | Under 5% |  |
| `sh_short_u10` | Under 10% |  |
| `sh_short_o5` | Over 5% | some short interest |
| `sh_short_o10` | Over 10% | high short, 숏스퀴즈후보 |
| `sh_short_o15` | Over 15% |  |
| `sh_short_o20` | Over 20% | heavily shorted |
| `sh_short_o25` | Over 25% | very heavily shorted |
| `sh_short_o30` | Over 30% | extreme short interest |

### 발행주식수 (`sh_outstanding_`)


패턴: `sh_outstanding_u{N}` (NM 미만), `sh_outstanding_o{N}` (NM 초과).


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_outstanding_u1` | Under 1M |  |
| `sh_outstanding_u5` | Under 5M |  |
| `sh_outstanding_u10` | Under 10M | very low shares |
| `sh_outstanding_u50` | Under 50M |  |
| `sh_outstanding_u100` | Under 100M |  |
| `sh_outstanding_o10` | Over 10M |  |
| `sh_outstanding_o50` | Over 50M |  |
| `sh_outstanding_o100` | Over 100M |  |
| `sh_outstanding_o200` | Over 200M |  |
| `sh_outstanding_o500` | Over 500M |  |
| `sh_outstanding_o1000` | Over 1000M | high shares outstanding |

### 옵션/공매도 (`sh_opt_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_opt_option` | Optionable | optionable, 옵션거래가능 |
| `sh_opt_short` | Shortable | shortable, 공매도가능 |
| `sh_opt_notoption` | Not Optionable | 옵션불가 |
| `sh_opt_notshort` | Not Shortable | 공매도불가 |
| `sh_opt_optionshort` | Optionable and Shortable | 옵션/공매도 모두가능 |
| `sh_opt_optionnotshort` | Optionable and Not Shortable |  |
| `sh_opt_notoptionshort` | Not Optionable and Shortable |  |
| `sh_opt_notoptionnotshort` | Not Optionable and Not Shortable |  |

### 내부자 보유율 (`sh_insiderown_`)


패턴: `sh_insiderown_o{N}` (N% 초과). 특수값: `low` (<5%), `high` (>30%), `veryhigh` (>50%)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_insiderown_low` | Low (<5%) | low insider |
| `sh_insiderown_high` | High (>30%) | insider owned |
| `sh_insiderown_veryhigh` | Very High (>50%) | majority insider |
| `sh_insiderown_o10` | Over 10% | 내부자보유10%+ |
| `sh_insiderown_o20` | Over 20% |  |
| `sh_insiderown_o30` | Over 30% |  |
| `sh_insiderown_o50` | Over 50% | 과반수내부자 |
| `sh_insiderown_o70` | Over 70% |  |
| `sh_insiderown_o90` | Over 90% |  |

### 내부자 거래 (`sh_insidertrans_`)


패턴: `sh_insidertrans_o{N}` (+N% 초과), `sh_insidertrans_u-{N}` (-N% 미만). N = 5–90.

특수값: `pos` (>0%), `neg` (<0%), `verypos` (>20%), `veryneg` (<20%)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_insidertrans_pos` | Positive (>0%) | insider buying, 내부자매수 |
| `sh_insidertrans_neg` | Negative (<0%) | insider selling, 내부자매도 |
| `sh_insidertrans_verypos` | Very Positive (>20%) | heavy insider buying, 내부자대량매수 |
| `sh_insidertrans_veryneg` | Very Negative (<20%) | heavy insider selling |

### 기관 보유율 (`sh_instown_`)


패턴: `sh_instown_o{N}` (N% 초과), `sh_instown_u{N}` (N% 미만). N = 10–90.

특수값: `low` (<5%), `high` (>90%)


### 기관 거래 (`sh_insttrans_`)


패턴: `sh_insttrans_o{N}` (+N% 초과), `sh_insttrans_u-{N}` (-N% 미만). N = 5–50.

특수값: `pos` (>0%), `neg` (<0%), `verypos` (>20%), `veryneg` (<20%)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `sh_insttrans_pos` | Positive (>0%) | institutional buying, 기관매수 |
| `sh_insttrans_neg` | Negative (<0%) | institutional selling |

---


## 애널리스트 필터 (`an_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `an_recom_strongbuy` | Strong Buy (1) | strong buy, 강력매수추천 |
| `an_recom_buybetter` | Buy or better (1-2) | buy, 매수추천 |
| `an_recom_buy` | Buy (2) |  |
| `an_recom_holdbetter` | Hold or better (1-3) | hold, 보유이상 |
| `an_recom_hold` | Hold (3) |  |
| `an_recom_holdworse` | Hold or worse (3-5) |  |
| `an_recom_sell` | Sell (4) |  |
| `an_recom_sellworse` | Sell or worse (4-5) | sell, 매도추천 |
| `an_recom_strongsell` | Strong Sell (5) | strong sell, 강력매도 |

---


## 목표주가 (`targetprice_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `targetprice_above` | Above Price | target above, 목표주가이상 |
| `targetprice_below` | Below Price | target below, 목표주가이하 |
| `targetprice_a5` | 5% Above Price |  |
| `targetprice_a10` | 10% Above Price |  |
| `targetprice_a20` | 20% Above Price | 저평가, 상승여력 |
| `targetprice_a30` | 30% Above Price |  |
| `targetprice_a40` | 40% Above Price |  |
| `targetprice_a50` | 50% Above Price | 대폭저평가 |
| `targetprice_b5` | 5% Below Price |  |
| `targetprice_b10` | 10% Below Price |  |
| `targetprice_b20` | 20% Below Price |  |
| `targetprice_b30` | 30% Below Price |  |
| `targetprice_b40` | 40% Below Price |  |
| `targetprice_b50` | 50% Below Price | 대폭고평가 |

---


## 최신 뉴스 (`news_date_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `news_date_today` | Today | news today, 오늘뉴스 |
| `news_date_todayafter` | Aftermarket Today |  |
| `news_date_yesterday` | Yesterday |  |
| `news_date_yesterdayafter` | In the Aftermarket Yesterday |  |
| `news_date_sinceyesterday` | Since Yesterday |  |
| `news_date_sinceyesterdayafter` | Since Aftermarket Yesterday |  |
| `news_date_prevminutes5` | In the last 5 minutes | 최근5분 |
| `news_date_prevminutes30` | In the last 30 minutes | 최근30분 |
| `news_date_prevhours1` | In the last hour | 최근1시간 |
| `news_date_prevhours24` | In the last 24 hours | 최근24시간 |
| `news_date_prevdays7` | In the last 7 days | 최근1주일 |
| `news_date_prevmonth` | In the last month | 최근1개월 |

---


## 테마 필터


### 테마 (`theme_`)


| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `theme_agingpopulationlongevity` | Aging Population & Longevity |  |
| `theme_agriculturefoodtech` | Agriculture & FoodTech |  |
| `theme_artificialintelligence` | Artificial Intelligence | AI, 인공지능 |
| `theme_autonomoussystems` | Autonomous Systems | autonomous, 자율시스템 |
| `theme_bigdata` | Big Data | big data, 빅데이터 |
| `theme_biometrics` | Biometrics |  |
| `theme_cloudcomputing` | Cloud Computing | cloud, 클라우드 |
| `theme_commoditiesagriculture` | Commodities - Agriculture |  |
| `theme_commoditiesenergy` | Commodities - Energy |  |
| `theme_commoditiesmetals` | Commodities - Metals |  |
| `theme_consumergoods` | Consumer Goods |  |
| `theme_cryptoblockchain` | Crypto & Blockchain | crypto, 암호화폐, 블록체인 |
| `theme_cybersecurity` | Cybersecurity | cybersecurity, 사이버보안 |
| `theme_defenseaerospace` | Defense & Aerospace |  |
| `theme_digitalentertainment` | Digital Entertainment |  |
| `theme_ecommerce` | E-commerce | e-commerce, EC |
| `theme_educationtechnology` | Education Technology |  |
| `theme_electricvehicles` | Electric Vehicles | EV, 전기차 |
| `theme_energyrenewable` | Energy - Renewable | renewable, 재생에너지 |
| `theme_energytraditional` | Energy - Traditional |  |
| `theme_environmentalsustainability` | Environmental Sustainability |  |
| `theme_fintech` | FinTech | fintech, 핀테크 |
| `theme_hardware` | Hardware | hardware, 하드웨어 |
| `theme_healthcarebiotech` | Healthcare & Biotech | biotech, 바이오테크 |
| `theme_healthyfoodnutrition` | Healthy Food & Nutrition |  |
| `theme_industrialautomation` | Industrial Automation |  |
| `theme_internetofthings` | Internet of Things | IoT |
| `theme_nanotechnology` | Nanotechnology |  |
| `theme_quantumcomputing` | Quantum Computing | quantum, 양자컴퓨팅 |
| `theme_realestatereits` | Real Estate & REITs | REITs, 부동산투자신탁 |
| `theme_robotics` | Robotics | robotics, 로보틱스 |
| `theme_semiconductors` | Semiconductors | semiconductors, 반도체 |
| `theme_smarthome` | Smart Home |  |
| `theme_socialmedia` | Social Media |  |
| `theme_software` | Software | software, 소프트웨어 |
| `theme_spacetech` | Space Tech | space, 우주 |
| `theme_telecommunications` | Telecommunications |  |
| `theme_transportationlogistics` | Transportation & Logistics |  |
| `theme_virtualaugmentedreality` | Virtual & Augmented Reality | VR, AR, 메타버스 |
| `theme_wearables` | Wearables |  |

### 세부 테마 (`subtheme_`)


268개 sub-theme 사용 가능. 패턴: `subtheme_{category}{subtopic}`.

카테고리 예시: `ai`, `automation`, `autonomous`, `bigdata`, `blockchain`, `cloud`, `cybersecurity`, `defense`, `ecommerce`, `education`, `energy`, `entertainment`, `environmental`, `evs`, `fintech`, `hardware`, `healthcare`, `iot`, `longevity`, `nanotech`, `nutrition`, `quantum`, `realestate`, `robotics`, `semis`, `smarthome`, `social`, `software`, `space`, `telecom`.


**예시 코드:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `subtheme_aicompute` | AI - Compute & Acceleration | AI반도체 |
| `subtheme_aicloud` | AI - Cloud & Infrastructure | AI클라우드 |
| `subtheme_aimodels` | AI - Foundation Models & Platforms | AI모델 |
| `subtheme_semiscompute` | Semis - Logic & CPUs, GPUs, Accelerators | 반도체로직 |
| `subtheme_semsmemory` | Semis - Memory & Storage | 반도체메모리 |
| `subtheme_evsbatteries` | EVs - Batteries & Materials | EV배터리 |
| `subtheme_evscharging` | EVs - Charging & Infrastructure | EV충전 |
| `subtheme_cybersecuritycloud` | Cybersecurity - Cloud Security | 클라우드보안 |
| `subtheme_healthcaregenomics` | Healthcare - Genomics & Personalized Medicine | 게놈 |

---


## ETF 필터 (`etf_`)


ETF 전용 필터는 ETF 스크리닝 시(industry = Exchange Traded Fund) 나타납니다.


### 연환산 수익률 (`etf_return_`)


패턴: `etf_return_{period}o{N}` (N% 초과), `etf_return_{period}u{N}` (-N% 미만). 기간: `1y`, `3y`, `5y`. N = 0, 05, 10, 25.


### 순보수율 (`etf_netexpense_`)


패턴: `etf_netexpense_u{NN}` (N.N% 미만). NN = 01–10 (0.1%–1.0%).


### 순자금 유입 (`etf_fundflows_`)


패턴: `etf_fundflows_{period}o{N}` / `etf_fundflows_{period}u{N}`. 기간: `1m`, `3m`, `ytd`. N = 0, 10, 25, 50.


### 자산 유형 (`etf_assettype_`)


28개 자산 유형: bonds, commodities, equities, currency, crypto, MLP, preferred stock, SPAC, multi-asset, target date.


### 단일 카테고리 (`etf_category_`)


ETF 세분 분류용 34개 카테고리(bonds, commodities, currency, equity subtypes).


### 운용사 (`etf_sponsor_`)


437개 ETF 운용사(e.g., `etf_sponsor_blackrockishares`, `etf_sponsor_vanguard`, `etf_sponsor_schwab`, `etf_sponsor_fidelity`).


---


## Industry 코드 (`ind_`)


150개 industry 코드. 패턴: `ind_{lowercasename}` (공백, 하이픈, 특수문자 제거).


**주요 예시:**

| Code | 의미 | 자연어 키워드 |
|------|---------|---------------------------|
| `ind_stocksonly` | Stocks only (ex-Funds) | 펀드제외, 주식만 |
| `ind_exchangetradedfund` | Exchange Traded Fund | ETF |
| `ind_semiconductors` | Semiconductors | 반도체 |
| `ind_softwareapplication` | Software - Application | 앱 |
| `ind_softwareinfrastructure` | Software - Infrastructure | 인프라소프트 |
| `ind_biotechnology` | Biotechnology | 바이오테크놀로지 |
| `ind_banksregional` | Banks - Regional | 지방은행 |
| `ind_banksdiversified` | Banks - Diversified | 대형은행 |
| `ind_oilgasep` | Oil & Gas E&P | 석유가스탐사 |
| `ind_oilgasintegrated` | Oil & Gas Integrated | 통합석유 |
| `ind_reitindustrial` | REIT - Industrial | 물류REIT |
| `ind_reitresidential` | REIT - Residential | 주거REIT |
| `ind_utilitiesregulatedelectric` | Utilities - Regulated Electric | 규제전력 |
| `ind_insurancepropertycasualty` | Insurance - Property & Casualty | 손해보험 |
| `ind_capitalmarkets` | Capital Markets | 자본시장 |
| `ind_drugmanufacturersgeneral` | Drug Manufacturers - General | 대형제약 |
| `ind_medicaldevices` | Medical Devices | 의료기기 |
| `ind_aerospacedefense` | Aerospace & Defense | 항공우주/방위 |
| `ind_restaurants` | Restaurants | 외식 |
| `ind_internetretail` | Internet Retail | 온라인쇼핑 |
| `ind_gold` | Gold | 금광 |
| `ind_steel` | Steel | 철강 |

150개 industry 코드 전체 목록은 finviz screener dropdown 또는 `finviz` Python library를 사용하세요.


---


## 자주 쓰는 스크리닝 레시피


### High Dividend Value (고배당밸류)

```

f=cap_midover,fa_div_o3,fa_pe_u20,fa_pb_u2,fa_roe_o10,geo_usa

```

미국 Mid-cap+ 종목 중 배당 3%+, P/E 20 미만, P/B 2 미만, ROE 10% 초과 조건입니다.


### Small-Cap Growth (소형성장주)

```

f=cap_small,fa_epsqoq_o25,fa_salesqoq_o15,fa_roe_o15,sh_avgvol_o200

```

Small-cap 중 분기 EPS 성장 25%+, 매출 성장 15%+, ROE 15%+, 충분한 유동성 조건입니다.


### Oversold Large-Cap (과매도대형주)

```

f=cap_largeover,ta_rsi_os30,ta_sma200_pa,fa_pe_profitable,sh_avgvol_o500

```

Large-cap+ 중 RSI 30 미만이지만 200-day MA 위에 있고, 흑자이며 유동성이 있는 조건입니다.


### Breakout Candidates (돌파후보)

```

f=cap_midover,ta_highlow52w_b0to5h,sh_relvol_o1.5,ta_sma50_pa,sh_avgvol_o300

```

52-week high 대비 5% 이내의 Mid-cap+, 평균 이상 거래량, 50-day MA 상단 조건입니다.


### Insider Buying (내부자매수)

```

f=cap_smallover,sh_insidertrans_verypos,fa_pe_profitable,sh_avgvol_o100

```

Small-cap+ 중 내부자 거래가 매우 긍정적이고, 흑자이며, 최소 거래량을 만족하는 조건입니다.


### Short Squeeze Candidates (숏스퀴즈후보)

```

f=sh_short_o20,sh_relvol_o2,ta_perf_1wup,cap_smallover

```

short float 20%+, relative volume 2x+, 이번 주 상승, small-cap 이상 조건입니다.


### Dividend Growth (배당성장)

```

f=fa_div_o2,fa_divgrowth_3yo10,fa_payoutratio_u60,fa_roe_o15,cap_midover,geo_usa

```

배당 2%+, 3Y 배당 성장 10%+, payout 60% 미만, ROE 15%+, 미국 mid-cap+ 조건입니다.


### Deep Value (딥밸류)

```

f=fa_pb_u1,fa_pe_u10,fa_curratio_o1.5,fa_netmargin_pos,sh_avgvol_o100,cap_smallover

```

P/B 1 미만, P/E 10 미만, current ratio 1.5 초과, 흑자, 유동성 조건입니다.


### Momentum Leaders (모멘텀리더)

```

f=ta_perf_13wup,ta_perf_26wup,ta_sma50_pa,ta_sma200_pa,sh_relvol_o1,cap_midover

```

13주/26주 상승, 50/200 MA 상단, 평균 이상 거래량, mid-cap+ 조건입니다.


### Fallen Angels (급락후반등후보)

```

f=cap_largeover,ta_highlow52w_b20h,ta_rsi_os40,fa_pe_profitable,sh_avgvol_o500

```

52W high 대비 20%+ 하락한 Large-cap+, RSI 40 미만, 흑자, 유동성 조건입니다.


### AI Theme (AI테마)

```

f=theme_artificialintelligence,cap_midover,ta_perf_13wup

```

AI 테마 종목, mid-cap+, 이번 분기 상승 조건입니다.


### Earnings Positive Surprise (실적호조)

```

f=fa_epsrev_bp,cap_midover,sh_avgvol_o200

```

EPS와 Revenue가 모두 예상치를 상회하고, mid-cap+이며 유동성이 있는 조건입니다.


### Near All-Time High (최고가부근)

```

f=ta_alltime_b0to5h,cap_largeover,sh_avgvol_o500

```

all-time high 대비 5% 이내, large-cap+, 유동성 조건입니다.


### Low EV/EBITDA Value (저EV/EBITDA)

```

f=fa_evebitda_u10,fa_evebitda_profitable,cap_midover,fa_roe_o10

```

EV/EBITDA 10 미만이면서 흑자, mid-cap+, ROE 10% 초과 조건입니다.
