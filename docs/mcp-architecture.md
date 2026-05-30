# MCP 2계층 구조

## 제1계층: 공정 MCP (Manufacturing Process)
**역할**: ParksyLog 원자재를 가공하여 완제품을 생산하는 독립 공정 라인

| MCP | 생산물 | 위상 |
|-----|--------|------|
| parksy-actor | MP4 녹화 | 독립 공정 |
| parksy-audiolog | 오디오북 (master.mp3) | 독립 공정 |
| parksy-voice | TTS/음성 합성 | 독립 공정 |
| parksy-distributor | 채널 송출 | 독립 공정 |
| parksy-webpage | 페이지 빌드 | 독립 공정 |

**특징**: 각자 독립된 인프라에서 실행. 하나의 완성품(영상/음원/글)을 만드는 제조 라인.

---

## 제2계층: 모듈 MCP (Thought Module Satellite)
**역할**: 캡처된 대화 로그 → 사고 모듈 추출 → 갤러리 전시

| MCP | 생산물 | 위상 |
|-----|--------|------|
| mcp-parksy-module-gallery | Thought Module (index.html + whitepaper) | OrbitPrompt 위성 |

**특징**: 
- OrbitPrompt 레포 안에 존재 (`mcp-parksy-module-gallery/`)
- 제1계층 MCP가 생산한 원자재(로그/캡처)를 가져와서 사고 모듈로 가공
- 출력물을 `index.html` MODULES 배열에 등록 → 갤러리 전시
- 다른 MCP와 달리 "완제품"이 아닌 "사고 과정 자체"를 아티팩트화

---

## 데이터 흐름

```
ParksyLog (원자재)
  │
  ├─→ 제1계층 공정 MCP → MP4 / audio / blog post / page (완제품)
  │     (actor / audiolog / distributor / webpage)
  │
  └─→ 제2계층 모듈 MCP → Thought Module (사고 모듈)
        (mcp-parksy-module-gallery)
              │
              ↓
        OrbitPrompt Gallery (index.html MODULES)
```

---

## 설계 원칙

1. **제1계층 MCP는 이 레포 밖에 있다.** 각자의 인프라와 저장소에서 독립 운영.
2. **제2계층 MCP는 이 레포 위성이다.** 오직 갤러리에 모듈을 공급하는 역할.
3. **로그는 유일한 원자재다.** 모든 MCP는 같은 ParksyLog 캡처를 입력으로 받는다.
4. **갤러리는 전시장이다.** 모듈 MCP가 등록한 artifact를 배열하여 전시.
