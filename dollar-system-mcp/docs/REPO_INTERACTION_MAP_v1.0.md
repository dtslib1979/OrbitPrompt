# 레포지토리 상호작용 맵 — 박씨 생태계 조직도
### v1.0 | 2026.06.30 | 기준: PEM MCP 4사분면 구현 완료 시점

---

## 0. 이 문서의 목적

**레포는 각자 따로 노는 게 아니다.** 28개 레포는 회사 조직처럼 상호작용한다.
철학(100서)이 완성되고 MCP로 코드화되면서, 각 레포의 역할이 명확해졌다.
이 맵은 그 상호작용을 정리해서, 새 레포를 만들거나 기존 레포를 수정할 때
"이게 어느 부서 일이고 누구한테 보고해야 하는지"를 알기 위해 존재한다.

---

## 1. 조직도 — 5개 부서 + 인프라

```
                    ┌─────────────────────────────┐
                    │     100서 (FX_PHILOSOPHY)    │
                    │     철학 = 헌법              │
                    └──────────┬──────────────────┘
                               │ 철학을 코드로 박음
                               ▼
                    ┌─────────────────────────────┐
                    │  dollar-system-mcp           │
                    │  (parksy-economy-fx)         │
                    │  제조/엔지니어링              │
                    │  26개 툴 / 4사분면           │
                    └──┬────┬────┬────┬───────────┘
                       │    │    │    │
             ┌─────────┘    │    │    └──────────┐
             ▼              ▼    ▼               ▼
     ┌────────────┐  ┌──────────┐  ┌────────────────┐
     │ eae-univ   │  │ parksy-  │  │ parksy-        │
     │ 지식갤러리  │  │ rawmat   │  │ distributor    │
     │ 출판/전시   │  │ 원자재   │  │ 유통/물류      │
     └────────────┘  └──────────┘  └────────────────┘
                              ▲
                              │
                     ┌────────┴────────┐
                     │  parksy-logs    │
                     │  parksy-audio   │
                     │  parksy-image   │
                     │  OrbitPrompt    │
                     │  etc. (28레포)   │
                     │  생산 현장       │
                     └─────────────────┘
```

---

## 2. 부서별 역할

### 2.1 철학/헌법 — 100서 (FX_PHILOSOPHY_100seo.md)

| 역할 | 담당 |
|------|------|
| 모든 MCP의 존재 이유 | "이건 왜 만드는가"에 답함 |
| GATE 0 인식론의 원천 | 데이터 검증 기준의 철학적 근거 |
| 변경 주기 | 거의 안 바뀜 (철학은 한 번 정해지면 안 흔들림) |
| 영향 범위 | 생태계 전체 |

**위치**: `dollar-system-mcp/FX_PHILOSOPHY_100seo.md`
**정식 명칭**: "박씨의 환율 철학 — 100서(百書)"

### 2.2 제조/엔지니어링 — dollar-system-mcp

| 모듈 | MCP 툴 | PEM 사분면 | 원재료 공급처 |
|------|--------|-----------|-------------|
| FX Engine | 17개 툴 | Q1 (환율) | yfinance |
| module11 | ai_labor_rate, ai_vs_human, labor_fee | Q4 (임률) | OrbitPrompt 세션로그 |
| module12 | platform_fee, view_anomaly_check, platform_reduce | Q2 (플랫폼) | parksy-distributor |
| module13 | sonho_fee, attraction_capital | Q3 (소호) | namoneygoal, hoyadang |

**변경 규칙**:
- GATE 0, hegemonic_fee는 다른 MCP가 import만 함 (재작성 금지)
- source_tier 의무 표기 — 데이터 등급 없으면 C급 페널티
- 출력물은 항상 사후분석 워터마크 포함

### 2.3 출판/갤러리 — eae-univ

| 디렉토리 | 내용 | 연결된 MCP |
|---------|------|-----------|
| courses/ | 과정 메타데이터 (6개, 전부 draft) | — |
| research/body/ | Perplexity 경제/철학 리서치 | parksy-rawmat |
| research/butterfly/ | Perplexity 자유 리서치 | parksy-rawmat |
| whitepaper/ | 백서 (whitepaper-v0, AI-functioner) | dollar-system-mcp |
| broadcast/ | 편집술 스킬셋 + 인터랙티브 게임 | — |
| philosophy/ | EAE 세계관 철학문서 | — |
| publish/ | 퍼블리시된 HTML | 전부 |

**역할**: MCP가 생산한 지식을 **전시/교육 가능한 형태로 변환**. 
아직 courses/는 전부 draft — MCP 출력물이 게시되기 시작하면 역할이 본격화됨.

### 2.4 원자재 — parksy-rawmat

| 기능 | 내용 | 출력 |
|------|------|------|
| run_episode() | Perplexity Space 호출 | episodes.db |
| write_article() | article JSON 변환 | articles/ |
| call_space_mcp() | 특정 Space 직접 호출 | raw 텍스트 |

**역할**: Perplexity 리서치 결과를 정형화해서 eae-univ research/에 공급.
**현재 한계**: article이 MCP 툴로 노출되지 않아서 "야 철학 알려줘"에 즉답 불가.

### 2.5 유통/물류 — parksy-distributor

| 채널 | MCP 툴 | 상태 |
|------|--------|------|
| Telegram | parksy_distribute_telegram_text/photo | ✅ 작동 |
| YouTube | parksy_distribute_youtube | ✅ 작동 |
| Tistory | parksy_distribute_tistory | ✅ 작동 |
| Naver | parksy_distribute_naver | ✅ 작동 |
| Discord | parksy_distribute_discord | ✅ 작동 |

**역할**: MCP 출력물(개발일지, 보고서, 매뉴얼)을 박씨가 지정한 채널로 송출.

---

## 3. 데이터 흐름 (협업 구조)

### 흐름 A: 경제학 MCP (오늘 완성된 파이프라인)

```
100서 (철학)
  ↓ "환율은 시장이 아니다"
dollar-system-mcp (GATE 0 + 헤게모니수수료)
  ↓ 26개 툴
eae-univ (research/에 게시)
  ↓
parksy-distributor (Telegram/YouTube → 박씨)
```

### 흐름 B: Perplexity 리서치 (지금 개선 중)

```
parksy-rawmat (run_episode → write_article)
  ↓ article JSON
eae-univ (research/body + butterfly 저장)
  ↓
[지금 여기까지임 — MCP 툴化 안 돼서 재검색 불가]
  ↓ 필요함
dollar-system-mcp (knowledge-atom MCP 등록)
  ↓ "야 철학 알려줘" → 즉시 튀어나옴
```

### 흐름 C: 음악/오디오 (Q3 Q4 사이드)

```
parksy-audio (voice RVC/DiffSinger)
  │
  ├──→ parksy-music (MIDI → BGM)
  │       ↓
  │     parksy-distributor (YouTube @musician-parksy)
  │
  └──→ parksy-voice (TTS/나레이션)
          ↓
        gohsy-production (방송)
          ↓
        parksy.kr (송출)
```

---

## 4. 조직도 원칙

### 4.1 순서가 있다

```
철학(100서)이 먼저 정해져야
  → MCP(코드)가 나올 수 있음
    → eae-univ(출판)가 무슨 내용을 전시할지 결정됨
      → parksy-distributor(유통)가 어디로 보낼지 결정됨
```

이 순서가 뒤집히면 "어디다 쓰는지 모르는 코드"나 "철학 없는 콘텐츠"가 나온다.

### 4.2 각 레포는 하나의 역할

- dollar-system-mcp는 **제조만** (출판/유통 안 함)
- eae-univ는 **전시만** (제조/유통 안 함)
- parksy-distributor는 **유통만** (제조/전시 안 함)

하나가 두 역할을 하면 그 레포가 비대해져서 유지보수 불가능해짐.
이게 FX Engine v3.3의 loose coupling 원칙이 레포 단위로 확장된 버전.

### 4.3 막힌 흐름은 즉시 보인다

지금 흐름 B가 막혀 있다. parksy-rawmat → eae-univ까지는 가는데,
eae-univ → MCP 툴(검색)이 안 돼서 박씨가 "아까 그 article 뭐였지?" 하고
다시 Perplexity를 돌려야 하는 상황. 이게 "반복"의 원인.

---

## 5. 이 맵의 갱신 규칙

- 새 MCP 모듈 추가될 때마다 2.2 표 업데이트
- 새 레포가 생기면 어느 부서에 속하는지 정의
- 흐름이 막히거나 새로 열리면 3번 섹션 업데이트
- 조직도는 PEM 매트릭스가 바뀌면 같이 바뀜

---

*작성일: 2026.06.30 | 버전: v1.0 | 기준: PEM MCP 4사분면 구현 완료*
