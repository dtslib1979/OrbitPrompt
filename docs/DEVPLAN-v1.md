# OrbitPrompt 개발 계획 v1 (2026-04-21)

> phoneparis 관찰 3회 → 미러링 목록 확정 → OrbitPrompt 특화 설계 통합

---

## 0. 현황 스냅샷

### phoneparis가 완성한 패턴 (레퍼런스)

| 패턴 | 파일 | 상태 |
|------|------|------|
| youtube-cache.json 루프백 | `data/youtube-cache.json` + index.html 최신 영상 섹션 | ✅ 2026-04-21 완성 |
| Discord 공지 캐시 | `data/latest-messages.json` + `.github/workflows/discord-cache.yml` | ✅ 완성 |
| prompts/index.json 자동 갱신 | `.github/workflows/update-index.yml` | ✅ 완성 |
| data/ SSOT 구조 | notices.json / phases.json / portfolio.json / team.json / registry.json | ✅ 완성 |
| CSS 아키텍처 분리 | `assets/css/theme.css` + film-border.css + graph-map.css | ✅ 완성 |

### OrbitPrompt 현재 상태

| 항목 | 상태 |
|------|------|
| index.html | ✅ 전면 개편 완료 (681줄) |
| .github/workflows/ | ✅ update-index + discord-cache + discord-notify + repo-guard |
| docs/dev-logs/ | ✅ 신설 (001 기록) |
| data/ | ⚠️ fab-manifest.json만 있음 — SSOT JSON 없음 |
| youtube-cache.json | ❌ 없음 (EAE-University 채널 연동 필요) |
| CSS 분리 | ❌ 전부 index.html inline |
| Discord 섹션 | ⚠️ discord-cache.yml만 있고 data/latest-messages.json 없음, 렌더러 없음 |
| Generator 활성화 | ⚠️ 14개 중 4개만 live (broadcast/publisher/engine/guide) |
| Generator SSOT | ❌ index.html inline 하드코딩 → 외부 JSON 없음 |

---

## 1. 미러링 목록 (phoneparis → OrbitPrompt)

### 1-A: youtube-cache.json 루프백 ★★★ (최우선)

**phoneparis 패턴:**
```html
<section id="latest-videos">
  <div id="yt-latest-container"></div>
</section>
<script>
(async () => {
  const data = await fetch('./data/youtube-cache.json').then(r=>r.json());
  const videos = data.videos || [];
  container.innerHTML = videos.map(v => `카드 HTML`).join('');
})();
</script>
```

**OrbitPrompt 적용:**
- 대상 채널: `@EAE-University` (채널ID: UCogemhYGCnbVp13ARqFYM8A)
- `youtube-setup.json` 이미 있음 → `node tools/youtube/export.cjs c` 실행 → `data/youtube-cache.json` 생성
- index.html 하단에 "EAE 최신 강의" 섹션 추가

---

### 1-B: Discord 섹션 렌더러

**phoneparis 패턴:** discord-cache.yml → `data/latest-messages.json` → index.html에 공지 섹션

**OrbitPrompt 적용:**
- discord-cache.yml ✅ 이미 생성됨
- 필요한 것: Secrets 설정 + index.html에 Discord 공지 섹션 추가
- 섹션 위치: PHL Protocol 섹션 아래

---

### 1-C: data/ SSOT JSON 구조

**phoneparis 패턴:** 모든 동적 콘텐츠를 `data/*.json`으로 분리 → HTML은 fetch만

**OrbitPrompt 적용:**

```
data/
├── generators.json      ← 14개 Generator 정의 SSOT (index.html 인라인에서 분리)
├── youtube-cache.json   ← export.cjs 자동 생성
├── latest-messages.json ← discord-cache.yml 자동 생성
└── notices.json         ← Generator 업데이트 공지
```

---

### 1-D: CSS 분리

**phoneparis 패턴:** `assets/css/theme.css` + 추가 CSS 파일들

**OrbitPrompt 적용:**
- `assets/css/orbit-theme.css` 분리
- index.html inline `<style>` → 외부 파일로

---

## 2. OrbitPrompt 특화 개발 (phoneparis에 없는 것)

### 2-A: data/generators.json SSOT ★★★

현재 14개 Generator가 index.html 자바스크립트에 하드코딩되어 있음.
외부 JSON으로 분리 → index.html은 fetch만.

```json
{
  "version": "1.0",
  "updated": "2026-04-21",
  "generators": [
    {
      "id": "broadcast",
      "icon": "📡",
      "name": "Broadcast",
      "status": "live",
      "files": ["math-tutor", "memorial", "music-curation"],
      "path": "prompts/broadcast/",
      "description": "방송 칠판 템플릿"
    },
    ...
  ]
}
```

→ update-index.yml 트리거에 `data/generators.json` 갱신 추가

---

### 2-B: Generator 순차 활성화 계획

| 단계 | Generator | 전제 조건 |
|------|-----------|-----------|
| 현재 live | broadcast / publisher / engine / guide | ✅ |
| STEP 3 | chalkboard / editorial | 칠판 템플릿 파일 추가 |
| STEP 4 | instruction / form | 인스트럭션 카테고리 파일 추가 |
| STEP 5 | identity / studio | 브랜딩 템플릿 추가 |
| STEP 6 | apk / dataset / route / whitepaper | APK/데이터 카테고리 파일 추가 |

---

### 2-C: PHL Whitepaper 페이지 완성

- `whitepaper.html` 이미 있음
- `docs/PHL-WHITEPAPER.md` 읽어서 HTML로 변환
- index.html에서 whitepaper.html 링크 연결

---

### 2-D: YouTube 채널 연동 (EAE-University)

```bash
# 실행 순서
node /home/dtsli/dtslib-papyrus/tools/youtube/export.cjs c
# → OrbitPrompt/data/youtube-cache.json 생성
```

eae-univ와 같은 `@EAE-University` 채널 → OrbitPrompt도 같은 캐시 참조 가능.
OR OrbitPrompt 자체 채널이 생기면 별도 export.

---

## 3. 전체 개발 시퀀스 (STEP)

```
STEP 1  data/generators.json 신설
        index.html Generator 렌더링 → fetch 기반으로 전환
        커밋: "refactor: Generator SSOT — data/generators.json 분리"

STEP 2  youtube-cache.json 루프백
        export.cjs c 실행 → data/youtube-cache.json 생성
        index.html에 "EAE 최신 강의" 섹션 추가 (phoneparis 패턴)
        커밋: "feat: EAE-University youtube-cache 루프백 연결"

STEP 3  Discord 섹션
        data/latest-messages.json 렌더러 추가 (Secrets 설정 필요)
        index.html에 Discord 공지 섹션 추가
        커밋: "feat: Discord 공지 섹션 — latest-messages.json 루프백"

STEP 4  CSS 분리
        assets/css/orbit-theme.css 추출
        index.html inline style 제거
        커밋: "refactor: CSS 분리 — orbit-theme.css"

STEP 5  Generator 활성화 (chalkboard + editorial)
        prompts/chalkboard/ + prompts/editorial/ 파일 추가
        generators.json status → "live"
        커밋: "feat: chalkboard/editorial Generator 활성화"

STEP 6  데이터 공지 파이프라인
        data/notices.json 신설 (Generator 업데이트 알림)
        index.html notices 섹션 렌더러 추가
        커밋: "feat: notices.json 파이프라인"

STEP 7  PHL Whitepaper 완성
        whitepaper.html 콘텐츠 채움
        index.html → whitepaper.html 링크
        커밋: "feat: PHL Whitepaper 페이지 완성"
```

---

## 4. 파일 구조 최종 형태 (STEP 7 완료 후)

```
OrbitPrompt/
├── index.html                      ← fetch 기반 (inline 최소화)
├── whitepaper.html                 ← PHL Whitepaper
├── manifest.webmanifest
│
├── assets/
│   ├── css/
│   │   └── orbit-theme.css        ← ← STEP 4 분리
│   └── icons/
│
├── data/                           ← SSOT JSON 집합
│   ├── generators.json            ← ← STEP 1 신설
│   ├── youtube-cache.json         ← ← STEP 2 생성 (export.cjs)
│   ├── latest-messages.json       ← ← STEP 3 (discord-cache.yml 자동)
│   └── notices.json               ← ← STEP 6 신설
│
├── prompts/                        ← Generator HTML 파일들
│   ├── index.json                 ← update-index.yml 자동 갱신
│   ├── broadcast/
│   ├── publisher/
│   ├── engine/
│   ├── guide/
│   ├── chalkboard/                ← STEP 5 활성화
│   ├── editorial/                 ← STEP 5 활성화
│   └── ...
│
├── docs/
│   ├── dev-logs/
│   │   └── 001-...md
│   ├── DEVPLAN-v1.md              ← 이 파일
│   └── ...기존 docs...
│
├── .github/workflows/
│   ├── update-index.yml           ← prompts/*.html → index.json
│   ├── discord-cache.yml          ← 30분 cron → latest-messages.json
│   ├── discord-notify.yml
│   └── repo-guard.yml
│
└── orbit/                          ← Prompt Atom 엔진 (기존)
    ├── atoms/
    ├── raw/
    ├── schemas/
    └── templates/
```

---

## 5. GitHub Secrets 필요 목록

| Secret 이름 | 용도 | 설정 위치 |
|-------------|------|-----------|
| `DISCORD_BOT_TOKEN` | discord-cache.yml | OrbitPrompt repo → Settings → Secrets |
| `DISCORD_CHANNEL_ID` | discord-cache.yml | OrbitPrompt repo → Settings → Secrets |

---

## 6. 우선순위 판단 근거

| STEP | 이유 |
|------|------|
| STEP 1 (generators.json) | index.html 유지보수성 핵심. Generator 추가할 때마다 JSON만 수정하면 됨 |
| STEP 2 (youtube 루프백) | phoneparis가 2026-04-21 완성. EAE-University 채널 87개 영상 이미 있음. 바로 적용 가능 |
| STEP 3 (Discord) | Secrets 설정이 선행 조건. 박씨 Discord 채널 확정 후 진행 |
| STEP 4 (CSS) | 기능 영향 없음. STEP 1~3 완료 후 |
| STEP 5~7 | 콘텐츠 의존. Generator 파일이 먼저 있어야 활성화 가능 |
