#!/usr/bin/env python3
"""
football-mcp-server.py — Φ-I-C-K-P 축구 예측 MCP 서버
역할: 실제 데이터 기반 예측 (FIFA 랭킹 + ELO)
용도: DeepSeek Aider가 Bash로 직접 호출
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from simulation import win_prob, predict_match, monte_carlo
from team_data import TEAMS, WEIGHTS, calc_strength, all_strengths

def predict(team1: str, team2: str) -> dict:
    """Φ-I-C-K-P 예측 (실제 데이터 기반)"""
    result = predict_match(team1, team2)
    result["source"] = "FIFA Ranking 2026-04 + ELO Rating"
    return result

def strength(team: str = "") -> dict:
    """팀 강점 조회"""
    if team:
        if team in TEAMS:
            return {"name": team, **TEAMS[team], "strength": calc_strength(team)}
        return {"error": f"'{team}' not found"}
    return {"teams": all_strengths()}

def all_teams() -> list:
    """전체 팀 목록"""
    return sorted(TEAMS.keys())

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "predict" and len(sys.argv) >= 4:
        result = predict(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif cmd == "strength":
        team = sys.argv[2] if len(sys.argv) > 2 else ""
        result = strength(team)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif cmd == "list":
        for t in all_teams():
            print(f"  {t:20s} {calc_strength(t):.1f}")
    else:
        print("⚽ Φ-I-C-K-P 축구 예측 MCP")
        print("  predict [A] [B]  → 승률 예측")
        print("  strength [team]  → 팀 강점")
        print("  list             → 전체 팀 목록")
        print("  데이터 출처: FIFA 랭킹 2026-04 + ELO Rating")
