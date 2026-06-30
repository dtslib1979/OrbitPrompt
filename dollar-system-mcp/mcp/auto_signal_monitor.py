#!/usr/bin/env python3
"""
Auto Signal Monitor — yfinance 실시간 데이터 기반 시그널 자동 기록.

Module 8 Signal Logger + GATE 0 연동.
cron 등록: 매일 09:00 KST 실행 (장 시작 전 스냅샷)

백서 13.3절 시그널 기준:
  1. won_overvaluation  — Rolling Forecast 대비 고평가 윈도우
  2. treasury_watchlist — 재무부 모니터링 리스트 압박
  3. fed_hike_cycle     — FOMC 긴축 신호
  4. dsi_stress         — DSI 65 초과
  5. gold_discount      — 금 30일 이평 대비 -5% 이상
  6. regime_change      — GATE 0 체제변화 감지
"""

import json, os, sys
from datetime import datetime, timedelta
import pandas as pd

# 경로 설정
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "modules"))

from signal_logger import record_signal, get_stats
from gate0 import run_gate0


# ─── 기준 파라미터 ──────────────────────────────────────────────────────────────

FX_BASELINES = {
    "KRW": 1240.0,  # 백서 5.3절
    "JPY": 128.0,
    "TWD": 29.2,
}

# Rolling Forecast 대비 고평가 기준 (약세율이 baseline 대비 15% 초과 시)
WON_OVERVALUATION_DEPRECIATION_THRESHOLD = 15.0  # %

# 금 가격 30일 이평 대비 할인율 기준
GOLD_DISCOUNT_THRESHOLD = -5.0  # %

# DSI 스트레스 기준
DSI_STRESS_THRESHOLD = 65.0


def fetch_market_data() -> dict:
    """yfinance 실시간 시장 데이터 수집"""
    import yfinance as yf

    data = {}

    # 환율
    pairs = {
        "USDKRW": "KRW",
        "USDJPY": "JPY",
        "USDTWD": "TWD",
    }
    for ticker, currency in pairs.items():
        try:
            t = yf.Ticker(f"{ticker}=X")
            info = t.history(period="1d")
            if not info.empty:
                rate = info["Close"].iloc[-1]
            else:
                rate = t.fast_info.last_price if hasattr(t.fast_info, "last_price") else None
            if rate:
                data[currency] = float(rate)
        except Exception as e:
            data[currency] = None
            print(f"  ⚠️ {ticker} fetch failed: {e}")

    # 금 가격
    try:
        gold = yf.Ticker("GC=F")
        hist = gold.history(period="2mo")
        if not hist.empty:
            data["gold_price"] = float(hist["Close"].iloc[-1])
            # 30일 이평
            ma30 = hist["Close"].rolling(30).mean().iloc[-1]
            data["gold_ma30"] = float(ma30) if not pd.isna(ma30) else None
        else:
            data["gold_price"] = None
            data["gold_ma30"] = None
    except Exception as e:
        data["gold_price"] = None
        data["gold_ma30"] = None
        print(f"  ⚠️ Gold fetch failed: {e}")

    # 미국 10년물 금리 (DSI 보조지표)
    try:
        tnx = yf.Ticker("^TNX")
        hist = tnx.history(period="1mo")
        if not hist.empty:
            data["tnx"] = float(hist["Close"].iloc[-1])
        else:
            data["tnx"] = None
    except Exception:
        data["tnx"] = None

    # DXY 달러 인덱스
    try:
        dxy = yf.Ticker("DX-Y.NYB")
        hist = dxy.history(period="1d")
        if not hist.empty:
            data["dxy"] = float(hist["Close"].iloc[-1])
        else:
            data["dxy"] = None
    except Exception:
        data["dxy"] = None

    return data


def check_won_overvaluation(data: dict) -> list:
    """원화 일시 고평가 시그널 — 각 통화별 체크"""
    signals = []
    for currency, baseline in FX_BASELINES.items():
        rate = data.get(currency)
        if rate is None:
            continue
        depreciation_pct = (rate - baseline) / baseline * 100
        if depreciation_pct >= WON_OVERVALUATION_DEPRECIATION_THRESHOLD:
            strength = min(0.35, depreciation_pct / 100)
            signals.append({
                "signal_type": "won_overvaluation",
                "strength": round(strength, 3),
                "basis": (
                    f"[{currency}] yfinance: {rate:.2f}, "
                    f"약세율 {depreciation_pct:.1f}% (baseline {baseline}). "
                    f"기준 {WON_OVERVALUATION_DEPRECIATION_THRESHOLD:.0f}% 초과."
                ),
                "metadata": {
                    "currency": currency,
                    "rate": rate,
                    "baseline": baseline,
                    "depreciation_pct": round(depreciation_pct, 1),
                    "source": "yfinance",
                },
            })
    return signals


def check_gold_discount(data: dict) -> list:
    """금 가격 일시 조정 시그널"""
    signals = []
    gold_price = data.get("gold_price")
    gold_ma30 = data.get("gold_ma30")
    if gold_price is None or gold_ma30 is None:
        return signals
    discount_pct = (gold_price - gold_ma30) / gold_ma30 * 100
    if discount_pct <= GOLD_DISCOUNT_THRESHOLD:
        strength = min(0.15, abs(discount_pct) / 50)
        signals.append({
            "signal_type": "gold_discount",
            "strength": round(strength, 3),
            "basis": (
                f"금 ${gold_price:.0f}, 30일 이평 ${gold_ma30:.0f} "
                f"대비 {discount_pct:.2f}%. 기준 {GOLD_DISCOUNT_THRESHOLD:.0f}% 초과."
            ),
            "metadata": {
                "gold": gold_price,
                "ma30": gold_ma30,
                "discount_pct": round(discount_pct, 2),
            },
        })
    return signals


def check_regime_change(data: dict) -> list:
    """GATE 0 체제변화 감지 — DXY 급변 탐지"""
    signals = []
    dxy = data.get("dxy")
    if dxy is None:
        return signals

    # DXY 30일 변화율
    import yfinance as yf
    try:
        dxy_ticker = yf.Ticker("DX-Y.NYB")
        hist = dxy_ticker.history(period="2mo")
        if len(hist) >= 20:
            old = float(hist["Close"].iloc[-20])
            change_pct = (dxy - old) / old * 100
            if abs(change_pct) > 3.0:
                signals.append({
                    "signal_type": "regime_change",
                    "strength": round(min(0.20, abs(change_pct) / 20), 3),
                    "basis": (
                        f"DXY {dxy:.2f}, 20거래일 전 {old:.2f} 대비 "
                        f"{change_pct:+.2f}% 변동. 기준 ±3% 초과."
                    ),
                    "metadata": {
                        "dxy": dxy,
                        "dxy_20d_ago": old,
                        "change_pct": round(change_pct, 2),
                    },
                })
    except Exception as e:
        print(f"  ⚠️ DXY regime check failed: {e}")

    return signals


def check_dsi_stress(data: dict) -> list:
    """DSI 스트레스 — TNX 기준 단순화 탐지"""
    signals = []
    tnx = data.get("tnx")
    if tnx is None:
        return signals

    # TNX 급등 시 금리 스트레스 신호
    import yfinance as yf
    try:
        tnx_ticker = yf.Ticker("^TNX")
        hist = tnx_ticker.history(period="1mo")
        if len(hist) >= 5:
            old = float(hist["Close"].iloc[-5])
            change = tnx - old
            if change > 0.3:  # 5거래일 내 30bp 이상 상승
                signals.append({
                    "signal_type": "dsi_stress",
                    "strength": round(min(0.20, change / 1.5), 3),
                    "basis": (
                        f"TNX {tnx:.2f}%, 5거래일 전 {old:.2f}% 대비 "
                        f"{change:.2f}%p 상승. 금리 스트레스 신호."
                    ),
                    "metadata": {
                        "tnx": tnx,
                        "tnx_5d_ago": old,
                        "change_pct": round(change, 2),
                    },
                })
    except Exception as e:
        print(f"  ⚠️ DSI stress check failed: {e}")

    return signals


def run_monitor(dry_run: bool = False) -> dict:
    """
    메인 모니터링 실행.

    Args:
        dry_run: True면 기록 없이 탐지만

    Returns:
        모니터링 결과 (탐지된 시그널 + 누적 통계)
    """
    print(f"\n{'='*50}")
    print(f"Auto Signal Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M KST')}")
    print(f"{'='*50}")

    # 1. 데이터 수집
    print("\n📡 Fetching market data...")
    data = fetch_market_data()
    for k, v in data.items():
        if v is not None:
            print(f"  {k}: {v}")

    # 2. 시그널 체크
    detected = []
    for check_fn in [check_won_overvaluation, check_gold_discount, check_regime_change, check_dsi_stress]:
        detected.extend(check_fn(data))

    print(f"\n📊 Signals detected: {len(detected)}")
    for s in detected:
        print(f"  [{s['signal_type']}] strength={s['strength']} — {s['basis'][:80]}...")

    # 3. 기록
    recorded = []
    if not dry_run:
        print(f"\n💾 Recording signals...")
        for s in detected:
            result = record_signal(
                signal_type=s["signal_type"],
                strength=s["strength"],
                basis=s["basis"],
                metadata=s.get("metadata"),
            )
            if "recorded" in result:
                recorded.append(result["recorded"])
                print(f"  ✅ {result['recorded']['id']}")
            else:
                print(f"  ❌ {result.get('error', 'unknown error')}")
    else:
        print("\n🔍 DRY RUN — no signals recorded")

    # 4. 누적 통계
    stats = get_stats()

    print(f"\n📈 Cumulative stats:")
    print(f"  Total signals: {stats['total_signals']}")
    print(f"  Distinct rounds: {stats['distinct_rounds']}")
    print(f"  Capital deployment allowed: {stats['capital_deployment_allowed']}")
    print(f"  Rounds needed: {stats['rounds_needed']}")

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
        "market_data": {k: v for k, v in data.items() if v is not None},
        "signals_detected": detected,
        "signals_recorded": recorded,
        "cumulative_stats": stats,
        "dry_run": dry_run,
    }


# ─── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="FX Engine Auto Signal Monitor")
    parser.add_argument("--dry-run", action="store_true", help="탐지만 하고 기록 안 함")
    parser.add_argument("--json", action="store_true", help="JSON 출력")
    args = parser.parse_args()

    result = run_monitor(dry_run=args.dry_run)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
