#!/usr/bin/env python3
"""Media MCP 서버 — 결정 엔진 + Flux 슬롯 + 확증편향 방지"""
import sys, json, os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import decide_item, get_status, promote, flux_log, flux_list, flux_stats, log_review_case, get_review_summary

VERSION = "2.0.0"
ITEMS_DB = []

def handle(req):
    tool = req.get("tool", "")
    params = req.get("params", {})

    if tool == "decide":
        item_id = f"mcp-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(ITEMS_DB)+1:03d}"
        result = decide_item(item_id, params)
        result["_meta"] = {"version": VERSION}
        ITEMS_DB.append(result)
        if result["state"] == "candidate":
            result["_action"] = "tts_build → upload.cjs (private)"
        elif result["state"] == "hold":
            reason = result.get("reason_code", "")
            if "confirmation_bias" in reason:
                result["_action"] = "🔴 확증편향 경고 — 반대 의견 또는 다양한 채널 입력 필요"
            else:
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

    # ─── Flux 슬롯 (사람 대면) ────────────────────────
    elif tool == "flux_log":
        result = flux_log({
            "date": params.get("date", datetime.now().strftime("%Y-%m-%d")),
            "type": params.get("type", "offline_meeting"),
            "summary": params.get("summary", ""),
            "feeling": params.get("feeling", ""),
            "key_points": params.get("key_points", []),
            "action_later": params.get("action_later", "")
        })
        result["_meta"] = {"version": VERSION}
        return result

    elif tool == "flux_list":
        result = flux_list(params.get("limit", 10))
        result["_meta"] = {"version": VERSION}
        return result

    elif tool == "flux_stats":
        result = flux_stats()
        result["_meta"] = {"version": VERSION}
        return result

    # ─── 자기검증 ────────────────────────────────────
    elif tool == "review_log":
        result = log_review_case({
            "date": params.get("date", datetime.now().strftime("%Y-%m-%d")),
            "system_decision": params.get("system_decision", ""),
            "actual_result": params.get("actual_result", ""),
            "lesson": params.get("lesson", ""),
            "rule_update_needed": params.get("rule_update_needed", False)
        })
        result["_meta"] = {"version": VERSION}
        return result

    elif tool == "review_summary":
        result = get_review_summary()
        result["_meta"] = {"version": VERSION}
        return result

    elif tool == "version":
        return {
            "name": "Media MCP",
            "version": VERSION,
            "description": "주의력 방어벽 — 진실 발견 시스템이 아님",
            "tools": ["decide", "status", "promote", "items", "flux_log", "flux_list", "flux_stats", "review_log", "review_summary", "version"],
            "states": ["input", "reject", "hold", "draft", "candidate", "private", "public"],
            "features": {
                "confirmation_bias_prevention": True,
                "flux_slot": "사람 말을 듣는 채널. 분석 금지. 청취만.",
                "humility_check": "MCP가 틀린 케이스를 기록합니다."
            }
        }

    else:
        return {"error": f"unknown tool '{tool}'", "tools": [
            "decide", "status", "promote", "items",
            "flux_log", "flux_list", "flux_stats",
            "review_log", "review_summary", "version"
        ]}

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
