# 플레이북: PHL 토큰 실행

> Claude Code가 PHL 토큰을 받았을 때 따르는 실행 체크리스트.

---

## 사전 조건

- [ ] `PHL_SPEC.md` 읽었는가?
- [ ] `PHL_INDEX.json`에서 토큰 매핑 확인했는가?
- [ ] 해당 토큰 정의 파일(`/phl/tokens/PHL-{Name}.md`) 읽었는가?
- [ ] 관련 공통 계약(`/phl/contracts/*`) 확인했는가?

---

## 실행 순서

### 1. Loaded Specs 보고
```
읽은 파일:
- PHL_SPEC.md
- PHL_INDEX.json
- /phl/tokens/PHL-{Name}.md
- /phl/contracts/{relevant}.md
```

### 2. 상태 점검
- [ ] 대상 모듈/파일 존재 확인
- [ ] 현재 테스트 상태 확인 (통과/실패/없음)
- [ ] git 상태 확인 (clean/dirty)
- [ ] 의존성 상태 확인

### 3. Plan 작성 및 보고
- [ ] 토큰 Procedure의 각 Step을 현재 프로젝트에 매핑
- [ ] Non-Goals 확인 (하지 말아야 할 것)
- [ ] 사용자에게 Plan 보여주고 진행 여부 확인
  - 범위가 명확하면: 바로 실행
  - 범위가 모호하면: 질문 먼저

### 4. 실행
- [ ] Step별로 순차 수행
- [ ] 각 Step 완료 시 중간 보고 (큰 변경일 경우)
- [ ] 에러 발생 시: Questions Policy에 따라 질문 또는 Rollback

### 5. 검증
- [ ] 토큰 정의의 Validation 항목 전체 수행
- [ ] 공통 계약 준수 확인 (에러 처리, 로깅, 보안)
- [ ] 기존 테스트 regression 확인

### 6. 커밋
- [ ] `/phl/contracts/commit.md` 형식에 따라 메시지 작성
- [ ] 변경 파일 목록 확인
- [ ] 커밋 실행
- [ ] push

### 7. 결과 보고
```
## Changes
- [파일별 변경 요약]

## Validation
- [테스트 결과]
- [린트 결과]

## Commit
- [커밋 해시 + 메시지]

## Notes
- [리스크/후속 작업]
```

---

## 실패 시

| 상황 | 대응 |
|------|------|
| Step 중간에 실패 | 성공 부분만 커밋, 실패 부분 로그 |
| 테스트 실패 | 수정 시도 → 불가 시 revert |
| 범위 초과 발견 | 사용자에게 보고, 추가 토큰 제안 |
| 정의되지 않은 상황 | 질문 (추측 금지) |
