# 에지의 인스티튜셔널라이제이션 프로세스

일상의 "떠오른 아이디어"를, 속인적 메모로 끝내지 않고, 재현 가능한 전략 자산으로 승격시키기 위한 표준 플로우.

## 목적

- 관찰 -> 추상화 -> 전략화 -> 파이프라인 검증을 분업화한다
- 각 단계에서 "승급 게이트"를 정의하여 품질을 맞춘다
- 에지의 생성과 열화 모니터링을 동일한 운용 체계에 탑재한다

## 1. 3스킬 구성 + 파이프라인 접속

### 1-1. 메인라인

```mermaid
flowchart TD
    A[edge-hint-collector<br/>관찰의 구조화<br/>output: hints.yaml]
    B[edge-concept-synth<br/>가설의 추상화<br/>output: edge_concepts.yaml]
    C[edge-strategy-export<br/>전략화/엑스포트<br/>output: strategy.yaml + metadata.json]
    D[trade-strategy-pipeline<br/>Phase I -> IS Gate -> Walk-Forward<br/>-> OOS Gate -> Robustness -> Paper -> Live]

    A --> B --> C --> D
```

### 1-2. 반려 루프 (게이트 운용)

```mermaid
flowchart TD
    H0[edge-hint-collector]
    C0[edge-concept-synth]
    S0[edge-strategy-export]
    P0[trade-strategy-pipeline]

    G1{"Concept Gate<br/>메커니즘 가설 + 성립 조건 + FMEA<br/>사전 등록(평가 기준/성공 임계값)"}
    G2{"Spec Gate<br/>StrategySpec 적합 체크"}
    G3{"Coverage Gate<br/>비대응은 research-only로 보류"}
    G4{"Pipeline Gate<br/>IS/OOS/Robustness를 통과"}

    H0 --> C0
    C0 --> G1
    G1 -->|Fail| H0
    G1 -->|Pass| S0
    S0 --> G2
    G2 -->|Fail| C0
    G2 -->|Pass| G3
    G3 -->|보류| C0
    G3 -->|export 대상| P0
    P0 --> G4
    G4 -->|Fail| C0
    G4 -->|Pass| L0[Paper/Live로 승격]
```

### 1-3. 구현 매핑 (현 리포지토리)

| 논리 스킬명 | 현재 구현 |
|---|---|
| edge-hint-collector | `skills/edge-hint-extractor` |
| edge-concept-synth | `skills/edge-concept-synthesizer` |
| edge-strategy-export | `skills/edge-strategy-designer` + `skills/edge-candidate-agent` (`export_candidate.py` / `validate_candidate.py`) |

## 2. 에지의 승급 스테이트 (진학 모델)

```mermaid
stateDiagram-v2
    [*] --> Hint
    Hint --> Ticket: 관찰 근거 있음
    Ticket --> Concept: 복수 증거를 추상화
    Concept --> Draft: 룰화 가능
    Draft --> Candidate: v1 I/F에 매핑 가능
    Candidate --> Phase1Pass: validate + dry-run pass
    Phase1Pass --> BacktestPass: 기대값/안정성 pass
    BacktestPass --> Paper: 페이퍼 운용으로 재현
    Paper --> LiveSmall: 소량 실운용
    LiveSmall --> Live: 지속 재현
    Live --> Monitor
    Monitor --> Concept: 열화 탐지로 재설계
    Monitor --> Retired: 유의한 열화가 지속
```

## 3. 일간/주간 운용 리듬

```mermaid
flowchart TD
    subgraph Daily[Daily Loop]
        D1[관찰 데이터 갱신] --> D2[hints 생성]
        D2 --> D3[자동 탐지로 ticket 생성]
        D3 --> D4[개념 추상화]
        D4 --> D5[전략 드래프트 갱신]
    end

    subgraph Weekly[Weekly Review]
        W1[Concept Review<br/>채택/보류/각하] --> W2[검증 큐 우선순위 갱신]
        W2 --> W3[파이프라인 투입 계획]
    end

    subgraph Monthly[Monthly Governance]
        M1[열화 모니터링 리뷰] --> M2[현역 에지의 지속/축소/퇴역]
        M2 --> M3[가설 라이브러리 갱신]
    end

    D5 --> W1
    W3 --> M1
```

## 4. 승급 게이트의 최소 요건

| 게이트 | 최소 요건 | 실격 조건 |
|---|---|---|
| Concept Gate | thesis + invalidation_signals가 명시되어 있음 | 가설이 관찰의 환언에 불과 |
| Draft Gate | entry/exit/risk/cost가 정의 완료 | 비용 미고려, 구현 불가 조건 |
| Pipeline Gate | `edge-finder-candidate/v1` 계약을 충족 | schema 위반, dry-run 실패 |
| Promotion Gate | OOS에서 재현하며, 열화 모니터링 가능 | 특정 기간만 유효, 용량 부족 |

## 5. 우선 확인 포인트

1. `edge_concepts.yaml`의 `abstraction.thesis`와 `invalidation_signals`
2. `strategy_drafts/*.yaml`의 `risk`와 `validation_plan`
3. `validate_candidate.py` 결과 (I/F 적합)
4. 파이프라인 결과의 재현성 (기간 분할/레짐 분할)
