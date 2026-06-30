#!/usr/bin/env python3
"""
Module 8 — Accumulation Signal Logger (백서 13장 + 허생전 프로토콜)

기록 전용 로거. 절대 매매하지 않음.
신호만 쌓는다. 최소 8회(반기단위 4년치) 누적 전까지 자본투입 금지.

허생전 프로토콜 1단계:
  Module 8이 신호를 낼 때마다 signal_log.json에 기록.
  반기(6개월)를 1 observation round로 간주.
  같은 반기 내 여러 신호 = 같은 round로 묶임.
  최소 8개 반기(4년)에 걸친 분산 신호 필요.
"""

import json, os
from datetime import datetime
from typing import Optional

# 로그 파일 경로 (MCP 서버 기준 상대경로)
_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
_LOG_PATH = os.path.join(_LOG_DIR, "signal_log.json")

# ─── 시그널 기준 (백서 13.3절) ──────────────────────────────────────────────────

_SIGNAL_WEIGHTS = {
    "won_overvaluation": {
        "label": "원화 일시 고평가",
        "max_strength": 0.35,
        "source": "12장 Rolling Forecast 대비 일시 고평가 윈도우",
    },
    "treasury_watchlist": {
        "label": "재무부 모니터링 리스트 압박",
        "max_strength": 0.25,
        "source": "7장 재무부 FX Report 등재 → 압박 윈도우 진입",
    },
    "fed_hike_cycle": {
        "label": "Fed 긴축 사이클 초입",
        "max_strength": 0.25,
        "source": "9.3절 FOMC 신호 — CME FedWatch 확률 급등",
    },
    "dsi_stress": {
        "label": "DSI 스트레스 경고",
        "max_strength": 0.20,
        "source": "DSI v2.2 65초과 → 손실전가 가속 구간 진입",
    },
    "gold_discount": {
        "label": "금 가격 일시 조정",
        "max_strength": 0.15,
        "source": "금 가격 30일 이동평균 대비 -5% 이상 하락",
    },
    "regime_change": {
        "label": "GATE 0 체제변화 감지",
        "max_strength": 0.20,
        "source": "14장 GATE 0 regime_change_flag=True → 정책 전환 신호",
    },
}

_SIGNAL_TYPES = list(_SIGNAL_WEIGHTS.keys())


def _ensure_log_dir():
    """로그 디렉토리 생성"""
    os.makedirs(_LOG_DIR, exist_ok=True)


def _get_semi_annual_key(timestamp_str: str) -> str:
    """타임스탬프 → 반기 키 (예: '2026-06-30 13:59 KST' → '2026H1')"""
    try:
        dt = datetime.strptime(timestamp_str.split(" ")[0], "%Y-%m-%d")
        h = "H1" if dt.month <= 6 else "H2"
        return f"{dt.year}{h}"
    except Exception:
        return "unknown"


def _load_log() -> list:
    """기존 로그 로드"""
    if not os.path.exists(_LOG_PATH):
        return []
    try:
        with open(_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return []


def _save_log(entries: list):
    """로그 저장"""
    _ensure_log_dir()
    with open(_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def record_signal(
    signal_type: str,
    strength: float,
    basis: str,
    metadata: Optional[dict] = None,
) -> dict:
    """
    시그널 기록 (기록 전용. 매매 금지.)

    Args:
        signal_type: 시그널 종류
        strength: 시그널 강도 (0.0 ~ 1.0)
        basis: 시그널 발생 근거 (자연어 설명)
        metadata: 추가 메타데이터 (선택)

    Returns:
        기록된 시그널 엔트리 + 누적 통계
    """
    if signal_type not in _SIGNAL_TYPES:
        valid = ", ".join(_SIGNAL_TYPES)
        return {"error": f"알 수 없는 시그널 타입: {signal_type}. 유효: {valid}"}

    strength = max(0.0, min(1.0, float(strength)))
    max_st = _SIGNAL_WEIGHTS[signal_type]["max_strength"]
    if strength > max_st:
        strength = max_st

    entry = {
        "id": f"SIG-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{signal_type}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
        "signal_type": signal_type,
        "signal_label": _SIGNAL_WEIGHTS[signal_type]["label"],
        "strength": round(strength, 3),
        "max_strength": max_st,
        "strength_ratio": round(strength / max_st * 100, 1) if max_st > 0 else 0,
        "basis": basis,
        "metadata": metadata or {},
    }

    log = _load_log()
    log.append(entry)
    _save_log(log)

    stats = get_stats()

    return {
        "recorded": entry,
        "cumulative": {
            "total_signals": stats["total_signals"],
            "distinct_rounds": stats["distinct_rounds"],
            "unique_types": stats["unique_types"],
            "date_range": stats["date_range"],
            "avg_strength": stats["avg_strength"],
            "min_rounds_before_capital": 8,
            "capital_deployment_allowed": stats["distinct_rounds"] >= 8,
            "rule": "최소 8개 반기(4년) 분산 누적 전 자본투입 금지 (허생전 프로토콜)",
        },
    }


def get_stats() -> dict:
    """시그널 누적 통계 — 반기(半期) 단위 독립 round 카운트"""
    log = _load_log()

    if not log:
        return {
            "total_signals": 0,
            "distinct_rounds": 0,
            "unique_types": 0,
            "date_range": "N/A",
            "avg_strength": 0.0,
            "type_breakdown": {},
            "rounds": [],
            "recent_signals": [],
            "capital_deployment_allowed": False,
            "min_rounds_before_capital": 8,
            "rounds_needed": 8,
        }

    timestamps = [e["timestamp"] for e in log if "timestamp" in e]
    strengths = [e["strength"] for e in log if "strength" in e]
    types = {}
    for e in log:
        st = e.get("signal_type", "unknown")
        types[st] = types.get(st, 0) + 1

    # 반기 단위 grouping
    rounds: dict[str, dict] = {}
    for e in log:
        ts = e.get("timestamp", "")
        round_key = _get_semi_annual_key(ts)
        if round_key not in rounds:
            rounds[round_key] = {
                "round": round_key,
                "signal_count": 0,
                "types_observed": set(),
                "total_strength": 0.0,
                "first_signal": ts,
            }
        rounds[round_key]["signal_count"] += 1
        rounds[round_key]["types_observed"].add(e.get("signal_type", "unknown"))
        rounds[round_key]["total_strength"] += e.get("strength", 0)

    # round 목록 정렬 (오래된 순)
    sorted_round_keys = sorted(rounds.keys())
    round_list = []
    for rk in sorted_round_keys:
        r = rounds[rk]
        round_list.append({
            "round": r["round"],
            "signals": r["signal_count"],
            "types": len(r["types_observed"]),
            "total_strength": round(r["total_strength"], 3),
        })

    distinct_rounds = len(rounds)
    recent = sorted(log, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]

    return {
        "total_signals": len(log),
        "distinct_rounds": distinct_rounds,
        "unique_types": len(types),
        "date_range": f"{timestamps[-1][:10]} ~ {timestamps[0][:10]}" if len(timestamps) >= 2 else timestamps[0][:10] if timestamps else "N/A",
        "avg_strength": round(sum(strengths) / len(strengths), 3) if strengths else 0.0,
        "total_strength": round(sum(strengths), 3) if strengths else 0.0,
        "type_breakdown": types,
        "rounds": round_list,
        "recent_signals": recent,
        "capital_deployment_allowed": distinct_rounds >= 8,
        "min_rounds_before_capital": 8,
        "rounds_needed": max(0, 8 - distinct_rounds),
    }


def get_log(limit: int = 50, signal_type: Optional[str] = None) -> list:
    """
    로그 조회.

    Args:
        limit: 최근 N개
        signal_type: 특정 타입 필터 (선택)
    """
    log = _load_log()
    log.reverse()

    if signal_type:
        log = [e for e in log if e.get("signal_type") == signal_type]

    return log[:limit]


def clear_log(confirm: bool = False) -> dict:
    """로그 초기화 (테스트용)"""
    if not confirm:
        return {"error": "confirm=True 필요"}
    _save_log([])
    return {"status": "cleared", "message": "시그널 로그 초기화 완료"}


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--stats":
        print(json.dumps(get_stats(), ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--clear":
        print(json.dumps(clear_log(confirm="--force" in sys.argv), ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # 데모: 3개 시그널 기록
        demo_signals = [
            ("dsi_stress", 0.72, "DSI 68.3 — 손실전가 가속 구간"),
            ("won_overvaluation", 0.55, "12장 모델 대비 원화 3.2% 고평"),
            ("fed_hike_cycle", 0.60, "FOMC 점도표 상향 — 긴축 사이클 신호"),
        ]
        results = []
        for sig_type, strength, basis in demo_signals:
            r = record_signal(sig_type, strength, basis)
            results.append(r["recorded"])
        print(json.dumps({"recorded": len(results), "signals": results}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(get_stats(), ensure_ascii=False, indent=2))
