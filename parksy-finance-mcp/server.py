"""
parksy-finance MCP 서버 v2.0

12개 재무비율 시계 × 5개 관점(Form/Flow/Frag/Field/Fit) = 60개 분석 슬롯.
각 좌표를 60갑자 국면으로 즉시(P0) 또는 LLM 서사로(P1) 해석.

도구 8개:
  P0 (결정론적, LLM 없음):
    narrative_explain   — 좌표 → 갑자 국면 즉시 반환
    gapja_info          — 1~60 인덱스 → 갑자 전체 조회
    score_position      — 수치 입력 → 상대 점수 + 국면 판단
    compare_positions   — 여러 좌표 병렬 비교
    list_slots          — 60개 슬롯 전체 목록

  P1 (LLM 연동):
    analyze_position    — 좌표 + 컨텍스트 → LLM 서사 생성
    company_analysis    — 기업명 + 비율 딕셔너리 → 전체 국면 진단
    slot_info           — 특정 좌표 메타데이터 조회
"""

import json
import os

import anthropic as _anthropic
from mcp.server.fastmcp import FastMCP

from gapja_master import (
    PHASE_MEANINGS,
    get_gapja,
    get_gapja_by_index,
)
from prompt_builder import build
from ratio_map import SMART_CLAND_AXES, all_slots, describe_slot, get_names, slot_id
from schema import AnalyzeInput

# ---------------------------------------------------------------------------
# LLM 클라이언트
# ---------------------------------------------------------------------------

_llm_client = None


def get_llm():
    global _llm_client
    if _llm_client is not None:
        return _llm_client

    provider = os.environ.get("PARKSY_FINANCE_LLM", "anthropic")

    if provider == "anthropic":
        _llm_client = _anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
    elif provider == "openai":
        from openai import OpenAI
        _llm_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    elif provider == "deepseek":
        from openai import OpenAI
        _llm_client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")

    return _llm_client


def _call_llm(sys_p: str, user_p: str) -> str:
    llm = get_llm()
    model = os.environ.get(
        "PARKSY_FINANCE_MODEL",
        "claude-sonnet-4-20250514" if isinstance(llm, _anthropic.Anthropic) else "deepseek-chat",
    )

    if isinstance(llm, _anthropic.Anthropic):
        resp = llm.messages.create(
            model=model,
            max_tokens=1200,
            system=sys_p,
            messages=[{"role": "user", "content": user_p}],
        )
        return resp.content[0].text
    else:
        resp = llm.chat.completions.create(
            model=model,
            max_tokens=1200,
            messages=[
                {"role": "system", "content": sys_p},
                {"role": "user", "content": user_p},
            ],
        )
        return resp.choices[0].message.content


# ---------------------------------------------------------------------------
# MCP 서버
# ---------------------------------------------------------------------------

mcp = FastMCP("parksy-finance")


# ── P0: 결정론적 도구 ────────────────────────────────────────────────────────


@mcp.tool()
def narrative_explain(hour: int, minute: int) -> dict:
    """LLM 없이 좌표(시·분) → 60갑자 국면 즉시 반환.

    Args:
        hour: 재무비율 시계 위치 (1~12)
        minute: 하위 관점 인덱스 (1~5)
    """
    gj = get_gapja(hour, minute)
    r_ko, r_en, p_code, p_desc = get_names(hour, minute)
    pm = PHASE_MEANINGS.get(gj["phase_code"], {})

    return {
        "slot_id": slot_id(hour, minute),
        "ratio_ko": r_ko,
        "ratio_en": r_en,
        "perspective": f"{p_code} — {p_desc}",
        "gapja": gj["hanja"],
        "gapja_ko": gj["hangul"],
        "ohaeng": gj["ohaeng"],
        "phase": pm.get("ko", gj["phase_code"]),
        "story": gj["story"],
        "signal": pm.get("signal", ""),
        "index": gj["index"],
    }


@mcp.tool()
def gapja_info(index: int) -> dict:
    """1~60 인덱스로 갑자 전체 메타데이터 조회.

    Args:
        index: 갑자 순번 (1=甲子 … 60=癸亥)
    """
    gj = get_gapja_by_index(index)
    pm = PHASE_MEANINGS.get(gj["phase_code"], {})
    r_ko, r_en, p_code, p_desc = get_names(gj["hour"], gj["minute"])

    return {
        **gj,
        "ratio_ko": r_ko,
        "ratio_en": r_en,
        "perspective_code": p_code,
        "perspective_desc": p_desc,
        "phase_name": pm.get("ko", gj["phase_code"]),
        "signal": pm.get("signal", ""),
    }


@mcp.tool()
def score_position(
    hour: int,
    minute: int,
    value: float,
    industry_avg: float,
    industry_best: float = 0.0,
) -> dict:
    """재무 수치를 입력해 해당 좌표의 상대 점수와 국면을 판단한다.

    Args:
        hour: 재무비율 시계 위치 (1~12)
        minute: 하위 관점 인덱스 (1~5)
        value: 해당 기업의 실제 비율 값
        industry_avg: 업계 평균값
        industry_best: 업계 최고값 (없으면 0 → 자동 추정)
    """
    r_ko, r_en, p_code, _ = get_names(hour, minute)
    gj = get_gapja(hour, minute)
    pm = PHASE_MEANINGS.get(gj["phase_code"], {})

    best = industry_best if industry_best != 0.0 else industry_avg * 1.5
    if best == industry_avg:
        best = industry_avg * 1.01

    # 0~100 상대 점수 (업계 최고 대비)
    raw_score = (value / best) * 100
    score = max(0.0, min(100.0, round(raw_score, 1)))

    # 업계 대비 판정
    ratio = value / industry_avg if industry_avg else 1.0
    if ratio >= 1.3:
        grade = "A"
        verdict = "업계 상위 — 강점 구간"
    elif ratio >= 0.9:
        grade = "B"
        verdict = "업계 평균 — 유지 구간"
    elif ratio >= 0.6:
        grade = "C"
        verdict = "업계 하위 — 개선 필요"
    else:
        grade = "D"
        verdict = "위험 구간 — 즉각 대응 필요"

    return {
        "slot_id": slot_id(hour, minute),
        "ratio_ko": r_ko,
        "perspective": p_code,
        "value": value,
        "industry_avg": industry_avg,
        "score": score,
        "grade": grade,
        "verdict": verdict,
        "gapja": gj["hanja"],
        "phase": pm.get("ko", gj["phase_code"]),
        "signal": pm.get("signal", ""),
    }


@mcp.tool()
def compare_positions(positions: list[dict]) -> list[dict]:
    """여러 좌표를 한번에 비교해 국면 맵을 반환한다.

    Args:
        positions: [{"hour": 1~12, "minute": 1~5, "label": "선택적 레이블"}, ...]
    """
    results = []
    for pos in positions:
        h, m = pos.get("hour", 1), pos.get("minute", 1)
        label = pos.get("label", "")
        try:
            r = narrative_explain(h, m)
            r["label"] = label
            results.append(r)
        except Exception as e:
            results.append({"hour": h, "minute": m, "label": label, "error": str(e)})
    return results


@mcp.tool()
def list_slots() -> list[dict]:
    """60개 전체 분석 슬롯 목록 반환 (갑자 정보 포함)."""
    slots = all_slots()
    for s in slots:
        gj = get_gapja(s["hour"], s["minute"])
        s["gapja"] = gj["hanja"]
        s["gapja_ko"] = gj["hangul"]
        s["phase_code"] = gj["phase_code"]
        pm = PHASE_MEANINGS.get(gj["phase_code"], {})
        s["phase_name"] = pm.get("ko", "")
    return slots


# ── P1: LLM 도구 ─────────────────────────────────────────────────────────────


@mcp.tool()
def analyze_position(
    hour: int,
    minute: int,
    context: str = "",
    axis: str = "",
) -> dict:
    """재무비율 시계 좌표 + 컨텍스트 → LLM 60갑자 서사 생성.

    Args:
        hour: 재무비율 시계 위치 (1~12)
        minute: 하위 관점 인덱스 (1~5)
        context: 기업명 / 추가 데이터 / 키워드 (선택)
        axis: SMART/CLAND 해석 축 (S/M/A/R/T/C/L/A2/N/D, 선택)
    """
    inp = AnalyzeInput(
        hour=hour, minute=minute,
        context=context or None, axis=axis or None,
    )
    sys_p, user_p = build(inp.hour, inp.minute, inp.context, inp.axis)
    raw = _call_llm(sys_p, user_p)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        import re
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        data = json.loads(m.group()) if m else {}

    r_ko, r_en, p_code, p_desc = get_names(inp.hour, inp.minute)
    gj = get_gapja(inp.hour, inp.minute)

    result = {
        "slot_id": slot_id(inp.hour, inp.minute),
        "ratio_name_ko": r_ko,
        "ratio_name_en": r_en,
        "perspective_code": p_code,
        "perspective_desc": p_desc,
        "gapja": gj["hanja"],
        "gapja_ko": gj["hangul"],
        "phase": PHASE_MEANINGS.get(gj["phase_code"], {}).get("ko", ""),
        "raw_ratio_block": data.get("raw_ratio_block", ""),
        "story_blocks": data.get("story_blocks", [gj["story"]]),
        "prompt_suggestions": data.get("prompt_suggestions", []),
    }

    if inp.axis:
        a_en, a_ko = SMART_CLAND_AXES.get(inp.axis, ("", ""))
        result["axis_analysis"] = {
            "code": inp.axis,
            "name_en": a_en,
            "name_ko": a_ko,
        }

    return result


@mcp.tool()
def company_analysis(
    company: str,
    ratios: dict,
) -> dict:
    """기업의 재무 비율 딕셔너리를 입력해 전체 국면 진단을 반환한다.

    Args:
        company: 기업명 또는 티커 (예: "삼성전자", "AAPL")
        ratios: {비율명: 수치} 딕셔너리. 지원 키:
            revenue_growth, revenue_scale, gross_margin, op_margin, net_margin,
            roe, roic, asset_turnover, inventory_turnover,
            debt_ratio, interest_coverage, per (또는 psr)
    """
    KEY_MAP = {
        "revenue_growth":    (1, "매출 성장률"),
        "revenue_scale":     (2, "매출 규모"),
        "gross_margin":      (3, "매출총이익률"),
        "op_margin":         (4, "영업이익률"),
        "net_margin":        (5, "순이익률"),
        "roe":               (6, "ROE"),
        "roic":              (7, "ROIC"),
        "asset_turnover":    (8, "자산회전율"),
        "inventory_turnover":(9, "재고회전율"),
        "debt_ratio":        (10, "부채비율"),
        "interest_coverage": (11, "이자보상배율"),
        "per":               (12, "PER"),
        "psr":               (12, "PSR"),
    }

    slots_hit = []
    for key, val in ratios.items():
        if key not in KEY_MAP:
            continue
        hour, label = KEY_MAP[key]
        # 재무 특성에 따라 최적 관점(minute) 자동 선택
        # 성장률·규모 → Form(1), 수익성 → Flow(2), 부채·이자 → Frag(3)
        # 회전율 → Field(4), 밸류에이션 → Fit(5)
        minute_hint = {1: 1, 2: 1, 3: 2, 4: 2, 5: 2,
                       6: 2, 7: 2, 8: 4, 9: 4, 10: 3, 11: 3, 12: 5}
        minute = minute_hint.get(hour, 1)
        gj = get_gapja(hour, minute)
        pm = PHASE_MEANINGS.get(gj["phase_code"], {})
        slots_hit.append({
            "ratio": label,
            "value": val,
            "slot_id": slot_id(hour, minute),
            "gapja": gj["hanja"],
            "gapja_ko": gj["hangul"],
            "phase": pm.get("ko", gj["phase_code"]),
            "signal": pm.get("signal", ""),
            "story": gj["story"],
        })

    # 국면 빈도 집계
    phase_counts: dict[str, int] = {}
    for s in slots_hit:
        phase_counts[s["phase"]] = phase_counts.get(s["phase"], 0) + 1
    dominant = max(phase_counts, key=phase_counts.get) if phase_counts else "분석 부족"

    return {
        "company": company,
        "slots": slots_hit,
        "dominant_phase": dominant,
        "phase_distribution": phase_counts,
        "summary": f"{company}의 {len(slots_hit)}개 비율 분석 완료. 지배 국면: {dominant}",
    }


@mcp.tool()
def slot_info(hour: int, minute: int) -> dict:
    """특정 좌표의 슬롯 메타데이터 + 갑자 정보 반환.

    Args:
        hour: 재무비율 시계 위치 (1~12)
        minute: 하위 관점 인덱스 (1~5)
    """
    base = describe_slot(hour, minute)
    gj = get_gapja(hour, minute)
    pm = PHASE_MEANINGS.get(gj["phase_code"], {})
    return {
        **base,
        "gapja": gj["hanja"],
        "gapja_ko": gj["hangul"],
        "ohaeng": gj["ohaeng"],
        "phase": pm.get("ko", gj["phase_code"]),
        "signal": pm.get("signal", ""),
        "story": gj["story"],
    }


# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
