# 추모 다큐멘터리 제작 워크플로

> Gemini 분석 → Chalkboard 인터랙티브 → Galaxy 녹화 → YouTube

---

## 컨셉

**"역사의 증인이자 치열했던 승부사"**

- 슬픔 강조 ❌
- 거대한 서사 정리 ⭕
- 고인의 육성으로 스토리 전개 (내레이션 없음)

---

## 전략

| 구분 | 전략 |
|------|------|
| 오디오 | 고인 육성만 사용 → 진정성 극대화 |
| 비주얼 | 흑백(과거/투쟁) → 컬러(현재/영광) 자연 전환 |
| 감정 곡선 | 투쟁 → 성취 → 여유 → 감사 |

---

## 타임라인 구조

### ① 도입부: 운명의 시작 [00:00 ~ 00:30]

**의도:** 평범한 청년이 역사의 소용돌이로 들어가는 순간

| 요소 | 설정 |
|------|------|
| 비디오 | 흑백 자료, Ken Burns 효과 (줌인/줌아웃) |
| 오디오 | 덤덤한 회고 육성 + 첼로 솔로 |
| 자막 | 명조체, 날짜/사건명만 간결하게 |
| 무드 | somber, grayscale |

**핵심 멘트:** *"10월 17일이 제 인생을 바꾼 날입니다"*

---

### ② 전개: 투사의 시대 [00:30 ~ 02:00]

**의도:** 불의와 타협하지 않는 강인한 이미지

| 요소 | 설정 |
|------|------|
| 비디오 | SD 화질 그대로 (현장감), 눈빛 클로즈업 |
| 오디오 | 강렬한 멘트 믹싱, Percussion 추가 |
| 효과 | 필름 노이즈, 플래시 컷 |
| 무드 | intense, high-contrast |

**핵심 멘트:** *"걸레는 빨아도 걸레"*

---

### ③ 절정: 리더의 무게 [02:00 ~ 03:00]

**의도:** 투사 → 정치가/행정가로 변모

| 요소 | 설정 |
|------|------|
| 비디오 | HD/4K 컬러 전환, 군중과 함께하는 풀샷 |
| 오디오 | 웅장한 오케스트라 |
| 효과 | 컬러 복원, 채도 상승 |
| 무드 | triumphant, full-color |

**핵심 멘트:** *"더불어민주당의 역사입니다"*

---

### ④ 환기: 인간적 면모 [03:00 ~ 03:45]

**의도:** 딱딱한 이미지 탈피, 여유와 해학

| 요소 | 설정 |
|------|------|
| 비디오 | 파안대소, 어깨동무, Warm Tone |
| 오디오 | 현장 웃음소리/박수, 피아노 선율 |
| 효과 | 따뜻한 색감 |
| 무드 | warm, relaxed |

**핵심 멘트:** *"독재하고 싸우다가... 가짜 같아서 싸우는 재미가 없다"*

---

### ⑤ 결말: 영원한 안식 [04:00 ~ 끝]

**의도:** 마지막 당부와 작별

| 요소 | 설정 |
|------|------|
| 비디오 | 뒷모습, 손 흔드는 모습, 롱테이크 |
| 오디오 | 감사 인사 + Echo 효과 |
| 효과 | White Out 또는 Black Fade |
| 무드 | farewell, peaceful |

**핵심 멘트:** *"국민들께 많은 성원을 받았습니다. 결코 잊지 않겠습니다."*

**마무리:** "늘 행복하고 건강하십시오" → 에코 → 추모 자막 5초

---

## Chalkboard 구현

### JSON 데이터 구조

```json
{
  "type": "memorial-documentary",
  "subject": {
    "name": "이해찬",
    "title": "전 국무총리",
    "years": "1952-2025"
  },
  "concept": "역사의 증인이자 치열했던 승부사",
  "sections": [
    {
      "id": "intro",
      "time": "00:00-00:30",
      "title": "운명의 시작",
      "mood": "somber",
      "filter": "grayscale",
      "effect": "ken-burns-zoom-in",
      "quote": "10월 17일이 제 인생을 바꾼 날입니다",
      "bgm": "cello-solo",
      "images": ["1972-youth.jpg", "military-truck.jpg"]
    },
    {
      "id": "fighter",
      "time": "00:30-02:00",
      "title": "투사의 시대",
      "mood": "intense",
      "filter": "high-contrast",
      "effect": "film-grain",
      "quote": "걸레는 빨아도 걸레",
      "bgm": "percussion-tension",
      "images": ["hearing-1988.jpg", "closeup-eyes.jpg"]
    },
    {
      "id": "leader",
      "time": "02:00-03:00",
      "title": "리더의 무게",
      "mood": "triumphant",
      "filter": "full-color",
      "effect": "orchestral-swell",
      "quote": "더불어민주당의 역사입니다",
      "bgm": "orchestra-grand",
      "images": ["party-leader.jpg", "crowd-victory.jpg"]
    },
    {
      "id": "human",
      "time": "03:00-03:45",
      "title": "인간 이해찬",
      "mood": "warm",
      "filter": "warm-tone",
      "effect": "ambient-laughter",
      "quote": "가짜 같아서 싸우는 재미가 없다",
      "bgm": "piano-light",
      "images": ["laughing.jpg", "colleagues.jpg"]
    },
    {
      "id": "farewell",
      "time": "04:00-end",
      "title": "영원한 안식",
      "mood": "peaceful",
      "filter": "soft-fade",
      "effect": "white-out",
      "quote": "결코 잊지 않겠습니다",
      "bgm": "silence-echo",
      "images": ["walking-away.jpg", "waving.jpg"]
    }
  ]
}
```

### CSS 효과 매핑

```css
/* Mood Filters */
.mood-somber { filter: grayscale(100%) contrast(1.1); }
.mood-intense { filter: grayscale(80%) contrast(1.3); }
.mood-triumphant { filter: saturate(1.1) brightness(1.05); }
.mood-warm { filter: sepia(20%) saturate(1.2) brightness(1.1); }
.mood-peaceful { filter: brightness(1.2) contrast(0.9); }

/* Ken Burns Effect */
@keyframes ken-burns-zoom-in {
  from { transform: scale(1); }
  to { transform: scale(1.15); }
}

/* Film Grain */
.film-grain::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('grain.svg');
  opacity: 0.15;
  pointer-events: none;
}

/* White Out */
@keyframes white-out {
  from { opacity: 0; }
  to { opacity: 1; background: white; }
}
```

### 인터랙션

```
터치/클릭 → 다음 섹션
스와이프 좌우 → 섹션 이동
길게 누르기 → 현재 섹션 반복
```

---

## 제작 파이프라인

```
1. 대상 인물 선정
      ↓
2. Gemini에게 YouTube 영상 분석 요청
      ↓
3. 워크플로 JSON 생성
      ↓
4. Chalkboard에 JSON 로드
      ↓
5. 이미지/오디오 에셋 준비 (parksy-image, parksy-audio)
      ↓
6. Galaxy 화면 녹화 + 터치로 섹션 전환
      ↓
7. YouTube 업로드
      ↓
8. 완성
```

---

## 핵심 원칙

1. **편집 제로** — 녹화 = 완성물
2. **내레이션 제로** — 고인 육성만 사용
3. **감정 곡선 설계** — 투쟁 → 성취 → 여유 → 감사
4. **재사용 가능** — JSON만 바꾸면 새 추모 영상

---

## 참고

- 원본 분석: Gemini (YouTube 영상 분석)
- 참고 영상: [故 이해찬 전 국무총리 추모](https://youtu.be/R0WENgpytEs)
- Ken Burns 효과: 다큐멘터리 표준 기법
- 오디오 덕킹: 목소리 나올 때 BGM 자동 감소
