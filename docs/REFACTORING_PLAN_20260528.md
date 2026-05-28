# OrbitPrompt 리팩토링 계획
> 확정: 2026-05-28 / 박씨 직접 정의
> 연관: parksy-logs/docs/, eae-univ/docs/, eae.kr/docs/ (동일 플랜 각 레포 시각)

---

## 3축 정의

| 축 | 정의 |
|----|------|
| **리걸 엔터티** | PHL 프로토콜 IP + 편집 솔루션 회사 |
| **공정 (FAB)** | RT-α — 개념 추출 → PHL 태깅 → topics 딕셔너리 생성 |
| **소설 단위** | 2부 "언어를 분해하다" |

파이프라인 위치: **level 3** — 편집 OS

```
parksy-logs (원자재)
    ↓
OrbitPrompt ← 여기 (편집 OS)
    ↓ RT-α
eae-univ (강의 생산)
    ↓
eae.kr (글로벌 배포)
```

---

## 현황 진단

### 이 레포가 담당해야 할 것 (올바른 위치)
```
PHL_SPEC.md         ← PHL 프로토콜 최상위 정의 (SSOT)
PHL_INDEX.json      ← 토큰 → 정의 파일 매핑
phl/tokens/         ← 토큰별 정의 (Expansion, Hardening, Reverse)
phl/contracts/      ← 공통 계약 (에러/로깅/테스트/보안/커밋)
phl/playbooks/      ← 실행 플레이북
prompts/            ← 7개 Generator (PWA, Chalkboard, Identity 등)
boards/             ← 생성된 칠판 아카이브
topics/             ← 언어별 개념 DB (언어 무관 PHL 입력 자산)
```

### 문제 1: phl/ 네이밍 충돌
```
현재:
  OrbitPrompt/phl/  — HTML Generator + 프로토콜 정의 (Spec)
  eae-univ/phl/     — Python Runtime 구현체 (Engine)

동명이지만 완전히 다른 것.
혼란 제거를 위한 rename:

  OrbitPrompt/phl/ → OrbitPrompt/phl-spec/
  eae-univ/phl/   → eae-univ/engine/
```

### 문제 2: youtube-setup.json SSOT 불명확
```
현재: OrbitPrompt, eae-univ, eae.kr 3곳에 동일 파일 존재
→ SSOT: eae.kr/youtube-setup.json 단일화
→ OrbitPrompt/youtube-setup.json → 삭제
```

### 문제 3: topics/ 콘텐츠 부족
```
현재: math, memorial, music, pwa-demo만 있음
필요: 할머니·할아버지 콘텐츠 (Track A 시작 조건)

추가 대상:
  topics/grandparent/
    life_en.md          ← 인생 개념 영어 (1회 작성)
    wisdom_en.md        ← 지혜 개념 영어
    story_en.md         ← 이야기 개념 영어
    life_ko.md          ← 인생 개념 한국어
    wisdom_ko.md        ← 지혜 개념 한국어

  topics/index.json 업데이트 (grandparent 카테고리 추가)
```

---

## 액션 플랜

### Phase 1 — 즉시 (Track A 시작 조건)
| 항목 | 액션 |
|------|------|
| topics/grandparent/ 생성 | EN 3개 + KO 2개 개념 파일 작성 |
| topics/index.json 업데이트 | grandparent 카테고리 등록 |
| youtube-setup.json 삭제 | eae.kr SSOT로 통합 |
| 00_TRUTH 레벨 수정 | level 2 → level 3 |

### Phase 2 — 다음 세션
| 항목 | 액션 |
|------|------|
| phl/ → phl-spec/ rename | 네이밍 충돌 해소 |
| prompts/dictionary/ 정비 | EN 편집 프롬프트 추가 (`en_grandparent.md`) |

---

## 00_TRUTH 재정의

```json
{
  "repo": "OrbitPrompt",
  "level": 3,
  "parent": "dtslib-papyrus",
  "type": "editorial-os",
  "pipeline_position": "midstream",
  "receives_from": ["parksy-logs"],
  "feeds_into": ["eae-univ"],
  "inherit": {
    "immutable": "strict",
    "defaults": "override-allowed"
  },
  "created": "2026-01-26"
}
```

---

## 소설 서사 구조

```
2부 — "언어를 분해하다"

챕터 1: PHL_SPEC.md    — 언어 분해의 법칙 제정
챕터 2: phl-spec/      — 법칙을 도구로 만들다
챕터 3: prompts/       — 도구를 7개 Generator로 구현
챕터 4: topics/        — 인류의 개념을 DB화하다
챕터 5: boards/        — 분해된 언어가 방송으로 나가다

이 레포의 클라이맥스:
  어느 나라 할머니·할아버지 이야기가 들어와도
  같은 PHL 구조를 통과하면 → 세계 어느 언어로든 나갈 수 있다.
```

---

## 이 레포의 경계 (침범 금지)

```
담당 O: PHL 프로토콜 정의, 편집 Generator, topics 딕셔너리
담당 X: 원자재 수집 (parksy-logs)
담당 X: 강의 HTML 생산 (eae-univ)
담당 X: 배포 라우팅 (eae.kr)
담당 X: youtube-setup.json 관리 (eae.kr SSOT)
```

---

*문서 위치: OrbitPrompt/docs/REFACTORING_PLAN_20260528.md*
*연관: parksy-logs/docs/REFACTORING_PLAN_20260528.md*
*연관: eae-univ/docs/REFACTORING_PLAN_20260528.md*
*연관: eae.kr/docs/REFACTORING_PLAN_20260528.md*
