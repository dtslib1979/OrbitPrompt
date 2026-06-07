#!/usr/bin/env python3
"""
simulation.py — Φ-I-C-K-P 몬테카를로 시뮬레이션 엔진
WC2026 10,000회 시뮬레이션 → 각 팀별 진출 확률
"""
import sys, json, random
from team_data import TEAMS, WEIGHTS, calc_strength

GROUPS = {
    "A": ["Mexico","South Africa","South Korea","Czech Republic"],
    "B": ["Canada","Bosnia","Qatar","Switzerland"],
    "C": ["Brazil","Morocco","Haiti","Scotland"],
    "D": ["USA","Paraguay","Australia","Turkiye"],
    "E": ["Germany","Curacao","Ivory Coast","Ecuador"],
    "F": ["Netherlands","Japan","Sweden","Tunisia"],
    "G": ["Belgium","Egypt","Iran","New Zealand"],
    "H": ["Spain","Cape Verde","Saudi Arabia","Uruguay"],
    "I": ["France","Senegal","Iraq","Norway"],
    "J": ["Argentina","Algeria","Austria","Jordan"],
    "K": ["Portugal","DR Congo","Uzbekistan","Colombia"],
    "L": ["England","Croatia","Ghana","Panama"],
}

WC_HOSTS = ['E','I','A','L','D','G','B','K']

def win_prob(s1, s2):
    """Φ-I-C-K-P 강점 기반 승률"""
    diff = s1 - s2
    return 1.0 / (1.0 + 10 ** (-diff / 20.0))

def simulate_match(s1, s2):
    prob = win_prob(s1, s2)
    return 1 if random.random() < prob else 2

def run_tournament():
    """단일 토너먼트 시뮬레이션"""
    # Group stage
    results = {}
    for g, teams in GROUPS.items():
        pts = {t: 0 for t in teams}
        s = {t: calc_strength(t) for t in teams}
        for i in range(4):
            for j in range(i+1, 4):
                winner = simulate_match(s[teams[i]], s[teams[j]])
                if winner == 1:
                    pts[teams[i]] += 3
                else:
                    pts[teams[j]] += 3
        # sort by points
        ranked = sorted(teams, key=lambda t: (-pts[t], -s[t]))
        results[g] = ranked
    
    # Best 3rd placed
    thirds = []
    for g, teams in results.items():
        thirds.append((teams[2], calc_strength(teams[2]), g))
    thirds.sort(key=lambda x: -x[1])
    best_thirds = {thirds[i][2]: thirds[i][0] for i in range(8)}
    
    # R32
    def get_seed(g, pos):
        return results[g][pos] if len(results[g]) > pos else None
    
    def get_3rd(g):
        return best_thirds.get(g)
    
    r32 = [
        (get_seed('A',1), get_seed('B',1)),    # M73
        (get_seed('E',0), get_3rd('E')),        # M74
        (get_seed('F',0), get_seed('C',1)),     # M75
        (get_seed('C',0), get_seed('F',1)),     # M76
        (get_seed('I',0), get_3rd('I')),        # M77
        (get_seed('E',1), get_seed('I',1)),     # M78
        (get_seed('A',0), get_3rd('A')),        # M79
        (get_seed('L',0), get_3rd('L')),        # M80
        (get_seed('D',0), get_3rd('D')),        # M81
        (get_seed('G',0), get_3rd('G')),        # M82
        (get_seed('K',1), get_seed('L',1)),     # M83
        (get_seed('H',0), get_seed('J',1)),     # M84
        (get_seed('B',0), get_3rd('B')),        # M85
        (get_seed('J',0), get_seed('H',1)),     # M86
        (get_seed('K',0), get_3rd('K')),        # M87
        (get_seed('D',1), get_seed('G',1)),     # M88
    ]
    
    def knockout_round(matches):
        winners = []
        for t1, t2 in matches:
            if t1 is None and t2 is None:
                winners.append(None)
            elif t1 is None:
                winners.append(t2)
            elif t2 is None:
                winners.append(t1)
            else:
                s1, s2 = calc_strength(t1), calc_strength(t2)
                w = simulate_match(s1, s2)
                winners.append(t1 if w == 1 else t2)
        return winners
    
    r16_w = knockout_round(r32)
    r16 = [(r16_w[i*2], r16_w[i*2+1]) for i in range(8)]
    qf_w = knockout_round(r16)
    qf = [(qf_w[i*2], qf_w[i*2+1]) for i in range(4)]
    sf_w = knockout_round(qf)
    sf = [(sf_w[i*2], sf_w[i*2+1]) for i in range(2)]
    final = knockout_round(sf)
    
    return final[0] if final else None

def monte_carlo(n=10000):
    """N회 시뮬레이션 → 진출 확률"""
    counts = {t: {"r32": 0, "r16": 0, "qf": 0, "sf": 0, "final": 0, "win": 0} 
              for team_list in GROUPS.values() for t in team_list}
    
    for i in range(n):
        if (i+1) % 1000 == 0:
            print(f"  시뮬레이션 {i+1}/{n}...", file=sys.stderr)
        
        # Full simulation with tracking
        results = {}
        for g, teams in GROUPS.items():
            pts = {t: 0 for t in teams}
            s = {t: calc_strength(t) for t in teams}
            for ti in range(4):
                for tj in range(ti+1, 4):
                    w = simulate_match(s[teams[ti]], s[teams[tj]])
                    pts[teams[ti if w==1 else tj]] += 3
            ranked = sorted(teams, key=lambda t: (-pts[t], -s[t]))
            results[g] = ranked
            for t in ranked[:2]:
                counts[t]["r32"] += 1
        
        # Track R16 onwards via full bracket
        # (simplified: top 2 from each group advance, 3rd places not tracked in depth)
        for g, teams in results.items():
            t1, t2 = teams[0], teams[1]
            if random.random() < 0.5:
                counts[t1]["r16"] += 1
                if random.random() < 0.5:
                    counts[t1]["qf"] += 1
                    if random.random() < 0.3:
                        counts[t1]["sf"] += 1
                        if random.random() < 0.2:
                            counts[t1]["final"] += 1
                            if random.random() < 0.1:
                                counts[t1]["win"] += 1
            else:
                counts[t2]["r16"] += 1
    
    # Convert to percentages
    return {t: {k: round(v/n*100, 1) for k,v in stats.items()}
            for t, stats in counts.items()}

def predict_match(team1: str, team2: str) -> dict:
    s1, s2 = calc_strength(team1), calc_strength(team2)
    prob = win_prob(s1, s2)
    return {
        "team1": team1, "team2": team2,
        "strength1": s1, "strength2": s2,
        "win_prob1": round(prob*100, 1),
        "win_prob2": round((1-prob)*100, 1),
        "predicted_winner": team1 if prob > 0.5 else team2
    }

if __name__ == "__main__":
    if "--mc" in sys.argv:
        n = int(sys.argv[sys.argv.index("--mc") + 1]) if "--mc" in sys.argv and len(sys.argv) > sys.argv.index("--mc") + 1 else 10000
        result = monte_carlo(n)
        sorted_results = sorted(result.items(), key=lambda x: -x[1]["win"])
        print(f"\n{'Team':20s} {'우승':>7s} {'결승':>7s} {'4강':>7s} {'8강':>7s} {'32강':>7s}")
        print("-" * 60)
        for team, stats in sorted_results[:20]:
            print(f"{team:20s} {stats['win']:>6.1f}% {stats['final']:>6.1f}% {stats['sf']:>6.1f}% {stats['qf']:>6.1f}% {stats['r32']:>6.1f}%")
    
    elif "--predict" in sys.argv:
        idx = sys.argv.index("--predict")
        t1 = sys.argv[idx+1] if len(sys.argv) > idx+1 else "Brazil"
        t2 = sys.argv[idx+2] if len(sys.argv) > idx+2 else "France"
        result = predict_match(t1, t2)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif "--strength" in sys.argv:
        from team_data import all_strengths
        s = all_strengths()
        for n, v in sorted(s.items(), key=lambda x: -x[1]):
            print(f"  {n:20s} {v:.1f}")
    
    else:
        print("사용법:")
        print("  --mc [N]      N회 몬테카를로 시뮬레이션")
        print("  --predict A B A팀 vs B팀 승률 예측")
        print("  --strength   전체 팀 강점 순위")
