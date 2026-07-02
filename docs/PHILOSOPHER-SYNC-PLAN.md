# 철학자 박씨 — 전 플랫폼 싱크 개발 계획서

> **목표:** Discord × OrbitPrompt × GitHub Pages × YouTube 완전 동기화  
> **PD:** Claude Code | **승인:** 박씨 (Telegram) | **기한:** 단계별 1일~1주  
> **2026-07-02**

---

## 0. 현재 상태 (AS-IS)

| 플랫폼 | 상태 | 문제 |
|--------|------|------|
| **OrbitPrompt (index.html)** | ✅ MCP 갤러리 그래프뷰 | 철학 카운터 등 일부 MCP 미링크 |
| **philosopher-parksy (GitHub)** | ❌ 빈 레포 | 로컬 클론 안 됨, GitHub Pages 미설정 |
| **Discord** | ✅ 28채널 webhook | philosopher-parksy 전용 채널 없음 |
| **YouTube @philosopher-parksy** | ✅ 7개 플레이리스트 | Making Film 외 5개 비어있음 |
| **parksy-distributor MCP** | ✅ TG/YouTube/Discord 전부 연결 | 철학 전용 라우트 없음 |
| **철학 자동화 문서** | ✅ JUSTIFICATION-v2.md | 실행 파이프라인 코드화 필요 |

---

## 1. Phase 1: 인프라 정비 (오늘)

### 1.1 philosopher-parksy GitHub Pages 셋업

```bash
mkdir -p ~/philosopher-parksy
cd ~/philosopher-parksy && git init
# index.html = 철학자 박씨 포트폴리오/링크 페이지
# GitHub Pages 활성화 (gh repo edit --description "철학자 박씨 — MCP로 철학한다")
```

**파일 구조:**
```
philosopher-parksy/
├── index.html          ← 채널 포트폴리오 (플레이리스트 + MCP 링크)
├── CNAME               ← philosopher.parksy.io (선택)
├── CLAUDE.md           ← PD 운영 인스트럭션
├── README.md           ← 철학 자동화 선언문
└── justification/      ← JUSTIFICATION-v2.md 복사
```

**GitHub Pages URL:** `dtslib1979.github.io/philosopher-parksy`

### 1.2 Discord 채널 신설

| 채널명 | 용도 | webhook |
|--------|------|---------|
| `#philosopher-영상` | YouTube 업로드 알림 | `parksy_distribute_discord channel=philosopher-parksy` |
| `#philosopher-피드백` | 시청자 의견/토론 | 수동 |
| `#philosopher-작업일지` | Claude 작업 로그 자동 포스트 | `parksy_distribute_discord channel=philosopher-log` |

**webhooks.json 업데이트:** 28개 → 31개 (philosopher 3채널 추가)

### 1.3 parksy-distributor 철학 라우트 추가

```python
# 철학 라우트 (기존 publish 계열과 별도)
philosopher_publish:
  1. script_agent → 대본 생성
  2. synth_voice → TTS
  3. FFmpeg → MP4
  4. upload.cjs → YouTube (unlisted)
  5. parksy_distribute_discord (philosopher-영상) → 알림
  6. parksy_distribute_telegram → 박씨 승인
```

**MCP 명령어:** `parksy_distribute_all platform=["youtube","discord","telegram"] plan={episode_spec}`

---

## 2. Phase 2: OrbitPrompt ↔ philosopher-parksy 싱크 (1일)

### 2.1 index.html 노드 → philosopher-parksy GitHub Pages 연결

현재 index.html의 5개 허브 중 **철학 허브(purple)** 의 4개 리프:

| 현재 노드 | 변경 후 링크 |
|----------|-------------|
| WHY | → `philosopher-parksy/WHITEPAPER-FINAL.md` |
| 백서 | → `philosopher-parksy/docs/WHITEPAPER-FINAL-20260608.md` |
| 7축 | → `philosopher-parksy/justification/PHI7.md` |
| 휴머니티 | → `philosopher-parksy/justification/JUSTIFICATION-v2.md` |

**철학 카운터 MCP 노드 추가** (28개 → 32개):

| 노드 | 타입 | 허브 | 링크 |
|------|------|------|------|
| 철학카운터 | leaf | MCP 서버 | `philosopher-parksy/philosophy-counter/` |
| 라필로소피아 | leaf | 철학 | `philosopher-parksy/docs/PHI7-ECO-COUNTER-METHOD.md` |
| 변호문 | leaf | 철학 | `philosopher-parksy/justification/JUSTIFICATION-v2.md` |
| 채널소개 | leaf | 아카이브 | `philosopher-parksy/index.html` |

### 2.2 Playwright 검증 스크립트

```python
# verify_philosopher_sync.py
# 1. philosopher-parksy GitHub Pages 로드
# 2. 각 링크가 200 응답하는지 확인
# 3. OrbitPrompt index.html의 철학 노드와 philosopher-parksy 페이지 매칭 확인
# 4. Discord webhook 전송 테스트
```

---

## 3. Phase 3: YouTube 콘텐츠 자동화 파이프라인 (1~2일)

### 3.1 파이프라인 구조

```
트리거: 박씨 "에피소드 X 만들어"
  │
  ├── [박씨 몫] Making Film
  │     └── 화면 녹화 + 잡담 → raw MP4 → 업로드 (private)
  │
  └── [Claude 몫] 자동화 5트랙
        │
        ├── script_agent (대본)
        │     └── parksy_writer.py --engine claude-cli --format {type}
        │
        ├── synth_voice (TTS)
        │     └── parksy_synth_voice(voice_id, text, lang=ko)
        │
        ├── BGM (parksy-music)
        │     └── parksy_music_full(midi_path, style=warm)
        │
        ├── FFmpeg 영상 합성
        │     └── 슬라이드/자막/TTS/BGM → MP4
        │
        └── 배포
              ├── upload.cjs → YouTube (unlisted, 맞는 플레이리스트)
              ├── parksy_distribute_discord (#philosopher-영상)
              └── parksy_distribute_telegram (박씨 승인 요청)
```

### 3.2 5개 트랙별 대본 템플릿

| 트랙 | script_agent format | 길이 | 템플릿 |
|------|--------------------|------|--------|
| **La Filosofia** | "essay" | 5~8분 | "움베르토 에코의 {철학자}와 박씨의 Φ7 비교" |
| **MCP World** | "lecture" | 3~5분 | "{MCP명} 시연: server.py 실행부터 결과까지" |
| **Φ7 Counter** | "narration" | 3~7분 | "카운터 #{n}: {대상} — Claude가 분석한 결정적 차이" |
| **15-Second Philo** | "shorts" | 15~60초 | "{개념}: {압축문장}" |
| **Parksy Log** | "blog" | 2~5분 | "오늘의 커밋: {작업내용}" |

### 3.3 트리거 파일 시스템

```
~/philosopher-parksy/queue/
├── pending/          ← 대기 중인 에피소드
│   └── ep001.json   ← {type, source_doc, title, status}
├── in_progress/      ← 제작 중
└── done/             ← 완료

pending/ep001 예시:
{
  "type": "la_filosofia",
  "source": "PHI7-ECO-COUNTER-METHOD.md",
  "philosopher": "니체",
  "title": "니체와 박씨: 생철학의 엘리트 버전 vs 아웃라이어 버전",
  "status": "pending",
  "created": "2026-07-02"
}
```

---

## 4. Phase 4: Discord ↔ YouTube ↔ OrbitPrompt 3-way sync (2일)

### 4.1 sync 스크립트

```bash
# sync_philosopher.sh — 매시간 실행 (cron)
# 1. YouTube 채널 최근 영상 체크 (parksy_youtube_list_videos)
# 2. 새 영상 → Discord #philosopher-영상 자동 포스트
# 3. OrbitPrompt index.html 체크 (사이트 업데이트 확인)
# 4. philosopher-parksy GitHub Pages 체크
# 5. 차이 발견 → 텔레그램 보고
```

### 4.2 알림 체인

```
YouTube 업로드 (unlisted)
  → Discord #philosopher-영상: "📺 새 영상: {제목} (검수용)"
  → Telegram: "📺 승인 필요: {제목} /link"

박씨 OK
  → YouTube visibility → public
  → Discord #philosopher-영상: "✅ 공개: {제목}"
  → OrbitPrompt index.html 업데이트 (있으면)

Discord 피드백
  → 주간 리포트에 반영
  → 다음 콘텐츠 방향 참고
```

### 4.3 역할 분담 매트릭스 (최종)

| 역할 | 담당 | 작업 | 자동화 |
|------|------|------|--------|
| **철학자** | 박씨 | 말하기, 최종 승인, Making Film 녹화 | ❌ 수동 |
| **PD** | Claude (여기) | 대본 생성, MCP 구현, 영상 제작, 문서 정리 | ✅ 자동 |
| **감사관** | Claude (형) | 카운터, 품질 검증, 논리 검사 | ✅ 자동 |
| **실행자** | DeepSeek | TTS 렌더링, 배치 처리, 반복 작업 | ✅ 자동 |
| **알리미** | Discord | 업로드 알림, 피드백 수집, 커뮤니티 | ✅ webhook 자동 |
| **배포자** | YouTube | 콘텐츠 호스팅, 검색 노출, 시청자 접점 | ⚠️ 반자동 |

---

## 5. Phase 5: Playwright QA 파이프라인 (지속)

### 5.1 검증 스크립트 목록

| 스크립트 | 검증 대상 | 실행 시점 |
|----------|----------|----------|
| `verify_orbit_links.py` | index.html 내 모든 링크 200 확인 | 커밋 후 |
| `verify_philosopher_pages.py` | philosopher-parksy GitHub Pages 정상 렌더링 | 배포 후 |
| `verify_discord_webhook.py` | Discord webhook 정상 발송 | 설정 변경 후 |
| `verify_youtube_playlist.py` | 플레이리스트 구조 일치 확인 | 업로드 전 |
| `verify_full_sync.py` | 전체 4개 플랫폼 일관성 통합 체크 | 주 1회 |

### 5.2 Playwright 체크리스트

```
[ ] philosopher-parksy GitHub Pages 200 OK
[ ] OrbitPrompt 철학 노드 → philosopher-parksy 링크 정상
[ ] Discord webhook 메시지 형식 정상
[ ] YouTube 플레이리스트 6개 구조 일치
[ ] 각 MCP 페이지 실제 로딩 확인
```

---

## 6. 실행 순서 (우선순위)

| 순서 | 작업 | 예상 시간 | 완료 조건 |
|:----:|------|:---------:|-----------|
| **P0** | philosopher-parksy GitHub Pages 생성 + index.html | 30분 | `https://dtslib1979.github.io/philosopher-parksy` 접속 OK |
| **P0** | Discord 채널 3개 생성 + webhooks.json 업데이트 | 15분 | TG로 webhook 테스트 메시지 |
| **P0** | 기존 플레이리스트 정리 (Flyer/Making film) | 15분 | 플레이리스트 6개로 확정 |
| **P1** | index.html 철학 노드 링크 업데이트 | 30분 | 철학 허브 링크 전부 philosopher-parksy로 |
| **P1** | 첫 자동화 영상 제작 (15-Second Philosophy #1) | 1시간 | 대본→TTS→FFmpeg→업로드 완료 |
| **P2** | 큐 시스템 구축 (pending/in_progress/done) | 1시간 | `ep001.json` → YouTube 업로드 |
| **P2** | sync_philosopher.sh + cron | 30분 | 시간당 동기화 |
| **P3** | Playwright QA 전 스크립트 | 2시간 | verify_*.py 전부 통과 |
| **P3** | La Filosofia #1 (니체 카운터) 풀 제작 | 1.5시간 | 영상 업로드 + Discord 알림 완료 |

---

## 7. 예상 결과물

```
1주일 후 @philosopher-parksy 상태:

📺 플레이리스트 6개
  ├── Making Film        — 1~2개 (박씨 직접)
  ├── MCP World          — 1개 (Claude 자동)
  ├── La Filosofia       — 1개 (니체 카운터)
  ├── Φ7 Counter         — 1개 (카운터 #009)
  ├── 15-Second Philosophy — 3개 (자동 양산)
  └── Parksy Log         — 2개 (작업 일지)

🔗 연동
  ├── OrbitPrompt index.html 철학 허브
  ├── philosopher-parksy GitHub Pages
  ├── Discord 3채널
  └── Telegram 승인 파이프라인
```

---

*작성: Claude Code (PD) | 승인 대기: 박씨 | 2026-07-02*
