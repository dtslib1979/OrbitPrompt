#!/usr/bin/env python3
"""
model.py — Φ-I-C-K-P 모형 (실제 데이터 기반)
DB에 수집된 실제 데이터로 5변수 계산
fallback: team_data.py 하드코딩값
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import db
from team_data import TEAMS as FALLBACK_TEAMS  # fallback용

# WC 우승 이력 보너스 (실제 역사)
WC_CHAMP_BONUS = {
    "Brazil": 10, "Germany": 8, "Argentina": 8,
    "France": 5,  "Italy": 8,   "Spain": 5,
    "England": 5, "Uruguay": 5,
}

# UEFA 소속 보정 (인프라 우위)
UEFA_TEAMS = {
    "France","Spain","England","Germany","Netherlands","Portugal","Belgium",
    "Croatia","Switzerland","Austria","Serbia","Scotland","Turkey","Hungary",
    "Denmark","Czech Republic","Ukraine","Greece","Bosnia","Sweden","Norway",
    "Poland","Romania","Slovakia",
}


def calc_phi(fifa_rank: int, name: str) -> float:
    """φ(철학): FIFA 랭킹 + 월드컵 역사"""
    base = max(20.0, 95.0 - (fifa_rank - 1) * 1.6)
    bonus = WC_CHAMP_BONUS.get(name, 0)
    return min(100.0, round(base + bonus, 1))


def calc_infra(elo: float, name: str) -> float:
    """I(인프라): 실제 ELO 레이팅 + 리그 계수"""
    base = max(20.0, (elo - 1350) / 5.5)
    if name in UEFA_TEAMS:
        base += 8
    return min(100.0, round(base, 1))


def calc_ctx(stats: dict, name: str) -> float:
    """C(맥락): 최근 N년 승률 + 홈어드밴티지"""
    played = stats.get("played", 0)
    if played == 0:
        return 50.0
    wins   = stats.get("wins", 0)
    draws  = stats.get("draws", 0)
    pts    = wins * 3 + draws
    max_pts = played * 3
    win_rate = pts / max_pts if max_pts > 0 else 0.5
    base = 20.0 + win_rate * 80.0
    # 홈 어드밴티지 (WC26 개최국)
    if name in ("USA", "Mexico", "Canada"):
        base += 5
    return min(100.0, round(base, 1))


def calc_k(stats: dict, elo: float, fifa_rank: int) -> float:
    """K(전략): 골득실 + ELO 대비 FIFA 랭킹 효율"""
    played = stats.get("played", 0)
    if played > 0:
        gd = (stats.get("gf", 0) - stats.get("ga", 0)) / played
        gd_score = min(100.0, max(0.0, 50.0 + gd * 15.0))
    else:
        gd_score = 50.0
    rank_score = max(20.0, 100.0 - fifa_rank * 1.5)
    return round((gd_score + rank_score) / 2, 1)


def calc_p(elo: float, stats: dict) -> float:
    """P(슈퍼스타): ELO 절대값 반영"""
    played = stats.get("played", 0)
    win_rate = (stats.get("wins", 0) / played) if played > 0 else 0.5
    base = max(15.0, (elo - 1380) / 5.0)
    return min(100.0, round(base * (0.7 + win_rate * 0.6), 1))


WEIGHTS = {"phi": 1.0, "infra": 1.2, "ctx": 0.8, "k": 1.3, "p": 1.5}
WEIGHT_SUM = sum(WEIGHTS.values())


def calc_strength(name: str, teams_data: dict = None) -> float:
    """
    Φ-I-C-K-P 종합 강도 계산
    teams_data: DB에서 가져온 딕셔너리. None이면 DB 조회 후 fallback.
    """
    if teams_data and name in teams_data:
        d = teams_data[name]
        stats = {"wins": d.get("wins",0), "draws": d.get("draws",0),
                 "losses": d.get("losses",0), "gf": d.get("gf",0),
                 "ga": d.get("ga",0), "played": d.get("played",0)}
        elo       = d.get("elo") or 1500
        fifa_rank = d.get("fifa_rank") or 50
    else:
        # DB 직접 조회
        row = db.get_team(name)
        if row:
            stats = {"wins": row.get("wins",0), "draws": row.get("draws",0),
                     "losses": row.get("losses",0), "gf": row.get("goals_for",0),
                     "ga": row.get("goals_against",0), "played": row.get("matches_played",0)}
            elo       = row.get("elo") or 1500
            fifa_rank = row.get("fifa_rank") or 50
        elif name in FALLBACK_TEAMS:
            # fallback: team_data.py 하드코딩값
            fd = FALLBACK_TEAMS[name]
            return round(
                (fd["phi"]*WEIGHTS["phi"] + fd["infra"]*WEIGHTS["infra"] +
                 fd["ctx"]*WEIGHTS["ctx"] + fd["k"]*WEIGHTS["k"] + fd["p"]*WEIGHTS["p"])
                / WEIGHT_SUM, 1)
        else:
            return 40.0  # 완전 미지 팀

    phi   = calc_phi(fifa_rank, name)
    infra = calc_infra(elo, name)
    ctx   = calc_ctx(stats, name)
    k     = calc_k(stats, elo, fifa_rank)
    p     = calc_p(elo, stats)

    strength = (phi*WEIGHTS["phi"] + infra*WEIGHTS["infra"] + ctx*WEIGHTS["ctx"] +
                k*WEIGHTS["k"] + p*WEIGHTS["p"]) / WEIGHT_SUM
    return round(strength, 1)


def get_team_profile(name: str, teams_data: dict = None) -> dict:
    """팀 전체 프로필 반환"""
    if teams_data and name in teams_data:
        d = teams_data[name]
        stats = {"wins": d.get("wins",0), "draws": d.get("draws",0),
                 "losses": d.get("losses",0), "gf": d.get("gf",0),
                 "ga": d.get("ga",0), "played": d.get("played",0)}
        elo       = d.get("elo") or 1500
        fifa_rank = d.get("fifa_rank") or 50
        fifa_pts  = d.get("fifa_points") or 0
    else:
        row = db.get_team(name)
        if not row:
            return {"error": f"{name} not in DB — fetch_data 먼저"}
        stats = {"wins": row.get("wins",0), "draws": row.get("draws",0),
                 "losses": row.get("losses",0), "gf": row.get("goals_for",0),
                 "ga": row.get("goals_against",0), "played": row.get("matches_played",0)}
        elo       = row.get("elo") or 1500
        fifa_rank = row.get("fifa_rank") or 50
        fifa_pts  = row.get("fifa_points") or 0

    phi   = calc_phi(fifa_rank, name)
    infra = calc_infra(elo, name)
    ctx   = calc_ctx(stats, name)
    k     = calc_k(stats, elo, fifa_rank)
    p     = calc_p(elo, stats)
    strength = round((phi*WEIGHTS["phi"] + infra*WEIGHTS["infra"] + ctx*WEIGHTS["ctx"] +
                      k*WEIGHTS["k"] + p*WEIGHTS["p"]) / WEIGHT_SUM, 1)
    played = stats.get("played", 0)
    return {
        "name": name,
        "fifa_rank": fifa_rank, "fifa_points": fifa_pts,
        "elo": elo,
        "recent_record": f"W{stats.get('wins',0)}-D{stats.get('draws',0)}-L{stats.get('losses',0)} ({played}경기)",
        "phi": phi, "infra": infra, "ctx": ctx, "k": k, "p": p,
        "strength": strength,
    }


if __name__ == "__main__":
    db.init()
    teams_data = db.get_all_teams()
    if not teams_data:
        print("⚠️  DB 비어있음 — server.py fetch_data 먼저 실행")
    else:
        print("📊 강도 순위 (실제 데이터 기반):")
        scores = [(t, calc_strength(t, teams_data)) for t in teams_data]
        for t, s in sorted(scores, key=lambda x: -x[1])[:15]:
            print(f"  {t:20s} {s:.1f}")
