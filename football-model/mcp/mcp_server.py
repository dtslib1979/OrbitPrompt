#!/usr/bin/env python3
"""
football-mcp-server.py — Φ-I-C-K-P 축구 예측 MCP
사용: python3 mcp_server.py predict Korea Japan
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from simulation import win_prob, predict_match
from team_data import TEAMS, WEIGHTS, calc_strength, all_strengths

def predict(t1, t2):
    r = predict_match(t1, t2)
    r["source"] = "FIFA+ELO"
    return r

def strength(team=""):
    if team:
        if team in TEAMS:
            return {"name": team, **TEAMS[team], "strength": calc_strength(team)}
        return {"error": f"not found: {team}"}
    return {"teams": all_strengths()}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "p":
        print(json.dumps(predict(sys.argv[2], sys.argv[3]), indent=2, ensure_ascii=False))
    elif cmd == "s":
        t = sys.argv[2] if len(sys.argv) > 2 else ""
        print(json.dumps(strength(t), indent=2, ensure_ascii=False))
    elif cmd == "l":
        for n in sorted(TEAMS):
            print(f"  {n:20s} {calc_strength(n):.1f}")
    else:
        print("p [A] [B] | s [team] | l")
