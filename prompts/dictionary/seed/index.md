# 📚 SEED Dictionary

> **Prompt Atom 추출용 SEED 사전. CDN 임베드 영상 → 재사용 가능한 프롬프트 원자.**

## 정의

박씨가 "CDN으로 유튜브 활용해 웹페이지나 코딩시 적용 임베드 하는 개인 프로젝트 아카이브"로 시작한 SEED 컬렉션. Garage 플레이리스트의 51개 영상이 원본.

각 영상 = 1 SEED. SEED는 다른 어떤 프롬프트 작업에도 atom 단위로 박을 수 있다.

## YouTube 연동

- **플레이리스트**: 📚 SEED Dictionary (1번)
- **원본 보존**: Garage (`PLp4XpLOr--JRnr7qV2_ker5IiP2urH0Fp`) 안 PARKSY SEED DICTIONARY 51영상
- **추출 방법**: 각 영상 → broadcast-packager Generator → Atom 생성 → `seed-atoms.json` 박음

## 파일

- `seed-atoms.json` — 영상 ID + 추출된 SEED 메타 (현재 빈 배열, 펜딩)
- `seed-template.md` — 새 SEED 추가 시 박는 템플릿 (펜딩)

## OrbitPrompt 정합

- **schemas**: `orbit/schemas/prompt-atom.schema.json` 정합
- **broadcast-packager**: 기존 Generator 재사용
- **YouTube 임베드**: 박씨 CDN 패턴 (기존 51영상 그대로)
