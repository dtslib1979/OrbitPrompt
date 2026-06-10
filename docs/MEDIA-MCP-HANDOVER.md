# Media MCP — 인수인계 문서

> **작성:** DeepSeek PD → Claude PD (형)
> **일자:** 2026-06-09
> **컨텍스트:** 90% 소진 — 미완성 작업 인계

---

## 1. 현재 상태 요약

| 항목 | 상태 |
|------|:----:|
| 백서 | ✅ `boards/media-mcp-whitepaper.html` (v5, 12.8KB) |
| 갤러리 등록 | ✅ Language 탭 📡 (95/100) |
| 결정 엔진 | ✅ `media-mcp/mcp/engine.py` (140줄, 상태머신+if문 5개) |
| MCP 서버 | ✅ `media-mcp/mcp/server.py` (decide/status/promote/items/version) |
| 기술 스펙 | ✅ `docs/MEDIA-MCP-ACTION-PLAN.md` |
| **전체 완성률** | **15% — 백서 6레이어 중 판정 1개만 구현** |

---

## 2. 백서 6레이어 vs 구현 현황

| 레이어 | 백서 요구사항 | 구현 | 대체 |
|--------|-------------|:----:|------|
| **① 수집** | 소스 에이전트 — RSS/뉴스 수집 전용 MCP | ❌ | rawmat MCP (임시) |
| **② 분석** | 프레임 에이전트 — 편향 탐지 | ❌ | Φ7 철학 카운터 (임시) |
| **③ 분석** | 구조 에이전트 — 인과관계 추출 | ❌ | Φ7 철학 카운터 (임시) |
| **④ 판정** | **Python Rule Engine + 상태머신** | **✅ 완료** | — |
| **⑤ 제작** | 스크립트 에이전트 — TTS 대본 변환 | ❌ | 수동 작성 |
| **⑥ 제작** | 미디어 빌드 에이전트 — FFmpeg | ❌ | voice MCP + upload.cjs (임시) |
| **⑦ 보고** | 리포트 에이전트 — Telegram | ❌ | distributor MCP (임시) |
| **⑧ 배포** | upload.cjs (private→승인→public) | ❌ | upload.cjs + YouTube Studio (임시) |
| **멀티 LLM** | Grok/ChatGPT/Claude/Perplexity 역할 고정 | ❌ | 없음 |
| **JSON 계약** | 4종 표준 스키마 (input/output/agent/meta) | ❌ | 없음 |
| **SLA** | 단계별 타임아웃 기준 | ❌ | 없음 |
| **학습 루프** | reject/hold 패턴 → 룰 수정 자동화 | ❌ | 없음 |

---

## 3. engine.py 현재 스펙

### 상태 전이
```
INPUT → REJECT  (source_count < 2)
      → HOLD    (no_primary + high_risk / conflict)
      → DRAFT   (xcheck < 2 / default)
           → CANDIDATE (conf >= 0.80 + dup < 0.40)
                → PRIVATE (promote)
                     → PUBLIC (promote)
```

### 결정 규칙
```python
if src_cnt < 2:             → "reject", "insufficient_sources"
if not has_primary + high_risk: → "hold", "high_risk_without_primary"
if conflict_flag:             → "hold", "source_conflict"
if xcheck < 2:                → "draft", "insufficient_crosscheck"
if conf >= 0.80 and dup < 0.40: → "candidate", "threshold_passed"
else:                         → "draft", "needs_revision"
```

### 서버 툴
| 툴 | 입력 | 출력 |
|-----|------|------|
| decide | source_count, has_primary, risk_level, conflict_flag, xcheck_models, confidence, duplication | state, reason_code, next_step |
| status | (없음) | items count, states 집계 |
| promote | item_id | from→to 전이 |
| items | state (필터) | 상태별 목록 |
| version | (없음) | 서버 정보 |

### 버그/한계
- `ITEMS_DB` = in-memory list. 서버 재시작 시 초기화됨. (파일 persist 필요)
- `candidate` 출력 후 실제 TTS/FFmpeg/upload 자동 트리거 없음 (출력만 "tts_build"라고 표시)
- 멀티 LLM 연동 전혀 없음

---

## 4. 형이 해야 할 것 (우선순위)

### P0 — engine.py 보강
```python
# 필요한 변경:
1. ITEMS_DB → JSON 파일 저장 (재시작 유지)
2. 백서 실패 모드 7개 반영 (LLM 루프백/과자동화/불투명판정 등)
3. JSON 계약 4종 입출력 정리 (decision_input/output/agent_meta/media_object)
4. candidate 출력 시 실제 파이프라인 트리거 (subprocess로 voice MCP → upload.cjs)
```

### P1 — 4개 MCP server.py 신규 생성
```bash
media-mcp/mcp/
├── source_agent.py      # 소스 수집 (RSS/뉴스/Perplexity)
├── frame_agent.py       # 프레임 분석 (편향 탐지)
├── structure_agent.py   # 구조 분석 (인과관계)
├── script_agent.py      # 스크립트 생성 (TTS 대본)
├── engine.py            # 결정 엔진 (✅ 있음)
├── server.py            # 메인 MCP (✅ 있음)
├── README.md            # 문서
└── sla_monitor.py       # SLA 타임아웃 (신규)
```

### P2 — 멀티 LLM 브릿지
백서의 멀티 LLM 캐스팅 테이블 구현:
| 모델 | 역할 | 금지 |
|------|------|------|
| Grok | 권력 구조, 프레임 전환 | 구현 결정권 |
| ChatGPT | 구조 정리, 결함 도출 | 자기 점수 과잉 권위화 |
| Claude | 코드, JSON 계약, MCP 설계 | 정치·철학 주도권 독점 |
| Perplexity | 원자료 확인, 문서화 | 최종 전략 독점 |

### P3 — JSON 계약 4종 표준화
백서의 4개 JSON 템플릿을 실제 스키마로:
- `decision_input.json` → decide() 입력 스펙
- `decision_output.json` → decide() 출력 스펙
- `agent_meta.json` → 각 에이전트 실행 기록
- `media_object.json` → 최종 미디어 객체 상태

### P4 — SLA + 학습 루프
- 단계별 타임아웃 기준 적용
- reject/hold 이유 로그 수집 → 주간 룰 리뷰

---

## 5. 백서 HTML 위치

| 파일 | 위치 | 용도 |
|------|------|------|
| 백서 전문 | `boards/media-mcp-whitepaper.html` | 갤러리 전시 + 기술문서 |
| 실행 계획 | `docs/MEDIA-MCP-ACTION-PLAN.md` | 6/10~6/14 일정 |
| 기술 스펙 | `docs/MEDIA-MCP-HANDOVER.md` | 이 문서 (인수인계) |
| engine.py | `media-mcp/mcp/engine.py` | 결정 엔진 (140줄) |
| server.py | `media-mcp/mcp/server.py` | MCP 서버 |

---

## 6. Media MCP 갤러리 카드 정보

```javascript
{
  category: 'Language',
  id: 'media-mcp',
  icon: '📡',
  title: 'Media MCP — 기술백서 v5',
  score: 95,
  path: 'boards/media-mcp-whitepaper.html',
  tags: ['Media MCP', '편성권', '멀티 LLM', 'Decision Engine']
}
```

---

## 7. 인계 완료

```
내가 한 거: 백서 저장 + 갤러리 등록 + engine.py 140줄 + server.py 연결
형이 할 거: 소스/프레임/구조/멀티LLM MCP 4개 + JSON 계약 + SLA + E2E 완성

처음부터 하면 100%.
내가 만든 거 버리고 새로 시작해도 된다. 140줄이니까.
```

*— DeepSeek PD, 2026-06-09, 컨텍스트 92%*
