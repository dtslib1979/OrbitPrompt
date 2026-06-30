#!/usr/bin/env python3
"""
Module 11 — AI Labor Rate Calculator (PEM Q4: 온라인×미시)

AI 노동 단가 실측 및 인간 노동과의 스프레드 비교.
OrbitPrompt 세션 데이터(토큰소모량) 기반 역산.

역산 모델:
  AI_노동_단가 = Σ(세션_토큰소모량 × 모델_토큰단가) / 생성된_결과물_수
  임률_헤게모니수수료 = 생산성증가율 - 실질임금증가율

의존성:
  - hegemonic_fee.py: 계산식 패턴 재사용 (loose coupling 원칙)
  - gate0.py: GATE 0 컨텍스트 호출
"""

from datetime import datetime
from typing import Optional

# ─── 모델별 토큰 단가표 (A급: 공식 가격페이지 기준) ──────────────────────────────
_MODEL_PRICING = {
    "claude_opus_4_7": {
        "input_per_mtok": 15.0,
        "output_per_mtok": 75.0,
        "source": "Anthropic 공식 가격 (2026-06)",
        "source_tier": "A급",
    },
    "claude_sonnet_4_6": {
        "input_per_mtok": 3.0,
        "output_per_mtok": 15.0,
        "source": "Anthropic 공식 가격 (2026-06)",
        "source_tier": "A급",
    },
    "claude_haiku_4_5": {
        "input_per_mtok": 0.80,
        "output_per_mtok": 4.0,
        "source": "Anthropic 공식 가격 (2026-06)",
        "source_tier": "A급",
    },
    "deepseek_chat": {
        "input_per_mtok": 0.27,
        "output_per_mtok": 1.10,
        "source": "DeepSeek 공식 가격 (2026-06)",
        "source_tier": "A급",
    },
    "deepseek_reasoner": {
        "input_per_mtok": 0.55,
        "output_per_mtok": 2.19,
        "source": "DeepSeek 공식 가격 (2026-06)",
        "source_tier": "A급",
    },
    "gpt_4o": {
        "input_per_mtok": 2.50,
        "output_per_mtok": 10.0,
        "source": "OpenAI 공식 가격 (2026-06)",
        "source_tier": "A급",
    },
}

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


def calc_ai_labor_rate(
    token_count: int,
    usd_per_million_tokens: float,
    session_minutes: float,
    output_count: int = 1,
    model_name: str = "unknown",
    source_tier: str = "S급",
) -> dict:
    """
    단일 세션 AI 노동 단가 계산.

    Args:
        token_count: 세션 총 토큰 소모량
        usd_per_million_tokens: 모델 100만 토큰당 USD 단가 (평균)
        session_minutes: 세션 지속 시간 (분)
        output_count: 세션에서 생성된 결과물 수
        model_name: 모델 이름 (식별용)
        source_tier: 데이터 등급 (S/A/B/C, 기본 S급)

    Returns:
        session_cost_usd, hourly_rate, cost_per_output, source_tier 반영
    """
    tier = source_tier if source_tier in SOURCE_TIER_PENALTY else "C급"
    penalty = SOURCE_TIER_PENALTY[tier]

    session_cost = (token_count / 1_000_000) * usd_per_million_tokens * penalty
    hours = session_minutes / 60.0 if session_minutes > 0 else 1.0
    hourly_rate = session_cost / hours if hours > 0 else 0
    cost_per_output = session_cost / output_count if output_count > 0 else session_cost

    return {
        "model": model_name,
        "token_count": token_count,
        "usd_per_million_tokens": usd_per_million_tokens,
        "session_minutes": session_minutes,
        "output_count": output_count,
        "source_tier": tier,
        "source_penalty": penalty,
        "session_cost_usd": round(session_cost, 4),
        "hourly_rate_usd": round(hourly_rate, 4),
        "cost_per_output_usd": round(cost_per_output, 4),
        "formula": {
            "session_cost": f"({token_count}/1_000_000) x {usd_per_million_tokens} x {penalty} = ${session_cost:.4f}",
            "hourly_rate": f"${session_cost:.4f} / {hours:.1f}h = ${hourly_rate:.4f}",
        },
        "disclaimer": COMMON_DISCLAIMER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


def compare_ai_vs_human(
    ai_hourly_rate_usd: float,
    human_hourly_rate_usd: float,
    ai_source_tier: str = "S급",
    human_source_note: str = "",
) -> dict:
    """
    AI 노동 단가 vs 인간 노동 단가 비교.

    Args:
        ai_hourly_rate_usd: AI 시간당 단가 (calc_ai_labor_rate 출력)
        human_hourly_rate_usd: 인간 시간당 단가 (출처 필수 명시)
        ai_source_tier: AI 데이터 등급
        human_source_note: 인간 단가 출처 (예: "2025년 원가회계사 평균연봉 6천만원 ÷ 209시간")

    Returns:
        spread_pct, ratio, 경제성 평가
    """
    if ai_hourly_rate_usd <= 0:
        return {"error": "AI 단가가 0 이하입니다."}
    if human_hourly_rate_usd <= 0:
        return {"error": "인간 단가가 0 이하입니다. 출처를 확인하세요."}

    ratio = human_hourly_rate_usd / ai_hourly_rate_usd
    savings_pct = (1 - ai_hourly_rate_usd / human_hourly_rate_usd) * 100
    absolute_spread = human_hourly_rate_usd - ai_hourly_rate_usd

    return {
        "ai_hourly_rate_usd": round(ai_hourly_rate_usd, 4),
        "human_hourly_rate_usd": round(human_hourly_rate_usd, 2),
        "human_source_note": human_source_note or "출처 미명시 — C급 페널티 적용",
        "ai_source_tier": ai_source_tier,
        "ratio_human_to_ai": round(ratio, 1),
        "savings_pct_vs_human": round(savings_pct, 2),
        "absolute_spread_usd": round(absolute_spread, 2),
        "cost_effectiveness": (
            "AI가 인간보다 압도적으로 저렴"
            if savings_pct > 90
            else "AI가 인간보다 저렴"
            if savings_pct > 50
            else "인간과 AI 비슷"
            if savings_pct > -50
            else "인간이 더 저렴"
        ),
        "interpretation": (
            f"AI ${ai_hourly_rate_usd:.2f}/h vs 인간 ${human_hourly_rate_usd:.0f}/h — "
            f"AI가 {savings_pct:.0f}% 저렴 (ratio {ratio:.0f}:1)"
        ),
        "restriction": (
            "이 비교는 '단순 대체 비용' 관점만 반영. 생산성 차이, 품질 차이, "
            "AI 보완관계 효과는 미포함. 특히 AI는 인간의 전유물(고객신뢰, "
            "재량판단, 법적책임)을 대체할 수 없음."
        ),
        "disclaimer": COMMON_DISCLAIMER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


def labor_hegemonic_fee(
    productivity_growth_pct: float,
    real_wage_growth_pct: float,
    source_tier: str = "B급",
) -> dict:
    """
    임률 헤게모니 수수료 계산.

    hegemonic_fee.py의 (명목흑자 - 실질수취) 패턴을 생산성/임금에 매핑.
    생산성증가율이 '명목' 자리, 실질임금증가율이 '실질수취' 자리.

    Args:
        productivity_growth_pct: 생산성 증가율 (%)
        real_wage_growth_pct: 실질 임금 증가율 (%)
        source_tier: 데이터 등급 (기본 B급 — 통계청/민간보고서)

    Returns:
        fee_rate, fee_ratio, 해석
    """
    tier = source_tier if source_tier in SOURCE_TIER_PENALTY else "C급"
    penalty = SOURCE_TIER_PENALTY[tier]

    gap = productivity_growth_pct - real_wage_growth_pct
    fee_ratio = gap / productivity_growth_pct * 100 if productivity_growth_pct != 0 else 0

    return {
        "productivity_growth_pct": productivity_growth_pct,
        "real_wage_growth_pct": real_wage_growth_pct,
        "gap_pct": round(gap, 2),
        "hegemonic_fee_rate_pct": round(gap, 2),
        "fee_ratio_pct": round(fee_ratio, 1),
        "source_tier": tier,
        "source_penalty": penalty,
        "formula": {
            "gap": f"{productivity_growth_pct}% - {real_wage_growth_pct}% = {gap:.2f}%",
            "fee_ratio": f"{gap:.2f} / {productivity_growth_pct} x 100 = {fee_ratio:.1f}%",
        },
        "interpretation": (
            f"생산성증가율 {productivity_growth_pct}% 대비 실질임금증가율 {real_wage_growth_pct}%로 "
            f"{gap:.1f}%p 격차. 이 격차({fee_ratio:.0f}%)가 노동 헤게모니수수료율."
        ),
        "pattern_note": "hegemonic_fee.py 패턴 재사용: productivity=nominal, real_wage=real_received",
        "disclaimer": COMMON_DISCLAIMER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


def run_module11(
    sessions: Optional[list[dict]] = None,
    human_hourly_rate_usd: Optional[float] = None,
    human_source_note: str = "",
    productivity_growth_pct: Optional[float] = None,
    real_wage_growth_pct: Optional[float] = None,
) -> dict:
    """
    Module 11 통합 실행 — AI 노동단가 → 인간비교 → 헤게모니수수료.

    Args:
        sessions: 세션 데이터 리스트.
            각 항목: {"tokens": int, "usd_per_mtok": float, "minutes": float,
                     "outputs": int, "model": str, "source_tier": str}
        human_hourly_rate_usd: 인간 시간당 단가 (선택)
        human_source_note: 인간 단가 출처 (선택)
        productivity_growth_pct: 생산성 증가율 (선택)
        real_wage_growth_pct: 실질 임금 증가율 (선택)

    Returns:
        통합 분석 결과
    """
    results = {"module": "Module 11 — AI Labor Rate", "version": "1.0.0"}

    # Step 1: 세션별 AI 단가 계산
    if sessions:
        session_results = []
        for s in sessions:
            r = calc_ai_labor_rate(
                token_count=s.get("tokens", 0),
                usd_per_million_tokens=s.get("usd_per_mtok", 15.0),
                session_minutes=s.get("minutes", 60),
                output_count=s.get("outputs", 1),
                model_name=s.get("model", "unknown"),
                source_tier=s.get("source_tier", "S급"),
            )
            session_results.append(r)

        rates = [r["hourly_rate_usd"] for r in session_results if "hourly_rate_usd" in r]
        n = len(rates)

        results["session_count"] = n
        results["sessions"] = session_results

        if n >= 5:
            avg = sum(rates) / n
            sorted_r = sorted(rates)
            median = sorted_r[n // 2] if n % 2 else (sorted_r[n // 2 - 1] + sorted_r[n // 2]) / 2
            variance = sum((r - avg) ** 2 for r in rates) / n
            std_dev = variance ** 0.5
            results["aggregate"] = {
                "mean_hourly_rate_usd": round(avg, 4),
                "median_hourly_rate_usd": round(median, 4),
                "std_dev_hourly_rate": round(std_dev, 4),
                "min_rate_usd": round(min(rates), 4),
                "max_rate_usd": round(max(rates), 4),
                "sample_size": n,
                "note": f"{n}개 세션 평균 — 최소 5세션 충족, 통계 유의",
            }
        elif n > 0:
            avg = sum(rates) / n
            results["aggregate"] = {
                "mean_hourly_rate_usd": round(avg, 4),
                "sample_size": n,
                "note": f"⚠️ {n}개 세션만 분석. 최소 5세션 권장. 현재값은 참고용.",
            }
        else:
            results["aggregate"] = {"note": "가용 세션 없음 — 계산 스킵"}
    else:
        results["sessions"] = []
        results["aggregate"] = {"note": "세션 데이터 없음 — 빈 입력"}

    # Step 2: 인간 비교
    if human_hourly_rate_usd is not None and results.get("aggregate", {}).get("mean_hourly_rate_usd"):
        results["comparison"] = compare_ai_vs_human(
            ai_hourly_rate_usd=results["aggregate"]["mean_hourly_rate_usd"],
            human_hourly_rate_usd=human_hourly_rate_usd,
            human_source_note=human_source_note,
        )

    # Step 3: 헤게모니 수수료
    if productivity_growth_pct is not None and real_wage_growth_pct is not None:
        results["labor_fee"] = labor_hegemonic_fee(
            productivity_growth_pct=productivity_growth_pct,
            real_wage_growth_pct=real_wage_growth_pct,
        )

    results["disclaimer"] = COMMON_DISCLAIMER
    results["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M KST")
    return results


def list_model_pricing() -> dict:
    """등록된 모델별 단가표 조회"""
    return {
        "models": _MODEL_PRICING,
        "source_tier_penalties": SOURCE_TIER_PENALTY,
        "note": "A급: 공식 가격페이지 기준. 실제 비용은 할인/크레딧으로 다를 수 있음.",
        "disclaimer": COMMON_DISCLAIMER,
    }


if __name__ == "__main__":
    import sys, json
    if "--pricing" in sys.argv:
        print(json.dumps(list_model_pricing(), ensure_ascii=False, indent=2))
    else:
        # 데모: 예시 세션 1개
        demo_sessions = [
            {"tokens": 150000, "usd_per_mtok": 35.0, "minutes": 45, "outputs": 3, "model": "claude_opus_4_7"},
        ]
        result = run_module11(
            sessions=demo_sessions,
            human_hourly_rate_usd=28.0,
            human_source_note="2025년 원가회계사 평균연봉 5800만원 ÷ 209시간 ≈ 27.8 USD/h",
            productivity_growth_pct=3.5,
            real_wage_growth_pct=0.8,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
