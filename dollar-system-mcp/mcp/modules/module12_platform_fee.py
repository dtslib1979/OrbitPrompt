#!/usr/bin/env python3
"""
Module 12 — Platform Fee Calculator (PEM Q2: 온라인×거시)

플랫폼 헤게모니 수수료 측정 — 콘텐츠 조회수 대비 실제 정산액 격차.
parksy-distributor 송출 기록 + YouTube/Telegram/Tistory/Naver 데이터.

역산 모델:
  플랫폼_헤게모니수수료 = 콘텐츠_조회수_가치 - 실제_정산액

의존성:
  - gate0.py: benford_check 재사용 (loose coupling)
  - hegemonic_fee.py: 계산식 패턴 재사용
  - dual_unit.py: N→1 유닛 환원 패턴 재사용
"""

from datetime import datetime, timedelta
from typing import Optional

# ─── GATE 0 benford_check import ──────────────────────────────────────────────
try:
    from gate0 import benford_check as _gate0_benford
except ImportError:
    def _gate0_benford(data, label=""):
        """Fallback: gate0 benford_check 사용 불가"""
        return {"error": "gate0.benford_check import 실패", "data_label": label}


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

# ─── 플랫폼별 기준 CPV (Cost Per View, USD) — B급(민간/업계 보고서) ──────────────
_PLATFORM_CPV_ESTIMATES = {
    "youtube": {"cpv_usd": 0.01, "note": "업계 평균 CPM $10 / 1000 views", "source_tier": "B급"},
    "telegram": {"cpv_usd": 0.005, "note": "Telegram 광고 CPM ~$5 (추정)", "source_tier": "C급"},
    "tistory": {"cpv_usd": 0.003, "note": "국내 블로그 CPM ~$3 (추정)", "source_tier": "C급"},
    "naver": {"cpv_usd": 0.008, "note": "Naver CPM ~$8 (업계 보고서)", "source_tier": "B급"},
}


def calc_platform_fee(
    gross_view_value_usd: float,
    net_settlement_usd: float,
    platform_name: str = "unknown",
    source_tier: str = "S급",
) -> dict:
    """
    플랫폼 헤게모니 수수료 계산.

    hegemonic_fee.py 패턴 재사용: gross_view_value = 명목흑자,
    net_settlement = 실질수취.

    Args:
        gross_view_value_usd: 콘텐츠 조회수 추정 가치 (USD)
        net_settlement_usd: 실제 정산액 (USD)
        platform_name: 플랫폼 이름 (식별용)
        source_tier: 데이터 등급

    Returns:
        fee_amount, fee_rate, 해석
    """
    tier = source_tier if source_tier in SOURCE_TIER_PENALTY else "C급"
    penalty = SOURCE_TIER_PENALTY[tier]

    if gross_view_value_usd <= 0:
        return {"error": "조회수 가치가 0 이하입니다."}

    fee_amount = gross_view_value_usd - net_settlement_usd
    fee_rate = fee_amount / gross_view_value_usd * 100
    settlement_rate = net_settlement_usd / gross_view_value_usd * 100

    return {
        "platform": platform_name,
        "gross_view_value_usd": round(gross_view_value_usd, 2),
        "net_settlement_usd": round(net_settlement_usd, 2),
        "fee_amount_usd": round(fee_amount, 2),
        "hegemonic_fee_rate_pct": round(fee_rate, 2),
        "settlement_rate_pct": round(settlement_rate, 2),
        "source_tier": tier,
        "source_penalty": penalty,
        "formula": {
            "fee_amount": f"{gross_view_value_usd:.2f} - {net_settlement_usd:.2f} = {fee_amount:.2f}",
            "fee_rate": f"{fee_amount:.2f} / {gross_view_value_usd:.2f} x 100 = {fee_rate:.2f}%",
        },
        "interpretation": (
            f"{platform_name}: 콘텐츠 가치 ${gross_view_value_usd:.2f} 중 "
            f"실제 정산 ${net_settlement_usd:.2f}, "
            f"플랫폼 수수료 ${fee_amount:.2f} ({fee_rate:.0f}%)"
        ),
        "pattern_note": "hegemonic_fee.py 패턴 재사용: gross_value=nominal, settlement=real_received",
        "restriction": (
            "정산액은 광고수익/구독수익 등 실제 입금액 기준. "
            "'추정 조회수 가치'는 업계 평균 CPM 기반 추정치일 수 있음."
        ),
        "disclaimer": COMMON_DISCLAIMER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


def benford_view_count_check(
    daily_view_series: list[int],
    label: str = "daily_views",
) -> dict:
    """
    조회수 시계열 Benford's Law 검증.

    GATE 0의 benford_check()를 그대로 재사용 — 봇트래픽/조회수 조작 의심 탐지.

    Args:
        daily_view_series: 일별 조회수 리스트
        label: 데이터 식별 라벨

    Returns:
        benford 결과 + 봇트래픽 의심도
    """
    if not daily_view_series or len(daily_view_series) < 50:
        return {
            "error": f"데이터 부족: {len(daily_view_series) if daily_view_series else 0}개 (최소 50 필요)",
            "label": label,
        }

    result = _gate0_benford(daily_view_series, label=label)

    # 봇트래픽 의심 판정
    if "error" in result:
        return result

    chi_square = result.get("chi_square", 0)
    is_suspicious = chi_square > 15.0

    result["bot_traffic_suspected"] = is_suspicious
    result["bot_warning"] = (
        "⚠️ Benford 분포 이탈 감지 — 봇트래픽/조회수 조작 의심. "
        "단, 이 결과만으로 무효 판정하지 말 것. 추가 검증 필요."
        if is_suspicious
        else "✅ Benford 분포 정상 — 봇트래픽 징후 없음."
    )
    result["action"] = (
        "경고만 표시, 판단은 보류. 추가 분석(IP 패턴, 행동 시계열) 필요."
        if is_suspicious
        else "정상"
    )
    result["disclaimer"] = COMMON_DISCLAIMER

    return result


def reduce_platform_units(
    platform_exposures: list[dict],
) -> dict:
    """
    N개 플랫폼 노출 → '유효_조회당_단가' 1개 유닛 환원.

    dual_unit.py reduce() 패턴 변형 — N→2유닛이 아니라 N→1유닛.

    Args:
        platform_exposures: 플랫폼별 노출 데이터.
            각 항목: {"platform": str, "views": int, "settlement_usd": float, "source_tier": str}

    Returns:
        weighted_avg_cpv, platform_breakdown, 총조회수/총정산
    """
    if not platform_exposures:
        return {"error": "플랫폼 노출 데이터 없음"}

    total_views = 0
    total_settlement = 0.0
    total_gross_value = 0.0
    breakdown = []

    for p in platform_exposures:
        platform = p.get("platform", "unknown")
        views = p.get("views", 0)
        settlement = p.get("settlement_usd", 0.0)
        tier = p.get("source_tier", "C급")
        penalty = SOURCE_TIER_PENALTY.get(tier, 0.5)

        cpv_est = _PLATFORM_CPV_ESTIMATES.get(platform, {}).get("cpv_usd", 0.005)
        gross_value = views * cpv_est * penalty

        total_views += views
        total_settlement += settlement
        total_gross_value += gross_value

        breakdown.append({
            "platform": platform,
            "views": views,
            "estimated_gross_value_usd": round(gross_value, 2),
            "settlement_usd": round(settlement, 2),
            "effective_cpv_usd": round(settlement / views, 6) if views > 0 else 0,
            "source_tier": tier,
        })

    weighted_avg_cpv = total_settlement / total_views if total_views > 0 else 0
    total_fee = total_gross_value - total_settlement
    total_fee_rate = total_fee / total_gross_value * 100 if total_gross_value > 0 else 0

    return {
        "total_views": total_views,
        "total_gross_value_usd": round(total_gross_value, 2),
        "total_settlement_usd": round(total_settlement, 2),
        "total_fee_est_usd": round(total_fee, 2),
        "total_fee_rate_pct": round(total_fee_rate, 2),
        "weighted_avg_cpv_usd": round(weighted_avg_cpv, 6),
        "platform_breakdown": breakdown,
        "unit": "유효_조회당_단가(weighted_avg_cpv_usd) — N개 플랫폼을 1개 단위로 환원",
        "pattern_note": "dual_unit.py reduce() 패턴 변형: N→1유닛 환원",
        "restriction": (
            "Gross value는 업계 평균 CPV 기반推定치. "
            "실제 정산액이 0에 수렴하면 플랫폼 수수료율이 100%에 근접할 수 있음 — "
            "이는 '수익화 이전 단계'의 정상적 현상이지 '실패'가 아님."
        ),
        "disclaimer": COMMON_DISCLAIMER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


def fetch_distribution_log(
    channel_type: str = "all",
    days: int = 30,
) -> dict:
    """
    parksy-distributor 송출 로그 조회 (인터페이스만 — 실제 DB 연동은 별도).

    Args:
        channel_type: 채널 유형 필터 ("youtube"/"telegram"/"tistory"/"naver"/"all")
        days: 최근 N일 (기본 30)

    Returns:
        채널별 송출건수, 채널 목록, 데이터 상태
    """
    # TODO: parksy-distributor DB/webhook 로그 연동
    # 현재는 인터페이스 정의만 반환
    return {
        "status": "인터페이스 정의됨 — 실제 DB 미연동",
        "channel_type": channel_type,
        "days": days,
        "data": [],
        "note": (
            "parksy-distributor DB 연동 전: 이 함수는 인터페이스 스펙만 정의. "
            "실제 데이터 조회는 DB/webhook 연동 후 가능."
        ),
        "platforms_available": list(_PLATFORM_CPV_ESTIMATES.keys()),
        "integration_required": [
            "parksy-distributor DB 스키마 확인",
            "YouTube Data API v3 OAuth 연동",
            "Telegram bot API 통계 로깅",
        ],
        "disclaimer": COMMON_DISCLAIMER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


if __name__ == "__main__":
    import sys, json

    if "--benford" in sys.argv:
        # 데모: 정상 vs 의심 조회수
        import random
        normal = [random.randint(50, 200) for _ in range(100)]
        result = benford_view_count_check(normal, "정상_조회수")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif "--fetch" in sys.argv:
        print(json.dumps(fetch_distribution_log(), ensure_ascii=False, indent=2))
    else:
        # 데모: 플랫폼 수수료
        result = calc_platform_fee(
            gross_view_value_usd=1000.0,
            net_settlement_usd=120.0,
            platform_name="YouTube",
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
