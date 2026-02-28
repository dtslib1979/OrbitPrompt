# 공통 계약: 로깅

> 모든 PHL 토큰 실행 시 이 규칙을 따른다.

## 로그 레벨

| 레벨 | 용도 |
|------|------|
| `ERROR` | 실패, 예외, 복구 불가 |
| `WARN` | 비정상이지만 진행 가능 |
| `INFO` | 핵심 동작 기록 (함수 진입, 상태 전이) |
| `DEBUG` | 상세 디버깅 (역순 로깅, 변수 덤프) |

## 필수 로그 지점

- [ ] 함수 진입 (핵심 함수만): `INFO`
- [ ] 에러 발생: `ERROR` + 입력값 + 에러 객체
- [ ] 핵심 분기 (if/else 주요 갈림길): `INFO` 또는 `DEBUG`
- [ ] 외부 호출 전후: `INFO`

## 포맷

```
[LEVEL] [TIMESTAMP] [MODULE] message key=value key=value
```

예시:
```
[INFO] 2026-02-28T12:00:00Z [parseConfig] Loading config file path="/etc/app.json"
[ERROR] 2026-02-28T12:00:01Z [parseConfig] Parse failed input="null" error="Unexpected token"
```

## 금지

- 민감정보 로깅 (비밀키, 토큰, 비밀번호, 개인정보)
- `console.log("here")` 스타일 디버그 로그를 프로덕션에 남기기
- 로그 없는 catch 블록
