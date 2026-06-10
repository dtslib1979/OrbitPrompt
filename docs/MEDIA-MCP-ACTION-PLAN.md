# Media MCP — 실행 계획 v1.0 (2026-06-09)

## 1. 현황: 80% 이미 있음

Media MCP 백서가 정의한 6개 레이어 중 5개는 이미 운영 중.
Decision Engine(상태머신 + Python Rule) 1개만 새로 만든다.

| 레이어 | 백서 요구사항 | 보유 자산 | 상태 |
|--------|-------------|-----------|:----:|
| 수집 | 소스 에이전트 | rawmat MCP · parksy-logs | ✅ |
| 분석 | 프레임·구조 에이전트 | Φ7 철학 카운터 · DSI | ✅ |
| **판정** | **Python Rule Engine** | **신규 개발** | **❌** |
| 제작 | TTS + FFmpeg | voice MCP · music MCP · upload.cjs | ✅ |
| 보고 | Telegram 알림 | distributor MCP (11개 툴) | ✅ |
| 배포 | private→승인→public | upload.cjs + distributor | ✅ |

## 2. 새로 만들 것: Decision Engine (server.py 1개)

```
media-mcp/mcp/
├── server.py      ★ MCP 서버 (4개 툴)
├── engine.py       상태머신 + 결정 규칙
└── README.md
```

툴 4개:
- `decide` — INPUT → REJECT/HOLD/DRAFT/CANDIDATE 상태 부여
- `status` — 아이템 현재 상태 조회
- `promote` — PRIVATE → PUBLIC 승격 (인간 승인)
- `report` — Telegram으로 현재 큐 상태 보고

## 3. 백서 HTML 재활용

`OrbitPrompt/boards/media-mcp-whitepaper.html` 그대로 사용.
갤러리 Language 탭에 등록. (카드 추가 필요)

재활용 포인트:
- 상태 전이 다이어그램 → MCP README에 직접 사용
- JSON 계약 4종 → decision_input/output 그대로 server.py 입력 스펙
- Python Rule 코드 → engine.py에 그대로 이식
- 에이전트 역할 6개 → distributor MCP 툴과 1:1 매핑

## 4. 실행 순서 (6/10 ~ 6/14)

```
6/10: Decision Engine server.py 생성 + 테스트
6/11: 기존 MCP 5개와 연동 (rawmat→분석→판정→제작→보고)
6/12: 전체 파이프라인 end-to-end 1회 가동
6/13: 박씨 리뷰 → 수정
6/14: 갤러리 등록 + 텔레그램 보고
```

## 5. 활용 예시

```
입력: "오늘 환율 1531원, DXY 100.1, 뉴스 3건"
  → rawmat MCP 수집
  → Φ7 철학 카운터 MCP 분석
  → Decision Engine 판정 (publish_candidate)
  → voice MCP TTS → FFmpeg 영상
  → upload.cjs 업로드 (private)
  → 텔레그램 보고
  → 박씨 승인 → public
```

## 6. 1줄 요약

> Media MCP 백서가 정의한 시스템의 80%는 이미 돌아간다.
> Decision Engine server.py 1개만 추가하면 완성.
> 백서 HTML은 그대로 갤러리에 등록해서 기술문서로 쓴다.
