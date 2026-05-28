# 🧩 Concept Parser — GENERATOR 정의

> **7축 분석 + 4축×8감정 + 이미지 프롬프트 → 개념어 그림 사전**

**작성일**: 2026-05-28
**연계**: concept_picture_pipeline.py, concept-taxonomy.json

## 입력

```
concept: str (개념어 1개)
category: str (seed/cliche/concept/emotion/symbol/masterpiece)
definition: str (1-2문장 정의)
stage: str (meta/reverse/module/zoom/quantum/spiral/language)
phl_token: str (Expansion/Hardening/Reverse)
```

## 처리 파이프라인

### Step 1 — 7축 분석 자동 추출
```
개념어 + 정의 → LLM → 7축 좌표 JSON
1. 의미 (semantic): 개념의 핵심 의미
2. 시대성 (temporal): 시대적 위치
3. 추상도 (abstraction): 구체↔추상 스펙트럼
4. 적용범위 (scope): 개인↔보편 스펙트럼
5. 대체가능성 (replaceability): 대체 가능성
6. 결합가능성 (combinability): 다른 개념과의 결합력
7. 생산성 (generativity): 새로운 것 생성 능력
```

### Step 2 — 4축×8감정 매핑
```
4축(생존/소유/공간/시간) × 8감정(분노/공포/기쁨/슬픔/신뢰/혐오/기대/놀람)
→ 각 셀 0-100 점수 매핑
→ PHL 토큰 매핑 (Expansion=고기쁨·신뢰·기대, Hardening=고분노·혐오, Reverse=고놀람·공포)
```

### Step 3 — 이미지 프롬프트 생성
```
개념어 정의 + 7축 + 4축×8감정 → 카테고리별 스타일 이미지 프롬프트
→ concept_picture_pipeline.py concept_to_image_prompt()
```

### Step 4 — 영상 생성
```
이미지/텍스트 슬라이드 → FFMPEG 슬라이드쇼 (1920×1080, 8초)
→ YouTube 쇼츠/롱폼 메타데이터 동시 생성
```

## 출력

| 출력물 | 포맷 | 용도 |
|--------|------|------|
| 이미지 프롬프트 | .txt | Vast.ai ComfyUI 입력 |
| 슬라이드쇼 영상 | .mp4 (1920×1080) | YouTube 쇼츠/롱폼 |
| 메타데이터 | .json | YouTube 업로드 |
| 개념 엔트리 | .json (taxonomy에 추가) | OrbitPrompt 사전 영구 등록 |

## 연동 MCP

```python
# parksy_rawmat_mcp.py
mcp.tool() concept_dict_generate(concept, category, definition, ...)
mcp.tool() concept_dict_batch(category)  # logs → batch 생성
```

## 실행

```bash
# 단일
python3 ~/parksy-logs/pipelines/concept_picture_pipeline.py \
  --concept 자유 --category concept \
  --definition "외부 강제 없이 스스로 선택할 수 있는 상태"

# 배치
python3 ~/parksy-logs/pipelines/concept_picture_pipeline.py \
  --batch --category concept
```

*Co-Authored-By: Claude Code <noreply@anthropic.com>*
