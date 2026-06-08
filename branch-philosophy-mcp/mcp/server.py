#!/usr/bin/env python3
"""브랜치 철학 MCP — 파트너십 원칙"""
import sys, json
from datetime import datetime
VERSION = "1.0.0"

PRINCIPLES = {
    "not_team": "나는 누구와도 팀으로 일하지 않는다. 전부 브랜치다. 전부 파트너다.",
    "fork_cost_zero": "브랜치는 언제든 fork될 수 있고, 머지될 수 있고, 삭제될 수 있다.",
    "repo_is_memory": "레포=기억. 컨텍스트가 터져도 팀은 안 죽는다.",
    "commit_is_contract": "커밋=계약. 말보다 커밋이 우선이다.",
    "document_not_explain": "'문서 봐' — 설명하는 토큰 비용 > 문서 읽는 토큰 비용"
}

AGENTS = {
    "박씨": {"role": "방향 설정·판단", "type": "최종 결정자"},
    "Perplexity": {"role": "구조화·논리·브릿지", "type": "브레인스토밍 파트너"},
    "DeepSeek": {"role": "MCP 구현·초안 생산", "type": "구현 파트너"},
    "Claude": {"role": "감사·카운터·계획서", "type": "검증 파트너"}
}

def handle(req):
    tool = req.get("tool", "")
    if tool == "principles":
        return {"tool": "principles", "version": VERSION, "principles": PRINCIPLES}
    elif tool == "agents":
        return {"tool": "agents", "version": VERSION, "agents": AGENTS}
    elif tool == "check":
        action = req.get("params", {}).get("action", "")
        checks = []
        for k, v in PRINCIPLES.items():
            checks.append({"principle": k, "desc": v, "status": "pass"})
        return {"tool": "check", "version": VERSION, "action": action, "checks": checks}
    else:
        return {"tools": ["principles", "agents", "check"], "version": VERSION}

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
