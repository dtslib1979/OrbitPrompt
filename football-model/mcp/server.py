#!/usr/bin/env python3
"""
server.py — Φ-I-C-K-P-7AXIS MCP Server (stdio protocol)

Claude가 직접 툴로 호출 가능:
  predict_korea_japan
  compare_models
  team_philosophy
  generate_script
  run_simulation
"""
import sys, json, os, asyncio
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from model import predict_win_prob, predict_with_baseline, calc_phi_12, content_script, calc_phi7

# ─── MCP stdio protocol ─────────────────────────────
async def main():
    request = json.loads(sys.stdin.read())
    tool = request.get("tool", "")
    params = request.get("params", {})
    
    if tool == "predict":
        r = predict_win_prob(params.get("team_a", ""), params.get("team_b", ""))
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "compare":
        r = predict_with_baseline(params.get("team_a", ""), params.get("team_b", ""))
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "philosophy":
        team = params.get("team", "")
        profile = calc_phi_12(team)
        profile["phi7_descriptions"] = {
            "meta": "자기 스타일 인식 — 이 팀은 자신의 강점을 아는가",
            "reverse": "약점 보완 — 약점을 어떻게 숨기거나 보완하는가",
            "modular": "전술 패턴 — 반복 가능한 전술이 있는가",
            "lang": "정체성 — 팀의 축구 철학이 뚜렷한가",
            "zoom": "빅매치 — 결정적 순간에 집중하는가",
            "spiral": "성장 곡선 — 대회 기간 동안 발전하는가",
            "quantum": "이변 가능성 — 예측 불가능한 변수를 가졌는가"
        }
        print(json.dumps(profile, ensure_ascii=False))
    
    elif tool == "script":
        r = predict_with_baseline(params.get("team_a", ""), params.get("team_b", ""))
        script = content_script(r)
        print(json.dumps({"script": script}, ensure_ascii=False))
    
    elif tool == "rank":
        from team_data import TEAMS
        sr = sorted(TEAMS.keys(), key=lambda n: calc_phi_12(n)["phi12_strength"], reverse=True)
        result = []
        for n in sr:
            r = calc_phi_12(n)
            result.append({"rank": len(result)+1, "team": n, "phi12": r["phi12_strength"], "phi5": r["phi5_strength"], "phi7": r["phi7_strength"]})
        print(json.dumps(result, ensure_ascii=False))
    
    else:
        print(json.dumps({
            "tools": ["predict", "compare", "philosophy", "script", "rank"],
            "usage": {
                "predict": {"team_a": "Korea", "team_b": "Japan"},
                "compare": {"team_a": "Korea", "team_b": "Japan"},
                "philosophy": {"team": "Brazil"},
                "script": {"team_a": "Korea", "team_b": "Japan"},
                "rank": {}
            }
        }, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
