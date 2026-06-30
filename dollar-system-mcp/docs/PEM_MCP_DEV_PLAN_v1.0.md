# PEM 기반 MCP 3종 개발 계획서
### Q2(플랫폼) / Q3(소호) / Q4(임률) — 바텀업 역산 → 코드
### 2026.06.30 | PEM v2.0 기반

---

## 개요: 개발 원칙

PEM v2.0의 바텀업 접근법에 따라, 각 MCP는 **이론 먼저 → 코드 나중이 아니라, 기존 레포 데이터를 역산 → GATE 0/Module3/Module7 인터페이스 재정의 → 구현** 순서로 개발한다.

공통 모듈(GATE0/Module3/Module7)은 dollar-system-mcp에서 분리하지 않고, `입력 인터페이스만 교체`하는 방식으로 개발 — 백서 7.5절 loose coupling 원칙 준수.

---

## MCP #1: Q4 — labor-rate-mcp (임률, AI 대체분) — 1순위

### 데이터 증빙 (이미 존재)
- OrbitPrompt Generator 별 세션당 토큰소모량 (100K~200K/세션)
- Claude Code / DeepSeek 모델별 단가
- parksy-logs: 전체 대화 세션 로그

### 역산 모델
```
AI_노동_단가 = Σ(세션_토큰소모량 × 모델_토큰단가) / 생성된_결과물_수
             → "AI에게 일 시키는 시간당 단가" 실측값

GATE 0 전용: 기업·연구소의 "AI 생산성 보고서" 발행기관 인센티브 분석
Module 3 전용: 생산성증가율 vs 실질임금증가율 격차 → 노동_헤게모니수수료
Module 7 전용: N개 직무 → AI_복제비용_대비_스프레드 1개 유닛으로 환원
```

### 개발 단계
| 단계 | 내용 | 데이터/도구 |
|---|---|---|
| Step 1 | OrbitPrompt 세션 데이터 수집 파이프라인 | parksy-logs RAG |
| Step 2 | AI_노동_단가 실측 계산기 | 토큰소모량 × 단가 |
| Step 3 | GATE 0 인터페이스 전용 (AI 보고서 발행사 인센티브) | gate0.py |
| Step 4 | Module 3 전용 (임률 헤게모니수수료) | hegemonic_fee.py |
| Step 5 | MCP 툴 등록 + 전체 파이프라인 | server.py |

### 예상 소요
- 데이터 수집: 1세션 (기존 로그 접근)
- 구현: 2~3세션
- **총: 3~4세션**

---

## MCP #2: Q2 — platform-fee-mcp (플랫폼경제, 콘텐츠유통) — 2순위

### 데이터 증빙 (일부 존재, 일부 연동 필요)
- parksy-distributor 송출 기록 (Telegram 28채널, YouTube 8채널)
- YouTube Studio API (조회수, 정산액 — 연동 필요)
- Telegram bot 통계 (채널별 메시지 도달률)
- Tistory/Naver 송출 기록

### 역산 모델
```
플랫폼_헤게모니수수료 = 콘텐츠_조회수_가치 - 실제_정산액
                     → 플랫폼(유튜브/네이버/틱톡)이 가져가는 구조적 수수료율

GATE 0 전용: 
  - 플랫폼 알고리즘 변경 공지의 발표 타이밍/이해상충 검증
  - "조회수"라는 지표 자체의 Benford 검증 (봇 트래픽 탐지)
Module 3 전용: 조회수 대비 정산액 격차 → 헤게모니수수료율
Module 7 전용: N개 플랫폼 → "유효_조회당_단가" 1개 유닛으로 환원
```

### 필요한 추가 연동
- YouTube Data API v3 (OAuth) — 조회수/정산액 자동 수집
- Telegram bot API — 채널별 통계 로깅

### 개발 단계
| 단계 | 내용 | 데이터/도구 |
|---|---|---|
| Step 1 | parksy-distributor 송출 로그 수집 파이프라인 | 기존 DB/webhook 로그 |
| Step 2 | YouTube API 연동 (조회수/정산액) | YouTube Data API |
| Step 3 | GATE 0 전용 + Benford 검증 (조회수 봇트래픽) | gate0.py 전용 |
| Step 4 | Module 3 전용 (플랫폼 수수료율) | hegemonic_fee.py 전용 |
| Step 5 | MCP 툴 등록 | server.py |

### 예상 소요
- 데이터 파이프라인: 1세션
- YouTube API 연동: 1~2세션 (OAuth 처리)
- 구현: 3세션
- **총: 5~6세션**

---

## MCP #3: Q3 — sonho-mcp (소호스튜디오, 물성공간) — 3순위

### 데이터 증빙 (일부 존재)
- namoneygoal: 길드원 모집/운영 로그, 지역 부동산 실험 데이터
- hoyadang.com: 식당 운영 프로토콜 데이터
- buddies.kr: 로컬 유통 실험 데이터
- obokzip: 물리 스튜디오 기획 데이터

### 역산 모델
```
소호_임대료_헤게모니수수료 = 공방_매출 - (임대료 + 장비감가상각 + 관리비)
                         → 물리공간이 가져가는 고정비 부담률

매력_자본_계수 = 길드_모집_응답률 / (마케팅비 + 시간비용)
              → "인류를 측정했다"는 실측 계수

GATE 0 전용:
  - 국토부/통계청 부동산 통계 발표 인센티브 분석 (집값 통계 조작/발표시점)
  - 지역 상권 보고서 발행기관 이해상충 검증
Module 3 전용: 
  - 공방/소호 단위 매출 대비 고정비 부담 → 헤게모니수수료율
  - 매력자본계수 시계열 (길드 운영기간별 추이)
Module 7 전용: N개 공간/지역 → "소호_운영_효율" 1개 유닛으로 환원
```

### 개발 단계
| 단계 | 내용 | 데이터/도구 |
|---|---|---|
| Step 1 | namoneygoal/hoyadang 데이터 수집 | 레포 로그 |
| Step 2 | 매력자본계수 계산기 | 기초 통계 |
| Step 3 | GATE 0 전용 (부동산 통계 기관 인센티브) | gate0.py 전용 |
| Step 4 | Module 3 전용 (임대료/고정비 부담률) | hegemonic_fee.py 전용 |
| Step 5 | MCP 툴 등록 | server.py |

### 예상 소요
- 데이터 정리: 1~2세션
- 구현: 2~3세션
- **총: 3~5세션**

---

## 통합 개발 로드맵

| 순서 | MCP | 예상 세션 | 비고 |
|---|---|---|---|
| 1순위 | Q4 labor-rate-mcp | 3~4세션 | 데이터 가장 깨끗, 가장 빠름 |
| 2순위 | Q2 platform-fee-mcp | 5~6세션 | YouTube API 연동 필요 |
| 3순위 | Q3 sonho-mcp | 3~5세션 | 데이터 정리 선행 필요 |
| **합계** | **3개 MCP** | **11~15세션** | **공통모듈 재사용으로 단축 가능** |

### 위험 요소
- Q2: YouTube API OAuth 토큰 갱신 자동화 — 기존 yt_oauth_auto.cjs 활용 가능
- Q3: namoneygoal 로그 데이터의 정형화 정도 — 비정형 텍스트가 많을 경우 전처리 필요
- Q4: 모델별 토큰 단가 변동 (Claude/DeepSeek 정책 변경 시 재계산 필요)

### 아키텍처 결정사항 (추후 논의)
1. 3개 MCP를 각각 독립 서버로 띄울지, dollar-system-mcp에 통합할지
2. 공통 모듈(GATE0/Module3/Module7)을 pip 패키지로 분리할지
3. PEM 매트릭스 전체를 관장하는 orchestrator MCP가 필요한지
