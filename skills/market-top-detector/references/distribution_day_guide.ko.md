# Distribution Day 가이드

## Distribution Day란?

Distribution Day는 주요 주가지수(S&P 500 또는 NASDAQ Composite)가 전일 종가 대비 0.2% 이상 하락하면서 거래량이 전 거래일보다 증가한 날을 의미합니다. 이는 기관투자자가 물량을 동반해 주식을 매도하며 보유분을 "분산(distributing)"하고 있음을 시사합니다.

William O'Neil은 "How to Make Money in Stocks"에서 이를 상승 추세가 압박받고 있음을 보여주는 가장 신뢰도 높은 신호 중 하나로 소개했습니다.

## 정확한 규칙

### Distribution Day 기준 (두 조건 모두 충족):
1. **가격 하락 >= 0.2%** (전일 종가 대비)
2. **거래량 > 전일 거래량** (소폭 증가도 인정)

### Stalling Day 기준 (두 조건 모두 충족):
1. **거래량 > 전일 거래량** (기관 활동 존재)
2. **가격 상승 < 0.1%** (거래량 대비 가격 전진 실패)
3. Stalling day는 유효 카운트에서 **0.5 distribution days**로 계산

### 25일 만료 규칙:
- Distribution day는 **25거래일** 경과 시 자동 만료(약 5주)
- 롤링 25일 창(window)만 중요
- 오래된 분산 신호가 현재 판단을 왜곡하지 않도록 방지

### Distribution으로 보지 않는 경우:
- 거래량 감소를 동반한 지수 하락(일반적 차익실현)
- 큰 갭상승 후 소폭 음봉 마감(여전히 순상승일)
- 평균 이하 거래량(기관 참여 부족)

## 카운팅과 해석

| Effective Count | Interpretation | Action |
|----------------|----------------|--------|
| 0-1 | 건강한 시장 | 일반 운영 |
| 2-3 | 매도 압력 일부 있으나 정상 범위 | 면밀 모니터링 |
| 4 | O'Neil 초기 경고 | 손절 기준 강화 |
| 5 | 유의미한 분산 | 익스포저 축소 |
| 6+ | 강한 분산 | 적극적 자본 보호 |

**Effective Count 공식:**
```
Effective Count = Distribution Days + (0.5 × Stalling Days)
```

## 듀얼 인덱스 접근

이 도구는 S&P 500과 NASDAQ(QQQ 대용)를 모두 모니터링합니다. 두 지수 중 더 높은 effective count를 점수화에 사용합니다. 이유는 다음과 같습니다.

1. 한 지수에서 분산이 먼저 집중될 수 있음
2. NASDAQ은 성장주 비중이 높아 선행하는 경우가 많음
3. 둘 중 더 나쁜 신호를 반영하는 보수적 접근이 유리

## 시장 고점에서 자주 보이는 패턴

### 전형적 Distribution 시퀀스 (2022 사례):
1. 1주차: distribution day 1회(겉보기엔 경미)
2. 2주차: distribution day 2회 추가
3. 3주차: stalling day 1회(반등에서 매도 출회)
4. 4주차: distribution day 2회 추가(총 5-6 effective)
5. 직후 시장 붕괴 진행

### False Alarm 패턴:
1. 짧은 기간 distribution day 2회 발생
2. 시장 강한 반등으로 우려 해소
3. 분산일이 임계치 도달 전에 만료
4. 상승 추세 지속

### 핵심 구분점:
Distribution day의 **클러스터링**이 중요합니다. 5주에 걸쳐 3회보다 1주 내 3회가 훨씬 위험 신호입니다.

## Follow-Through Day (FTD)

FTD는 distribution day의 반대 개념으로, 조정 후 새로운 상승 추세 시작 가능성을 시사합니다.

### FTD 규칙:
1. **Rally Attempt:** 시장이 저점을 만들고 반등 시작(첫 상승일)
2. **카운팅 시작:** rally attempt day를 day 1로 계산
3. **FTD 발생 구간 Day 4-7:** 의미 있는 상승(>1.5%) + 전일 대비 거래량 증가
4. **확인:** day 4 이전 랠리(day 1-3)는 신뢰도 낮음

### FTD 신뢰도:
- 모든 FTD가 지속 상승으로 이어지지 않음(약 25% 실패)
- 짧은 기간 다중 FTD 출현 시 신뢰도 상승
- breadth 개선과 결합될 때 성능 향상
- O'Neil: "I never try to buy at the bottom. I wait for the Follow-Through Day."

## 실전 팁

### Distribution 모니터링 시:
1. 불확실한 시장에서는 DAILY로 카운트 점검
2. 카운트 3 도달 시(사전 경고 구간) 특히 주의
3. 4+에서는 다른 신호와 무관하게 방어 조치 시작
4. 6+까지 기다리지 말 것 - 그때는 이미 손상이 클 수 있음

### 흔한 실수:
1. **Stalling day 무시:** 미묘하지만 의미가 큼
2. **수동 리셋:** 25일 만료 규칙을 신뢰해야 함
3. **잘못된 거래량 비교:** 평균 대비가 아니라 전일 대비 비교가 기준
4. **지수 혼합 카운팅:** S&P 500과 NASDAQ은 별도 계산
5. **맥락 무시:** 강한 상승장 4회와 박스권 4회는 의미가 다름
