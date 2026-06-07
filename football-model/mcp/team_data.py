#!/usr/bin/env python3
"""
team_data.py — Φ-I-C-K-P 5변수 데이터셋 (실제 FIFA 랭킹 + ELO 기반)
데이터 출처: FIFA World Ranking 2026-04 + ELO Rating 2026
추정 알고리즘: FIFA 랭킹 + ELO → 5변수 수치화
"""
import json

# 실제 FIFA 랭킹 + ELO 기반 추정 데이터
# φ(철학) = FIFA 랭킹 기반 + 역사적 성과
# I(인프라) = 리그 수준 + 유소년 시스템 (ELO 반영)
# C(맥락) = 축구 문화 + 정치적 안정
# K(전략) = 감독 + 최근 성적 (FIFA 변동성 반영)
# P(슈퍼스타) = 핵심 선수 보유 (ELO 상위 편차)
TEAMS = {
    "Argentina": {"phi": 100, "infra": 94, "ctx": 100, "k": 100, "p": 100},
    "France": {"phi": 100, "infra": 92, "ctx": 100, "k": 100, "p": 99},
    "Spain": {"phi": 100, "infra": 89, "ctx": 100, "k": 100, "p": 95},
    "England": {"phi": 100, "infra": 87, "ctx": 98, "k": 100, "p": 93},
    "Brazil": {"phi": 100, "infra": 93, "ctx": 100, "k": 100, "p": 100},
    "Portugal": {"phi": 100, "infra": 84, "ctx": 95, "k": 100, "p": 90},
    "Netherlands": {"phi": 99, "infra": 86, "ctx": 97, "k": 100, "p": 92},
    "Belgium": {"phi": 99, "infra": 81, "ctx": 92, "k": 100, "p": 87},
    "Croatia": {"phi": 98, "infra": 80, "ctx": 90, "k": 100, "p": 85},
    "Germany": {"phi": 97, "infra": 83, "ctx": 93, "k": 100, "p": 88},
    "Uruguay": {"phi": 96, "infra": 77, "ctx": 87, "k": 100, "p": 82},
    "Switzerland": {"phi": 95, "infra": 73, "ctx": 82, "k": 100, "p": 77},
    "Mexico": {"phi": 95, "infra": 71, "ctx": 80, "k": 100, "p": 75},
    "Morocco": {"phi": 94, "infra": 70, "ctx": 78, "k": 100, "p": 73},
    "Japan": {"phi": 93, "infra": 69, "ctx": 77, "k": 100, "p": 72},
    "USA": {"phi": 92, "infra": 67, "ctx": 75, "k": 100, "p": 70},
    "Senegal": {"phi": 90, "infra": 66, "ctx": 73, "k": 100, "p": 68},
    "Colombia": {"phi": 89, "infra": 64, "ctx": 72, "k": 99, "p": 67},
    "South Korea": {"phi": 87, "infra": 63, "ctx": 70, "k": 95, "p": 65},
    "Australia": {"phi": 86, "infra": 60, "ctx": 67, "k": 93, "p": 62},
    "Norway": {"phi": 80, "infra": 61, "ctx": 68, "k": 85, "p": 63},
    "Sweden": {"phi": 84, "infra": 59, "ctx": 65, "k": 89, "p": 60},
    "Iran": {"phi": 83, "infra": 56, "ctx": 62, "k": 87, "p": 57},
    "Austria": {"phi": 83, "infra": 51, "ctx": 57, "k": 84, "p": 52},
    "Ecuador": {"phi": 73, "infra": 57, "ctx": 63, "k": 72, "p": 58},
    "Czech Republic": {"phi": 75, "infra": 53, "ctx": 58, "k": 74, "p": 53},
    "Turkiye": {"phi": 82, "infra": 49, "ctx": 53, "k": 81, "p": 48},
    "Ivory Coast": {"phi": 69, "infra": 54, "ctx": 60, "k": 65, "p": 55},
    "Egypt": {"phi": 76, "infra": 47, "ctx": 52, "k": 72, "p": 47},
    "Tunisia": {"phi": 79, "infra": 44, "ctx": 48, "k": 76, "p": 43},
    "Canada": {"phi": 66, "infra": 50, "ctx": 55, "k": 58, "p": 50},
    "Qatar": {"phi": 75, "infra": 41, "ctx": 45, "k": 68, "p": 40},
    "Algeria": {"phi": 67, "infra": 46, "ctx": 50, "k": 57, "p": 45},
    "Scotland": {"phi": 71, "infra": 40, "ctx": 43, "k": 62, "p": 38},
    "Paraguay": {"phi": 56, "infra": 43, "ctx": 47, "k": 40, "p": 42},
    "Panama": {"phi": 62, "infra": 37, "ctx": 40, "k": 46, "p": 35},
    "Ghana": {"phi": 57, "infra": 39, "ctx": 42, "k": 39, "p": 37},
    "Saudi Arabia": {"phi": 60, "infra": 36, "ctx": 38, "k": 43, "p": 33},
    "Iraq": {"phi": 51, "infra": 34, "ctx": 37, "k": 28, "p": 32},
    "DR Congo": {"phi": 61, "infra": 27, "ctx": 28, "k": 40, "p": 23},
    "Uzbekistan": {"phi": 48, "infra": 33, "ctx": 35, "k": 23, "p": 30},
    "Bosnia": {"phi": 54, "infra": 29, "ctx": 30, "k": 30, "p": 25},
    "South Africa": {"phi": 58, "infra": 24, "ctx": 25, "k": 34, "p": 20},
    "Cape Verde": {"phi": 44, "infra": 30, "ctx": 32, "k": 20, "p": 27},
    "New Zealand": {"phi": 32, "infra": 31, "ctx": 33, "k": 20, "p": 28},
    "Haiti": {"phi": 35, "infra": 26, "ctx": 27, "k": 20, "p": 22},
    "Jordan": {"phi": 39, "infra": 23, "ctx": 23, "k": 20, "p": 18},
    "Curacao": {"phi": 43, "infra": 20, "ctx": 20, "k": 20, "p": 15},
}

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
    print(f"{'Team':20s} {'Strength':>8s} | {'Φ':>4s} {'I':>4s} {'C':>4s} {'K':>4s} {'P':>4s}")
    print("-" * 70)
    for name, data in sorted_teams:
        s = calc_strength(name)
        print(f"{name:20s} {s:>7.1f} | {data['phi']:>3d} {data['infra']:>3d} {data['ctx']:>3d} {data['k']:>3d} {data['p']:>3d}")
