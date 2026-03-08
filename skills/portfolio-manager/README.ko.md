# Portfolio Manager

Alpaca MCP Server와 통합해 실시간 보유 종목 데이터를 가져오고, 리밸런싱 권고를 포함한 상세 포트폴리오 보고서를 생성하는 종합 포트폴리오 분석/관리 스킬입니다.

## 개요

Portfolio Manager는 여러 관점에서 투자 포트폴리오를 분석합니다:

- **자산 배분 (Asset Allocation)** - 주식/채권/현금 분포와 목표 배분 비교
- **분산 투자 (Diversification)** - 섹터 분해, 포지션 집중도, 상관관계 분석
- **리스크 평가 (Risk Assessment)** - 포트폴리오 베타, 변동성, 최대 낙폭, 리스크 점수
- **성과 검토 (Performance Review)** - 승자/패자, 절대/상대 수익률, 벤치마크 비교
- **포지션 분석 (Position Analysis)** - 개별 보유 종목 상세 평가 (HOLD/ADD/TRIM/SELL 권고)
- **리밸런싱 계획 (Rebalancing Plan)** - 포트폴리오 배분 최적화를 위한 구체적 액션

## 기능

✅ **Alpaca 통합** - Alpaca MCP Server를 통해 포지션 자동 조회  
✅ **다차원 분석** - 자산군, 섹터, 지역, 시가총액, 스타일 분석  
✅ **리스크 지표** - Beta, 변동성, Drawdown, 집중도, HHI  
✅ **포지션 평가** - 투자 아이디어 검증, 밸류에이션, 비중 적정성, 상대 기회  
✅ **리밸런싱 권고** - 우선순위 기반 액션 (TRIM/ADD/HOLD/SELL)  
✅ **종합 보고서** - 저장소에 Markdown 보고서 저장  
✅ **모델 포트폴리오** - Conservative/Moderate/Growth/Aggressive 벤치마크 비교

## 사전 준비

### 필수: Alpaca 계정 및 MCP Server

이 스킬을 사용하려면 다음이 필요합니다:

1. **Alpaca Brokerage Account** (paper 또는 live)
   - 가입: https://alpaca.markets/
   - 테스트에는 Paper trading account(무료, 가상자금) 권장

2. **Claude에 Alpaca MCP Server 구성**
   - MCP 도구를 통해 포트폴리오 포지션 접근 제공
   - 설정 가이드: `references/alpaca-mcp-setup.md`

3. **API Credentials** (API Key ID, Secret Key)
   - Alpaca 대시보드에서 생성
   - 환경 변수 설정:
     ```bash
     export ALPACA_API_KEY="your_api_key_id"
     export ALPACA_SECRET_KEY="your_secret_key"
     export ALPACA_PAPER="true"  # 실거래는 "false"
     ```

### 선택 사항: 수동 데이터 입력

Alpaca MCP Server를 사용할 수 없다면 CSV로 포트폴리오 데이터를 수동 제공할 수 있습니다:

```csv
symbol,quantity,cost_basis,current_price
AAPL,100,150.00,175.50
MSFT,50,280.00,310.25
```

## 설치

### Claude Desktop/Code 사용자

1. **스킬을 Claude Skills 디렉터리로 복사:**
   ```bash
   cp -r portfolio-manager ~/.claude/skills/
   ```

2. 스킬 감지를 위해 **Claude 재시작**

3. **Alpaca credentials 구성** (사전 준비 섹션 참고)

### Claude Web App 사용자

1. **스킬 패키지 다운로드:**
   - `skill-packages/portfolio-manager.skill`

2. **Claude에 업로드:**
   - Claude 웹 인터페이스에서 "+" 클릭
   - "Upload Skill" 선택
   - `portfolio-manager.skill` 선택

3. **참고:** 웹 버전에서는 Alpaca MCP Server가 제한될 수 있으므로 수동 CSV 입력 사용

## 사용법

### 기본 포트폴리오 분석

Claude에게 포트폴리오 분석을 요청하세요:

```
"Analyze my portfolio"
"Review my current positions"
"How's my portfolio doing?"
```

스킬 동작:
1. MCP를 통해 Alpaca에서 포지션 조회
2. 시장 데이터로 데이터 보강
3. 종합 분석 수행
4. 상세 보고서 생성
5. 리밸런싱 권고 제공

### 분석 유형별 예시

**자산 배분 점검:**
```
"What's my current asset allocation?"
"Am I properly diversified?"
```

**리스크 평가:**
```
"How risky is my portfolio?"
"What's my portfolio beta?"
"What are my biggest risks?"
```

**리밸런싱:**
```
"Should I rebalance my portfolio?"
"What should I buy or sell?"
"Is anything too concentrated?"
```

**포지션 리뷰:**
```
"Should I sell Tesla?"
"Is Apple overweight in my portfolio?"
"What should I do with my tech stocks?"
```

**성과:**
```
"What are my best performing stocks?"
"Which positions are losing money?"
"How am I doing vs the S&P 500?"
```

## 분석 결과물

Portfolio Manager는 다음을 포함한 종합 Markdown 보고서를 생성합니다:

### 1. Executive Summary
- 포트폴리오 전반 상태
- 핵심 강점과 우려 사항
- 주요 권고

### 2. Holdings Overview
- 모든 포지션의 수량, 가치, 손익

### 3. Asset Allocation Analysis
- 현재 배분 vs 목표 배분
- 섹터 분해
- 지역 분포
- 시가총액 분포

### 4. Diversification Assessment
- 포지션 집중도 분석
- 섹터 분산 점수
- 상관관계 리스크
- HHI 집중도 지수

### 5. Risk Assessment
- 포트폴리오 베타와 변동성
- 최대 낙폭
- 리스크 집중 구간
- 종합 리스크 점수

### 6. Performance Review
- 총 포트폴리오 가치 및 손익
- 최고/최저 성과 종목
- 벤치마크 대비 성과(가능 시)

### 7. Position Analysis
- 상위 10-15개 보유 종목 상세 분석
- 투자 아이디어 검증
- 밸류에이션 평가
- 포지션 비중 적정성
- HOLD/ADD/TRIM/SELL 권고

### 8. Rebalancing Recommendations
- 우선순위별 액션 (High/Medium/Low)
- 구체적 거래 권고
- 현금 배치 제안
- 세금 고려 사항

### 9. Action Items
- 즉시 조치 항목
- 중기 과제
- 모니터링 우선순위

**보고서 경로:** 저장소 루트의 `portfolio_analysis_YYYY-MM-DD.md`

## 참고 자료

스킬에는 다음 참고 문서가 포함됩니다:

- **`references/alpaca-mcp-setup.md`** - Alpaca API 설정 가이드
- **`references/asset-allocation.md`** - 자산 배분 이론과 프레임워크
- **`references/diversification-principles.md`** - 분산 투자 개념과 지표
- **`references/portfolio-risk-metrics.md`** - 리스크 측정과 해석
- **`references/position-evaluation.md`** - 포지션 분석 프레임워크
- **`references/rebalancing-strategies.md`** - 리밸런싱 방법론
- **`references/target-allocations.md`** - 위험 성향별 모델 포트폴리오
- **`references/risk-profile-questionnaire.md`** - 위험 성향 진단

분석 과정에서 필요 시 이 참고 문서들이 자동 로드됩니다.

## Alpaca 연결 테스트

스킬 사용 전 Alpaca API 연결을 테스트하세요:

```bash
python3 portfolio-manager/scripts/test_alpaca_connection.py
```

예상 출력:
```
✓ Successfully connected to Alpaca API
Account Status: ACTIVE
Equity: $100,000.00
Cash: $50,000.00
Buying Power: $200,000.00
Positions: 5
```

오류가 발생하면 `references/alpaca-mcp-setup.md`의 트러블슈팅을 참고하세요.

## 예시 워크플로

### 초기 포트폴리오 점검

1. **분석 트리거:**
   ```
   User: "Analyze my portfolio"
   ```

2. **스킬 워크플로:**
   - Alpaca MCP에서 포지션 조회
   - 계정 정보 조회
   - 각 포지션의 시장 데이터 수집
   - 종합 분석 수행
   - 상세 보고서 생성

3. **생성 보고서:**
   - `portfolio_analysis_2025-11-08.md`
   - 모든 분석 섹션 포함
   - 구체적 권고 제시

4. **후속 질문:**
   ```
   User: "Why should I trim NVDA?"
   User: "What should I buy instead?"
   User: "Is my tech allocation too high?"
   ```

### 지속 모니터링

**분기 리뷰:**
```
User: "Review my portfolio for Q4 2025"
```

**시장 이벤트 이후:**
```
User: "How did the market crash affect my portfolio?"
```

**리밸런싱 전:**
```
User: "Generate rebalancing recommendations"
```

## 핵심 개념

### Asset Allocation
포트폴리오를 자산군(주식, 채권, 현금)으로 배분하는 것. 포트폴리오 리스크와 수익의 주요 결정 요인입니다.

### Diversification
비체계적 리스크를 줄이기 위해 포지션/섹터/지역에 걸쳐 투자하는 것.

### Rebalancing
목표 배분을 유지하기 위해 과대 비중 포지션을 매도하고 과소 비중 포지션을 매수하는 체계적 조정.

### Position Sizing
확신도, 리스크, 포트폴리오 제약을 고려해 각 보유 종목의 적정 비중을 결정하는 것.

### Risk-Adjusted Returns
감수한 리스크 대비 성과를 평가하는 지표 (Sharpe ratio, Sortino ratio).

### Concentration Risk
단일 포지션/섹터/테마에 과도하게 노출되어 포트폴리오 리스크가 상승하는 상태.

## 제한 사항 및 고지

**중요 안내:**

1. **Not Financial Advice** - 이 도구는 정보 제공 목적의 분석이며 개인 맞춤형 투자 자문이 아닙니다.

2. **Data Accuracy** - 분석 품질은 Alpaca API 데이터 정확도와 제3자 시장 데이터 품질에 의존합니다.

3. **Market Conditions** - 과거 기반 분석은 특히 레짐 전환 구간에서 미래 성과를 보장하지 않습니다.

4. **Tax Implications** - 세금 영향 추정은 근사치이며, 세무 전문 상담이 필요합니다.

5. **Execution Risk** - 권고는 현재 시장 가격에서 거래를 체결할 수 있다는 가정에 기반합니다.

**항상 다음을 수행하세요:**
- 핵심 데이터는 독립적으로 검증
- 중대한 의사결정 전 자격 있는 재무 전문가 상담
- 본인 상황/위험 성향/목표 반영
- 세금 영향은 세무 전문가와 검토

## 트러블슈팅

### "Alpaca MCP Server not connected"

**해결 방법:**
1. MCP 서버 실행 상태 확인 (`claude mcp status` 사용 가능 시)
2. 환경 변수 확인: `echo $ALPACA_API_KEY`
3. Claude 재시작으로 MCP 서버 재초기화
4. Alpaca 대시보드에서 API 키 검증
5. 상세 설정은 `references/alpaca-mcp-setup.md` 참고

### "Invalid API credentials"

**해결 방법:**
1. API Key ID/Secret Key 오타 및 공백 확인
2. `ALPACA_PAPER` 설정과 키 종류 일치 여부 확인 (paper vs live)
3. Alpaca 대시보드에서 키 재발급
4. 계정 상태 active 확인

### "No positions found"

**해결 방법:**
1. Alpaca 대시보드에 포지션 존재 여부 확인
2. 올바른 계정(paper/live) 확인
3. 계정 번호 일치 확인
4. Claude에 포지션 재조회 요청

### 보고서가 부정확해 보일 때

**해결 방법:**
1. Alpaca 데이터 최신성 확인 (Alpaca 대시보드)
2. 시장 데이터 지연 여부 확인 (무료 티어는 15분 지연)
3. 핵심 포지션 일부 수동 검증
4. 분석 개선을 위해 불일치 사례 공유

## 버전 히스토리

- **v1.0** (2025년 11월) - 초기 릴리스
  - Alpaca MCP Server 통합
  - 종합 포트폴리오 분석
  - 다차원 리스크 평가
  - 포지션 평가 프레임워크
  - 리밸런싱 권고
  - 모델 포트폴리오 벤치마크

## 지원 및 기여

**이슈 대응:**
- `references/` 문서 확인
- 위 트러블슈팅 섹션 검토
- `test_alpaca_connection.py`로 연결 테스트
- Alpaca API 상태 확인: https://status.alpaca.markets/

**문의:**
- Alpaca API docs: https://alpaca.markets/docs/
- Alpaca community: https://forum.alpaca.markets/

**스킬 개선 아이디어:**
- 추가 브로커 통합 (Interactive Brokers, Schwab)
- 옵션 포트폴리오 분석
- 팩터 노출 분석
- 몬테카를로 은퇴 시뮬레이션
- Tax-loss harvesting 자동화

## 관련 스킬

다음 스킬과 함께 사용하면 효과적입니다:

- **US Stock Analysis** - 개별 포지션 심층 분석
- **Value Dividend Screener** - 리밸런싱 대체 종목 탐색
- **Market News Analyst** - 최근 시장 이벤트 해석
- **Sector Analyst** - 섹터 로테이션 분석
- **US Market Bubble Detector** - 시장 전반 리스크 환경 점검

## 라이선스

라이선스 정보는 저장소 루트를 참고하세요.

---

**기억하세요:** 성공적인 포트폴리오 관리는 규율, 인내, 장기 시각이 핵심입니다. 이 스킬로 체계적 접근을 유지하고 감정적 의사결정을 줄이세요. 가장 좋은 포트폴리오는 모든 시장 환경에서 지속할 수 있는 포트폴리오입니다.
