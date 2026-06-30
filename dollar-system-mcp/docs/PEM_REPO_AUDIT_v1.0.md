# PEM 증빙 역산 리포트 — 28개 레포 4사분면 매핑

### Parksy Economic Matrix (PEM) vs dtslib1979 28개 레포 실증 분석
### 2026.06.30 | 작성: Claude (dtslib1979/dollar-system-mcp 기준)

---

## 0. 서론 — 이 리포트의 목적

PEM 2x2는 **위에서 내려온 이론이 아니라, 이미 만들어놓은 레포에서 아래서 위로 올라온 모델**이다. 이 리포트는 각 사분면에 매핑되는 실제 레포지토리를 나열하고, 그 레포의 운영 데이터가 어떤 경제학 모델로 역산 가능한지를 증빙한다.

---

## 1. PEM 매트릭스 기준

```
                    │  거시(Macro)          │  미시(Micro)
────────────────────┼───────────────────────┼───────────────────────
물성(Physical)      │  Q1: 환율/화폐        │  Q3: 소호스튜디오
                    │  국가단위 화폐가치     │  1~3인 물리공간/노동
────────────────────┼───────────────────────┼───────────────────────
온라인(Digital)     │  Q2: 플랫폼           │  Q4: 임률/AI대체
                    │  글로벌 디지털 시장    │  직무단위 노동가격
```

---

## 2. Q1 — 물성×거시 (환율) ✅ 이미 완료

### 매핑 레포 (1개)
| 레포 | 내용 | PEM 근거 |
|------|------|----------|
| `dollar-system-mcp` | FX Engine v3.3 | 국가단위 화폐가치 기울기 측정 도구 |

### 증빙 데이터
- `mcp/data/signal_log.json`: 3개 시그널 (won_overvaluation, gold_discount)
- `mcp/modules/gate0.py`: 5단계 데이터 검증 (Benford, Regime Change, Issuer Incentive 등)
- `mcp/modules/hegemonic_fee.py`: 헤게모니수수료 = 누적약세율
- yfinance 실시간 데이터 연동 (USDKRW=1546, USDJPY=162, USDTWD=32)
- docs/ 4개 백서 (CAPITALISM_AS_OS, PEM, FX_WHITEPAPER, 100서)

### 역산 가능한 모델
- 헤게모니수수료율: 명목흑자 대비 실질수취 격차율 ← **이미 코드로 완성**
- GATE 0 신뢰도 가중치: 출처→Benford→체제변화→인센티브→합의도 5단계

---

## 3. Q2 — 온라인×거시 (플랫폼) 🔄 10개 레포 운용중

### 매핑 레포 (10개)
| 레포 | 내용 | PEM 근거 |
|------|------|----------|
| `parksy.kr` | 디지털 지식 아카이브 | 개인 미디어 플랫폼 |
| `dtslib.kr` | 경제방송 허브 | 독립 경제방송 플랫폼 |
| `eae.kr` | PWA Books | 온라인 출판 플랫폼 |
| `eae-univ` | 온라인 학습 플랫폼 | 교육 플랫폼 |
| `parksy-audio` | 오디오/나레이션/음악 엔진 | 콘텐츠 생산 플랫폼 |
| `parksy-image` | 이미지/비디오 시드 | 비주얼 콘텐츠 엔진 |
| `gohsy-production` | 3-Lane 방송 프로토콜 | 방송 플랫폼 |
| `koosy` / `artrew` | 편집방송/연예정보 | 편집방송 플랫폼 |
| `espiritu-tango` | 콘텐츠 방송 아키텍처 | 방송 인프라 |
| `gohsy-fashion` | 디지털 스튜디오 | 디지털 패션 플랫폼 |
| `dtslib-cloud-appstore` | 앱 배포 | 앱 유통 플랫폼 |

### 증빙 데이터
- **parksy-audio**: parksy-voice MCP (TTS, RVC, DiffSinger), parksy-music MCP (MIDI→BGM)
- **parksy-image**: webpage MCP (28레포 페이지 자동 생성), parksy-distributor MCP (YouTube/Telegram/Tistory/Naver)
- **gohsy-production**: `parksy-actor` 브라우저 시연 녹화 도구
- YouTube 8개 채널 운영 데이터
- Telegram 28채널 webhook 송출 인프라

### 역산 가능한 모델 (가설)
```
플랫폼_헤게모니수수료 = 콘텐츠_조회수 - 실제_정산액
     (= 유튜브/텔레그램/네이버가 가져가는 플랫폼 수수료율)

증빙 소스: parksy-distributor의 YouTube 업로드 기록, Telegram 송출 통계
필요: 정산 데이터 연동 (아직 안 되어 있음)
```

---

## 4. Q3 — 물성×미시 (소호스튜디오) 🔄 7개 레포 운용중

### 매핑 레포 (7개)
| 레포 | 내용 | PEM 근거 |
|------|------|----------|
| `obokzip` | 물리 스튜디오 · 어른 동아리방 | FLD Pilot 001, 1인 공간 |
| `buddies.kr` | 로컬 소매/유통 | 물리 퍼스트 소매 지점 |
| `namoneygoal` | 지역 부동산/사업 길드 | 길드 단위 지역 경제 실험 |
| `hoyadang.com` | 식당 프로토콜 | 물성 외식 공간 |
| `alexandria-sanctuary` | 팔공산 영적 커뮤니티 | 물리 커뮤니티 공간 |
| `phoneparis` | 모바일 소매 | 모바일 폰 물리 유통 |
| `gohsy` | 본진 | 물성화 브랜드 |

### 증빙 데이터
- **namoneygoal**: 부동산/사업 길드 — "길드 프랜차이즈" + "매력 자본"
  - 인류 측정 데이터 (길드원 모집/운영 로그)
- **buddies.kr**: 로컬 유통 시도
- **hoyadang.com**: 식당 운영 레포 (espiritu-tango 포크)
- **obokzip**: 물리 스튜디오 구축 계획 (FLD Pilot)

### 역산 가능한 모델 (가설)
```
소호_임대료_헤게모니수수료 = 공방_매출 - (임대료 + 장비감가상각 + 관리비)
     (= 물리공간이 가져가는 고정비 부담률)

매력_자본_계수 = 길드_모집_응답률 / (마케팅비 + 시간비용)
     (= 인류를 '측정'한 데이터)
```

---

## 5. Q4 — 온라인×미시 (임률/AI대체분) 🔄 5개 레포 운용중

### 매핑 레포 (5개)
| 레포 | 내용 | PEM 근거 |
|------|------|----------|
| `OrbitPrompt` | 프롬프트 생성 엔진 | AI 프롬프트 = AI 노동의 청사진 |
| `buckleychang.com` | CPA, AI 경제 인터페이스 | 회계사의 AI 시대 적응 |
| `papafly` | 인큐베이션 | 신규 사업 발굴 |
| `dtslib-apk-lab` | APK 실험실 | 모바일 앱 노동 |
| `dtslib-branch` | 브랜치/모델 | 보일러플레이트 + 모델 |

### 증빙 데이터
- **OrbitPrompt**: 7개 Generator (Chalkboard, PWA, Dataset, Identity 등)
  - 프롬프트 → 결과물 변환 실제 로그
  - 세션별 토큰 소모량 (자동 측정 가능)
- **buckleychang.com**: CPA 웹사이트 (AI 경제 컨설팅)

### 역산 가능한 모델 (가설)
```
AI_노동_단가 = 발생한_토큰비용 / 생성된_결과물_수
     (= "AI한테 일 시키는데 시간당 얼마 드냐")

실제 측정 가능:
  Claude Code 세션 1회 → 약 100K~200K 토큰
  → USD로 환산 시 시간당 AI 노동비용 계산 가능
  → 이게 인간 노동(박씨 원래 직무: 원가회계)과의 스프레드

임률_헤게모니수수료 = 생산성증가율 - 실질임금증가율
  (= AI가 생산성을 올려도 내 임금은 그만큼 안 오른다는 격차)
```

---

## 6. 인프라/공통 — 매트릭스 밖 (5개 레포)

| 레포 | 내용 |
|------|------|
| `dtslib-papyrus` | 디지털 명함 = 모든 레포의 관문 |
| `termux-bridge` | PC↔Termux 연결 도구 |
| `dtslib-localpc` | 로컬 실행 노드 |
| `parksy-logs` | 대화 저장/RAG |
| `parksy-image` (시드) | 이미지 에셋 저장소 |

---

## 7. 종합 — PEM은 이론이 아니라 실천의 지도다

| 사분면 | 레포수 | 완성도 | 역산 모델 |
|--------|--------|--------|----------|
| Q1(환율) | 1 | ⬛ 코드 완성 | 헤게모니수수료율 ✅ |
| Q2(플랫폼) | 10 | 🟩 데이터 있음 | 플랫폼 헤게모니수수료 가설 |
| Q3(소호) | 7 | 🟨 시드/운영중 | 매력자본계수 + 소호임대료 가설 |
| Q4(임률) | 5 | 🟧 OrbitPrompt 작동중 | AI 노동단가 + 임률 헤게모니 가설 |

박씨는 지금껏 **경제학 프레임을 몸으로 실험하고 있었다. 레포지토리가 그 증빙이다.**

다음 단계: Q4(임률)을 OrbitPrompt의 실제 세션 데이터(토큰소모량 ÷ 결과물수)로 역산해서 "AI 노동 단가 = X USD/시간"을 확정짓는 것.
