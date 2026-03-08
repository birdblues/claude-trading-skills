# Cross-Sector 테마 정의

이 레퍼런스는 FINVIZ industry, 섹터, proxy ETF, 대표 종목 기준으로 시장 테마를 정의합니다. `theme_classifier.py` 스크립트는 이 정의를 읽어 industry 레벨 데이터를 theme 레벨 집계로 매핑합니다.

**사용 노트:**
- Industry 이름은 FINVIZ industry 이름과 정확히 일치해야 합니다 (`finviz_industry_codes.md` 참고)
- `min_matching_industries`: 테마가 탐지되기 위해 활동 신호가 나타나야 하는 최소 구성 industry 수
- `static_stocks`: industry 레벨 데이터가 부족할 때 사용하는 대체 대표 종목
- `proxy_etfs`: 빠른 거래량/모멘텀 점검과 사용자 노출 추천에 활용

---

## AI & Semiconductors

- **Direction bias**: Bullish (일반적)
- **Industries**: Semiconductors, Software - Application, Software - Infrastructure, Information Technology Services, Electronic Components, Computer Hardware, Scientific & Technical Instruments
- **Sectors**: Technology (primary), Communication Services, Industrials
- **Proxy ETFs**: SMH, SOXX, AIQ, BOTZ, CHAT
- **Static stocks**: NVDA, AVGO, AMD, INTC, QCOM, MRVL, AMAT, LRCX, KLAC, TSM, MU, ARM, SNPS, CDNS, MCHP
- **Min matching industries**: 2

---

## Clean Energy & EV

- **Direction bias**: Bullish (일반적)
- **Industries**: Solar, Utilities - Renewable, Auto Manufacturers, Auto Parts, Electrical Equipment & Parts, Specialty Chemicals
- **Sectors**: Utilities, Consumer Cyclical, Industrials, Basic Materials
- **Proxy ETFs**: ICLN, QCLN, TAN, DRIV, LIT
- **Static stocks**: ENPH, SEDG, FSLR, RUN, TSLA, RIVN, LCID, NIO, PLUG, BE, CHPT, ALB, SQM, LAC, LTHM
- **Min matching industries**: 2

---

## Cybersecurity

- **Direction bias**: Bullish (일반적)
- **Industries**: Software - Infrastructure, Information Technology Services, Software - Application, Communication Equipment
- **Sectors**: Technology (primary)
- **Proxy ETFs**: CIBR, HACK, BUG
- **Static stocks**: CRWD, PANW, FTNT, ZS, NET, S, OKTA, CYBR, QLYS, RPD, TENB, VRNS, SAIL, MNDT, DDOG
- **Min matching industries**: 2

**노트:** Cybersecurity는 광범위한 소프트웨어 industry와 겹칩니다. 테마 분류 시 일반 소프트웨어 테마와의 구분을 위해 proxy ETF 거래량과 static stock 성과를 사용합니다.

---

## Cloud Computing & SaaS

- **Direction bias**: Bullish (일반적)
- **Industries**: Software - Application, Software - Infrastructure, Information Technology Services
- **Sectors**: Technology (primary), Communication Services
- **Proxy ETFs**: SKYY, WCLD, CLOU
- **Static stocks**: CRM, NOW, SNOW, DDOG, TEAM, MDB, ESTC, NET, ZS, HUBS, BILL, TTD, PLTR, DOCN, DT
- **Min matching industries**: 2

**노트:** Cloud/SaaS는 Cybersecurity 및 AI 테마와 중복이 큽니다. 여러 테마가 같은 industry를 공유할 때 proxy ETF 성과를 통해 구분합니다.

---

## Biotech & Genomics

- **Direction bias**: Bullish (일반적이지만 변동성 큼)
- **Industries**: Biotechnology, Drug Manufacturers - Specialty & Generic, Medical Devices, Diagnostics & Research, Drug Manufacturers - General
- **Sectors**: Healthcare (primary)
- **Proxy ETFs**: XBI, IBB, ARKG, GNOM
- **Static stocks**: AMGN, GILD, VRTX, REGN, MRNA, BIIB, ILMN, CRSP, NTLA, BEAM, EDIT, EXAS, TWST, SGEN, BMRN
- **Min matching industries**: 2

---

## Infrastructure & Construction

- **Direction bias**: Bullish (일반적, 정책 영향 큼)
- **Industries**: Engineering & Construction, Building Materials, Industrial Distribution, Farm & Heavy Construction Machinery, Steel, Specialty Industrial Machinery, Railroads, Waste Management
- **Sectors**: Industrials (primary), Basic Materials
- **Proxy ETFs**: PAVE, IFRA, SIMS
- **Static stocks**: CAT, DE, VMC, MLM, URI, PWR, EME, MTZ, GVA, AECOM, STRL, GBX, NUE, CLF, RS
- **Min matching industries**: 3

---

## Gold & Precious Metals

- **Direction bias**: Bullish (보통 risk-off 또는 인플레이션 국면)
- **Industries**: Gold, Silver, Other Precious Metals & Mining
- **Sectors**: Basic Materials (primary)
- **Proxy ETFs**: GDX, GDXJ, RING, SIL
- **Static stocks**: NEM, GOLD, AEM, FNV, WPM, RGLD, KGC, AGI, AU, HMY, PAAS, CDE, HL, MAG, EQX
- **Min matching industries**: 2

---

## Oil & Gas (Energy Sector)

- **Direction bias**: Varies (경기순환형)
- **Industries**: Oil & Gas E&P, Oil & Gas Equipment & Services, Oil & Gas Midstream, Oil & Gas Refining & Marketing, Oil & Gas Integrated, Oil & Gas Drilling
- **Sectors**: Energy (primary)
- **Proxy ETFs**: XLE, XOP, OIH
- **Static stocks**: XOM, CVX, COP, EOG, SLB, HAL, PXD, DVN, MPC, VLO, PSX, OXY, FANG, HES, WMB
- **Min matching industries**: 2

---

## Financial Services & Banks

- **Direction bias**: Varies (금리 민감)
- **Industries**: Banks - Diversified, Banks - Regional, Capital Markets, Insurance - Diversified, Insurance - Property & Casualty, Financial Data & Stock Exchanges, Credit Services, Asset Management, Insurance Brokers, Mortgage Finance
- **Sectors**: Financial Services (primary)
- **Proxy ETFs**: XLF, KBE, KRE, IAI
- **Static stocks**: JPM, BAC, WFC, GS, MS, C, SCHW, BLK, AXP, ICE, CME, MCO, SPGI, BX, KKR
- **Min matching industries**: 3

---

## Healthcare & Pharma

- **Direction bias**: Varies (하락장 방어 성격)
- **Industries**: Drug Manufacturers - General, Health Care Plans, Medical Care Facilities, Health Information Services, Medical Distribution, Medical Instruments & Supplies, Pharmaceutical Retailers
- **Sectors**: Healthcare (primary)
- **Proxy ETFs**: XLV, IHE, IHI
- **Static stocks**: UNH, JNJ, LLY, PFE, ABT, TMO, DHR, MDT, ISRG, SYK, BSX, EW, HCA, CVS, CI
- **Min matching industries**: 3

**노트:** Healthcare & Pharma는 Biotech & Genomics와 구분됩니다. Healthcare는 성숙 제약, 보험, 의료기기에 초점을 두고, Biotech는 신약 개발 및 유전체 중심입니다.

---

## Defense & Aerospace

- **Direction bias**: Bullish (지정학 긴장 시 일반적으로 강함)
- **Industries**: Aerospace & Defense, Airlines, Security & Protection Services
- **Sectors**: Industrials (primary)
- **Proxy ETFs**: ITA, PPA, ROKT, ARKX
- **Static stocks**: LMT, RTX, NOC, BA, GD, LHX, HII, TDG, HWM, AXON, LDOS, BWXT, KTOS, RKLB, SPR
- **Min matching industries**: 2

---

## Real Estate & REITs

- **Direction bias**: Varies (금리 민감)
- **Industries**: REIT - Residential, REIT - Industrial, REIT - Retail, REIT - Office, REIT - Healthcare Facilities, REIT - Diversified, REIT - Hotel & Motel, REIT - Specialty, Real Estate Services, Real Estate - Diversified, Real Estate - Development
- **Sectors**: Real Estate (primary)
- **Proxy ETFs**: VNQ, XLRE, IYR
- **Static stocks**: PLD, AMT, CCI, EQIX, SPG, O, WELL, DLR, PSA, VICI, EXR, AVB, ARE, MAA, IRM
- **Min matching industries**: 3

---

## Retail & Consumer

- **Direction bias**: Varies (소비 심리 주도)
- **Industries**: Internet Retail, Specialty Retail, Apparel Retail, Home Improvement Retail, Department Stores, Discount Stores, Luxury Goods, Restaurants, Leisure, Resorts & Casinos, Gambling, Apparel Manufacturing, Footwear & Accessories
- **Sectors**: Consumer Cyclical (primary), Consumer Defensive
- **Proxy ETFs**: XLY, XRT, XLP, IBUY
- **Static stocks**: AMZN, HD, LOW, TJX, COST, WMT, TGT, NKE, SBUX, MCD, DPZ, LULU, ROST, BURL, DECK
- **Min matching industries**: 3

---

## Crypto & Blockchain

- **Direction bias**: Bullish (risk-on 국면에서 일반적)
- **Industries**: Capital Markets, Software - Application, Financial Data & Stock Exchanges, Information Technology Services
- **Sectors**: Financial Services, Technology
- **Proxy ETFs**: BITO, BLOK, BITQ, IBIT, DAPP
- **Static stocks**: COIN, MSTR, MARA, RIOT, CLSK, HUT, BITF, SQ, PYPL, HOOD, CIFR, IREN, HIVE, CORZ, BTBT
- **Min matching industries**: 2

**노트:** Crypto 테마는 industry 분류보다 proxy ETF와 static stock 신호를 우선적으로 사용합니다. 블록체인 기업이 여러 전통 industry에 걸쳐 있기 때문입니다.

---

## Nuclear Energy

- **Direction bias**: Bullish (정책 수혜, AI 데이터센터 수요)
- **Industries**: Uranium, Utilities - Independent Power Producers, Specialty Industrial Machinery, Electrical Equipment & Parts
- **Sectors**: Energy, Utilities, Industrials
- **Proxy ETFs**: URA, URNM, NLR, NUKZ
- **Static stocks**: CCJ, UEC, NXE, DNN, UUUU, LEU, SMR, OKLO, BWX, GEV, CEG, VST, TLN, NRG, BWXT
- **Min matching industries**: 2

---

## Uranium

- **Direction bias**: Bullish (공급 부족 내러티브)
- **Industries**: Uranium, Other Industrial Metals & Mining
- **Sectors**: Energy (primary), Basic Materials
- **Proxy ETFs**: URA, URNM, URNJ
- **Static stocks**: CCJ, UEC, NXE, DNN, UUUU, LEU, URG, GLATF, EU, PALAF, SRUUF, LTBR, FCUUF, AEC, WSTRF
- **Min matching industries**: 1

**노트:** Uranium은 Nuclear Energy의 하위 테마이지만, 상품(commodity) 중심의 고유한 동학 때문에 별도로 추적합니다. 섹터 범위가 좁아 `1`개 industry 매칭만으로도 탐지를 허용합니다.

---

## Obesity & GLP-1

- **Direction bias**: Bullish (의료 혁신)
- **Industries**: Drug Manufacturers - General, Drug Manufacturers - Specialty & Generic, Medical Devices, Biotechnology
- **Sectors**: Healthcare (primary)
- **Proxy ETFs**: SLIM, HRTS
- **Static stocks**: LLY, NVO, AMGN, VKTX, ALT, GPCR, SMLR, RVMD, PTGX, IVA
- **Min matching industries**: 2

**노트:** Obesity/GLP-1은 Healthcare & Pharma와 중복되는 협소한 테마입니다. industry 분류보다 proxy ETF 거래량과 static stock 성과로 주로 차별화합니다.

---

## 요약 표

| Theme | Industries | Sectors | Proxy ETFs | Static Stocks | Min Industries |
|-------|-----------|---------|-----------|--------------|----------------|
| AI & Semiconductors | 7 | 3 | 5 | 15 | 2 |
| Clean Energy & EV | 6 | 4 | 5 | 15 | 2 |
| Cybersecurity | 4 | 1 | 3 | 15 | 2 |
| Cloud Computing & SaaS | 3 | 2 | 3 | 15 | 2 |
| Biotech & Genomics | 5 | 1 | 4 | 15 | 2 |
| Infrastructure & Construction | 8 | 2 | 3 | 15 | 3 |
| Gold & Precious Metals | 3 | 1 | 4 | 15 | 2 |
| Oil & Gas (Energy) | 6 | 1 | 3 | 15 | 2 |
| Financial Services & Banks | 10 | 1 | 4 | 15 | 3 |
| Healthcare & Pharma | 7 | 1 | 3 | 15 | 3 |
| Defense & Aerospace | 3 | 1 | 4 | 15 | 2 |
| Real Estate & REITs | 11 | 1 | 3 | 15 | 3 |
| Retail & Consumer | 13 | 2 | 4 | 15 | 3 |
| Crypto & Blockchain | 4 | 2 | 5 | 15 | 2 |
| Nuclear Energy | 4 | 3 | 4 | 15 | 2 |
| Uranium | 2 | 2 | 3 | 15 | 1 |
| Obesity & GLP-1 | 4 | 1 | 2 | 10 | 2 |

**총계: 17개 테마**로 주요 시장 내러티브를 포괄합니다.

---

## 테마 중복 매트릭스

일부 industry는 여러 테마에 동시에 기여합니다. 스코어링 시 각 industry 데이터는 해당되는 모든 테마에 사용됩니다.

| Industry | Themes |
|----------|--------|
| Software - Application | AI, Cybersecurity, Cloud, Crypto |
| Software - Infrastructure | AI, Cybersecurity, Cloud |
| Drug Manufacturers - General | Healthcare, Biotech, Obesity |
| Biotechnology | Biotech, Obesity |
| Capital Markets | Financial Services, Crypto |
| Electrical Equipment & Parts | Clean Energy, Nuclear |
| Uranium | Nuclear, Uranium |

이 중복은 의도된 설계입니다. 예를 들어 소프트웨어 industry가 강하면 여러 테마가 동시에 강화될 수 있으며, 이는 시장 내러티브의 상호연결성을 반영합니다.
