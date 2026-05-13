# OrbitPrompt Dictionary

> **6 사전 시리즈 × YouTube @EAE-University 채널 1:1 매핑**

**작성일**: 2026-05-13
**용도**: 박씨 28레포 생태계의 어휘/개념/감정/상징/마스터피스 영구 사전화

## 6 사전

| 폴더 | 카테고리 | YouTube PL | OrbitPrompt Generator |
|---|---|---|---|
| `seed/` | 📚 SEED Dictionary | 📚 SEED | (기존 broadcast-packager reuse) |
| `cliche/` | 💬 CLICHÉ Thesaurus | 💬 CLICHÉ | **Cliché Breaker** (신규) |
| `concept/` | 🧩 CONCEPT Taxonomy | 🧩 CONCEPT | **Concept Parser** (신규) |
| `emotion/` | 🎭 EMOTION Palette | 🎭 EMOTION | **Emotion Mapper** (신규) |
| `symbol/` | ⚡ SYMBOL Database | ⚡ SYMBOL | **Symbol Encoder** (신규) |
| `masterpiece/` | 🏛️ MASTERPIECE Gallery | 🏛️ MASTERPIECE | **Masterpiece Analyzer** (신규) |

## 구조 (각 카테고리 공통)

```
{category}/
├── index.md              ← 카테고리 정의 + YouTube PL 링크 + Generator 매핑
├── {category}-{type}.json ← 데이터 (atoms/thesaurus/taxonomy/palette/database/gallery)
└── {category}-{generator}.md (Cliché~Masterpiece 5개) ← 신규 Generator 정의
```

## 정합성

- OrbitPrompt 14 Generator → **19 Generator로 확장** (5 사전 Generator 신규)
- @EAE-University 채널 12 플레이리스트 (Garage 1 + 메인 12) 중 **사전 6개**가 본 폴더 1:1
- 박씨 헌법 "스튜디오(엔진) + 과정저널" 정합

## 다음 작업

1. SEED Atoms 추출 (Garage 51개 SEED 영상 → JSON)
2. CLICHÉ Thesaurus 데이터 박음 (한국어 클리셰 100개)
3. 5 신규 Generator 코드 박음 (각 .md 템플릿 → HTML 페이지로)
