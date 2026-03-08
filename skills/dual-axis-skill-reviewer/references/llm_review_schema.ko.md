# LLM 리뷰 JSON 스키마

LLM-axis 리뷰를 요청할 때 이 스키마를 사용하세요.

## 필수 JSON 형태

```json
{
  "score": 0,
  "summary": "one-paragraph assessment",
  "findings": [
    {
      "severity": "high|medium|low",
      "path": "skills/<skill-name>/file.ext",
      "line": 0,
      "message": "problem statement",
      "improvement": "concrete fix"
    }
  ]
}
```

## 제약 조건

- JSON만 반환하세요 (markdown wrapper 금지).
- `score`는 `0..100` 범위로 설정하세요.
- 알 수 없는 경우 `line`을 `null`로 설정하세요.
- `severity`는 `high`, `medium`, `low`만 사용하세요.
- `message`는 구체적이고 테스트 가능해야 합니다.
- `improvement`는 실행 가능해야 하며, 가능하면 파일 단위 대상을 포함하세요.

## 리뷰 초점

- 스크립트(`scripts/*.py`)의 로직과 동작을 검증합니다.
- `SKILL.md` 지침과 실제 스크립트 동작 간 불일치를 점검합니다.
- 테스트 누락과 회귀 리스크를 점검합니다.
- 실행 신뢰성을 낮추는 모호한 지침을 식별합니다.
