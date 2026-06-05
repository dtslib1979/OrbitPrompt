# OrbitPrompt 미디어 양산 플랜

> **확정일: 2026-06-05**  
> **채널: @philosopher-parksy (UCJaGuXjxoNjFMqfYUSFjZVg)**  
> **작업 드라이브: WD 패스포트 (D드라이브 `/mnt/d/PARKSY/philosopher-parksy/`)**

---

## 한 줄 정의

> OrbitPrompt에 쌓인 박씨의 대화·사유·이력을 재료로,  
> AI가 알아서 선별·제작·업로드하는 YouTube 양산 파이프라인.

---

## 작업 디렉토리 (WD 패스포트 고정)

```
/mnt/d/PARKSY/philosopher-parksy/
  ├── raw/        ← OrbitPrompt 로그 원본
  ├── scripts/    ← 선별·렌더·업로드 스크립트
  ├── tts/        ← 생성된 WAV (박씨 음성)
  ├── renders/    ← 완성 영상
  └── uploaded/   ← 업로드 완료 보관
```

C드라이브(86% 사용) 부하 방지 — TTS·영상 전량 D드라이브 생성.

---

## 파이프라인 3단계

### Stage 1 — 선별 (원료 추출)
```
OrbitPrompt/parksy-logs/*.md
OrbitPrompt/data/latest-messages.json
OrbitPrompt/prompts/** (MCP 이력 전체)
  ↓
LLM 선별 기준:
  - 통찰 밀도 높은 대화
  - 서사 완결된 흐름
  - 3분 이상 분량
  ↓
출력: 정제 텍스트 + 제목 + 설명문 + 태그
```

### Stage 2 — 제작 (공장)
```
정제 텍스트
  → parksy_writer.py 대본 다듬기
  → split_inference.py TTS (박씨 음성, GPT-SoVITS)
  → ffmpeg 영상 렌더링
      롱폼: 배경 이미지 + 자막, 5~15분
      쇼츠: 핵심 1줄 뽑아서 60초
```

### Stage 3 — 업로드 (배포)
```
완성 영상
  → YouTube Data API v3
  → @philosopher-parksy 채널
  → 제목·설명·태그 자동 생성
  → 업로드 완료 → uploaded/ 이동
```

---

## 스케줄

- 롱폼 1편 + 쇼츠 1편 / 일
- tmux 배치 세션 야간 자동 실행
- 신규 ParksyLog 생기면 자동 감지 → 파이프라인 투입
- YouTube API 쿼터: 60,000 units/day (충분)

---

## 착수 순서

| # | 작업 | 상태 |
|---|------|------|
| 1 | D드라이브 작업 디렉토리 생성 | ✅ 완료 |
| 2 | philosopher-parksy OAuth 토큰 발급 | ⏳ 박씨 PC 앞 확인 필요 |
| 3 | 선별 스크립트 작성 | ⏳ |
| 4 | TTS + ffmpeg 렌더러 연결 | ⏳ |
| 5 | YouTube 업로드 스크립트 연결 | ⏳ |
| 6 | tmux 크론 등록 (야간 자동) | ⏳ |

---

## 재료 현황

| 재료 | 위치 | 상태 |
|------|------|------|
| 대화 로그 | `OrbitPrompt/parksy-logs/` | ✅ |
| MCP 이력 | `OrbitPrompt/data/latest-messages.json` | ✅ |
| 철학·사유 콘텐츠 | `OrbitPrompt/prompts/` | ✅ |
| 박씨 TTS 음성 | `parksy-audio/scripts/split_inference.py` | ✅ |
| YouTube OAuth | `dtslib-papyrus/tools/youtube/yt_oauth_auto.cjs` | ✅ |
| YouTube API 쿼터 | dtslib1979 60,000 units/day | ✅ |
| 채널 타겟 | @philosopher-parksy | ✅ |
| 작업 드라이브 | WD 패스포트 D드라이브 | ✅ |
