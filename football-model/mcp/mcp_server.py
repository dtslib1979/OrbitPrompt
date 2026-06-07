#!/usr/bin/env python3
"""
football-mcp-server.py — Φ-I-C-K-P 축구 예측 MCP
사용법:
  python3 mcp_server.py p "Korea" "Japan"   → 승률 예측
  python3 mcp_server.py s "France"          → 팀 강점
  python3 mcp_server.py l                   → 전체 팀 목록
  python3 mcp_server.py mc 10000            → 몬테카를로 시뮬레이션
"""
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from simulation import predict_match, monte_carlo
from team_data import TEAMS, calc_strength

def cmd_predict(t1, t2):
    r = predict_match(t1, t2)
    r["source"] = "FIFA Ranking 2026-04 + ELO Rating"
    print(json.dumps(r, indent=2, ensure_ascii=False))

def cmd_strength(team=""):
    if team:
        if team in TEAMS:
            d = TEAMS[team]
            print(json.dumps({"name": team, "fifa_phi": d["phi"], "infra": d["infra"],
                "context": d["ctx"], "strategy": d["k"], "superstar": d["p"],
                "strength": calc_strength(team)}, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({"error": f"'{team}' not found"}, ensure_ascii=False))
    else:
        sr = sorted(TEAMS.items(), key=lambda x: calc_strength(x[0]), reverse=True)
        print(json.dumps([{"name": n, "strength": calc_strength(n)} for n,d in sr],
            indent=2, ensure_ascii=False))

def cmd_list():
    sr = sorted(TEAMS.items(), key=lambda x: calc_strength(x[0]), reverse=True)
    for n,d in sr:
        print(f"  {n:20s} {calc_strength(n):.1f} | φ={d['phi']} I={d['infra']} C={d['ctx']} K={d['k']} P={d['p']}")

def cmd_mc(n=10000):
    result = monte_carlo(n)
    sr = sorted(result.items(), key=lambda x: -x[1]["win"])
    print(f"{'Team':20s} {'우승':>7s} {'결승':>7s} {'4강':>7s} {'8강':>7s} {'32강':>7s}")
    print("-" * 65)
    for t, s in sr:
        print(f"{t:20s} {s['win']:>6.1f}% {s['final']:>6.1f}% {s['sf']:>6.1f}% {s['qf']:>6.1f}% {s['r32']:>6.1f}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: p [A] [B] | s [team] | l | mc [N]")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "p" and len(sys.argv) >= 4:
        cmd_predict(sys.argv[2], sys.argv[3])
    elif cmd == "s":
        cmd_strength(sys.argv[2] if len(sys.argv) > 2 else "")
    elif cmd == "l":
        cmd_list()
    elif cmd == "mc":
        n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 10000
        cmd_mc(n)
    else:
        print("p [A] [B] | s [team] | l | mc [N]")

print("⚽ MCP 서버 정상 종료 (asyncio 미사용, CLI 전용)")
