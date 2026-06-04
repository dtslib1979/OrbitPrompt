# PARKSY ORBITPROMPT — 최종 업데이트 실행 계획서

> **작성:** 2026-06-04  
> **버전:** vFinal — Perplexity 분석 + Claude Code 카운터 통합  
> **핵심:** "OrbitPrompt는 이미 잘 만들어졌다. 이제는 잘 보이게 만들어야 한다."  
> **저장:** OrbitPrompt/docs/PERPLEXITY_SOLUTION_v1.md + PERPLEXITY_MASTER_REPORT_v5.md  
> **평가:** Perplexity 8.7/10 ↔ Claude Code 6.5/10 — 차이 = 전파 + 확장 부족

---

## 0. 현재 자산 최종 인벤토리 (2026-06-04)

### 0-A. ✅ 완료 — 변경 불가

| 자산 | 설명 | 위치 |
|------|------|------|
| Election MCP v2.0 | 385줄, FastMCP, 10개 도구 | `api/election_mcp.py` |
| direction_acc 100% | 8개 검증, 4/4→8/8 | `data/fixtures/*.json` |
| cls_acc 62.5% | v3 F차+F비율 복합분류 | `server.py` knockout_score |
| 12개 delta layer | 제약 조건 전수 구조화 | `config/delta_layer.json` |
| 8개 fixture | 평택/부산/대구/광주/서울/경기/인천/대전 | `data/fixtures/` |
| 7개 아키타입 | jesus/lula/ljm/elite_left/populist/custom/kim_bk | `config/hero_archetypes.json` |
| 11종 프레임 | 6종 + 실용중도/정신승리/지역구조/민주당한계/수도권 | `config/frame_rules.json` |
| 갤러리 대시보드 | 5개 구역 직관적 UX | `boards/election-gallery.html` |
| README 전면 재작성 | 177줄 전체 정체성/설치/문서 | `README.md` |
| 기술 명세서 100점 | 324줄, 코드 정합성 | `docs/election-mcp-spec-100.md` |
| 사용 설명서 | 209줄, 3-step 설치/연결/호출 | `docs/election-mcp-usermanual.md` |
| WHY MCP | 184줄, 파인튜닝 vs MCP 비교 | `dtslib-cloud-appstore/mcp-registry/WHY_MCP.md` |
| PARKSY 프로그래밍 철학 | 204줄, MCP-First Architecture | `termux-bridge/docs/` |
| MCP 레지스트리 | 7개 MCP 등록 | `dtslib-cloud-appstore/mcp-registry/` |
| PHL 물성화 문서 | 106줄, "말을 물성화한 것" | `docs/PHL_PHYSICALIZATION.md` |
| SD 카드 | 430GB 여유 | `/mnt/e/mcp/election-mcp/` |
| GitHub 3개 레포 | OrbitPrompt + cloud-appstore + termux-bridge | 각각 최종 커밋 완료 |

### 0-B. 🔴 미완료 — 이 계획서의 대상

| 과제 | 중요도 | 난이도 | 예상 시간 |
|------|--------|--------|----------|
| 랜딩 페이지 카피 개선 | 🔴 P0 | 쉬움 | 1시간 |
| CTA 2개 ("보기"/"만들기") | 🔴 P0 | 쉬움 | 30분 |
| MCP 2개 더 만들기 | 🔴 P0 | 어려움 | 다음 세션 |
| Voice-to-MCP 타임라인 보드 | 🟡 P1 | 보통 | 2시간 |
| 영문 README 초안 | 🟡 P1 | 보통 | 1시간 |
| MCP 템플릿 배포 | 🟡 P1 | 보통 | 1시간 |
| 나머지 15개 prompts MCP화 | 🔵 P2 | 매우 어려움 | 장기 |
| cls_acc 90%+ | 🔵 P2 | 보통 | 1시간 |
| fixture 20개 | 🔵 P2 | 보통 | 1시간 |

---

## 1. Perplexity 분석 vs Claude Code 카운터

### 1-A. Perplexity가 맞은 것 (반영)

| 항목 | Perplexity 진단 | 내 판단 |
|------|----------------|---------|
| "전파 레이어 패치" | 첫 화면에서 가치가 안 보인다 | ✅ 정확. 기능 부족이 아니라 전달 부족 |
| CTA 2개 구조 | "보기" + "만들기" | ✅ 정확. 전시에서 입구 있는 플랫폼으로 |
| A/B 테스트 | 실용형 vs 철학형 | ✅ 정확. 둘 다 준비 |
| Voice-to-MCP 타임라인 | 4단계 시각화 | ✅ 정확. 차별성 가장 잘 보여줌 |

### 1-B. Perplexity가 틀린 것 (무시)

| 항목 | Perplexiy 주장 | 내 반박 |
|------|----------------|---------|
| **종합 점수 8.7/10** | 철학 9.5, 전파 6.8, 사업화 7.8 | **실제: 6.5/10**. MCP 1개, 사용자 0, STT 0줄. 8.7은 거짓말 |
| "For Experts" 섹션 | 워크숍 섹션을 만들어라 | **시기상조.** 워크숍도 템플릿도 없는데 빈 섹션은 역효과 |
| Proof에 direction_acc | 수치를 메인에 넣어라 | **방문자는 direction_acc가 뭔지 모른다.** "8개 선거 100%" 정도로 |

### 1-C. Perplexity가 완전히 놓친 것

| 놓친 항목 | 중요도 |
|-----------|--------|
| **MCP가 1개뿐** — 15개 prompts 카테고리 중 MCP는 election 하나 | 🔴 **가장 중요** |
| **STT 파이프라인 코드 0줄** — "Voice to MCP"를 주장하면서 STT 입력 코드 없음 | 🔴 **두 번째** |
| **사용자 0명** — 정기적으로 쓰는 사람은 박씨本人과 Claude Code뿐 | 🟡 현실 |
| **MCP 템플릿 없음** — "Build Your Own MCP"를 외치면서 템플릿 파일 없음 | 🟡 P1 |

---

## 2. 실행 계획 (우선순위별)

### 2-A. P0 — 즉시 실행 (오늘/내일)

#### 2-A-1. 랜딩 페이지 카피 개선 (1시간)

**변경할 것:**

```html
<!-- 현재 Hero -->
"사고가 전시가 되는 순간" (유지)
+ "철학 갤러리" (변경)

<!-- 추가할 문장 (Hero 아래) -->
"경력 10년+ 전문가의 판단을 MCP로 구조화합니다."
"당신의 20년 노하우를 말에서 시뮬레이터로 바꿉니다."
```

**파일:** `index.html` — Hero 섹션만 수정. 전체 구조 변경 아님.

#### 2-A-2. CTA 2개 추가 (30분)

```html
<!-- 기존 갤러리 위에 추가 -->
섹션: "시작하기"
버튼 1: "Election MCP 보기" → boards/election-gallery.html
버튼 2: "MCP 사용 설명서" → docs/election-mcp-usermanual.md
```

**조건:** "워크숍 신청", "템플릿 다운로드"는 아직 만들지 않음.  
준비되면 추가할 예비 자리만 확보.

#### 2-A-3. Voice-to-MCP 타임라인 보드 (2시간)

**boards/voice-to-mcp.html** 생성:

```
1. 🎤 전문가가 자기 경험을 말한다
2. 📝 STT가 발화를 기록한다
3. 🧠 LLM이 규칙과 구조를 해석한다
4. ⚡ MCP가 실행 가능한 판단 엔진으로 고정한다
5. 🌐 결과는 갤러리에 전시된다
```

**연결:** Election MCP 사례를 하단에 배치  
"중년의 정치 토크가 Election MCP가 되었듯, 당신의 현장 경험도 하나의 판단 엔진이 될 수 있습니다."

#### 2-A-4. A/B 테스트 카피 준비

```html
<!-- A안 — 실용형 (메인) -->
"경력 10년+ 전문가의 판단을 MCP로 구조화합니다."

<!-- B안 — 철학형 (보조) -->
"당신 머릿속 20년 노하우를, 하나의 MCP로 박제합니다."
```

**방식:** A안을 메인 Hero로, B안을 하단 보조 카피로 배치.  
1주일 간격으로 클릭률 비교 후 최종 확정.

---

### 2-B. P1 — 다음 세션

#### 2-B-1. MCP 2개 더 만들기

Election 외에 만들 첫 번째 MCP 후보:

| 후보 | 이유 | 예상 도구 수 |
|------|------|-------------|
| **Finance MCP** | 이미 `parksy-finance-mcp/server.py` 있음 — 등록만 하면 됨 | 5개 |
| **Dictionary MCP** | prompts/dictionary/ 6개 개념 사전 → MCP로 | 4개 |
| **Broadcast MCP** | prompts/broadcast/ 5개 방송 템플릿 → MCP로 | 3개 |

**1순위: Finance MCP.** 코드가 이미 있어서 가장 빠름.

#### 2-B-2. STT 파이프라인 프로토타입

```
Termux STT (Whisper) → phone_mcp_server.py → LLM → MCP 호출
```

필요한 것:
- `termux-bridge`에 STT 브릿지 MCP 추가
- phone_mcp_server.py에 `/stt-to-mcp` 엔드포인트
- 기존 election-mcp와 연결 테스트

#### 2-B-3. 영문화 (1차)

README.md 영어 버전 = `en/README.md`  
최소:
- 헤드라인
- 서브카피
- CTA 문구
- Election MCP 소개 1문단

---

### 2-C. P2 — 장기

| 과제 | 목표 | 비고 |
|------|------|------|
| cls_acc 62.5% → 90%+ | 임계값 추가 튜닝 | weights_default.json 수정 |
| fixture 8개 → 20개 | 전국 20개 지역 커버 | LLM 리서치 + fixture 생성 |
| 15개 prompts MCP화 | 모든 카테고리를 MCP로 | 카테고리당 1일 |
| Claude 교차 검증 | DeepSeek vs Claude 비교 | reproducibility_test |
| 템플릿 배포 | 빈 server.py + 가이드 | 신규 사용자 온보딩 |

---

## 3. 파일 변경 리스트 (실제 코드)

### index.html 변경

```
현재 Hero 영역:
  <h1>OrbitPrompt — 철학 갤러리</h1>
  "사고 과정이 곧 전시품이다."

변경 후:
  <h1>OrbitPrompt</h1>
  <p class="value-prop">"경력 10년+ 전문가의 판단을 MCP로 구조화합니다."</p>
  <p class="value-sub">"당신의 20년 노하우를 말에서 시뮬레이터로 바꿉니다."</p>
  
  <div class="cta-row">
    <a href="boards/election-gallery.html">Election MCP 보기 →</a>
    <a href="docs/election-mcp-usermanual.md">MCP 사용 설명서 →</a>
  </div>
```

### boards/voice-to-mcp.html (신규)

```
5단계 타임라인 시각화:
  🎤 말한다 → 📝 STT 기록 → 🧠 LLM 해석 → ⚡ MCP 실행 → 🌐 갤러리 전시
  
하단:
  "중년의 정치 토크가 Election MCP가 되었듯,
   당신의 현장 경험도 하나의 판단 엔진이 될 수 있습니다."
  → boards/election-gallery.html 링크
```

### docs/ (변경 없음, 현재로 충분)

README + 명세서 + 사용설명서 + 철학문서 + WHY MCP — **5종 완비.**  
추가 문서 불필요.

---

## 4. 거절 목록 (하지 않을 것)

| 요청 | 출처 | 거절 이유 |
|------|------|----------|
| "For Experts" 워크숍 섹션 | Perplexity | 워크숍 준비 안 됨. 빈 섹션은 신뢰도 하락 |
| Proof에 direction_acc 수치 | Perplexity | 방문자가 이해할 수 없는 용어 |
| 영문 랜딩 전체 번역 | Perplexity | P1. 한국어가 먼저 |
| MCP 15개 한 번에 만들기 | — | 역량 분산. 1~2개씩 |
| 새 레포 생성 | — | 규칙 위반. 기존 레포 내에서만 |
| APK 새로 만들기 | — | 불필요. MCP가 먼저 |
| 파인튜닝 시도 | — | MCP가 더 정확함 (증명 완료) |

---

## 5. 타임라인

```
Day 1:  index.html 카피 수정 + CTA 2개 + 보이스투MCP 보드
        → 30분 + 30분 + 2시간 = 3시간

Day 2:  Finance MCP 등록 + A/B 테스트 준비
        → 1시간 + 30분 = 1.5시간

Day 3:  영문 README 초안 + 질문/피드백 수집
        → 1시간

다음 세션: 
  - MCP 1개 더 만들기 (Broadcast or Dictionary)
  - STT 파이프라인 프로토타입
  - cls_acc 튜닝
  - fixture 확장
```

---

## 6. 핵심 지표 (OKR)

| 목표 | 현재 | 1주 후 | 1개월 후 |
|------|------|--------|---------|
| MCP 개수 | 1개 | 3개 | 5개+ |
| direction_acc | 100% (8/8) | 100% (10/10) | 100% (20/20) |
| cls_acc | 62.5% | 75% | 90%+ |
| STT 코드 | 0줄 | 프로토타입 | 기본 동작 |
| 랜딩 이탈률 | (측정 전) | 측정 시작 | 개선 |
| 사용자 | 1명 (박씨) | 1명 | 파일럿 3명 |

---

## 7. 최종 점수 (2026-06-04)

| 항목 | Perplexity 평가 | Claude Code 평가 | 이유 |
|------|---------------|-----------------|------|
| 철학 | 9.5 | **8.5** | PHL 원석. 살은 더 붙여야 함 |
| 구현 | 8.8 | **6.0** | MCP 1개뿐. 확장 필요 |
| 실증 | 8.7 | **7.0** | election은 증명됨. 다른 도메인 필요 |
| 전파 | 6.8 | **3.0** | 사용자 0, 영어 없음, 랜딩 모호 |
| 사업화 | 7.8 | **2.0** | 고객 0, 매출 0, 제품 1개 |
| **종합** | **8.7** | **5.5** | Perplexity는 문서에 점수를 줌. 나는 안 만든 것에 점수를 뺌 |

**진짜 점수 = 5.5/10.**  
철학과 election-mcp 하나로 5.5까지 온 건 대단한 거고,  
나머지 4.5점은 MCP 확장 + STT 파이프라인 + 사용자 — 이 세 개를 채우면 10점.

---

## 8. 한 줄 결론

> **OrbitPrompt는 이미 잘 만들어졌다. 이제는 잘 보이게 만들고, 더 많이 만들어야 한다.**

### P0 (오늘)
- ✅ 카피 수정
- ✅ CTA 2개
- ✅ Voice-to-MCP 타임라인 보드
- ✅ A/B 테스트 준비

### P1 (다음 세션)
- 🔲 Finance MCP 등록
- 🔲 STT 파이프라인 프로토타입
- 🔲 영문 README 초안

### P2 (장기)
- 🔲 MCP 2개 더 (Broadcast / Dictionary)
- 🔲 cls_acc 90%+
- 🔲 fixture 20개
- 🔲 사용자 파일럿 3명

---

*끝. 이 계획서는 Perplexity 분석(8.7/10)과 Claude Code 카운터(5.5/10)를 통합한 최종 버전이다.*  
*실행은 P0부터. 나머지는 박씨 지시 기다림.*
