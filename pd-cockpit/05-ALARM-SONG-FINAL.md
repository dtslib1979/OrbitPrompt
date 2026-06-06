# 가창 머신 MCP — 최종 개발 계획서

> 버전: v3.0 FINAL (2026-06-06)
> 작성: Claude PD + DeepSeek PD 합산
> 철학: "AI가 노래하지 않는다. 박씨가 노래한다. AI는 구조만 만든다."
> 전략: 지금 쌓는 무반주 가창 데이터가 나중에 오케스트라 뮤직의 소재가 된다.

---

## 한 줄 정의

외울 가치가 있는 문장을 무반주로 직접 불러서 몸에 남기고, 쌓인 가창 데이터로 나중에 진짜 음악을 만든다.

---

## 방향 전환 기록 — 왜 가창 머신인가

### parksy-audio 가창 실패 6회 이력

```
시도 1: SF2 풀 오케스트라 반주           → 기계음 (폐기)
시도 2: BBC SO + REAPER 렌더링           → -91dB 무음 (폐기)
시도 3: DiffSinger v1~v4 (발화 데이터)  → 외계인 소리 (폐기)
시도 4: DiffSinger 영어 팝 학습          → 한국어 불가 (폐기)
시도 5: parksy_ko_v1 (CSD Korean)       → 박씨 목소리 아님 (폐기)
시도 6: DDSP 바순                        → 데이터 부족 (중단)
────────────────────────────────────────────────────────────────
성공:   RVC 박씨 음색 변환               → 박씨 청취 OK ✅ (2026-05-12)
성공:   GPT-SoVITS parksy_v2            → 발화 본진 ✅ (TTS용)
```

### DiffSinger 실패 근본 원인

| 원인 | 내용 |
|------|------|
| 데이터 종류 | 발화 59분으로 가창 학습 — DiffSinger는 피치 레이블 필수 |
| 언어 | 영어 팝(singing_en_v5) → 한국어 불가, CMU 영어 음소 체계 |
| 목소리 | parksy_ko_v1 = CSD Korean 한국 여성 성악가, 박씨 목소리 아님 |

### 왜 모국어 한국어인가

박씨 자신의 리마인더 = 남이 듣는 게 아님. 불편한 영어로 부를 이유 없음.
한국어로 "언어는 도구가 아니라 환경이다"가 영어 어설프게 부른 것보다 뇌에 백배 박힌다.

---

## 코어 파이프라인 — 8단계

| 단계 | AI 필요? | 구현 | 상태 |
|------|---------|------|------|
| `unit_split` | ❌ | 한국어 음절 카운터 + BPM 계산 | chanting_mcp.py 완성 |
| `pattern_suggest` | ❌ | JSON 규칙 3종 (불교/그레고리안/팝/단음) | chanting_mcp.py 완성 |
| `preview` | ❌ | sox 1초 기준음 재생 (옵션) | Phase 1 |
| `record` | ❌ | termux-microphone-record 30초 | chanting_mcp.py 완성 |
| `trim_norm` | ❌ | sox silence remove + ffmpeg loudnorm -14 LUFS | chanting_mcp.py 완성 |
| `STT_verify` | **✅ 유일한 AI** | whisper-tiny ONNX + NNAPI | Phase 2~3 |
| `alarm_set` | ❌ | cp + am start 인텐트 | chanting_mcp.py 완성 |
| `archive` | ❌ | 날짜/패턴/BPM/STT점수 태깅 → parksy-logs/ | chanting_mcp.py 완성 |

**8단계 중 7단계 AI 불필요. STT_verify 하나만 AI.**

---

## 가창 패턴 4종 (확정)

| 패턴 | 음계 | BPM | 특징 |
|------|------|-----|------|
| gregorian | 도리언 6음계 | 50 | 엄숙, 경건 |
| buddhist | 황종 5음계 | 56 | 명상, 반복 |
| pop | C장조 도-미-솔 | 80 | 밝음, 기억 쉬움 |
| monotone | 단음 반복 | 60 | 음정 없음, 발음 집중 |

---

## 하드웨어 (실측 완료 — DeepSeek 확인)

| 항목 | 상태 |
|------|------|
| 기기 | SM-S938N (Galaxy S25 Ultra) |
| SoC | Snapdragon 8 Elite (sun) |
| NPU | Hexagon — `ort.get_available_providers()` 실측: `['NnapiExecutionProvider', 'XnnpackExecutionProvider', 'CPUExecutionProvider']` |
| 저장공간 | 92GB free (parksy_ko_v1.onnx 319MB 충분) |
| onnxruntime | 1.26.0 설치 완료 |

---

## AI 코어 플러그인 구조 (선택, 코어 아님)

```
[플러그인 A] 가이드 보컬 — "어떻게 불러야 할지 모를 때만"
  OpenUtau CLI + Allen Crow v170 (한국어 완전 지원, 469MB)
  → pyworld F0/스펙트럼 추출
  → RVC parksy_rvc.pth 박씨 음색 변환 (300epoch, 48kHz)
  = 박씨 목소리 비슷한 가이드 10초 → 박씨가 듣고 따라 부름

[플러그인 B] STT 검증 — Phase 2~3
  whisper-tiny ONNX + NNAPI
  = 내가 뭐라고 불렀는지 텍스트 확인
  = 원문 80% 이상 일치 → 알람 등록

[플러그인 C] AI 가창 코어 — 장기 (Phase 4+)
  Phase 1~3 박씨 직접 가창 아카이브 축적
  → 한국어 가창 DiffSinger 재학습 데이터 완성
  → 박씨 한국어 AI 가창 코어 플러그인 장착
```

---

## 데이터 축적 전략 — 지금이 미래의 재료

```
Phase 1-3: 무반주 가창 유닛 100개 쌓기
  각 유닛: 원문 텍스트 + BPM/패턴/강세 + STT 정확도 + 날짜
                 ↓
v2: 쌓인 데이터 → Allen Crow + RVC + WORLD
    → 박씨 목소리 가이드 보컬 자동 생성
                 ↓
v3: 가이드 보컬 + 오케스트라 반주 → DAW 편곡 → 완성된 음악
```

**지금 무반주로 부르는 게 나중에 오케스트라 뮤직 소재가 된다.**

---

## Phase 계획

### Phase 1 — 3일 (코어 완성)

```
unit_split + pattern_suggest + record + trim_norm + alarm_set + TG bot
```

완료 기준: 텍스트 입력 → 30초 내 알람 설치

현재 상태: `chanting_mcp.py` 작성 완료, 폰 업로드 완료

### Phase 2 — 1주 (MCP 서버)

```
FastAPI :7788 전체 가동
6 tools: coach / record / verify / alarm_set / list / archive
~/.claude.json MCP 등록 → Claude Code에서 직접 호출
```

### Phase 3 — 2주 (STT + 가이드 보컬)

```
whisper-tiny ONNX + NNAPI 벤치마크
STT 정확도 80% 미만 → 재녹음 유도 루프
플러그인 A 테스트: OpenUtau Allen Crow → WORLD → RVC
```

### Phase 4 — 장기 (AI 가창 코어)

```
Phase 1~3 박씨 가창 아카이브 → 한국어 DiffSinger 재학습
= 박씨 목소리 + 피치 레이블 있는 데이터 완성
= AI 가창 코어 플러그인 장착
```

---

## 성공 기준

| 시점 | 기준 |
|------|------|
| 3일차 | 텍스트 입력 → 30초 내 알람 설치 |
| 7일차 | MCP 6개 도구 폰에서 전부 동작 |
| 14일차 | whisper-tiny STT 정확도 80% 이상 |
| 30일차 | 10개 이상 유닛 실제 알람 사용 중 |
| v2 이후 | 쌓인 가창 데이터로 오케스트라 음악 제작 |

---

## 기존 자산 인벤토리 (Claude + DeepSeek 합산)

### 폰 (Termux)

| 자산 | 위치 | 상태 |
|------|------|------|
| alarm_phone.py | ~/alarm-song/engine/ | ✅ fluidsynth 반주 (옵션) |
| chanting_mcp.py | ~/alarm-song/server/ | ✅ 6개 도구 이번 세션 완성 |
| fluidsynth / ffmpeg / sox | pkg | ✅ |
| termux-microphone-record | termux-api | ✅ |
| onnxruntime 1.26.0 + NNAPI | pip | ✅ 실측 확인 |

### WSL

| 자산 | 위치 | 상태 |
|------|------|------|
| alarm_final.py | /mnt/d/PARKSY/alarm-song/engine/ | ✅ GPT-SoVITS 래퍼 |
| parksy_v2 모델 | ~/parksy-audio/voice_models/matched_v2/ | ✅ |
| parksy_rvc.pth | ~/rvc_models/parksy_rvc/ | ✅ 300epoch, 48kHz |
| OpenUtau | ~/openutau-linux/ | ✅ CLI 헤드리스 가능 |
| Allen Crow v170 | E:\parksy-data\openutau-singers\ | ✅ 한국어 완전 지원 |
| pyworld + resampy | rvc-venv | ✅ WORLD 보코더 |
| DiffSingerMiniEngine | ~/DiffSingerMiniEngine/ | ✅ HTTP 서버 포트 9266 |
| nsf_hifigan.onnx | MiniEngine/assets/vocoder/ | ✅ |
| parksy_ko_v1.onnx | ~/DiffSinger/parksy_onnx/ | ⚠️ CSD Korean (박씨 목소리 아님, 가이드 보컬용) |

---

## 파일 구조

```
/mnt/d/PARKSY/alarm-song/
├── WHITEPAPER_v6.md           ← 방향 전환 선언
├── DEVELOPMENT_PLAN.md        ← DeepSeek 계획서 원본
├── engine/
│   ├── alarm_phone.py         ← 폰 네이티브 (fluidsynth 반주)
│   └── alarm_final.py         ← WSL GPT-SoVITS 래퍼
├── server/
│   └── chanting_mcp.py        ← FastAPI MCP 6도구 (이번 세션)
└── templates/                 ← MIDI 템플릿 보관용

~/alarm-song/ (폰 Termux)
├── engine/alarm_phone.py
└── server/chanting_mcp.py

OrbitPrompt/pd-cockpit/
├── 04-ALARM-SONG-DEVPLAN.md   ← v2 세션 이력
└── 05-ALARM-SONG-FINAL.md     ← 본 문서 (최종본)
```

---

*Built between shifts. 박씨가 노래한다. AI는 구조만 만든다. 지금 쌓이는 게 나중의 재료다.*
