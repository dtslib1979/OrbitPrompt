# 001 — OrbitPrompt 전면 개편 + phoneparis 미러링 (2026-04-21)

## 세션 컨텍스트
- **레인**: tab_claude (knowledge management track)
- **5-Lane 역할**: OrbitPrompt + eae-univ 동시 개발

---

## Phase 1: 전체 파싱

### 파싱 대상
- parksy-logs / dtslib-papyrus / OrbitPrompt / eae-univ
- phoneparis (phone_claude 세션 관찰)
- OrbitPrompt/docs/ 전체 (POSITION-PAPER, RULES, TECHNICAL_SPECIFICATIONS 등)

### 파악한 핵심 구조
- OrbitPrompt = "공장 찍어내는 설계도면실" — papyrus급 위상
- 14개 Generator 카테고리 (broadcast/chalkboard/apk/dataset/editorial/engine/form/guide/identity/instruction/publisher/route/studio + whitepaper)
- PHL Protocol: 8-step cycle, 3 tokens, 46 tests
- Dual Lane: Lane A (University) + Lane B (Orbit)
- Perplexity Spaces: 8개 (`parksy-logs/perplexity/`)

---

## Phase 2: index.html 전면 개편

### eae-univ/index.html
- **Before**: 2447줄 (기존 복잡한 구조)
- **After**: 634줄
- Commit: `a26a069`
- 버그 발견: `cache.playlists.find(...)` — 실제 캐시는 `data.videos[]` top-level

### OrbitPrompt/index.html
- **Before**: 402줄
- **After**: 681줄
- Publisher/칠판센터 허브로 개편
- 14 Generator 그리드 (broadcast/publisher/engine/guide live, 나머지 disabled)
- PHL Protocol 4-card 섹션, Dual Lane, Perplexity Spaces 8개
- Commit: `aeb8f63`

---

## Phase 3: phoneparis 관찰 → 미러링

### phoneparis에서 발견한 패턴
1. **discord-cache.yml**: 30분 cron → Discord Bot API → `data/latest-messages.json`
2. **update-index.yml**: `prompts/*.html` push 시 `prompts/index.json` 자동 갱신
3. **youtube-cache.json 실제 구조**: `{videos: [...], stats: {...}}` — `playlists: []` 비어있음

### OrbitPrompt에 이미 있던 것
- `.github/workflows/update-index.yml` ✅ (이미 미러됨)
- `.github/workflows/discord-notify.yml` ✅
- `.github/workflows/repo-guard.yml` ✅

### 미러링 실행
1. **eae-univ youtube BUG 수정**: `cache.playlists.find()` → `cache.stats.videoCount` 사용
2. **discord-cache.yml 생성**: OrbitPrompt용 (이번 세션)
3. **docs/dev-logs/ 구조 생성**: 오늘부터 OrbitPrompt 자체 기록

---

## 기술 결정사항

### youtube-cache.json 패턴
```js
// 버그 (phoneparis 관찰 전)
if (cache?.playlists) { cache.playlists.find(p => p.playlistId === pl.id) }

// 수정 (실제 구조 반영)
const total = cache?.stats?.videoCount || 0;
if (total > 0) statEl.textContent = total;
```

### OrbitPrompt 포지션
- papyrus처럼 자체 `docs/dev-logs/` 구조 필요
- Discord + YouTube 연동이 다음 우선순위

---

## 커밋 현황
| 레포 | 커밋 | 내용 |
|------|------|------|
| eae-univ | a26a069 | index.html 전면 개편 |
| OrbitPrompt | aeb8f63 | index.html 전면 개편 |
| dtslib-papyrus | 0c038c5 | dev-log 046 Session 13 추가 (잘못된 위치 — 이후 OrbitPrompt로 이전) |

---

## 다음 작업
- [ ] discord-cache.yml → OrbitPrompt (Discord Bot Token 설정 필요)
- [ ] export.cjs c계정 실행 → eae-univ/data/youtube-cache.json 갱신
- [ ] OrbitPrompt unread docs 완료 (PHL-WHITEPAPER, TECHNICAL_SPECIFICATIONS 등)
