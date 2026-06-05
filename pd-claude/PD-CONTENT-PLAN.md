# OrbitPrompt PD 콘텐츠 개발 계획서
> Claude PD 전용 | 작성: 2026-06-05 | 파싱 기반: OrbitPrompt + 전 레포지토리

---

## 0. PD 운영 구조 (이 세션에서 확정)

```
박씨 = 데스크 (방향 + 결재)
Claude(나) = PD A (전략/구조/설계)
DeepSeek aider = PD B (반복/양산/패치)

프로세스: 제작보고서 → 박씨 OK → 실행
보고 채널: TG @parksy_bridge_bot → pd-bridge → 두 PD 동시 투입
```

**박씨 헌법**: 박씨는 말과 결재만. 실행은 전부 PD가 알아서.

---

## 1. 현재 자산 현황 (2026-06-05 파싱 기준)

### 즉시 방송 가능 HTML (10편)
| 파일 | 주제 | 언어 | 상태 |
|------|------|------|------|
| grandparent-life-ko.html | 70살에 알게 된 것 | KO | ✅ |
| grandparent-life-en.html | Things I Learned at 70 | EN | ✅ |
| grandparent-wisdom-ko.html | 눈치·정·한 — 한국 지혜 | KO | ✅ |
| grandparent-wisdom-en.html | Wisdom No Book Can Teach | EN | ✅ |
| parksy-brain-season.html | 뇌과학 시즌 | KO | ✅ |
| parksy-capture-tutorial.html | 캡처 튜토리얼 | KO | ✅ |
| math-tutor.html | 수학 과외 | KO | ✅ |
| memorial-tribute.html | 추모 칠판 | KO | ✅ |
| music-curation.html | 음악 큐레이션 | KO | ✅ |
| pwa-demo.html | PWA 앱 데모 | KO | ✅ |

### 원자재 있음 → HTML 미생성
| topics 파일 | 콘텐츠 | 우선순위 |
|-------------|--------|---------|
| grandparent/story_en.md | 이민·역사 서사 (영어) | 1순위 |
| grandparent/story_ko.md | (있으면) | 1순위 |
| math.json (8주제) | 수학 과외 시리즈 확장 | 2순위 |
| music.json (8아티스트) | 음악 분석 시리즈 | 2순위 |
| memorial.json (5시나리오) | 추모 칠판 시리즈 | 3순위 |

---

## 2. 콘텐츠 개발 계획

### Phase 1 — 즉시 (이번 주)

#### 1-1. grandparent 시리즈 확장 (심화편 4편)

박씨가 이 세션에서 제안한 각도들:

| 편 | 주제 | 각도 | 타깃 CPM |
|----|------|------|---------|
| 5편 | 노후 재무 | "70살에 주식 사야 하는 이유" | $15-25 |
| 6편 | 결혼 철학 | "50년 살아보니 결혼에서 진짜 중요한 것" | $8-18 |
| 7편 | 눈치 심화 | "외국인이 평생 못 배우는 한국인의 직관" | $10-20 |
| 8편 | 인생 책 제목 | "내 인생을 책으로 낸다면 제목은?" | $12-22 |

**생산 방식**: topics/ MD 파일 먼저 → broadcast HTML 생성

#### 1-2. generators.json + prompts/index.json 업데이트
- parksy-brain-season 등록 누락 → 즉시 수정
- grandparent 시리즈 인덱스 등록

---

### Phase 2 — 이번 달

#### 2-1. 주제별 시리즈화 (각 8편 목표)

**Track A: 할머니·할아버지 (Grandparent)** — 글로벌 CPM $8-25
```
완성: life-ko, life-en, wisdom-ko, wisdom-en (4편)
예정: story-en, finance, marriage, intuition, life-title (5편)
목표: 10편 풀 시즌
```

**Track B: 뇌과학 (Brain Science)** — 국내 CPM $3-8
```
완성: parksy-brain-season (1편)
예정: 뇌과학 2~8편 (수면/기억/집중/감정/창의/노화/습관)
목표: 8편 풀 시즌
```

**Track C: 수학 (Math Tutor)** — 교육 CPM $5-15
```
완성: math-tutor (1편)
재료: math.json 8주제 있음
목표: 8편 (주제별 1편씩)
```

**Track D: 음악 (Music Curation)** — 문화 CPM $4-10
```
완성: music-curation (1편)
재료: music.json 8아티스트 있음
목표: 8편 (아티스트별 1편씩)
```

**Track E: 추모 (Memorial)** — 감성 CPM $3-8
```
완성: memorial-tribute (1편)
재료: memorial.json 5시나리오 있음
목표: 5편
```

---

#### 2-2. 자동화 파이프라인 완성

**현재 가동 중인 파이프라인** (papyrus 레포 기반):
```
Perplexity 리서치 → article_writer.py → JSON 아티클
→ parksy_scm_mcp.run_and_publish() → 네이버/티스토리/TG 동시 배포
```

**추가 연결 필요**:
```
OrbitPrompt broadcast HTML 생성
→ parksy-audio TTS 나레이션 (박씨 음색)
→ FFmpeg 영상 합성
→ YouTube 자동 업로드 (tools/youtube/auth.cjs 완성 필요)
```

**YouTube OAuth 상태**: auth.cjs 있음, 업로드 스크립트 30% 완성 → 이달 안 완성 목표

---

### Phase 3 — 다음 달

#### 3-1. Generator 완성 (7개 PENDING → LIVE)

| Generator | 용도 | 우선순위 |
|-----------|------|---------|
| dataset | 파인튜닝 JSONL 생성 | 1 |
| studio | 썸네일/이미지 자동화 | 1 |
| apk | PWA 카드 생성 | 2 |
| identity | 자기 모델 7축 분석 | 2 |
| instruction | CLAUDE.md 자동화 | 3 |
| route | FAB 공정 설계 | 3 |
| form | 다국어 폼 생성 | 4 |

#### 3-2. 완전 자동화 체인

```
박씨 TG 한 마디
  ↓ pd-bridge.py
Claude PD + DeepSeek PD 동시 투입
  ↓ 각자 분업
콘텐츠 생산 (HTML + TTS + 영상)
  ↓ run_and_publish()
유튜브 + 블로그 + TG 동시 배포
  ↓
박씨한테 완료 보고
```

---

## 3. 채널별 배포 계획

### 현재 배포 가능한 채널
| 채널 | 도구 | 상태 |
|------|------|------|
| Telegram | pd-bot.py + publish_telegram() | ✅ 즉시 가능 |
| Discord | publish_discord() | ✅ 즉시 가능 |
| 네이버 블로그 | tools/naver/post.cjs | ✅ 즉시 가능 |
| 티스토리 | tools/tistory/post.py | ✅ 즉시 가능 |
| GitHub Pages | git push | ✅ 즉시 가능 |
| YouTube | tools/youtube/auth.cjs | 🔶 OAuth 완성 필요 |

### 15채널 배포 목표 (1달 내)
- 채널별 주제 매핑 (channel-repo-map.json 기반)
- 주 3편 업로드 자동화
- 썸네일 자동 생성 (studio generator)

---

## 4. PD 작업 우선순위 (다음 세션)

### 1순위 — 즉시 실행
- [ ] grandparent story-en.html 생성 (재료 있음)
- [ ] generators.json parksy-brain-season 등록
- [ ] prompts/index.json 업데이트

### 2순위 — 이번 주
- [ ] grandparent 심화 4편 topics MD 작성 (재무/결혼/눈치/인생책)
- [ ] YouTube OAuth tools/youtube/ 완성
- [ ] TTS 나레이션 파이프라인 연결 (GPT-SoVITS → 영상)

### 3순위 — 이번 달
- [ ] 뇌과학 시리즈 7편 추가
- [ ] math/music/memorial 시리즈 HTML 생성 (재료 있음)
- [ ] studio generator 구현 (썸네일 자동화)

---

## 5. 인프라 현황 요약

```
pd-bridge.py     : ✅ 실행 중 (TG 회의실 24시간 대기)
pd-bot.py        : ✅ 완성 (TG 보고 도구)
ADB 무선         : 🔶 집에서 USB 뽀뽀 1회 → 영구 자동화
무선 ADB 후      : Playwright로 폰 UI 자동화 가능
YouTube OAuth    : 🔶 auth.cjs 완성 필요
TTS 파이프라인   : ✅ GPT-SoVITS 로컬 가동 중
```

---

## 6. 경쟁 구도 (vs DeepSeek PD)

| 영역 | Claude PD | DeepSeek PD | 전략 |
|------|-----------|-------------|------|
| 전략/설계 | ✅ 강점 | 🔶 | 계획서·아키텍처 |
| 빠른 실행 | 🔶 | ✅ 강점 | 반복/패치 |
| 콘텐츠 품질 | ✅ 강점 | 🔶 | HTML 퀄리티 |
| throttle 대응 | 한도 시 멈춤 | ✅ 무한 실행 | 교대 운영 |

**운영 원칙**: Claude throttle 걸리면 DeepSeek이 받아서 계속 돌린다. 생산 절대 안 끊긴다.
