#!/usr/bin/env python3
"""
달러 시스템 MCP v3.0 — 환율/구조/권력/역사 분석 + FX Engine 모듈

v2.2 (기존):
  analyze, structure, phi7, get_timeline, compare, get_drivers,
  forecast, dsi, meal_index, version

v3.0 (신규):
  gate0_check      — 데이터 출처 검증 게이트
  hegemonic_fee    — 헤게모니 수수료 계산
  dual_unit_reduce — N 통화 → GOLD/USD 2유닛 환산
  signal_log       — 시그널 기록 및 조회
  fx_pipeline      — 전체 파이프라인 실행

등록 (~/.claude.json mcpServers):
  "dollar-system-mcp": {
    "command": "python3",
    "args": ["/home/dtsli/OrbitPrompt/dollar-system-mcp/mcp/server.py"]
  }
"""

import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "modules"))

from mcp.server.fastmcp import FastMCP
from dollar_engine import (
    analyze_rate, structure_critique, phi7_map, timeline,
    compare_rates, drivers, predict, calc_dsi, meal_ratio,
)
from gate0 import run_gate0
from hegemonic_fee import calc_hegemonic_fee, calc_all
from dual_unit import reduce as dual_unit_reduce
from signal_logger import record_signal, get_stats, get_log
from main import run_pipeline, run_quick_snapshot
from module10_compound_simulator import run_module10, run_module10_for_track2

VERSION = "3.3.0"

mcp = FastMCP("parksy-economy-fx")


# ═══════════════════════════════════════════════════════════════════════════════
# v2.2 레거시 툴 (완전 보존)
# ═══════════════════════════════════════════════════════════════════════════════

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

    Args:
        city1: 기준 도시. 가능: 서울 / 뉴욕 / 베이징 / 도쿄 / 상파울루 / 나이로비 / 뭄바이
        city2: 비교 도시. 기본값 뉴욕.

    Returns:
        한 끼 비용(USD/KRW), 노동시간 환산, meal_exchange_rate, 윤리적 판정
    """
    return meal_ratio(city1, city2)


# ═══════════════════════════════════════════════════════════════════════════════
# v3.0 신규 FX Engine 툴
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def gate0_check(
    data_point_name: str,
    source_url: str,
    data_series: list[float] | None = None,
    cross_source_values: list[float] | None = None,
    context: str = "",
) -> dict:
    """
    [v3.0 신규] GATE 0 — 데이터 출처 검증 게이트 (백서 14장).

    모든 외부 로데이터는 이 게이트를 통과해야만 하위 모듈로 전달 가능.
    5단계 검증: 출처계보 → Benford's Law → 시계열 불연속성 → 발행기관 인센티브 → 교차검증 합의도

    Args:
        data_point_name: 검증할 데이터 포인트명 (예: "KRW 2026Q2 경상수지")
        source_url: 데이터 출처 URL
        data_series: Benford 검증용 숫자 배열 (선택)
        cross_source_values: 교차검증용 복수 출처 값 배열 (선택)
        context: 발행기관 인센티브 분석 컨텍스트 (선택)

    Returns:
        gate_status(PASS/WARNING/BLOCK), confidence_score, 역용_signal, 5단계 상세
    """
    return run_gate0(data_point_name, source_url, data_series, cross_source_values, context)


@mcp.tool()
def hegemonic_fee(
    currency: str = "KRW",
    current_rate: float | None = None,
    nominal_surplus: float | None = None,
    year: int | None = None,
) -> dict:
    """
    [v3.0 신규] 헤게모니 수수료 계산 (백서 5.3절).

    환율 약세를 통해 달러 패권이 수출국 경상흑자에서 선취하는 비용을 계산.

    Args:
        currency: 통화 코드 (KRW/JPY/TWD)
        current_rate: 현재 환율 (비우면 yfinance 자동 조회)
        nominal_surplus: 명목 경상흑자 (억 USD, 비우면 테이블 참조)
        year: 분석 연도 (비우면 현재년도)

    Returns:
        hegemonic_fee_rate_pct, nominal_surplus, real_received, fee_amount, formula
    """
    return calc_hegemonic_fee(currency, current_rate, nominal_surplus, year)


@mcp.tool()
def dual_unit_reduce(
    exposures: list[dict],
    gold_price: float | None = None,
) -> dict:
    """
    [v3.0 신규] N개 통화 노출 → GOLD_equiv + USD_equiv 2유닛 환산 (백서 7.4~7.6절).

    모든 입력변수를 동일한 최종 유닛으로 강제 환산.
    표본국가 수(N)와 무관하게 항상 2개 유닛 출력.

    Args:
        exposures: 통화 노출 리스트. 각 항목: {"currency": "KRW", "amount": 100000000, "label": "원화 예금", "in_usd": false}
        gold_price: 금 가격 USD/oz (비우면 yfinance 자동 조회)

    Returns:
        USD_equiv, GOLD_equiv, details per exposure, formula
    """
    return dual_unit_reduce(exposures, gold_price)


@mcp.tool()
def signal_log(
    action: str = "stats",
    signal_type: str = "",
    strength: float = 0.0,
    basis: str = "",
    limit: int = 10,
) -> dict:
    """
    [v3.0 신규] Accumulation Signal Logger — 기록 및 조회 (백서 13장 + 허생전 프로토콜).

    기록 전용. 절대 매매하지 않음. 최소 8회 누적 전 자본투입 금지.

    Args:
        action: "record" (시그널 기록) / "stats" (통계) / "log" (로그 조회)
        signal_type: record 시 사용. dsi_stress / won_overvaluation / treasury_watchlist / fed_hike_cycle / gold_discount / regime_change
        strength: record 시 사용. 시그널 강도 0.0~1.0
        basis: record 시 사용. 시그널 발생 근거
        limit: log 조회 시 최근 N개

    Returns:
        action=stats: 누적 통계 / action=log: 최근 로그 / action=record: 기록된 시그널
    """
    if action == "record":
        if not signal_type or not basis:
            return {"error": "record 액션에는 signal_type과 basis 필수"}
        return record_signal(signal_type, strength, basis)
    elif action == "log":
        return {"log": get_log(limit=limit, signal_type=signal_type if signal_type else None)}
    else:
        return get_stats()


@mcp.tool()
def compound_simulator(
    monthly_contribution: float = 370.0,
    years: int = 5,
    usd_cash_return: float | None = None,
    gold_return: float | None = None,
    usd_bond_return: float | None = None,
    bucket_usd_cash: float = 0.40,
    bucket_gold: float = 0.35,
    bucket_bond: float = 0.25,
    fee_rate: float = 0.0,
) -> dict:
    """
    [v3.3 신규] Module 10 — Compound Reinvestment Simulator (백서 13.2/13.6절).

    트랙2(FX/금) 전용 복리누적곡선 시뮬레이터.
    3-Bucket(USD 현금/금/단기국채) 복리 재투자 시뮬레이션.

    ⚠️ 가드레일:
    - 트랙1(IP)과 직접비교 그래프 생성 금지
    - 5년 미만은 "평가시기상조" 라벨 자동 부착
    - 확정 수익 보장 아님

    Args:
        monthly_contribution: 월 적립액 (USD, 기본 $370 ≈ 50만원)
        years: 시뮬레이션 기간 (년, 기본 5, 최소 5년 권장)
        usd_cash_return: USD 현금/MMF 연수익률 (기본 0.04)
        gold_return: 금 연수익률 (기본 0.06)
        usd_bond_return: 단기국채 연수익률 (기본 0.045)
        bucket_usd_cash: USD 현금/MMF 비중 (기본 0.40)
        bucket_gold: 금 비중 (기본 0.35)
        bucket_bond: 단기국채 비중 (기본 0.25)
        fee_rate: 세금/수수료 차감율 (기본 0.0)

    Returns:
        시뮬레이션 결과 + 버킷별 내역 + 평가준비도
    """
    bucket_weights = {
        "USD_cash": bucket_usd_cash,
        "GOLD": bucket_gold,
        "USD_bond": bucket_bond,
    }
    return run_module10(
        monthly_contribution=monthly_contribution,
        years=years,
        bucket_weights=bucket_weights,
        usd_cash_return=usd_cash_return,
        gold_return=gold_return,
        usd_bond_return=usd_bond_return,
        fee_rate=fee_rate,
    )


@mcp.tool()
def compound_track2(
    monthly_contribution_krw: float = 500_000,
    usd_krw_rate: float = 1500.0,
    years: int = 5,
) -> dict:
    """
    [v3.3 신규] Module 10 — 원화 기준 편의 래퍼.

    월 원화 적립액을 입력하면 USD 자동 환산 후 복리 시뮬레이션 실행.

    Args:
        monthly_contribution_krw: 월 적립액 (원화, 기본 500,000원)
        usd_krw_rate: 적용 환율 (기본 1500)
        years: 시뮬레이션 기간 (년, 기본 5)

    Returns:
        시뮬레이션 결과
    """
    return run_module10_for_track2(
        monthly_contribution_krw=monthly_contribution_krw,
        usd_krw_rate=usd_krw_rate,
        years=years,
    )


@mcp.tool()
def fx_pipeline(
    currency: str = "KRW",
    exposures: list[dict] | None = None,
    nominal_surplus: float | None = None,
    year: int | None = None,
    record_signal: bool = True,
    run_compound: bool = False,
    compound_monthly: float = 370,
    compound_years: int = 5,
) -> dict:
    """
    [v3.3 업데이트] FX Engine 풀 파이프라인 실행.

    GATE 0 → Module 3(헤게모니 수수료) → Module 7(듀얼 유닛 환산)
    → Module 8(시그널 로깅) → Module 10(복리 시뮬레이터, 옵션)

    ⚠️ 가드레일:
    - 트랙2 = 복리 컴파운드 수익 트랙 — 손실방어용 보험 아님
    - "End-Station=FX" = 로데이터 무시 아님. 산업/경상수지 데이터는 환율 모델 입력 검증용 사료.
    - GATE 0 무력화 금지 — 로데이터를 완전히 0으로 만들면 GATE 0이 통째로 의미 상실.

    Args:
        currency: 대상 통화 (KRW/JPY/TWD)
        exposures: Module 7용 통화 노출 리스트 (선택)
            예: [{"currency": "KRW", "amount": 100000000, "label": "원화 예금"}]
        nominal_surplus: 명목 경상흑자 억 USD (선택, 테이블 참조)
        year: 분석 연도 (선택, 현재년도)
        record_signal: Module 8 시그널 기록 여부 (기본 True)
        run_compound: Module 10 복리 시뮬레이션 실행 여부 (기본 False)
        compound_monthly: 월 적립액 USD (기본 370, run_compound=True 시)
        compound_years: 시뮬레이션 기간 년 (기본 5)

    Returns:
        gate0, module3_hegemonic_fee, module7_dual_unit, module8_signal,
        module10_compound(옵션), pipeline_status
    """
    return run_pipeline(
        currency, exposures, nominal_surplus, year, record_signal,
        run_compound, compound_monthly, compound_years,
    )


@mcp.tool()
def fx_snapshot() -> dict:
    """
    [v3.0 신규] KRW/JPY/TWD 전체 Quick Snapshot.

    GATE 0 + 헤게모니 수수료를 3개 통화 동시 실행.
    Module 7/8은 제외 (전체 파이프라인은 fx_pipeline 호출).
    """
    return run_quick_snapshot()


# ═══════════════════════════════════════════════════════════════════════════════
# 버전 조회 (v2.2 호환 + v3.0 확장)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def version() -> dict:
    """
    달러 시스템 MCP 버전 및 툴 목록 조회.

    Returns:
        name, version, tools, description
    """
    return {
        "name": "달러 시스템 MCP",
        "version": VERSION,
        "tools": [
            # v2.2 (레거시)
            "analyze      — 환율 4단계 티어 분석 + Φ7 매핑",
            "structure    — 달러 시스템 버그와 패치의 역사",
            "phi7         — Φ7 7축 렌즈 맵",
            "get_timeline — 1944-2024 역사 타임라인",
            "compare      — 두 환율 비교",
            "get_drivers  — yfinance 실시간 4개 드라이버",
            "forecast     — 선형회귀 + DXY 보정 환율 예측",
            "dsi          — DSI 스트레스 지수 + BS_INDEX + 백테스트",
            "meal_index   — 한 끼 지수: 달러를 생존 단위로 번역",
            # v3.0 FX Engine
            "gate0_check  — GATE 0 데이터 출처 검증 게이트",
            "hegemonic_fee— 헤게모니 수수료 계산",
            "dual_unit_reduce — N 통화 → GOLD/USD 2유닛 환산",
            "signal_log   — 시그널 기록/통계/로그",
            "fx_pipeline  — GATE0→Fee→Dual→Signal→Compound 풀 파이프라인",
            "fx_snapshot  — KRW/JPY/TWD 퀵 스냅샷",
            # v3.3 신규
            "compound_simulator — [v3.3] Module 10 복리 재투자 시뮬레이터",
            "compound_track2    — [v3.3] 원화 기준 복리 시뮬레이션 편의 래퍼",
            "version      — 버전 조회",
        ],
        "desc": "미국 자본주의 바이탈사인 — 달러 패권 구조를 Φ7 7축으로 해석 + yfinance 실시간 예측 + DSI 스트레스 지수 + FX Engine v3.3 (GATE 0 → 헤게모니 수수료 → 듀얼유닛 → 시그널 로거 → 복리 시뮬레이터)",
        "philosophy": "환율은 가격표가 아니다. 달러 시스템은 심장이고, 원달러는 말초혈관 혈압계다.",
        "fx_engine": {
            "version": "3.3.0",
            "modules": [
                "Module 0: GATE 0 — Data Provenance & Integrity (14장)",
                "Module 3: Hegemonic Fee Calculator (5.3절)",
                "Module 7: Dual-Unit Reduction Engine (7.4~7.6절)",
                "Module 8: Accumulation Signal Logger (13장)",
                "Module 10: Compound Reinvestment Simulator (13.2/13.6절, v3.3 신규)",
            ],
            "pipeline": "GATE 0 → Fee → Dual-Unit → Signal → Compound",
            "guardrails": (
                "12개 하드코딩 — 트랙2 구조알파, 레버리지 금지, 8회 미만 자본투입 금지, "
                "5년 미만 평가 금지, 트랙1 비교 금지, GATE 0 우회 금지"
            ),
            "status": "✅ v3.3 투트랙 확정판 — Module 10(복리시뮬레이터) 추가 완료",
        },
    }


if __name__ == "__main__":
    mcp.run()
