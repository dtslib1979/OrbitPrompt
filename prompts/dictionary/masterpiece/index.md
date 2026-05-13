# 🏛️ MASTERPIECE Gallery

> **마스터피스 분석 + 보존. 8 Boards 결과물 + FAVORITES 큐레이션.**

## 정의

마스터피스 = 박씨가 "이건 살린다"고 결정한 작품. 분석 + 보존 + 다음 작품의 레퍼런스.

## YouTube 연동

- **플레이리스트**: 🏛️ MASTERPIECE Gallery (12번)
- **원본 자산**:
  - Garage 안 FAVORITES 8영상 (큐레이션 시작점)
  - 8 Boards (memorial-tribute/luxury-editorial/music-curation/math-tutor 등) 시연 영상화
  - 박씨 미래 마스터피스

## 분석 프레임

| 축 | 평가 |
|---|---|
| 시간성 (Temporal) | 만든 시점 + 영구성 |
| 작가성 (Authorship) | 박씨 시그니처 |
| 기술성 (Technical) | Generator/도구 |
| 정서성 (Emotional) | Plutchik 8축 (Emotion Palette 정합) |
| 상징성 (Symbolic) | Symbol Database 정합 |
| 영향력 (Impact) | 다른 작품 영감 횟수 |
| 재사용성 (Reusability) | Atom 추출 가능 정도 |

## Generator

`masterpiece-analyzer.md` — 신규 Generator:
1. 입력: 영상/작품/콘텐츠 1개
2. 7축 자동 분석
3. Atom 추출 (Seed Dictionary에 박을 만한 것)
4. 마스터피스 등재 결정 (점수 ≥ 80)

## 파일

- `masterpiece-gallery.json` — 마스터피스 등재 목록 (펜딩, 초기 FAVORITES 8개 박음 예정)
- `masterpiece-analyzer.md` — Generator 정의 (펜딩)

## OrbitPrompt 정합

- **boards/**: 8 PWA가 1차 마스터피스 후보
- **archive.html**: 기존 archive UI 재사용
- **모든 사전 통합**: Seed/Cliché/Concept/Emotion/Symbol 모두 Masterpiece로 수렴
