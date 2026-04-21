# OrbitPrompt 개발 계획 v1.1 (2026-04-21)

> parksy-logs 원자재 → 리버스 엔지니어링 → Prompt Atom 생산 — 이것이 OrbitPrompt의 FAB 공정이다.

---

## 0. 철학 확정 (파피루스 검증 완료)

### OrbitPrompt의 진짜 역할

```
[INPUT]  parksy-logs/raw/  ←── 박씨 대화 캡처 (원자재 투입)
           ↓
[PROCESS] OrbitPrompt 칠판센터
           ├── 철학 조건 필터 (7축: Meta/Reverse/Modular/Language/Zoom/Spiral/Quantum)
           ├── 패턴 리버스 엔지니어링
           └── Prompt Atom 생성
           ↓
[OUTPUT]  prompts/ 6종 Atom  ←── Generator가 꺼내 쓰는 완제품
```

**칠판센터(Prompt Compiler)** = 출력 플랫폼이 아닌 **리버스 엔지니어링 공정**.

### Prompt Atom 6종 (완제품 규격)

| Atom | 설명 | 적용 Generator |
|------|------|---------------|
| `repo-janitor` | 레포 정리/감사 프롬프트 | Engine / Route |
| `broadcast-packager` | 칠판 방송 패키징 | Broadcast / Chalkboard |
| `branch-onboarding` | 신규 레포 온보딩 | Instruction |
| `web-deploy` | GitHub Pages 배포 | Engine |
| `asset-forge` | 에셋 생성/변환 | Studio |
| `automation-lab` | 자동화 스크립트 생성 | Dataset / Form |

---

## 1. 현황 스냅샷 (2026-04-21)

| 항목 | 상태 |
|------|------|
| index.html | ✅ fetch 기반 (generators.json SSOT 완료) |
| data/generators.json | ✅ 신설 완료 — 14개 Generator SSOT |
| .github/workflows/ | ✅ update-index + discord-cache + discord-notify + repo-guard |
| links/index.html | ✅ 신설 완료 — 4섹션 허브 |
| youtube-setup.json | ✅ EAE-University (account c) scaffold 완료 |
| docs/dev-logs/ | ✅ 신설 (001 기록) |
| data/youtube-cache.json | ❌ export.cjs c 실행 필요 (박씨 수동) |
| data/latest-messages.json | ❌ Discord Secrets 설정 필요 (박씨 수동) |
| CSS 분리 | ⚠️ index.html inline — STEP 4 예정 |
| Prompt Atom 파이프라인 | ❌ parksy-logs → Atom 스크립트 없음 |
| Generator 활성화 | ⚠️ 4개 live / 10개 pending |

---

## 2. 개발 시퀀스 (INPUT 파이프라인 우선)

### STEP 1 ✅ data/generators.json SSOT
- 14개 Generator 외부 JSON으로 분리
- index.html fetch 기반 렌더링 전환
- `커밋: "refactor: Generator SSOT — data/generators.json 분리"`

---

### STEP 2 — Prompt Atom 리버스 엔지니어링 파이프라인 ★★★ (핵심)

**OrbitPrompt의 존재 이유가 이것이다.**

```
parksy-logs/raw/*.md (대화 캡처)
  ↓
orbit/raw/ (원자재 스테이징)
  ↓
orbit/atoms/ (Atom 생성)
  ├── repo-janitor.md
  ├── broadcast-packager.md
  ├── branch-onboarding.md
  ├── web-deploy.md
  ├── asset-forge.md
  └── automation-lab.md
  ↓
prompts/*/index.html (Generator UI에서 소비)
```

**작업:**
1. `orbit/schemas/atom-schema.json` — Atom 규격 정의
2. `orbit/templates/` — 6종 템플릿 초안 작성
3. `scripts/extract-atoms.py` — parksy-logs/raw/ → Atom 추출 스크립트
4. `data/atom-index.json` — 생성된 Atom 목록 SSOT

커밋: `"feat: Prompt Atom 파이프라인 — parksy-logs → orbit/atoms/"`

---

### STEP 3 — youtube-cache.json 루프백

**전제조건:** 박씨가 `node /home/dtsli/dtslib-papyrus/tools/youtube/export.cjs c` 실행

- youtube-setup.json ✅ 이미 완료
- index.html에 "EAE 최신 강의" 섹션 추가
- 커밋: `"feat: EAE-University youtube-cache 루프백 연결"`

---

### STEP 4 — Discord 공지 섹션

**전제조건:** GitHub repo Settings → Secrets → DISCORD_BOT_TOKEN / DISCORD_CHANNEL_ID 설정

- discord-cache.yml ✅ 이미 완료
- index.html에 Discord 공지 섹션 추가
- 커밋: `"feat: Discord 공지 섹션 — latest-messages.json 루프백"`

---

### STEP 5 — CSS 분리

```
index.html inline <style>
  → assets/css/orbit-theme.css
```

커밋: `"refactor: CSS 분리 — orbit-theme.css"`

---

### STEP 6 — Generator 활성화 (chalkboard + editorial)

- prompts/chalkboard/ 파일 추가
- prompts/editorial/ 파일 추가
- generators.json status → "live"
- 커밋: `"feat: chalkboard/editorial Generator 활성화"`

---

### STEP 7 — PHL Whitepaper 완성

- whitepaper.html 콘텐츠 채움 (docs/PHL-WHITEPAPER.md 기반)
- index.html → whitepaper.html 링크 연결
- 커밋: `"feat: PHL Whitepaper 페이지 완성"`

---

## 3. 박씨 수동 작업 2개 (블로커)

| 블로커 | 방법 | 비고 |
|--------|------|------|
| youtube-cache.json 생성 | `node /home/dtsli/dtslib-papyrus/tools/youtube/export.cjs c` WSL에서 실행 | STEP 3 전제조건 |
| Discord Secrets | OrbitPrompt GitHub repo → Settings → Secrets and variables → Actions → 2개 추가 | STEP 4 전제조건 |

---

## 4. 파일 구조 최종 형태 (STEP 7 완료 후)

```
OrbitPrompt/
├── index.html                      ← fetch 기반 (inline 최소화)
├── whitepaper.html                 ← PHL Whitepaper
├── youtube-setup.json              ← EAE-University scaffold
├── manifest.webmanifest
│
├── assets/
│   └── css/
│       └── orbit-theme.css        ← STEP 5 분리
│
├── data/                           ← SSOT JSON 집합
│   ├── generators.json            ← ✅ STEP 1 완료
│   ├── atom-index.json            ← STEP 2 신설
│   ├── youtube-cache.json         ← STEP 3 (export.cjs)
│   ├── latest-messages.json       ← STEP 4 (discord-cache.yml)
│   └── notices.json               ← 추후
│
├── orbit/                          ← Prompt Atom 공정 (핵심)
│   ├── atoms/                     ← ← 완제품 Atom 6종
│   ├── raw/                       ← 원자재 스테이징
│   ├── schemas/
│   │   └── atom-schema.json       ← STEP 2 신설
│   └── templates/                 ← 6종 템플릿
│
├── prompts/                        ← Generator HTML 파일들
│   ├── index.json                 ← update-index.yml 자동 갱신
│   ├── broadcast/
│   ├── publisher/
│   ├── engine/
│   ├── guide/
│   ├── chalkboard/                ← STEP 6 활성화
│   └── editorial/                 ← STEP 6 활성화
│
├── links/
│   └── index.html                 ← ✅ 신설 완료
│
├── docs/
│   ├── dev-logs/
│   │   └── 001-...md
│   └── DEVPLAN-v1.md              ← 이 파일
│
└── .github/workflows/
    ├── update-index.yml
    ├── discord-cache.yml
    ├── discord-notify.yml
    └── repo-guard.yml
```

---

## 5. 우선순위 판단 근거

| STEP | 이유 |
|------|------|
| STEP 2 (Atom 파이프라인) | OrbitPrompt 존재 이유. 없으면 껍데기. |
| STEP 3 (YouTube) | export.cjs 이미 있음. 박씨 1개 명령어로 즉시 완성 |
| STEP 4 (Discord) | Secrets 설정이 전제. 박씨 수동 |
| STEP 5 (CSS) | 기능 무관. 유지보수 편의 |
| STEP 6~7 | 콘텐츠/파일 의존 |
