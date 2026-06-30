#!/usr/bin/env python3
"""
Module 7 — Dual-Unit Reduction Engine (백서 7.4~7.6절)

N개 통화 노출을 GOLD_equiv + USD_equiv 2개 유닛으로 강제 환산.
표본국가 수(N) 논쟁을 구조적으로 무력화 — N이 몇 개든 출력은 항상 2변수.

공식:
  USD_equiv(t)   = Σ[i] Exposure_i(t) × FX_to_USD_i(t)
  GOLD_equiv(t)  = USD_equiv(t) / GOLD_price_USD(t)
"""

from datetime import datetime
from typing import Optional


def get_fx_rate(currency: str) -> Optional[float]:
    """yfinance로 USD/통화 환율 조회"""
    sym_map = {
        "KRW": "USDKRW=X", "JPY": "USDJPY=X", "TWD": "USDTWD=X",
        "EUR": "USDEUR=X", "CNY": "USDCNY=X", "GBP": "USDGBP=X",
        "CHF": "USDCHF=X", "SGD": "USDSGD=X", "VND": "USDVND=X",
    }
    sym = sym_map.get(currency.upper())
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


def get_gold_price() -> Optional[float]:
    """금 가격 (USD/oz) — yfinance GLD ETF"""
    try:
        import yfinance as yf
        t = yf.Ticker("GLD")
        h = t.history(period="5d")
        if h.empty:
            # 대체: GC=F (선물)
            t2 = yf.Ticker("GC=F")
            h2 = t2.history(period="5d")
            if h2.empty:
                return None
            return float(h2["Close"].iloc[-1])
        return float(h["Close"].iloc[-1])
    except Exception:
        return None


def reduce(
    exposures: list[dict],
    gold_price: Optional[float] = None,
    prefer_safe_equiv: bool = False,
) -> dict:
    """
    N개 통화 노출 → GOLD_equiv + USD_equiv 환산.

    Args:
        exposures: [
            {"currency": "KRW", "amount": 100000000},  # 원화 금액
            {"currency": "JPY", "amount": 5000000},     # 엔화 금액
        ]
        gold_price: 금 가격 (USD/oz). None이면 yfinance 자동 조회
        prefer_safe_equiv: True면 실물보유 비중 자동 산출

    Returns:
        USD_equiv, GOLD_equiv, details per exposure
    """
    usd_equiv = 0.0
    details = []
    errors = []

    for exp in exposures:
        ccy = exp["currency"].upper()
        amount = float(exp.get("amount", 0))
        label = exp.get("label", f"{ccy} Exposure")

        # USD 환산율
        fx_rate = get_fx_rate(ccy)
        if fx_rate is None:
            errors.append(f"{ccy} 환율 조회 실패")
            continue

        # amount가 이미 USD면 그대로, 아니면 /fx_rate
        if exp.get("in_usd", False):
            usd_value = amount
            fx_note = "이미 USD"
        else:
            usd_value = amount / fx_rate
            fx_note = f"1 USD = {fx_rate:.2f} {ccy}"

        usd_equiv += usd_value

        details.append({
            "label": label,
            "currency": ccy,
            "amount_local": amount,
            "fx_rate_to_usd": fx_rate,
            "usd_value": round(usd_value, 2),
            "fx_note": fx_note,
        })

    # 금 가격
    if gold_price is None:
        gold_price = get_gold_price()

    gold_equiv = round(usd_equiv / gold_price, 4) if gold_price and gold_price > 0 else None

    # 비중 계산
    total_usd = usd_equiv
    for d in details:
        d["weight_pct"] = round(d["usd_value"] / total_usd * 100, 1) if total_usd > 0 else 0

    result = {
        "n_currencies": len(exposures),
        "n_success": len(details),
        "n_errors": len(errors),
        "USD_equiv": round(usd_equiv, 2),
        "GOLD_equiv": round(gold_equiv, 4) if gold_equiv is not None else None,
        "gold_price_usd_per_oz": round(gold_price, 2) if gold_price else None,
        "details": details,
        "formula": {
            "USD_equiv": f"Σ 각 통화노출 / USD환율",
            "GOLD_equiv": f"USD_equiv({usd_equiv:.0f}) / 금가격({gold_price:.0f}) = {gold_equiv:.4f} oz"
            if gold_equiv else "금 가격 조회 실패",
        },
        "errors": errors if errors else None,
        "interpretation": (
            f"총 {len(details)}개 통화 노출 → USD ${usd_equiv:,.0f} →"
            f" 금 {gold_equiv:.4f} oz"
            if gold_equiv else f"총 USD ${usd_equiv:,.0f} (금 환산 실패)"
        ),
        "principle": "모든 입력변수가 동일한 최종 유닛으로 강제 환산. 검증 대상 = 환산 함수 하나로 수렴.",
        "note": "표본국가 수(N)와 무관하게 항상 2개 유닛 출력. Module 8/13장 입력 인터페이스 고정.",
        "disclaimer": "환산 결과는 현재 시점 기준. 금 가격 및 환율 변동에 따라 실시간 변경.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }

    # Safe-haven 비중 정보
    if prefer_safe_equiv and gold_equiv:
        result["safe_equiv"] = {
            "usd_weight_pct": 100.0 if usd_equiv > 0 else 0,
            "note": "전체 노출이 USD_equiv로 환산됨. 금은 가치저장수단이지 노출이 아님. 실물 금 보유량은 별도 입력 필요."
        }

    return result


if __name__ == "__main__":
    import json, sys

    # 테스트 exposures
    exposures = [
        {"currency": "KRW", "amount": 100000000, "label": "원화 예금"},
        {"currency": "JPY", "amount": 5000000, "label": "엔화 자산"},
        {"currency": "TWD", "amount": 1000000, "label": "대만달러 자산"},
    ]

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        result = reduce(exposures)
    else:
        result = reduce(exposures)

    print(json.dumps(result, ensure_ascii=False, indent=2))
