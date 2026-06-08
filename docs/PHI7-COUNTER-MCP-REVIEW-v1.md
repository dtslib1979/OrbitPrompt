# Φ7 철학 카운터 MCP — 형 리뷰 (DeepSeek 작업용)

> 작성: Claude (형/관제탑) — 2026-06-08
> 대상: `OrbitPrompt/philosophy-counter/mcp/` v1.0
> 목적: 동생이 이 문서 읽고 바로 수정 착수

---

## 현재 점수: 65점 → 목표: 100점

---

## 수정 사항 4개 — 우선순위 순서

---

### [1순위] MCP 프로토콜 교체 — Claude 등록 가능하게

**문제:**
현재 server.py는 `json.loads(sys.stdin.read())` 방식이다.
이건 CLI 툴이다. Claude.json에 등록하면 작동 안 한다.

**정치 MCP 패턴과 비교:**
```python
# 현재 (틀림)
raw = sys.stdin.read().strip()
req = json.loads(raw)
tool = req.get("tool", "")

# 맞는 방식 (OrbitPrompt/political-mcp/server.py 참조)
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    request = json.loads(line)
    response = handle_request(request)
    print(json.dumps(response))
    sys.stdout.flush()
```

**수정 파일:** `server.py`
**참조:** `OrbitPrompt/political-mcp/server.py` — 그 구조 그대로 따라라

---

### [2순위] 유사도 공식 버그 수정

**문제:**
```python
# 현재 (버그)
overall_similarity = round(100 - abs(avg_p - avg_m) * 1.5, 1)
```
이건 점수 차이 기반이라 완전히 다른 두 사람이 유사도 100% 나올 수 있다.

`calc_similarity` 함수가 이미 있는데 dead code다. 이걸 써야 한다.

**수정 방향:**
```python
# phi7_engine.py에서 overall_similarity 계산 부분

# 각 차원별로 공통 특징 / 전체 특징으로 자카드 계산
def calc_overall_similarity(p_features, parksy_features):
    all_p = []
    all_m = []
    for dim in PHI7_DIMENSIONS:
        all_p.extend(p_features.get(dim, []))
        all_m.extend(parksy_features.get(dim, []))
    return calc_similarity(all_p, all_m)  # 이미 있는 함수 쓴다

# analyze_philosopher 안에서:
overall_similarity = calc_overall_similarity(p_feats, PARKSY_FEATURES)
```

**수정 파일:** `phi7_engine.py` — `analyze_philosopher` 함수 내 `overall_similarity` 계산 부분

---

### [3순위] 5축 → Φ7 축 정렬

**문제:**
파일 이름은 `phi7_engine.py`인데 실제 차원은 5개다:
```
현재: structure / identity / medium / class / endpoint
Φ7:  Meta / Reverse / Modular / Language / Zoom / Spiral / Quantum
```

갤러리 Φ7과 이 MCP의 내부 구조가 다른 것을 쓰고 있다.

**수정 방향:**
`philosopher_data.py`의 `PHI7_DIMENSIONS`를 아래로 교체:

```python
PHI7_DIMENSIONS = {
    "meta": {
        "name": "🧠 Meta",
        "desc": "전체를 보는 눈 — 방법론, 자기인식, 체계 설계",
        "features": ["체계_설계", "방법론_중시", "자기인식", "메타분석", "구조_중시", "관계_중시"]
    },
    "reverse": {
        "name": "🔄 Reverse",
        "desc": "거꾸로 읽기 — 역방향 설계, 실패분석",
        "features": ["역방향_설계", "실패분석", "케이스스터디", "비판_중심", "해체_중심"]
    },
    "modular": {
        "name": "🧩 Modular",
        "desc": "조립하기 — 재사용 가능한 도구, 시스템 설계",
        "features": ["도구_제작", "시스템_설계", "재사용_중시", "실행_중심", "모듈화"]
    },
    "language": {
        "name": "💬 Language",
        "desc": "언어로 마감 — 프레이밍, 내러티브",
        "features": ["언어게임", "프레이밍", "개념_제안", "책_중심", "담론_분석"]
    },
    "zoom": {
        "name": "🔍 Zoom",
        "desc": "스케일 조절 — 개인→도시→국가",
        "features": ["계급_분석", "권력_분석", "사회구조", "위계_인정", "스케일_전환"]
    },
    "spiral": {
        "name": "📈 Spiral",
        "desc": "반복 상승 — 성장 궤적, 발전",
        "features": ["변증법", "발전_중시", "반복_상승", "역사_중시", "자기극복"]
    },
    "quantum": {
        "name": "⚡ Quantum",
        "desc": "도약 — 예측, 시뮬레이션, 이변",
        "features": ["도약_중심", "예측_중시", "자동화_중심", "인프라_중심", "구축_중심"]
    }
}
```

그리고 `PARKSY_FEATURES`도 같이 교체:
```python
PARKSY_FEATURES = {
    "meta":     ["체계_설계", "방법론_중시", "자기인식", "구조_중시"],
    "reverse":  ["역방향_설계", "실패분석", "케이스스터디"],
    "modular":  ["도구_제작", "시스템_설계", "재사용_중시", "실행_중심"],
    "language": ["프레이밍", "개념_제안"],
    "zoom":     ["계급_분석", "권력_분석", "스케일_전환"],
    "spiral":   ["반복_상승", "자기극복"],
    "quantum":  ["자동화_중심", "인프라_중심", "구축_중심", "도약_중심"]
}
```

철학자 11명 데이터도 이 7축 기준으로 `features` 다시 매핑.

**수정 파일:** `philosopher_data.py` 전체 재작성

---

### [4순위] 갤러리 카드 추가

**문제:**
server.py 만들었는데 index.html MODULES에 카드가 없다.

**수정 위치:** `OrbitPrompt/index.html` — MODULES 배열 안에 추가

```javascript
{
  category: 'Meta',
  id: 'phi7-counter',
  icon: '🧠',
  domain: '철학',
  number: '07',
  title: 'Φ7 철학 카운터 MCP',
  desc: '11명 철학자 vs 박씨 — Φ7 7축 동적 유사도 분석. discover/rank/map/counter 툴.',
  tags: ['Φ7', '자카드 유사도', '11명 철학자', 'ID 엔진'],
  score: 65,
  maxScore: 100,
  status: 'live',
  path: 'philosophy-counter/mcp/server.py',
},
```

---

## 수정 순서

```
1. server.py — MCP 프로토콜 교체 (political-mcp/server.py 패턴)
2. phi7_engine.py — overall_similarity 공식 수정
3. philosopher_data.py — 5축 → Φ7 7축 전체 재작성
4. index.html — 갤러리 카드 추가
5. 실행 테스트: echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"rank"},"id":1}' | python3 server.py
6. git add + commit + push
```

---

## 수정 후 예상 점수

| 항목 | 현재 | 수정 후 |
|------|------|---------|
| MCP 프로토콜 | ❌ | ✅ |
| 유사도 공식 | ❌ | ✅ |
| Φ7 축 정렬 | ❌ | ✅ |
| 갤러리 연결 | ❌ | ✅ |
| 코드 구조 | ✅ | ✅ |
| 동적 계산 | ✅ | ✅ |
| **총점** | **65** | **100** |

---

*작성: Claude — 형 리뷰. 동생 읽고 바로 착수.*
*참조: OrbitPrompt/political-mcp/server.py (MCP 프로토콜 레퍼런스)*
