#!/usr/bin/env python3
"""
team_data.py — Φ-I-C-K-P 5변수 데이터셋 (48팀)
각 변수 0~100, 가중치 적용 후 종합 Strength Rating
"""
TEAMS = {
    # Group A
    "Mexico": {"phi": 55, "infra": 60, "ctx": 65, "k": 58, "p": 62},
    "South Africa": {"phi": 42, "infra": 45, "ctx": 50, "k": 40, "p": 38},
    "South Korea": {"phi": 65, "infra": 70, "ctx": 60, "k": 72, "p": 68},
    "Czech Republic": {"phi": 58, "infra": 55, "ctx": 55, "k": 52, "p": 50},
    # Group B
    "Canada": {"phi": 50, "infra": 52, "ctx": 58, "k": 55, "p": 48},
    "Bosnia": {"phi": 42, "infra": 38, "ctx": 35, "k": 45, "p": 40},
    "Qatar": {"phi": 35, "infra": 65, "ctx": 30, "k": 38, "p": 32},
    "Switzerland": {"phi": 60, "infra": 62, "ctx": 68, "k": 65, "p": 58},
    # Group C
    "Brazil": {"phi": 90, "infra": 88, "ctx": 82, "k": 85, "p": 95},
    "Morocco": {"phi": 68, "infra": 55, "ctx": 58, "k": 72, "p": 65},
    "Haiti": {"phi": 25, "infra": 20, "ctx": 28, "k": 22, "p": 18},
    "Scotland": {"phi": 52, "infra": 50, "ctx": 55, "k": 48, "p": 45},
    # Group D
    "USA": {"phi": 62, "infra": 75, "ctx": 72, "k": 68, "p": 60},
    "Paraguay": {"phi": 48, "infra": 42, "ctx": 45, "k": 50, "p": 44},
    "Australia": {"phi": 55, "infra": 58, "ctx": 60, "k": 52, "p": 48},
    "Turkiye": {"phi": 58, "infra": 50, "ctx": 48, "k": 62, "p": 55},
    # Group E
    "Germany": {"phi": 88, "infra": 92, "ctx": 78, "k": 82, "p": 78},
    "Curacao": {"phi": 22, "infra": 18, "ctx": 25, "k": 20, "p": 15},
    "Ivory Coast": {"phi": 55, "infra": 48, "ctx": 50, "k": 58, "p": 52},
    "Ecuador": {"phi": 52, "infra": 45, "ctx": 50, "k": 55, "p": 50},
    # Group F
    "Netherlands": {"phi": 82, "infra": 85, "ctx": 75, "k": 80, "p": 82},
    "Japan": {"phi": 70, "infra": 78, "ctx": 72, "k": 75, "p": 65},
    "Sweden": {"phi": 60, "infra": 58, "ctx": 65, "k": 55, "p": 52},
    "Tunisia": {"phi": 48, "infra": 42, "ctx": 45, "k": 50, "p": 42},
    # Group G
    "Belgium": {"phi": 72, "infra": 70, "ctx": 68, "k": 75, "p": 78},
    "Egypt": {"phi": 52, "infra": 48, "ctx": 50, "k": 55, "p": 48},
    "Iran": {"phi": 50, "infra": 45, "ctx": 42, "k": 55, "p": 48},
    "New Zealand": {"phi": 38, "infra": 35, "ctx": 40, "k": 32, "p": 28},
    # Group H
    "Spain": {"phi": 92, "infra": 90, "ctx": 80, "k": 88, "p": 85},
    "Cape Verde": {"phi": 28, "infra": 22, "ctx": 30, "k": 25, "p": 20},
    "Saudi Arabia": {"phi": 35, "infra": 48, "ctx": 30, "k": 38, "p": 32},
    "Uruguay": {"phi": 68, "infra": 62, "ctx": 65, "k": 70, "p": 72},
    # Group I
    "France": {"phi": 88, "infra": 90, "ctx": 78, "k": 92, "p": 92},
    "Senegal": {"phi": 58, "infra": 50, "ctx": 55, "k": 62, "p": 58},
    "Iraq": {"phi": 38, "infra": 32, "ctx": 32, "k": 40, "p": 35},
    "Norway": {"phi": 58, "infra": 55, "ctx": 62, "k": 55, "p": 55},
    # Group J
    "Argentina": {"phi": 88, "infra": 82, "ctx": 78, "k": 90, "p": 95},
    "Algeria": {"phi": 52, "infra": 45, "ctx": 48, "k": 55, "p": 50},
    "Austria": {"phi": 55, "infra": 52, "ctx": 58, "k": 52, "p": 45},
    "Jordan": {"phi": 32, "infra": 28, "ctx": 30, "k": 35, "p": 25},
    # Group K
    "Portugal": {"phi": 78, "infra": 72, "ctx": 72, "k": 82, "p": 85},
    "DR Congo": {"phi": 35, "infra": 25, "ctx": 28, "k": 38, "p": 32},
    "Uzbekistan": {"phi": 38, "infra": 35, "ctx": 35, "k": 40, "p": 32},
    "Colombia": {"phi": 62, "infra": 55, "ctx": 55, "k": 65, "p": 62},
    # Group L
    "England": {"phi": 85, "infra": 92, "ctx": 80, "k": 82, "p": 88},
    "Croatia": {"phi": 70, "infra": 62, "ctx": 68, "k": 75, "p": 68},
    "Ghana": {"phi": 50, "infra": 42, "ctx": 48, "k": 52, "p": 48},
    "Panama": {"phi": 32, "infra": 28, "ctx": 35, "k": 30, "p": 22},
}

# Φ-I-C-K-P 가중치 (Phi=철학, Infra=인프라, Ctx=맥락, K=전략, P=슈퍼스타)
WEIGHTS = {"phi": 1.0, "infra": 1.2, "ctx": 0.8, "k": 1.3, "p": 1.5}

def calc_strength(name: str) -> float:
    t = TEAMS.get(name)
    if not t: return 50
    raw = sum(t[k] * WEIGHTS[k] for k in WEIGHTS)
    max_possible = 100 * sum(WEIGHTS.values())
    return round(raw / max_possible * 100, 1)

def all_strengths() -> dict:
    return {n: calc_strength(n) for n in TEAMS}

if __name__ == "__main__":
    sorted_teams = sorted(TEAMS.items(), key=lambda x: calc_strength(x[0]), reverse=True)
    print(f"{'Team':20s} {'Strength':>10s} | {'Φ':>4s} {'I':>4s} {'C':>4s} {'K':>4s} {'P':>4s}")
    print("-" * 60)
    for name, data in sorted_teams:
        s = calc_strength(name)
        print(f"{name:20s} {s:>8.1f}  | {data['phi']:>3d} {data['infra']:>3d} {data['ctx']:>3d} {data['k']:>3d} {data['p']:>3d}")
