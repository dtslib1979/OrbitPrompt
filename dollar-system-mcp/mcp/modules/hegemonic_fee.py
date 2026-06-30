#!/usr/bin/env python3
"""
Module 3 — Hegemonic Fee Calculator (백서 5.3절)

헤게모니 수수료율 및 실질 수취액 계산.

공식:
  hegemonic_fee_rate = 누적 약세율 (사후 확정치)
  real_received = nominal_surplus / (1 + hegemonic_fee_rate)
  fee_amount = nominal_surplus - real_received

지원 통화:
  - KRW (baseline: 1240, 2022H1)
  - JPY (baseline: 128, 2022H1)
  - TWD (baseline: 29.2, 2022H1)
"""

import json, os
from datetime import datetime
from typing import Optional

# ─── 베이스라인 환율 (2022H1 = Fed 금리인상 사이클 시작점) ──────────────────────
_BASELINE_RATES = {
    "KRW": 1240.0,   # 2022H1 평균
    "JPY": 128.0,    # 2022H1 평균
    "JPY_ALT": 115.0, # 2021말 (보조 기준)
    "TWD": 29.2,     # 2022H1 평균
}

# ─── 경상흑자 참조 테이블 (USD) ──────────────────────────────────────────────
_SURPLUS_TABLE = {
    "KRW": {2024: 990, 2025: 1200, 2026: 1600},  # 억 달러
    "JPY": {2024: 2100, 2025: 2300, 2026: 2400},
    "TWD": {2024: 1980, 2025: 2140, 2026: 2500},
}


def get_current_rate(currency: str) -> Optional[float]:
    """yfinance로 현재 환율 조회"""
    sym_map = {"KRW": "USDKRW=X", "JPY": "USDJPY=X", "TWD": "USDTWD=X"}
    sym = sym_map.get(currency)
    if not sym:
        return None
    try:
        import yfinance as yf
        t = yf.Ticker(sym)
        h = t.history(period="5d")
        if h.empty:
            return None
        return float(h["Close"].iloc[-1])
    except Exception:
        return None


def calc_hegemonic_fee(
    currency: str = "KRW",
    current_rate: Optional[float] = None,
    nominal_surplus: Optional[float] = None,
    year: Optional[int] = None,
) -> dict:
    """
    헤게모니 수수료 계산.

    Args:
        currency: 통화 코드 (KRW/JPY/TWD)
        current_rate: 현재 환율 (None이면 yfinance 자동 조회)
        nominal_surplus: 명목 경상흑자 (억 USD, None이면 테이블 참조)
        year: 연도 (None이면 현재년도)

    Returns:
        hegemonic_fee_rate, nominal_surplus, real_received, fee_amount, etc.
    """
    if year is None:
        year = datetime.now().year

    currency = currency.upper()
    if currency not in _BASELINE_RATES:
        return {"error": f"지원하지 않는 통화: {currency}. 지원: {list(_BASELINE_RATES.keys())}"}

    baseline = _BASELINE_RATES[currency]

    # 현재 환율
    if current_rate is None:
        current_rate = get_current_rate(currency)
    if current_rate is None:
        return {"error": f"{currency} 현재 환율 조회 실패"}

    # 누적 약세율 = (현재 - 베이스라인) / 베이스라인
    cumulative_depreciation = (current_rate - baseline) / baseline

    # 명목흑자
    if nominal_surplus is None:
        surplus_table = _SURPLUS_TABLE.get(currency, {})
        nominal_surplus = surplus_table.get(year, surplus_table.get(max(surplus_table.keys(), default=0), 0))

    if not nominal_surplus or nominal_surplus <= 0:
        return {"error": "경상흑자 데이터 없음. nominal_surplus 매개변수로 직접 입력 필요."}

    # 실질 수취액
    real_received = nominal_surplus / (1 + cumulative_depreciation)
    fee_amount = nominal_surplus - real_received

    return {
        "currency": currency,
        "year": year,
        "baseline_rate": baseline,
        "current_rate": round(current_rate, 2),
        "cumulative_depreciation_rate": round(cumulative_depreciation * 100, 2),
        "hegemonic_fee_rate_pct": round(cumulative_depreciation * 100, 2),
        "nominal_surplus_billion_usd": nominal_surplus,
        "real_received_billion_usd": round(real_received, 1),
        "fee_amount_billion_usd": round(fee_amount, 1),
        "fee_ratio": round(fee_amount / nominal_surplus * 100, 1) if nominal_surplus else 0,
        "formula": {
            "hegemonic_fee_rate": f"({current_rate:.1f} - {baseline}) / {baseline} = {cumulative_depreciation*100:.1f}%",
            "real_received": f"{nominal_surplus} / (1 + {cumulative_depreciation:.3f}) = {real_received:.1f}",
            "fee": f"{nominal_surplus} - {real_received:.1f} = {fee_amount:.1f} (억 USD)",
        },
        "interpretation": (
            f"{currency} 기준 {year}년 헤게모니 수수료율 {cumulative_depreciation*100:.1f}%. "
            f"명목흑자 ${nominal_surplus}억 중 실질수취 ${real_received:.0f}억, "
            f"수수료 ${fee_amount:.0f}억 ({fee_amount/nominal_surplus*100:.0f}%)."
        ),
        "disclaimer": "사후분석. 예측 아님. 헤게모니 수수료는 누적 약세율 기반 사후 확정치.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


def calc_all(surplus_override: Optional[dict] = None) -> dict:
    """KRW/JPY/TWD 전체 한 번에 계산"""
    results = {}
    for ccy in ["KRW", "JPY", "TWD"]:
        rate = get_current_rate(ccy)
        surplus = surplus_override.get(ccy) if surplus_override else None
        results[ccy] = calc_hegemonic_fee(ccy, current_rate=rate, nominal_surplus=surplus)

    # 합계
    total_nominal = sum(
        r.get("nominal_surplus_billion_usd", 0) for r in results.values()
        if isinstance(r, dict) and "error" not in r
    )
    total_real = sum(
        r.get("real_received_billion_usd", 0) for r in results.values()
        if isinstance(r, dict) and "error" not in r
    )
    total_fee = sum(
        r.get("fee_amount_billion_usd", 0) for r in results.values()
        if isinstance(r, dict) and "error" not in r
    )

    return {
        "results": results,
        "summary": {
            "total_nominal_surplus_billion_usd": round(total_nominal, 1),
            "total_real_received_billion_usd": round(total_real, 1),
            "total_fee_amount_billion_usd": round(total_fee, 1),
            "total_fee_ratio_pct": round(total_fee / total_nominal * 100, 1) if total_nominal else 0,
            "interpretation": (
                f"KRW+JPY+TWD 합산 헤게모니 수수료 ${total_fee:.0f}억 "
                f"(명목 ${total_nominal:.0f}억의 {total_fee/total_nominal*100:.0f}%)"
            ),
        },
        "disclaimer": "사후분석. 예측 아님.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


if __name__ == "__main__":
    import sys
    import json

    if "--all" in sys.argv:
        result = calc_all()
    else:
        ccy = sys.argv[1] if len(sys.argv) > 1 else "KRW"
        result = calc_hegemonic_fee(ccy)

    print(json.dumps(result, ensure_ascii=False, indent=2))
