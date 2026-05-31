"""
parksy-finance MCP 서버

12개 재무비율 시계 × 5개 관점(Form/Flow/Frag/Field/Fit) = 60개 분석 슬롯.
각 좌표를 LLM이 60갑자 서사로 자동 해석.

사용 예:
  claude mcp add parksy-finance -- python /path/to/server.py
"""

import json
import os
import sys

from mcp.server.fastmcp import FastMCP

from ratio_map import slot_id, get_names, describe_slot, all_slots
from schema import AnalyzeInput
from prompt_builder import build

# ---------------------------------------------------------------------------
# LLM 클라이언트 — 여러 백엔드 지원
# ---------------------------------------------------------------------------

_llm_client = None


def get_llm():
    global _llm_client
    if _llm_client is not None:
        return _llm_client

    provider = os.environ.get("PARKSY_FINANCE_LLM", "anthropic")

    if provider == "anthropic":
        import anthropic

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        _llm_client = anthropic.Anthropic(api_key=api_key)

    elif provider == "openai":
        from openai import OpenAI

        api_key = os.environ.get("OPENAI_API_KEY")
        _llm_client = OpenAI(api_key=api_key)

    elif provider == "deepseek":
        from openai import OpenAI

        api_key = os.environ.get("DEEPSEEK_API_KEY")
        _llm_client = OpenAI(
            api_key=api_key, base_url="https://api.deepseek.com"
        )

    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

    return _llm_client


# ---------------------------------------------------------------------------
# MCP 서버
# ---------------------------------------------------------------------------

mcp = FastMCP("parksy-finance", description="재무비율 시계 × 60갑자 MCP 분석 엔진")


@mcp.tool()
def analyze_position(
    hour: int,
    minute: int,
    context: str = "",
    axis: str = "",
) -> dict:
    """재무비율 시계 좌표(시·분)로 국면 분석 + 60갑자 서사 생성.

    Args:
        hour: 재무비율 시계 위치 (1~12)
        minute: 하위 관점 인덱스 (1~5)
        context: 기업명 / 추가 데이터 / 키워드 (선택)
        axis: SMART/CLAND 해석 축 (S/M/A/R/T/C/L/A2/N/D, 선택)
    """
    inp = AnalyzeInput(
        hour=hour,
        minute=minute,
        context=context or None,
        axis=axis or None,
    )

    sys_p, user_p = build(inp.hour, inp.minute, inp.context, inp.axis)
    llm = get_llm()

    r_ko, r_en, p_code, p_desc = get_names(inp.hour, inp.minute)

    # LLM 호출
    if isinstance(llm.__class__.__name__, str) and "Anthropic" in llm.__class__.__name__:
        resp = llm.messages.create(
            model=os.environ.get("PARKSY_FINANCE_MODEL", "claude-sonnet-4-20250514"),
            max_tokens=1000,
            system=sys_p,
            messages=[{"role": "user", "content": user_p}],
        )
        raw = resp.content[0].text
    else:
        # OpenAI-compatible
        resp = llm.chat.completions.create(
            model=os.environ.get("PARKSY_FINANCE_MODEL", "deepseek-chat"),
            max_tokens=1000,
            messages=[
                {"role": "system", "content": sys_p},
                {"role": "user", "content": user_p},
            ],
        )
        raw = resp.choices[0].message.content

    data = json.loads(raw)

    result = {
        "slot_id": slot_id(inp.hour, inp.minute),
        "ratio_name_ko": r_ko,
        "ratio_name_en": r_en,
        "perspective_code": p_code,
        "perspective_desc": p_desc,
        "raw_ratio_block": data.get("raw_ratio_block", ""),
        "story_blocks": data.get("story_blocks", []),
        "prompt_suggestions": data.get("prompt_suggestions", []),
    }

    if inp.axis:
        from ratio_map import SMART_CLAND_AXES

        a_en, a_ko = SMART_CLAND_AXES.get(inp.axis, ("", ""))
        result["axis_analysis"] = {
            "code": inp.axis,
            "name_en": a_en,
            "name_ko": a_ko,
        }

    return result


@mcp.tool()
def list_slots() -> list[dict]:
    """60개 전체 분석 슬롯 목록을 반환합니다."""
    return all_slots()


@mcp.tool()
def slot_info(hour: int, minute: int) -> dict:
    """특정 좌표의 슬롯 메타데이터를 반환합니다.

    Args:
        hour: 재무비율 시계 위치 (1~12)
        minute: 하위 관점 인덱스 (1~5)
    """
    return describe_slot(hour, minute)


# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
