# 🧩 CONCEPT Taxonomy

> **개념 분해 + 7축 계층화. PHL 토큰과 정합.**

## 정의

개념은 단일 단어가 아니라 **계층/관계 구조**. 7축 분석으로 각 개념을 좌표화한 후 다른 개념과 비교/조합 가능.

## YouTube 연동

- **플레이리스트**: 🧩 CONCEPT Taxonomy (9번)
- **원본**: Garage 안 CONCEPT DICTIONARY 2영상
- **확장**: 박씨 28레포 핵심 개념 100개 영상화

## 7축 (Identity Generator 정합)

1. 의미 (semantic)
2. 시대성 (temporal)
3. 추상도 (abstraction)
4. 적용범위 (scope)
5. 대체가능성 (replaceability)
6. 결합가능성 (combinability)
7. 생산성 (generativity)

## Generator

`concept-parser.md` — 신규 Generator:
1. 입력: 개념어 1개
2. 7축 좌표 자동 추출
3. PHL 토큰 매핑 (Expansion/Hardening/Reverse 중 어느 토큰에 적합한지)
4. 관련 개념 N개 자동 제시 (taxonomy 계층 안)

## 파일

- `concept-taxonomy.json` — 개념 계층 데이터 (펜딩)
- `concept-parser.md` — Generator 정의 (펜딩)

## OrbitPrompt 정합

- **PHL_INDEX.json**: 3 토큰과 매핑
- **philosophy.html**: 7축 프레임 reuse
- **identity-model.schema.json**: 7축 정의 정합
