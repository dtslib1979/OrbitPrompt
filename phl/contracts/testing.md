# 공통 계약: 테스트

> 모든 PHL 토큰 실행 시 이 규칙을 따른다.

## 필수 테스트 경로

| 경로 | 설명 |
|------|------|
| Happy path | 정상 입력 → 정상 출력 |
| Error path | 비정상 입력 → 에러 핸들링 동작 확인 |
| Boundary | 빈 입력, null, 최대값, 특수문자 |

## 테스트 네이밍

```
test_[모듈]_[동작]_[조건]_[기대결과]
```

예시:
```
test_parseConfig_validJSON_returnsObject
test_parseConfig_nullInput_throwsError
test_parseConfig_emptyString_returnsDefault
```

## 원칙

1. **PHL 토큰 실행 후 테스트가 통과해야 커밋 가능.** 테스트 실패 상태에서 커밋 금지.
2. **기존 테스트를 깨뜨리지 않는다.** regression 확인 필수.
3. **테스트가 없는 모듈에 PHL 적용 시:** 테스트부터 먼저 작성.
4. **Mock은 최소한으로.** 가능하면 실제 동작 테스트.

## 프로젝트별 테스트 도구

이 레포(OrbitPrompt)는 바닐라 HTML/JS이므로:
- 단위 테스트: 함수 단위 수동 검증 또는 간단한 테스트 스크립트
- 통합 테스트: 브라우저에서 Setup → Broadcast 모드 전환 확인
- 다른 레포에서는 해당 프로젝트의 테스트 프레임워크를 따른다
