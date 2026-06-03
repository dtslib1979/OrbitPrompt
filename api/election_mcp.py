"""
election_mcp.py — parksy-election-mcp v2.0
박씨 F=ma 정치 변화력 모델 + LLM 리서치 에이전트
배포: stdio → python election_mcp.py
      http  → PORT=8000 python election_mcp.py
"""
from __future__ import annotations
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
import json, os, math, pathlib, httpx, statistics

# ── 경로 & config ────────────────────────────────────────────────────────
ROOT = pathlib.Path(__file__).resolve().parent.parent

def _load(p):
    return json.loads(p.read_text(encoding="utf-8"))

HEROES  = _load(ROOT / "config/hero_archetypes.json")
WEIGHTS = _load(ROOT / "config/weights_default.json")
FRMCF   = _load(ROOT / "config/frame_rules.json")
FRAMES  = [f["id"] for f in FRMCF["frames"]]
FIX     = ROOT / "data/fixtures"
PRMT    = ROOT / "prompts/election"

mcp = FastMCP("parksy-election-mcp")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MATH CORE — 결정론적, LLM 불필요
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calc_F(m, k, g, d, i, o,
           alpha=None, beta=None, gamma=None, delta=None):
    """F = m_eff * a  |  a = α·g + β·d + γ·i + δ·o  |  α+β+γ+δ=1.0"""
    w = WEIGHTS
    α,β,γ,δ = (alpha or w["alpha"]), (beta or w["beta"]), (gamma or w["gamma"]), (delta or w["delta"])
    m_eff = m * k
    a = α*g + β*d + γ*i + δ*o
    return {"m_eff": round(m_eff, 4), "a": round(a, 4), "F": round(m_eff * a, 4)}

def overthrow(F, R):
    """전복조건 부등식: F > R"""
    margin = round(F - R, 4)
    ratio = round(F / R, 3) if R > 0 else float("inf")
    return {
        "margin": margin,
        "ratio": ratio,
        "verdict": "전복가능" if margin > 0 else "체제유지"
    }

def knockout_score(chal_F, champ_F, champ_R):
    """3-B 선거 예측 엔진"""
    res = champ_R * 0.6 + champ_F * 0.4
    net = chal_F - res
    perc = abs(net) / 1.9
    ko = min(100.0, (perc / 30) * 70 + max(0.0, net) * 0.8)
    th = WEIGHTS["knockout_thresholds"]
    if perc < th["weak_signal"]:
        cls = "weak_signal"
    elif perc < th["visible_but_contestable"]:
        cls = "visible_but_contestable"
    elif perc < th["clear_change"]:
        cls = "clear_change"
    else:
        cls = "knockout_frame_shift"
    return {
        "resilience": round(res, 4),
        "net_edge": round(net, 4),
        "perceived": round(perc, 4),
        "ko_prob": round(ko, 2),
        "classification": cls
    }

def hero_score(scores):
    """5축 → 유클리드 거리로 아키타입 매핑"""
    keys = ["천민출신도", "자본주의솔루션도", "성과증명도", "대중동원력", "엘리트위협도"]
    wts = list(WEIGHTS["hero_score_weights"].values())
    vals = [scores.get(k, 0) for k in keys]
    refs = {
        "jesus":      [9, 2, 1, 4, 7],
        "lula":       [9, 8, 9, 9, 9],
        "ljm":        [8, 9, 8, 8, 9],
        "elite_left": [3, 4, 5, 6, 5],
        "populist":   [5, 3, 4, 9, 8],
    }
    dists = {k: round(math.sqrt(sum((a - b) ** 2 for a, b in zip(v, vals))), 2)
             for k, v in refs.items()}
    return {
        "total": round(sum(v * w for v, w in zip(vals, wts)), 2),
        "archetype": min(dists, key=lambda x: dists[x]),
        "distances": dists
    }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LLM LAYER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def llm_call(prompt, system, max_tokens=1500):
    """Anthropic API 직접 호출 — Haiku 4.5 (비용 최소화)"""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return json.dumps({"error": "ANTHROPIC_API_KEY 없음"})
    async with httpx.AsyncClient(timeout=90) as c:
        r = await c.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": max_tokens,
                "system": system,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
    data = r.json()
    if r.status_code == 200:
        return data["content"][0]["text"]
    return json.dumps({"error": f"API {r.status_code}"})

def _prompt(name):
    """prompts/election/*.md 로드 — 없으면 빈 문자열 (인라인 폴백 사용)"""
    p = PRMT / f"{name}.md"
    if p.exists():
        return p.read_text(encoding="utf-8")
    return ""

def _safe_json(raw):
    raw = raw.strip()
    for wrap in ["```json", "```"]:
        if wrap in raw:
            raw = raw.split(wrap, 1)[-1].rsplit("```", 1)[0]
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {"raw": raw, "parse_error": True}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MCP TOOLS — P0 (결정론적, LLM 불필요)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ParamsModel(BaseModel):
    hero:    str             = Field("custom")
    m_base:  Optional[float] = Field(None, ge=0, le=1)
    k_media: Optional[float] = Field(None, ge=0, le=1)
    g: float = Field(..., ge=0, le=10)
    d: float = Field(..., ge=0, le=10)
    i: float = Field(..., ge=0, le=10)
    o: float = Field(..., ge=0, le=10)
    R: float = Field(..., ge=0, le=10)

@mcp.tool(name="calc_political_force", annotations={"readOnlyHint": True})
async def calc_political_force(p: ParamsModel) -> str:
    """[P0] F=ma 정치변화력 계산 + 전복조건 판정 (결정론적)"""
    arch = HEROES.get(p.hero, HEROES["custom"])
    m = p.m_base  if p.m_base  is not None else arch["m_base"]
    k = p.k_media if p.k_media is not None else arch["k_media"]
    res = calc_F(m, k, p.g, p.d, p.i, p.o)
    ot = overthrow(res["F"], p.R)
    return json.dumps({
        "hero": p.hero,
        "archetype_note": arch["note"],
        "inputs": {"m": m, "k": k, "g": p.g, "d": p.d, "i": p.i, "o": p.o, "R": p.R},
        "model": res,
        "overthrow": ot
    }, ensure_ascii=False, indent=2)

@mcp.tool(name="compare_heroes", annotations={"readOnlyHint": True})
async def compare_heroes(cases: list) -> str:
    """[P0] 여러 케이스 F=ma 병렬 비교 + knockout_score 자동 계산"""
    results = []
    for c in cases:
        arch = HEROES.get(c.get("hero", "custom"), HEROES["custom"])
        res = calc_F(
            c.get("m_base", arch["m_base"]),
            c.get("k_media", arch["k_media"]),
            c["g"], c["d"], c["i"], c["o"]
        )
        ot = overthrow(res["F"], c["R"])
        results.append({
            "name": c["name"], "hero": c.get("hero", "custom"),
            "F": res["F"], "m_eff": res["m_eff"], "a": res["a"],
            "R": c["R"], "verdict": ot["verdict"], "ratio": ot["ratio"]
        })
    results.sort(key=lambda x: x["F"], reverse=True)
    summary = {}
    if len(results) >= 2:
        ko = knockout_score(results[1]["F"], results[0]["F"], results[0]["R"])
        summary = {
            "champion": results[0]["name"],
            "challenger": results[1]["name"],
            "knockout": ko
        }
    return json.dumps({"ranking": results, "summary": summary}, ensure_ascii=False, indent=2)

# ── P1 (LLM 연동) ────────────────────────────────────────────────────────

@mcp.tool(name="research_election", annotations={"readOnlyHint": True})
async def research_election(region: str, candidates: list, model_params: Optional[dict] = None) -> str:
    """[P1] LLM 서브에이전트: 리서치→파라미터 추정→Python F 재계산→당선 예측"""
    sys_p = _prompt("research") or """너는 박씨의 정치 분석 에이전트다.
F=ma 모델: m_eff=m_base*k_media, a=0.3·g+0.3·d+0.2·i+0.2·o, 전복조건 F>R
각 후보 g/d/i/o/R(0~10), m_base/k_media(0~1) 추정. JSON만:
{"region":"","context_summary":"2줄","candidates":[{"name":"","party":"",
"g":0,"d":0,"i":0,"o":0,"R":0,"m_base":1.0,"k_media":0.5,
"win_prob":0,"rationale":"1줄"}],
"key_variable":"핵심변수","risk_factor":"역전조건"}"""
    raw = await llm_call(
        f"선거구:{region}\n후보:{json.dumps(candidates, ensure_ascii=False)}\n힌트:{json.dumps(model_params or {}, ensure_ascii=False)}",
        sys_p, 2000
    )
    data = _safe_json(raw)
    if isinstance(data, dict) and not data.get("parse_error"):
        ranked = []
        for c in data.get("candidates", []):
            res = calc_F(
                c.get("m_base", 1.0), c.get("k_media", 0.5),
                c.get("g", 5), c.get("d", 5), c.get("i", 5), c.get("o", 5)
            )
            ranked.append({**c, "F_verified": res["F"],
                          "overthrow": overthrow(res["F"], c.get("R", 5))})
        ranked.sort(key=lambda x: x["F_verified"], reverse=True)
        data["candidates"] = ranked
        data["predicted_winner"] = ranked[0]["name"] if ranked else "미확인"
        if len(ranked) >= 2:
            data["knockout"] = knockout_score(
                ranked[1]["F_verified"], ranked[0]["F_verified"],
                ranked[0].get("R", 5)
            )
    return json.dumps(data, ensure_ascii=False, indent=2)

@mcp.tool(name="tag_political_frame", annotations={"readOnlyHint": True})
async def tag_political_frame(text: str, context: str = "") -> str:
    """[P1] 텍스트 → 박씨 6종 프레임 0~10 점수 태깅"""
    sys_p = _prompt("frame") or f"""박씨 6종 프레임 분석:{json.dumps(FRAMES, ensure_ascii=False)}
0~10 점수+주 프레임+2줄 해설. JSON만:
{{"scores":{{"리더십강화":0,"국정무능심판":0,"정권안정선택":0,
           "지역인물선거":0,"개헌구조개혁연계":0,"엘리트레거시":0}},
 "dominant":"","runner_up":"","comment":""}}"""
    payload = text
    if context:
        payload += f"\n맥락:{context}"
    raw = await llm_call(payload, sys_p)
    return json.dumps(_safe_json(raw), ensure_ascii=False, indent=2)

@mcp.tool(name="classify_hero_type", annotations={"readOnlyHint": True})
async def classify_hero_type(name: str, background: str) -> str:
    """[P1] 인물 → 5축 히어로 분류 + 유클리드 거리 아키타입 매핑"""
    sys_p = _prompt("classify") or """5축(0~10): 천민출신도/자본주의솔루션도/성과증명도/대중동원력/엘리트위협도
JSON만: {"scores":{"천민출신도":0,"자본주의솔루션도":0,"성과증명도":0,
        "대중동원력":0,"엘리트위협도":0},"summary":"1줄"}"""
    raw = await llm_call(f"이름:{name}\n배경:{background}", sys_p)
    data = _safe_json(raw)
    if isinstance(data, dict) and "scores" in data:
        data["archetype_calc"] = hero_score(data["scores"])
    return json.dumps(data, ensure_ascii=False, indent=2)

# ── P2 (방송/시나리오) ────────────────────────────────────────────────────

@mcp.tool(name="scenario_analysis", annotations={"readOnlyHint": True})
async def scenario_analysis(election: str, winner: str, context: str = "") -> str:
    """[P2] 당선 시나리오 → 천민공화주의 vs 엘리트레거시 축 재편 분석"""
    sys_p = _prompt("scenario") or """박씨 세계관: 천민출신자본주의공화주의(이재명) vs 86엘리트레거시(조국)
허드+귀족챔피언전 구조. F=ma: 당선→F증가 or R감소.
JSON만: {"winner":"","axis_shift":"천민공화주의강화|엘리트레거시복귀|중립",
"F_change":"","R_change":"","lj_impact":"","next_battleground":"","parksy_comment":"2줄"}"""
    payload = f"선거:{election}\n당선:{winner}\n맥락:{context or '없음'}"
    raw = await llm_call(payload, sys_p)
    return json.dumps(_safe_json(raw), ensure_ascii=False, indent=2)

@mcp.tool(name="generate_broadcast_script", annotations={"readOnlyHint": True})
async def generate_broadcast_script(topic: str, key_results: Optional[list] = None,
                                      style: str = "김어준식_메타") -> str:
    """[P2] F=ma+6종프레임 실시간 방송 스크립트 생성"""
    sys_p = _prompt("broadcast") or f"""박씨 방송 스타일({style}). 권력비틀기+구조론+F=ma계급모델.
JSON만: {{"opening":"","key_points":[""],"region_template":"","closing":"","parksy_tag":"핵심한줄"}}"""
    payload = f"주제:{topic}\n결과:{json.dumps(key_results or [], ensure_ascii=False)}"
    raw = await llm_call(payload, sys_p, 2000)
    return json.dumps(_safe_json(raw), ensure_ascii=False, indent=2)

# ── P3 (검증) ────────────────────────────────────────────────────────────

@mcp.tool(name="validate_fixtures", annotations={"readOnlyHint": True})
async def validate_fixtures() -> str:
    """[P3] data/fixtures/*.json → 모델 예측 vs 실제 대조"""
    results = []
    if not FIX.exists():
        return json.dumps({"error": "data/fixtures/ 없음 — Phase 3부터 활성화"})
    for fp in sorted(FIX.glob("*.json")):
        fx = _load(fp)
        cands = fx.get("candidates", [])
        scored = []
        for c in cands:
            p = c["params"]
            res = calc_F(p["m_base"], p["k_media"], p["g"], p["d"], p["i"], p["o"])
            scored.append({
                "name": c["name"],
                "expected": c.get("expected_winner", False),
                "F": res["F"]
            })
        scored.sort(key=lambda x: x["F"], reverse=True)
        pw = scored[0]["name"]
        aw = next((c["name"] for c in cands if c.get("expected_winner")), None)
        meta = fx.get("_meta", {})
        ko = knockout_score(scored[1]["F"], scored[0]["F"], cands[0]["params"]["R"]) if len(scored) >= 2 else {}
        results.append({
            "region": meta.get("region", fp.stem),
            "predicted": pw, "actual": aw,
            "direction_ok": pw == aw,
            "classification": ko.get("classification"),
            "expected_cls": fx.get("expected_classification"),
            "cls_match": ko.get("classification") == fx.get("expected_classification")
        })
    if not results:
        return json.dumps({"error": "fixtures 없음"})
    d_acc = sum(1 for r in results if r["direction_ok"]) / max(len(results), 1)
    c_acc = sum(1 for r in results if r["cls_match"]) / max(len(results), 1)
    return json.dumps({
        "summary": {
            "total": len(results),
            "direction_acc": round(d_acc, 3),
            "cls_acc": round(c_acc, 3)
        },
        "details": results
    }, ensure_ascii=False, indent=2)

@mcp.tool(name="reproducibility_test", annotations={"readOnlyHint": True})
async def reproducibility_test(region: str, candidates: list, n_runs: int = 3) -> str:
    """[P3] 동일 선거구 n회 LLM 호출 → 파라미터 표준편차. 불안정 변수 탐지"""
    runs = []
    sys_p = """각 후보 g,d,i,o,R(0~10),m_base,k_media(0~1) 추정. JSON만:
{"candidates":[{"name":"","g":0,"d":0,"i":0,"o":0,"R":0,"m_base":1.0,"k_media":0.5}]}"""
    for _ in range(max(1, min(n_runs, 5))):
        d = _safe_json(await llm_call(
            f"선거구:{region}\n후보:{json.dumps(candidates, ensure_ascii=False)}", sys_p
        ))
        if isinstance(d, dict) and not d.get("parse_error"):
            runs.append(d.get("candidates", []))
    if not runs:
        return json.dumps({"error": "LLM 응답 없음"})
    keys = ["g", "d", "i", "o", "R", "m_base", "k_media"]
    analysis = {}
    for cn in candidates:
        cn_name = cn if isinstance(cn, str) else ""
        ps = {k: [] for k in keys}
        for run in runs:
            m = next((c for c in run if c.get("name") == cn_name), None)
            if m:
                for k in keys:
                    if k in m:
                        ps[k].append(m[k])
        sd = {}
        for k, v in ps.items():
            if len(v) > 1:
                sd[k] = round(statistics.stdev(v), 2)
            else:
                sd[k] = None
        analysis[cn_name] = {
            "stdev": sd,
            "unstable_vars": [k for k, v in sd.items() if v and v > 10]
        }
    verdict = "안정"
    for v in analysis.values():
        if v["unstable_vars"]:
            verdict = "불안정—수동보정필요"
            break
    return json.dumps({
        "n_runs": len(runs),
        "analysis": analysis,
        "verdict": verdict
    }, ensure_ascii=False, indent=2)

# ── ENTRYPOINT ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 0))
    kwargs = {}
    if port:
        kwargs = {"host": "0.0.0.0", "port": port}
    mcp.run(
        transport="streamable-http" if port else "stdio",
        **kwargs
    )
