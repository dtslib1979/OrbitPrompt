#!/usr/bin/env python3
"""
Module 10: Compound Reinvestment Simulator (백서 13.2/13.6절, v3.3 신규)

트랙2(FX/금) 전용 복리누적곡선 시뮬레이터.

공식:
  복리_자산(t) = Σ[i=1..t] 매집액(i) × (1 + 자산수익률)^(t-i)

가드레일 (백서 15.5절):
  - 트랙1(IP) 수익률과 직접비교 그래프 생성 금지
  - 5년 미만 데이터로 트랙2 복리성과 단정 금지
  - 트랙2를 "단순 베타헤지/보험"으로만 단정 금지
"""

import json
from datetime import datetime
from typing import Optional


# ─── 3-Bucket 기본 비중 (백서 13.4절) ─────────────────────────────────────────────

_DEFAULT_BUCKET_WEIGHTS = {
    "USD_cash": 0.40,   # USD 현금/MMF — 유동성 + 단기금리
    "GOLD": 0.35,       # 금 — 비-소버린 장기 누적
    "USD_bond": 0.25,   # 달러표시 우량채(단기) — 이자수익 + 환헤지
}

_DEFAULT_RETURNS = {
    "USD_cash": 0.04,   # MMF 금리 가정
    "GOLD": 0.06,       # 금 장기 연평균 가정
    "USD_bond": 0.045,  # 단기국채 가정
}

_BUCKET_LABELS = {
    "USD_cash": "USD 현금/MMF",
    "GOLD": "금",
    "USD_bond": "달러표시 단기국채",
}


def compound_curve(
    monthly_contribution: float,
    annual_return_rate: float,
    years: int,
) -> dict:
    """
    단일 자산군 복리곡선.

    Args:
        monthly_contribution: 월 적립액 (USD)
        annual_return_rate: 연 수익률 (0.06 = 6%)
        years: 운용 기간 (년)

    Returns:
        yearly_curve, final values
    """
    months = years * 12
    monthly_rate = annual_return_rate / 12
    balance = 0.0
    curve = []
    for m in range(1, months + 1):
        balance = balance * (1 + monthly_rate) + monthly_contribution
        if m % 12 == 0:
            curve.append({
                "year": m // 12,
                "balance": round(balance, 2),
                "contributed_ytd": round(monthly_contribution * 12, 2),
            })

    total_contributed = monthly_contribution * months
    total_growth = balance - total_contributed
    growth_ratio = (balance / total_contributed - 1) * 100 if total_contributed > 0 else 0.0

    return {
        "years": years,
        "monthly_contribution": monthly_contribution,
        "annual_return_rate_pct": round(annual_return_rate * 100, 2),
        "final_balance": round(balance, 2),
        "total_contributed": round(total_contributed, 2),
        "total_growth": round(total_growth, 2),
        "total_growth_pct": round(growth_ratio, 2),
        "yearly_curve": curve,
    }


def evaluate_readiness(years_elapsed: int) -> str:
    """13.5절 규칙6: 5년 미만은 평가시기상조"""
    if years_elapsed >= 5:
        return "평가가능"
    return "평가시기상조 (백서 13.5절 규칙6, 최소 5년 필요)"


def run_module10(
    monthly_contribution: float,
    years: int = 5,
    bucket_weights: Optional[dict] = None,
    usd_cash_return: Optional[float] = None,
    gold_return: Optional[float] = None,
    usd_bond_return: Optional[float] = None,
    fee_rate: float = 0.0,
) -> dict:
    """
    Module 10 메인 실행 — 3-Bucket 복리 시뮬레이션.

    Args:
        monthly_contribution: 월 총 적립액 (USD)
        years: 시뮬레이션 기간 (년)
        bucket_weights: 3-Bucket 비중 (기본값: 13.4절)
        usd_cash_return: USD 현금/MMF 연수익률
        gold_return: 금 연수익률
        usd_bond_return: 단기국채 연수익률
        fee_rate: 세금/수수료 차감율 (0.0~1.0, 기본 0)

    Returns:
        버킷별 + 통합 복리 결과
    """
    if bucket_weights is None:
        bucket_weights = _DEFAULT_BUCKET_WEIGHTS.copy()

    returns = {
        "USD_cash": usd_cash_return if usd_cash_return is not None else _DEFAULT_RETURNS["USD_cash"],
        "GOLD": gold_return if gold_return is not None else _DEFAULT_RETURNS["GOLD"],
        "USD_bond": usd_bond_return if usd_bond_return is not None else _DEFAULT_RETURNS["USD_bond"],
    }

    # 수수료 차감 후 순수익률
    net_returns = {k: r * (1 - fee_rate) for k, r in returns.items()}

    bucket_results = {}
    combined_final = 0.0
    combined_contributed = 0.0

    for name in ["USD_cash", "GOLD", "USD_bond"]:
        weight = bucket_weights.get(name, 0.0)
        if weight <= 0:
            continue
        contrib = monthly_contribution * weight
        result = compound_curve(contrib, net_returns[name], years)
        result["bucket_name"] = _BUCKET_LABELS.get(name, name)
        result["weight_pct"] = round(weight * 100, 1)
        bucket_results[name] = result
        combined_final += result["final_balance"]
        combined_contributed += result["total_contributed"]

    readiness = evaluate_readiness(years)
    combined_growth = combined_final - combined_contributed

    result = {
        "simulation": {
            "monthly_contribution_usd": monthly_contribution,
            "years": years,
            "total_contributed_usd": round(combined_contributed, 2),
            "final_balance_usd": round(combined_final, 2),
            "total_growth_usd": round(combined_growth, 2),
            "total_growth_pct": round(
                (combined_final / combined_contributed - 1) * 100, 2
            ) if combined_contributed > 0 else 0.0,
        },
        "buckets": bucket_results,
        "inputs": {
            "bucket_weights": bucket_weights,
            "annual_returns": {
                "USD_cash_pct": round(returns["USD_cash"] * 100, 2),
                "GOLD_pct": round(returns["GOLD"] * 100, 2),
                "USD_bond_pct": round(returns["USD_bond"] * 100, 2),
            },
            "fee_rate_pct": round(fee_rate * 100, 2),
        },
        "evaluation_readiness": readiness,
        "guardrails": [
            "트랙2(구조알파) 복리누적 시뮬레이션 — 트랙1(IP)과 별개 메커니즘",
            "트랙1·트랙2 수익률 직접비교 그래프 생성 금지 (백서 15.5절)",
            "5년 미만 구간은 평가시기상조 (백서 13.5절 규칙6)",
            "확정 수익 보장 아님 — 시뮬레이션은 가정 기반",
        ],
        "disclaimer": (
            "이것은 트랙2(구조알파) 복리누적 시뮬레이션이며 트랙1(IP)과 별개 메커니즘이다. "
            "확정 수익 보장이 아니며, 트랙1과의 직접 비교는 의도적으로 생성하지 않는다 "
            "(백서 15.5절 가드레일 — 두 트랙은 상관관계가 낮은 별개 곡선이 목적)."
        ),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }

    return result


def run_module10_for_track2(
    monthly_contribution_krw: float = 500_000,
    usd_krw_rate: float = 1500.0,
    years: int = 5,
) -> dict:
    """
    편의 래퍼: 원화 월 적립액 → Module 10 자동 실행.

    Args:
        monthly_contribution_krw: 월 적립액 (원화)
        usd_krw_rate: 적용 환율
        years: 시뮬레이션 기간

    Returns:
        Module 10 결과 (원화→USD 자동 환산)
    """
    monthly_usd = monthly_contribution_krw / usd_krw_rate
    return run_module10(
        monthly_contribution=monthly_usd,
        years=years,
    )


if __name__ == "__main__":
    import sys

    # 기본 실행: 월 $370 (50만원), 5년
    result = run_module10(monthly_contribution=370, years=5)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if "--track2" in sys.argv:
        krw_result = run_module10_for_track2(monthly_contribution_krw=500_000, years=10)
        print("\n--- 원화 기준 10년 ---")
        print(json.dumps(krw_result, ensure_ascii=False, indent=2))
