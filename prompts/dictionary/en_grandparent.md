# EN Grandparent — Track A Editing Prompt

> **용도**: 영미권 할머니·할아버지 콘텐츠 편집 Generator
> **경로**: OrbitPrompt → EAE-University (RT-β) → eae.kr (RT-δ)
> **CPM 타겟**: $3-8 (Health / Finance / Resilience / Relationship)

---

## 입력

`topics/grandparent/*.md` — PHL 프레임이 적용된 개념 파일들:

| 파일 | 개념 | PHL 토큰 |
|------|------|-----------|
| `wisdom_en.md` | Wisdom | PHL-wisdom-en |
| `life_en.md` | Life | PHL-life-en |
| `story_en.md` | Story | PHL-story-en |

각 파일은 다음 구조:
- frontmatter (id, lang, track, category, concept, phl_token)
- Core Concept (한 줄 정의)
- PHL Frame (INPUT / FILTER / OUTPUT)
- Editorial Prompts (opening / depth / closing)
- Key Concepts (4개)
- YouTube Content Angles (4개, 고CPM 우선)

---

## 출력 포맷

### 1. YouTube 대본 (롱폼 8-15분)

```markdown
# Title: {고CPM 키워드 포함, 40자 이내}

## Hook (0:00-0:30)
{할머니/할아버지의 한 줄 — "I was 72 when I learned..."}

## Context (0:30-2:00)
{PHL Frame INPUT — 어떤 결정? 어떤 맥락?}

## Depth (2:00-8:00)
{PHL Frame FILTER — 책에서 못 배운 것?}
- Key Concept 1: {Earned wisdom}
- Key Concept 2: {Contrast wisdom}
- Vivid detail: {smell, sound, place}

## Lesson (8:00-10:00)
{PHL Frame OUTPUT — 한 줄 원칙}

## CTA (10:00-end)
{Editorial Prompts closing을 질문 형태로}
```

### 2. YouTube 메타데이터

```json
{
  "title": "{SEO 최적화, 70자}",
  "description": "{PHL Core Concept + PHL Frame OUTPUT}",
  "tags": ["grandparent", "wisdom", "life-lessons", "elder-advice", "{concept specific}"],
  "category": "22 (People & Blogs)",
  "target_cpm": "$3-8"
}
```

### 3. 쇼츠 (60초, 세로)

```markdown
# 쇼츠 스크립트
Text: {PHL Core Concept 한 줄}
Visual: {연관 이미지/영상}
Audio: {잔잔한 피아노 or 할머니/할아버지 내레이션}
```

---

## 편집 원칙

### 언어
- 영미권 원어민 자연스러움 유지 (번역체 금지)
- 단문 위주. 문장 20단어 이하.
- "you know", "let me tell you" 등 구어체 허용

### CPM 최적화
- 건강/재정/회복력 각도 우선 (Track A 고CPM)
- 광고주 친화 키워드 포함 (retirement planning, family values, health tips)
- 논란/정치/종양 주제 금지

### 감정 곡선
```
↓ 문제 제기 (0-15%): "I never thought I'd survive..."
↓↓ 깊이 (15-50%): 실제 경험, 구체적 디테일
↗ 반전 (50-75%): "Then I realized..."
↑ 교훈 (75-90%): 명확한 원칙
→ 여운 (90-100%): 질문으로 마무리
```

### PHL 강제
모든 출력은 PHL Frame을 통과해야 함:
1. INPUT 수집 → 할머니/할아버지의 실제 결정/경험
2. FILTER 적용 → "책에서 못 배운 것" 필터
3. OUTPUT 추출 → 한 줄 원칙으로 압축

---

## Track B (한국어) 연동

Track B는 동일한 PHL 구조 사용, 언어만 한국어:
- `topics/grandparent/wisdom_ko.md` ↔ `life_ko.md`
- 한국어 편집 프롬프트: 고유어 감성 + 정서적 공감 우선
- CPM: Track A보다 낮지만 한국 프리미엄 사용자 대상

---

## 체크리스트

- [ ] PHL Frame OUTPUT이 한 줄로 압축되었는가?
- [ ] 고CPM 각도 (건강/재정/회복력) 중 하나를 포함하는가?
- [ ] Opening Question으로 시작하는가?
- [ ] Closing Question으로 끝나는가?
- [ ] Key Concept 4개 중 최소 2개가 대본에 녹아있는가?
- [ ] 영미권 원어민에게 자연스러운가? (AI 번역체 아님)

---

*Generator: OrbitPrompt / PHL Frame: RT-α / Target: @EAE-University Track A*
