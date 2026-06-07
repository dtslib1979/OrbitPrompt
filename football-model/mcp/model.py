#!/usr/bin/env python3
"""
model.py — Φ-I-C-K-P-7AXIS (12차원 축구 예측 모델)

5변수(Φ-I-C-K-P) + 7드라이버(실제 경기 데이터) = 12차원
7드라이버: 형(phone_claude) 설계, martj42 CSV 5319건 기반
"""
import json, sys, os, warnings
from pathlib import Path

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(__file__))
from team_data import TEAMS, ELO_RATING, WEIGHTS, calc_strength

# ─── 7드라이버 (실제 경기 데이터) ─────────────────────
_PHI7_CACHE = {}

def _get_phi7():
    if not _PHI7_CACHE:
        try:
            from phi7_driver import calc_all_drivers
            _PHI7_CACHE.update(calc_all_drivers())
        except Exception as e:
            for t in TEAMS:
                _PHI7_CACHE[t] = {"meta":60,"reverse":60,"modular":60,"lang":60,"zoom":60,"spiral":60,"quantum":60}
    return _PHI7_CACHE

AXIS_WEIGHTS = {"meta":1.2,"reverse":1.1,"modular":1.0,"lang":1.0,"zoom":1.2,"spiral":1.3,"quantum":1.5}

# ─── 점수 계산 ───────────────────────────────────────────
PHI7_WEIGHT = 0.3

def calc_phi7(name: str) -> dict:
    return _get_phi7().get(name, {k: 50 for k in AXIS_WEIGHTS})

def calc_phi7_score(name: str) -> float:
    p = calc_phi7(name)
    raw = sum(p[k] * AXIS_WEIGHTS[k] for k in AXIS_WEIGHTS)
    return round(raw / (100 * sum(AXIS_WEIGHTS.values())) * 100, 1)

def calc_phi5(name: str) -> float:
    return calc_strength(name)

def calc_phi_12(name: str) -> dict:
    s5 = calc_phi5(name)
    s7 = calc_phi7_score(name)
    c = round(s5 * (1 - PHI7_WEIGHT) + s7 * PHI7_WEIGHT, 1)
    return {"team": name, "phi5_strength": s5, "phi7_strength": s7, "phi12_strength": c}

def predict_win_prob(name_a: str, name_b: str) -> dict:
    a = calc_phi_12(name_a)["phi12_strength"]
    b = calc_phi_12(name_b)["phi12_strength"]
    diff = a - b
    pa = 1.0 / (1.0 + 10 ** (-diff / 20.0))
    return {
        "team_a": name_a, "team_b": name_b,
        "strength_a": a, "strength_b": b,
        "win_prob_a": round(pa * 100, 1),
        "win_prob_b": round((1-pa) * 100, 1),
        "predicted_winner": name_a if pa > 0.5 else name_b,
        "model": "phi12", "confidence": "high" if abs(pa-0.5) > 0.2 else "medium" if abs(pa-0.5) > 0.1 else "low"
    }

def predict_with_baseline(name_a: str, name_b: str) -> dict:
    a12 = calc_phi_12(name_a)["phi12_strength"]
    b12 = calc_phi_12(name_b)["phi12_strength"]
    p12 = 1.0 / (1.0 + 10 ** (-(a12 - b12) / 20.0))
    a5 = calc_phi5(name_a)
    b5 = calc_phi5(name_b)
    p5 = 1.0 / (1.0 + 10 ** (-(a5 - b5) / 20.0))
    ea = ELO_RATING.get(name_a, 1500)
    eb = ELO_RATING.get(name_b, 1500)
    pe = 1.0 / (1.0 + 10 ** (-(ea - eb) / 400.0))
    return {
        "team_a": name_a, "team_b": name_b,
        "phi12": {"winner": name_a if p12>0.5 else name_b, "prob": round(max(p12,1-p12)*100,1)},
        "phi5": {"winner": name_a if p5>0.5 else name_b, "prob": round(max(p5,1-p5)*100,1)},
        "elo_baseline": {"winner": name_a if pe>0.5 else name_b, "prob": round(max(pe,1-pe)*100,1)},
        "agreement": "unanimous" if (p12>0.5)==(p5>0.5)==(pe>0.5) else "split",
        "phi7_profile": calc_phi7(name_a)
    }

def content_script(m: dict) -> str:
    a, b = m["team_a"], m["team_b"]
    lines = [f"🎯 Φ-I-C-K-P-7AXIS 예측: {a} vs {b}", "",
             "【3레이어 비교】"]
    for model in ["phi12","phi5","elo_baseline"]:
        lbl = {"phi12":"Φ12 (7축통합)","phi5":"Φ5 (5변수)","elo_baseline":"ELO 기준선"}[model]
        w = m[model]["winner"]
        p = m[model]["prob"]
        lines.append(f"  {lbl}: {w} 승 ({p}%)")
    if m["agreement"] == "unanimous":
        lines.append(f"\n✅ 세 모델 모두 {m['phi12']['winner']} 승 예측")
    else:
        lines.append("\n⚠️ 모델 간 이견 — 이변 가능성")
    p7 = m.get("phi7_profile", {})
    if p7:
        lines.append(f"\n【{a} 7축 분석】")
        ax_d = {"meta":"자기인식","reverse":"회복력","modular":"전술패턴","lang":"정체성","zoom":"빅매치","spiral":"성장","quantum":"이변"}
        em = {"meta":"🧠","reverse":"🔄","modular":"🧩","lang":"💬","zoom":"🔍","spiral":"📈","quantum":"⚡"}
        for axis in ["meta","reverse","modular","lang","zoom","spiral","quantum"]:
            if axis in p7:
                lines.append(f"  {em.get(axis,'')} {ax_d.get(axis,axis)}: {p7[axis]}/100")
    lines.append("\n#WorldCup2026 #PhiICKP #축구예측")
    return "\n".join(lines)

# ─── CLI ─────────────────────────────────────────────────
if __name__ == "__main__":
    if "--compare" in sys.argv and len(sys.argv) >= 4:
        i = sys.argv.index("--compare")
        print(json.dumps(predict_with_baseline(sys.argv[i+1], sys.argv[i+2]), indent=2, ensure_ascii=False))
    elif "--phi12" in sys.argv and len(sys.argv) >= 3:
        i = sys.argv.index("--phi12")
        print(json.dumps(calc_phi_12(sys.argv[i+1]), indent=2, ensure_ascii=False))
    elif "--script" in sys.argv and len(sys.argv) >= 4:
        i = sys.argv.index("--script")
        print(content_script(predict_with_baseline(sys.argv[i+1], sys.argv[i+2])))
    elif "--list" in sys.argv:
        sr = sorted(TEAMS.keys(), key=lambda n: calc_phi_12(n)["phi12_strength"], reverse=True)
        print(f"{'Team':20s} {'Φ5':>7s} {'Φ7':>7s} {'Φ12':>7s}")
        print("-" * 45)
        for n in sr:
            r = calc_phi_12(n)
            print(f"{n:20s} {r['phi5_strength']:>6.1f} {r['phi7_strength']:>6.1f} {r['phi12_strength']:>6.1f}")
    else:
        print("--compare A B | --phi12 A | --script A B | --list")
