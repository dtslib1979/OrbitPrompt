#!/usr/bin/env python3
"""
Module 13 — Sonho (Small Office/Home Office) Fee Calculator (PEM Q3: 물성×미시)

소호스튜디오 임대료 헤게모니 수수료 + 매력 자본 계수 측정.
namoneygoal(부동산/길드), hoyadang.com(식당), obokzip(물리스튜디오) 데이터 기반.

역산 모델 2종:
  1. 소호_임대료_헤게모니수수료 = 공방매출 - (임대료+장비감가상각+관리비)
  2. 매력_자본_계수 = 길드_모집_응답률 / (마케팅비 + 시간비용)

의존성:
  - hegemonic_fee.py: 계산식 패턴 재사용
"""

from datetime import datetime
from typing import Optional

SOURCE_TIER_PENALTY = {
    "S급": 1.0,
    "A급": 0.9,
    "B급": 0.7,
    "C급": 0.5,
}

COMMON_DISCLAIMER = {
    "analysis_type": "사후분석(post-hoc)",
    "predictive": False,
    "watermark": "이 수치는 과거~현재 시점 확정데이터 기반. 미래예측 아님.",
}


def calc_sonho_fee(
    monthly_revenue: float,
    rent: float,
    depreciation: float = 0.0,
    overhead: float = 0.0,
    venue_name: str = "unknown",
    source_tier: str = "S급",
) -> dict:
    """
    소호 임대료 헤게모니 수수료 계산.

    hegemonic_fee.py 패턴 재사용: monthly_revenue = 명목흑자,
    (rent+depreciation+overhead) = 마크업(헤게모니 수수료) 자리.

    Args:
        monthly_revenue: 월 매출 (USD 또는 KRW — 단위 일치 유지)
        rent: 월 임대료
        depreciation: 월 장비 감가상각비
        overhead: 월 관리비/공과금
        venue_name: 공간명 (식별용)
        source_tier: 데이터 등급

    Returns:
        fee_amount, fee_rate, fixed_cost_ratio, 해석
    """
    tier = source_tier if source_tier in SOURCE_TIER_PENALTY else "C급"
    penalty = SOURCE_TIER_PENALTY[tier]

    if monthly_revenue <= 0:
        return {"error": "매출이 0 이하입니다."}

    total_fixed = rent + depreciation + overhead
    fee_amount = total_fixed
    fee_rate = total_fixed / monthly_revenue * 100
    net_income = monthly_revenue - total_fixed
    net_margin = net_income / monthly_revenue * 100

    return {
        "venue": venue_name,
        "monthly_revenue": round(monthly_revenue, 2),
        "rent": round(rent, 2),
        "depreciation": round(depreciation, 2),
        "overhead": round(overhead, 2),
        "total_fixed_costs": round(total_fixed, 2),
        "fixed_cost_ratio_pct": round(fee_rate, 2),
        "hegemonic_fee_rate_pct": round(fee_rate, 2),
        "net_income": round(net_income, 2),
        "net_margin_pct": round(net_margin, 2),
        "source_tier": tier,
        "source_penalty": penalty,
        "formula": {
            "total_fixed": f"{rent} + {depreciation} + {overhead} = {total_fixed}",
            "hegemonic_fee_rate": f"{total_fixed} / {monthly_revenue} x 100 = {fee_rate:.1f}%",
            "net_margin": f"({monthly_revenue} - {total_fixed}) / {monthly_revenue} x 100 = {net_margin:.1f}%",
        },
        "interpretation": (
            f"{venue_name}: 월 매출 {monthly_revenue:,.0f} 중 "
            f"고정비 {total_fixed:,.0f} ({fee_rate:.0f}%), "
            f"순수익 {net_income:,.0f} ({net_margin:.0f}%)"
        ),
        "pattern_note": "hegemonic_fee.py 패턴 재사용: revenue=nominal, fixed_cost=fee",
        "disclaimer": COMMON_DISCLAIMER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


def calc_attraction_capital(
    guild_response_count: int,
    marketing_cost: float = 0.0,
    time_cost_hours: float = 0.0,
    hourly_rate_usd: float = 0.0,
    guild_name: str = "unknown",
    source_tier: str = "S급",
) -> dict:
    """
    매력 자본 계수 계산.

    "인류를 측정했다"는 박씨 표현의 정확한 수식화.
    길드 모집 응답률을 마케팅 비용 + 시간 비용으로 나눈 값.

    Args:
        guild_response_count: 길드 모집 응답자 수
        marketing_cost: 마케팅 비용 (USD)
        time_cost_hours: 투입 시간 (시간)
        hourly_rate_usd: 시간당 단가 (USD, 0이면 시간비용 미산정)
        guild_name: 길드/그룹명
        source_tier: 데이터 등급 (기본 S급 — 자기생산 운영로그)

    Returns:
        attraction_coefficient, cost_per_response, 해석

    ⚠️ 가드레일: 이 계수는 1차 정의 후 변경 금지 (시계열 단절 방지)
    """
    tier = source_tier if source_tier in SOURCE_TIER_PENALTY else "C급"
    penalty = SOURCE_TIER_PENALTY[tier]

    time_cost = time_cost_hours * hourly_rate_usd
    total_cost = marketing_cost + time_cost

    if total_cost <= 0:
        return {
            "error": "비용이 0 이하입니다. 최소 마케팅비 또는 시간을 입력하세요.",
            "guild": guild_name,
            "note": "비용 0이면 계수가 무한대 — 의미있는 계수 산출 불가",
        }

    attraction_coefficient = guild_response_count / total_cost
    cost_per_response = total_cost / guild_response_count if guild_response_count > 0 else 0

    return {
        "guild": guild_name,
        "guild_response_count": guild_response_count,
        "marketing_cost_usd": round(marketing_cost, 2),
        "time_cost_hours": time_cost_hours,
        "hourly_rate_usd": round(hourly_rate_usd, 2),
        "time_cost_usd": round(time_cost, 2),
        "total_cost_usd": round(total_cost, 2),
        "attraction_coefficient": round(attraction_coefficient * penalty, 6),
        "raw_coefficient": round(attraction_coefficient, 6),
        "cost_per_response_usd": round(cost_per_response, 4),
        "source_tier": tier,
        "source_penalty": penalty,
        "formula": {
            "total_cost": f"{marketing_cost} + ({time_cost_hours}h x ${hourly_rate_usd}/h) = ${total_cost:.2f}",
            "attraction_coefficient": f"{guild_response_count} / {total_cost:.2f} = {attraction_coefficient:.6f}",
            "cost_per_response": f"{total_cost:.2f} / {guild_response_count} = {cost_per_response:.4f}",
        },
        "interpretation": (
            f"{guild_name}: ${total_cost:.2f} 비용으로 {guild_response_count}명 응답 → "
            f"매력자본계수 {attraction_coefficient:.6f} "
            f"(1 USD당 {attraction_coefficient:.4f}명 반응)"
        ),
        "definition": (
            "매력자본계수 = 길드_모집_응답률 / (마케팅비 + 시간비용). "
            "Bourdieu 문화자본/사회자본 개념의 계량화 버전 — "
            "분모/분자가 명확한 비율로, 추상적 자본개념이 아닌 직접 측정가능한 KPI."
        ),
        "guardrail": (
            "⚠️ 이 계수 정의는 1차 확정 후 변경 금지 — 시계열 단절 방지. "
            "변경 필요시 별도 v2 계수(v2_attraction_coefficient)로 추가."
        ),
        "disclaimer": COMMON_DISCLAIMER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


def run_module13(
    venues: Optional[list[dict]] = None,
    guilds: Optional[list[dict]] = None,
) -> dict:
    """
    Module 13 통합 실행.

    Args:
        venues: 소호 공간 리스트.
            각 항목: {"name": str, "revenue": float, "rent": float,
                     "depreciation": float, "overhead": float, "source_tier": str}
        guilds: 길드 데이터 리스트.
            각 항목: {"name": str, "responses": int, "marketing_cost": float,
                     "time_hours": float, "hourly_rate": float, "source_tier": str}

    Returns:
        소호 수수료 + 매력자본 통합 분석
    """
    results = {"module": "Module 13 — Sonho (SOHO) Economy", "version": "1.0.0"}

    # Step 1: 소호 임대료 헤게모니 수수료
    if venues:
        venue_results = []
        for v in venues:
            r = calc_sonho_fee(
                monthly_revenue=v.get("revenue", 0),
                rent=v.get("rent", 0),
                depreciation=v.get("depreciation", 0),
                overhead=v.get("overhead", 0),
                venue_name=v.get("name", "unknown"),
                source_tier=v.get("source_tier", "S급"),
            )
            venue_results.append(r)

        results["venues"] = venue_results
        rates = [v.get("hegemonic_fee_rate_pct", 0) for v in venue_results if "error" not in v]
        if rates:
            results["venue_summary"] = {
                "count": len(rates),
                "avg_fee_rate_pct": round(sum(rates) / len(rates), 2),
                "note": "베이커리와 부동산길드는 고정비구조가 다름 — 단순평균은 참고용",
            }
    else:
        results["venues"] = []
        results["venue_summary"] = {"note": "공간 데이터 없음"}

    # Step 2: 매력 자본 계수
    if guilds:
        guild_results = []
        for g in guilds:
            r = calc_attraction_capital(
                guild_response_count=g.get("responses", 0),
                marketing_cost=g.get("marketing_cost", 0),
                time_cost_hours=g.get("time_hours", 0),
                hourly_rate_usd=g.get("hourly_rate", 0),
                guild_name=g.get("name", "unknown"),
                source_tier=g.get("source_tier", "S급"),
            )
            guild_results.append(r)

        results["guilds"] = guild_results
        coefs = [g.get("attraction_coefficient", 0) for g in guild_results if "error" not in g]
        if coefs:
            results["guild_summary"] = {
                "count": len(coefs),
                "avg_attraction_coefficient": round(sum(coefs) / len(coefs), 6),
            }
    else:
        results["guilds"] = []
        results["guild_summary"] = {"note": "길드 데이터 없음"}

    results["disclaimer"] = COMMON_DISCLAIMER
    results["guardrail_note"] = (
        "obokzip, alexandria-sanctuary는 기획단계 — S급 데이터 아님. "
        "매력자본계수 정의는 1차 확정 후 변경 금지."
    )
    results["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M KST")
    return results


if __name__ == "__main__":
    import sys, json

    if "--demo" in sys.argv:
        demo_venues = [
            {"name": "호야당 베이커리", "revenue": 8000, "rent": 2500,
             "depreciation": 500, "overhead": 800},
        ]
        demo_guilds = [
            {"name": "namoneygoal 길드", "responses": 15,
             "marketing_cost": 50, "time_hours": 10, "hourly_rate": 15},
        ]
        result = run_module13(venues=demo_venues, guilds=demo_guilds)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({
            "module": "Module 13 — Sonho (SOHO) Economy",
            "available_functions": [
                "calc_sonho_fee(revenue, rent, depreciation, overhead, venue_name, source_tier)",
                "calc_attraction_capital(responses, marketing_cost, time_hours, hourly_rate, guild_name, source_tier)",
                "run_module13(venues, guilds)",
            ],
            "guardrails": [
                "매력자본계수 1차 정의 후 변경 금지",
                "베이커리/부동산길드 수수료 단순합산 금지",
                "obokzip/alexandria는 기획단계 — 동일신뢰도 취급 금지",
                "사후분석만 (예측 금지)",
            ],
        }, ensure_ascii=False, indent=2))
