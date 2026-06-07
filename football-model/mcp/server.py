#!/usr/bin/env python3
"""
server.py — football-model MCP stdio 서버
프로토콜: JSON-RPC 2.0 over stdin/stdout (MCP 표준)

툴 목록:
  fetch_data      — FIFA 랭킹 + 경기 결과 실제 수집 → DB 저장
  run_simulation  — Monte Carlo n회 → 누적 DB 저장
  get_prediction  — 누적 예측 결과 반환
  predict_match   — 두 팀 간 승률 예측
  team_profile    — 팀 전체 프로필 (Φ-I-C-K-P + 실제 전적)
  db_status       — 현재 DB 상태 (수집일, 총 시뮬레이션 횟수)
"""
import sys, json, random, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import db
from scraper import fetch_all, WC26_TEAMS
from model import calc_strength, get_team_profile, WEIGHTS, WEIGHT_SUM

# ─── 그룹 배정 (WC2026 확정 그룹) ───────────────────────────
GROUPS = {
    "A": ["USA",        "Bolivia",      "Serbia",       "Ghana"],
    "B": ["Mexico",     "Ukraine",      "Uruguay",      "Jamaica"],
    "C": ["Canada",     "Morocco",      "Australia",    "Jordan"],
    "D": ["Germany",    "Japan",        "Cameroon",     "Honduras"],
    "E": ["Spain",      "Brazil",       "Ivory Coast",  "New Zealand"],
    "F": ["France",     "Argentina",    "South Africa", "Tunisia"],
    "G": ["England",    "Netherlands",  "Egypt",        "Panama"],
    "H": ["Portugal",   "Colombia",     "Iraq",         "Paraguay"],
    "I": ["Belgium",    "Ecuador",      "Iran",         "DR Congo"],
    "J": ["Croatia",    "South Korea",  "Nigeria",      "Uzbekistan"],
    "K": ["Switzerland","Senegal",      "Saudi Arabia", "Czech Republic"],
    "L": ["Austria",    "Denmark",      "Turkey",       "Scotland"],
}

# ─── 승률 / 시뮬레이션 ──────────────────────────────────────
def win_prob(s1: float, s2: float) -> float:
    return 1.0 / (1.0 + 10 ** (-(s1 - s2) / 20.0))

def sim_match(s1: float, s2: float) -> int:
    """1: team1 win, 2: team2 win"""
    return 1 if random.random() < win_prob(s1, s2) else 2

def run_one(teams_data: dict) -> dict:
    """단일 토너먼트 시뮬레이션"""
    def s(name):
        return calc_strength(name, teams_data)

    # 그룹 스테이지
    group_results = {}
    for g, teams in GROUPS.items():
        pts = {t: 0 for t in teams}
        for i in range(4):
            for j in range(i+1, 4):
                t1, t2 = teams[i], teams[j]
                w = sim_match(s(t1), s(t2))
                pts[t1 if w==1 else t2] += 3
        group_results[g] = sorted(teams, key=lambda t: (-pts[t], -s(t)))

    # 3위 8팀 선발 (강도 기준)
    thirds = [(group_results[g][2], s(group_results[g][2])) for g in group_results]
    thirds.sort(key=lambda x: -x[1])
    third_qualifiers = {thirds[i][0] for i in range(8)}

    def gs(g, pos):
        t = group_results[g][pos] if len(group_results[g]) > pos else None
        return t

    def g3(g):
        t = group_results[g][2]
        return t if t in third_qualifiers else None

    # R32 대진 (12그룹 → 32팀)
    r32 = []
    for g in "ABCDEFGHIJKL":
        r32.append((gs(g, 0), gs(g, 1)))  # 1위 vs 2위 교차
    # 단순화: 각 그룹 1위 vs 인접그룹 2위 + 3위 8팀
    # 실제 FIFA 2026 대진 공식 미확정 → 강도 기반 쌍 배정
    q1 = [gs(g, 0) for g in "ABCDEFGHIJKL"]  # 12명 1위
    q2 = [gs(g, 1) for g in "ABCDEFGHIJKL"]  # 12명 2위
    q3 = [t for t, _ in thirds[:8]]           # 8명 3위

    r32_teams = q1 + q2 + q3  # 32팀
    # 1위들은 약한 상대와 매칭 (시드 보정)
    r32_pairs = [(r32_teams[i], r32_teams[31-i]) for i in range(16)]

    def ko(pairs):
        winners = []
        for t1, t2 in pairs:
            if not t1: winners.append(t2); continue
            if not t2: winners.append(t1); continue
            winners.append(t1 if sim_match(s(t1), s(t2))==1 else t2)
        return winners

    r32w = ko(r32_pairs)
    r16w = ko([(r32w[i*2], r32w[i*2+1]) for i in range(8)])
    qfw  = ko([(r16w[i*2], r16w[i*2+1]) for i in range(4)])
    sfw  = ko([(qfw[i*2],  qfw[i*2+1])  for i in range(2)])
    champion = sfw[0] if sim_match(s(sfw[0]), s(sfw[1]))==1 else sfw[1]

    # 집계
    all_teams = [t for ts in GROUPS.values() for t in ts]
    track = {t: {"r32":0,"r16":0,"qf":0,"sf":0,"final":0,"win":0} for t in all_teams}

    for t in (q1+q2+q3):
        if t and t in track: track[t]["r32"] += 1
    for t in r32w:
        if t and t in track: track[t]["r16"] += 1
    for t in r16w:
        if t and t in track: track[t]["qf"] += 1
    for t in qfw:
        if t and t in track: track[t]["sf"] += 1
    for t in sfw:
        if t and t in track: track[t]["final"] += 1
    if champion and champion in track: track[champion]["win"] += 1

    return track

def monte_carlo(n: int, teams_data: dict) -> dict:
    """n회 Monte Carlo 시뮬레이션"""
    all_teams = [t for ts in GROUPS.values() for t in ts]
    agg = {t: {"r32":0,"r16":0,"qf":0,"sf":0,"final":0,"win":0} for t in all_teams}

    for i in range(n):
        r = run_one(teams_data)
        for t in r:
            for k in agg[t]:
                agg[t][k] += r[t][k]

    return {t: {k: round(v/n*100, 1) for k,v in s.items()} for t,s in agg.items()}


# ─── MCP 툴 구현 ────────────────────────────────────────────
def tool_fetch_data(params: dict) -> dict:
    years = params.get("years", 5)
    db.init()
    data = fetch_all(years=years)

    # DB에 저장 — ELO 있는 모든 팀 포함 (FIFA 랭킹 Top20만 긁히더라도 전부 저장)
    all_names = set(data["rankings"].keys()) | set(data["elo"].keys())
    # ELO 기반 임시 순위 (FIFA 랭킹 없는 팀용)
    elo_sorted = sorted(data["elo"].items(), key=lambda x: -x[1])
    elo_rank_map = {name: i+1 for i, (name, _) in enumerate(elo_sorted)}

    for name in all_names:
        elo   = data["elo"].get(name, 1500)
        r     = data["rankings"].get(name, {})
        rank  = r.get("rank") or elo_rank_map.get(name, 99)
        pts   = r.get("points", 0.0)
        db.upsert_team(name, rank, pts, elo)

    db.bulk_upsert_match_stats(data["stats"])
    db.insert_matches(data["matches"])

    wc26_in_db = [n for n in WC26_TEAMS if n in all_names]
    return {
        "status": "ok",
        "fetched": data["fetched"],
        "teams_saved": len(all_names),
        "wc26_teams_in_db": len(wc26_in_db),
        "match_records": len(data["matches"]),
        "elo_calculated": len(data["elo"]),
        "sample_top5": [
            {"team": t,
             "fifa_rank": data["rankings"].get(t, {}).get("rank", elo_rank_map.get(t,"?")),
             "elo": data["elo"].get(t,"?")}
            for t in ["France","Argentina","Spain","South Korea","Brazil"]
        ]
    }

def tool_run_simulation(params: dict) -> dict:
    n = max(1, min(50000, params.get("n", 1000)))
    db.init()
    teams_data = db.get_all_teams()
    if not teams_data:
        return {"error": "DB 비어있음 — fetch_data 먼저 실행"}

    results = monte_carlo(n, teams_data)
    total_before = db.get_run_count()
    db.save_simulation(n, results)
    total_after  = db.get_run_count()

    top10 = sorted(results.items(), key=lambda x: -x[1]["win"])[:10]
    return {
        "status": "ok",
        "this_run": n,
        "total_simulations_ever": total_after,
        "top10": [{"team": t, "win_pct": s["win"], "final_pct": s["final"],
                   "sf_pct": s["sf"], "r32_pct": s["r32"]} for t,s in top10]
    }

def tool_get_prediction(params: dict) -> dict:
    db.init()
    preds = db.get_predictions(top=30)
    total = db.get_run_count()
    if not preds:
        return {"error": "예측 없음 — run_simulation 먼저"}
    return {
        "total_simulations": total,
        "note": f"{total}회 누적 시뮬레이션 기반 (많을수록 정확)",
        "predictions": preds,
    }

def tool_predict_match(params: dict) -> dict:
    t1 = params.get("team1", "")
    t2 = params.get("team2", "")
    if not t1 or not t2:
        return {"error": "team1, team2 필수"}
    db.init()
    teams_data = db.get_all_teams()
    s1 = calc_strength(t1, teams_data)
    s2 = calc_strength(t2, teams_data)
    p  = win_prob(s1, s2)
    return {
        "team1": t1, "team2": t2,
        "strength1": s1, "strength2": s2,
        "win_prob1": round(p * 100, 1),
        "win_prob2": round((1-p) * 100, 1),
        "winner": t1 if p >= 0.5 else t2,
        "data_source": "real" if teams_data else "fallback",
    }

def tool_team_profile(params: dict) -> dict:
    name = params.get("team", "")
    if not name:
        return {"error": "team 필수"}
    db.init()
    teams_data = db.get_all_teams()
    return get_team_profile(name, teams_data)

def tool_db_status(params: dict) -> dict:
    db.init()
    teams_data = db.get_all_teams()
    total_runs = db.get_run_count()
    return {
        "teams_in_db": len(teams_data),
        "total_simulations": total_runs,
        "db_path": str(db.DB_PATH),
        "note": f"시뮬레이션 {total_runs}회 누적. fetch_data로 데이터 갱신, run_simulation으로 추가 누적 가능"
    }

TOOLS_DEF = [
    {
        "name": "fetch_data",
        "description": "실제 FIFA 랭킹 + 국제경기 결과를 인터넷에서 긁어와 DB에 저장. 최초 1회 또는 데이터 갱신 시 실행.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "years": {"type": "integer", "description": "최근 N년 경기 결과 수집 (기본 5)", "default": 5}
            }
        }
    },
    {
        "name": "run_simulation",
        "description": "WC2026 Monte Carlo 시뮬레이션 n회 실행 후 누적 저장. 여러 번 돌릴수록 예측 정확도 향상.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n": {"type": "integer", "description": "시뮬레이션 횟수 (기본 1000, 최대 50000)", "default": 1000}
            }
        }
    },
    {
        "name": "get_prediction",
        "description": "누적된 시뮬레이션 결과 기반 WC2026 우승 예측 반환. total_simulations가 많을수록 신뢰도 높음.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "predict_match",
        "description": "두 팀 간 단일 경기 승률 예측 (실제 데이터 기반 Φ-I-C-K-P 모형).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "team1": {"type": "string", "description": "팀1 이름 (예: South Korea)"},
                "team2": {"type": "string", "description": "팀2 이름 (예: France)"}
            },
            "required": ["team1", "team2"]
        }
    },
    {
        "name": "team_profile",
        "description": "팀 전체 프로필: FIFA 랭킹, ELO, 최근 전적, Φ-I-C-K-P 5변수, 종합 강도.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "team": {"type": "string", "description": "팀명 (예: South Korea)"}
            },
            "required": ["team"]
        }
    },
    {
        "name": "db_status",
        "description": "현재 DB 상태: 팀 수, 누적 시뮬레이션 횟수, DB 경로.",
        "inputSchema": {"type": "object", "properties": {}}
    },
]

TOOL_HANDLERS = {
    "fetch_data":     tool_fetch_data,
    "run_simulation": tool_run_simulation,
    "get_prediction": tool_get_prediction,
    "predict_match":  tool_predict_match,
    "team_profile":   tool_team_profile,
    "db_status":      tool_db_status,
}

# ─── MCP JSON-RPC stdio 루프 ────────────────────────────────
def send(obj):
    print(json.dumps(obj, ensure_ascii=False), flush=True)

def handle(req: dict) -> dict:
    rid    = req.get("id")
    method = req.get("method", "")
    params = req.get("params", {})

    if method == "initialize":
        return {"jsonrpc":"2.0","id":rid,"result":{
            "protocolVersion":"2024-11-05",
            "capabilities":{"tools":{}},
            "serverInfo":{"name":"football-model","version":"2.0"}
        }}

    elif method == "tools/list":
        return {"jsonrpc":"2.0","id":rid,"result":{"tools": TOOLS_DEF}}

    elif method == "tools/call":
        name   = params.get("name","")
        args   = params.get("arguments", {})
        if name not in TOOL_HANDLERS:
            return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":f"Unknown tool: {name}"}}
        try:
            result = TOOL_HANDLERS[name](args)
            return {"jsonrpc":"2.0","id":rid,"result":{
                "content":[{"type":"text","text":json.dumps(result, ensure_ascii=False, indent=2)}]
            }}
        except Exception as e:
            return {"jsonrpc":"2.0","id":rid,"error":{"code":-32603,"message":str(e)}}

    elif method == "notifications/initialized":
        return None  # no response

    else:
        return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":f"Method not found: {method}"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(req)
        if resp is not None:
            send(resp)

if __name__ == "__main__":
    # CLI 모드 (테스트용)
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        arg = sys.argv[2] if len(sys.argv) > 2 else ""
        if cmd == "fetch":
            print(json.dumps(tool_fetch_data({"years": int(arg) if arg else 5}), indent=2, ensure_ascii=False))
        elif cmd == "sim":
            print(json.dumps(tool_run_simulation({"n": int(arg) if arg else 1000}), indent=2, ensure_ascii=False))
        elif cmd == "pred":
            print(json.dumps(tool_get_prediction({}), indent=2, ensure_ascii=False))
        elif cmd == "match":
            t2 = sys.argv[3] if len(sys.argv) > 3 else "France"
            print(json.dumps(tool_predict_match({"team1": arg, "team2": t2}), indent=2, ensure_ascii=False))
        elif cmd == "profile":
            print(json.dumps(tool_team_profile({"team": arg}), indent=2, ensure_ascii=False))
        elif cmd == "status":
            print(json.dumps(tool_db_status({}), indent=2, ensure_ascii=False))
        else:
            print("사용법: server.py [fetch|sim|pred|match|profile|status] [args]")
    else:
        main()  # MCP stdio 모드
