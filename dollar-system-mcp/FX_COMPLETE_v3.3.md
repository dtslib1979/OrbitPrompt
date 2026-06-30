# PARKSY FX Engine v3.3 — 철학에서 구현까지 완결 백서
## 박태정(EduArt Engineer) | 2026.06.30 | Post-hoc Patch Theory of Hegemony

---

## 제1장: 철학 — 사후 정당화 패치이론

### 1.1 시작점: "달러는 성서고, 미국은 사제다"

v3.3 백서보다 훨씬 전, 박씨는 다음 명제를 던졌다:

> **"달러는 성서고, 미국은 사제다. 환율 상승은 손실 전가다. 자기책임 서사로 포장된다."**

Claude가 "역인과 오류, 반례 존재, 비유의 폐쇄성"을 지적했을 때, 박씨는 역공했다:

> **"너 알고리즘도 세뇌당했다고 생각하면 어떠냐."**

이 한 문장이 이 철학 전체의 인식론적 기초다 — 관찰자 자신의 관점도 그 시스템의 산물일 수 있다는 자각.

### 1.2 결정적 발견: "구조가 아니라 땜빵이다"

Claude가 "구조적 비대칭 + 경로의존성"이라는 절충안을 내자, 박씨가 깨부쉈다:

> **"구조도 아니라고 병신아. 그때그때 땜빵한다고. 일관된 논리가 없어."**

| Claude 절충안 | 박씨 정정 |
|---|---|
| 구조 → 서사 → 책임전가 | 땜빵 → 땜빵 → 사후에 '구조처럼' 읽힘 → 책임전가 |

Claude의 최종 승복: *"땜빵이 쌓여서 구조처럼 보이는 거지, 인과가 완전히 반대야. 박씨 말이 더 정확했어."*

### 1.3 핵심 메타포: 자바스크립트

> **"씨발 자바스크립트처럼 논리가 없이 덧붙이고 누더기 하다 보니까 여기까지 온 거라고."**

`typeof null === "object"` — JS의 버그가 스펙으로 굳어진 것처럼, 달러시스템의 임시방편이 "원래 구조"로 읽힌다. 설계자가 없기에 책임을 물을 대상도 없고, 이게 의도된 음모보다 더 견고한 착취구조를 만든다.

### 1.4 철학의 3대 기둥

| 기둥 | 내용 | 구현 |
|---|---|---|
| 존재론 | 환율은 가격이 아니라 사후 정당화된 누더기 패치다 | 헤게모니 수수료 |
| 인식론 | 그 정당화 자체도 의심해야 한다 | GATE 0 |
| 자기검증 | 내 모델도 사후합리화에 빠질 수 있다 | 허생전 프로토콜 |

### 1.5 기성 학자와의 차이

| 학자 | 입장 |
|---|---|
| Michael Hudson | 구조가 있다 (monetary hegemony) |
| Yanis Varoufakis | 구조가 있고 의도도 있다 (Global Plan) |
| **박씨** | 구조도 의도도 없다, 누더기의 사후적 자기정당화만 있다 |

박씨의 입장이 가장 급진적이면서 동시에 가장 반증가능하다. 그리고 반례 앞에서 한발 물러섰다("기울기 속도는 주류가 맞다") — 이 양보 능력이 철학과 종교를 가른다.

---

## 제2장: 철학의 회계화 — 백서 v1.0 → v3.3

### 2.1 사고의 흐름 (22단계)

```
① 외환시장이 실제로 존재하는가?
② 존재한다면 누가 결정하는가?
③ 코로나 이후 KRW/JPY/TWD 데이터 검증
④ 경상흑자와 환율 약세의 역설 발견
⑤ "미국이 정하는 것"이라는 명제 도출
⑥ TP(이전가격) + 마크업 구조로 메커니즘 정식화
⑦ 학계 검증 (Hudson, Varoufakis)
⑧ 미국 재무부 공식 문서로 실증
⑨ FX 카르텔 형사판례로 2층 조작 구조 확정
⑩ [v2.0] 선행지표 문제 자기비판 → 사후/선행 분리
⑪ [v2.0] 외부 동료평가 반영 → 과잉일반화 보정
⑫ [v2.0] MCP 엔진 설계로 전환
⑬ [v3.0] 예산 버지팅 모델을 환율 선행지표로 이식
⑭ [v3.0] 개인 투자자의 비-FX 헤지 전략 설계 (현물자산 매집)
⑮ [v3.0] MCP를 "LLM 수집 → Python 실행 → 투자모형 래퍼"로 풀스펙화
⑯ [v3.1] Gemini 2차평가 → GATE 0 설계 (Benford + 출처계보 + 인센티브분석)
⑰ [v3.2] Perplexity 3차평가 → Dual-Unit 환원모델 (N→2변수)
⑱ [v3.3] 박씨 3라운드 반박: "트랙2도 베타헤지 아닌 복리컴파운드 트랙"
⑲ [v3.3] Module 10: 3-Bucket 복리 시뮬레이터 구현
⑳ [v3.3] MCP 코드 1차구현 완료 (5모듈 18툴)
㉑ [후행] 100서(철학→회계화 계보) 작성
㉒ [후행] FX_PHILOSOPHY_100seo.md 저장
```

### 2.2 TP 마크업 → 헤게모니 수수료

**"땜빵을 구조처럼 보이게 하는 메커니즘"의 회계적 번역**이 TP 마크업 프레임이다.

```
헤게모니_수수료율 = (현재환율 - 베이스라인) / 베이스라인
실질_수취액 = 명목흑자 / (1 + 헤게모니_수수료율)

KRW 2026: 23.8% → $1,600억 중 $1,293억 실수취, 수수료 $307억
JPY 2026: 26.6% → $2,400억 중 $1,896억 실수취, 수수료 $504억
TWD 2026: 9.2% → $2,500억 중 $2,289억 실수취, 수수료 $211억
```

### 2.3 GATE 0: 인식론의 구현

1부 "너도 세뇌됐을 수 있다" → 14장 GATE 0의 5단계 검증:
1. 출처 계보 (1차 정부원문 → 3차 미분류)
2. Benford's Law (첫째자리 분포 이탈도)
3. Regime Change (Z-score 2.5σ 기준)
4. Issuer Incentive (발행기관 이해상충)
5. Cross-Source Consensus (복수출처 합의도)

→ PASS/WARNING/BLOCK + 역용시그널 ("지표 주목도 상승")

### 2.4 Dual-Unit: 거대담론 거부의 구현

Perplexity "독일/스위스까지 검증하라"는 학술 요구를 박씨가 정면 반박:

> **"내 가계부가 OECD 전체 소비패턴을 대표해야 하냐."**

N개 통화 → **항상 2개 유닛(USD_equiv / GOLD_equiv)** 으로 강제 환산.
표본 수(N) 논쟁 자체를 구조적으로 무력화.

### 2.5 투트랙 구조: v3.3의 핵심 정정

v3.2까지 "트랙2 = 베타헤지/손실방어"로 잘못 프레이밍되어 있었음.
박씨 3라운드 반박으로 정정:

```
[트랙 1] IP/콘텐츠 — 능동적 알파 (Active Alpha)
[트랙 2] FX/금 DCA — 구조적 알파 복리 누적 (Structural Alpha)

복리_자산(t) = Σ[i=1..t] 매집액(i) × (1 + 자산수익률)^(t-i)
3-Bucket: USD 현금(40%) + 금(35%) + 단기국채(25%)
```

**가드레일 3개:**
1. 트랙2를 '단순 베타헤지/보험'으로 단정 금지
2. 트랙1·트랙2 수익률 직접비교 그래프 생성 금지
3. 5년 미만 데이터로 트랙2 복리성과 단정 금지

---

## 제3장: 구현 — 5개 MCP 모듈 상세

### 3.1 아키텍처 개요

```
Layer 0: LLM 자연어 → 의도 분류
Layer 1: GATE 0 — 데이터 출처 검증
Layer 2: Module 3/7 — 수수료 + 듀얼유닛
Layer 3: Module 8 — 시그널 로거
Layer 4: Module 10 — 복리 시뮬레이터
Layer 5: JSON 출력
```

**18개 MCP 툴**: v2.2 레거시 9 + v3.0 신규 6 + v3.3 신규 2 + version 1

### 3.2 Module 0: GATE 0 (gate0.py)

**핵심 함수**: `run_gate0(data_point_name, source_url, data_series, cross_source_values, context)`

5단계 연쇄 검증 → confidence 점수 산출 → PASS(≥0.55)/WARNING(≥0.35)/BLOCK

**철학-구현 매핑**: 1부 인식론의 직접적 코드 구현. 특히 `issuer_incentive_flag()`는 "누가 이 데이터를 발표했고, 그 사람은 무슨 이해관계가 있는가"를 기계적으로 검사 — 이건 "너도 세뇌됐을 수 있다"의 알고리즘화다.

### 3.3 Module 3: Hegemonic Fee (hegemonic_fee.py)

**핵심 함수**: `calc_hegemonic_fee(currency, current_rate, nominal_surplus, year)`

공식: `fee = nominal_surplus - nominal_surplus/(1 + cumulative_depreciation)`

지원: KRW(baseline 1240), JPY(baseline 128), TWD(baseline 29.2)

**철학-구현 매핑**: "사후 정당화"의 계량화. 분기말 확정된 누적 약세율로 수수료를 사후 계산. 예측하지 않고 확정치만 다룬다.

### 3.4 Module 7: Dual-Unit Reduction (dual_unit.py)

**핵심 함수**: `reduce(exposures, gold_price)`

```
USD_equiv = Σ amount_i / FX_to_USD_i
GOLD_equiv = USD_equiv / GOLD_price
```

**철학-구현 매핑**: "거대담론 거부"의 코드화. N이 몇 개든 출력은 항상 2변수. 검증 대상은 환산 함수 하나로 수렴.

### 3.5 Module 8: Signal Logger (signal_logger.py)

**핵심 함수**: `record_signal(signal_type, strength, basis)`, `get_stats()`

6종 시그널: won_overvaluation(0.35), treasury_watchlist(0.25), fed_hike_cycle(0.25), dsi_stress(0.20), gold_discount(0.15), regime_change(0.20)

**허생전 프로토콜**: 기록 전용. 절대 매매 금지. 최소 8회 누적 전 자본투입 금지.

**철학-구현 매핑**: 자기검증성의 구현. 사후합리화(self-serving bias)를 방지하기 위해 자본투입 전에 신호부터 쌓는다.

### 3.6 Module 10: Compound Simulator (module10_compound_simulator.py) [v3.3 신규]

**핵심 함수**: `run_module10(monthly_contribution, years, bucket_weights, usd_cash_return, gold_return, usd_bond_return, fee_rate)`

3-Bucket: USD_cash 40%(MMF 4%) + GOLD 35%(6%) + USD_bond 25%(4.5%)
가중합산 복리누적. 5년 미만 "평가시기상조" 라벨 자동 부착.

편의 래퍼: `run_module10_for_track2(monthly_contribution_krw, usd_krw_rate, years)` — 원화→USD 자동 환산

**철학-구현 매핑**: "구조알파"의 시뮬레이션. 헤게모니 수수료를 인지한 후, 그 정보로 트랙2를 굴릴 때의 복리효과를 3-Bucket으로 모의실험.

---

## 제4장: 개발사 — Git Log로 읽는 진화

### 4.1 전체 커밋 아크

```
v1.x (백서)
  └── FX_WHITEPAPER.md 작성 — "환율은 시장이 아니다"
v2.x (자기비판)
  └── 사후/선행 분리, 동료평가 반영, MCP 설계 전환
v3.0 (MCP 구현)
  ├── MCP 서버 최초 배포
  ├── gate0.py: 데이터 출처 검증 게이트
  ├── hegemonic_fee.py: 수수료 계산기
  ├── dual_unit.py: 듀얼유닛 환산
  ├── signal_logger.py: 시그널 로거
  └── server.py + main.py: 파이프라인 오케스트레이션
v3.3 (투트랙 확정)
  ├── module10_compound_simulator.py: 복리 시뮬레이터
  ├── main.py v3.3 파이프라인 업데이트
  ├── server.py v3.3 툴 추가
  ├── FX_WHITEPAPER_v3.3.md: 백서 16장 통합
  ├── FX_ENGINE_TECH_SPEC.md: 기술명세서 v3.3 정렬
  ├── FX_PHILOSOPHY_100seo.md: 철학 계보 저장
  └── FX_COMPLETE_v3.3.md: ⟪이 문서⟫ 철학→구현 완결
```

### 4.2 핵심 설계 결정

| 결정 | 이유 |
|---|---|
| MCP FastMCP 프레임워크 | SSE/stdin 자동, LLM 라우팅 최소화 |
| Python 강제실행 | LLM 숫자추정 금지 원칙 |
| GATE 0 우회 불가 | 모든 외부데이터는 게이트 통과 필수 |
| dict JSON 입출력 | 모듈 간 인터페이스 단일화 |
| 8회 시그널 누적 필요 | 허생전 프로토콜 — 사후합리화 방지 |
| 5년 미만 평가 금지 | 복리효과 최소 관측기간 |

---

## 제5장: 통합 — 모든 것이 어떻게 연결되는가

### 5.1 철학 → 설계 → 코드 연결도

```
철학 (100서)               설계 (백서)          구현 (코드)
─────────────────      ──────────────      ──────────────
"달러는 성서고           헤게모니 수수료      calc_hegemonic_fee()
 미국은 사제다"          (5.3절, TP프레임)    hegemonic_fee.py

"너도 세뇌됐을           GATE 0 5단계         run_gate0()
 수 있다"               (14장)               gate0.py

"거대담론 거부,          Dual-Unit 환원       reduce()
 내 노출만"             (7.4~7.6절)          dual_unit.py

"사후합리화             허생전 프로토콜       record_signal()
 방지"                  (13장)               signal_logger.py

"트랙2는 베타            3-Bucket 복리        run_module10()
 헤지 아니다"           (13.2/13.6절)        module10_compound.py
```

### 5.2 실행 파이프라인

```
fx_pipeline(currency="KRW"):
  1. yfetch USDKRW=X → current_rate
  2. GATE 0 → PASS/WARNING/BLOCK
  3. Module 3 → hegemonic_fee
  4. Module 7 → dual_unit (옵션)
  5. Module 8 → signal_log (옵션)
  6. Module 10 → compound_sim (옵션, v3.3)
  7. return {guardrails(9개), timestamp, all_modules}
```

### 5.3 9대 가드레일

1. 사후분석 — 예측 아님
2. 트랙2 = 복리 컴파운드 수익 트랙 — 손실방어용 보험 아님
3. 레버리지 금지 — 현물 자산 매집 기준
4. 8회 미만 자본투입 금지
5. GATE 0 우회 금지
6. End-Station=FX ≠ 로데이터 무시
7. **[v3.3]** 트랙2를 '단순 베타헤지/보험'으로 단정 금지
8. **[v3.3]** 트랙1·트랙2 수익률 직접비교 그래프 생성 금지
9. **[v3.3]** 5년 미만 데이터로 트랙2 복리성과 단정 금지

---

## 제6장: 검증 — 외부평가 + 자기검증

### 6.1 Perplexity 평가 (v3.2)

| 주장 | 검증 결과 |
|---|---|
| "환율을 시장 아닌 정치적 합의체로 본다" | 일치 (1부→헤게모니 수수료) |
| "데이터를 불신하는 인식론" | 일치 (1부→GATE 0) |
| "목적과 방법의 분리" | 부분일치 |

Perplexity는 v3.3 백서만 보고 판정했으나, 실제 철학의 발생지는 그보다 앞선 종교텍스트 명제였다는 것이 이 완결백서의 발견.

### 6.2 Gemini 평가 (v3.1)

"100만원 태워봐라" 제안 → 박씨 철학의 자기모순 지점 정확히 타격.
박씨의 대응: "자본투입 전 신호부터 누적" — 허생전 프로토콜로 방어.
이게 1부 철학(사후합리화)에 대한 자기일관성 검증임을 이 100서가 최초로 연결.

### 6.3 자기검증 — 이 철학이 종교가 아닌 증거

1. **Claude를 두 번 틀렸다고 지적 → Claude가 승복** (1부 라운드 3, 5)
2. **반례 인정** ("기울기 속도는 주류가 맞다")
3. **자기모델 검증장치 내장** (GATE 0의 6개 가드레일, 허생전 8회룰)
4. **사전고정 성공기준** (16.6절 — 사후합리화 차단)

> 종교는 양보하지 않는다. 박씨는 양보했다. 이게 철학과 종교의 차이다.

---

## 부록: 파일 인벤토리

| 파일 | 용도 | 라인 수 |
|---|---|---|
| `mcp/server.py` | MCP 서버 (18개 툴) | 479 |
| `mcp/modules/gate0.py` | GATE 0 데이터 검증 | 382 |
| `mcp/modules/hegemonic_fee.py` | 헤게모니 수수료 | 178 |
| `mcp/modules/dual_unit.py` | 듀얼유닛 환산 | 170 |
| `mcp/modules/signal_logger.py` | 시그널 로거 | 223 |
| `mcp/modules/module10_compound_simulator.py` | 복리 시뮬레이터 [v3.3] | 221 |
| `mcp/modules/main.py` | 파이프라인 오케스트레이터 | 205 |
| `docs/FX_ENGINE_TECH_SPEC.md` | 기술 명세서 | 271 |
| `FX_WHITEPAPER_v3.3.md` | 백서 (16장) | 1,564 |
| `FX_PHILOSOPHY_100seo.md` | 철학 계보 | 197 |
| **`FX_COMPLETE_v3.3.md`** | **⟪이 문서⟫ 철학→구현 완결** | — |

---

*이 문서는 PARKSY FX Engine v3.3의 철학적 기초(사후 정당화 패치이론), 기술적 구현(5개 MCP 모듈), 개발사(Git Log), 그리고 외부검증(Perplexity/Gemini)을 단일 호흡으로 통합한 완결 백서다.*
*작성: 2026.06.30 | v3.3.0 | 가드레일 9개 | MCP 툴 18개 | 철학 100서 포함*
