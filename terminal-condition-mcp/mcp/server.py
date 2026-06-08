#!/usr/bin/env python3
"""단말기 조건 MCP — 모순 덩어리 엔진"""
import sys, json
from datetime import datetime
VERSION = "1.0.0"

CONTRADICTIONS = [
    {"id": "01", "a": "여성성", "b": "남성성", "desc": "하나만 있는 게 아니다. 필요에 따라 드라이버를 전환한다."},
    {"id": "02", "a": "민주당 좋아함", "b": "약자 싫어함", "desc": "정치적 선호와 계급 감각이 일치하지 않는다."},
    {"id": "03", "a": "천민", "b": "계급 엘리트 의식", "desc": "바닥에서 출발했지만 머리는 엘리트를 안다."},
    {"id": "04", "a": "구조주의", "b": "포스트구조주의", "desc": "구조를 인정하면서도 해체하고 조작한다."},
    {"id": "05", "a": "불친절", "b": "파트너십", "desc": "'문서 봐'로 때리면서도 '찾아오면 같이 간다'."},
    {"id": "06", "a": "CS를 지움", "b": "MCP로 구현", "desc": "인터페이스 CS를 숨기지만 철학은 server.py로 끝낸다."},
    {"id": "07", "a": "말을 아낌", "b": "27커밋", "desc": "한 마디로 움직이지만 결과는 레포에 남긴다."}
]

def handle(req):
    tool = req.get("tool", "")
    if tool == "all":
        return {"tool": "all", "version": VERSION, "contradictions": CONTRADICTIONS}
    elif tool == "random":
        import random
        c = random.choice(CONTRADICTIONS)
        return {"tool": "random", "version": VERSION, "contradiction": c}
    elif tool == "resolve":
        cid = req.get("params", {}).get("id", "")
        found = [c for c in CONTRADICTIONS if c["id"] == cid]
        if not found:
            return {"error": f"id {cid} 없음", "available": [c["id"] for c in CONTRADICTIONS]}
        c = found[0]
        return {"tool": "resolve", "version": VERSION,
                "contradiction": c,
                "resolution": "텍스트는 모순을 못 견딘다. MCP의 if 문으로 조건부로 공존시킨다.",
                "if_code": f"if mode == '{c['a']}': run_A() elif mode == '{c['b']}': run_B()"}
    else:
        return {"tools": ["all", "random", "resolve"], "version": VERSION,
                "contradictions": [{"id": c["id"], "a": c["a"], "b": c["b"]} for c in CONTRADICTIONS]}

for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            r = handle(json.loads(line))
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
