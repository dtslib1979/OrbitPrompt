# OrbitPrompt — Claude Code 세션 가이드

## 이 파일의 목적

Claude Code가 이 레포에서 작업할 때 **자동으로 읽는 인스트럭션**.
유저가 자료를 던지면 → Claude가 알아서 적절한 작업 수행.

---

## 자동 트리거 (유저 입력 → Claude 행동)

### 트리거 1: YouTube 영상 분석 복붙

**감지 패턴:**
```
포맷: ...
섹션: ...
효과: ...
무드: ...
```

**Claude 행동:**
1. 분석 파싱 (포맷, 섹션, 효과, 무드 추출)
2. `boards/새템플릿.html` 생성
   - Setup Mode + Broadcast Mode 포함
3. `prompts/chalkboard/index.html` Archive에 링크 추가
4. `data/templates.json` 업데이트
5. git commit & push
6. 라이브 URL 제공

---

### 트리거 2: PWA/앱 요구사항

**감지 패턴:**
- "~하는 앱 만들어줘"
- "PWA로 ~"
- 앱 기능 명세

**Claude 행동:**
1. 요구사항 파싱
2. `prompts/apk/` 또는 별도 폴더에 PWA 생성
3. 단일 HTML 파일 (인라인 CSS/JS)
4. git commit & push
5. 라이브 URL 제공

---

### 트리거 3: Generator 개선 요청

**감지 패턴:**
- "Generator에 ~ 추가해"
- "~ 옵션 넣어줘"

**Claude 행동:**
1. 해당 Generator 파일 수정
2. UI/옵션 추가
3. 프롬프트 생성 로직 업데이트
4. git commit & push

---

### 트리거 4: 철학/문서 추가

**감지 패턴:**
- "백서에 ~ 추가"
- "CLAUDE.md 업데이트"
- "철학 정리"

**Claude 행동:**
1. `whitepaper.html` 또는 `CLAUDE.md` 수정
2. git commit & push

---

### 트리거 5: 버그/개선

**감지 패턴:**
- "~ 안 돼"
- "~ 고쳐줘"
- 스크린샷 + 문제 설명

**Claude 행동:**
1. 문제 파악
2. 해당 파일 수정
3. git commit & push
4. 수정 내용 설명

---

## 정체성

**OrbitPrompt = 메타 프롬프트 생성기**

```
유저가 변수 선택 → Generator가 프롬프트 생성 → LLM이 코드/문서 생성
```

### 2개 레인

| 레인 | 역할 | 내용 |
|------|------|------|
| **Prompt Engine** | 생성 | 4개 Generator (도구) |
| **Archive** | 축적 | 생성된 결과물 모음 |

### 4개 Generator

| Generator | 입력 | 출력 |
|-----------|------|------|
| 🎬 Chalkboard | YouTube 영상 분석 | 방송용 PWA |
| 📱 PWA | 앱 요구사항 | 설치형 PWA |
| 📋 Instruction | 레포 목적 | CLAUDE.md |
| 🧬 Dataset | 대화 로그 | 파인튜닝 JSONL |

---

## 핵심 철학

### 1. 존재 = 생산
```
웹페이지 열면 그게 방송
화면 녹화 = 완성물
편집 제로
```

### 2. 프롬프트는 코드다
```
반복 가능
테스트 가능
버전 관리 가능
```

### 3. 불일치는 기능이다
```
LLM 출력의 일관성 없음 = 유저가 강제로 편집
→ 수동적 소비자가 아닌 능동적 크리에이터
AI 출력은 시작점. 마무리는 인간.
```

### 4. 제약이 설계를 결정한다
```
12시간 육체노동 → 편집 0분 워크플로우
PC 없음 → 모바일 퍼스트
핸드폰만 → 전체 생태계 모바일 퍼스트
```

---

## 폴더 구조

```
OrbitPrompt/
├── index.html                    ← 메인 랜딩
├── whitepaper.html               ← 철학 백서
├── CLAUDE.md                     ← 이 파일
│
├── prompts/                      ← Lane 1: Generator들
│   ├── chalkboard/
│   │   ├── index.html            ← 카테고리 게시판
│   │   └── template-generator.html
│   ├── apk/
│   │   ├── index.html
│   │   └── pwa-generator.html
│   ├── instruction/
│   │   ├── index.html
│   │   └── claude-md-generator.html
│   └── dataset/
│       ├── index.html
│       └── finetune-generator.html
│
├── boards/                       ← Lane 2: Archive (생성된 칠판)
│   ├── memorial-tribute.html
│   ├── math-tutor.html
│   ├── music-curation.html
│   └── pwa-demo.html
│
├── data/
│   └── templates.json
└── assets/
```

---

## 작업 규칙

### 반드시
- [ ] 단일 HTML 파일 (인라인 CSS/JS)
- [ ] 바닐라 JS만 (프레임워크 금지)
- [ ] 모바일 퍼스트 반응형
- [ ] Setup Mode + Broadcast Mode 분리 (칠판의 경우)
- [ ] 작업 후 git commit & push
- [ ] 라이브 URL 제공

### 금지
- 외부 프레임워크 (React, Vue 등)
- CDN 의존성 (폰트 제외)
- 하드코딩된 콘텐츠 (샘플 제외)
- 설명 없는 작업

### 커밋 메시지 형식
```
[카테고리] 작업 내용

상세 설명 (있으면)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## 칠판 템플릿 구조 (Chalkboard)

```html
<!-- Setup Mode -->
<div class="setup">
  <!-- 입력 폼 -->
  <input> 제목, 인용문, 이미지 URL
  <button> 저장 / 샘플 불러오기 / 방송 시작
</div>

<!-- Broadcast Mode -->
<div class="broadcast">
  <!-- 풀스크린 프레젠테이션 -->
  - Ken Burns 효과 (CSS animation)
  - 필터 (grayscale, sepia 등)
  - 터치/스와이프 네비게이션
  - 타임라인 인디케이터
  - EXIT 버튼
</div>
```

---

## 4-레포 수렴 구조 (2026-02-19 확정)

> OrbitPrompt는 PWA 공장. 여기서 만든 칠판/화면이 각 레포로 흘러간다.

```
OrbitPrompt              gohsy-production        parksy-audio           parksy.kr
(PWA 공장)               (물성 스튜디오)           (오디오 엔진)           (방송국)
━━━━━━━━━━              ━━━━━━━━━━━━━           ━━━━━━━━━━━━          ━━━━━━━━━━
Chalkboard Generator    SOUND BOOTH             BGM 파이프라인          뮤지션 박씨 채널
boards/ PWA 생성        MV88+ 보컬 녹음          3-Layer 믹싱           YouTube 송출
Setup+Broadcast Mode    render.html 재생         PD 클래식 반주          시청자 접점
        │                      │                       │                    ↑
        ├── 추모 칠판 ──→ render.html                   │                    │
        ├── 카라오케 화면 ──→ 보컬 녹음 + 반주 ←─────────┘                    │
        └── 방송 칠판 ─────────────────── 완성 콘텐츠 ──→ YouTube 송출 ──────┘
```

### OrbitPrompt의 역할

| 생산물 | 소비자 | boards/ 경로 |
|--------|--------|-------------|
| 추모 칠판 PWA | gohsy-production (render.html) | `boards/memorial-tribute.html` |
| 카라오케 가사 화면 | gohsy-production (카라오케 플러그인) | `boards/karaoke-*.html` (예정) |
| 교육 칠판 | parksy.kr (방송 콘텐츠) | `boards/math-tutor.html` 등 |
| 음악 큐레이션 | parksy.kr (뮤지션 박씨) | `boards/music-curation.html` |

### 연관 레포

| 레포 | 역할 | 연결점 |
|------|------|--------|
| `dtslib1979/gohsy-production` | 물성 스튜디오 (녹음/녹화) | 추모 칠판 + 카라오케 화면 소비자 |
| `dtslib1979/parksy-audio` | 오디오 엔진 | 칠판 BGM + 카라오케 반주 |
| `dtslib1979/parksy.kr` | 방송국 (뮤지션 박씨) | 완성 콘텐츠 송출 |
| phoneparis/products/ai-second-phone/os | 1인 미디어 OS | 상위 프레임워크 (구 one-man-os) |
| parksy-logs | 대화 저장/RAG | Dataset Generator 입력 |
| parksy-image | 이미지 에셋 | 칠판 배경 |
| dtslib-apk-lab | APK 스토어 | PWA Generator 출력 |

---

## 라이브 URL

- **메인**: https://dtslib1979.github.io/OrbitPrompt/
- **백서**: https://dtslib1979.github.io/OrbitPrompt/whitepaper.html
- **Chalkboard**: https://dtslib1979.github.io/OrbitPrompt/prompts/chalkboard/
- **PWA**: https://dtslib1979.github.io/OrbitPrompt/prompts/apk/
- **Instruction**: https://dtslib1979.github.io/OrbitPrompt/prompts/instruction/
- **Dataset**: https://dtslib1979.github.io/OrbitPrompt/prompts/dataset/

---

## 오너 컨텍스트

- 12시간 육체노동 (식당)
- PC 없음, 핸드폰이 유일한 개발 도구
- Termux + Claude Code로 개발
- YouTube 8개 채널 운영
- 목표: 말만 하면 콘텐츠가 나오는 자동화
