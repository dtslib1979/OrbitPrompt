#!/usr/bin/env python3
"""
server.py — Φ7 철학 카운터 MCP v1.0 (만점판)

변경:
  1. 수동 점수 제거 → 특징 기반 동적 유사도 계산
  2. 진짜 발견 엔진 — 예상치 못한 연결을 찾아냄
  3. 11명 철학자 DB (키르케고르/아렌트/마르크스 추가)
  4. ID-MANIFEST 실제 업데이트 제안 생성
  5. 실행 즉시 rank 결과로 검증 가능
"""
import sys, json, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from phi7_engine import (
    analyze_philosopher, rank_by_similarity,
    get_identity_update, generate_counter_md
)
from philosopher_data import list_philosophers, PHILOSOPHERS

VERSION = "1.0.0"
MCP_NAME = "phi7_philosophy_counter"

def tool_analyze(key):
    """툴 1: 철학자 1명 전체 분석"""
    if key not in PHILOSOPHERS:
        return {"error": f"'{key}' 없음", "available": list_philosophers()}
    r = analyze_philosopher(key)
    r["_meta"] = {"version": VERSION, "tool": "analyze", "timestamp": datetime.now().isoformat()}
    return r

def tool_discover():
    """툴 2: 예상치 못한 발견 찾기"""
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
        "tool": "discover",
        "version": VERSION,
        "total_discoveries": sum(len(d["discoveries"]) for d in all_discoveries),
        "discoveries": all_discoveries,
        "_meta": {"version": VERSION, "timestamp": datetime.now().isoformat()}
    }

def tool_rank():
    """툴 3: 유사도 순위"""
    results = rank_by_similarity()
    return {
        "tool": "rank",
        "version": VERSION,
        "ranking": results,
        "_meta": {"version": VERSION, "timestamp": datetime.now().isoformat()}
    }

def tool_id_update(key):
    """툴 4: ID-MANIFEST 업데이트 제안"""
    if key not in PHILOSOPHERS:
        return {"error": f"'{key}' 없음", "available": list_philosophers()}
    r = get_identity_update(key)
    r["_meta"] = {"version": VERSION, "tool": "id_update", "timestamp": datetime.now().isoformat()}
    return r

def tool_counter(key):
    """툴 5: counter.md 자동 생성"""
    if key not in PHILOSOPHERS:
        return {"error": f"'{key}' 없음", "available": list_philosophers()}
    r = generate_counter_md(key)
    r["_meta"] = {"version": VERSION, "tool": "counter_md", "timestamp": datetime.now().isoformat()}
    return r

def tool_map():
    """툴 6: 철학적 계보 지도"""
    results = rank_by_similarity()
    tiers = {"S": [], "A": [], "B": [], "C": []}
    for r in results:
        if r["similarity"] >= 70: tiers["S"].append(r)
        elif r["similarity"] >= 55: tiers["A"].append(r)
        elif r["similarity"] >= 40: tiers["B"].append(r)
        else: tiers["C"].append(r)
    return {
        "tool": "map",
        "version": VERSION,
        "tiers": {
            "S (매우 유사)": [{"name": r["name"], "sim": r["similarity"]} for r in tiers["S"]],
            "A (유사)": [{"name": r["name"], "sim": r["similarity"]} for r in tiers["A"]],
            "B (차이 있음)": [{"name": r["name"], "sim": r["similarity"]} for r in tiers["B"]],
            "C (매우 다름)": [{"name": r["name"], "sim": r["similarity"]} for r in tiers["C"]]
        },
        "_meta": {"version": VERSION, "timestamp": datetime.now().isoformat()}
    }

WELCOME = f"""
╔══════════════════════════════════════════════╗
║  {MCP_NAME} v{VERSION}                       ║
║  Φ7 철학 카운터 — 만점판                     ║
╚══════════════════════════════════════════════╝

툴 6개:
  analyze   — 철학자 1명 전체 분석 (동적 점수)
  discover  — 예상치 못한 철학적 발견
  rank      — 유사도 순위
  id_update — ID-MANIFEST 반영안 생성
  counter   — counter.md 자동 생성
  map       — 철학적 계보 지도 (S/A/B/C)

철학자 11명:
  {', '.join(list_philosophers())}

사용법:
  echo '{{"tool":"analyze","params":{{"philosopher":"kierkegaard"}}}}' | python3 server.py
  echo '{{"tool":"discover","params":{{}}}}' | python3 server.py
  echo '{{"tool":"rank","params":{{}}}}' | python3 server.py
"""

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(WELCOME)
        return
    
    req = json.loads(raw)
    tool = req.get("tool", "")
    params = req.get("params", {})
    
    if tool == "analyze":
        print(json.dumps(tool_analyze(params.get("philosopher", "")), ensure_ascii=False, indent=2))
    elif tool == "discover":
        print(json.dumps(tool_discover(), ensure_ascii=False, indent=2))
    elif tool == "rank":
        print(json.dumps(tool_rank(), ensure_ascii=False, indent=2))
    elif tool == "id_update":
        print(json.dumps(tool_id_update(params.get("philosopher", "")), ensure_ascii=False, indent=2))
    elif tool == "counter":
        print(json.dumps(tool_counter(params.get("philosopher", "")), ensure_ascii=False, indent=2))
    elif tool == "map":
        print(json.dumps(tool_map(), ensure_ascii=False, indent=2))
    else:
        print(json.dumps({
            "tools": ["analyze", "discover", "rank", "id_update", "counter", "map"],
            "philosophers": list_philosophers(),
            "version": VERSION
        }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
