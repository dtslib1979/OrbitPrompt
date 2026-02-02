# OrbitPrompt — Claude Code 세션 가이드

## 정체성

**OrbitPrompt = 프롬프트 엔지니어링 엔진**

LLM과의 대화를 구조화하는 도구.
멀티 쿼리 생성, 프롬프트 역분석, 사고 프레임워크.

## 핵심 철학

```
프롬프트는 코드다.
- 반복 가능해야 한다
- 테스트 가능해야 한다
- 버전 관리 가능해야 한다

OrbitPrompt는 프롬프트를 "작성"하는 게 아니라 "설계"하는 도구다.
```

## 폴더 구조

```
OrbitPrompt/
├── index.html              ← 랜딩 (엔진 도구 목록)
├── prompts/
│   └── engine/             ← 프롬프트 생성 엔진
│       └── Gitgub-publishing.html
├── archive.html            ← 프롬프트 아카이브
├── 00_TRUTH/               ← 원본 데이터
├── assets/
├── config/
└── CLAUDE.md
```

## 도구 목록

| 도구 | 상태 | 설명 |
|------|------|------|
| Multi-Query Gen | ✅ | 하나의 의도 → 여러 각도 프롬프트 |
| Reverse Engineering | ⬜ | 결과물에서 원본 프롬프트 추론 |
| Frameworks | ⬜ | CRISPE, Chain-of-Thought 등 |
| Prompt Library | ⬜ | 검증된 템플릿 모음 |

## 분리된 레포

방송용 칠판 기능은 **Chalkboard**로 분리됨:

| 레포 | 역할 |
|------|------|
| OrbitPrompt | 프롬프트 엔진 (사고 도구) |
| Chalkboard | 방송용 칠판 (생산 도구) |

- Chalkboard: https://github.com/dtslib1979/chalkboard

## 연관 레포

- **chalkboard** — 방송용 칠판 시스템
- **one-man-os** — 1인 미디어 OS
- **parksy-logs** — 대화 저장/RAG

## 작업 규칙

### 반드시
- 도구 단위로 개발 (독립 HTML)
- 프롬프트 구조 문서화
- archive.html에 결과물 축적

### 금지
- 방송/칠판 관련 기능 추가 (→ Chalkboard로)
- 불필요한 의존성
