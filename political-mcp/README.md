# Φ-I-C-K-P-7AXIS Political MCP v1.0

> 시민이 AI로 정치 인프라를 만들고, 정치인이 그 인프라를 쓰는 모델.

## Quick Start

```bash
cd political-mcp/

# 정치인 분석
echo '{"tool":"analyze_politician","params":{"name":"박찬대"}}' | python3 server.py

# 두 정치인 비교
echo '{"tool":"compare_policy","params":{"politician_a":"박찬대","politician_b":"이재명"}}' | python3 server.py

# 선거 시뮬레이션
echo '{"tool":"simulate_election","params":{"candidate":"박찬대","region":"인천 연수구을"}}' | python3 server.py

# 전체 순위
echo '{"tool":"rank_politicians","params":{}}' | python3 server.py

# 메타: 방법론
echo '{"tool":"orchestrate","params":{}}' | python3 server.py
```

## Tools

| Tool | Function | Example |
|------|----------|---------|
| `analyze_politician` | 7축 Φ드라이버 분석 | 박찬대: Φ12 80.9 / 등급 S |
| `compare_policy` | 두 정치인 Φ12 비교 | 박찬대 vs 이재명 축별 gap |
| `simulate_election` | 3개 시나리오 시뮬레이션 | 현상유지/역풍/기회 |
| `rank_politicians` | 전체 순위 (1위 이재명) | Φ12 + 등급 + 강/약축 |

## Politicians

| Name | Party | Φ12 | Grade |
|------|-------|-----|-------|
| 이재명 | 더불어민주당 | 88.6 | S |
| 박찬대 | 더불어민주당 | 80.9 | S |
| 조국 | 조국혁신당 | 65.7 | A |
| 한동훈 | 국민의힘 | 56.6 | B |

## Architecture

```
OrbitPrompt (Φ드라이버 철학)
  ↓ 포팅
political-mcp/ (정치인 7축 분석)
  ↓ 배포
GitHub 공개 → 역방향 유통 → 보좌관이 찾아옴
```

## License

Open Source. Φ-I-C-K-P-7AXIS — OrbitPrompt 철학의 정치 버전.
