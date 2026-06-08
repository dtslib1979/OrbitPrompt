#!/usr/bin/env python3
"""
political_model.py — Φ드라이버 7축 정치 분석 (v1.0 통합)

형 설계:   구조 + 툴 네이밍 + simulate_election
DeepSeek:  데이터 기반 7축 자동 계산 엔진
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from politician_data import POLITICIANS, AXIS_WEIGHTS, PHI5_WEIGHT, PHI7_LABELS, calc_base_strength, calc_phi7_scores

def calc_phi7_score(name: str) -> float:
    p = calc_phi7_scores(name)
    raw = sum(p[k] * AXIS_WEIGHTS[k] for k in AXIS_WEIGHTS)
    return round(raw / (100 * sum(AXIS_WEIGHTS.values())) * 100, 1)

def calc_phi12(name: str) -> dict:
    s5 = calc_base_strength(name)
    s7 = calc_phi7_score(name)
    combined = round(s5 * (1 - PHI5_WEIGHT) + s7 * PHI5_WEIGHT, 1)
    return {
        "politician": name,
        "phi5_strength": s5,
        "phi7_strength": s7,
        "phi12_strength": combined,
        "phi7_axes": calc_phi7_scores(name),
    }

def analyze_politician(name: str) -> dict:
    """Φ드라이버 7축으로 정치인 해부"""
    if name not in POLITICIANS:
        return {"error": f"'{name}' 데이터 없음", "available": list(POLITICIANS.keys())}
    profile = calc_phi12(name)
    axes = profile["phi7_axes"]
    avg = round(sum(axes.values()) / 7, 1)
    strengths = {k: v for k, v in axes.items() if v >= 70}
    weaknesses = {k: v for k, v in axes.items() if v < 55}
    grade = "S" if avg >= 75 else "A" if avg >= 65 else "B" if avg >= 55 else "C"
    
    return {
        "name": name,
        "party": POLITICIANS[name]["party"],
        "region": POLITICIANS[name]["region"],
        "terms": POLITICIANS[name]["terms"],
        "role": POLITICIANS[name]["role"],
        "phi12_strength": profile["phi12_strength"],
        "phi5": profile["phi5_strength"],
        "phi7": profile["phi7_strength"],
        "phi7_average": avg,
        "grade": grade,
        "strengths": list(strengths.keys()),
        "weaknesses": list(weaknesses.keys()),
        "axes_analysis": {
            k: f"{PHI7_LABELS[k].split(' — ')[0]} {v}/100"
            for k, v in axes.items()
        },
        "phi7_scores": axes,
        "model": "Φ-I-C-K-P-7AXIS Political v1.0"
    }

def compare_policy(politician_a: str, politician_b: str) -> dict:
    """두 정치인 Φ드라이버 비교"""
    if politician_a not in POLITICIANS or politician_b not in POLITICIANS:
        return {"error": "정치인 데이터 없음"}
    a = calc_phi12(politician_a)
    b = calc_phi12(politician_b)
    diff = {}
    for axis in AXIS_WEIGHTS:
        da = a["phi7_axes"].get(axis, 50)
        db = b["phi7_axes"].get(axis, 50)
        diff[axis] = {"a": da, "b": db, "gap": round(da - db, 1),
                      "advantage": politician_a if da > db + 3 else politician_b if db > da + 3 else "even"}
    pa = 1.0 / (1.0 + 10 ** (-(a["phi12_strength"] - b["phi12_strength"]) / 20.0))
    return {
        "politician_a": politician_a,
        "politician_b": politician_b,
        "phi12_a": a["phi12_strength"],
        "phi12_b": b["phi12_strength"],
        "win_prob_a": round(pa * 100, 1),
        "win_prob_b": round((1 - pa) * 100, 1),
        "predicted_stronger": politician_a if pa > 0.5 else politician_b,
        "axis_comparison": diff,
    }

def simulate_election(candidate: str, region: str = None) -> dict:
    """시나리오 시뮬레이션"""
    if candidate not in POLITICIANS:
        return {"error": f"'{candidate}' 데이터 없음"}
    profile = calc_phi12(candidate)
    p = POLITICIANS[candidate]
    s = profile["phi12_strength"]
    base_prob = min(85, max(30, s * 0.9 + p["terms"] * 2))
    scenarios = {
        "현상 유지": round(base_prob, 1),
        "역풍 시나리오": round(min(85, base_prob * 0.75), 1),
        "기회 시나리오": round(min(90, base_prob * 1.15), 1),
    }
    axes = profile["phi7_axes"]
    strongest = max(axes, key=axes.get)
    weakest = min(axes, key=axes.get)
    return {
        "candidate": candidate,
        "region": region or p["region"],
        "party": p["party"],
        "phi12_strength": s,
        "grade": "S" if s >= 75 else "A" if s >= 65 else "B",
        "base_win_probability": round(base_prob, 1),
        "scenarios": scenarios,
        "key_axes": {
            "strongest": {"axis": strongest, "score": axes[strongest], "description": PHI7_LABELS[strongest].split(' — ')[0]},
            "weakest": {"axis": weakest, "score": axes[weakest], "description": PHI7_LABELS[weakest].split(' — ')[0]},
        },
        "model": "Φ-I-C-K-P-7AXIS Political v1.0"
    }
