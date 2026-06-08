#!/usr/bin/env python3
"""
phi7_engine.py — Φ7 5축 비교 엔진

철학자 데이터를 Φ7 5축 프레임으로 분석하고,
박씨 철학과의 닮은 점/다른 점을 계산한다.
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from philosopher_data import PHILOSOPHERS, PHI7_AXES, get_philosopher

# 박씨 Φ7 기준점 (백서 기준)
PARKSY_PHI7 = {
    "structure": "구조 인정 + 삶에서 역산 (둘 다)",
    "identity": "생산/조작/튜닝의 대상",
    "medium": "프로그램 (MCP, server.py, 레포)",
    "class": "철학의 생산 조건이자 동력 (워킹 클래스)",
    "endpoint": "server.py로 끝난다 (실행)"
}

def compare_phi7(philosopher_key):
    """철학자 1명을 Φ7 5축으로 비교"""
    p = get_philosopher(philosopher_key)
    if not p:
        return {"error": f"{philosopher_key} 없음"}
    
    scores = p["phi7_scores"]
    
    comparisons = {}
    total_diff = 0
    similarities = []
    differences = []
    
    for axis_key, axis_data in PHI7_AXES.items():
        p_score = scores.get(axis_key, 50)
        # 박씨 점수 (기준: 85~95)
        parksy_score = 90  
        diff = p_score - parksy_score
        
        total_diff += diff
        
        bar_p = "█" * (p_score // 10) + "░" * (10 - p_score // 10)
        bar_m = "█" * 9 + "░" * 1  # 박씨 = 90
        
        verdict = ""
        if diff > 20:
            verdict = f"{p['name']}이/가 더 강함"
        elif diff > 5:
            verdict = "비슷하지만 약간 우세"
        elif diff > -5:
            verdict = "유사한 위치"
        elif diff > -20:
            verdict = "비슷하지만 약간 열세"
        else:
            verdict = f"박씨가 훨씬 더 강함"
        
        comparisons[axis_key] = {
            "axis_name": axis_data["name"],
            "question": axis_data["question"],
            "philosopher_score": p_score,
            "parksy_score": parksy_score,
            "diff": diff,
            "philosopher_bar": bar_p,
            "parksy_bar": bar_m,
            "philosopher_position": axis_data["name"] + ": " + (p["key_concepts"][0] if axis_key in ["identity","medium"] else p["key_concepts"][1] if len(p["key_concepts"]) > 1 else ""),
            "verdict": verdict
        }
        
        # 닮은 점/다른 점 추출
        if abs(diff) <= 15:
            similarities.append(f"  {axis_data['name']}: 점수 차이 {diff} — 비슷한 축")
        else:
            differences.append(f"  {axis_data['name']}: 점수 차이 {diff} — 결정적 차이")
    
    avg_diff = round(total_diff / 5, 1)
    stronger = sum(1 for s in scores.values() if s > 80)
    weaker = sum(1 for s in scores.values() if s < 50)
    
    return {
        "philosopher": p["name"],
        "era": p["era"],
        "eco_volume": p["eco_volume"],
        "key_concepts": p["key_concepts"],
        "phi7_comparison": comparisons,
        "summary": {
            "avg_diff": avg_diff,
            "total_similar_axes": len(similarities),
            "total_different_axes": len(differences),
            "박씨_강세_축": stronger,
            "철학자_강세_축": weaker
        },
        "similarities": similarities,
        "differences": differences,
        "notes": p.get("notes", "")
    }

def batch_compare(keys=None):
    """여러 철학자 한 번에 비교"""
    if not keys:
        keys = list(PHILOSOPHERS.keys())
    results = {}
    for k in keys:
        results[k] = compare_phi7(k)
    return results

def find_most_similar():
    """박씨와 가장 비슷한 철학자 찾기"""
    results = batch_compare()
    rankings = []
    for k, v in results.items():
        avg = v["summary"]["avg_diff"]
        rankings.append((abs(avg), k, PHILOSOPHERS[k]["name"]))
    rankings.sort()
    return rankings

if __name__ == "__main__":
    if "--compare" in sys.argv and len(sys.argv) >= 3:
        i = sys.argv.index("--compare")
        result = compare_phi7(sys.argv[i+1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif "--rank" in sys.argv:
        rankings = find_most_similar()
        print("Φ7 유사도 랭킹 (차이 적은 순):")
        for diff, key, name in rankings:
            print(f"  {name:<20} 차이: {diff:>5.1f}")
    elif "--list" in sys.argv:
        print(f"{'철학자':<20} {'구조':>5} {'정체성':>5} {'매체':>5} {'계급':>5} {'종착점':>5} {'평균':>5}")
        print("-" * 55)
        for k, v in PHILOSOPHERS.items():
            s = v["phi7_scores"]
            avg = round(sum(s.values()) / 5, 1)
            print(f"{v['name']:<20} {s['structure']:>5} {s['identity']:>5} {s['medium']:>5} {s['class']:>5} {s['endpoint']:>5} {avg:>5}")
    else:
        print("--compare <philosopher> | --rank | --list")
