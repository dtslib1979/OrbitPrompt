#!/usr/bin/env python3
"""
server.py — OrbitPrompt Political MCP (JSON-RPC stdio)
tools: analyze_politician / compare_policy / simulate_election / rank_politicians
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from political_model import analyze_politician, compare_policy, simulate_election, calc_phi12
from politician_data import POLITICIANS

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "no input"})); return

    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON parse error: {e}"})); return

    tool   = req.get("tool", "")
    params = req.get("params", {})

    if tool == "analyze_politician":
        name = params.get("name", "")
        print(json.dumps(analyze_politician(name), ensure_ascii=False, indent=2))

    elif tool == "compare_policy":
        a = params.get("politician_a", "")
        b = params.get("politician_b", "")
        print(json.dumps(compare_policy(a, b), ensure_ascii=False, indent=2))

    elif tool == "simulate_election":
        candidate = params.get("candidate", "")
        region    = params.get("region", None)
        print(json.dumps(simulate_election(candidate, region), ensure_ascii=False, indent=2))

    elif tool == "rank_politicians":
        ranked = sorted(POLITICIANS.keys(),
                        key=lambda n: calc_phi12(n)["phi12_strength"], reverse=True)
        result = []
        for i, n in enumerate(ranked):
            r = calc_phi12(n)
            result.append({
                "rank": i + 1,
                "name": n,
                "party": POLITICIANS[n]["party"],
                "phi12": r["phi12_strength"],
                "phi5":  r["phi5_strength"],
                "phi7":  r["phi7_strength"],
            })
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(json.dumps({
            "tools": ["analyze_politician", "compare_policy", "simulate_election", "rank_politicians"],
            "usage": {
                "analyze_politician": {"name": "박찬대"},
                "compare_policy":     {"politician_a": "박찬대", "politician_b": "이재명"},
                "simulate_election":  {"candidate": "박찬대", "region": "인천 연수구을"},
                "rank_politicians":   {},
            }
        }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
