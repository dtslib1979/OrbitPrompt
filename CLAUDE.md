# OrbitPrompt — Claude Code 세션 가이드

## 정체성

**OrbitPrompt = 프롬프트 엔진 + 방송용 칠판**

2개 레인:
- **Prompt Engine** — 생성 도구 (Chalkboard Generator, 멀티 쿼리, 역분석)
- **Archive** — 생성된 칠판 모음 (참고/재사용)

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

---

## Chalkboard 템플릿 생성 워크플로우

### 트리거

유저가 **YouTube 영상 분석**을 복붙하면 → 새 Chalkboard 템플릿 생성

분석 예시 (Gemini가 YouTube 영상 분석한 결과):
```
포맷: Ken Burns 다큐멘터리
섹션: 5개 (도입→전개→절정→환기→결말)
효과: 흑백→컬러 전환, Ken Burns 줌
무드: somber → intense → triumphant → warm → peaceful
```

### Claude가 하는 일

1. **분석 파싱** — 포맷, 섹션 구조, 효과, 무드 추출
2. **템플릿 생성** — `boards/새템플릿.html` 파일 생성
   - Setup Mode: 유저가 텍스트/이미지 입력하는 폼
   - Broadcast Mode: 화면 녹화용 프레젠테이션
3. **templates.json 등록** — 새 템플릿 메타데이터 추가
4. **GitHub 푸시** — 라이브 배포
5. **URL 제공** — `https://dtslib1979.github.io/OrbitPrompt/boards/새템플릿.html`

### 유저가 하는 일

1. 템플릿 URL 열기
2. Setup Mode에서 텍스트/이미지 입력
3. [방송 시작] 버튼
4. Galaxy 화면 녹화
5. YouTube 업로드

### 템플릿 구조 (필수)

```html
<!-- Setup Mode -->
<div class="setup">
  - 인물/주제 정보 입력 폼
  - 섹션별 제목/인용문/이미지 URL 입력
  - 이미지 미리보기
  - [저장] [샘플 불러오기] [방송 시작] 버튼
</div>

<!-- Broadcast Mode -->
<div class="broadcast">
  - 풀스크린 프레젠테이션
  - Ken Burns / 필터 효과
  - 터치/스와이프/키보드 네비게이션
  - 타임라인 인디케이터
  - [EXIT] 버튼
</div>
```

### 이미지 가이드 (유저용)

| 소스 | 형식 |
|------|------|
| Unsplash | `https://images.unsplash.com/photo-xxx?w=1200` |
| 로컬 | `../assets/images/파일명.jpg` |
| 권장 크기 | 1200x800 이상 |

---

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

### Lane 2: Archive (생성된 칠판)

이전에 생성된 Chalkboard 템플릿. 참고하거나 재사용.

| 템플릿 | 원본 포맷 | 상태 |
|--------|----------|------|
| Memorial Tribute | Ken Burns 다큐 | ✅ 완성 |
| Math Tutor | Khan Academy | ⬜ 껍데기 |
| Music Curation | NPR Tiny Desk | ⬜ 껍데기 |
| PWA Demo | Apple Keynote | ⬜ 껍데기 |

*새 템플릿은 Chalkboard Generator로 생성 → 자동으로 Archive에 추가됨*

---

## 연관 레포

- **one-man-os** — 1인 미디어 OS 프레임워크
- **parksy-image** — 이미지 에셋
- **parksy-audio** — 오디오 에셋
- **parksy-logs** — 대화 저장/RAG

## 작업 규칙

### 반드시
- 도구/템플릿 단위로 개발 (독립 HTML)
- Setup Mode + Broadcast Mode 분리
- templates.json에 새 템플릿 등록
- 유저가 이미지/텍스트만 갈아끼우면 되도록

### 금지
- 불필요한 의존성
- 외부 프레임워크 (바닐라 JS/CSS만)
- 하드코딩된 콘텐츠 (데모용 샘플 제외)
