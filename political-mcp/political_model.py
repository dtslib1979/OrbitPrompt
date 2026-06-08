#!/usr/bin/env python3
"""
political_model.py — Φ드라이버 7축 정치 버전
football-model 동일 구조, 데이터 소스만 정치로 교체
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from politician_data import POLITICIANS, AXIS_WEIGHTS, PHI5_WEIGHT, calc_base_strength

# 7축 정치 드라이버 — 정치인별 Φ점수
# 실데이터 연결 전 베이스라인 (법안 투표 DB 연결 시 자동 교체)
_PHI7_BASELINE = {
    "박찬대": {"meta":72,"reverse":68,"modular":75,"language":80,"zoom":70,"spiral":74,"quantum":55},
    "이재명": {"meta":65,"reverse":78,"modular":70,"language":85,"zoom":82,"spiral":80,"quantum":72},
    "한동훈": {"meta":60,"reverse":55,"modular":58,"language":78,"zoom":65,"spiral":62,"quantum":68},
    "조국":   {"meta":58,"reverse":72,"modular":60,"language":88,"zoom":70,"spiral":65,"quantum":80},
}

def calc_phi7(name: str) -> dict:
    return _PHI7_BASELINE.get(name, {k: 50 for k in AXIS_WEIGHTS})

def calc_phi7_score(name: str) -> float:
    p = calc_phi7(name)
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
        "phi7_axes": calc_phi7(name),
    }

def analyze_politician(name: str) -> dict:
    """Φ드라이버 7축으로 정치인 해부"""
    if name not in POLITICIANS:
        return {"error": f"{name} 데이터 없음. 등록된 정치인: {list(POLITICIANS.keys())}"}
    profile = calc_phi12(name)
    p = POLITICIANS[name]
    axes = profile["phi7_axes"]
    ax_desc = {
        "meta":     f"발언 일관성 {axes['meta']}/100 — 공약 vs 실제 행동 정합성",
        "reverse":  f"위기 대응 {axes['reverse']}/100 — 역풍 맞았을 때 회복력",
        "modular":  f"정책 패턴 {axes['modular']}/100 — 반복 가능한 정책 공식 보유",
        "language": f"수사력 {axes['language']}/100 — 프레이밍·언어 장악력",
        "zoom":     f"의제 집중 {axes['zoom']}/100 — 핵심 이슈 관통력",
        "spiral":   f"성장 궤적 {axes['spiral']}/100 — 선수 거듭할수록 강해지는가",
        "quantum":  f"이변 가능성 {axes['quantum']}/100 — 판세 뒤집는 변수 보유",
    }
    return {
        "name": name,
        "party": p["party"],
        "region": p["region"],
        "terms": p["terms"],
        "role": p["role"],
        "phi12_strength": profile["phi12_strength"],
        "phi5": profile["phi5_strength"],
        "phi7": profile["phi7_strength"],
        "axes_analysis": ax_desc,
        "model": "Φ-I-C-K-P-7AXIS Political v1.0"
    }

def compare_policy(politician_a: str, politician_b: str) -> dict:
    """두 정치인 Φ드라이버 비교"""
    a = calc_phi12(politician_a)
    b = calc_phi12(politician_b)
    if "error" in a or "error" in b:
        return {"error": "정치인 데이터 없음"}
    diff = {}
    for axis in AXIS_WEIGHTS:
        da = a["phi7_axes"].get(axis, 50)
        db = b["phi7_axes"].get(axis, 50)
        diff[axis] = {"a": da, "b": db, "gap": round(da - db, 1),
                      "advantage": politician_a if da > db else politician_b}
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
    """시나리오 시뮬레이션 — 후보 Φ점수 기반"""
    if candidate not in POLITICIANS:
        return {"error": f"{candidate} 데이터 없음"}
    profile = calc_phi12(candidate)
    p = POLITICIANS[candidate]
    s = profile["phi12_strength"]
    # 간이 시나리오: Φ12 기반 당선 확률 추정
    base_prob = min(85, max(30, s * 0.9 + p["terms"] * 2))
    scenarios = {
        "현상 유지": round(base_prob, 1),
        "역풍 시나리오": round(base_prob * 0.75, 1),
        "기회 시나리오": round(min(90, base_prob * 1.15), 1),
    }
    return {
        "candidate": candidate,
        "region": region or p["region"],
        "phi12_strength": s,
        "base_win_probability": round(base_prob, 1),
        "scenarios": scenarios,
        "key_axes": {
            "strongest": max(profile["phi7_axes"], key=profile["phi7_axes"].get),
            "weakest":   min(profile["phi7_axes"], key=profile["phi7_axes"].get),
        },
        "model": "Φ-I-C-K-P-7AXIS Political v1.0"
    }
