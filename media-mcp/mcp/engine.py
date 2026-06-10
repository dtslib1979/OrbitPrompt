#!/usr/bin/env python3
"""Media MCP 결정 엔진 — 상태머신 + Python Rule"""
import json, sys, os
from datetime import datetime

STATES = ["input", "reject", "hold", "draft", "candidate", "private", "public"]
TRANSITIONS = {
    "input":      ["reject", "hold", "draft"],
    "draft":      ["hold", "candidate"],
    "candidate":  ["private"],
    "private":    ["public"],
}

def decide(item):
    src_cnt = item.get("source_count", 0)
    has_primary = item.get("has_primary", False)
    risk = item.get("risk_level", "low")
    conflict = item.get("conflict_flag", False)
    xcheck = item.get("xcheck_models", 0)
    conf = item.get("confidence", 0.0)
    dup = item.get("duplication", 0.0)

    if src_cnt < 2:
        return "reject", "insufficient_sources"
    if not has_primary and risk == "high":
        return "hold", "high_risk_without_primary"
    if conflict:
        return "hold", "source_conflict"
    if xcheck < 2:
        return "draft", "insufficient_crosscheck"
    if conf >= 0.80 and dup < 0.40:
        return "candidate", "threshold_passed"
    return "draft", "needs_revision"

def decide_item(item_id, params):
    state, reason = decide(params)
    return {
        "item_id": item_id,
        "state": state,
        "reason_code": reason,
        "human_review": state in ("hold", "candidate"),
        "next_step": "tts_build" if state == "candidate" else "review" if state == "hold" else "reject",
        "timestamp": datetime.now().isoformat()
    }

def get_status(items):
    counts = {s: 0 for s in STATES}
    for item in items:
        s = item.get("state", "input")
        counts[s] = counts.get(s, 0) + 1
    return {"items": len(items), "states": counts}

def promote(item_id, items):
    for item in items:
        if item.get("item_id") == item_id:
            cur = item.get("state", "input")
            if cur == "private":
                item["state"] = "public"
                item["promoted_at"] = datetime.now().isoformat()
                return {"item_id": item_id, "from": cur, "to": "public", "status": "approved"}
            elif cur == "candidate":
                item["state"] = "private"
                item["promoted_at"] = datetime.now().isoformat()
                return {"item_id": item_id, "from": cur, "to": "private", "status": "moved_to_private"}
            return {"item_id": item_id, "error": f"cannot promote from {cur}"}
    return {"item_id": item_id, "error": "not_found"}

if __name__ == "__main__":
    import sys, json
    if "--decide" in sys.argv:
        i = sys.argv.index("--decide")
        params = json.loads(sys.argv[i+1])
        print(json.dumps(decide_item("test-001", params), ensure_ascii=False, indent=2))
    else:
        print("--decide '{\"source_count\":3,\"has_primary\":true,\"confidence\":0.84}'")
