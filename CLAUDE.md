# OrbitPrompt — Claude Code 세션 가이드

## 정체성

**OrbitPrompt = 프롬프트 엔진 + 방송용 칠판**

2개 레인:
- **Prompt Engine** — 사고 도구 (멀티 쿼리, 역분석, 프레임워크)
- **Chalkboard** — 생산 도구 (방송용 칠판 PWA)

## 핵심 철학

```
프롬프트는 코드다.
- 반복 가능해야 한다
- 테스트 가능해야 한다
- 버전 관리 가능해야 한다

존재 = 생산
- 웹페이지 열면 그게 방송
- 화면 녹화 = 완성물
- 편집 제로
```

## 폴더 구조

```
OrbitPrompt/
├── index.html              ← 2레인 랜딩
├── archive.html            ← 프롬프트 아카이브
├── 00_TRUTH/               ← 원본 데이터
├── prompts/
│   └── engine/             ← 프롬프트 생성 엔진
│       └── Gitgub-publishing.html
├── boards/                 ← 방송용 칠판 템플릿
│   ├── math-tutor.html       (Khan Academy)
│   ├── music-curation.html   (NPR Tiny Desk)
│   ├── memorial-tribute.html (Ken Burns)
│   └── pwa-demo.html         (Apple Keynote)
├── data/
│   └── templates.json      ← 칠판 템플릿 데이터
├── docs/
│   └── workflow-memorial-documentary.md
├── assets/
├── config/
└── CLAUDE.md
```

## 레인별 도구

### Lane 1: Prompt Engine (사고 도구)

| 도구 | 상태 | 설명 |
|------|------|------|
| Multi-Query Gen | ✅ | 하나의 의도 → 여러 각도 프롬프트 |
| Reverse Engineering | ⬜ | 결과물에서 원본 프롬프트 추론 |
| Frameworks | ⬜ | CRISPE, Chain-of-Thought 등 |
| Prompt Library | ⬜ | 검증된 템플릿 모음 |

### Lane 2: Chalkboard (생산 도구)

| 템플릿 | 포맷 | 상태 |
|--------|------|------|
| Math Tutor | Khan Academy | ✅ |
| Music Curation | NPR Tiny Desk | ✅ |
| Memorial Tribute | Ken Burns | ✅ |
| PWA Demo | Apple Keynote | ✅ |
| Interview | Hot Ones | ⬜ |
| News Brief | Morning Brew | ⬜ |
| Code Review | Fireship | ⬜ |

## 워크플로우

```
1. OrbitPrompt 열기
2. 레인 선택 (Engine / Board)
3-A. Engine: 프롬프트 설계 → Archive 저장
3-B. Board: 칠판 선택 → Galaxy 녹화 → YouTube
```

## 연관 레포

- **one-man-os** — 1인 미디어 OS 프레임워크
- **parksy-image** — 이미지 에셋
- **parksy-audio** — 오디오 에셋
- **parksy-logs** — 대화 저장/RAG

## 작업 규칙

### 반드시
- 도구/템플릿 단위로 개발 (독립 HTML)
- 프롬프트 구조 문서화
- templates.json에 새 템플릿 등록

### 금지
- 불필요한 의존성
- 외부 프레임워크 (바닐라 JS/CSS만)
