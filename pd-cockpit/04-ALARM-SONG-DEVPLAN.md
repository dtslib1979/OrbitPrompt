# 알람 송 학습법 MCP — 개발 계획서 v2

> 갱신: 2026-06-06 (방향 전환 세션)
> PD: Claude (WSL 메인) + DeepSeek (phone_aider)
> 핵심 결정: 렌더링 머신 → **가창 머신**

---

## 한 줄 정의

> "외울 가치가 있는 문장을 무반주로 직접 불러서 몸에 남긴다"

---

## ── v1 이력 보존 ─────────────────────────────────────────────

> v1 방향: 텍스트 → MIDI + TTS 발화 → mp3 알람 (렌더링 머신)
> 전환 이유: TTS = 남의 목소리. AI 가창 = 전부 외계인. 박씨 직접이 답.

---

## 방향 전환 기록 (2026-06-06)

### parksy-audio 가창 실패 이력 전체

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

**결론**: AI 생성 가창은 전부 실패. 박씨 목소리만 살아남음.

### DiffSinger 실패 근본 원인

| 원인 | 내용 |
|------|------|
| 데이터 종류 | 발화 59분으로 가창 학습 → 외계인 (DiffSinger는 피치 레이블 필수) |
| 언어 | 영어 팝(singing_en_v5) → 한국어 불가 (CMU 영어 음소 체계) |
| 목소리 | parksy_ko_v1 = CSD Korean 한국 여성 성악가 → 박씨 목소리 아님 |

### 왜 모국어인가

박씨 자신의 리마인더 = 남 듣는 게 아님. 불편한 영어로 부를 이유 없음.
한국어 "언어는 도구가 아니라 환경이다"가 영어 어설프게 부른 것보다 뇌에 백배 박힌다.

---

## 코어 파이프라인 (확정)

```
텍스트 입력
  ↓
unit_split — 한국어 음절 카운터 + BPM/박자/호흡 가이드
  ↓
pattern_suggest — 그레고리안/불교/팝/단음 패턴 선택
  ↓
[선택] guide_vocal 플러그인 — "어떻게 불러야 할지 모를 때만"
  ↓
박씨 직접 무반주 가창 (termux-microphone-record 30초)
  ↓
trim_norm — silence remove + loudnorm -14 LUFS
  ↓
alarm_set — ~/storage/alarms/ 설치
  ↓
archive — 날짜/패턴/BPM 태깅 → parksy-logs/
```

---

## AI 코어 플러그인 구조 (선택, 코어 아님)

```
[플러그인 A] 가이드 보컬 (DeepSeek 발굴)
  OpenUtau CLI + Allen Crow v170 (한국어 완전 지원, 469MB, E드라이브)
  → pyworld F0/스펙트럼 추출
  → RVC parksy_rvc.pth 박씨 음색 변환
  = "박씨 목소리 비슷한 가이드" 10초 생성
  → 박씨가 듣고 따라 부름 → 코어 루프 복귀

[플러그인 B] STT 검증
  whisper-tiny ONNX + NNAPI (S25 Ultra Hexagon NPU 실측 확인)
  = 내가 뭐라고 불렀는지 텍스트 확인
  = 원문 80% 이상 일치 → 알람 등록

[플러그인 C] AI 가창 코어 (장기)
  Phase 1~3 직접 가창 아카이브 축적
  → 한국어 가창 DiffSinger 재학습 데이터가 됨
  → Phase 4에서 박씨 한국어 AI 가창 코어 완성
```

---

## 가창 패턴 (확정)

| 패턴 | 음계 | BPM | 특징 |
|------|------|-----|------|
| gregorian | 도리언 6음계 | 50 | 엄숙, 경건 |
| buddhist | 황종 5음계 | 56 | 명상, 반복 |
| pop | C장조 도-미-솔 | 80 | 밝음, 기억 쉬움 |
| monotone | 단음 반복 | 60 | 음정 없음, 발음 집중 |

---

## 이번 세션 작업 이력 (2026-06-06)

### Claude (WSL 메인)

| 작업 | 결과 |
|------|------|
| alarm_phone.py 폰 네이티브 수정 | fluidsynth `-F` 플래그 버그 수정, edge-tts `--rate=-10%` 문법 수정 |
| alarm_final.py | GPT-SoVITS parksy_v2 음색 4종 렌더 (gregorian/buddhist/buddhist_flute/pop) |
| 4종 알람 TG 전송 | gregorian 572K / buddhist 323K / buddhist_flute 446K / pop 401K |
| WHITEPAPER_v6.md | 가창 머신 방향 확정 + 플러그인 구조 |
| chanting_mcp.py | 6개 도구 FastAPI MCP 작성 → 폰 업로드 |
| parksy-audio 실패 이력 파싱 | 6회 시도 전체 문서화 |
| 개발 계획서 TG 전송 | 성공 (plain text) |

### DeepSeek phone_aider

| 작업 | 결과 |
|------|------|
| 기존 자산 7개 발굴 | parksy_ko_v1.onnx(319MB) / DiffSingerMiniEngine / nsf_hifigan.onnx / Allen Crow v170 / WORLD / RVC / OpenUtau |
| NNAPI 실측 | `['NnapiExecutionProvider', 'XnnpackExecutionProvider', 'CPUExecutionProvider']` |
| OpenUtau 커뮤니티 리서치 | Allen Crow v170 한국어 지원, WSL CLI 헤드리스 가능 확인 |
| RVC 모델 상태 | parksy_rvc.pth 48kHz 300epoch 정상 |
| 100점 계획서 + TG 전송 | STT_verify + preview + 성공 기준 추가 |
| 가이드 보컬 플러그인 설계 | OpenUtau → WORLD → RVC 파이프라인 |

---

## 기존 자산 인벤토리

### 폰 (Termux)

| 자산 | 위치 | 상태 |
|------|------|------|
| alarm_phone.py | ~/alarm-song/engine/ | ✅ 폰 네이티브 |
| chanting_mcp.py | ~/alarm-song/server/ | ✅ 이번 세션 |
| fluidsynth / ffmpeg / sox | pkg | ✅ |
| termux-microphone-record | termux-api | ✅ |
| onnxruntime + NNAPI | pip | ✅ 실측 확인 |

### WSL

| 자산 | 위치 | 상태 |
|------|------|------|
| alarm_final.py | /mnt/d/PARKSY/alarm-song/engine/ | ✅ |
| parksy_v2 모델 | ~/parksy-audio/voice_models/matched_v2/ | ✅ |
| GPT-SoVITS api_v2.py | ~/GPT-SoVITS/ | ✅ |
| parksy_rvc.pth | ~/rvc_models/parksy_rvc/ | ✅ 300epoch |
| OpenUtau | ~/openutau-linux/ | ✅ CLI 가능 |
| Allen Crow v170 | E드라이브 | ✅ 한국어 지원 |
| WORLD (pyworld) | pip | ✅ |
| parksy_ko_v1.onnx | ~/DiffSinger/parksy_onnx/ | ⚠️ CSD Korean (박씨 목소리 아님) |
| nsf_hifigan.onnx | ~/DiffSingerMiniEngine/assets/vocoder/ | ✅ |

---

## Phase 계획 (v2)

### Phase 1 — 3일 (코어)

```
unit_split    한국어 음절 카운터 + BPM 계산
record        termux-microphone-record 30초
trim_norm     sox silence remove + ffmpeg loudnorm -14 LUFS
alarm_set     ~/storage/alarms/ 복사
TG bot        텍스트 → 유닛 가이드 → 음성메시지 → 알람 설치
```

완료 기준: 텍스트 입력 → 30초 내 알람 설치

### Phase 2 — 1주 (MCP 서버)

```
FastAPI :7788 (chanting_mcp.py 기반)
6 tools: unit_split / pattern_suggest / record / trim_norm / alarm_set / archive
~/.claude.json MCP 등록
```

### Phase 3 — 2주 (STT + 플러그인 A)

```
whisper-tiny ONNX + NNAPI 벤치마크
STT 정확도 80% 미만 → 재녹음 유도
가이드 보컬: OpenUtau Allen Crow → WORLD → RVC 파이프라인 테스트
```

### Phase 4 — 장기 (AI 코어)

```
Phase 1~3 박씨 한국어 가창 아카이브 → DiffSinger 재학습
= 박씨 목소리 + 피치 레이블 있는 한국어 가창 데이터 완성
= AI 가창 코어 플러그인 장착 가능
```

---

## 파일 위치

| 레포 | 위치 | 역할 |
|------|------|------|
| alarm-song (폰) | ~/alarm-song/ | 코어 엔진 + MCP 서버 |
| alarm-song (WSL) | /mnt/d/PARKSY/alarm-song/ | 백서 + WSL 엔진 |
| parksy-audio | ~/parksy-audio/ | 음성 모델 + TTS 래퍼 |
| OrbitPrompt | pd-cockpit/04-ALARM-SONG-DEVPLAN.md | 이 문서 |

---

*Built between shifts. 박씨가 노래한다. AI는 구조만 만든다.*
