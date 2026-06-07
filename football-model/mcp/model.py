#!/usr/bin/env python3
"""
model.py — Φ-I-C-K-P-7AXIS 엔진

5변수(Φ-I-C-K-P) + OrbitPrompt 7축 철학 통합
= 12개 차원의 팀 평가 모델

철학 레이어 (7축):
  Meta     — 자기 스타일 인식도
  Reverse  — 약점 보완 능력
  Modular  — 전술 패턴 반복성
  Language — 팀 정체성 선명도
  Zoom     — 빅매치 디테일
  Spiral   — 대회 성장 곡선
  Quantum  — 이변 잠재력
"""

import json, sys, os, random
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from team_data import TEAMS, WEIGHTS, calc_strength

# ═══════════════════════════════════════════════
# 7-AXIS 철학 데이터 (OrbitPrompt 철학 기반)
# ═══════════════════════════════════════════════
PHI7 = {
    # 각 축 0~100. 0=전혀 해당 안 됨, 100=완벽함
    # 축구팀 7축 평가 — 박씨 직관 + 데이터 교차검증
    "Argentina":   {"meta":85,"reverse":78,"modular":82,"lang":90,"zoom":88,"spiral":75,"quantum":65},
    "France":      {"meta":88,"reverse":72,"modular":85,"lang":80,"zoom":92,"spiral":82,"quantum":70},
    "Brazil":      {"meta":92,"reverse":65,"modular":75,"lang":95,"zoom":85,"spiral":78,"quantum":80},
    "England":     {"meta":70,"reverse":82,"modular":88,"lang":72,"zoom":75,"spiral":68,"quantum":55},
    "Spain":       {"meta":85,"reverse":75,"modular":90,"lang":82,"zoom":78,"spiral":72,"quantum":60},
    "Portugal":    {"meta":78,"reverse":70,"modular":75,"lang":75,"zoom":82,"spiral":65,"quantum":68},
    "Netherlands": {"meta":82,"reverse":80,"modular":85,"lang":78,"zoom":80,"spiral":70,"quantum":72},
    "Germany":     {"meta":75,"reverse":85,"modular":92,"lang":75,"zoom":72,"spiral":65,"quantum":58},
    "Belgium":     {"meta":72,"reverse":68,"modular":78,"lang":68,"zoom":70,"spiral":62,"quantum":55},
    "Croatia":     {"meta":80,"reverse":85,"modular":75,"lang":78,"zoom":82,"spiral":72,"quantum":78},
    "Uruguay":     {"meta":78,"reverse":82,"modular":72,"lang":75,"zoom":80,"spiral":68,"quantum":75},
    "Switzerland": {"meta":72,"reverse":85,"modular":82,"lang":65,"zoom":75,"spiral":62,"quantum":58},
    "Mexico":      {"meta":75,"reverse":70,"modular":72,"lang":82,"zoom":78,"spiral":65,"quantum":72},
    "Morocco":     {"meta":68,"reverse":82,"modular":70,"lang":72,"zoom":85,"spiral":88,"quantum":90},
    "Japan":       {"meta":82,"reverse":78,"modular":85,"lang":85,"zoom":75,"spiral":80,"quantum":85},
    "USA":         {"meta":72,"reverse":75,"modular":78,"lang":70,"zoom":82,"spiral":78,"quantum":80},
    "South Korea": {"meta":78,"reverse":75,"modular":72,"lang":85,"zoom":80,"spiral":72,"quantum":82},
    "Australia":   {"meta":70,"reverse":72,"modular":75,"lang":68,"zoom":75,"spiral":70,"quantum":72},
    "Senegal":     {"meta":68,"reverse":75,"modular":72,"lang":72,"zoom":80,"spiral":78,"quantum":85},
    "Colombia":    {"meta":72,"reverse":70,"modular":75,"lang":78,"zoom":85,"spiral":72,"quantum":80},
    "Sweden":      {"meta":70,"reverse":78,"modular":80,"lang":62,"zoom":72,"spiral":65,"quantum":58},
    "Iran":        {"meta":75,"reverse":82,"modular":85,"lang":72,"zoom":68,"spiral":62,"quantum":65},
    "Ecuador":     {"meta":65,"reverse":70,"modular":68,"lang":72,"zoom":78,"spiral":68,"quantum":75},
    "Czech":       {"meta":68,"reverse":72,"modular":78,"lang":62,"zoom":70,"spiral":62,"quantum":58},
    "Norway":      {"meta":65,"reverse":68,"modular":72,"lang":62,"zoom":72,"spiral":62,"quantum":65},
    "Canada":      {"meta":62,"reverse":65,"modular":68,"lang":65,"zoom":75,"spiral":72,"quantum":72},
    "Tunisia":     {"meta":68,"reverse":72,"modular":70,"lang":68,"zoom":70,"spiral":65,"quantum":68},
    "Austria":     {"meta":65,"reverse":68,"modular":72,"lang":60,"zoom":68,"spiral":62,"quantum":55},
    "Turkiye":     {"meta":72,"reverse":68,"modular":65,"lang":72,"zoom":78,"spiral":68,"quantum":75},
    "Egypt":       {"meta":68,"reverse":72,"modular":70,"lang":65,"zoom":72,"spiral":65,"quantum":68},
    "Algeria":     {"meta":62,"reverse":68,"modular":68,"lang":68,"zoom":72,"spiral":65,"quantum":70},
    "Paraguay":    {"meta":65,"reverse":70,"modular":68,"lang":62,"zoom":68,"spiral":62,"quantum":62},
    "Scotland":    {"meta":62,"reverse":65,"modular":72,"lang":68,"zoom":65,"spiral":60,"quantum":58},
    "Qatar":       {"meta":58,"reverse":62,"modular":65,"lang":55,"zoom":62,"spiral":55,"quantum":52},
    "Saudi":       {"meta":55,"reverse":62,"modular":65,"lang":58,"zoom":65,"spiral":60,"quantum":62},
    "Ghana":       {"meta":65,"reverse":68,"modular":65,"lang":68,"zoom":72,"spiral":65,"quantum":72},
    "Panama":      {"meta":55,"reverse":58,"modular":62,"lang":55,"zoom":60,"spiral":55,"quantum":58},
    "South Africa":{"meta":62,"reverse":65,"modular":62,"lang":65,"zoom":68,"spiral":62,"quantum":65},
    "Bosnia":      {"meta":58,"reverse":62,"modular":62,"lang":58,"zoom":65,"spiral":58,"quantum":60},
    "DR Congo":    {"meta":55,"reverse":58,"modular":60,"lang":55,"zoom":65,"spiral":60,"quantum":65},
    "Haiti":       {"meta":48,"reverse":52,"modular":50,"lang":48,"zoom":48,"spiral":45,"quantum":48},
    "Jordan":      {"meta":52,"reverse":55,"modular":52,"lang":52,"zoom":55,"spiral":50,"quantum":52},
    "Uzbekistan":  {"meta":52,"reverse":55,"modular":55,"lang":52,"zoom":55,"spiral":52,"quantum":55},
    "Cape Verde":  {"meta":48,"reverse":52,"modular":50,"lang":48,"zoom":55,"spiral":50,"quantum":52},
    "Iraq":        {"meta":52,"reverse":58,"modular":55,"lang":52,"zoom":58,"spiral":52,"quantum":58},
    "New Zealand": {"meta":48,"reverse":55,"modular":52,"lang":45,"zoom":52,"spiral":48,"quantum":50},
    "Curacao":     {"meta":42,"reverse":45,"modular":42,"lang":40,"zoom":45,"spiral":42,"quantum":45},
}

# 7축 가중치 (팀 성격에 따라 중요도 다름)
AXIS_WEIGHTS = {
    "meta": 1.2, "reverse": 1.1, "modular": 1.0,
    "lang": 1.0, "zoom": 1.2, "spiral": 1.3, "quantum": 1.5
}

def calc_phi7(name: str) -> dict:
    """팀 7축 프로필 반환"""
    return PHI7.get(name, {k: 50 for k in AXIS_WEIGHTS})

def calc_phi7_score(name: str) -> float:
    """7축 종합 점수 (0~100)"""
    p = calc_phi7(name)
    if not p: return 50
    raw = sum(p[k] * AXIS_WEIGHTS[k] for k in AXIS_WEIGHTS)
    max_possible = 100 * sum(AXIS_WEIGHTS.values())
    return round(raw / max_possible * 100, 1)

# ═══════════════════════════════════════════════
# Φ-I-C-K-P-7AXIS 통합 점수
# ═══════════════════════════════════════════════
PHI5_WEIGHTS = {"phi": 1.0, "infra": 1.2, "ctx": 0.8, "k": 1.3, "p": 1.5}
PHI7_WEIGHT = 0.3  # 7축 비중 (30%)

def calc_phi5(name: str) -> float:
    """Φ-I-C-K-P 5변수 점수 (team_data.py 기반)"""
    return calc_strength(name)

def calc_phi_12(name: str) -> dict:
    """통합 12차원 점수"""
    phi5 = TEAMS.get(name, {})
    phi7 = calc_phi7(name)
    strength_5 = calc_phi5(name)
    strength_7 = calc_phi7_score(name)
    combined = round(strength_5 * (1 - PHI7_WEIGHT) + strength_7 * PHI7_WEIGHT, 1)
    
    return {
        "team": name,
        "phi5_factors": phi5,
        "phi7_factors": phi7,
        "phi5_strength": strength_5,
        "phi7_strength": strength_7,
        "phi12_strength": combined,
        "active": "phi12"
    }

def predict_win_prob(name_a: str, name_b: str, use_phi12: bool = True) -> dict:
    """Φ-I-C-K-P-7AXIS 승률 예측"""
    if use_phi12:
        a = calc_phi_12(name_a)["phi12_strength"]
        b = calc_phi_12(name_b)["phi12_strength"]
    else:
        a = calc_phi5(name_a)
        b = calc_phi5(name_b)
    
    diff = a - b
    prob_a = 1.0 / (1.0 + 10 ** (-diff / 20.0))
    prob_b = 1.0 - prob_a
    
    return {
        "team_a": name_a, "team_b": name_b,
        "strength_a": a, "strength_b": b,
        "win_prob_a": round(prob_a * 100, 1),
        "win_prob_b": round(prob_b * 100, 1),
        "predicted_winner": name_a if prob_a > 0.5 else name_b,
        "model": "phi12" if use_phi12 else "phi5",
        "confidence": "high" if abs(prob_a - prob_b) > 0.2 else "medium" if abs(prob_a - prob_b) > 0.1 else "low"
    }

def predict_with_baseline(name_a: str, name_b: str) -> dict:
    """3레이어 비교: Φ12 vs Φ5 vs ELO-only"""
    # Φ-I-C-K-P-7AXIS
    a12 = calc_phi_12(name_a)["phi12_strength"]
    b12 = calc_phi_12(name_b)["phi12_strength"]
    diff12 = a12 - b12
    p12 = 1.0 / (1.0 + 10 ** (-diff12 / 20.0))
    
    # Φ-I-C-K-P 5변수 (ELO 보정)
    a5 = calc_phi5(name_a)
    b5 = calc_phi5(name_b)
    diff5 = a5 - b5
    p5 = 1.0 / (1.0 + 10 ** (-diff5 / 20.0))
    
    # ELO-only (baseline)
    from team_data import ELO_RATING
    elo_a = ELO_RATING.get(name_a, 1500)
    elo_b = ELO_RATING.get(name_b, 1500)
    diff_elo = elo_a - elo_b
    p_elo = 1.0 / (1.0 + 10 ** (-diff_elo / 400.0))
    
    return {
        "team_a": name_a, "team_b": name_b,
        "phi12": {"winner": name_a if p12 > 0.5 else name_b, "prob": round(max(p12, 1-p12)*100, 1)},
        "phi5": {"winner": name_a if p5 > 0.5 else name_b, "prob": round(max(p5, 1-p5)*100, 1)},
        "elo_baseline": {"winner": name_a if p_elo > 0.5 else name_b, "prob": round(max(p_elo, 1-p_elo)*100, 1)},
        "agreement": "unanimous" if (p12>0.5)==(p5>0.5)==(p_elo>0.5) else "split",
        "phi7_profile": calc_phi7(name_a)
    }

def content_script(matchup: dict) -> str:
    """예측 결과 → 유튜브 대본 자동 생성"""
    a, b = matchup["team_a"], matchup["team_b"]
    w12 = matchup["phi12"]["winner"]
    w5 = matchup["phi5"]["winner"]
    w_elo = matchup["elo_baseline"]["winner"]
    
    lines = [
        f"🎯 Φ-I-C-K-P-7AXIS 예측: {a} vs {b}",
        "",
        "【3레이어 비교】",
        f"  Φ-I-C-K-P-7AXIS (12차원): {w12} 승 (확률 {matchup['phi12']['prob']}%)",
        f"  Φ-I-C-K-P 5변수:       {w5} 승 (확률 {matchup['phi5']['prob']}%)",
        f"  ELO 기준선:            {w_elo} 승 (확률 {matchup['elo_baseline']['prob']}%)",
    ]
    
    if matchup["agreement"] == "unanimous":
        lines.append(f"\n✅ 세 모델 모두 {w12} 승을 예측 — 합의됨")
    else:
        lines.append(f"\n⚠️ 모델 간 이견 발생 — 이변 가능성")
    
    p7 = matchup.get("phi7_profile", {})
    if p7:
        lines.append(f"\n【{a} 7축 철학 분석】")
        for axis, val in sorted(p7.items(), key=lambda x: -x[1]):
            emoji = {"meta":"🧠","reverse":"🔄","modular":"🧩","lang":"💬","zoom":"🔍","spiral":"📈","quantum":"⚡"}
            lines.append(f"  {emoji.get(axis,'')} {axis.capitalize()}: {val}/100")
    
    lines.append(f"\n#WorldCup2026 #PhiICKP #축구예측")
    return "\n".join(lines)

if __name__ == "__main__":
    if "--compare" in sys.argv:
        i = sys.argv.index("--compare")
        r = predict_with_baseline(sys.argv[i+1], sys.argv[i+2])
        print(json.dumps(r, indent=2, ensure_ascii=False))
    elif "--phi12" in sys.argv:
        i = sys.argv.index("--phi12")
        r = calc_phi_12(sys.argv[i+1])
        print(json.dumps(r, indent=2, ensure_ascii=False))
    elif "--script" in sys.argv:
        i = sys.argv.index("--script")
        r = predict_with_baseline(sys.argv[i+1], sys.argv[i+2])
        print(content_script(r))
    elif "--list" in sys.argv:
        sr = sorted(TEAMS.keys(), key=lambda n: calc_phi_12(n)["phi12_strength"], reverse=True)
        print(f"{'Team':20s} {'Φ5':>7s} {'Φ7':>7s} {'Φ12':>7s}")
        print("-" * 45)
        for n in sr:
            r = calc_phi_12(n)
            print(f"{n:20s} {r['phi5_strength']:>6.1f} {r['phi7_strength']:>6.1f} {r['phi12_strength']:>6.1f}")
    else:
        print("사용법:")
        print("  --compare A B   3레이어 비교")
        print("  --phi12 A       Φ12 통합 점수")
        print("  --script A B   유튜브 대본 생성")
        print("  --list         전체 팀 순위")
