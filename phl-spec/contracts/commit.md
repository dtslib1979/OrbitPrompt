# 공통 계약: 커밋

> 모든 PHL 토큰 실행 시 이 규칙을 따른다.

## 커밋 메시지 형식

```
PHL-{토큰}: {대상} - {요약}

- {카테고리1}: {변경 내용}
- {카테고리2}: {변경 내용}

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## 예시

```
PHL-Expansion: parseConfig - 에러 처리 강화 및 테스트 추가

- 에러 처리: null 입력 시 명시적 에러 반환
- 로깅: 파싱 실패 지점에 ERROR 로그 추가
- 테스트: happy/error/boundary 3경로 테스트 추가

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## 커밋 단위

| 상황 | 단위 |
|------|------|
| PHL 토큰 1개 실행 | 1 커밋 (모든 변경 포함) |
| PHL 토큰 실행 중 버그 발견 | 별도 `fix:` 커밋으로 분리 |
| PHL 토큰 실행 범위가 큰 경우 | Step별로 커밋 가능 (사용자 확인 후) |

## 원칙

1. **squash 금지.** 커밋은 전표다. 뭉개지 않는다 (헌법 제1조).
2. **`reset --hard` 금지.** 되돌릴 때는 `git revert` (헌법 제2조).
3. **증빙 없는 커밋 금지.** 메시지에 이유와 변경 내용 필수.
4. **Co-Authored-By 필수.** AI/Human 협업 기록.
