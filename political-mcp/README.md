# OrbitPrompt Political MCP

**Φ-I-C-K-P-7AXIS Political Intelligence** — 시민이 만든 AI 정치 인프라

> "시민이 AI로 정치 인프라를 만들고, 정치인이 그 인프라를 쓴다."

---

## 뭐가 다른가

| 기존 AI 정치 도구 | 이 MCP |
|---|---|
| AI를 정치 설득 도구로 | 시민이 AI로 인프라 제작 |
| 캠프 전문가가 운영 | `server.py` 실행하면 누구든 사용 |
| 타겟 광고·챗봇 | Φ드라이버 7축 철학 기반 분석 |

---

## 설치 & 실행

```bash
git clone https://github.com/dtslib1979/orbitprompt-political-mcp
cd orbitprompt-political-mcp
python3 server.py
```

Python 3.8+ 외 의존성 없음.

---

## 툴 4개

### analyze_politician — Φ드라이버 7축 해부
```bash
echo '{"tool":"analyze_politician","params":{"name":"박찬대"}}' | python3 server.py
```
```json
{
  "phi12_strength": 70.8,
  "axes_analysis": {
    "meta":     "발언 일관성 72/100",
    "reverse":  "위기 대응 68/100",
    "modular":  "정책 패턴 75/100",
    "language": "수사력 80/100",
    "zoom":     "의제 집중 70/100",
    "spiral":   "성장 궤적 74/100",
    "quantum":  "이변 가능성 55/100"
  }
}
```

### compare_policy — 두 정치인 Φ 비교
```bash
echo '{"tool":"compare_policy","params":{"politician_a":"박찬대","politician_b":"이재명"}}' | python3 server.py
```

### simulate_election — 시나리오 시뮬레이션
```bash
echo '{"tool":"simulate_election","params":{"candidate":"박찬대","region":"인천 연수구을"}}' | python3 server.py
```

### rank_politicians — 전체 Φ12 랭킹
```bash
echo '{"tool":"rank_politicians","params":{}}' | python3 server.py
```
```
1위 이재명  Φ12: 77.9
2위 박찬대  Φ12: 70.8
3위 조국    Φ12: 57.0
4위 한동훈  Φ12: 47.7
```

---

## Φ드라이버 7축 (정치 버전)

| 축 | 의미 | 가중치 |
|---|---|---|
| Meta | 발언 일관성 — 공약 vs 실제 행동 | 1.2 |
| Reverse | 위기 대응 — 역풍 후 회복력 | 1.1 |
| Modular | 정책 패턴 — 반복 가능한 공식 | 1.0 |
| Language | 수사력 — 프레이밍·언어 장악 | 1.0 |
| Zoom | 의제 집중 — 핵심 이슈 관통 | 1.2 |
| Spiral | 성장 궤적 — 선수 거듭할수록 강해지나 | 1.3 |
| Quantum | 이변 가능성 — 판세 뒤집는 변수 | 1.5 |

같은 Φ드라이버 구조가 [축구 WC2026 MCP](../football-model/mcp/)에도 적용됨.

---

## 슬롯 구조 — 박찬대가 아니어도 된다

```
박찬대 = Episode 02 샘플 슬롯
이름/도시/의제 교체하면 누구든 분석 가능
```

`politician_data.py`에 정치인 데이터 추가하면 바로 확장.

---

## 설계 철학

- [Φ드라이버 7축](../docs/TRIANGULAR-STAFF-METHOD.md)
- [삼각 실행 루프 방법론](../docs/TRIANGULAR-STAFF-METHOD.md)
- 박찬대 되기 프로젝트 (Episode 02)

---

Built with [OrbitPrompt](https://dtslib1979.github.io/OrbitPrompt/) — Citizen AI Infrastructure
