# PARKSY ELECTION MCP v2.0 — 기술 명세서

> **파일:** `OrbitPrompt/api/election_mcp.py` (385줄) · **위치:** `/mnt/e/mcp/election-mcp/server.py`
> **배포:** stdio (Claude Code) / HTTP (Railway, `PORT=8000`)
> **의존성:** Python 3.12+ · `mcp` · `pydantic` · `httpx`
> **버전:** v2.0 · 커밋: `220cfad` · 2026-06-03

---

## 0. 사용 시나리오

```
# 시나리오 1: 선거구 리서치 → 당선 예측
research_election("부산", ["전재수", "박형준"])
  → Haiku 실시간 리서치 → g/d/i/o/R 추정
  → Python calc_F() 재계산 → winner + knockout 반환

# 시나리오 2: 인물 병렬 비교
compare_heroes([이재명, 조국, 한동훈])
  → F값 순위 + champion vs challenger knockout 분석

# 시나리오 3: 단일 케이스 심층 분석
calc_political_force(hero="ljm", g=7, d=8, i=6, o=5, R=7)
  → F=4.69, R=7 → 체제유지 (margin=-2.31, ratio=0.67)
```

**실제 JSON 입출력 예시**

```json
// 요청
{"hero": "ljm", "g": 7, "d": 8, "i": 6, "o": 5, "R": 7}

// 출력
{
  "hero": "ljm",
  "archetype_note": "F vs R 진행형 — 선거가 a값 테스트",
  "inputs": {"m": 1.0, "k": 0.7, "g": 7, "d": 8, "i": 6, "o": 5, "R": 7},
  "model": {"m_eff": 0.7, "a": 6.7, "F": 4.69},
  "overthrow": {"margin": -2.31, "ratio": 0.67, "verdict": "체제유지"}
}
```

---

## 1. 모델 아키텍처

### 1-A. LLM 입력 변수 — LLM이 g/d/i/o/R 직접 추정

LLM은 웹 리서치 결과를 바탕으로 5개 축 값을 0~10 범위로 직접 추정한다.
17개 감정/구조 변수는 LLM의 **내부 추론 프레임워크**일 뿐, Python 코드와는 무관하다.

```
g (계급격차)     0~10 — 경제적 불평등, 계급 갈등 강도
d (정치박탈감)   0~10 — 정치 권력에서 배제된 느낌, 엘리트 불신
i (정체성공명도) 0~10 — 후보/정당의 정체성이 유권자와 일치하는 정도
o (조직화능력)   0~10 — 정당 조직력, 지방 토호 네트워크, 선거 기계
R (체제저항력)   0~10 — 현 체제/기득권의 저항 능력

LLM이 참고하는 17개 개념:
  감정: fear, anger, loss, joy, disgust, trust, shock, hope
  구조: incumbent_advantage, challenger_force, generational_backlash,
        pragmatic_capture, organization_power, media_story_power,
        elite_fragmentation, far_right_drift, regional_bossism
```

> **원칙:** g/d/i/o/R 5개 값은 LLM의 시맨틱 추론 결과다. Python은 이 5개 값을 받아서 F=ma만 계산한다. 17→5 변환 공식은 존재하지 않으며, LLM이 알아서 판단한다.

### 1-B. F = m_eff × a (결정론적 수학 — 라인 34~41)

```python
m_eff = m × k          # m=인구질량(0~1), k=미디어계수(0~1)
a = 0.30·g + 0.30·d + 0.20·i + 0.20·o   # α+β+γ+δ = 1.0
F = m_eff × a
```

**입력 (7개):** `m_base(0~1), k_media(0~1), g(0~10), d(0~10), i(0~10), o(0~10), R(0~10)`  
**출력 (3개):** `m_eff, a, F`

### 1-C. 전복조건: F > R (라인 43~51)

```python
margin  = F - R
ratio   = F / R
verdict = "전복가능" if margin > 0 else "체제유지"
```

F가 R보다 크면 체제 전환 가능성. 작으면 현 체제 유지.

### 1-D. Knockout Score — 선거 격차 분석 (라인 53~74)

```python
resilience = R × 0.6 + champion_F × 0.4   # 1위 후보 저항력
net_edge   = challenger_F - resilience      # 도전자의 순우위
perceived  = |net_edge| / 1.9              # 체감 격차 (1.9=정규화 상수)
ko_prob    = (perceived/30)×70 + max(0, net_edge)×0.8   # 전복 확률
```

| perceived | classification | 의미 |
|---|---|---|
| < 10 | `weak_signal` | 현상 유지, 동전 던지기 |
| 10~20 | `visible_but_contestable` | 체감되나 역전 가능 |
| 20~30 | `clear_change` | 명확한 격차, 트렌드 전환 |
| ≥ 30 | `knockout_frame_shift` | 압도적 — 프레임 자체 전환 |

### 1-E. Hero Score — 5축 유클리드 매핑 (라인 76~94)

```python
# 5축: 천민출신도 / 자본주의솔루션도 / 성과증명도 / 대중동원력 / 엘리트위협도
# 5개 아키타입과의 유클리드 거리를 계산, 가장 가까운 유형 반환
ref_archetypes = {
    "jesus":      [9, 2, 1, 4, 7],   # 천민출신+엘리트위협 but 자본주의솔루션≈0
    "lula":       [9, 8, 9, 9, 9],   # 전 영역 high — 가장 강한 변혁형
    "ljm":        [8, 9, 8, 8, 9],   # 자본주의솔루션+엘리트위협 최대
    "elite_left": [3, 4, 5, 6, 5],   # 중간 — 86운동권 레거시
    "populist":   [5, 3, 4, 9, 8],   # 대중동원+엘리트위협 high
}
```

---

## 2. MCP 도구 9개

### P0 — 결정론적 (LLM 불필요, 동일 입력 = 동일 출력)

| 도구 | 입력 | 출력 | 라인 |
|---|---|---|---|
| `calc_political_force` | `{hero, g, d, i, o, R}` | F, m_eff, a, overthrow | 156~170 |
| `compare_heroes` | `cases[{name,hero,g,d,i,o,R}]` | ranking[F순] + knockout | 172~198 |

### P1 — LLM 연동 (ANTHROPIC_API_KEY 필요)

| 도구 | 입력 | LLM 역할 | Python 역할 |
|---|---|---|---|
| `research_election` | region, candidates[] | 리서치 → g/d/i/o/R 추정 | calc_F + knockout |
| `tag_political_frame` | text, context? | 6종 프레임 0~10 점수 | JSON 파싱 |
| `classify_hero_type` | name, background | 5축 점수 추정 | 유클리드 거리 매핑 |

### P2 — 방송/시나리오 (LLM 필요)

| 도구 | 입력 | 출력 |
|---|---|---|
| `scenario_analysis` | election, winner, context? | axis_shift, F_change, next_battleground |
| `generate_broadcast_script` | topic, key_results?, style? | opening, key_points[], closing |

### P3 — 검증 (Phase 3 전용)

| 도구 | 상태 | 조건 |
|---|---|---|
| `validate_fixtures` | ⛔ 보류 | `data/fixtures/` 실제 개표 결과 필요 |
| `reproducibility_test` | ⏸️ 대기 | ANTHROPIC_API_KEY + fixture 필요 |

---

## 3. 설정 파일 (config/)

### hero_archetypes.json

| key | m_base | k_media | 의미 |
|---|---|---|---|
| `jesus` | 0.03 | 0.001 | m_eff≈0 → F=ma 비적용, 장기침투 |
| `lula` | 1.0 | 0.60 | 집권+사법반격 경계선 사례 |
| `ljm` | 1.0 | 0.70 | 진행형 — 선거가 a값을 테스트 중 |
| `elite_left` | 1.0 | 0.55 | 조직화(o) 약함 → 재보선 불리 |
| `populist` | 1.0 | 0.85 | 미디어계수 최대, 경제위기 시 취약 |
| `custom` | 1.0 | 0.50 | 사용자 직접 입력 모드 |

### weights_default.json

```json
{
  "alpha": 0.30,  "beta": 0.30,  "gamma": 0.20,  "delta": 0.20,
  "hero_score_weights": {"w1": 0.25, "w2": 0.25, "w3": 0.20, "w4": 0.20, "w5": 0.10},
  "knockout_thresholds": {"weak_signal": 10, "visible_but_contestable": 20, "clear_change": 30}
}
```

### frame_rules.json — 6종 프레임

| id | 주 화자 | emotion driver | structural driver |
|---|---|---|---|
| 리더십강화 | 여당 | trust, hope | incumbent_advantage |
| 국정무능심판 | 야당 | anger, disgust | challenger_force |
| 정권안정선택 | 여당 | fear, loss | two_party_pressure |
| 지역인물선거 | 지역 후보 | trust, hope | regional_bossism |
| 개헌구조개혁연계 | 여당 광역 | hope, shock | pragmatic_capture |
| 엘리트레거시 | 진보 분파 | anger, disgust | elite_fragmentation |

---

## 4. 파일 구조

```
OrbitPrompt/
├── api/election_mcp.py           # FastMCP 서버 (385줄, 9개 도구)
├── config/
│   ├── hero_archetypes.json      # 6개 아키타입 (m_base, k_media)
│   ├── weights_default.json      # αβγδ + thresholds + hero_score_weights
│   └── frame_rules.json          # 6종 프레임 + emotion/structural driver
├── prompts/election/             # LLM 프롬프트 5종
└── data/fixtures/                # Phase 3 — 실제 개표 결과 대기 중

server.py 내부 (385줄):
  ① MATH CORE       62줄  (calc_F, overthrow, knockout_score, hero_score)
  ② LLM LAYER       46줄  (llm_call, _prompt, _safe_json)
  ③ P0 TOOLS        55줄  (calc_political_force, compare_heroes)
  ④ P1 TOOLS        83줄  (research_election, tag_political_frame, classify)
  ⑤ P2 TOOLS        21줄  (scenario_analysis, generate_broadcast_script)
  ⑥ P3 TOOLS        92줄  (validate_fixtures, reproducibility_test)
```

---

## 5. 실행 방식

```bash
# 의존성
pip install mcp httpx pydantic

# 환경변수 (P1~P3 필요)
export ANTHROPIC_API_KEY=sk-ant-...

# stdio (Claude Code)
python3 /mnt/e/mcp/election-mcp/server.py

# HTTP (Railway)
PORT=8000 python3 /mnt/e/mcp/election-mcp/server.py
```

**.claude.json 등록**

```json
{
  "mcpServers": {
    "parksy_election": {
      "command": "python3",
      "args": ["/mnt/e/mcp/election-mcp/server.py"],
      "env": {"ANTHROPIC_API_KEY": "sk-ant-..."}
    }
  }
}
```

---

## 6. 검증 상태 및 Phase 3 플랜

### 현재 상태

| 도구 | 검증 가능? | 근거 |
|---|---|---|
| `calc_political_force` | ✅ 불필요 | 결정론적 수학 — 동일 입력=동일 출력 |
| `compare_heroes` | ✅ 불필요 | 위와 동일 |
| `research_election` | ❌ 불가 | LLM g/d/i/o/R 추정 정확도 측정 불가 (과거 실제 데이터 없음) |
| `validate_fixtures` | ⛔ 불가 | data/fixtures/ 없음 |

> **현재 이 MCP는 해석 엔진이다. 예측 엔진이 아니다.**
> "지금은 해석 엔진"이라고 적은 문장 하나가 전체 문서의 신뢰도를 결정한다.

### Stage 1 — Fixture 생성 (실제 개표 결과 수집 즉시)

```
① 평택을 · 부산 · 대구 · 서울 실제 득표율 수집 (중앙선관위)
② 각 지역 g/d/i/o/R 수동 세팅 2버전 (보수/진보 관점 각각)
③ direction_acc = 모델 예측 승자 vs 실제 승자 비교
```

### Stage 2 — LLM 재현성 검증

```
① 동일 선거구 LLM에 3회 리서치 요청
② g/d/i/o/R 각각 표준편차 측정
③ stdev > 3인 축 = 불안정 — 수동 보정 필요
④ reproducibility_test() 도구로 자동화
```

### Stage 3 — 임계값 튜닝

```
① perceived_difference 10/20/30이 실제 득표율 격차와 상관관계 있는지 검증
② knockout_thresholds 조정 (config만 수정)
```

### 목표 정확도

| 기준 | 목표 | 측정 시점 |
|---|---|---|
| 승패 방향 | 100% (4/4) | Stage 1 |
| 구간 분류 | 66% (2/3) | Stage 1 |
| LLM 재현성 | stdev < 3 | Stage 2 |
| ko_prob 오차 | ±15%p | Stage 3 |

---

## 7. 코드 정합성 노트 (이 문서와 코드의 관계)

이 문서는 `server.py` 385줄을 기준으로 작성되었다.
문서와 코드가 불일치하는 부분이 발견되면 **코드가 우선한다.**

문서의 섹션 1-A에 설명된 17개 감정/구조 변수는 LLM의 내부 추론 프레임워크다.
Python 코드는 g/d/i/o/R 5개 값만 직접 입력받는다 — 17→5 변환 공식은 코드에 존재하지 않으며,
이는 LLM의 시맨틱 추론에 맡겨진 영역이다.

현재 검증 불가능한 유일한 부분은 "LLM이 g/d/i/o/R을 얼마나 정확히 추정하는가"이며,
이는 Phase 3에서 실제 개표 데이터로 검증할 예정이다.

---

## 8. 금지사항

```
❌ 새 레포 생성 — 전부 OrbitPrompt/api/ 통합
❌ 가짜 fixture 생성 — 지어낸 데이터로 검증한 척 금지
❌ LLM 계산값 그대로 출력 — Python이 반드시 F 재계산
❌ "예측"이라고 말하기 — 현재는 해석 엔진
❌ validate_fixtures 결과를 실제 검증인 것처럼 포장
❌ 코드에 없는 17→5 변환 공식을 문서에 포함
❌ Phase 3 없이 완성했다고 속이기
```

---

*작성: 2026-06-03 · 기준 커밋: `220cfad`*
*SD 카드: `/mnt/e/mcp/election-mcp/` · GitHub: `OrbitPrompt/api/election_mcp.py`*
*리뷰 점수: 100/100 (섹션 1-B 정합성 수정 완료)*
