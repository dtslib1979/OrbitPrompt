# 플레이북: 새 PHL 토큰 정의

> 사용자가 새로운 PHL 토큰을 만들려 할 때 따르는 절차.

---

## 트리거

- "새 토큰 만들어" / "PHL-{Name} 정의해"
- 기존 토큰으로 커버되지 않는 반복 작업 패턴 발견 시

---

## 절차

### 1. 요구사항 수집
- [ ] Intent: 무엇을 달성하는가? (1문장)
- [ ] Scope: 어디까지 적용하는가?
- [ ] Non-Goals: 하지 말아야 할 것은?
- [ ] 기존 토큰과 겹치는 부분은?

### 2. 스펙 작성
- [ ] `/phl/tokens/PHL-{Name}.md` 파일 생성
- [ ] `PHL_SPEC.md` 섹션 5의 스키마 준수:
  ```yaml
  Name, Intent, Scope, Non-Goals, Preconditions,
  Procedure, Validation, Artifacts,
  Commit Policy, Rollback Policy, Questions Policy
  ```
- [ ] Procedure는 체크리스트 형태로 (Step별)
- [ ] Questions Policy는 구체적으로 (어떤 상황에서 무엇을 질문)

### 3. 인덱스 등록
- [ ] `PHL_INDEX.json`의 `tokens` 객체에 추가:
  ```json
  "PHL-{Name}": {
    "file": "/phl/tokens/PHL-{Name}.md",
    "intent": "1문장 요약",
    "aliases": ["한국어 별칭", "영어 별칭"],
    "category": "카테고리"
  }
  ```

### 4. SPEC 레지스트리 갱신
- [ ] `PHL_SPEC.md` 섹션 8 (토큰 레지스트리) 테이블에 행 추가

### 5. 검증
- [ ] 토큰 정의가 스키마를 완전히 충족하는가?
- [ ] 기존 토큰과 Non-Goals 충돌이 없는가?
- [ ] aliases가 기존 토큰과 겹치지 않는가?

### 6. 커밋
```
PHL-Define: PHL-{Name} - 새 토큰 정의

- 토큰: /phl/tokens/PHL-{Name}.md
- 인덱스: PHL_INDEX.json 업데이트
- 레지스트리: PHL_SPEC.md 업데이트

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

---

## 토큰 품질 기준

| 기준 | 통과 조건 |
|------|-----------|
| Intent | 1문장으로 명확 |
| Procedure | 체크리스트 형태, 3개 이상 Step |
| Validation | 측정 가능한 성공 기준 |
| Non-Goals | 최소 1개 이상 명시 |
| Questions Policy | 최소 2개 이상 질문 시나리오 |
| Rollback Policy | 실패 시 대응 명시 |
