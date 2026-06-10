#!/usr/bin/env python3
"""Media MCP 결정 엔진 — 상태머신 + Python Rule + 겸손/확증편향 방지"""

import json, os, sys
from datetime import datetime

STATES = ["input", "reject", "hold", "draft", "candidate", "private", "public"]
TRANSITIONS = {
    "input":      ["reject", "hold", "draft"],
    "draft":      ["hold", "candidate"],
    "candidate":  ["private"],
    "private":    ["public"],
}

# ─── 겸손/확증편향 방지 룰 ──────────────────────────────
# Flux 슬롯: 사람 대면 기록 저장소
FLUX_LOG = []

def decide(item):
    """
    결정 규칙 v2.0 — 확증편향 방지 룰 포함
    """
    src_cnt = item.get("source_count", 0)
    has_primary = item.get("has_primary", False)
    risk = item.get("risk_level", "low")
    conflict = item.get("conflict_flag", False)
    xcheck = item.get("xcheck_models", 0)
    conf = item.get("confidence", 0.0)
    dup = item.get("duplication", 0.0)
    
    # 입력 추가: 반대 의견 여부, 선호 채널 여부
    has_hostile = item.get("has_hostile_source", False)  # 반대 입장 소스
    familiar_only = item.get("familiar_only", False)      # 좋아하는 채널만?
    
    # ── 확증편향 방지 룰 ──
    
    # 룰 1: 반대 의견 없으면 위험도 상향
    if not has_hostile and src_cnt >= 2:
        risk = "high"
        conflict = True
    
    # 룰 2: 좋아하는 채널만 있으면 hold
    if familiar_only and src_cnt >= 2:
        return "hold", "confirmation_bias_familiar_only"
    
    # 룰 3: hostile source 없고 리스크 높으면 hold
    if not has_hostile and risk == "high":
        return "hold", "confirmation_bias_no_hostile"
    
    # ── 기존 결정 규칙 ──
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
    warnings = []
    
    # 확증편향 경고
    if not params.get("has_hostile_source", False) and params.get("source_count", 0) >= 2:
        warnings.append("⚠️ 반대 입장 소스 없음 — 확증편향 가능성")
    if params.get("familiar_only", False):
        warnings.append("⚠️ 친숙한 채널만 입력됨 — 다양성 부족")
    
    return {
        "item_id": item_id,
        "state": state,
        "reason_code": reason,
        "warnings": warnings,
        "human_review": state in ("hold", "candidate"),
        "next_step": "tts_build" if state == "candidate" else "review" if state == "hold" else "reject" if state == "reject" else "draft_work",
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


# ─── Flux 슬롯 (사람 대면 기록) ──────────────────────────

def flux_log(entry):
    """
    사람 대면 내용 기록 (청취 전용, 분석 금지)
    
    entry = {
        "date": "2026-06-09",
        "type": "offline_meeting" | "discord" | "phone" | "family",
        "summary": "무슨 이야기를 들었는지 (MCP 분석 말고 있는 그대로)",
        "feeling": "내 감정 상태",
        "key_points": ["중요하게 들은 것들"],
        "action_later": "나중에 MCP에 넣을 것들 (선택사항)"
    }
    """
    entry["_logged_at"] = datetime.now().isoformat()
    FLUX_LOG.append(entry)
    return {
        "status": "logged",
        "note": "분석하지 않음. 기록만 저장.",
        "total_entries": len(FLUX_LOG),
        "last_date": entry.get("date", "unknown")
    }


def flux_list(limit=10):
    """Flux 슬롯 기록 조회 (최근 N개)"""
    recent = FLUX_LOG[-limit:] if FLUX_LOG else []
    return {
        "total": len(FLUX_LOG),
        "recent": recent,
        "note": "이 기록은 MCP 분석 대상이 아님. 사람 말을 그대로 보존."
    }


def flux_stats():
    """Flux 슬롯 통계 (분석이 아니라 단순 집계)"""
    types = {}
    for entry in FLUX_LOG:
        t = entry.get("type", "unknown")
        types[t] = types.get(t, 0) + 1
    return {
        "total_entries": len(FLUX_LOG),
        "by_type": types,
        "purpose": "사람 말을 듣는 슬롯. 분석 금지. 청취만."
    }


# ─── 분기별 자기검증 ────────────────────────────────────
REVIEW_LOG = []

def log_review_case(case):
    """
    MCP가 틀린 케이스 기록
    
    case = {
        "date": "2026-06-09",
        "system_decision": "reject" | "hold" | "draft",
        "actual_result": "실제로는 중요한 신호였음",
        "lesson": "무엇을 배웠는지",
        "rule_update_needed": True | False
    }
    """
    case["_logged_at"] = datetime.now().isoformat()
    REVIEW_LOG.append(case)
    total_wrong = len([c for c in REVIEW_LOG if c.get("actual_result") != c.get("system_decision")])
    return {
        "status": "logged",
        "total_cases": len(REVIEW_LOG),
        "total_wrong": total_wrong,
        "humility_note": f"MCP가 {total_wrong}번 틀렸습니다. 시스템이 완벽하지 않습니다."
    }


def get_review_summary():
    wrong = [c for c in REVIEW_LOG if c.get("actual_result") != c.get("system_decision")]
    return {
        "total_cases": len(REVIEW_LOG),
        "wrong_cases": len(wrong),
        "wrong_details": wrong[-5:],
        "message": f"지금까지 MCP가 {len(wrong)}번 틀렸습니다. 겸손해질 필요가 있습니다."
    }


if __name__ == "__main__":
    import sys, json
    if "--decide" in sys.argv:
        i = sys.argv.index("--decide")
        params = json.loads(sys.argv[i+1])
        r = decide_item("test-001", params)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif "--flux" in sys.argv:
        print("Flux 슬롯 — 사람 말을 듣는 채널. 분석 금지.")
    elif "--review" in sys.argv:
        print(json.dumps(get_review_summary(), ensure_ascii=False, indent=2))
    else:
        print("--decide '{...}' | --flux | --review")
