# OrbitPrompt 전략 포지셔닝 — 글로벌 2트랙
> 확정: 2026-05-28 / 박씨 직접 정의
> 연관 문서: parksy-logs/docs/, eae-univ/docs/, eae.kr/docs/ (동일 전략 각 레포 시각)

---

## DTSlib 정체성

> **글로벌 할머니·할아버지들의 이야기와 지혜를 편집하고 출판하는 AI 시대 대학/출판사**

---

## 2트랙 전략

| | Track A — 영미권 자동화 | Track B — 한국 로컬 |
|---|---|---|
| 대상 | 영미권 할머니·할아버지 | 한국 할머니·할아버지 |
| 언어 | 영어 (AI 자동 생성) | 한국어 (박씨 직접) |
| 수익 | YouTube 고CPM 광고 | 로컬 구독/비즈니스 |
| 운영 | 무인 자동화 | 박씨 직접 관계 |

---

## OrbitPrompt 역할 (언어 초월 편집 OS)

### 핵심 포지션
> **OrbitPrompt = 언어 무관 편집 엔진**
> 어느 나라 할머니·할아버지 이야기가 들어와도 같은 PHL 구조를 통과한다.

### Track A에서의 역할 — 영어 1회 세팅의 핵심
```
영어 콘텐츠는 박씨가 직접 강의하지 않아도 된다.
OrbitPrompt 개념 프레임을 영어로 1회 잘 작성
→ Edge Runtime이 동적으로 서빙
→ 영미권 YouTube 고CPM 자동 수익
```

- `topics/` — 인생/관계/실패·회복 개념을 영어로 정의 (1회)
- `prompts/editorial/` — 영어 편집 프롬프트 세팅
- `prompts/dictionary/` — 영어 개념 사전 생성기

### Track B에서의 역할 — 한국 버전 고도화
- 박씨 구술 → PHL 태깅 → 더 깊은 한국 강의 구조
- 한국 할머니·할아버지에게 더 정교한 콘텐츠 제공
- 로컬 프리미엄 서비스의 품질 엔진

---

## 언어별 topics/ 구조 (목표)

```
topics/
  life/
    ko.md    ← 한국어 인생 개념 (현재)
    en.md    ← 영어 버전 (1회 작성)
    ja.md    ← 일본어 (추후)
  relationships/
    ko.md
    en.md
  resilience/
    ko.md
    en.md
```

**PHL 토큰 구조 자체는 언어 무관** — 토큰은 바뀌지 않고 각 언어 텍스트만 추가.

---

## 파이프라인 (이 레포 기준)

```
parksy-logs (원자재)
    ↓ rawmat.collect_primer
OrbitPrompt   ← 여기
  PHL 태깅 + 개념 추출
  언어 감지 → ko/en/ja 분기
    ↓ 영어: webpage.build_page → eae.kr Edge Runtime
    ↓ 한국어: 박씨 직접 편집 → eae-univ 한국 슬롯
```

---

## 즉시 해야 할 것

1. `topics/life/en.md` — 영어 인생 개념 1회 작성 (Track A 시작점)
2. `prompts/editorial/en_grandparent.md` — 영미권 할머니·할아버지용 편집 프롬프트
3. `prompts/dictionary/en_seed.md` — SEED Dictionary 영어 버전

**이 3개만 세팅하면 Track A 파이프라인 돌릴 수 있다.**

---

*문서 위치: OrbitPrompt/docs/STRATEGY_GLOBAL_2TRACK_20260528.md*
*연관: parksy-logs/docs/STRATEGY_GLOBAL_2TRACK_20260528.md*
*연관: eae-univ/docs/STRATEGY_GLOBAL_2TRACK_20260528.md*
*연관: eae.kr/docs/STRATEGY_GLOBAL_2TRACK_20260528.md*
