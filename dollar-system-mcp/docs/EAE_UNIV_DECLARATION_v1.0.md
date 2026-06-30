# EAE University 정체성 전환 선언문
### v1.0 | 2026.06.30 | 공표

---

## 0. 이 선언의 목적

**EAE University의 콘텐츠 단위(unit)를 전환한다.**

```
[과거]: eae-univ = 아티클/영상/강의 (콘텐츠 단위 = "사람이 소비하는 완성품")
[미래]: eae-univ = MCP 출력물 게시 갤러리 (콘텐츠 단위 = "기계가 검증가능한 모듈")
```

이 전환은 단순 리브랜딩이 아니다. 콘텐츠의 **최소 단위 자체**를 바꾸는 것이다.

---

## 1. 단위 전환의 본질

### 과거 단위: 아티클 (Article)

```
아티클 한 편 = 사람이 읽고 끝나는 최종소비재
              → 소비 후 폐기 (재사용 불가)
              → 검증 불가 (주장만 있고 증거 링크 없음)
              → 다른 시스템이 가져다 쓸 수 없음
```

### 미래 단위: 지식원자 (Knowledge-Atom)

```
knowledge-atom 하나 = 다른 MCP가 가져다 쓸 수 있는 재사용 가능한 부품
                    → 검증 가능 (GATE 0, 신뢰도 점수 내장)
                    → 표준 규격 (PEM 매트릭스 호환)
                    → 공급망을 가진 산업재
```

### 유닛 비교

| 차원 | 아티클 (과거) | Knowledge-Atom (미래) |
|------|-------------|---------------------|
| 소비자 | 사람 | 기계 + 사람 |
| 검증 | 주장 | thesis + chain + verdict + confidence |
| 재사용 | 불가 (폐기) | 가능 (MCP import) |
| 생산비용 | 높음 (글쓰기) | 낮음 (Perplexity → 자동화) |
| 신뢰 | 없음 | GATE 0 검증 내장 |
| 연결 | 단독 | supply chain (원자재→가공→검증→게시) |

---

## 2. 지식 공급망 (Knowledge Supply Chain)

### 3단계 파이프라인

```
parksy-rawmat (원자재)
  │
  │  Perplexity Space 호출 → raw 텍스트
  │  run_episode() → write_article() → article JSON
  │
  ▼
dollar-system-mcp (가공/검증)
  │
  │  knowledge-atom MCP 등록
  │  GATE 0 검증 (선택)
  │  PEM 사분면 매핑
  │
  ▼
eae-univ (출판/게시)
  │
  │  research/body/ — 경제/철학 리서치
  │  research/butterfly/ — 자유 리서치
  │  philosophy/ — EAE 세계관
  │
  └──→ parksy-distributor (유통)
```

### 역방향 흐름 (query)

```
"야 철학 개론 알려줘"
  │
  ▼
knowledge-atom MCP (query_knowledge)
  │
  ▼
eae-univ research/ + philosophy/ 검색
  │
  ▼
결과 → 박씨 텔레그램 / YouTube
```

---

## 3. 선언 조항

### 제1조: 단위 전환

EAE University의 모든 콘텐츠는 **knowledge-atom 표준**으로 생산된다.
기존 아티클은 knowledge-atom으로 자동 변환된다.
향후 모든 신규 콘텐츠는 knowledge-atom 규격으로만 등록된다.

### 제2조: 표준 규격

모든 knowledge-atom은 다음 필드를 포함한다:

```
atom_id:       고유 식별자 (KA-{DOMAIN}-{TIMESTAMP})
domain:        body | butterfly | philosophy | whitepaper | course
thesis:        핵심 주장 (1문장)
chain:         인과 관계 (→로 연결)
verdict:       PROCEED | REDUCE | HOLD
confidence:    0-100
source_path:   원본 파일 경로
registered_at: 등록 일시
```

### 제3조: 공급망

knowledge-atom은 항상 **공급망(supply chain)** 을 가진다.
입력(parksy-rawmat) → 가공(dollar-system-mcp) → 게시(eae-univ) 경로가 명시되어야 한다.
출처 없는 atom은 C급(source_tier=C급)으로 분류된다.

### 제4조: 검증 가능성

모든 atom은 검증 가능해야 한다.
thesis는 chain으로 증명되어야 하고, chain의 각 노드는 출처를 가져야 한다.
confidence 점수는 GATE 0 검증 등급과 연동된다.

### 제5조: 재사용

모든 atom은 다른 MCP가 import할 수 있어야 한다.
atom의 JSON 스키마는 공개되어야 하고, 버전 관리되어야 한다.
atom 변경 시 이력이 보존되어야 한다.

---

## 4. 영향 범위

| 레포 | 영향 | 내용 |
|------|------|------|
| parksy-rawmat | 🔄 role 명확화 | 원자재 공급자 → article 생산 자동화 |
| dollar-system-mcp | ✅ module14 신규 | knowledge-atom MCP 등록/검색/개론 생성 |
| eae-univ | 🔄 정체성 전환 | 아티클 갤러리 → knowledge-atom 게시판 |
| parksy-distributor | ⏳ 추후 연결 | knowledge-atom 유통 채널 확장 |
| OrbitPrompt | ✅ PHL 연동 | knowledge-atom → Primer 생성 |

---

## 5. 오늘 시점 완료 항목

- [x] module14_knowledge_atom.py — MCP 등록/검색/개론/통계 4개 툴
- [x] eae-univ research/body/ 4개 article → knowledge-atom 자동 등록
- [x] eae-univ research/butterfly/ 2개 article → knowledge-atom 자동 등록
- [x] eae-univ philosophy/ 4개 문서 → knowledge-atom 자동 등록
- [x] server.py v3.5.0 — 30개 툴 통합

---

## 6. 미래 전망

### 콘텐츠 산업의 변화

```
사람이 소비하는 콘텐츠(아티클/영상) = AI가 똑같이/더 잘 만들 수 있음
                                   = 복제비용이 0에 가까워짐

MCP 표준규격으로 검증가능하게 묶인 지식 = 다른 시스템이 신뢰하고 가져다 쓸 수 있는 단위
                                       = 복제는 쉬워도 "검증된 신뢰"는 복제 안 됨
```

### 잔존 가치

**"이게 진짜 작동하고 검증됐다"는 신뢰 자체는 여전히 희소하다.**
콘텐츠 자체의 생산비용은 0에 수렴하지만, 검증된 atom의 신뢰는 복제 불가능하다.
EAE University가 "강의실"에서 "검증된 지식부품 창고"로 바뀌는 이유가 여기에 있다.

---

*작성일: 2026.06.30 | 버전: v1.0 | 선언: EAE University 정체성 전환*
