# PHL_SPEC.md — Single Source of Truth

> **이 파일은 PHL 프로토콜의 최상위 규칙이다.**
> Claude Code는 PHL 토큰을 받으면 이 파일을 먼저 읽는다.

---

## 1. PHL이란

PHL(Protocol for Human Language)은 **의미 압축 프로토콜**이다.
사용자가 짧은 토큰(1~3단어)을 말하면, Claude Code가 레포에 정의된 엄격한 규칙을 로드하여 실행한다.

**PHL은 단축키가 아니다. 상태 전이(state transition) 인터페이스다.**

---

## 2. 실행 사이클 (필수)

PHL 토큰을 받으면 Claude는 **반드시** 이 순서를 따른다:

```
1. SPEC 로드    → 이 파일 + PHL_INDEX.json + 해당 토큰 정의 파일 읽기
2. 상태 점검    → 현재 파일 구조/테스트/로그/의존성 확인
3. 계획 보고    → Plan을 사용자에게 보여줌
4. 실행         → 변경 수행
5. 검증         → 테스트/린트/타입체크/빌드
6. 산출         → 코드/문서/CHANGELOG 업데이트
7. 커밋         → 커밋 메시지 규칙에 따라 commit
8. 상태 갱신    → push하여 다음 작업 기준점 확정
```

---

## 3. 표준 출력 형식

PHL 토큰 실행 시 Claude는 **항상** 아래 형식으로 보고한다:

```
## Loaded Specs
- [읽은 파일 목록]

## Plan
1. [단계별 계획]

## Changes
- [파일 단위 변경 요약]

## Validation
- [실행한 검증 결과]

## Commit
- [커밋 메시지/범위]

## Notes
- [리스크/추가 제안]
```

---

## 4. 질문(Ask) 규칙

다음 중 **하나라도** 해당하면 반드시 질문한다. 추측하지 않는다:

| 상황 | 질문 |
|------|------|
| 범위가 모호함 | "어느 모듈에 적용합니까?" |
| 정책 충돌 | "보안 vs 속도, 어디에 우선순위?" |
| 테스트/빌드 실패 + 진행 요청 | "실패 상태에서 강제 진행합니까?" |
| 외부 API/비밀키 필요 | "민감정보가 필요합니다. 제공 방법은?" |
| 정의되지 않은 토큰 호출 | "이 토큰은 정의되어 있지 않습니다. 새로 정의합니까?" |

---

## 5. 토큰 스펙 스키마

모든 PHL 토큰은 `/phl/tokens/` 에 개별 파일로 존재하며, 아래 스키마를 따른다:

```yaml
Name:              PHL-XXXX
Intent:            무엇을 달성하는가 (1문장)
Scope:             어디까지 (모듈/파일/레포 범위)
Non-Goals:         하지 말아야 할 것
Preconditions:     실행 전 요구 상태
Procedure:         단계별 수행 (체크리스트)
Validation:        성공 판정 기준
Artifacts:         생성/수정 파일 목록
Commit Policy:     커밋 메시지 규칙
Rollback Policy:   실패 시 되돌림/대안
Questions Policy:  불확실할 때 질문 대상
```

---

## 6. 상태 전이 원칙

- **커밋 없는 변경은 "임시 상태"**로 간주. 확정되지 않은 것이다.
- PHL 토큰 실행은 **반드시 검증을 포함**한다. 검증 없는 커밋은 금지.
- 실패 시: `git revert`로 되돌리거나 실패 로그를 남긴다. `reset --hard` 금지.
- 같은 토큰이라도 **프로젝트 맥락에 따라 수행이 달라진다.** 이것이 스니펫과의 차이다.

---

## 7. 모드 선언

### 7.1 실행 모드 (기본)
PHL 토큰 → 코드 변경 → 검증 → 커밋

### 7.2 Architecture Validation Mode
사용자가 "더미/리허설/양산 전 검증"을 말하면:
- 구현 모드가 아니라 **설계 검증 모드**로 전환
- 파일이 없어도 계약/프로토콜/스캐폴딩/Mock을 만든다
- "파일 없음" 에러로 멈추지 않는다

### 7.3 토큰 정의 모드
사용자가 새 PHL 토큰을 정의하려 할 때:
- 섹션 5의 스키마에 따라 `/phl/tokens/PHL-{Name}.md` 생성
- `PHL_INDEX.json` 업데이트
- 이 파일의 토큰 목록 갱신

---

## 8. 토큰 레지스트리

현재 정의된 토큰 목록. 빠른 참조용.

| 토큰 | 파일 | Intent |
|------|------|--------|
| `PHL-Expansion` | `/phl/tokens/PHL-Expansion.md` | 모듈 확장/보강/견고화 |
| `PHL-Hardening` | `/phl/tokens/PHL-Hardening.md` | 보안/안정성 강화 |
| `PHL-Reverse` | `/phl/tokens/PHL-Reverse.md` | 역방향 검증/역로깅 |

---

## 9. 공통 계약 참조

프로젝트 전체에 적용되는 공통 규칙:

| 계약 | 파일 | 내용 |
|------|------|------|
| 에러 처리 | `/phl/contracts/error-handling.md` | 예외 전략, 리턴 타입, 폴백 |
| 로깅 | `/phl/contracts/logging.md` | 로그 레벨, 포맷, 필수 지점 |
| 테스트 | `/phl/contracts/testing.md` | 커버리지 기준, 필수 경로 |
| 보안 | `/phl/contracts/security.md` | 입력 검증, 인증, 비밀키 |
| 커밋 | `/phl/contracts/commit.md` | 메시지 형식, 단위, Co-Author |

---

## 10. 운영 선언문

> 너는 코드를 "생성"하는 게 아니라, **PHL 프로토콜을 실행**한다.
> 모든 규칙의 진실원천은 이 파일(`PHL_SPEC.md`)과 `/phl/tokens/*` 이다.
> 토큰을 받으면: **(1) 스펙 로드 (2) 계획 (3) 변경 (4) 검증 (5) 커밋** 순서로 보고한다.
> 불확실하면 질문한다.
> 결과는 커밋으로 상태를 확정한다.

---

*Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>*
