#!/usr/bin/env python3
"""
server.py — Φ7 철학 카운터 MCP v1.0 (형 리뷰 1순위 반영)

변경: json.loads(sys.stdin.read()) → MCP stdio protocol (political-mcp 패턴)
"""
import sys, json, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from phi7_engine import analyze_philosopher, rank_by_similarity, get_identity_update, generate_counter_md
from philosopher_data import list_philosophers, PHILOSOPHERS, PHI7_DIMENSIONS, PARKSY_FEATURES

VERSION = "1.0.0"

def handle_request(request):
    tool = request.get("tool", "")
    params = request.get("params", {})
    
    if tool == "analyze":
        key = params.get("philosopher", "")
        if key not in PHILOSOPHERS:
            return {"error": f"'{key}' 없음", "available": list_philosophers()}
        r = analyze_philosopher(key)
        r["_meta"] = {"version": VERSION, "tool": "analyze"}
        return r
    
    elif tool == "rank":
        results = rank_by_similarity()
        return {"tool": "rank", "version": VERSION, "ranking": results}
    
    elif tool == "id_update":
        key = params.get("philosopher", "")
        if key not in PHILOSOPHERS:
            return {"error": f"'{key}' 없음", "available": list_philosophers()}
        r = get_identity_update(key)
        r["_meta"] = {"version": VERSION, "tool": "id_update"}
        return r
    
    elif tool == "counter":
        key = params.get("philosopher", "")
        if key not in PHILOSOPHERS:
            return {"error": f"'{key}' 없음", "available": list_philosophers()}
        r = generate_counter_md(key)
        r["_meta"] = {"version": VERSION, "tool": "counter"}
        return r
    
    elif tool == "discover":
        results = rank_by_similarity()
        all_discoveries = []
        for r in results[:5]:
            rr = analyze_philosopher(r["key"])
            if rr["discoveries"]:
                all_discoveries.append({
                    "philosopher": rr["philosopher"],
                    "similarity": rr["summary"]["overall_similarity"],
                    "discoveries": rr["discoveries"]
                })
        return {
            "tool": "discover", "version": VERSION,
            "total_discoveries": sum(len(d["discoveries"]) for d in all_discoveries),
            "discoveries": all_discoveries
        }
    
    elif tool == "map":
        results = rank_by_similarity()
        tiers = {"S": [], "A": [], "B": [], "C": []}
        for r in results:
            if r["similarity"] >= 45: tiers["S"].append(r)
            elif r["similarity"] >= 35: tiers["A"].append(r)
            elif r["similarity"] >= 25: tiers["B"].append(r)
            else: tiers["C"].append(r)
        return {
            "tool": "map", "version": VERSION,
            "tiers": {
                "S (유사)": [{"name": r["name"], "sim": r["similarity"]} for r in tiers["S"]],
                "A (약간 유사)": [{"name": r["name"], "sim": r["similarity"]} for r in tiers["A"]],
                "B (차이)": [{"name": r["name"], "sim": r["similarity"]} for r in tiers["B"]],
                "C (매우 다름)": [{"name": r["name"], "sim": r["similarity"]} for r in tiers["C"]]
            }
        }
    
    elif tool == "version":
        return {
            "name": "Φ7 철학 카운터 MCP",
            "version": VERSION,
            "tools": ["analyze", "rank", "id_update", "counter", "discover", "map", "version"],
            "philosophers": list_philosophers(),
            "phi7_axes": {k: v["desc"] for k, v in PHI7_DIMENSIONS.items()}
        }
    
    else:
        return {"error": f"unknown tool '{tool}'", "tools": ["analyze", "rank", "id_update", "counter", "discover", "map", "version"]}

def main():
    # MCP stdio protocol — 한 줄씩 읽고 JSON 응답 출력
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response, ensure_ascii=False))
            sys.stdout.flush()
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"JSON parse error: {e}"}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
