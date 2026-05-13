# 🎭 EMOTION Palette

> **감정 필터 + Editorial 적용 팔레트. Plutchik 8축 + 박씨 음성/음악/시각 결합.**

## 정의

감정은 콘텐츠의 드라이버. Plutchik 8축(joy/sadness/trust/disgust/fear/anger/surprise/anticipation)을 좌표로 박씨 결과물(음성/음악/시각/문장)에 일관 적용.

## YouTube 연동

- **플레이리스트**: 🎭 EMOTION Palette (10번)
- **원본**: 미존재 (신규 영상 양산 대상)
- **목표**: 8 감정 × 4 미디어(음성/음악/시각/문장) = 32 시연 영상

## Plutchik 8축

| 감정 | 색상 | BGM 톤 | 시각 무드 |
|---|---|---|---|
| joy | yellow | major | 밝음 |
| sadness | blue | minor | 어둠 |
| trust | green | warm | 안정 |
| disgust | purple | dissonant | 왜곡 |
| fear | black | tremolo | 떨림 |
| anger | red | percussive | 격렬 |
| surprise | orange | sudden | 단절 |
| anticipation | gold | rising | 상승 |

## Generator

`emotion-mapper.md` — 신규 Generator:
1. 입력: 텍스트 또는 감정명
2. Plutchik 8축 벡터 자동 추출
3. Editorial Generator에 박씨 색상/BGM/시각 파라미터 전달
4. 출력: 8축 좌표 + 적용 권장 미디어 조합

## 파일

- `emotion-palette.json` — 8축 정의 + 색/음/시각 매핑 (펜딩)
- `emotion-mapper.md` — Generator 정의 (펜딩)

## OrbitPrompt 정합

- **prompts/editorial/**: 럭셔리 룩북 Generator에 색상/감정 인자 전달
- **parksy-audio**: SEA-MCP Φ₁ Plutchik 정합 (`papyrus/docs/sea-mcp/`)
