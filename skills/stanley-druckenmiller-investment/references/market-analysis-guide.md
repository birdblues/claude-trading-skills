# 드러켄밀러식 시장 분석 가이드

## 매크로 경제 분석 프레임워크

### 1. 중앙은행 정책의 평가

#### 분석 포인트
- **금리 정책의 방향성**: 완화·중립·긴축 사이클의 위치
- **유동성의 변화**: 머니서플라이, QE/QT의 동향
- **정책의 지속 가능성**: 과도한 정책의 징후를 탐색
- **시장 기대와의 괴리**: 중앙은행의 의도와 시장 이해의 갭

#### 경계해야 할 정책 실수의 신호
- 장기간의 극단적인 저금리 유지
- 인플레이션 압력을 무시한 완화 지속
- 지나치게 급격한 정책 전환
- 시장과의 커뮤니케이션 실패

### 2. 18개월 앞의 미래 예측

#### 예측의 구성 요소
1. **경제 사이클의 위치**
   - 확장 초기·중기·후기·감속·후퇴 중 어느 단계인가
   - 다음 전환점은 언제쯤인가

2. **정책 사이클과의 관계**
   - 금융 정책은 경제에 대해 선행적인가 후행적인가
   - 재정 정책의 영향도

3. **시장 기대의 반영도**
   - 컨센서스 예상은 낙관적인가 비관적인가
   - 서프라이즈의 가능성은 어디에 있는가

### 3. 글로벌 자산 배분의 결정

#### 자산 클래스별 평가 기준

**주식**
- 유동성 환경 (완화적인가 긴축적인가)
- 기업 이익의 방향성 (개선인가 악화인가)
- 밸류에이션 (고평가인가 저평가인가)
- 센티먼트 (낙관인가 비관인가)

**채권**
- 금리의 방향성 예측
- 일드 커브의 형태
- 크레딧 스프레드의 동향
- 인플레이션 기대

**통화**
- 금리 차의 동향
- 경상수지 상황
- 정치적 안정성
- 자본 플로우의 방향

**커모디티**
- 수급 밸런스
- 달러의 강약
- 인플레이션/디플레이션 압력
- 지정학 리스크

## From Data to Decision (시그널→액션 변환)

The Strategy Synthesizer uses the following rules to convert multi-skill signals into actionable decisions. See `references/conviction_matrix.md` for the full cross-reference tables.

### Green Light Conditions (Aggressive Posture)
- Breadth composite >= 60 **AND** Uptrend zone = Bull/Strong Bull
- Market Top score < 40 (low distribution risk)
- Macro Regime = broadening **AND** confidence = high
- FTD state = FTD_CONFIRMED (if applicable)
- **Action:** 80-100% equity, concentrated positions, standard stops

### Yellow Light Conditions (Cautious Posture)
- Breadth composite 40-59 **OR** Uptrend zone = Neutral
- Market Top score 40-60 (moderate risk)
- Macro Regime = transitional
- Mixed signal convergence (convergence score 40-60)
- **Action:** 50-70% equity, reduced sizing, tighter stops

### Red Light Conditions (Defensive Posture)
- Breadth composite < 40 **OR** Uptrend zone = Bear
- Market Top score >= 60 (elevated/high risk)
- Macro Regime = contraction
- FTD state = RALLY_FAILED
- **Action:** 0-30% equity, high cash, no new entries

### Pattern-Specific Overrides
- **Policy Pivot detected:** Overweight bonds + equity even if signals are mixed (anticipate regime shift)
- **Unsustainable Distortion detected:** Override green light → reduce to yellow light minimum
- **Extreme Contrarian detected:** Override red light → allow pilot equity entries (FTD confirmation)

---

## 포지션 구축의 실전

### 확신도의 평가 기준

#### 고확신도 (크게 베팅)의 조건
1. **복수의 요인이 같은 방향을 가리킨다** ("오리가 줄을 선다")
2. **시장 컨센서스와 크게 괴리**
3. **리스크·리워드가 매우 유리**
4. **명확한 촉매(카탈리스트)가 존재**

#### 저확신도 (관망)의 신호
- 상반되는 시그널이 혼재
- 불확실성이 극도로 높다
- 리스크·리워드가 불명확
- 타이밍을 읽을 수 없다

### 진입과 청산의 판단

#### 진입 조건
1. **테크니컬 확인**: 트렌드의 초기 단계를 확인
2. **펀더멘털**: 투자 테마가 명확
3. **센티먼트**: 과도한 낙관·비관의 존재
4. **리스크 관리**: 최대 손실이 허용 범위 내

#### 청산 조건
- **투자 이유의 소실**: 당초의 시나리오가 무너졌다
- **목표 달성**: 상정한 수익에 도달
- **더 좋은 기회**: 다른 곳에 더 매력적인 투자 기회가 출현
- **리스크 환경의 변화**: 시장 환경이 크게 변화

## 위기 대응 프로토콜

### 베어 마켓 진입의 징후

1. **금융 정책의 전환점**
   - 완화에서 긴축으로의 명확한 전환
   - 유동성의 급속한 수축

2. **신용 시장의 스트레스**
   - 크레딧 스프레드의 급확대
   - 은행 간 시장의 기능 부전

3. **센티먼트의 극단적인 낙관**
   - 전원이 강세
   - 리스크의 과소평가
   - 레버리지의 과잉 사용

### 위기 시의 행동 지침

1. **즉각적인 방어 태세**
   - 리스크 자산의 축소
   - 레버리지의 해소
   - 유동성의 확보

2. **안전 자산으로의 시프트**
   - 장기 국채
   - 금
   - 안전 통화 (엔, 스위스 프랑 등)

3. **역발상 기회의 탐색**
   - 과도한 매도로 인한 왜곡
   - 질로의 도피로 인한 우량 자산의 저평가
   - 정책 대응에 의한 전환점

## 일상적인 모니터링 항목

### 매일 체크해야 할 지표
- 주요국의 금리 동향
- 주식 시장의 내부 구조 (상승/하락 종목 수 등)
- 통화 시장의 움직임
- VIX 등의 볼라틸리티 지표
- 크레딧 시장의 동향

### 주간·월간 리뷰 항목
- 경제 지표의 예상과 실적의 괴리
- 중앙은행 고위 관계자의 발언 톤
- 자금 플로우 데이터
- 포지셔닝 데이터
- 센티먼트 지표

### 분기별 대국관 점검
- 투자 테마의 타당성 확인
- 18개월 앞 예측의 수정
- 포트폴리오 전체의 리스크 평가
- 새로운 투자 기회의 발굴
