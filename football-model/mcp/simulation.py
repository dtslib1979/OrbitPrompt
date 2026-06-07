#!/usr/bin/env python3
"""
simulation.py — Φ-I-C-K-P 몬테카를로 시뮬레이션
실행: python3 simulation.py --mc 10000
"""
import sys, json, random
from team_data import TEAMS, WEIGHTS, calc_strength

GROUPS = {
    "A":["Mexico","South Africa","South Korea","Czech Republic"],
    "B":["Canada","Bosnia","Qatar","Switzerland"],
    "C":["Brazil","Morocco","Haiti","Scotland"],
    "D":["USA","Paraguay","Australia","Turkiye"],
    "E":["Germany","Curacao","Ivory Coast","Ecuador"],
    "F":["Netherlands","Japan","Sweden","Tunisia"],
    "G":["Belgium","Egypt","Iran","New Zealand"],
    "H":["Spain","Cape Verde","Saudi Arabia","Uruguay"],
    "I":["France","Senegal","Iraq","Norway"],
    "J":["Argentina","Algeria","Austria","Jordan"],
    "K":["Portugal","DR Congo","Uzbekistan","Colombia"],
    "L":["England","Croatia","Ghana","Panama"],
}
WC_HOSTS=['E','I','A','L','D','G','B','K']

def win_prob(s1,s2): return 1.0/(1.0+10**(-(s1-s2)/20.0))

def sim(s1,s2): return 1 if random.random()<win_prob(s1,s2) else 2

def run_one():
    results={}
    for g,teams in GROUPS.items():
        pts={t:0 for t in teams}
        strs={t:calc_strength(t) for t in teams}
        for i in range(4):
            for j in range(i+1,4):
                w=sim(strs[teams[i]],strs[teams[j]])
                pts[teams[i if w==1 else j]]+=3
        results[g]=sorted(teams,key=lambda t:(-pts[t],-strs[t]))
    
    # 3위 8개 선발
    thirds=[(results[g][2],calc_strength(results[g][2]),g) for g in results]
    thirds.sort(key=lambda x:-x[1])
    bt={thirds[i][2]:thirds[i][0] for i in range(8)}
    
    def gs(g,p): return results[g][p] if len(results[g])>p else None
    def g3(g): return bt.get(g)
    
    r32=[
        (gs('A',1),gs('B',1)),(gs('E',0),g3('E')),(gs('F',0),gs('C',1)),(gs('C',0),gs('F',1)),
        (gs('I',0),g3('I')),(gs('E',1),gs('I',1)),(gs('A',0),g3('A')),(gs('L',0),g3('L')),
        (gs('D',0),g3('D')),(gs('G',0),g3('G')),(gs('K',1),gs('L',1)),(gs('H',0),gs('J',1)),
        (gs('B',0),g3('B')),(gs('J',0),gs('H',1)),(gs('K',0),g3('K')),(gs('D',1),gs('G',1)),
    ]
    
    def ko(ms):
        w=[]
        for t1,t2 in ms:
            if not t1:w.append(t2)
            elif not t2:w.append(t1)
            else:w.append(t1 if sim(calc_strength(t1),calc_strength(t2))==1 else t2)
        return w
    
    r32w=ko(r32)                              # R32: 16경기 → 16승자
    r16w=ko([(r32w[i*2],r32w[i*2+1]) for i in range(8)])  # R16: 8경기 → 8승자
    qfw=ko([(r16w[i*2],r16w[i*2+1]) for i in range(4)])   # QF: 4경기 → 4승자
    sfw=ko([(qfw[i*2],qfw[i*2+1]) for i in range(2)])     # SF: 2경기 → 2승자

    # 결승
    finalists=[sfw[0],sfw[1]]
    champion=None
    if sfw[0] and sfw[1]:
        champion=sfw[0] if sim(calc_strength(sfw[0]),calc_strength(sfw[1]))==1 else sfw[1]
    elif sfw[0]: champion=sfw[0]
    elif sfw[1]: champion=sfw[1]

    track={t:{"32":0,"16":0,"8":0,"4":0,"2":0,"1":0} for tl in GROUPS.values() for t in tl}
    for g in results:
        track[results[g][0]]["32"]+=1
        track[results[g][1]]["32"]+=1
    for t in r32w:
        if t: track[t]["16"]+=1
    for t in r16w:
        if t: track[t]["8"]+=1
    for t in qfw:
        if t: track[t]["4"]+=1
    for t in finalists:
        if t: track[t]["2"]+=1
    if champion: track[champion]["1"]+=1
    
    return track

def monte_carlo(n=10000):
    agg={t:{"r32":0,"r16":0,"qf":0,"sf":0,"final":0,"win":0} for tl in GROUPS.values() for t in tl}
    for i in range(n):
        if (i+1)%2000==0: print(f"  {i+1}/{n}",file=sys.stderr)
        r=run_one()
        for t in r:
            agg[t]["r32"]+=r[t]["32"]
            agg[t]["r16"]+=r[t]["16"]
            agg[t]["qf"]+=r[t]["8"]
            agg[t]["sf"]+=r[t]["4"]
            agg[t]["final"]+=r[t]["2"]
            agg[t]["win"]+=r[t]["1"]
    return {t:{k:round(v/n*100,1) for k,v in s.items()} for t,s in agg.items()}

def predict_match(t1,t2):
    s1,s2=calc_strength(t1),calc_strength(t2)
    p=win_prob(s1,s2)
    return {"team1":t1,"team2":t2,"strength1":s1,"strength2":s2,
            "win_prob1":round(p*100,1),"win_prob2":round((1-p)*100,1),
            "predicted_winner":t1 if p>0.5 else t2}

if __name__=="__main__":
    if "--mc" in sys.argv:
        n=int(sys.argv[sys.argv.index("--mc")+1]) if len(sys.argv)>sys.argv.index("--mc")+1 else 10000
        r=monte_carlo(n)
        sr=sorted(r.items(),key=lambda x:-x[1]["win"])
        print(f"{'Team':20s} {'우승':>7s} {'결승':>7s} {'4강':>7s} {'8강':>7s} {'32강':>7s}")
        print("-"*60)
        for t,s in sr:
            print(f"{t:20s} {s['win']:>6.1f}% {s['final']:>6.1f}% {s['sf']:>6.1f}% {s['qf']:>6.1f}% {s['r32']:>6.1f}%")
    elif "--predict" in sys.argv:
        i=sys.argv.index("--predict")
        print(json.dumps(predict_match(sys.argv[i+1],sys.argv[i+2] if len(sys.argv)>i+2 else "France"),indent=2,ensure_ascii=False))
    elif "--strength" in sys.argv:
        sr=sorted(TEAMS.items(), key=lambda x: calc_strength(x[0]), reverse=True)
        for n,d in sr:
            print(f"  {n:20s} {calc_strength(n):.1f}")
    else:
        print("--mc [N] | --predict A B | --strength")
