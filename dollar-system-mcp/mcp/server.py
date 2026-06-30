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
from module11_ai_labor_rate import (
    run_module11 as run_ai_labor,
    calc_ai_labor_rate,
    compare_ai_vs_human,
    labor_hegemonic_fee,
    list_model_pricing,
)
from module12_platform_fee import (
    calc_platform_fee,
    benford_view_count_check,
    reduce_platform_units,
    fetch_distribution_log,
)
from module13_sonho import (
    calc_sonho_fee,
    calc_attraction_capital,
    run_module13 as run_sonho,
)
from module14_knowledge_atom import (
    scan_and_register as ka_scan,
    query_knowledge as ka_query,
    generate_primer as ka_primer,
    knowledge_stats as ka_stats,
    run_module14 as run_knowledge,
)

VERSION = "3.5.0"

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
# v3.4 — PEM 경제 MCP (Q2/Q3/Q4)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def ai_labor_rate(
    token_count: int,
    usd_per_million_tokens: float = 35.0,
    session_minutes: float = 60.0,
    output_count: int = 1,
    model_name: str = "unknown",
    source_tier: str = "S급",
) -> dict:
    """
    [v3.4 PEM Q4] AI 노동 단가 계산 — 세션 토큰소모량 기반 실측.

    단일 AI 세션의 시간당 노동단가를 토큰소모량 × 모델단가로 산출.
    "AI한테 일 시키는데 시간당 얼마 드냐"의 실측값.

    Args:
        token_count: 세션 총 토큰 소모량 (OrbitPrompt 실제 로그 기준 100K~200K)
        usd_per_million_tokens: 100만 토큰당 USD. 모델별 기본값: Claude Opus $35(입출력 평균), DeepSeek $0.7
        session_minutes: 세션 지속 시간 (분)
        output_count: 생성된 결과물 수
        model_name: 모델 식별자 (선택)
        source_tier: 데이터 등급 (S/A/B/C, 기본 S급)

    Returns:
        session_cost, hourly_rate, source_tier 반영
    """
    return calc_ai_labor_rate(token_count, usd_per_million_tokens, session_minutes, output_count, model_name, source_tier)


@mcp.tool()
def ai_vs_human(
    ai_hourly_rate_usd: float,
    human_hourly_rate_usd: float,
    human_source_note: str = "",
) -> dict:
    """
    [v3.4 PEM Q4] AI vs 인간 노동 단가 비교.

    스프레드 수치만 제시 — 해석은 사용자 판단.
    "AI가 인간을 대체한다"는 결론 자동생성 금지.

    Args:
        ai_hourly_rate_usd: AI 시간당 단가 (ai_labor_rate 결과)
        human_hourly_rate_usd: 인간 시간당 단가 (출처 필수 명시)
        human_source_note: 인간 단가 출처 (예: "2025년 원가회계사 평균연봉")

    Returns:
        ratio, savings_pct, absolute_spread, cost_effectiveness
    """
    return compare_ai_vs_human(ai_hourly_rate_usd, human_hourly_rate_usd, human_source_note=human_source_note)


@mcp.tool()
def labor_fee(
    productivity_growth_pct: float,
    real_wage_growth_pct: float,
    source_tier: str = "B급",
) -> dict:
    """
    [v3.4 PEM Q4] 임률 헤게모니 수수료.

    생산성증가율 vs 실질임금증가율 격차 = AI 시대 노동 헤게모니 수수료.
    hegemonic_fee.py 계산식 패턴 재사용.

    Args:
        productivity_growth_pct: 생산성 증가율 (%)
        real_wage_growth_pct: 실질 임금 증가율 (%)
        source_tier: 데이터 등급 (기본 B급)

    Returns:
        gap_pct, hegemonic_fee_rate_pct, fee_ratio_pct
    """
    return labor_hegemonic_fee(productivity_growth_pct, real_wage_growth_pct, source_tier)


@mcp.tool()
def platform_fee(
    gross_view_value_usd: float,
    net_settlement_usd: float,
    platform_name: str = "YouTube",
    source_tier: str = "S급",
) -> dict:
    """
    [v3.4 PEM Q2] 플랫폼 헤게모니 수수료.

    콘텐츠 조회수 가치 대비 실제 정산액 격차 → 유튜브/네이버가 가져가는 구조적 수수료율.
    hegemonic_fee.py 패턴 재사용.

    Args:
        gross_view_value_usd: 콘텐츠 조회수 추정 가치 (USD)
        net_settlement_usd: 실제 정산액 (USD, 0이면 수익화 이전)
        platform_name: 플랫폼명 (기본 YouTube)
        source_tier: 데이터 등급

    Returns:
        hegemonic_fee_rate_pct, settlement_rate_pct, interpretation
    """
    return calc_platform_fee(gross_view_value_usd, net_settlement_usd, platform_name, source_tier)


@mcp.tool()
def view_anomaly_check(
    daily_view_series: list[int],
    label: str = "daily_views",
) -> dict:
    """
    [v3.4 PEM Q2] 조회수 Benford's Law 검증 — 봇트래픽 탐지.

    GATE 0의 benford_check()를 조회수 시계열에 그대로 재적용.
    경고만 표시, 판단은 보류 (자동 무효화 금지).

    Args:
        daily_view_series: 일별 조회수 리스트 (최소 50개 필요)
        label: 데이터 라벨

    Returns:
        benford 결과, bot_traffic_suspected, warning
    """
    return benford_view_count_check(daily_view_series, label)


@mcp.tool()
def platform_reduce(
    platform_exposures: list[dict],
) -> dict:
    """
    [v3.4 PEM Q2] N개 플랫폼 → 유효_조회당_단가 1개 유닛 환원.

    dual_unit.py reduce() 패턴 변형: N→1유닛.
    유튜브/텔레그램/티스토리/네이버를 단일 CPV로 통합.

    Args:
        platform_exposures: 플랫폼별 노출 데이터.
            각 항목: {"platform": "youtube", "views": 1000, "settlement_usd": 5.0, "source_tier": "S급"}

    Returns:
        weighted_avg_cpv, platform_breakdown, total_fee_est
    """
    return reduce_platform_units(platform_exposures)


@mcp.tool()
def sonho_fee(
    monthly_revenue: float,
    rent: float,
    depreciation: float = 0.0,
    overhead: float = 0.0,
    venue_name: str = "unknown",
    source_tier: str = "S급",
) -> dict:
    """
    [v3.4 PEM Q3] 소호 임대료 헤게모니 수수료.

    공방/스튜디오 매출 대비 고정비(임대료+감가상각+관리비) 부담률.
    = 물리공간이 가져가는 구조적 비용.
    hegemonic_fee.py 패턴 재사용.

    Args:
        monthly_revenue: 월 매출 (KRW 또는 USD)
        rent: 월 임대료
        depreciation: 월 장비 감가상각비
        overhead: 월 관리비/공과금
        venue_name: 공간명
        source_tier: 데이터 등급 (기본 S급)

    Returns:
        hegemonic_fee_rate_pct, net_margin_pct, interpretation
    """
    return calc_sonho_fee(monthly_revenue, rent, depreciation, overhead, venue_name, source_tier)


@mcp.tool()
def attraction_capital(
    guild_response_count: int,
    marketing_cost: float = 0.0,
    time_cost_hours: float = 0.0,
    hourly_rate_usd: float = 0.0,
    guild_name: str = "unknown",
    source_tier: str = "S급",
) -> dict:
    """
    [v3.4 PEM Q3] 매력 자본 계수 — "인류를 측정했다"는 박씨 표현의 수식화.

    길드 모집 응답률 ÷ (마케팅비 + 시간비용).
    Bourdieu 문화자본 개념의 계량화 버전.

    ⚠️ 이 계수 정의는 1차 확정 후 변경 금지 (시계열 단절 방지).

    Args:
        guild_response_count: 길드 모집 응답자 수
        marketing_cost: 마케팅 비용 (USD)
        time_cost_hours: 투입 시간 (시간)
        hourly_rate_usd: 시간당 단가 (USD)
        guild_name: 길드명
        source_tier: 데이터 등급 (기본 S급)

    Returns:
        attraction_coefficient, cost_per_response_usd, interpretation
    """
    return calc_attraction_capital(guild_response_count, marketing_cost, time_cost_hours, hourly_rate_usd, guild_name, source_tier)


# ═══════════════════════════════════════════════════════════════════════════════
# v3.5 — Knowledge-Atom MCP (Q1-Q4 범용 / EAE Univ 전환)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def register_knowledge(
    include_body: bool = True,
    include_butterfly: bool = True,
    include_philosophy: bool = True,
    force_rescan: bool = False,
) -> dict:
    """
    [v3.5 신규] eae-univ 스캔 → knowledge-atom 레지스트리 구축.

    EAE University의 research/body, research/butterfly, philosophy/ 디렉토리를
    스캔해 article JSON과 철학 문서를 표준 knowledge-atom으로 등록.
    등록된 atom은 query_knowledge()로 검색 가능.

    Args:
        include_body: research/body/ 포함 (기본 True)
        include_butterfly: research/butterfly/ 포함 (기본 True)
        include_philosophy: philosophy/ 포함 (기본 True)
        force_rescan: True면 기존 레지스트리 무시하고 전수 재스캔

    Returns:
        total_atoms, newly_registered, domain_distribution
    """
    return ka_scan(include_body, include_butterfly, include_philosophy, force_rescan)


@mcp.tool()
def query_knowledge(
    keyword: str = "",
    domain: str = "",
    verdict: str = "",
    min_confidence: int = 0,
    max_results: int = 20,
) -> dict:
    """
    [v3.5 신규] knowledge-atom 검색.

    등록된 지식원자를 키워드/도메인/평결/신뢰도로 검색.
    "야 철학 개론 알려줘" → query_knowledge(domain="philosophy")
    "야 운동 관련 지식 있어?" → query_knowledge(keyword="운동")

    Args:
        keyword: 제목/테제/체인에서 검색 (공백=전체)
        domain: 도메인 필터 (body/butterfly/philosophy)
        verdict: 평결 필터 (PROCEED/REDUCE/HOLD)
        min_confidence: 최소 신뢰도 0-100
        max_results: 최대 결과 수 (기본 20)

    Returns:
        query 조건, total_matches, results(atom 목록)
    """
    return ka_query(keyword, domain, verdict, min_confidence, max_results)


@mcp.tool()
def generate_primer(
    domain: str = "",
    thesis_keyword: str = "",
    max_atoms: int = 10,
    include_analysis: bool = True,
) -> dict:
    """
    [v3.5 신규] knowledge-atom 종합 → 개론서(primer) 생성.

    관련 knowledge-atom을 모아서 개론서 형태로 재구성.
    각 atom의 thesis/chain/verdict/confidence 기반.
    "철학 개론서 만들어줘" → generate_primer(domain="philosophy")

    Args:
        domain: 도메인 필터 (body/butterfly/philosophy)
        thesis_keyword: 테제 키워드 필터
        max_atoms: 포함할 최대 atom 수 (기본 10)
        include_analysis: 종합 분석 포함 여부 (기본 True)

    Returns:
        title, sections[], summary(verdict분포/공통체인/평균신뢰도)
    """
    return ka_primer(domain, thesis_keyword, max_atoms, include_analysis)


@mcp.tool()
def knowledge_stats() -> dict:
    """
    [v3.5 신규] knowledge-atom 레지스트리 통계.

    등록된 전체 atom의 도메인별 분포, 평결 분포, 신뢰도 통계, PEM 사분면 분포.

    Returns:
        total_atoms, domain_distribution, verdict_distribution,
        confidence_stats, pem_quadrant_distribution
    """
    return ka_stats()


# ═══════════════════════════════════════════════════════════════════════════════
# 버전 조회 (v2.2 호환 + v3.0 확장 + v3.4 PEM MCP + v3.5 Knowledge-Atom)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def version() -> dict:
    """
    달러 시스템 MCP 버전 및 툴 목록 조회.

    Returns:
        name, version, tools, description
    """
    return {
        "name": "parksy-economy-fx",
        "version": VERSION,
        "tools": [
            # v2.2 (레거시)
            "analyze            — 환율 4단계 티어 분석 + Φ7 매핑",
            "structure          — 달러 시스템 버그와 패치의 역사",
            "phi7               — Φ7 7축 렌즈 맵",
            "get_timeline       — 1944-2024 역사 타임라인",
            "compare            — 두 환율 비교",
            "get_drivers        — yfinance 실시간 4개 드라이버",
            "forecast           — 선형회귀 + DXY 보정 환율 예측",
            "dsi                — DSI 스트레스 지수 + BS_INDEX + 백테스트",
            "meal_index         — 한 끼 지수: 달러를 생존 단위로 번역",
            # v3.0 FX Engine
            "gate0_check        — GATE 0 데이터 출처 검증 게이트",
            "hegemonic_fee      — 헤게모니 수수료 계산",
            "dual_unit_reduce   — N 통화 → GOLD/USD 2유닛 환산",
            "signal_log         — 시그널 기록/통계/로그",
            "fx_pipeline        — GATE0→Fee→Dual→Signal→Compound 풀 파이프라인",
            "fx_snapshot        — KRW/JPY/TWD 퀵 스냅샷",
            # v3.3 신규
            "compound_simulator — Module 10 복리 재투자 시뮬레이터",
            "compound_track2    — 원화 기준 복리 시뮬레이션 편의 래퍼",
            # v3.4 PEM Q4 (labor-rate)
            "ai_labor_rate      — [PEM Q4] AI 노동 단가 실측",
            "ai_vs_human        — [PEM Q4] AI vs 인간 단가 비교",
            "labor_fee          — [PEM Q4] 임률 헤게모니 수수료",
            # v3.4 PEM Q2 (platform-fee)
            "platform_fee       — [PEM Q2] 플랫폼 헤게모니 수수료",
            "view_anomaly_check — [PEM Q2] 조회수 Benford 검증 (봇트래픽)",
            "platform_reduce    — [PEM Q2] N개 플랫폼 → 1개 유닛 환원",
            # v3.4 PEM Q3 (sonho)
            "sonho_fee          — [PEM Q3] 소호 임대료 헤게모니 수수료",
            "attraction_capital — [PEM Q3] 매력 자본 계수",
            # v3.5 Knowledge-Atom MCP
            "register_knowledge — [v3.5] eae-univ 스캔 → knowledge-atom 등록",
            "query_knowledge    — [v3.5] knowledge-atom 검색 (keyword/domain/verdict/confidence)",
            "generate_primer    — [v3.5] knowledge-atom 종합 → 개론서 생성",
            "knowledge_stats    — [v3.5] knowledge-atom 레지스트리 통계",
            # 공통
            "version            — 버전 조회",
        ],
        "total_tools": 30,
        "desc": "parksy-economy-fx — FX Engine v3.5 + PEM Q2/Q3/Q4 경제 MCP + Knowledge-Atom MCP 통합. ",
        "philosophy": "환율은 가격표가 아니다. 달러 시스템은 심장이고, 원달러는 말초혈관 혈압계다.",
        "pem_matrix": {
            "Q1": {"name": "FX/환율", "status": "⬛ 완료", "module": "dollar_engine + gate0 + hegemonic_fee + dual_unit"},
            "Q2": {"name": "플랫폼", "status": "🟩 v1.0 구현", "module": "module12_platform_fee"},
            "Q3": {"name": "소호스튜디오", "status": "🟩 v1.0 구현", "module": "module13_sonho"},
            "Q4": {"name": "임률/AI노동", "status": "🟩 v1.0 구현", "module": "module11_ai_labor_rate"},
            "KA": {"name": "Knowledge-Atom", "status": "🟩 v1.0 구현", "module": "module14_knowledge_atom"},
            "infra": {"name": "공통모듈", "status": "⬜ GATE0/hegemonic_fee 재사용"},
        },
        "fx_engine": {
            "version": "3.5.0",
            "modules": [
                "Module 0: GATE 0 — Data Provenance & Integrity",
                "Module 3: Hegemonic Fee Calculator",
                "Module 7: Dual-Unit Reduction Engine",
                "Module 8: Accumulation Signal Logger",
                "Module 10: Compound Reinvestment Simulator",
                "Module 11: AI Labor Rate (PEM Q4)",
                "Module 12: Platform Fee (PEM Q2)",
                "Module 13: Sonho Economy (PEM Q3)",
                "Module 14: Knowledge-Atom (EAE Univ 전환)",
            ],
            "pipeline": "GATE 0 → Fee → Dual-Unit → Signal → Compound | PEM Q2-Q4 병렬 | Knowledge-Atom 레지스트리",
            "guardrails": (
                "loose coupling (GATE0 재사용), 사후분석 고정, source_tier 의무 표기, "
                "Q2/Q3/Q4 간 직접비교 금지 (우열비교 아님), 5년 미만 평가 금지, "
                "register_knowledge()는 scan_and_register() 경유 (직접 레지스트리 수정 금지)"
            ),
            "status": "✅ v3.5 Knowledge-Atom MCP 통합 — Q1(환율) + Q2(플랫폼) + Q3(소호) + Q4(임률) + Knowledge-Atom",
        },
    }


if __name__ == "__main__":
    mcp.run()
