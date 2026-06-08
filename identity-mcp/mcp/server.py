#!/usr/bin/env python3
"""ID-MANIFEST MCP — 정체성 조회/분석/업데이트"""
import sys, json, os
from datetime import datetime
VERSION = "1.0.0"

IDENTITY = {
    "name": "박태정",
    "aliases": ["철학자 박씨", "인프라 실험자", "워킹 클래스 아웃라이어", "마지막 아담", "브랜치 파트너"],
    "six_lines": {
        "01": {"label": "구조주의자", "desc": "위계와 차별 요소가 이미 설정된 구조를 인정하고 그 안에서 움직인다"},
        "02": {"label": "생철학자", "desc": "삶과 철학이 분리되지 않는다. 두 개가 동시에 있다"},
        "03": {"label": "아웃라이어", "desc": "5년 최저시급 12시간 알바 + 2년 자비출판. 엘리트와 재료가 다르다"},
        "04": {"label": "엔지니어", "desc": "철학을 코드로 구현한다. 말에서 끝나지 않는다"},
        "05": {"label": "메타모델러", "desc": "나 자신까지 파라미터로 올려놓고 조정한다"},
        "06": {"label": "브랜치 파트너", "desc": "팀장 아니다. 전부 브랜치다. fork 비용 0"}
    },
    "positioning": "AI 시대 정치 인프라 제작자. 첫 슬롯이 박찬대였을 뿐.",
    "manifesto": "레포에 저장했다. 커밋했다. 끝."
}

def handle(req):
    tool = req.get("tool", "")
    if tool == "identity":
        return {"tool": "identity", "version": VERSION, "identity": IDENTITY}
    elif tool == "aliases":
        return {"tool": "aliases", "version": VERSION, "aliases": IDENTITY["aliases"]}
    elif tool == "six_lines":
        return {"tool": "six_lines", "version": VERSION, "six_lines": IDENTITY["six_lines"]}
    elif tool == "compare":
        target = req.get("params", {}).get("alias", "")
        matches = [a for a in IDENTITY["aliases"] if target in a]
        return {"tool": "compare", "version": VERSION, "query": target, "matches": matches}
    else:
        return {"tools": ["identity", "aliases", "six_lines", "compare"], "version": VERSION}

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
