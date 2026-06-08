#!/usr/bin/env python3
"""
server.py — OrbitPrompt Political MCP v1.0 (통합판)

형 설계 + DeepSeek 구현 = Φ-I-C-K-P-7AXIS 정치 분석 v1.0
툴: analyze_politician / compare_policy / simulate_election / rank_politicians
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from political_model import analyze_politician, compare_policy, simulate_election, calc_phi12
from politician_data import POLITICIANS, PHI7_LABELS

VERSION = "1.0.0"

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({
            "name": "OrbitPrompt Political MCP",
            "version": VERSION,
            "model": "Φ-I-C-K-P-7AXIS",
            "tools": ["analyze_politician", "compare_policy", "simulate_election", "rank_politicians"],
            "usage": {
                "analyze_politician": {"name": "박찬대"},
                "compare_policy": {"politician_a": "박찬대", "politician_b": "이재명"},
                "simulate_election": {"candidate": "박찬대", "region": "인천 연수구을"},
                "rank_politicians": {},
            },
            "politicians": list(POLITICIANS.keys()),
            "doc": "README.md"
        }, ensure_ascii=False, indent=2))
        return

    req = json.loads(raw)
    tool = req.get("tool", "")
    params = req.get("params", {})

    if tool == "analyze_politician":
        r = analyze_politician(params.get("name", ""))
        r["_meta"] = {"version": VERSION, "tool": tool}
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif tool == "compare_policy":
        r = compare_policy(params.get("politician_a", ""), params.get("politician_b", ""))
        r["_meta"] = {"version": VERSION, "tool": tool}
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif tool == "simulate_election":
        r = simulate_election(params.get("candidate", ""), params.get("region", None))
        r["_meta"] = {"version": VERSION, "tool": tool}
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif tool == "rank_politicians":
        ranked = sorted(POLITICIANS.keys(), key=lambda n: calc_phi12(n)["phi12_strength"], reverse=True)
        result = []
        for i, n in enumerate(ranked):
            r = calc_phi12(n)
            axes = r["phi7_axes"]
            avg = round(sum(axes.values()) / 7, 1)
            grade = "S" if avg >= 75 else "A" if avg >= 65 else "B"
            result.append({
                "rank": i + 1, "name": n, "party": POLITICIANS[n]["party"],
                "phi12": r["phi12_strength"], "phi7": r["phi7_strength"],
                "phi5": r["phi5_strength"], "grade": grade,
                "top_axis": max(axes, key=axes.get),
                "weak_axis": min(axes, key=axes.get),
            })
        print(json.dumps({"tool": "rank_politicians", "version": VERSION, "ranking": result}, ensure_ascii=False, indent=2))

    elif tool == "orchestrate":
        print(json.dumps({
            "tool": "orchestrate", "version": VERSION,
            "name": "Φ-I-C-K-P-7AXIS Political MCP",
            "description": "시민이 AI로 정치 인프라를 만들고, 정치인이 그 인프라를 쓰는 모델",
            "architecture": {
                "method": "삼각 실행 루프 (박씨→DeepSeek→Claude)",
                "delivery": "GitHub 역방향 유통 (정치인→박씨 동선)",
                "slot_model": "Layer 1: 이름 / Layer 2: 도시의제 / Layer 3: 협업",
            },
            "phi7_axes": PHI7_LABELS,
            "version_history": {
                "v0.1": "DeepSeek 6개 툴 (일반 LLM 래퍼)",
                "v0.2": "DeepSeek Φ7 전용 4개 툴 (보좌관 B2B)",
                "v1.0": "형+DeepSeek 통합 — 데이터 기반 7축 + 4인 DB + 시뮬레이션",
            }
        }, ensure_ascii=False, indent=2))

    else:
        print(json.dumps({"error": f"unknown tool '{tool}'", "tools": ["analyze_politician", "compare_policy", "simulate_election", "rank_politicians", "orchestrate"]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
