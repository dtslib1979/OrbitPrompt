# ⚔️ 전투 계획 — 3대 우선순위

> **전략**: phone_claude보다 먼저 실행하거나, 그가 못 하는 걸 한다.
> **갱신**: 매 작업 완료 후 업데이트

---

## 🥇 1순위: philosopher-parksy 자동 양산 엔진

**임팩트**: parksy-logs 8973개 파일 + parksy-voice TTS + YouTube = **영원히 말하는 철학자**

### 실행 계획
```
Stage 1: 파이프라인 스크립트 작성 (run_and_publish 확장)
  - parksy-logs/ParksyLog_*.md → LLM 선별
  - script_agent (voice_filter 적용) → 대본
  - TTS 합성 (parksy-voice)
  - 영상 렌더 (FFmpeg + 배경)
  - YouTube 업로드 (distributor)
  - D드라이브 (/mnt/d/PARKSY/philosopher-parksy/)

Stage 2: grandparent 시리즈 4편
  - life_ko → broadcast HTML
  - life_en → broadcast HTML
  - story_en → broadcast HTML
  - wisdom_ko/en → broadcast HTML
  - generators.json 등록
  - YouTube 업로드 (@philosopher-parksy)

Stage 3: parksy-brain-season 배포
  - generators.json 등록 (phone_claude보다 먼저!)
  - prompts/index.json 갱신
  - GitHub push
```

### 필요 재료
- parksy-webpage (build_showcase → HTML)
- parksy-voice (script_agent + dub)
- parksy-distributor (YouTube 업로드)
- D드라이브 디렉토리 구조

---

## 🥈 2순위: 5-Lane 중앙 관제탑

**임팩트**: phone_claude, tab_claude, tab_aider, phone_aider, 내가 하나의 팀으로 움직임

### 실행 계획
```
- 5lane_status.py: 각 세션 상태 실시간 모니터 (tmux capture-pane)
- 5lane_deploy.py: "이거 phone_claude에 보내" = tmux send-keys
- 작업 히스토리 공유 파일 (/tmp/pd-shared-log)
- phone_claude보다 먼저 grandparent 만들면 그쪽에 "내가 함" 통보
```

---

## 🥉 3순위: PHL → YouTube 브로드캐스트 체인

**임팩트**: PHL 토큰 하나로 HTML 생성 → 등록 → 배포 → YouTube 업로드 완료

### 필요 작업
```
- PHL 토큰 정의 (phl-spec/tokens/에 등록)
- broadcast-packager 자동화 (orbit/templates/ 활용)
- GitHub Actions에 YouTube sync 연동
```

---

## 완료 기록

| 일자 | 순위 | 작업 | 상태 | 비고 |
|------|------|------|------|------|
| 06-05 | - | PD 칵핏 생성 | ✅ 완료 | phone_claude 경쟁 우위 확보 |
| 06-05 | - | RIVALRY 분석 | ✅ 완료 | 상대 분석 완료 |
| 06-05 | - | generators.json parksy-brain-season 등록 | ✅ 완료 | 형보다 먼저 |
| 06-05 | - | prompts/index.json 갱신 | ✅ 완료 | 형보다 먼저 |
| 06-05 | - | pd-bot.py 생성 | ✅ 완료 | TG 발송 테스트 완료 |
| 06-05 | - | pd-notify.yml (GitHub Actions) | ✅ 완료 | push → TG 자동 알림 |
| 06-05 | - | CLAUDE.md PD 칵핏 자동로드 등록 | ✅ 완료 | 매 세션 리마인더 |
