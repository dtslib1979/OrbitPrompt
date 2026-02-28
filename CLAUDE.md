# OrbitPrompt — Claude Code 세션 가이드

---

## 헌법 제0조: PHL 프로토콜

> **너는 코드를 "생성"하는 게 아니라, PHL 프로토콜을 실행한다.**

### PHL(Protocol for Human Language)이란

사용자가 짧은 토큰(1~3단어)을 말하면, Claude Code가 레포에 정의된 엄격한 규칙을 로드하여 실행하는 **의미 압축 프로토콜**.

### 진실원천 (SSOT)

| 파일 | 역할 |
|------|------|
| `/PHL_SPEC.md` | 최상위 규칙, 실행 사이클, 출력 형식 |
| `/PHL_INDEX.json` | 토큰 → 정의 파일 매핑 (빠른 탐색) |
| `/phl/tokens/*` | 토큰별 엄격한 정의 (Procedure, Validation 등) |
| `/phl/contracts/*` | 공통 계약 (에러/로깅/테스트/보안/커밋) |
| `/phl/playbooks/*` | 실행 플레이북 (체크리스트) |

### 실행 규칙

PHL 토큰을 받으면 **반드시** 이 순서:
1. **스펙 로드** — `PHL_SPEC.md` + `PHL_INDEX.json` + 토큰 정의 파일
2. **계획** — Plan 작성 및 보고
3. **변경** — 코드/문서 수정
4. **검증** — 테스트/린트/빌드
5. **커밋** — 상태 확정

불확실하면 **질문**한다. 추측하지 않는다.

### 현재 토큰

| 토큰 | 호출어 | Intent |
|------|--------|--------|
| `PHL-Expansion` | "확장", "보강", "튼튼하게" | 모듈 확장/보강/견고화 |
| `PHL-Hardening` | "보안", "하드닝" | 보안/안정성 강화 |
| `PHL-Reverse` | "역검증", "리버스" | 역방향 검증/역로깅 |

---

## 헌법 제1조: 레포지토리는 소설이다

> **모든 레포지토리는 한 권의 소설책이다.**
> **커밋이 문장이고, 브랜치가 챕터이고, git log --reverse가 줄거리다.**

- 삽질, 실패, 방향 전환 전부 남긴다. squash로 뭉개지 않는다.
- 기능 구현 과정 = 플롯 (문제→시도→실패→전환→해결)
- 레포 서사 → 블로그/웹툰/방송 콘텐츠로 파생 (액자 구성)

### 서사 추출 명령

```bash
narrative-extract.py --repo .                    # 이 레포 줄거리
narrative-extract.py --repo . --format synopsis  # 시놉시스
narrative-extract.py --repo . --format blog      # 블로그 원고
narrative-extract.py --repo . --climax           # 전환점만
narrative-extract.py --all ~                     # 28개 레포 연작 인덱스
```

### 서사 분류

| 커밋 유형 | 서사 | 의미 |
|-----------|------|------|
| `feat:` / 기능 추가 | 시도 | 주인공이 무언가를 만든다 |
| `fix:` / 버그 수정 | 삽질 | 예상대로 안 됐다 |
| `migration` / 전환 | 전환 | 버리고 다른 길을 간다 |
| `rewrite` / v2 | 각성 | 처음부터 제대로 다시 한다 |
| `refactor:` | 성장 | 같은 일을 더 잘하게 됐다 |
| `docs:` | 정리 | 지나온 길을 돌아본다 |

---

## ⚙️ 헌법 제2조: 매트릭스 아키텍처

> **모든 레포지토리는 공장이다.**
> **가로축은 재무 원장(ERP)이고, 세로축은 제조 공정(FAB)이다.**

### 가로축: 재무 원장 (ERP 로직)

커밋은 전표다. 한번 기표하면 수정이 아니라 반대 분개로 정정한다.

| 회계 개념 | Git 대응 | 예시 |
|-----------|----------|------|
| 전표 (Journal Entry) | 커밋 | `feat: 새 기능 구현` |
| 원장 (General Ledger) | `git log --reverse` | 레포 전체 거래 이력 |
| 계정과목 (Account) | 디렉토리 | `tools/`, `scripts/`, `assets/` |
| 회계 인터페이스 | 크로스레포 동기화 | 명시적 스크립트/매니페스트 |
| 감사 추적 (Audit Trail) | Co-Authored-By | AI/Human 협업 기록 |

### 세로축: 제조 공정 (FAB 로직)

레포는 반도체 팹이다. 원자재(아이디어)가 들어와서 완제품(콘텐츠)이 나간다.

| 제조 개념 | 레포 대응 | 예시 |
|-----------|----------|------|
| BOM (자재 명세) | 의존성 + 에셋 목록 | `pubspec.yaml`, `package.json`, `assets/` |
| 라우팅 (공정 순서) | 파이프라인 스크립트 | 빌드→테스트→배포 순차 실행 |
| WIP (재공품) | 브랜치 + Queue | `claude/*` 브랜치, `_queue/` |
| 수율 (Yield) | 빌드 성공률 | CI 통과율, 테스트 커버리지 |
| MES (제조실행) | 자동화 스크립트 | 동기화, 추출, 배포 도구 |
| 검수 (QC) | 테스트 + 리뷰 | `tests/`, 체크리스트 |

### 4대 원칙

1. **삭제는 없다, 반대 분개만 있다** — `git revert`로 정정. `reset --hard` 금지.
2. **증빙 없는 거래는 없다** — 커밋 메시지에 이유와 맥락. 크로스레포 이동은 명시적 스크립트로.
3. **BOM 확인 후 착공한다** — 의존성/에셋 명세 먼저, 공정 순서 명시 후 실행.
4. **재공품을 방치하지 않는다** — WIP 브랜치와 큐는 정기적으로 소화한다.

### 교차점: JSON 매니페스트

가로축과 세로축이 만나는 곳에 JSON이 있다. 매니페스트는 공정 기록이자 거래 증빙이다.

```
app-meta.json      = 제품 사양서
state.json         = 공정 현황판
*.youtube.json     = 출하 전표
*-SOURCES.md       = 원자재 입고 대장
```

### Claude 자동 체크

| 트리거 | 체크 | 위반 시 |
|--------|------|---------|
| `git commit` 전 | 커밋 메시지에 이유/맥락 있는가 | "증빙 누락" 경고 |
| `reset --hard` 요청 | 반대 분개(revert) 가능한가 | 차단, revert 제안 |
| 새 파일/도구 추가 | BOM(package.json 등) 업데이트했는가 | "BOM 미갱신" 경고 |
| 세션 시작 | `git branch --no-merged main` WIP 확인 | 3개 이상이면 정리 권고 |
| 크로스레포 작업 | 동기화 스크립트/매니페스트 경유하는가 | "인터페이스 우회" 경고 |

> **코드를 짜는 게 아니라 공장을 돌리고 있다.**
> **다만 그 공장의 원장이 git이고, 라인이 파이프라인일 뿐이다.**

---


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

### 트리거 6: 자기 모델링 / 대화 분석

**감지 패턴:**
- "이 대화에서 나를 분석해"
- "자기 모델 추출"
- "7축 분석"
- 대화 로그 + 분석 요청

**Claude 행동:**
1. Identity Engine (`prompts/identity/identity-engine.html`) 활용
2. 대화 로그를 7축(Meta, Reverse, Modular, Language, Zoom, Spiral, Quantum)으로 파싱
3. `identity-model` JSON 스키마에 맞춰 자기 모델 추출
4. 이전 모델이 있으면 Spiral 축으로 성장 궤적 비교
5. 결과물 제공 (JSON / 서사 요약)

---

## 정체성

**OrbitPrompt = 메타 프롬프트 생성기**

```
유저가 변수 선택 → Generator가 프롬프트 생성 → LLM이 코드/문서 생성
```

### 2개 레인

| 레인 | 역할 | 내용 |
|------|------|------|
| **Prompt Engine** | 생성 | 6개 Generator (도구) |
| **Archive** | 축적 | 생성된 결과물 모음 |

### 6개 Generator

| Generator | 입력 | 출력 |
|-----------|------|------|
| 🎬 Chalkboard | YouTube 영상 분석 | 방송용 PWA |
| 📱 PWA | 앱 요구사항 | 설치형 PWA |
| 📋 Instruction | 레포 목적 | CLAUDE.md |
| 🧬 Dataset | 대화 로그 | 파인튜닝 JSONL |
| 🪞 Identity | 대화 로그 + 7축 | 자기 모델 JSON |
| ✨ Editorial | 럭셔리 룩북 | 스토리텔링 PWA |

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
│   ├── dataset/
│   │   ├── index.html
│   │   └── finetune-generator.html
│   └── identity/
│       ├── index.html               ← 자기 모델링 엔진 포탈
│       └── identity-engine.html     ← 7축 파싱 프롬프트 생성기
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