#!/usr/bin/env python3
"""
PARKSY FX Engine v3.0 — Pipeline Orchestrator

실행 파이프라인:
  GATE 0 → Module 3 (Hegemonic Fee) → Module 7 (Dual-Unit) → Module 8 (Signal Logger)
"""

import sys, os, json
from datetime import datetime

# 모듈 임포트 (sys.path로 modules/ 직접 추가)
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gate0
import hegemonic_fee as hf
import dual_unit
import signal_logger as sl


def run_pipeline(
    currency: str = "KRW",
    exposures: list[dict] | None = None,
    surplus: float | None = None,
    year: int | None = None,
    record_signal: bool = True,
) -> dict:
    """
    FX Engine 풀 파이프라인 실행.

    1. GATE 0 — 현재 환율 데이터 출처 검증
    2. Module 3 — 헤게모니 수수료 계산
    3. Module 7 — 듀얼 유닛 환산 (노출 데이터 있을 시)
    4. Module 8 — 시그널 로깅 (옵션)

    Args:
        currency: 대상 통화
        exposures: Module 7용 통화 노출 리스트 (선택)
        surplus: 명목 경상흑자 (선택)
        year: 분석 연도 (선택)
        record_signal: Module 8 시그널 기록 여부

    Returns:
        파이프라인 전체 결과
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M KST")
    errors = []
    warnings = []

    # ── Step 0: GATE 0 ──────────────────────────────────────────────────────
    source_url = "https://finance.yahoo.com/quote/USDKRW=X/"
    current_rate = hf.get_current_rate(currency)

    gate_result = gate0.run_gate0(
        data_point_name=f"{currency} 현재환율",
        source_url=source_url,
        data_series=None,  # yfinance 실시간 — Benford 적용 안함
    )

    if gate_result["gate_status"] == "BLOCK":
        errors.append(f"GATE 0 BLOCK: {currency} 데이터 신뢰도 {gate_result['confidence_score']}")
    elif gate_result["gate_status"] == "WARNING":
        warnings.append(f"GATE 0 WARNING: {currency} 데이터 신뢰도 {gate_result['confidence_score']}")

    # ── Step 1: Module 3 — Hegemonic Fee ────────────────────────────────────
    fee_result = hf.calc_hegemonic_fee(
        currency=currency,
        current_rate=current_rate,
        nominal_surplus=surplus,
        year=year,
    )

    fee_error = fee_result.get("error")
    if fee_error:
        errors.append(f"Module 3: {fee_error}")

    # ── Step 2: Module 7 — Dual-Unit Reduction ─────────────────────────────
    dual_result = None
    if exposures and not fee_error:
        confidence = gate_result.get("confidence_score", 1.0)
        adj_exposures = []
        for exp in exposures:
            adj = dict(exp)
            adj["amount"] = float(exp.get("amount", 0)) * confidence
            adj_exposures.append(adj)

        dual_result = dual_unit.reduce(adj_exposures)

        if dual_result.get("errors"):
            warnings.append(f"Module 7: 일부 통화 환산 실패 — {dual_result['errors']}")

    # ── Step 3: Module 8 — Signal Logger ────────────────────────────────────
    signal_result = None
    if record_signal and not fee_error:
        signal_strength = 0.0
        basis_parts = []

        if isinstance(fee_result, dict) and "hegemonic_fee_rate_pct" in fee_result:
            fee_rate = fee_result["hegemonic_fee_rate_pct"]
            if fee_rate > 15:
                signal_strength += 0.3
                basis_parts.append(f"헤게모니 수수료율 {fee_rate}% (15% 초과)")

        if gate_result["gate_status"] == "WARNING":
            signal_strength += 0.15
            basis_parts.append("GATE 0 경고 — 데이터 주의 필요")

        if gate_result["regime_change_flag"]:
            signal_strength += 0.2
            basis_parts.append("체제 변화 감지 — GATE 0 regime_change_flag")

        if signal_strength > 0:
            if isinstance(fee_result, dict) and fee_result.get("hegemonic_fee_rate_pct", 0) > 15:
                sig_type = "dsi_stress"
            elif gate_result["regime_change_flag"]:
                sig_type = "regime_change"
            else:
                sig_type = "won_overvaluation"

            signal_result = sl.record_signal(
                signal_type=sig_type,
                strength=min(1.0, signal_strength),
                basis=" | ".join(basis_parts) if basis_parts else "파이프라인 자동 평가",
                metadata={
                    "currency": currency,
                    "hegemonic_fee_rate": fee_result.get("hegemonic_fee_rate_pct"),
                    "gate_confidence": gate_result.get("confidence_score"),
                },
            )

    result = {
        "pipeline": "PARKSY FX Engine v3.0",
        "timestamp": timestamp,
        "currency": currency,
        "gate0": gate_result,
        "module3_hegemonic_fee": fee_result,
        "module7_dual_unit": dual_result,
        "module8_signal": signal_result,
        "warnings": warnings if warnings else None,
        "errors": errors if errors else None,
        "pipeline_status": "BLOCKED" if errors else "COMPLETE",
        "guardrails": [
            "사후분석 — 예측 아님",
            "베타 헤지 전략 — 알파 아님",
            "레버리지 금지 — 현물 자산 매집 기준",
            "최소 8회 시그널 누적 전 자본투입 금지",
        ],
    }

    return result


def run_quick_snapshot() -> dict:
    """KRW/JPY/TWD 전체 스냅샷"""
    results = {}
    all_ok = True
    for ccy in ["KRW", "JPY", "TWD"]:
        r = run_pipeline(currency=ccy, record_signal=False)
        results[ccy] = r
        if r.get("errors"):
            all_ok = False
    return {
        "pipeline": "PARKSY FX Engine v3.0 — Quick Snapshot",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
        "results": results,
        "all_ok": all_ok,
        "note": "Module 7/8 생략. 전체 파이프라인은 run_pipeline() 호출.",
    }


if __name__ == "__main__":
    if "--snapshot" in sys.argv:
        result = run_quick_snapshot()
    elif "--full" in sys.argv:
        exposures = [
            {"currency": "KRW", "amount": 100000000, "label": "원화 예금"},
            {"currency": "JPY", "amount": 5000000, "label": "엔화 자산"},
        ]
        result = run_pipeline(currency="KRW", exposures=exposures, record_signal=True)
    else:
        result = run_pipeline(currency="KRW", record_signal=False)
    print(json.dumps(result, ensure_ascii=False, indent=2))
