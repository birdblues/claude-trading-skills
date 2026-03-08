# 포지션 평가 프레임워크

이 문서는 포트폴리오 내 개별 포지션을 평가하여 적절한 조치(HOLD, ADD, TRIM, SELL)를 결정하기 위한 체계적인 프레임워크를 제공합니다.

## 개요

포지션 평가는 정량 분석과 정성적 판단을 모두 요구합니다. 이 프레임워크는 다음 질문에 답하도록 돕습니다:

1. 원래 투자 논리는 여전히 유효한가?
2. 현재 확신도와 리스크를 감안할 때 포지션 크기가 적절한가?
3. 밸류에이션이 과도해졌는가, 아니면 매력적인가?
4. 기대되는 선행 수익률 대비 리스크는 어떤가?
5. 다른 곳에 더 나은 기회가 있는가?

## 4요인 평가 모델

모든 포지션은 네 가지 차원에서 평가해야 합니다:

### 1. 투자 논리 검증 (가중치 40%)
- 투자 논리가 예상대로 전개되고 있는가?
- 펀더멘털이 개선, 안정, 악화 중 어느 상태인가?
- 성장 전망이 유지되고 있는가, 혹은 변했는가?

### 2. 밸류에이션 평가 (가중치 30%)
- 주식이 고평가, 적정가치, 저평가 중 어디에 해당하는가?
- 현재 밸류에이션은 과거 범위와 비교해 어떤가?
- 동종 기업군과 비교하면 어떤가?

### 3. 포지션 사이징 (가중치 20%)
- 현재 포지션 크기가 적절한가?
- 확신 수준과 일치하는가?
- 포트폴리오 집중 리스크를 만들고 있는가?

### 4. 상대적 기회 (가중치 10%)
- 자본을 더 잘 활용할 방법이 있는가?
- 이 포지션을 매도하면 포트폴리오가 개선되는가?
- 보유 비용 대비 다른 곳에 배치했을 때의 이점은?

## 상세 평가 프레임워크

### 투자 논리 검증 분석

**원래 투자 논리 문서화:**

각 포지션에 대해 최초 투자 논리를 문서화합니다:

**예시 투자 논리 템플릿:**
```
Symbol: AAPL
Initial Thesis (Date: Jan 2023):
- Services revenue growing 15%+ annually
- Installed base expansion (1.8B → 2.0B devices)
- Margin expansion from services mix shift
- Capital return program (dividends + buybacks)
- Valuation: P/E 24x vs historical 18x, justified by services growth

Entry Price: $145
Target Price: $180 (12-month)
Expected Return: 24% (+2% dividend = 26% total)
Risk Factors: iPhone demand slowdown, China regulatory risk
```

**투자 논리 검증 체크리스트:**

- [ ] **매출/이익 성장:** 기대 대비 순조로운가?
  - 예상: +15% 매출 성장
  - 실제: +12% (약간 하회, 수용 가능 / -5% (우려))

- [ ] **마진:** 개선, 안정, 하락 중 어느 상태인가?
  - 예상: 100bps 확대
  - 실제: 80bps 확대 (충분히 근접 / 50bps 축소 (부정적))

- [ ] **경쟁 지위:** 강화되고 있는가, 약화되고 있는가?
  - 시장점유율 추세
  - 신제품 성공/실패
  - 경쟁사 대응

- [ ] **경영진 실행력:** 목표를 달성하고 있는가?
  - 가이던스 상회/부합/하회
  - 자본 배분 의사결정
  - 필요한 경우 전략 전환

- [ ] **산업 순풍 요인:** 여전히 존재하는가?
  - 구조적 추세 유지 여부
  - 규제 변화
  - 기술 변화

**투자 논리 상태 분류:**

| 상태 | 기준 | 권장 행동 |
|--------|----------|-------------|
| **강화 중** | 펀더멘털 개선, 투자 논리 가속 | ADD 고려 |
| **유지** | 기대치에 부합, 변화 없음 | HOLD |
| **약화 중** | 일부 우려, 투자 논리 일부 훼손 | TRIM 고려 |
| **붕괴** | 투자 논리 무효, 펀더멘털 악화 | SELL |

### 밸류에이션 평가

**밸류에이션 방법론:**

현재 밸류에이션을 여러 차원에서 비교합니다:

**1. 과거 밸류에이션 범위**

| 지표 | 현재 | 1Y 평균 | 3Y 평균 | 5Y 평균 | 최저 | 최고 |
|--------|---------|--------|--------|--------|-----|-----|
| P/E | 28x | 25x | 22x | 20x | 12x | 35x |
| P/B | 6.5x | 5.8x | 5.2x | 4.8x | 3.5x | 8.0x |
| EV/EBITDA | 22x | 19x | 17x | 16x | 10x | 25x |
| Div Yield | 1.2% | 1.4% | 1.6% | 1.8% | 0.8% | 2.5% |

**분석:**
- 현재 P/E(28x)는 3Y 최대치(35x)에 근접 → 과거 대비 비쌈
- P/B는 5Y 평균 대비 높음 → 프리미엄 밸류에이션
- 배당수익률은 범위 대비 낮음 → 가치주 성격 아님

**2. 동종 기업군 비교**

| 기업 | P/E | P/B | EV/EBITDA | 배당수익률 | 매출 성장 | 마진 |
|---------|-----|-----|-----------|----------------|------------|--------|
| **[대상]** | 28x | 6.5x | 22x | 1.2% | 12% | 28% |
| Peer A | 22x | 4.2x | 18x | 1.8% | 8% | 22% |
| Peer B | 31x | 7.8x | 25x | 0.9% | 18% | 32% |
| Peer C | 25x | 5.1x | 20x | 1.5% | 10% | 25% |
| **섹터 중앙값** | 25x | 5.5x | 20x | 1.4% | 11% | 26% |

**분석:**
- P/E는 섹터 중앙값보다 약간 높음 → 완만한 프리미엄
- 성장률(12%)이 중앙값(11%) 상회 → 프리미엄 일부 정당화
- 마진(28%)이 중앙값(26%) 상회 → 일부 프리미엄을 정당화하는 질적 우위
- **평가:** 동종 대비 적정~약간 고평가

**3. 성장 조정 밸류에이션 (PEG 비율)**

```
PEG Ratio = P/E / Earnings Growth Rate

Example:
P/E: 28x
Expected EPS growth: 15%
PEG = 28 / 15 = 1.87

Interpretation:
< 1.0 = Undervalued
1.0-2.0 = Fair value
> 2.0 = Overvalued
```

**4. DCF 적정가치 추정 (단순화)**

시간이 허용되면 할인현금흐름을 사용해 내재가치를 추정합니다:

```
Fair Value = (FCF × (1 + growth rate)^5) / (discount rate - terminal growth)

Example inputs:
Current FCF: $100B
Growth (5Y): 12%
Discount rate: 10%
Terminal growth: 4%
```

**밸류에이션 상태 분류:**

| 상태 | 기준 | 권장 행동 |
|--------|----------|-------------|
| **저평가** | 과거 평균 이하, 동종 대비 낮음, PEG 낮음 | ADD |
| **적정가치** | 과거 및 동종과 대체로 일치 | HOLD |
| **고평가** | 과거 범위 상단, 동종 대비 프리미엄, PEG 높음 | TRIM |
| **심각한 고평가** | 극단적 멀티플, 버블 유사 | SELL |

### 포지션 사이징 분석

**현재 포지션 평가:**

```
Position Size = Position Value / Total Portfolio Value

Example:
Position value: $18,000
Portfolio value: $120,000
Position size: 18,000 / 120,000 = 15%
```

**포지션 사이징 가이드라인:**

| 확신 수준 | 목표 포지션 크기 | 최대 포지션 크기 |
|------------------|---------------------|-------------------|
| **높은 확신** | 8-12% | 15% |
| **중간 확신** | 5-8% | 10% |
| **낮은 확신 / 투기적** | 2-5% | 7% |
| **시작 포지션** | 2-3% | 5% |

**포지션 사이징 리스크 평가:**

| 현재 비중 | 리스크 수준 | 일반적 조치 |
|--------------|-----------|----------------|
| **<5%** | 낮음 | 확신이 높다면 추가 가능 |
| **5-10%** | 보통 | 모니터링 |
| **10-15%** | 상승 | 확신이 매우 높지 않다면 트림 |
| **15-20%** | 높음 | 트림 권장 |
| **>20%** | 과도 | 긴급 트림 필요 |

**포지션 드리프트 분석:**

가격 상승으로 포지션 비중이 어떻게 변했는지 추적합니다:

```
Position Appreciation Impact:

Initial investment: $10,000 (10% of $100K portfolio)
Other holdings flat, this position doubled
Current value: $20,000 (18% of $110K portfolio)

Position drift: 10% → 18% (increased 8 percentage points)
Exceeded target: Yes (assuming 10% target)
Action: Trim back to 10-12% range
```

**리밸런싱 계산:**

```
To trim from 18% to 10%:

Target value: $110,000 × 10% = $11,000
Current value: $20,000
Amount to sell: $20,000 - $11,000 = $9,000
Shares to sell: $9,000 / Current Price
```

### 상대적 기회 분석

**기회비용 프레임워크:**

질문: "오늘 이 포지션을 매도한다면, 자본을 어디에 배치할 것인가?"

**비교 매트릭스:**

| 옵션 | 기대수익률 | 리스크 수준 | 확신도 | 메모 |
|--------|----------------|------------|-----------|-------|
| **보유 [현재]** | 8% | 중간 | 중간 | 적정가치, 투자 논리 유지 |
| 대안 A | 15% | 높음 | 높음 | 저평가, 강한 투자 논리 |
| 대안 B | 10% | 낮음 | 중간 | 방어적, 낮은 리스크 |
| 현금 (대기) | 4% | 없음 | N/A | 기회비용 |

**의사결정 로직:**

If (대안 기대수익률 - 보유 기대수익률) > 전환 비용:
→ 현재 포지션 매도 후 대안 매수 고려

**고려할 전환 비용:**
- **세금:** 양도차익세(장기 15-20%, 단기 일반소득세율)
- **거래 비용:** 수수료(미미) + 매수/매도 호가 스프레드
- **기회 리스크:** 대안 판단 오류, 현재 포지션 반등 놓침

**예시 계산:**

```
Current position: Expected 8% return
Alternative: Expected 15% return
Differential: 7%

Unrealized gain: $8,000 on $20,000 position (67% gain)
Tax on sale (20% long-term): $8,000 × 0.20 = $1,600
After-tax proceeds: $20,000 - $1,600 = $18,400

After-tax opportunity gain (1 year):
Hold current: $20,000 × 1.08 = $21,600
Buy alternative: $18,400 × 1.15 = $21,160

Conclusion: Tax drag eliminates benefit for 1-year hold
Consider if: (1) Multi-year horizon, or (2) Tax-advantaged account, or (3) Can tax-loss harvest elsewhere
```

## 포지션 액션 의사결정 매트릭스

네 가지 요인을 결합해 액션을 결정합니다:

### HOLD 결정

**기준:**
- ✅ 투자 논리: 유지 또는 강화
- ✅ 밸류에이션: 적정~저평가
- ✅ 포지션 크기: 목표 범위 내(중간 확신의 경우 5-10%)
- ✅ 상대적 기회: 비용 반영 후 더 나은 대안이 명확하지 않음

**예시:**
```
Position: Johnson & Johnson (JNJ)
Thesis: ✅ Intact (healthcare demand, dividend aristocrat)
Valuation: ✅ Fair (P/E 16x vs 15x historical avg)
Position Size: ✅ 7% of portfolio (target range)
Opportunity: ✅ No compelling alternative in healthcare

Decision: HOLD
Rationale: Position performing as expected, appropriately sized, no reason to change
Next Review: Quarterly earnings (Q3 2024)
```

### ADD 결정

**기준:**
- ✅ 투자 논리: 강화 중이거나, 높은 확신을 가진 유지 상태
- ✅ 밸류에이션: 저평가 또는 펀더멘털 개선을 동반한 적정가치
- ✅ 포지션 크기: 목표 대비 낮아 과도한 집중 없이 추가 가능
- ✅ 기회: 최상위 아이디어 중 하나이며 대안 대비 우수

**예시:**
```
Position: Meta Platforms (META)
Thesis: ✅ Strengthening (AI monetization exceeding expectations, cost discipline)
Valuation: ✅ Undervalued (P/E 22x vs 28x historical, PEG 1.2)
Position Size: ✅ 5% of portfolio (room to add to 8-10%)
Opportunity: ✅ Top conviction, better expected return than alternatives

Decision: ADD 3-5% more (increase position to 8-10% total)
Rationale: Thesis improving, valuation attractive, high conviction
Entry Strategy: Add 3% now, 2% more if pullback to $450 support
Risk Management: Set stop-loss at $420 (recent low)
```

### TRIM 결정

**기준:**
- ⚠️ 투자 논리: 약화 중이거나, 유지되더라도 확신이 낮아짐
- ⚠️ 밸류에이션: 고평가 또는 과거/동종 대비 비쌈
- ⚠️ 포지션 크기: 목표 초과(중간 확신 >12%, 높은 확신 >15%)
- ⚠️ 기회: 더 나은 대안 존재 또는 리스크 축소 필요

**예시:**
```
Position: NVIDIA (NVDA)
Thesis: ✅ Intact (AI demand strong) ⚠️ but slowing growth rates expected
Valuation: ⚠️ Expensive (P/E 65x vs 45x historical, extended vs peers)
Position Size: ⚠️ 18% of portfolio (exceeded 15% max)
Opportunity: ⚠️ Other high-quality tech at better valuations

Decision: TRIM from 18% to 10-12%
Rationale: Valuation extended, position too large, take some profits
Trim Strategy: Sell 6% now, consider selling another 2% if rallies above $950
Redeployment: Add to underweight healthcare and financials sectors
Tax Strategy: Sell highest-cost-basis shares first (minimize tax impact)
```

### SELL 결정

**기준:**
- ❌ 투자 논리: 붕괴 또는 중대하게 훼손
- OR: 펀더멘털 악화와 동반된 심각한 고평가
- OR: 더 나은 기회 존재 + 보유 종목 수 축소 필요
- OR: 리스크 관리(손절 트리거, 리스크 과도)

**예시:**
```
Position: Teladoc (TDOC)
Thesis: ❌ Broken (telehealth adoption slower than expected, competition intense, path to profitability unclear)
Valuation: ❌ Expensive vs peers despite losses (EV/Sales 2.5x vs 1.2x sector)
Position Size: ⚠️ 4% of portfolio (not excessive, but capital can be better deployed)
Opportunity: ❌ Multiple better healthcare alternatives (UNH, ELW, CVS)

Decision: SELL (exit position entirely)
Rationale: Investment thesis has not materialized, competitive position weakening, capital better deployed elsewhere
Exit Strategy: Sell entire position over 2-3 days (avoid moving market)
Redeployment: Reallocate to UnitedHealth Group (stronger healthcare thesis)
Tax Benefit: Harvest $2,000 capital loss to offset gains
Lesson Learned: Avoid unprofitable growth stocks in competitive industries
```

## 포지션 리뷰 체크리스트

각 포지션 리뷰 시 이 체크리스트를 사용하세요:

### 펀더멘털 리뷰
- [ ] 최근 실적 보고서와 콜 트랜스크립트 읽기
- [ ] 최신 재무 지표(매출, 마진, EPS) 점검
- [ ] 가이던스 변경 확인(상향, 하향, 유지)
- [ ] 최근 애널리스트 리포트 또는 뉴스 확인
- [ ] 경쟁 지위 검증(시장점유율, 신규 진입자)

### 밸류에이션 리뷰
- [ ] 현재 P/E, P/B, EV/EBITDA 계산
- [ ] 1Y, 3Y, 5Y 과거 평균과 비교
- [ ] 동종 기업군과 비교
- [ ] PEG 비율 계산
- [ ] 밸류에이션이 펀더멘털로 정당화되는지 평가

### 포트폴리오 적합성 리뷰
- [ ] 현재 포지션 비중 계산(포트폴리오 대비 %)
- [ ] 비중이 확신도와 일치하는지 평가
- [ ] 포지션이 집중 리스크에 기여하는지 점검
- [ ] 섹터 배분 영향 확인
- [ ] 다른 보유 종목과의 상관관계 평가

### 리스크 리뷰
- [ ] 신규 리스크 식별(규제, 경쟁, 거시경제)
- [ ] 손절 기준 업데이트 필요성 평가
- [ ] 하방 시나리오 검토(무엇이 잘못될 수 있는가?)
- [ ] 베타와 변동성 확인(증가했는가?)
- [ ] 여전히 리스크/보상 비율이 유리한지 평가

### 액션 결정
- [ ] 투자 논리가 HOLD/ADD/TRIM/SELL 중 무엇을 지지하는가?
- [ ] 변경이 필요하다면 구체적 액션은 무엇인가?
- [ ] 액션 실행 시점은?(즉시, 분할, 특정 가격 대기)
- [ ] 향후 액션 트리거 포인트는?
- [ ] 결정과 근거 문서화

## 포지션 평가의 흔한 실수

### 실수 1: 매입가에 고정(앵커링)

**문제:** "$100에 샀는데 지금 $80이니 본전 올 때까지 기다릴래"

**왜 틀렸나:** 매입가는 미래 수익률과 무관합니다. 매몰비용 오류입니다.

**올바른 접근:** 현재 펀더멘털과 선행 전망 기준으로 평가합니다. 투자 논리가 깨졌다면 손익과 무관하게 지금 매도합니다.

### 실수 2: 승자 포지션을 무기한 방치

**문제:** "내 최고 수익 종목이니 절대 안 팔아!"

**왜 틀렸나:** 포지션이 과대해져 집중 리스크가 생기고, 밸류에이션이 과열될 수 있습니다.

**올바른 접근:** 승자 포지션은 주기적으로 목표 비중까지 트림합니다. 일부 이익을 실현하고 저평가 영역에 재투자합니다.

### 실수 3: 패자 포지션을 너무 빨리 매도

**문제:** "15% 빠졌으니 손실을 잘라야 해"

**왜 틀렸나:** 변동성은 정상입니다. 공포 매도는 회복 전 손실을 확정하는 경우가 많습니다.

**올바른 접근:** 투자 논리가 여전히 유효한지 평가합니다. 유효하면 추가 매수(평균단가 인하)를 고려하고, 아니면 손실 규모와 무관하게 매도합니다.

### 실수 4: 밸류에이션 무시("어떤 가격이든 좋은 기업")

**문제:** "이 회사는 훌륭하니 밸류에이션은 중요하지 않아"

**왜 틀렸나:** 훌륭한 기업도 고평가될 수 있습니다. 미래 수익률은 진입 가격에 좌우됩니다.

**올바른 접근:** 좋은 기업도 적정 가격에 사야 합니다. 우량주라도 비싸면 트림하고, 싸면 추가합니다.

### 실수 5: 종목에 감정 이입

**문제:** 감정적 애착이 객관적 평가를 방해함

**왜 틀렸나:** 주식은 당신을 사랑하지 않습니다. 자본 배분은 냉정하고 합리적이어야 합니다.

**올바른 접근:** 포지션을 관계가 아닌 자본 배치 결정으로 취급합니다. 더 나은 기회가 있다면 어떤 종목이든 매도할 수 있어야 합니다.

## 요약

**포지션 평가 프레임워크:**

1. **투자 논리 검증 (40%)** - 스토리가 여전히 사실인가?
2. **밸류에이션 평가 (30%)** - 가격이 적절한가?
3. **포지션 사이징 (20%)** - 규모가 적절한가?
4. **상대적 기회 (10%)** - 자본의 더 나은 용처가 있는가?

**네 가지 액션:**

- **HOLD:** 투자 논리 유지, 적정 밸류에이션, 적절한 비중
- **ADD:** 투자 논리 강화, 저평가, 추가 여력 존재
- **TRIM:** 투자 논리 약화 OR 고평가 OR 과대 비중
- **SELL:** 투자 논리 붕괴 OR 심각한 고평가 OR 훨씬 나은 대안 존재

**베스트 프랙티스:**

- 포지션은 분기별(최소) 리뷰
- 매수 시 투자 논리 문서화
- 새 정보가 나오면 투자 논리 업데이트
- 실수는 조기에 인정
- 분산 유지를 위해 승자 포지션 트림
- 투자 논리가 유지될 때만 물타기
- 매입가(매몰비용) 무시
- 객관성과 감정 통제 유지

**기억할 점:** 포지션 평가는 예술이자 과학입니다. 정량 지표와 정성 판단을 결합하세요. 확신이 없을 때는 전량 보유나 전량 매도보다 포지션 크기 축소가 더 나은 선택일 수 있습니다.
