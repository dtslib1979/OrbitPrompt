# OrbitPrompt — Election MCP 최종 개발 계획서 v2.0 (통합본)

> **작성:** 2026-06-02  
> **베이스:** DeepSeek Aider 운영형 계획서 + Claude Code 검증 설계 통합  
> **원칙:** 새 레포 생성 금지 — 전부 `OrbitPrompt/api/` + `config/sources.json` 등록  
> **MCP 레지스트리:** `dtslib-cloud-appstore/mcp-registry/`에 전 MCP 모아서 관리  
> **SSOT:** `dtslib-papyrus/hq/config/channel-repo-map.json`  
> **범위:** 28개 레포 × 15개 YouTube 채널 × 4개 계정 × 3개 방송국

---

## 0. 현재 자산 현황

### 완료
- Parksy Capture v11.0.0 release APK (20MB, 서명) ✅
- 소스 리팩토링: 2,947줄→11파일/2,143줄 ✅
- Embed Server(MiniLM) 제거, DeepSeek API 직결 ✅
- TTS 전체 읽기 (4,000자 청크) ✅
- 레포×채널 Reverse Mapping ✅
- Distributor MCP 14개 도구 인벤토리 검증 ✅

### 진행 중
| 작업 | 상태 | 조건 |
|------|------|-------|
| Election MCP | 🔶 Phase 1 준비 | 아래 로드맵 |
| youtube-setup 13/15 채널 | ⚠️ 양산 대기 | 박씨 결재 |
| account c branding 403 | ⚠️ 펜딩 | OAuth 재발급 |

---

## 1. Election MCP — 프로젝트 정의

### 한 줄 정의
> **LLM이 리서치하고 Python이 계산하는 정치 예측 엔진**

### 철학 (PHL 정합)
```
OrbitPrompt PHL: "한 단어(토큰)로 정의된 수백 줄 규칙을 호출"
Election MCP:   "research_election('서울','홍준표') 한 줄로 17개 변수 → F 계산"
```

### 역할 분담 (고정)
| 역할 | 담당 | 책임 |
|------|------|------|
| **박씨** | 이론 제공 + 임계값 결정 | 정치 모델 방향, 10/20/30 기준 |
| **Claude Code** | MCP 서버 + 수학 모델 구현 | F=ma 계산, knockout 판정 |
| **LLM (runtime)** | 실시간 리서치 + 파라미터 추정 | 감정 점수, 구조 변수 추출 |

> **LLM은 데이터 저장 안 함. CSV 수집 안 함. 웹 스크래핑 안 함. DB 구축 안 함.**  
> 매번 호출 시 실시간으로 리서치해서 JSON 파라미터만 반환.

---

## 2. 변수 체계

### 2-A. 감정 드라이버 (8개, 0~100)

| 변수 | 의미 | LLM 추정 근거 |
|------|------|--------------|
| `fear` | 공포/불안 | 경제 위기, 안보, 코로나 등 |
| `anger` | 분노/반발 | 부정선거 의혹, 검찰 탄압, 언론 편향 |
| `loss` | 박탈감 | 내 집 마련 실패, 양극화 |
| `joy` | 획득 기쁨 | 복지 확대, 주가 상승 |
| `disgust` | 혐오/배척 | 극우 혐오, 세대 갈등 |
| `trust` | 신뢰/연대 | 리더십, 공동체 의식 |
| `shock` | 불안정/놀람 | 정치 이벤트, 스캔들 |
| `hope` | 기대/희망 | 변화 기대, 세대 교체 |

### 2-B. 구조 변수 (9개, 0~100)

| 변수 | 의미 |
|------|------|
| `incumbent_advantage` | 현직/기득권 프리미엄 |
| `challenger_force` | 도전자 돌파력 |
| `generational_backlash` | 세대 반동 강도 |
| `pragmatic_capture` | 실용 프레임 흡수력 (이재명 포지션) |
| `organization_power` | 조직력/지방 토호 |
| `media_story_power` | 미디어 서사 영향력 |
| `elite_fragmentation` | 엘리트 분열도 |
| `far_right_drift` | 보수 극우화 |
| `regional_bossism` | 지역 보스 구조 |

### 2-C. 컨텍스트 (6개, 0~100)

`two_party_pressure`, `polarization`, `turnout_energy`, `anti_incumbent_cycle`, `economic_anxiety`, `democracy_fatigue`

---

## 3. 모델 설계

### 3-A. F=ma 정치 변화력 (보조 엔진 — 서사/방송용)

```python
negative = mean(fear, loss, disgust, shock)
positive = mean(anger, joy, trust, hope)

g = mean(incumbent_advantage, organization_power, media_story_power)  # 저항 질량
d = mean(challenger_force, generational_backlash)                      # 도전 가속
i = mean(pragmatic_capture, elite_fragmentation)                      # 매개/분열
o = mean(far_right_drift, regional_bossism)                            # 조직 보수

m_eff = 100 * k  # k = 미디어/조직 승수
a = α*g + β*d + γ*i + δ*o  # αβγδ = 가중치 (config)
F = m_eff * a
R = mean(negative, g) * 0.8  # 저항력

overthrow = F > R  # 전복 가능성
```

### 3-B. 선거 예측 모델 (본 엔진 — 실제 예측용)

```python
champion_resilience = (R * 0.6 + g * 0.4)
challenger_momentum = (d * 0.5 + positive * 0.3 + i * 0.2)
perceived_difference = abs(challenger_momentum - champion_resilience) / 1.9
net_edge = challenger_momentum - champion_resilience

knockout_probability = min(100,
    (perceived_difference / 30) * 70 + max(0, net_edge) * 0.8)
```

### 3-C. 임계 구간 (박씨 10/20/30 체감차)

| perceived_difference | 분류 | 의미 |
|--------------------|------|-------|
| `< 10` | `weak_signal` | 현상 유지, 유의미한 격차 없음 |
| `10 ~ 20` | `visible_but_contestable` | 체감되나 뒤집힐 수 있음 |
| `20 ~ 30` | `clear_change` | 명확한 변화, 트렌드 전환 |
| `>= 30` | `knockout_frame_shift` | 압도적 격차, 프레임 전환 |

---

## 4. MCP 서버 설계

### 4-A. 파일 위치 (새 레포 생성 금지)

```
OrbitPrompt/
├── api/
│   └── election_mcp.py        # FastMCP 서버 — 단일 파일
├── config/
│   └── sources.json            # "studios"에 "election" 등록
├── prompts/
│   └── election/               # LLM 리서치용 프롬프트
│       ├── research.md
│       ├── compare.md
│       └── scenario.md
└── data/
    └── fixtures/               # 검증용 고정 테스트셋 (Phase 3)
        ├── pyeongtaek.json
        ├── busan.json
        └── daegu.json

dtslib-cloud-appstore/
└── mcp-registry/
    └── election-mcp.json       # MCP 레지스트리 등록
```

### 4-B. 7개 MCP 도구

| # | 도구 | 입력 | LLM 필요? | 우선순위 |
|---|------|------|----------|---------|
| 1 | `calc_political_force` | 17개 변수 JSON | ❌ | P0 |
| 2 | `compare_heroes` | heroes[name,params][] | ❌ | P0 |
| 3 | `tag_political_frame` | 텍스트 | ✅ | P0 |
| 4 | `research_election` | region, candidates | ✅ | P1 |
| 5 | `classify_hero_type` | 인물 설명 | ✅ | P1 |
| 6 | `scenario_analysis` | 시나리오 텍스트 | ✅ | P2 |
| 7 | `generate_broadcast_script` | 분석 결과 | ✅ | P2 |

### 4-C. 기술 스택

```python
from fastmcp import FastMCP
mcp = FastMCP("parksy-election-mcp")

@mcp.tool()
async def research_election(region: str, candidates: list[str]) -> dict:
    llm_params = await llm_research(region, candidates)
    result = calc_F(**llm_params)
    return result

@mcp.tool()
def calc_political_force(params: PoliticalParams) -> PoliticalResult:
    return calc_F(params)
```

---

## 5. 검증 설계 (이 파트가 v1.0 대비 핵심 추가)

### 5-A. 고정 테스트셋 (Phase 3 전 필수)

`data/fixtures/`에 다음 3개 지역 고정:

| 파일 | 지역 | 선거 | 특징 |
|------|------|------|-------|
| `pyeongtaek.json` | 평택 | 지역구 | 조직력 vs 도전자 |
| `busan.json` | 부산 | 광역 | 지역 보스 구조 |
| `daegu.json` | 대구 | 광역 | 보수 텃밭, 극우화 |

각 fixture는:
- 수동 세팅한 17개 변수
- 실제 득표율 (출처: 중앙선관위)
- 기대 classification

### 5-B. 정확도 기준

| 기준 | 정의 | 목표 |
|------|------|-------|
| 승패 방향 | 모델 우세 후보 = 실제 승자 | 100% (3/3) |
| 격차 구간 | perceived_difference 구간 일치 | 66% (2/3) |
| 오차 범위 | knockout_probability ±15%p | Phase 4에서 측정 |

### 5-C. 재현성 테스트

```
1. 같은 fixture를 LLM에 3회 제시
2. LLM이 추정한 파라미터의 표준편차 측정
3. 표준편차가 임계(예: ±10) 넘으면 해당 변수 보정 필요
```

---

## 6. 실행 로드맵

### Phase 1 (즉시) — 코어 모델 + MCP 기초

```
□ OrbitPrompt/prompts/election/ 디렉토리 생성
□ api/election_mcp.py — calc_political_force + compare_heroes (LLM 불필요)
□ config/sources.json "studios"에 "election" 등록
```

### Phase 2 (1회) — LLM 연동

```
□ research_election 구현 (LLM 리서치 + Python 계산)
□ tag_political_frame 구현
□ classify_hero_type 구현
□ prompts/election/ 프롬프트 파일 분리
```

### Phase 3 (검증) — 실전 테스트

```
□ data/fixtures/ 3개 지역 고정셋 생성
□ 재현성 테스트 (같은 질문 3회 → 파라미터 표준편차 측정)
□ perceived_difference 임계값 튜닝
```

### Phase 4 (선택) — 배포

```
□ dtslib-cloud-appstore/mcp-registry/ 등록
□ stdio 모드 Claude Code 연동
□ streamable-http Railway 배포 (선택)
```

---

## 7. 분산 가중치 전략 (오픈 모듈러)

```text
config/
├── weights_default.json        # 박씨 기준
├── weights_progressive.json    # 진보 시각
├── weights_conservative.json   # 보수 시각
├── frame_rules.json            # 6종 프레임 규칙
└── hero_archetypes.json        # 인물 유형 분류
```

이렇게 하면 누구나 자기 정치 전제에 맞게 포크 가능.
"박씨 모델"이 아니라 "너의 모델"이 되는 구조.

---

## 8. 금지사항 (위반 시 즉시 롤백)

```
❌ 새 레포 생성 — 전부 OrbitPrompt/api/에 통합
❌ FROZEN 레포 터치
❌ 과거 선거 데이터 CSV 수동 수집 — LLM이 리서치함
❌ 웹 스크래퍼 구현
❌ 데이터베이스 구축
❌ DB 설계
❌ "Phase 3 없이 완성했다고 속이기"
```

---

## 9. MCP 통합 레지스트리 (dtslib-cloud-appstore)

모든 MCP는 여기서 관리:

```
dtslib-cloud-appstore/
└── mcp-registry/
    ├── distributor-mcp.json    # parksy-distributor (14개 도구)
    ├── election-mcp.json       # parksy-election-mcp (7개 도구) ← 신규
    └── README.md
```

등록 포맷:
```json
{
  "name": "parksy-election-mcp",
  "location": "OrbitPrompt/api/election_mcp.py",
  "tools": 7,
  "status": "active"
}
```

---

## 10. 최종 포지셔닝

| 포지션 | 본질 | 여부 |
|--------|------|------|
| 정치 무당 | "기운이 와" | ❌ |
| 정치 전사 | "내가 해석한다" | ❌ |
| **정치 엔지니어** | **"모델이 계산한다"** | **✅ 여기** |

이 프로젝트의 목표는 "누가 더 예측을 잘 맞히느냐"가 아니다.  
**"누가 더 검증 가능한 방식으로 예측하느냐"** 에 있다.  
모델과 가중치를 공개하고, 누구나 포크해서 자기 버전을 만들 수 있는 구조.

---

*끝. v2.0 통합본: DeepSeek Aider(운영형) + Claude Code(검증형) 병합.*  
*다음: Phase 1 실행 — OrbitPrompt/prompts/election/ + api/election_mcp.py*
