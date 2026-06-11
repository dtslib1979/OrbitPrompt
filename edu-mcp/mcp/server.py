#!/usr/bin/env python3
"""
server.py — Φ-I-C-K-P-7AXIS 교육 MCP 서버 (FastMCP)

툴:
  evaluate_education_system — K,C,I,O_t → E_g + PASS/FAIL + weak_axis
  recommend_pivot          — E_g,B_human → priority_axis + solution_set
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import calc_e, judge, recommend_pivot
from data import DEFAULT_B_HUMAN, DEFAULT_EPS, DEFAULT_DELTA

VERSION = "1.0.0"
MCP_NAME = "edu-mcp"

def handle(req):
    tool = req.get("tool", "")
    params = req.get("params", {})

    if tool == "evaluate_education_system":
        k = params.get("K", {})
        c = params.get("C", {})
        i = params.get("I", {})
        o_t = params.get("O_t", {})
        b_human = params.get("B_human", DEFAULT_B_HUMAN)
        eps = params.get("eps", DEFAULT_EPS)
        delta = params.get("delta", DEFAULT_DELTA)
        
        e_g = calc_e(k, c, i, o_t)
        result = judge(e_g, b_human, eps, delta)
        weak = min(e_g, key=e_g.get)
        
        return {
            "tool": "evaluate_education_system",
            "version": VERSION,
            "E_g": e_g,
            "judgment": result,
            "weak_axis": weak,
            "params_used": {"eps": eps, "delta": delta, "B_human": b_human}
        }

    elif tool == "recommend_pivot":
        e_g = params.get("E_g", {})
        b_human = params.get("B_human", DEFAULT_B_HUMAN)
        
        if not e_g:
            return {"error": "E_g required. Run evaluate_education_system first."}
        
        result = recommend_pivot(e_g, b_human)
        result["tool"] = "recommend_pivot"
        result["version"] = VERSION
        return result

    elif tool == "version":
        return {
            "name": MCP_NAME,
            "version": VERSION,
            "description": "Φ-I-C-K-P-7AXIS 교육 시스템 평가 MCP",
            "tools": ["evaluate_education_system", "recommend_pivot", "version"],
            "references": ["축구 MCP (football-model/mcp/) — Φ5+Φ7 구조 포팅"]
        }

    elif tool == "samples":
        from data import SAMPLE_KOREA, SAMPLE_IDEAL
        return {
            "tool": "samples",
            "version": VERSION,
            "samples": {
                "korea_2026": SAMPLE_KOREA,
                "ideal": SAMPLE_IDEAL,
                "default_B_human": DEFAULT_B_HUMAN
            }
        }

    else:
        return {
            "error": f"unknown tool '{tool}'",
            "tools": ["evaluate_education_system", "recommend_pivot", "samples", "version"]
        }

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        r = handle(json.loads(line))
        print(json.dumps(r, ensure_ascii=False))
        sys.stdout.flush()
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.stdout.flush()
