# Φ7 철학 카운터 MCP — 개발 계획서 v1.0

> 발행: 2026-06-08
> 근거: 라 필로소피아(에코 3부작) = 학교 리포트 모음집
> 목적: "처음부터 끝까지 읽는 책"이 아니라 "필요할 때 철학자별로 꺼내보는 인덱스"를 MCP로 구현

---

## 배경

에코 3부작은 철학자별 이론을 정리한 마스터 테이블이다.
이걸 MCP로 만들면 철학자 이름만 던져도 Φ7 5축으로 비교 리포트를 뽑아주는 서버가 된다.

## 툴

### 1. `phi7_compare`
- 입력: 철학자 이름 + 시대
- 처리: 에코 요약(LLM) → Φ7 5축 비교
- 출력: "닮은 점 / 다른 점 / 결정적 차이"

### 2. `identity_diff`
- 입력: 비교 결과
- 처리: 기존 ID-MANIFEST와 diff
- 출력: "이번 비교로 ID 수정할 부분"

### 3. `counter_md`
- 입력: 전체 결과
- 처리: chan-dae-counter.md 포맷 자동 생성
- 출력: 바로 커밋 가능한 마크다운

## 구조

```
mcp/philosophy-counter/
├── server.py          ★ MCP 서버 (3개 툴)
├── phi7_engine.py     Φ7 5축 비교 엔진
├── identity_store.py  ID-MANIFEST + 버전 관리
├── counter_format.py  counter.md 자동 생성기
└── README.md
```

## 의미

이 MCP가 완성되면 "에코 3권 + LLM + Φ7 + counter.md"가
하나의 실행 가능한 시스템으로 묶인다.

철학 공부가 아니라 **ID 엔진 튜닝**이 MCP로 구현된다.
