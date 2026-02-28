# OrbitPrompt 레포지토리 목적 분석

> 분석 일시: 2026-02-28
> 분석 방법: git log, 폴더 구조, CLAUDE.md, Position Paper, 코드 전수 조사

---

## 한 줄 요약

**OrbitPrompt = 메타 프롬프트 생성기. 프롬프트를 만드는 프롬프트를 만드는 곳.**

---

## 1. 레포의 정체성

| 항목 | 내용 |
|------|------|
| **이름** | OrbitPrompt |
| **생성일** | 2026-01-26 |
| **상위 계보** | dtslib-papyrus → orbitprompt (Level 2) |
| **호스팅** | GitHub Pages (https://dtslib1979.github.io/OrbitPrompt/) |
| **기술 스택** | 바닐라 HTML/CSS/JS 단일 파일, 프레임워크 없음 |
| **개발 환경** | 핸드폰 Termux + Claude Code (PC 없음) |

---

## 2. 핵심 구조: 2개 레인

```
Lane 1: Prompt Engine (생성)     Lane 2: Archive (축적)
━━━━━━━━━━━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━━
prompts/                         boards/
├── chalkboard/  (방송 칠판)      ├── tribute-cinema.html
├── apk/         (PWA 생성)       ├── math-tutor.html
├── instruction/ (CLAUDE.md)      ├── music-curation.html
├── dataset/     (파인튜닝)       ├── memorial-tribute.html
├── identity/    (자기 모델)      ├── luxury-editorial.html
└── editorial/   (럭셔리 룩북)    └── ...
```

**흐름:** 유저가 변수 선택 → Generator가 프롬프트 생성 → LLM이 코드/문서 생성

---

## 3. 6개 Generator 분석

| # | Generator | 입력 | 출력 | 생태계 역할 |
|---|-----------|------|------|------------|
| 1 | 🎬 Chalkboard | YouTube 영상 분석 | 방송용 PWA 칠판 | 3개 방송국 화면 공급 |
| 2 | 📱 PWA | 앱 요구사항 | 설치형 웹앱 | 28개 레포 도구 생산 |
| 3 | 📋 Instruction | 레포 목적 | CLAUDE.md | 각 레포에 AI 두뇌 설치 |
| 4 | 🧬 Dataset | 대화 로그 | 파인튜닝 JSONL | 자기강화 학습 데이터 |
| 5 | 🪞 Identity | 대화 로그 + 7축 | 자기 모델 JSON | 페르소나 정밀화 |
| 6 | ✨ Editorial | 럭셔리 룩북 | 스토리텔링 PWA | 프리미엄 콘텐츠 |

---

## 4. 28개 레포 생태계에서의 위치

```
OrbitPrompt (설계도면실)
    │
    ├── 직접 공급 ──→ parksy.kr (방송국)
    │                  eae.kr (교육방송)
    │                  dtslib.kr (비즈니스 다큐)
    │
    ├── 소재 수신 ←── gohsy-production (녹음실)
    │                  parksy-audio (오디오 엔진)
    │                  parksy-image (이미지 에셋)
    │
    ├── 데이터 수신 ←── parksy-logs (대화 저장소)
    │
    └── 도구 배포 ──→ dtslib-apk-lab (APK 스토어)
```

**핵심 포지션:** 다른 27개 레포가 "제품을 만드는 공장"이라면, OrbitPrompt는 "공장을 만드는 설계실".

---

## 5. git log 서사 분석 (헌법 제1조 기준)

커밋 총 수: 약 50개. git log --reverse로 읽은 줄거리:

| 장 | 시기 | 서사 | 대표 커밋 |
|----|------|------|-----------|
| 1장: 탄생 | 초기 | 프롬프트 아카이브로 시작 | `Add 4 Generator categories` |
| 2장: 삽질 | 초중기 | PWA 서비스 워커 → 장애 발견 → 전량 제거 | `refactor: remove service worker` |
| 3장: 각성 | 중기 | 프롬프트 엔진 전용으로 재설계 | `refactor: 프롬프트 엔진 전용으로 재설계` |
| 4장: 성장 | 중후기 | 추모 칠판, 교육 칠판 등 실전 템플릿 양산 | `feat(memorial): 세계 최고 수준 추모 영상 PWA` |
| 5장: 철학 | 후기 | 헌법 제1조(소설), 제2조(매트릭스) 정립 | `docs: 헌법 제1조 — 레포지토리는 소설이다` |
| 6장: 자의식 | 현재 | Identity Engine, Position Paper | `feat: Identity Engine`, `[docs] 포지션 페이퍼` |

**서사 유형:** 전형적인 "시도→삽질→전환→각성→성장" 플롯. PWA 서비스 워커 제거가 **클라이맥스(전환점)**.

---

## 6. 설계 철학 4원칙

1. **존재 = 생산** — 웹페이지 열면 그게 방송. 화면 녹화 = 완성물. 편집 0분.
2. **프롬프트는 코드다** — 반복 가능. 테스트 가능. 버전 관리 가능.
3. **불일치는 기능이다** — LLM 출력의 변동성이 유저를 능동적 크리에이터로 만든다.
4. **제약이 설계를 결정한다** — 12시간 노동, PC 없음 → 편집 0분 워크플로우.

---

## 7. 기술적 특징

| 특징 | 설명 |
|------|------|
| **단일 HTML** | 모든 Generator/Board가 인라인 CSS/JS 포함 단일 파일 |
| **프레임워크 제로** | React, Vue 등 외부 의존성 없음 |
| **CDN 제로** | Google Fonts 외 외부 리소스 없음 |
| **서비스 워커 제거** | 캐시 문제로 의도적 제거. 순수 웹페이지 방식 |
| **모바일 퍼스트** | 핸드폰이 유일한 개발/사용 도구 |
| **Setup + Broadcast** | 칠판 템플릿은 설정 모드와 방송 모드 분리 |

---

## 8. 자기참조 구조 (가장 독특한 특성)

```
대화 → 박씨 캡처 → parksy-logs
                        │
                        ▼
                   OrbitPrompt가 가공
                        │
                        ▼
                   새 Generator/구조 탄생
                        │
                        ▼
                   그 과정이 다시 대화 → 캡처 → 가공 → ∞
```

**OrbitPrompt는 자기 자신을 입력으로 받아 자기 자신을 개선하는 유일한 레포.**

---

## 9. 결론

OrbitPrompt는 단순한 프롬프트 저장소가 아니다.

- **28개 레포 생태계의 두뇌** (Instruction Generator가 각 레포에 CLAUDE.md 설치)
- **3개 방송국의 화면 공장** (Chalkboard Generator → 방송용 칠판 PWA)
- **자기참조 생산 체계** (대화 → 캡처 → 가공 → 새 도구 → 대화 → ∞)
- **제약 기반 설계의 산물** (PC 없음, 12시간 노동 → 편집 0분 워크플로우)

> **공장을 만드는 공장. 생각을 만드는 생각. 프롬프트를 만드는 프롬프트.**

---

*Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>*
