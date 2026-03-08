# Strategy Archetypes Catalog

8개의 정형 전략 archetype이 주요 systematic trading 접근을 포괄합니다. 각 archetype은 기본 모듈, 전형적 실패 모드, 호환 pivot 타깃을 정의합니다.

---

## 1. Trend Following Breakout (`trend_following_breakout`)

**설명**: 가격이 박스권을 거래량 확인과 함께 상향 돌파할 때 매수합니다. trailing stop으로 추세를 추종합니다.

**Default Modules**:
- hypothesis_type: breakout
- mechanism_tag: behavior
- entry_family: pivot_breakout
- horizon: medium (10-60 days)
- risk_style: wide (trailing stop 8-12%)

**Typical Failure Modes**:
- 박스권 장세의 whipsaw
- 과도 상승 이후 늦은 진입
- stop 레벨을 갭으로 이탈하는 하락

**Compatible Pivots From**: mean_reversion_pullback, volatility_contraction, sector_rotation_momentum

---

## 2. Mean Reversion Pullback (`mean_reversion_pullback`)

**설명**: 확립된 상승 추세 내 과매도 pullback을 매수하고 평균회귀 수익을 노립니다.

**Default Modules**:
- hypothesis_type: mean_reversion
- mechanism_tag: statistical
- entry_family: research_only
- horizon: short (3-14 days)
- risk_style: tight (stop 3-5%)

**Typical Failure Modes**:
- 추세 전환 구간에서 falling knife 포착
- time stop 내 반등 부족
- 섹터 전반 급락으로 개별 종목 mean reversion 무력화

**Compatible Pivots From**: trend_following_breakout, volatility_contraction, earnings_drift_pead

---

## 3. Earnings Drift PEAD (`earnings_drift_pead`)

**설명**: 실적 서프라이즈 이후 진입해 post-earnings announcement drift를 공략합니다.

**Default Modules**:
- hypothesis_type: earnings_drift
- mechanism_tag: information
- entry_family: gap_up_continuation
- horizon: medium (5-30 days)
- risk_style: normal (stop 5-8%)

**Typical Failure Modes**:
- 드리프트를 되돌리는 one-day gap fill
- 시장 전반 매도로 개별 종목 드리프트 무력화
- 드리프트 진행 후 늦은 진입

**Compatible Pivots From**: event_driven_fade, trend_following_breakout, mean_reversion_pullback

---

## 4. Volatility Contraction (`volatility_contraction`)

**설명**: 변동성이 역사적 저점(VCP 패턴)으로 수축할 때 진입하여, 추세 방향의 확장을 노립니다.

**Default Modules**:
- hypothesis_type: breakout
- mechanism_tag: structural
- entry_family: pivot_breakout
- horizon: medium (10-40 days)
- risk_style: tight (stop 3-6%)

**Typical Failure Modes**:
- 수축 구간의 false breakout
- 장기 수축으로 time stop 비용 누적
- 잘못된 방향으로의 변동성 확장

**Compatible Pivots From**: trend_following_breakout, mean_reversion_pullback, statistical_pairs

---

## 5. Regime Conditional Carry (`regime_conditional_carry`)

**설명**: 유리한 macro regime에서만 포지션을 보유하고, regime detection으로 진입을 필터링합니다.

**Default Modules**:
- hypothesis_type: regime
- mechanism_tag: macro
- entry_family: research_only
- horizon: long (30-120 days)
- risk_style: normal (stop 5-8%)

**Typical Failure Modes**:
- regime detection 지연에 따른 늦은 진입/청산
- regime 전환 구간의 whipsaw
- 보수적 진입 시점으로 인한 추세장 언더퍼폼

**Compatible Pivots From**: sector_rotation_momentum, event_driven_fade, statistical_pairs

---

## 6. Sector Rotation Momentum (`sector_rotation_momentum`)

**설명**: 상대강도 모멘텀이 강한 섹터로 로테이션하고, 모멘텀이 약해지면 이탈합니다.

**Default Modules**:
- hypothesis_type: momentum
- mechanism_tag: behavior
- entry_family: research_only
- horizon: medium (20-60 days)
- risk_style: normal (stop 5-8%)

**Typical Failure Modes**:
- 섹터 로테이션 전환 구간의 모멘텀 반전
- 인기 섹터의 crowded trade
- 스트레스 장세 상관관계 급등으로 분산효과 무력화

**Compatible Pivots From**: trend_following_breakout, regime_conditional_carry, earnings_drift_pead

---

## 7. Event Driven Fade (`event_driven_fade`)

**설명**: 예정/비예정 이벤트에 대한 과잉 반응을 역추적하여 초기 움직임 이후 mean reversion에 베팅합니다.

**Default Modules**:
- hypothesis_type: mean_reversion
- mechanism_tag: information
- entry_family: research_only
- horizon: short (1-10 days)
- risk_style: tight (stop 2-5%)

**Typical Failure Modes**:
- 과잉 반응이 아니라 실제 regime 전환인 이벤트
- 초기 움직임을 증폭하는 연쇄 이벤트
- 극단 이벤트에서의 유동성 갭

**Compatible Pivots From**: earnings_drift_pead, mean_reversion_pullback, volatility_contraction

---

## 8. Statistical Pairs (`statistical_pairs`)

**설명**: cointegrated pair를 대상으로 스프레드가 균형에서 이탈할 때 저평가 종목 롱/고평가 종목 숏으로 거래합니다.

**Default Modules**:
- hypothesis_type: mean_reversion
- mechanism_tag: statistical
- entry_family: research_only
- horizon: medium (10-30 days)
- risk_style: normal (stop via z-score threshold)

**Typical Failure Modes**:
- 펀더멘털 변화에 따른 cointegration 붕괴
- 리스크 한도를 초과하는 스프레드 장기 발산
- 숏 레그 실행 리스크(차입 비용, 대차 물량)

**Compatible Pivots From**: mean_reversion_pullback, volatility_contraction, regime_conditional_carry

---

## Archetype Compatibility Matrix

| Source Archetype | Compatible Pivot Targets |
|---|---|
| trend_following_breakout | mean_reversion_pullback, volatility_contraction, sector_rotation_momentum |
| mean_reversion_pullback | trend_following_breakout, volatility_contraction, earnings_drift_pead |
| earnings_drift_pead | event_driven_fade, trend_following_breakout, mean_reversion_pullback |
| volatility_contraction | trend_following_breakout, mean_reversion_pullback, statistical_pairs |
| regime_conditional_carry | sector_rotation_momentum, event_driven_fade, statistical_pairs |
| sector_rotation_momentum | trend_following_breakout, regime_conditional_carry, earnings_drift_pead |
| event_driven_fade | earnings_drift_pead, mean_reversion_pullback, volatility_contraction |
| statistical_pairs | mean_reversion_pullback, volatility_contraction, regime_conditional_carry |
