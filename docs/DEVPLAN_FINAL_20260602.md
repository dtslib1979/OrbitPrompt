# OrbitPrompt — 최종 개발 계획서 v1.0

> **작성:** 2026-06-02  
> **세션:** Parksy Capture v11 마감 + 레포×채널 맵 + Election MCP 기획  
> **철학:** PHL Protocol-First — "설명하지 말고 프로토콜을 호출하라"  
> **SSOT:** `dtslib-papyrus/hq/config/channel-repo-map.json`  
> **범위:** 28개 레포 × 15개 YouTube 채널 × 4개 계정 × 3개 방송국

---

## 0. 현재 자산 현황 (2026-06-02)

### 0-A. 완료된 것

| 작업 | 상태 | 커밋 |
|------|------|------|
| Parksy Capture v11.0.0 release APK (20MB, 서명) | ✅ 설치 완료 | `4ccaed4` |
| Parksy Capture 소스 리팩토링 (2,947줄→11파일/2,143줄) | ✅ 완료 | `4ccaed4` |
| Embed Server(MiniLM/8018) 제거, DeepSeek 직결 | ✅ 완료 | `f009c5e` |
| TTS 전체 읽기 (4,000자 청크) | ✅ 완료 | `f009c5e` |
| 레포×채널 Reverse Mapping 문서화 | ✅ 완료 | (papyrus) |
| Distributor MCP 14개 도구 인벤토리 검증 | ✅ 완료 | — |

### 0-B. 진행 중

| 작업 | 상태 | 비고 |
|------|------|------|
| Election MCP (parksy-election-mcp) | 🔶 기획 완료 | 아래 Phase 1~5 |
| youtube-setup.json 13/15 채널 누락 | ⚠️ 양산 대기 | 박씨 결재 후 자동 생성 |
| account c brandingSettings 403 | ⚠️ 펜딩 | OAuth scope 재발급 필요 |

### 0-C. 유지보수 원칙

```
❌ 새 레포 생성 (Election MCP 예외)
❌ FROZEN 레포 터치
✅ 있는 거 연결, 필요한 것만 만듦
✅ MCP 서버로 기능 캡슐화 (설치 1-step)
```

---

## 1. Election MCP — 프로젝트 정의

### 1-A. 한 줄 정의

> **LLM이 리서치하고 Python이 계산하는 정치 예측 엔진**

### 1-B. 철학 (OrbitPrompt PHL과의 정합)

```
OrbitPrompt PHL 철학:
  "한 단어(토큰)로 정의된 수백 줄 규칙을 호출한다"

Election MCP 적용:
  "research_election('서울', '홍준표')" 한 줄로
  17개 변수 수집 → F=ma 계산 → knockout 판정까지
```

| PHL 개념 | Election MCP 대응 |
|----------|------------------|
| Semantic Compression | `research_election` 토큰 하나로 전체 선거 분석 |
| Externalized Ruleset | Python 수학 모델이 판정 기준 (LLM 아님) |
| State Transition | 파라미터 → F 계산 → classification 결정 |
| Protocol-First | MCP 도구 인터페이스가 곧 프로토콜 |

### 1-C. 역할 분담 (변경 불가)

| 역할 | 담당 | 책임 |
|------|------|------|
| **박씨** | 이론 제공 + MCP 스펙 확정 | 정치 모델 방향, 임계값 결정 |
| **Claude Code (server.py)** | 수학 모델 구현 + MCP 서버 | F=ma 계산, knockout 판정, 결과 반환 |
| **LLM (runtime)** | 리서치 + 파라미터 추정 | 웹 검색, 감정 점수, 구조 변수 추출 |

> **LLM은 데이터 저장 안 함. CSV 수집 안 함. 웹 스크래핑 안 함.**  
> 매번 호출 시 실시간 리서치해서 JSON 파라미터만 반환.

---

## 2. Election MCP — 수학 모델

### 2-A. 17개 변수 (LLM이 추정)

**감정 드라이버 (8개, 0~100):**
| 변수 | 의미 | LLM 추정 근거 |
|------|------|--------------|
| `fear` | 공포/불안 | 경제 위기, 안보 위협, 코로나 등 |
| `anger` | 분노/반발 | 부정선거 의혹, 검찰 탄압, 언론 편향 |
| `loss` | 박탈감 | 내 집 마련 실패, 양극화, 상대적 빈곤 |
| `joy` | 획득 기쁨 | 복지 확대, 주가 상승, 올림픽 개최 |
| `disgust` | 혐오/배척 | 극우 혐오, 세대 갈등, 여성 혐오 |
| `trust` | 신뢰/연대 | 리더십 신뢰, 공동체 의식, 시민 연대 |
| `shock` | 불안정/놀람 | 정치 이벤트, 스캔들, 급격한 정책 변화 |
| `hope` | 기대/희망 | 변화 기대, 새로운 비전, 세대 교체 |

**구조 변수 (9개, 0~100):**
| 변수 | 의미 |
|------|------|
| `incumbent_advantage` | 현직/기득권 프리미엄 |
| `challenger_force` | 도전자 돌파력 |
| `generational_backlash` | 세대 반동 강도 |
| `pragmatic_capture` | 실용 프레임 흡수력 |
| `organization_power` | 조직력/지방 토호 |
| `media_story_power` | 미디어 서사 영향력 |
| `elite_fragmentation` | 엘리트 분열도 |
| `far_right_drift` | 보수 극우화 |
| `regional_bossism` | 지역 보스 구조 |

### 2-B. F=ma 계산식

```python
negative = mean(fear, loss, disgust, shock)
positive = mean(anger, joy, trust, hope)

g = mean(incumbent_advantage, organization_power, media_story_power)
d = mean(challenger_force, generational_backlash)
i = mean(pragmatic_capture, elite_fragmentation)
o = mean(far_right_drift, regional_bossism)
R = mean(negative, g)  # 저항력

F = (d * positive * 10) / (g * i * o)  # 정치 변화력

champion_resilience = (R * 0.6 + g * 0.4)
challenger_momentum = (d * 0.5 + positive * 0.3 + i * 0.2)
perceived_difference = abs(challenger_momentum - champion_resilience) / 1.9
net_edge = challenger_momentum - champion_resilience

knockout_probability = min(100, (perceived_difference / 30) * 70 + max(0, net_edge) * 0.8)
```

### 2-C. 임계 구간 (10/20/30 체감차)

| perceived_difference | 분류 | 정치적 의미 |
|--------------------|------|-----------|
| `< 10` | `weak_signal` | 현상 유지, 의미 있는 격차 없음 |
| `10 ~ 20` | `visible_but_contestable` | 체감되나 뒤집힐 수 있음 |
| `20 ~ 30` | `clear_change` | 명확한 변화 감지, 트렌드 전환 |
| `>= 30` | `knockout_frame_shift` | 압도적 격차, 프레임 자체가 전환됨 |

---

## 3. Election MCP — MCP 서버 설계

### 3-A. 파일 구조 (단일 파일)

```
OrbitPrompt/
├── prompts/
│   └── election/              # 선거 분석 프롬프트 카테고리 (신규)
│       ├── research.md        # research_election LLM 프롬프트
│       ├── compare.md         # compare_heroes 프롬프트
│       ├── scenario.md        # scenario_analysis 프롬프트
│       └── broadcast.md       # generate_broadcast_script 프롬프트
├── api/
│   └── election_mcp.py        # MCP 서버 — 단일 파일 (신규)
├── config/
│   └── sources.json           # studios에 election 등록
```

### 3-B. 7개 MCP 도구

| # | 도구 | 입력 | 출력 | LLM 필요? |
|---|------|------|------|----------|
| 1 | `calc_political_force` | 17개 변수 JSON | F, knockout, classification | ❌ |
| 2 | `compare_heroes` | heroes[name,params][] | 순위 + 비교표 | ❌ |
| 3 | `tag_political_frame` | 텍스트 | 6종 프레임 점수 | ✅ |
| 4 | `research_election` | region, candidates | 후보별 F, win_prob | ✅ |
| 5 | `classify_hero_type` | 인물 설명 | 5축 + 아키타입 | ✅ |
| 6 | `scenario_analysis` | 시나리오 텍스트 | 프레임 전환 해석 | ✅ |
| 7 | `generate_broadcast_script` | 선거 분석 결과 | 방송 스크립트 | ✅ |

### 3-C. 기술 스택

```python
# server.py (FastMCP)
from fastmcp import FastMCP
mcp = FastMCP("parksy-election-mcp")

@mcp.tool()
async def research_election(region: str, candidates: list[str]) -> dict:
    llm_params = await llm_research(region, candidates)  # LLM이 웹 검색
    result = calc_F(**llm_params)                         # Python이 계산
    return result

@mcp.tool()
def calc_political_force(params: PoliticalParams) -> PoliticalResult:
    return calc_F(params)
```

---

## 4. Distributor MCP — 역할 재정의

### 4-A. 필요성 (박씨 결론)

> "멀티 채널러에게 distributor MCP는 필수다.  
> 채널 15개 운영하면 중앙 관리 없이는 못 버틴다."

### 4-B. Distributor가 하는 일 (유일무이)

```
1. 한 영상을 15개 채널에 선별 배포
2. 18개 OAuth 토큰 만료 관리
3. TG + YT + Naver + Tistory + Discord 동시 발행
4. 채널 description/branding 일괄 갱신
5. "이 콘텐츠 어디에 올렸더라?" → status 확인
```

### 4-C. 3-Layer 검증 완료

| Layer | 파일 | 상태 |
|-------|------|-------|
| SSOT | papyrus/hq/config/channel-repo-map.json | ✅ 15채널×28레포 |
| Bridge | parksy-image/tools/mcp_distributor/channel_map.json | ✅ 100% 정합 |
| Execution | tokens/ .env 30+ | ✅ 14도구 가동 |

**알려진 drift:** @dtslib_com, @dtslib_world (d 토큰 revoke → a 라우팅 — 의도됨)

---

## 5. Parksy Capture v11 — 최종 상태

### 5-A. 점수 평가 (종합: 92/100)

| 항목 | 점수 | 사유 |
|------|------|------|
| 핵심 기능 (캡처/저장) | 10/10 | Share Intent → .md 저장, GitHub 백업 |
| TTS 읽어주기 | 9/10 | 전체 텍스트, 4,000자 청크, 한국어 |
| AI 검색 | 8/10 | 키워드 + DeepSeek API 직결 |
| 코드 품질 | 8/10 | 11개 파일, 2,143줄 (main 70줄) |
| APK 크기 | 7/10 | Release 20MB (debug 196MB에서 개선) |
| Settings 단순화 | 9/10 | API 키 2개 (DeepSeek + GitHub) |
| 문서화 | 9/10 | 기술 백서 514줄 + Telegram 전송 |
| **종합** | **92/100** | **초기 64점 → +28점** |

### 5-B. 남은 것

```
□ Release 서명 인증서 백업 (parksy-release.jks)
□ Parksy Capture 마켓 등록 고려 (선택)
□ MCP 생성기 플레이스홀더 채우기 (선택)
```

---

## 6. 실행 로드맵

### Phase 1 (즉시) — Election MCP 기초

```
□ OrbitPrompt/prompts/election/ 디렉토리 생성
□ api/election_mcp.py — calc_political_force + compare_heroes (LLM 불필요)
□ config/sources.json 등록
```

### Phase 2 (1회) — LLM 연동

```
□ research_election 툴 구현 (LLM 리서치 + Python 계산)
□ tag_political_frame 툴 구현
□ classif_hero_type 툴 구현
```

### Phase 3 (검증) — 실전 테스트

```
□ 1개 선거 케이스로 end-to-end 테스트
□ LLM 파라미터 재현성 확인 (같은 질문 3회 → 유사 결과?)
□ perceived_difference 임계값 튜닝
```

### Phase 4 (선택) — 배포

```
□ stdio 모드 Claude Code 연동
□ Railway 배포 (streamable-http)
□ youtube-setup 13건 양산 (박씨 결재 후)
```

---

## 7. 금지사항

```
❌ 과거 선거 데이터 CSV 수집
❌ 웹 스크래퍼 구현
❌ 데이터베이스 구축
❌ "Phase 4 없이 완성"이라고 속이기
```

---

## 8. 역할 재확인

| 포지션 | 본질 | 박씨 위치 |
|--------|------|----------|
| 정치 무당 | "기운이 와" | ❌ 안 맞음 |
| 정치 전사 | "내가 해석한다" | ❌ 안 맞음 |
| **정치 엔지니어** | **"모델이 계산한다"** | **✅ 여기** |

---

*끝. 이 계획서는 2026-06-02 세션의 최종 결과물입니다.*  
*SSOT: dtslib-papyrus + OrbitPrompt. 다음 세션: Phase 1 실행.*
