# OrbitPrompt 갤러리 — Φ7 축 재편 플랜

> 작성: Claude — 2026-06-08
> 기준: OrbitPrompt 전체 파싱 + 박씨 방향 "7축으로 직관적으로"
> 목적: THINK/MAKE/DRAW/FRAME → Φ7 부드러운 전환

---

## 1. 현재 상태

```
필터: 전체 | THINK | MAKE | DRAW | FRAME

라이브 전시물 6개:
  THINK × 5 — 전부 쏠림
  FRAME × 1 (라이브)
  MAKE × 0 (planned만)
  DRAW × 0

문제: THINK에 5개 몰림 / DRAW 비어있음 / 카테고리가 박씨 철학과 무관
```

---

## 2. Φ7 축 — 직관적 라벨링

| 축 | 이모지 | 한 줄 |
|----|--------|-------|
| **Meta** | 🧠 | 전체를 보는 눈 — 방법론, 자기인식, 일관성 |
| **Reverse** | 🔄 | 거꾸로 읽기 — 역방향 설계, 실패분석, 케이스스터디 |
| **Modular** | 🧩 | 조립하기 — 재사용 가능한 도구, 템플릿, 생성기 |
| **Language** | 💬 | 언어로 마감 — 프레이밍, 내러티브, 출판 |
| **Zoom** | 🔍 | 스케일 조절 — 개인→도시→국가로 확대 |
| **Spiral** | 📈 | 반복 상승 — 성장 궤적, 발전 로드맵 |
| **Quantum** | ⚡ | 도약 — 예측, 시뮬레이션, 이변 계산 |

---

## 3. 현재 전시물 → Φ7 재배치

| 전시물 | 현재 | → | Φ7 | 이유 |
|--------|------|---|-----|------|
| KFA Φ-I-C-K-P 시뮬레이터 | THINK | → | ⚡ Quantum | 30시즌 시뮬레이션, 이변 예측 |
| WC2026 Φ-I-C-K-P 예측 MCP | THINK | → | ⚡ Quantum | MC 10K, 48팀 예측 |
| PARKSY ELECTION MCP | THINK | → | 🔍 Zoom | 유권자→선거→정치 스케일 |
| Φ7 정치 MCP (B2B) | THINK | → | 🔍 Zoom | 정치인 개인→정책→선거구 |
| 재무비율을 철학하는 모델 | THINK | → | 🧩 Modular | 12비율 × 5관점 조합 모듈 |
| PARKSY MCP METHODOLOGY | FRAME | → | 🧠 Meta | 방법론 자체를 설계하는 메타 |

---

## 4. 비어있는 축 — 향후 슬롯

| Φ7 | 현재 | 향후 채울 자산 |
|----|------|----------------|
| 🧠 Meta | MCP METHODOLOGY 1개 | PHL 스펙, 삼각실행루프 전시물 |
| 🔄 Reverse | 없음 | WC2026 케이스스터디, 실패→학습 분석 |
| 🧩 Modular | 재무비율 1개 | Chalkboard Generator, PWA Generator |
| 💬 Language | 없음 | 언어철학 백서, Editorial Generator |
| 🔍 Zoom | 정치 2개 | 도시 의제 분석, 예산 분석 |
| 📈 Spiral | 없음 | 발전 로드맵, DEVPLAN 시리즈 |
| ⚡ Quantum | 축구 2개 | 시뮬레이션 추가, 예측 모델 확장 |

---

## 5. 전환 방법 — 코드 변경 범위

### 필터 버튼 (index.html:447~451)

```html
<!-- 현재 -->
<button data-cat="THINK">🎯 THINK</button>
<button data-cat="MAKE">✍️ MAKE</button>
<button data-cat="DRAW">🔬 DRAW</button>
<button data-cat="FRAME">📐 FRAME</button>

<!-- 변경 후 -->
<button data-cat="Meta">🧠 Meta</button>
<button data-cat="Reverse">🔄 Reverse</button>
<button data-cat="Modular">🧩 Modular</button>
<button data-cat="Language">💬 Language</button>
<button data-cat="Zoom">🔍 Zoom</button>
<button data-cat="Spiral">📈 Spiral</button>
<button data-cat="Quantum">⚡ Quantum</button>
```

### 카드 데이터 (category 값 6개만 변경)

```js
// KFA 시뮬레이터
category: 'Quantum'  // THINK에서

// WC2026 MCP
category: 'Quantum'  // THINK에서

// ELECTION MCP
category: 'Zoom'     // THINK에서

// Φ7 정치 MCP
category: 'Zoom'     // THINK에서

// 재무비율 모델
category: 'Modular'  // THINK에서

// MCP METHODOLOGY
category: 'Meta'     // FRAME에서
```

**변경 범위: 필터 버튼 4→7개, category 값 6개. 나머지 코드 건드리지 않음.**

---

## 6. OrbitPrompt 전체 자산 → Φ7 매핑 (전체 맵)

레포 전체 파싱 기준. 갤러리에 올릴 수 있는 자산 전부.

### ⚡ Quantum
- `football-model/mcp/server.py` — WC2026 예측 MCP ✅ 갤러리 있음
- `football-model/wc2026-predictor.html` — 예측기 HTML
- `football-model/index.html` — KFA 시뮬레이터 ✅ 갤러리 있음
- `api/election_mcp.py` — 선거 시나리오 MCP

### 🔍 Zoom
- `political-mcp/server.py` — 정치 MCP ✅ 갤러리 있음
- `api/election_mcp.py` — ELECTION MCP ✅ 갤러리 있음
- `prompts/election/` — 선거 분석 프롬프트 5종

### 🧩 Modular
- `parksy-finance-mcp/server.py` — 재무비율 MCP ✅ 갤러리 있음
- `prompts/chalkboard/` — Chalkboard Generator
- `prompts/apk/` — PWA Generator
- `prompts/editorial/` — Editorial Generator
- `prompts/identity/` — Identity Engine
- `orbit/templates/` — 6개 재사용 템플릿

### 🧠 Meta
- `boards/mcp-methodology.html` — MCP 방법론 ✅ 갤러리 있음
- `docs/TRIANGULAR-STAFF-METHOD.md` — 삼각실행루프
- `PHL_SPEC.md` — PHL 프로토콜 전체
- `docs/MCP_DEVELOPMENT_METHODOLOGY.md`

### 💬 Language
- `prompts/publisher/` — KDP 출판
- `prompts/dictionary/` — 언어 사전 (개념/감정/클리셰)
- `prompts/broadcast/` — 방송 프롬프트
- 언어철학 백서 (오늘 DeepSeek 생성, 아직 미정착)

### 🔄 Reverse
- `football-model/case-study-wc2026.html` — 케이스스터디
- `engine/endpoint_classifier.py` — 역방향 분류기
- `docs/dev-logs/` — 삽질 로그

### 📈 Spiral
- `docs/DEVPLAN-v1.md` → `DEVPLAN_FINAL.md` → `DEVPLAN_FINAL_v2_MERGED.md` — 발전 궤적
- `pd-claude/WORKLOG.md` — 작업 로그
- `pd-cockpit/` — PD 코크핏 시리즈

---

## 7. 왜 7축이 THINK/MAKE보다 나은가

```
THINK/MAKE/DRAW/FRAME:
  - 동사 기반 ✅
  - 직관적 ✅
  - 박씨 철학과 무관 ❌
  - DRAW 비어있는 구조적 문제 ❌

Φ7:
  - 박씨 철학 자체 ✅
  - 7개 자리마다 채울 자산 존재 ✅
  - OrbitPrompt=Φ드라이버 전시관 정합성 ✅
  - 이름이 낯설 수 있음 → 이모지+한 줄 설명으로 보완 ✅
```

---

## 8. 실행 순서

```
Step 1. index.html 필터 버튼 4개 → 7개 교체
Step 2. 6개 카드 category 값 변경
Step 3. 빈 축(Reverse/Language/Spiral)에 planned 슬롯 2~3개 추가
Step 4. GitHub 푸시 → GitHub Pages 반영

예상 시간: 30분
```

---

*저장: OrbitPrompt/docs/ — DeepSeek가 이 문서 읽고 Step 1~4 바로 실행*
