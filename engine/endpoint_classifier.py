#!/usr/bin/env python3
"""
endpoint_classifier.py — ENDPOINT Classifier v0.1
실행: python3 endpoint_classifier.py --text "입력" [--debug]
의존성: Python 3 내장 모듈만
"""
import sys, json, re, os
from datetime import datetime

# ─── 키워드 사전 ──────────────────────────────────────────
P0_KW = ["시작해","만들어","구현","개발","phase","착수","지금","급","오늘"]
P3_KW = ["나중에","생각","고려","검토","아이디어","구상"]
MASS_KW = ["쇼츠","릴스","인스타","유튜브","대중","트렌드","바이럴"]
ARISTO_KW = ["컨셉","철학","백서","fld","오복","브랜딩","포지션","명제"]
IDEA_KW = ["아이디어","컨셉","기획","구상","제안"]
DECISION_KW = ["시작","착수","실행","개발","만들어","구현"]
CONTENT_KW = ["영상","글","포스팅","방송","쇼츠"]
ROUTE_PD = ["pd","에이전트","claude","deepseek","형"]
ROUTE_EAE = ["교육","강의","지식","학습","univ"]
ROUTE_BRANCH = ["브랜치","소설","출판","오복","비즈니스"]

# ─── 결정 테이블 (judge_rules.json 참조) ────────────────
DECISION_TABLE = [
    ("decision","P0","any","execute","pd-system",True),
    ("idea","P0","any","execute","pd-system",True),
    ("content","P0","mass","execute","dtslib-branch",False),
    ("content","P0","aristocrat","execute","orbitprompt",True),
    ("idea","P1","mass","execute","eae-univ",False),
    ("idea","P1","aristocrat","execute","orbitprompt",True),
    ("decision","P1","any","execute","pd-system",True),
    ("any","P2","mass","execute","dtslib-branch",False),
    ("any","P2","aristocrat","hold","brain_delta",False),
    ("any","P3","any","hold","brain_delta",False),
    ("noise","any","any","discard","events",False),
]

# ─── 충돌 해결 규칙 ──────────────────────────────────────
CONFLICT_RULES = [
    ("P0_and_P3","P0_priority"),
    ("idea_and_decision","decision_priority"),
    ("mass_and_aristocrat","aristocrat_priority"),
]

def match_kw(text: str, kw_list: list) -> bool:
    return any(kw in text.lower() for kw in kw_list)

def classify(text: str) -> dict:
    t = text.lower()
    
    # 1. 입력 유형
    input_type = "noise"
    if match_kw(t, DECISION_KW): input_type = "decision"
    elif match_kw(t, IDEA_KW): input_type = "idea"
    elif match_kw(t, CONTENT_KW): input_type = "content"
    
    # 2. 우선순위 (충돌 해결: P0 > P3)
    priority = "P2"
    if match_kw(t, P0_KW): priority = "P0"
    elif match_kw(t, P3_KW): priority = "P3"
    
    # 3. 레인 (충돌 해결: aristocrat > mass)
    lane = "mass"
    if match_kw(t, ARISTO_KW): lane = "aristocrat"
    
    # 4. 결정 테이블 조회
    action, route, human = "hold", "brain_delta", False
    for dtype, pri, ln, act, rte, hum in DECISION_TABLE:
        if (dtype == input_type or dtype == "any") and \
           (pri == priority or pri == "any") and \
           (ln == lane or ln == "any"):
            action, route, human = act, rte, hum
            break
    
    # 5. 라우팅 상세
    if match_kw(t, ROUTE_EAE): route = "eae-univ"
    elif match_kw(t, ROUTE_BRANCH): route = "dtslib-branch"
    elif match_kw(t, ROUTE_PD): route = "pd-system"
    
    return {
        "input_type": input_type,
        "priority": priority,
        "lane": lane,
        "action": action,
        "route": route,
        "human_approval": human,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "text_snippet": text[:60]
    }

def pretty_print(d: dict):
    colors = {"execute": "🟢", "hold": "🟡", "discard": "⚫"}
    print(f'{colors.get(d["action"],"⚪")} ENDPOINT 분류 결과')
    print(f'  유형:     {d["input_type"]}')
    print(f'  우선순위: {d["priority"]}')
    print(f'  레인:     {d["lane"]}')
    print(f'  행동:     {d["action"]}')
    print(f'  라우팅:   {d["route"]}')
    print(f'  인간승인: {"필요 ✅" if d["human_approval"] else "불필요 ❌"}')
    print(f'  원문:     {d["text_snippet"]}')

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read().strip()
    if not text:
        print(json.dumps({"error":"입력 없음"}, ensure_ascii=False))
        sys.exit(1)
    result = classify(text)
    if "--debug" in sys.argv:
        pretty_print(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
