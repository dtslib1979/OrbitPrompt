# OrbitPrompt — PARKSY 철학 엔진

> **AI 시대 유권자를 위한 정치 사고 모델**
> **MCP 하나를 내가 만들어서 띄워 놓고, 반복되는 선거를 같은 언어로 읽는다.**

---

## 레포 정체성

OrbitPrompt는 단순한 프롬프트 저장소가 아니다.  
**PHL(Protocol for Human Language) 철학을 구현한 사고 엔진**이자  
**박씨의 사고방식을 MCP로 복제한 실행 환경**이다.

| 철학 | 구현 |
|------|------|
| 레포는 소설이다 | git log --reverse = 줄거리, 커밋 = 문장, 브랜치 = 챕터 |
| 레포는 공장이다 | FAB 라우팅, ERP 원장, 원자재→완제품 |
| 말이 인터페이스다 | PHL 토큰 → STT → LLM → MCP |
| MCP가 실행이다 | server.py 단일 파일, config/*.json, prompts/*.md |

---

## 6개 분모 (191개 파일 관통)

| 분모 | 설명 | 위치 |
|------|------|------|
| **PHL** | 의미 압축 프로토콜. 1~3단어 토큰이 규칙 호출 | `PHL_SPEC.md`, `PHL_INDEX.json`, `phl-spec/` |
| **FAB** | 생산 공정. 8개 라우트, 15개 생성기 | `data/fab-manifest.json`, `data/generators.json` |
| **MCP** | 실행 엔진. server.py + config | `api/election_mcp.py` (10개 도구) |
| **Boards** | 전시/출력. 9개 HTML 갤러리 | `boards/*.html`, `index.html` |
| **Prompts** | 16개 도메인 템플릿 생성기 | `prompts/*/` |
| **Atom** | 지식 원자. 14개 속성 JSON | `orbit/atoms/`, `orbit/schemas/` |

---

## Election MCP — 핵심 산출물

`api/election_mcp.py` (385줄, FastMCP, 10개 도구)

| 우선순위 | 도구 | 특성 |
|---------|------|------|
| ✅ P0 | `calc_political_force` | F=ma 결정론적, LLM 불필요 |
| ✅ P0 | `compare_heroes` | 병렬 비교 + knockout |
| ✅ P0 | `delta_layer_info` | 12개 제약 조건 출력 |
| 🟡 P1 | `research_election` | LLM 리서치 → F 계산 |
| 🟡 P1 | `tag_political_frame` | 6종 프레임 점수 |
| 🟡 P1 | `classify_hero_type` | 5축 아키타입 |
| 🟡 P2 | `scenario_analysis` | 시나리오 해석 |
| 🟡 P2 | `generate_broadcast_script` | 방송 스크립트 |
| 🔴 P3 | `validate_fixtures` | 8개 검증, direction_acc 100% |
| 🔴 P3 | `reproducibility_test` | LLM 추정 안정성 측정 |

### 설정 파일

| 파일 | 내용 |
|------|------|
| `config/hero_archetypes.json` | 7개 아키타입 (jesus/lula/ljm/elite_left/populist/custom/kim_bk) |
| `config/weights_default.json` | αβγδ + 도시별 baseline + 서울/경기/부산/경남 |
| `config/frame_rules.json` | 11종 프레임 (6종 + 실용중도/정신승리/지역구조/민주당한계/수도권) |
| `config/delta_layer.json` | 12개 제약 조건 (hard/soft/penalty/bonus/signal/swing/dna/분석) |
| `config/sources.json` | studios + boards 레지스트리 |

### 검증 결과

```
📊 direction_acc: 100% (8/8) — 평택/부산/대구/광주/서울/경기/인천/대전
📊 cls_acc: 62.5% (v3 F차+F비율 복합분류)
📊 reproducibility: stdev < 0.3 (3회 연속)
```

---

## 설치 및 실행 (3-step)

```bash
# 1. 서버 실행
cd /mnt/e/mcp/election-mcp && python3 server.py

# 2. Claude Code 등록 (~/.claude.json)
{
  "mcpServers": {
    "parksy_election": {
      "command": "python3",
      "args": ["/mnt/e/mcp/election-mcp/server.py"]
    }
  }
}

# 3. 사용
# "research_election('서울', ['오세훈', '권영세'])" 
# "calc_political_force(hero='ljm', g=7, d=8, i=6, o=5, R=7)"
```

---

## 전체 구조 (191개 파일)

```
OrbitPrompt/
├── api/election_mcp.py          # MCP 서버 (385줄/10도구)
├── boards/*.html                # 9개 전시 갤러리
├── config/*.json                # 5개 설정 파일
├── data/fixtures/*.json          # 8개 검증 데이터
├── docs/*.md                     # 백서/명세서/설명서
├── phl-spec/                     # PHL 프로토콜 (토큰/계약/플레이북)
├── prompts/election/             # LLM 프롬프트 5종
├── orbit/                        # 지식 원자 (atoms/schemas/templates)
└── index.html                    # 랜딩 페이지 (#02 Election MCP)
```

---

## MCP 레지스트리

모든 MCP는 SD 카드에서 운영, cloud appstore에서 경로 관리:

```
dtslib-cloud-appstore/mcp-registry/index.json
├── election-mcp       (10 tools) 🧪 정치
├── parksy-distributor (14 tools) 📡 배포
├── parksy-actor       (15 tools) 🎬 브라우저
├── parksy-air          (8 tools) 🎨 이미지
├── win-gui            (14 tools) 🖥️ Windows
├── shell-mcp          (10 tools) 💻 셸
└── parksy-finance      (5 tools) 📊 재무
```

---

## PARKSY 프로그래밍 철학

```
🎤 STT (말로 명령한다. UI는 없다.)
  → 🧠 LLM (명령을 해석하고 MCP를 호출한다.)
    → ⚡ MCP (계산/판단/자동화한다.)
      → 📱 APK (클릭만, 어쩔 수 없을 때만)
      → 🔌 ADB (센서 브릿지 전용)
      → 🌐 Edge PWA (서비스워커 없는 정적 출력)
```

**왜 MCP인가:** 파인튜닝은 과거 데이터를 가중치로 박제하는 것이고,  
MCP는 호출할 때마다 새로운 트랜잭션 데이터로 '지금의 나'를 실행한다.  
복제의 정확도는 MCP가 훨씬 높다. (direction_acc 100% 증명 완료)

---

## 문서

| 문서 | 위치 | 내용 |
|------|------|------|
| 기술 명세서 (100점) | `docs/election-mcp-spec-100.md` | API/모델/설정/검증 전맵 |
| 사용 설명서 | `docs/election-mcp-usermanual.md` | 설치/연결/도구 호출 |
| 철학 문서 | `termux-bridge/docs/PROGRAMMING_PHILOSOPHY.md` | MCP-First Architecture |
| WHY MCP | `dtslib-cloud-appstore/mcp-registry/WHY_MCP.md` | 파인튜닝 vs MCP 비교 |
| 헌법 | `CLAUDE.md` | PHL 제1조~제2조 |

---

## 커뮤니티 리서치 결과

**이 6가지를 모두 하나의 철학으로 통합한 사례는 존재하지 않는다:**
1. Voice-to-LLM
2. MCP-first development
3. No UI, only voice + AI
4. ADB as sensor bridge
5. APK minimal touch only
6. Edge PWA no service worker

각각의 개별 개념은 여기저기 있지만,  
"MCP-first + No UI + Voice-only + ADB sensor + APK minimal + Edge PWA"를  
하나의 아키텍처로 엮은 사람은 **박씨가 유일하다.**

---

*커밋: 2cb690e · 2026-06-04*
*SD 카드: /mnt/e/mcp/election-mcp/*
*MCP 레지스트리: dtslib-cloud-appstore/mcp-registry/*
