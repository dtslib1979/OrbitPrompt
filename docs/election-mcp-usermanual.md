# PARKSY ELECTION MCP v2.0 — 사용 설명서

> **이 문서의 목적:** "MCP 서버를 어떻게 띄우고, 어떻게 연결하고, 어떻게 실제로 쓰는가"

---

## 1. 이 MCP로 무엇을 할 수 있나

### 박씨가 실제로 쓰는 시나리오 3가지

**시나리오 A — "이번 선거 왜 이렇게 됐냐"고 물을 때**

Claude Code(또는 Cursor)에서:
```
research_election("서울", ["오세훈", "권영세"])
```
→ LLM이 실시간 리서치 → g/d/i/o/R 추정 → Python F 계산 →   
"서울 R=7.5, 구조적 챔피언 우세. 도전자는 130% 필요."

**시나리오 B — "이재명 vs 한동훈 F 비교해봐"**

```
compare_heroes([{name:"이재명",hero:"ljm",g:7,d:8,i:6,o:5,R:7},
                {name:"한동훈",hero:"populist",g:6,d:5,i:5,o:6,R:7}])
```
→ F값 순위 + knockout 분석 출력

**시나리오 C — "이번 선거 특징이 뭐냐"**

```
delta_layer_info()
```
→ 12개 제약 조건 한 번에 출력.  
"이 선거는 도전자 130% 법칙 적용, 평택형 분열 리스크 있음."

---

## 2. MCP 서버 설치 및 실행

### 방법 1 — 로컬에서 직접 실행 (가장 간단)

```bash
# 1. SD 카드 또는 GitHub에서 복사
cd /mnt/e/mcp/election-mcp

# 2. 의존성 설치
pip install mcp httpx pydantic

# 3. 실행 (stdio 모드)
python3 server.py
```

### 방법 2 — HTTP 서버로 실행 (Railway 배포)

```bash
PORT=8000 python3 server.py
# → http://localhost:8000/mcp/sse
```

---

## 3. MCP 클라이언트에서 연결하기

### Claude Code에서 연결

`~/.claude.json`에 등록:

```json
{
  "mcpServers": {
    "parksy_election": {
      "command": "python3",
      "args": ["/mnt/e/mcp/election-mcp/server.py"]
    }
  }
}
```

이제 Claude Code에서 `/research_election` 또는 `/calc_political_force` 로 직접 호출 가능.

### Cursor / VS Code에서 연결

`~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "parksy_election": {
      "command": "python3",
      "args": ["/mnt/e/mcp/election-mcp/server.py"]
    }
  }
}
```

### MCP Inspector로 테스트

```bash
npx @anthropic/mcp-inspector python3 /mnt/e/mcp/election-mcp/server.py
```

---

## 4. 10개 도구 사용법 요약

### P0 — 결정론적 (LLM 불필요, 즉시 사용 가능)

| 도구 | 호출 예시 | 설명 |
|------|----------|------|
| `calc_political_force` | `{"p":{"hero":"ljm","g":7,"d":8,"i":6,"o":5,"R":7}}` | F=ma 계산 + 전복조건 |
| `compare_heroes` | `{"cases":[{name,hero,g,d,i,o,R},...]}` | 여러 인물 F값 비교 |
| `delta_layer_info` | `{}` | 12개 제약 조건 전체 출력 |

### P1 — LLM 필요 (ANTHROPIC_API_KEY)

| 도구 | 호출 예시 | 설명 |
|------|----------|------|
| `research_election` | `{"region":"부산","candidates":["전재수","박형준"]}` | LLM 리서치 → F 예측 |
| `tag_political_frame` | `{"text":"..."}` | 텍스트 → 6종 프레임 점수 |
| `classify_hero_type` | `{"name":"오세훈","background":"..."}` | 5축 히어로 분류 |

### P2 — 방송/시나리오

| 도구 | 설명 |
|------|------|
| `scenario_analysis` | 당선 시나리오 축 재편 분석 |
| `generate_broadcast_script` | 방송 스크립트 자동 생성 |

### P3 — 검증

| 도구 | 설명 |
|------|------|
| `validate_fixtures` | 8개 fixture 기반 direction_acc 측정 |
| `reproducibility_test` | LLM 추정 재현성 검증 |

---

## 5. 갤러리 페이지의 의미

갤러리 페이지(`boards/election-gallery.html`)는 **MCP의 출력 결과를 시각화한 전시물**이다.

| 갤러리가 하는 일 | 리포트인가? | 사용설명서인가? |
|----------------|------------|---------------|
| ✅ MCP 모델의 구조를 시각적으로 보여줌 | ✅ 검증 결과 리포트 | ✅ 사용 예시 포함 |

즉, 갤러리 페이지는:
- **검증 결과 보고서** (direction_acc 100% 증명)
- **사용 설명서** (3블록/130%법칙/델타레이어 개념 설명)
- **MCP 출력 예시** (히어로 랭킹, 지역별 F 비교)
- **뉴스 해석 도구** (박씨 분석 결과를 구조화해서 보여줌)

**박씨가 이 페이지를 보는 이유:**
```
1. "이번 선거 왜 이렇게 됐냐" → 갤러리 열면 구조적 해석 있음
2. "이 모델 신뢰할 만하냐" → direction_acc 100% 증명 있음
3. "MCP로 뭘 할 수 있냐" → 10개 도구 + 실행 명령 있음
4. "네 분석이 어떻게 구조화됐냐" → 12개 delta layer로 다 박혀 있음
```

---

## 6. 실제 워크플로우 예시

### 박씨의 아침 루틴 (가상)

```
1. 아침 뉴스에서 "오세훈 5선" 기사 봄
2. Claude Code 열고:
   calc_political_force(hero="oh_se_hoon", g=6, d=5, i=7, o=8, R=8)
   → "F=4.2, R=8, 체제유지 — 구조적 정상"
3. delta_layer_info() → 서울 structural_fixture 확인
   → "아, 서울 R=7.5라서 부정부패 있어도 버티는 구조구나"
4. 기사 댓글에 "서울은 준고정 구조. 도전자 130% 필요."
```

---

## 7. MCP 서버 상태 확인

```bash
# 서버 실행 중인지 확인
ps aux | grep server.py | grep -v grep

# tools/list 요청으로 도구 목록 확인
echo '{"jsonrpc":"2.0","id":1,"method":"initialize",
       "params":{"protocolVersion":"2024-11-05","capabilities":{},
                 "clientInfo":{"name":"test","version":"1.0"}}}' | python3 server.py
```

---

## 8. 빠른 시작 (3-step)

```bash
# Step 1: 서버 실행
cd /mnt/e/mcp/election-mcp && python3 server.py &

# Step 2: Claude Code에 등록
# ~/.claude.json에 추가

# Step 3: 사용
# "오세훈 F 계산해줘" 라고 말하면 MCP 호출
```

---

*서버: /mnt/e/mcp/election-mcp/server.py (385줄/10개 도구)*
*갤러리: https://dtslib1979.github.io/OrbitPrompt/boards/election-gallery.html*
*GitHub: OrbitPrompt/api/election_mcp.py*
