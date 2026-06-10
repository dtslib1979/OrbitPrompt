#!/usr/bin/env python3
"""Media MCP 서버 — 결정 엔진 + 상태 관리"""
import sys, json, os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import decide_item, get_status, promote

VERSION = "1.0.0"
ITEMS_DB = []  # in-memory (향후 JSON 파일 or SQLite)

def handle(req):
    tool = req.get("tool", "")
    params = req.get("params", {})

    if tool == "decide":
        item_id = f"mcp-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(ITEMS_DB)+1:03d}"
        result = decide_item(item_id, params)
        result["_meta"] = {"version": VERSION}
        ITEMS_DB.append(result)
        # 상태에 따른 실행 분기
        if result["state"] == "candidate":
            result["_action"] = "tts_build → upload.cjs (private)"
        elif result["state"] == "hold":
            result["_action"] = "텔레그램 검토 요청"
        elif result["state"] == "reject":
            result["_action"] = "폐기"
        return result

    elif tool == "status":
        summary = get_status(ITEMS_DB)
        summary["_meta"] = {"version": VERSION}
        return summary

    elif tool == "promote":
        result = promote(params.get("item_id", ""), ITEMS_DB)
        result["_meta"] = {"version": VERSION}
        return result

    elif tool == "items":
        state_filter = params.get("state", "")
        result = [it for it in ITEMS_DB if not state_filter or it.get("state") == state_filter]
        return {"tool": "items", "count": len(result), "items": result[-10:]}

    elif tool == "version":
        return {
            "name": "Media MCP",
            "version": VERSION,
            "tools": ["decide", "status", "promote", "items", "version"],
            "states": ["input", "reject", "hold", "draft", "candidate", "private", "public"],
            "pipeline": "rawmat MCP → Φ7 분석 MCP → decide → voice MCP → upload.cjs → 승인 → public"
        }

    else:
        return {"error": f"unknown tool '{tool}'", "tools": ["decide", "status", "promote", "items", "version"]}

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        r = handle(json.loads(line))
        print(json.dumps(r, ensure_ascii=False))
        sys.stdout.flush()
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.stdout.flush()
