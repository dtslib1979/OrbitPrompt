# ENDPOINT — OrbitPrompt 선형 판단 모델

> **버전**: v0.1 (2026-06-07)
> **철학**: Capture → Classify → Judge → Archive → Publish
> **통합**: parksy-logs(11,695개) + eae-univ + OrbitPrompt + dtslib-branch

---

## 1. 왜 ENDPOINT인가

OrbitPrompt는 지금까지 **철학(PHL/7축)과 실행(MCP/PD)** 사이에 **판단 모델**이 없었다.

| 있었다 | 없었다 |
|--------|--------|
| "왜" (7축 철학) | **"어떻게 판단할지" (선형 모델)** |
| "무엇을" (PHL 프로토콜) | **"무엇을 남기고 버릴지" (필터)** |
| "누가" (PD 시스템) | **"무엇을 어디로 보낼지" (라우팅)** |

ENDPOINT는 이 빈칸을 채운다.

---

## 2. 5단계 선형 모델

```
[CAPTURE] parksy-logs/parksy-capture
    → 박씨의 모든 입력이 쌓이는 원천
    → 11,695개 로그, 2025-12~2026-06
    → MP4, 이미지, 텍스트, 음성 메모
    │
    ▼
[CLASSIFY] LLM/7축 분석
    → 입력 유형 분류 (아이디어/결정/지식/잡음)
    → 7축 렌즈로 사고 패턴 추출
    → 중요도/긴급도 태깅 (P0~P3)
    │
    ▼
[JUDGE] ENDPOINT 판단
    → 이 입력을: 실행 / 보류 / 아카이브 / 폐기
    → 대중 레인 / 귀족 레인 분기
    → 인간 승인 필요 여부 판단
    │
    ▼
[ARCHIVE] brain_delta / finetune
    → 선발된 지식은 eae-univ로 (지식화)
    → 보류된 아이디어는 brain_delta로 (재검토 대기)
    → 실행 로그는 parksy-logs events/로 (감사)
    │
    ▼
[PUBLISH] dtslib-branch / YouTube
    → 비즈니스 소설 (FLD 백서)
    → 오복집 케이스 스터디
    → 가창 머신 결과물
    → 철학 백서
```

---

## 3. 레포지토리 통합 맵

```
parksy-logs (캡처/원천)
  ├── ParksyLog_*.md (11,695개)
  ├── events/ (구조화된 이벤트)
  ├── finetune/ (LLM 학습 데이터)
  ├── brain_delta/ (지식 변화 추적)
  └── session-logs/ (세션 기록)
       │
       │ ENDPOINT가 여기서 판단
       ▼
eae-univ (지식/교육)
  ├── broadcast/episodes/ (방송 콘텐츠)
  ├── courses/ (과정)
  └── DESIGN_BLUEPRINT.md (설계 청사진)
       │
       ▼
OrbitPrompt (철학/프로토콜)
  ├── PHL_SPEC.md (의미 압축 프로토콜)
  ├── philosophy.html (AI 철학 백서)
  ├── ENDPOINT.md (이 파일)
  └── CLAUDE.md (헌법)
       │
       ▼
dtslib-branch (출판/브랜치)
  ├── 비즈니스-소설/ (FLD 백서, 오복집)
  ├── philosophy/ (철학 웹페이지)
  └── index.html (랜딩 페이지)
```

---

## 4. 판단 매트릭스

| 입력 유형 | Judge 결과 | 경로 | 인간 승인 |
|-----------|-----------|------|:---------:|
| 아이디어/통찰 | eae-univ 지식화 | 지식 레인 | ✅ |
| 실행 결정 | PD 시스템 실행 | 실행 레인 | ✅ |
| 콘텐츠 원료 | dtslib-branch 출판 | 대중 레인 | ❌ (자동) |
| 잡음/중복 | brain_delta 보류 | 재검토 대기 | ❌ |
| 에러/실패 | events/ 감사 로그 | 아카이브 | ❌ |
| 철학/원칙 | OrbitPrompt 철학 수렴 | 귀족 레인 | ✅ |

---

## 5. 다음 단계

1. ENDPOINT.md를 OrbitPrompt 루트에 저장 ✅
2. parksy-logs brain_delta/ 와 연결 (capture→classify 자동화)
3. eae-univ broadcast/episodes 와 연결 (classify→publish)
4. PD 시스템에 ENDPOINT 참조 추가

---

## 5. 판단 매트릭스 (결정 테이블)

11개 규칙, if-elif 순서, 4개 충돌 해결 포함.

```json
// judge_rules.json — ENDPOINT JUDGE v0.1
{
  "priority_rules": [
    {"order": 1, "P0_keyword": "시작해/만들어/구현", "result": "P0"},
    {"order": 2, "P3_keyword": "나중에/검토/고려", "result": "P3"},
    {"order": 3, "DEFAULT": "any", "result": "P2"}
  ],
  "conflict_resolution": [
    "P0 AND P3 → P0 우선",
    "idea AND decision → decision 우선",
    "mass AND aristocrat → aristocrat 우선"
  ],
  "decision_table": [
    ["decision/P0/any   → execute/pd-system     ✅ 인간승인"],
    ["idea/P0/any       → execute/pd-system     ✅ 인간승인"],
    ["content/P0/mass   → execute/dtslib-branch ❌ 자동"],
    ["content/P0/arist  → execute/orbitprompt   ✅ 인간승인"],
    ["idea/P1/mass      → execute/eae-univ      ❌ 자동"],
    ["any/P2/mass       → execute/dtslib-branch ❌ 자동"],
    ["any/P2/arist      → hold/brain_delta      ❌ 보류"],
    ["any/P3/any        → hold/brain_delta      ❌ 보류"],
    ["noise/any/any     → discard/events        ❌ 폐기"]
  ]
}
```

실행:
```bash
python3 engine/endpoint_classifier.py "오복집 컨셉 검토"
# → idea/P3/aristocrat/hold/dtslib-branch

python3 engine/endpoint_classifier.py "쇼츠 하나 만들어"
# → decision/P0/mass/execute/pd-system
```
