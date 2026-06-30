# PEM MCP 사용자 매뉴얼 — 박씨 전용
### parksy-economy-fx v3.4 | 26개 툴 | 4사분면

---

## 이 매뉴얼의 목적

**박씨가 Claude Code에 "야" 한마디만 하면, MCP가 알아서 긁고 계산하고 해석해서 텔레그램으로 보내주는 게 최종 목표다.** 그런데 지금은 일단 박씨가 뭘 할 수 있는지를 알아야 써먹는다. 여기 다 적었다.

---

## Ⅰ. 퀵스타트 — 가장 자주 쓸 6개 툴

### ① 매일 아침 1방: fx_snapshot
```
→ Q1(환율) KRW/JPY/TWD 전체 현황
→ GATE 0 검증 + 헤게모니수수료율 한 번에
→ yfinance 실시간 반영
```

### ② AI 일 시키는데 얼마 드냐: ai_labor_rate
```
→ OrbitPrompt 세션 1회 150K 토큰 → 약 $5.25/세션
→ 시간당 $7.0 (Claude Opus 기준)
→ 안 물어보면 안 알려줌 — 물어볼 때만 계산
```

### ③ AI vs 인간: ai_vs_human
```
→ AI $7.0/h vs 인간 원가회계사 $28/h
→ AI가 75% 저렴 — 단, 단순대체비용 관점. 품질/신뢰도 차이는 미포함
```

### ④ 유튜브 수수료: platform_fee
```
→ 조회수 1000회 가치 $10 → 실제 정산 $1.2 → 수수료율 88%
→ "시가만 있고 아직 수익이 안 나서" = 정산 0에 수렴하는 이유 증명
```

### ⑤ 조작 의심: view_anomaly_check
```
→ 일별 조회수 넣으면 Benford 검증 → 봇트래픽 의심도
→ 경고만 하고 판단은 보류 — 박씨 판단 영역
```

### ⑥ 공방 수수료: sonho_fee
```
→ 월매출 800만원 중 임대료 250만원 = 31% 고정비 부담
→ 장비감가 50만원 + 관리비 80만원 포함하면 43%
```

---

## Ⅱ. 전체 툴 목록 (26개)

### Q1 — FX/환율 (17개 툴)
| 툴명 | 뭐하는 놈 | 부르는 법 |
|------|-----------|----------|
| `analyze` | 원달러 4단계 위험분석 | `analyze(rate=1546)` |
| `structure` | 달러 시스템 역사비판 | `structure()` |
| `phi7` | 7축 철학 렌즈 | `phi7()` |
| `get_timeline` | 1944~2024 타임라인 | `get_timeline()` |
| `compare` | 두 환율 비교 | `compare(1200, 1546)` |
| `get_drivers` | 실시간 4개 지표 | `get_drivers()` |
| `forecast` | 선형회귀 예측 | `forecast(days=30)` |
| `dsi` | 달러 스트레스 지수 | `dsi()` |
| `meal_index` | "1달러 = 몇 끼" | `meal_index("서울","뉴욕")` |
| `gate0_check` | ⭐ 데이터 출처 검증 | `gate0_check(data_point_name, source_url, ...)` |
| `hegemonic_fee` | ⭐ 헤게모니수수료 | `hegemonic_fee("KRW")` |
| `dual_unit_reduce` | N통화→금/달러 환산 | `dual_unit_reduce(exposures)` |
| `signal_log` | 시그널 기록/조회 | `signal_log("stats")` |
| `fx_pipeline` | ⭐ 풀 파이프라인 | `fx_pipeline(currency="KRW")` |
| `fx_snapshot` | ⭐ 3개 통화 한방에 | `fx_snapshot()` |
| `compound_simulator` | 복리 시뮬레이터 | `compound_simulator(monthly=370)` |
| `compound_track2` | 원화 기준 복리 | `compound_track2(500000)` |

### Q4 — AI 노동단가 (3개 툴)
| 툴명 | 뭐하는 놈 | 부르는 법 |
|------|-----------|----------|
| `ai_labor_rate` | ⭐ AI 시간당 단가 | `ai_labor_rate(token_count=150000, usd_per_million_tokens=35)` |
| `ai_vs_human` | ⭐ AIvs인간 비교 | `ai_vs_human(ai_hourly_rate_usd=7.0, human_hourly_rate_usd=28)` |
| `labor_fee` | 임률 헤게모니수수료 | `labor_fee(productivity_growth_pct=3.5, real_wage_growth_pct=0.8)` |

### Q2 — 플랫폼 수수료 (3개 툴)
| 툴명 | 뭐하는 놈 | 부르는 법 |
|------|-----------|----------|
| `platform_fee` | ⭐ 유튜브/네이버 수수료율 | `platform_fee(gross_view_value_usd=1000, net_settlement_usd=120)` |
| `view_anomaly_check` | 조회수 봇의심 검증 | `view_anomaly_check([150, 23, 80, ...])` |
| `platform_reduce` | N개 플랫폼→1개 단위 | `platform_reduce([{platform, views, settlement_usd}])` |

### Q3 — 소호스튜디오 (2개 툴)
| 툴명 | 뭐하는 놈 | 부르는 법 |
|------|-----------|----------|
| `sonho_fee` | ⭐ 공방 고정비 부담률 | `sonho_fee(monthly_revenue=8000, rent=2500, depreciation=500, overhead=800)` |
| `attraction_capital` | ⭐ 매력자본계수 | `attraction_capital(guild_response_count=15, marketing_cost=50, time_cost_hours=10, hourly_rate_usd=15)` |

---

## Ⅲ. ⭐ 핵심 8개 툴 상세 — 박씨가 진짜 써먹는 툴

### 1. fx_snapshot — Q1 전체 현황

```
$ fx_snapshot()
→ KRW: 1546.30 | JPY: 162.20 | TWD: 31.91
→ GATE 0: PASS | 헤게모니수수료율: KRW 24.7% | JPY 26.7% | TWD 9.3%
→ 언제 부르나: 매일 아침 1방. "오늘 시장 어때?"
```

### 2. gate0_check — 데이터 검증

```
$ gate0_check(data_point_name="한국은행 2026Q2 경상수지", source_url="https://bok.or.kr/...")
→ gate_status: PASS / WARNING / BLOCK
→ confidence_score: 0.0~1.0
→ 5단계 상세: 출처계보 → Benford → 체제변화 → 발행기관인센티브 → 교차검증
→ 언제 부르나: 뉴스에서 "경상흑자 1600억불" 같은 숫자 나왔을 때
```

### 3. hegemonic_fee — 헤게모니수수료

```
$ hegemonic_fee("KRW")
→ 누적약세율 24.7% = Fed 금리인상 사이클 시작(2022H1) 이후 원화가 까인 비율
→ 명목흑자 1600억불 중 실질수취 1283억불
→ 언제 부르나: "요즘 원래 어땠냐" 궁금할 때
```

### 4. ai_labor_rate — AI 노동단가 (Q4)

```
$ ai_labor_rate(token_count=150000, usd_per_million_tokens=35.0, session_minutes=45, output_count=3)
→ 세션비용 $5.25 | 시간당 $7.0 | 결과물당 $1.75
→ source_tier=S급 (OrbitPrompt 실제로그)
→ 언제 부르나: "오늘 Claude한테 일 시킨거 얼마 나왔냐"
```

### 5. ai_vs_human — AI vs 인간 (Q4)

```
$ ai_vs_human(ai_hourly_rate_usd=7.0, human_hourly_rate_usd=28.0)
→ ratio 4:1 | AI가 75% 저렴
→ 단, "고객신뢰/재량판단/법적책임은 인간 전유물"
→ 언제 부르나: "AI한테 시키는 게 나은가 사람한테 시키는 게 나은가"
```

### 6. platform_fee — 플랫폼 수수료 (Q2)

```
$ platform_fee(gross_view_value_usd=1000, net_settlement_usd=120, platform_name="YouTube")
→ 수수료율 88% | 정산비율 12%
→ source_tier 기본값 S급
→ 언제 부르나: "유튜브가 얼마나 떼가냐"
```

### 7. sonho_fee — 소호 고정비 (Q3)

```
$ sonho_fee(monthly_revenue=8000000, rent=2500000, depreciation=500000, overhead=800000)
→ 고정비부담률 47.5% | 순수익률 52.5%
→ "공방 하나 해볼까" 할 때 대략적인 계산
→ 언제 부르나: "호야당 800만원 벌면 실제로 남는 게 얼마냐"
```

### 8. attraction_capital — 매력자본 (Q3)

```
$ attraction_capital(guild_response_count=15, marketing_cost=50000, time_cost_hours=10, hourly_rate_usd=15)
→ 매력자본계수 0.00015 (1원당 몇명 반응)
→ "길드 모집 공고 냈는데 반응이 없네 → 매력자본 부족"
→ ⚠️ 이거 정의 확정 후 바꾸지 마라 (시계열 단절)
```

---

## Ⅳ. 사용 패턴 5가지

### 패턴 1: "야 오늘 시장 어때?"
```
1. fx_snapshot() — Q1 전체
2. get_drivers() — 실시간 지표
→ 10초면 나옴
```

### 패턴 2: "요즘 AI 한테 일 시키는 게 나은가?"
```
1. ai_labor_rate(150000, 35.0, 45, 3) — Opus 세션 1회 비용
2. ai_vs_human(7.0, 28.0) — 인간 대비
3. labor_fee(3.5, 0.8) — 생산성 격차
→ 3개 툴 연속 호출
```

### 패턴 3: "유튜브 채널 평가해봐"
```
1. platform_fee(1000, 120, "YouTube") — 수수료율
2. view_anomaly_check(조회수_리스트) — 봇트래픽?
→ "지금은 시드단계" 결론 나오면 그게 정답
```

### 패턴 4: "이 데이터 믿을만한가?"
```
1. gate0_check("한국은행 2026Q2 경상수지", "https://bok.or.kr/...", [데이터들])
→ PASS/WARNING/BLOCK, 신뢰도 점수
```

### 패턴 5: "전체 상태 보고"
```
1. fx_snapshot() → Q1
2. ai_labor_rate() → Q4
3. platform_fee() → Q2
4. sonho_fee() → Q3
→ 4개 중 관심있는 거만 골라서 불러도 됨
```

---

## Ⅴ. 주의사항 — 이거 명심하고 써라

### 절대 금지
```
❌ 예측/추정 수치를 "확정"으로 말하지 마라 — 전부 "사후분석"
❌ Q2 vs Q3 vs Q4 우열비교 하지 마라 — 4사분면은 좌표일 뿐
❌ "매력자본계수" 정의 나중에 바꾸지 마라 — 과거 데이터랑 비교 불가능해짐
```

### 데이터 부족 현황 (박씨가 알아야 한계)
```
Q2: YouTube OAuth 미연동 — 정산액 = 0으로 나옴 (수익화 이전 = 정상)
Q3: namoneygoal/hoyadang 데이터 미연동 — 예시값으로만 작동
Q4: 실데이터 꽂으면 바로 작동 (가장 안정적)
```

### 판단은 박씨 몫
```
MCP는 계산만 한다. 
"AI가 더 싸니까 사람 때려쳐" 같은 판단은 박씨가 해야 됨.
MCP는 "75% 저렴합니다"까지만.
```

---

*작성일: 2026.06.30 | 버전: v1.0 | parksy-economy-fx v3.4.0 대응*
