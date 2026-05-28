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
└── {category}-{generator}.md ← Generator 정의
```

## 현재 상태 ✅

| 카테고리 | JSON 데이터 | Generator | 영상 파이프라인 | 상태 |
|---------|------------|-----------|---------------|------|
| `seed/` | — | — | — | ⏳ TODO |
| `cliche/` | — | — | — | ⏳ TODO |
| `concept/` | `concept-taxonomy.json` (12개 개념) | `concept-parser.md` ✅ | concept_picture_pipeline.py ✅ | ✅ 완료 |
| `emotion/` | `emotion-palette.json` (8개 감정) | — | ✅ (공용 파이프라인) | ✅ 완료 |
| `symbol/` | — | — | — | ⏳ TODO |
| `masterpiece/` | — | — | — | ⏳ TODO |

## 파이프라인 연동

모든 개념어 그림 사전 데이터는 다음 파이프라인으로 영상화됨:

```
concept-taxonomy.json / emotion-palette.json
    ↓
concept_picture_pipeline.py
    ├── concept_to_image_prompt() — 7축 + 4축×8감정 → FLUX/SD 프롬프트
    ├── generate_image_vast() — Vast.ai ComfyUI 이미지 생성 (선택)
    ├── create_slideshow_video() — FFMPEG 슬라이드쇼 (1920×1080, 8초)
    └── generate_youtube_metadata() — 쇼츠/롱폼 메타데이터
    ↓
outputs/concept_pictures/ — .mp4 + .json + .txt
```

### 실행

```bash
# 단일 개념어 생성
python3 ~/parksy-logs/pipelines/batch_generate.py

# Vast.ai 이미지 포함
python3 ~/parksy-logs/pipelines/batch_generate.py --use-vast

# 특정 카테고리만 목록
python3 ~/parksy-logs/pipelines/batch_generate.py --list
```

## 정합성

- OrbitPrompt 14 Generator → **19+ Generator로 확장** (사전 6개 + 신규 Generator)
- 개념어 그림 사전 파이프라인 = `parksy_rawmat_mcp.py`의 `concept_dict_generate()`, `concept_dict_batch()` MCP 툴
- @EAE-University 채널 12 플레이리스트 중 **사전 6개**가 본 폴더 1:1 매핑

## 다음 작업

1. `cliche/` CLICHÉ Thesaurus 데이터 박음 (한국어 클리셰 100개)
2. `symbol/` SYMBOL Database 데이터 박음 (핵심 심볼 30개)
3. `seed/` SEED Atoms 추출 (Garage 51개 SEED 영상 → JSON)
4. `masterpiece/` MASTERPIECE Gallery 데이터 박음 (명작 10개)
5. Vast.ai ComfyUI 연동 검증 (--use-vast 플래그)
