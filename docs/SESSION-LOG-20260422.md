# OrbitPrompt 세션 로그 — 2026-04-22

## 세션 요약

이 세션에서 OrbitPrompt의 정체성과 목적이 근본적으로 재정의됨.

---

## 1. 이전 세션에서 이어받은 상태

- `whitepaper.html` — PHL-WHITEPAPER.md 전체 내용으로 재작성 완료 (14섹션)
- `about/position.html` — ORBITPROMPT-POSITION-PAPER.md로 신규 생성 완료
- `data/phases.json` v3 — 파트·챕터 구조 가드레일 (5파트 22챕터, 각 source 파일경로 + url 매핑)
- `index.html` — FAB 파트 카드 렌더러를 v2(채널맵) → v3(챕터맵)으로 교체

---

## 2. 방향 재확인: OrbitPrompt ↔ @philosopher-parksy 연동

**확인 경로**: `dtslib-papyrus/hq/config/channel-repo-map.json`

```json
"philosopher-parksy": {
  "title": "Parksy 철학",
  "repos": ["dtslib-papyrus", "OrbitPrompt", "parksy-logs"]
}
```

**5축 정체성 확인 (전부 YES):**

| 축 | 내용 | 확인 |
|----|------|------|
| PHL ↔ YouTube | @philosopher-parksy 채널과 연동 | ✅ channel-repo-map.json SSOT |
| 인터랙티브 웹페이지 제작 공정 | Generator 7개 (Chalkboard, PWA, Instruction, Dataset, Identity, Editorial, Route) | ✅ |
| 생각 리버스엔지니어링 → 코드 제너레이터 | PHL 토큰이 말버릇을 프로토콜로 물성화 | ✅ |
| 시드 = 대화 로그 | parksy-logs → Lane B Orbit Prompt 컴파일러 | ✅ |
| 출판사 구조 | "공장을 만드는 공장", 대화=원고, 레포=책 | ✅ |

---

## 3. PHL 페이지 설계 방향 확정

**결론**: PHL 토큰 3개(Expansion/Hardening/Reverse)를 단순 문서 페이지가 아닌 **인터랙티브 프롬프트 제너레이터**로 만들어야 함.

```
PHL-Expansion.html:
  입력: 어떤 모듈에 적용할지 텍스트 입력
  출력: Claude Code에 바로 붙여넣을 수 있는 완성 프롬프트
  버튼: [복사] [Claude에서 열기]
```

스펙 자체는 하단 접이식 섹션으로. 주인공은 생성기.

---

## 4. YouTube 루프백 구조 확정

```
YouTube 영상 (왜/개념 설명)
    ↓
OrbitPrompt 웹페이지 (어떻게 사용 — 인터랙티브 도구)
    ↓
Claude Code에서 PHL 실행
    ↓
결과물 (커밋, 변경된 레포)
    ↓
다음 YouTube 영상 소재
    ↑_________________________↓
```

**YouTube에 가야 할 것**: 보여줘야만 전달되는 것 (탄생 서사, 라이브 과정, 메타 공정)
**OrbitPrompt에 남아야 할 것**: 읽고 쓰는 것 (스펙, 도구, 아카이브)

---

## 5. Discord/알림 결론

**지금은 안 해도 된다.**

이 시스템은 외부 피드백 없이 자기완결:
```
대화 → 출판 → 영상 → 다음 대화
```

Discord는 YouTube 댓글이 먼저 차면 그때 고려. 지금은 GitHub + YouTube 댓글로 충분.
알림은 하나만: YouTube 최신 영상 → OrbitPrompt 사이트 자동 임베드.

---

## 6. 🔥 핵심 재정의 (이 세션의 가장 중요한 결론)

### Before
```
OrbitPrompt = Generator 도구 모음 + 출판물 전시장
```

### After
```
OrbitPrompt = 스튜디오 (엔진) — 납품은 밖으로, 사이트엔 과정만
```

**웹사이트의 목적 재정의:**
> "내가 어떻게 21세기 철학자의 방법론을 코드로 물성화했는가" 를 보여주는 **과정 저널**

### 전체 아키텍처

```
parksy-logs (대화 로그 — 원석 시드)
    ↓
OrbitPrompt 스튜디오 (엔진)
    ├── PHL — 나만의 프로그래밍 언어 체계 (개발 중)
    ├── 리버스엔지니어링 → 웹페이지 스튜디오 MCP (블랙박스)
    └── Generator들 → 납품 (다른 레포/클라이언트로 출력)

OrbitPrompt 웹사이트 = 과정 저널 (방법론만)
    ├── 왜 이 언어 체계를 만들었나
    ├── 어떻게 리버스엔지니어링으로 스튜디오를 뽑았나
    ├── 대화 로그가 어떻게 시드가 되는가
    ├── 지금 뭘 만들고 있나 (현재 진행형)
    └── 납품된 것들 링크 (전시 아님, 포인터만)

영상화 → @philosopher-parksy
    = 철학자가 되어가는 과정 서사
```

### phases.json v3 재해석

| 파트 | 기존 설명 | 재해석 |
|------|-----------|--------|
| 00 WHY | 이 시스템은 왜 존재하는가 | 왜 이 스튜디오를 짓기 시작했나 |
| 01 PHL | 말 기반 프로토콜 토큰 정의 | 내가 만든 언어 체계 — 개발 중 |
| 02 Atom | 재사용 가능한 실행 단위 | 발견한 빌딩블록들 |
| 03 Generator | Prompt Engine | 도구가 된 것들 (납품 엔진) |
| 04 Archive | 생성물·개발 로그 | 과정 로그 + 개발 기록 |

---

## 7. 다음 작업 (미완료)

### 즉시 착수 가능
- [ ] `index.html` 개편 — "도구 쇼케이스"에서 "스튜디오 저널 표지"로
- [ ] PHL 토큰 3개 인터랙티브 제너레이터 HTML 페이지 생성
  - `phl/expansion.html`
  - `phl/hardening.html`
  - `phl/reverse.html`
- [ ] `data/phases.json` 각 챕터 `url` 필드 업데이트 (pending → 실제 경로)

### 이후
- [ ] orbit/templates/ 6개 Prompt Atom → HTML 페이지
- [ ] archive.html — boards/ 컬렉션
- [ ] YouTube 최신 영상 자동 임베드 (루프백)
- [ ] DEVPLAN / COMPETITIVE-LANDSCAPE 페이지

---

## 8. 확정된 메타포

| 메타포 | 의미 |
|--------|------|
| **스튜디오** | OrbitPrompt 전체 — 납품 공장 |
| **블랙박스** | MCP 엔진, Generator 내부 — 방문자에게 숨김 |
| **과정 저널** | 웹사이트 — 방법론 기록 |
| **납품** | Generator 출력물 → 다른 레포로 |
| **원석 시드** | parksy-logs 대화 로그 |
| **물성화** | 말버릇/철학 → 코드/프로토콜 |
| **철학자 페르소나** | @philosopher-parksy — 영상으로만 등장 |
