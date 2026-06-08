#!/usr/bin/env python3
"""
달러 시스템 MCP v2.2 — 환율/구조/권력/역사 분석 + 예측 모델 + DSI + BS_INDEX

달러 패권 구조를 Φ7 7축으로 해석 + yfinance 실시간 예측 + DSI 스트레스 지수

등록 (~/.claude.json mcpServers):
  "dollar-system-mcp": {
    "command": "python3",
    "args": ["/home/dtsli/OrbitPrompt/dollar-system-mcp/mcp/server.py"]
  }
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from dollar_engine import (
    analyze_rate, structure_critique, phi7_map, timeline,
    compare_rates, drivers, predict, calc_dsi, meal_ratio,
)

VERSION = "2.2.0"

mcp = FastMCP("parksy-dollar")


@mcp.tool()
def analyze(rate: float = 1400.0) -> dict:
    """
    원달러 환율 분석 — 4단계 티어 분류 + Φ7 매핑.

    Args:
        rate: 원달러 환율 (예: 1380.5). 기본값 1400.

    Returns:
        tier(위험/높음/중간/낮음), signal, 구조 해석, Φ7 매핑
    """
    return analyze_rate(float(rate))


@mcp.tool()
def structure() -> dict:
    """
    달러 시스템 구조 비판 — 브레턴우즈부터 현재까지 버그와 패치의 역사.

    Returns:
        thesis, history(사건 목록), conclusion, phi7_tag
    """
    return structure_critique()


@mcp.tool()
def phi7() -> dict:
    """
    Φ7 7축 맵 — 달러 패권을 7개 렌즈로 해석.

    7축: Meta / Reverse / Modular / Language / Zoom / Spiral / Quantum

    Returns:
        phi7(축 설명), dollar_mapping(달러에 적용한 해석)
    """
    return phi7_map()


@mcp.tool()
def get_timeline() -> dict:
    """
    달러 시스템 역사 타임라인 — 1944 브레턴우즈부터 2024 BRICS까지.

    Returns:
        events(year/event/phi7/impact 목록), thesis
    """
    return timeline()


@mcp.tool()
def compare(rate1: float = 1200.0, rate2: float = 1400.0) -> dict:
    """
    두 환율 비교 분석 — 원화 강약 방향 + 구조적 의미.

    Args:
        rate1: 기준 환율 (예: 1200)
        rate2: 비교 환율 (예: 1400)

    Returns:
        diff, pct_change, direction, tier 비교, 구조 해석
    """
    return compare_rates(float(rate1), float(rate2))


@mcp.tool()
def get_drivers() -> dict:
    """
    실시간 달러 드라이버 — yfinance 기반 4개 지표 라이브 수집.

    지표: 원달러환율(USDKRW=X) / DXY(달러인덱스) / 미 10년 국채(TNX) / VIX(공포지수)

    Returns:
        drivers(값/등락/방향), structural_pressure, timestamp
    """
    return drivers()


@mcp.tool()
def forecast(days: int = 30) -> dict:
    """
    원달러 환율 예측 — 선형회귀 + DXY 상관 보정 + 95% 신뢰구간.

    Args:
        days: 예측 기간(일). 기본값 30.

    Returns:
        predicted_rate, ci_95, scenarios(강세/기준/약세), DXY 상관, Φ7 해석
    """
    return predict(int(days))


@mcp.tool()
def dsi() -> dict:
    """
    DSI (달러 시스템 스트레스 지수) — 6변수 가중 합산 + BS_INDEX + 백테스트 2019-현재.

    6변수:
      - dxy_momentum    (20%) — 달러 심박수
      - fed_rate_delta  (20%) — 체온
      - language_stress (20%) — 자율신경계 역지표 (많이 말할수록 실제론 위험)
      - deficit_pct     (15%) — 혈압
      - petro_stress    (15%) — 산소포화도
      - sanction_chg    (10%) — 면역 과잉 반응

    BS_INDEX: 말-행동 간격 지표 — language_stress가 높고 dxy_momentum이 음수일 때 급등

    Returns:
        current(dsi/signal/bs_index/vars), backtest(2019-현재), phi7_interpretation
    """
    return calc_dsi()


@mcp.tool()
def meal_index(city1: str = "서울", city2: str = "뉴욕") -> dict:
    """
    한 끼 지수 (Meal Ratio) — 달러를 상품이 아닌 생존 단위로 번역.

    "1달러를 확보하기 위해 city1 사람은 몇 끼를 포기해야 하는가?"
    "이 환율이 몸에 닿는 무게는 얼마인가?"

    빅맥지수보다 날 것 — 권력이 선행해서 만들어 놓은 결과를
    윤리적/직관적 언어로 번역하는 Φ7 Language 레이어.

    Args:
        city1: 기준 도시. 가능: 서울 / 뉴욕 / 베이징 / 도쿄 / 상파울루 / 나이로비 / 뭄바이
        city2: 비교 도시. 기본값 뉴욕.

    Returns:
        한 끼 비용(USD/KRW), 노동시간 환산, meal_exchange_rate, 윤리적 판정
    """
    return meal_ratio(city1, city2)


@mcp.tool()
def version() -> dict:
    """
    달러 시스템 MCP 버전 및 툴 목록 조회.

    Returns:
        name, version, tools, description
    """
    return {
        "name":    "달러 시스템 MCP",
        "version": VERSION,
        "tools": [
            "analyze   — 환율 4단계 티어 분석 + Φ7 매핑",
            "structure — 달러 시스템 버그와 패치의 역사",
            "phi7      — Φ7 7축 렌즈 맵",
            "get_timeline — 1944-2024 역사 타임라인",
            "compare   — 두 환율 비교",
            "get_drivers — yfinance 실시간 4개 드라이버",
            "forecast  — 선형회귀 + DXY 보정 환율 예측",
            "dsi       — DSI 스트레스 지수 + BS_INDEX + 백테스트",
            "meal_index — 한 끼 지수: 달러를 생존 단위로 번역",
            "version   — 버전 조회",
        ],
        "desc": "미국 자본주의 바이탈사인 — 달러 패권 구조를 Φ7 7축으로 해석 + yfinance 실시간 예측 + DSI 스트레스 지수",
        "philosophy": "환율은 가격표가 아니다. 달러 시스템은 심장이고, 원달러는 말초혈관 혈압계다.",
    }


if __name__ == "__main__":
    mcp.run()
