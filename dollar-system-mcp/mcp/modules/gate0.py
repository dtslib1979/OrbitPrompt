#!/usr/bin/env python3
"""
GATE 0 — Data Provenance & Integrity Gate (백서 14장)

모든 외부 로데이터는 이 게이트를 통과해야만 하위 모듈로 전달 가능.
PASS / WARNING / BLOCK 3단 판정 + 신뢰도 가중치 조정 + 역용 시그널.

5단계 검증:
  1. 출처 계보 확인 (Source Chain)
  2. Benford's Law 1차 분계
  3. 시계열 불연속성 탐지 (Regime Change)
  4. 발행기관 인센티브 분석 (Issuer Incentive)
  5. 교차검증 합의도 (Cross-Source Consensus)
"""

import math, hashlib
from datetime import datetime
from typing import Any


# ─── Step 1: 출처 계보 확인 ─────────────────────────────────────────────────────

_PRIMARY_DOMAINS = [
    "bok.or.kr", "bankofkorea.or.kr",        # 한국은행
    "boj.or.jp", "bankofjapan.or.jp",        # 일본은행
    "cbc.gov.tw",                              # 대만 중앙은행
    "treasury.gov", "federalreserve.gov",      # 미국 재무부/Fed
    "imf.org", "bis.org", "oecd.org",          # 국제기구
    "stats.gov.cn", "pbc.gov.cn",              # 중국 통계/인민은행
    "ecb.europa.eu", "bundesbank.de",          # 유럽중앙은행
]

_SECONDARY_DOMAINS = [
    "reuters.com", "bloomberg.com", "wsj.com",
    "ft.com", "cnbc.com", "marketwatch.com",
    "investing.com", "tradingview.com",
]

def _extract_domain(url: str) -> str:
    """URL에서 도메인 추출"""
    url = url.lower().strip()
    for prefix in ["https://", "http://"]:
        if url.startswith(prefix):
            url = url[len(prefix):]
    return url.split("/")[0].split("@")[-1].split(":")[0]

def classify_source(url_or_name: str) -> dict:
    """
    출처 분류 및 신뢰도 점수 산출.

    Returns:
        tier: "1차(정부원문)" / "1차(국제기구)" / "2차(금융전문)" / "2차(취합)" / "3차(미분류)"
        confidence_base: 0.0 ~ 1.0
    """
    domain = _extract_domain(url_or_name)

    for pd in _PRIMARY_DOMAINS:
        if pd in domain:
            if any(gov in domain for gov in ["or.kr", "go.jp", "gov", "bank"]):
                return {"tier": "1차(정부원문)", "confidence_base": 1.0}
            return {"tier": "1차(국제기구)", "confidence_base": 0.95}

    for sd in _SECONDARY_DOMAINS:
        if sd in domain:
            if sd in ["reuters.com", "bloomberg.com"]:
                return {"tier": "2차(금융전문)", "confidence_base": 0.80}
            return {"tier": "2차(취합)", "confidence_base": 0.65}

    return {"tier": "3차(미분류)", "confidence_base": 0.40}


# ─── Step 2: Benford's Law ─────────────────────────────────────────────────────

_BENFORD_EXPECTED = [math.log10(1 + 1/d) for d in range(1, 10)]

def _extract_first_digit(values: list[float]) -> list[int]:
    """숫자 배열에서 첫째 자리 추출"""
    digits = []
    for v in values:
        s = f"{abs(v):.10f}"
        for ch in s:
            if ch.isdigit() and ch != "0":
                digits.append(int(ch))
                break
    return digits

def benford_check(data_series: list[float]) -> dict:
    """
    Benford's Law 적합도 검정.

    Returns:
        deviation: 0~1 (0=완전일치, 1=완전이탈)
        status: "정상범위" / "주의" / "의심"
        detail: 각 첫째자리별 observed vs expected
    """
    if len(data_series) < 20:
        return {
            "deviation": 0.0,
            "status": "표본부족",
            "detail": f"표본 {len(data_series)}개 (최소 20개 필요)",
            "note": "Benford 검증 불가 — 표본 부족으로 PASS 처리"
        }

    digits = _extract_first_digit(data_series)
    if not digits:
        return {"deviation": 0.0, "status": "분석불가", "detail": "유효한 첫째자리 없음"}

    n = len(digits)
    observed = [digits.count(d) / n for d in range(1, 10)]

    # 카이제곱 유사도 이탈도
    deviation = sum((obs - exp) ** 2 / max(exp, 0.001)
                    for obs, exp in zip(observed, _BENFORD_EXPECTED))
    # 정규화 (0~1)
    normalized_dev = min(1.0, deviation / 5.0)

    if normalized_dev > 0.5:
        status = "의심"
    elif normalized_dev > 0.25:
        status = "주의"
    else:
        status = "정상범위"

    detail = {
        str(d): {
            "observed": round(observed[d-1], 4),
            "expected": round(_BENFORD_EXPECTED[d-1], 4)
        }
        for d in range(1, 10)
    }

    return {
        "deviation": round(normalized_dev, 3),
        "status": status,
        "detail": detail,
        "note": "Benford 이탈 = 확정 조작 증거 아님. 추가 검증 트리거로만 사용."
    }


# ─── Step 3: 시계열 불연속성 탐지 ──────────────────────────────────────────────

def regime_change_detect(
    series: list[float],
    window: int = 3,
    threshold_std: float = 2.5
) -> dict:
    """
    최근 데이터 포인트가 과거 분포 대비 급변했는지 탐지.

    Returns:
        flag: True/False
        z_score: 최근값의 표준편차 이탈도
        note: 해석
    """
    if len(series) < window + 1:
        return {"flag": False, "z_score": 0.0, "note": "데이터 부족"}

    recent = series[-window:]
    past = series[:-window]

    if len(past) < 2:
        return {"flag": False, "z_score": 0.0, "note": "과거 데이터 부족"}

    mu = sum(past) / len(past)
    std = math.sqrt(sum((x - mu) ** 2 for x in past) / len(past))

    if std == 0:
        return {"flag": False, "z_score": 0.0, "note": "과거 분산 0 — 변화 없음"}

    recent_mean = sum(recent) / len(recent)
    z = abs(recent_mean - mu) / std

    return {
        "flag": z > threshold_std,
        "z_score": round(z, 2),
        "note": f"최근 {window}개값 평균, 과거대비 {z:.1f}σ 이탈{' — 기준 변경 의심' if z > threshold_std else ''}"
    }


# ─── Step 4: 발행기관 인센티브 분석 ──────────────────────────────────────────────

_ISSUER_INTERESTS = {
    "us treasury":       "무역협상 레버리지, 달러 강세 선호 (수입물가 억제)",
    "federal reserve":   "물가안정 vs 고용, 금리정책 정당화 필요",
    "bank of korea":     "원화 방어 부담, 외환보유고 관리 압박",
    "bank of japan":     "국채 금리 억제, 엔화 약세 방어 한계",
    "cbc":               "대만달러 안정, TSMC 협상력 유지",
    "goldman sachs":     "FX 트레이딩 포지션 보유 — 전망에 이해상충 가능",
    "jp morgan":         "FX 트레이딩 포지션 보유 — 전망에 이해상충 가능",
    "moody's":           "국가신용등급 변경 전후 이해상충",
    "s&p":               "국가신용등급 변경 전후 이해상충",
    "imf":               "회원국 협력 유지 — 외교적 언어 제약",
}

def issuer_incentive_flag(source_name: str, context: str = "") -> dict:
    """
    데이터 발행기관의 인센티브 분석.

    Returns:
        flag_level: "낮음" / "중간" / "높음"
        reason: 인센티브 설명
        conflict: 잠재적 이해상충
    """
    source_lower = source_name.lower()

    for keyword, interest in _ISSUER_INTERESTS.items():
        if keyword in source_lower:
            if any(w in source_lower for w in ["trading", "research", "securities", "bank", "capital"]):
                level = "중간"
                return {
                    "flag_level": level,
                    "reason": interest,
                    "conflict": f"해당 기관이 관련 포지션 보유 가능성 — {interest}"
                }
            return {
                "flag_level": "낮음",
                "reason": interest,
                "conflict": "공식 기관 — 인센티브 존재하나 직접 포지션 충돌 낮음"
            }

    return {
        "flag_level": "미분류",
        "reason": "인센티브 데이터베이스에 등록되지 않은 발행처",
        "conflict": "분석 불가 — 주의 필요"
    }


# ─── Step 5: 교차검증 합의도 ─────────────────────────────────────────────────────

def cross_source_consensus(values: list[float]) -> dict:
    """
    동일 지표에 대한 복수 출처 값의 합의도.

    Returns:
        consensus: 0~1 (1=완전합의)
        cv: 변동계수
        status: "높음" / "중간" / "낮음"
    """
    if len(values) < 2:
        return {"consensus": 1.0, "cv": 0.0, "status": "단일출처", "note": "단일 출처 — 교차검증 불가"}

    mu = sum(values) / len(values)
    if mu == 0:
        return {"consensus": 0.0, "cv": float("inf"), "status": "오류"}

    std = math.sqrt(sum((x - mu) ** 2 for x in values) / len(values))
    cv = std / abs(mu)

    consensus = max(0.0, min(1.0, 1.0 - cv * 2))

    if consensus > 0.85:
        status = "높음"
    elif consensus > 0.60:
        status = "중간"
    else:
        status = "낮음"

    return {
        "consensus": round(consensus, 3),
        "cv": round(cv, 4),
        "status": status,
        "n_sources": len(values),
        "note": "불일치 클수록 GATE 신뢰도 점수 하락 → 하위모듈 가중치 자동 축소"
    }


# ─── Gate 0 통합 검증 ──────────────────────────────────────────────────────────

def run_gate0(
    data_point_name: str,
    source_url: str,
    data_series: list[float] | None = None,
    cross_source_values: list[float] | None = None,
    context: str = "",
) -> dict:
    """
    GATE 0 통합 실행 — 5단계 전체 검증.

    Args:
        data_point_name: 검증할 데이터 포인트명
        source_url: 데이터 출처 URL
        data_series: Benford 검증용 숫자 배열 (선택)
        cross_source_values: 교차검증용 복수 출처 값 배열 (선택)
        context: 발행기관 인센티브 분석 컨텍스트

    Returns:
        14.6절 JSON 포맷 준수
    """
    # Step 1: 출처 계보
    source_info = classify_source(source_url)
    confidence = source_info["confidence_base"]

    # Step 2: Benford
    benford_result = benford_check(data_series) if data_series else {
        "deviation": 0.0, "status": "미적용", "detail": "데이터 미제공"
    }
    if benford_result["status"] in ("의심", "주의"):
        confidence *= 0.7 if benford_result["status"] == "의심" else 0.85

    # Step 3: Regime Change
    regime_result = {"flag": False, "z_score": 0.0, "note": "데이터 미제공"}
    if data_series and len(data_series) >= 4:
        regime_result = regime_change_detect(data_series)
    if regime_result["flag"]:
        confidence *= 0.8

    # Step 4: Issuer Incentive
    incentive_result = issuer_incentive_flag(source_url, context)
    if incentive_result["flag_level"] == "높음":
        confidence *= 0.75
    elif incentive_result["flag_level"] == "중간":
        confidence *= 0.9

    # Step 5: Cross-Source Consensus
    consensus_result = cross_source_consensus(cross_source_values) if cross_source_values else {
        "consensus": 1.0, "cv": 0.0, "status": "미적용", "note": "교차검증 미실시"
    }
    confidence *= consensus_result["consensus"]

    # ── 역용 시그널 ──────────────────────────────────────────────────────────
    # 조정 횟수/이탈 빈도가 높은 지표 = "누군가 관리하고 싶어하는" 신호
    reverse_signal_flags = []
    if benford_result["status"] == "의심":
        reverse_signal_flags.append("Benford 이탈 반복 → 데이터 관리 의심")
    if regime_result["flag"]:
        reverse_signal_flags.append("기준 변경 감지 → 해당 지표 정책적 중요도 상승")
    if incentive_result["flag_level"] in ("중간", "높음"):
        reverse_signal_flags.append("발행기관 이해상충 → 데이터 해석에 보수적 가중치 필요")
    if consensus_result["status"] == "낮음":
        reverse_signal_flags.append("출처간 불일치 → 해당 지표의 측정방식 자체가 논쟁중")

    reverse_signal = "지표 주목도 상승 — Module 7 워치리스트 등록 권고" if len(reverse_signal_flags) >= 2 else "없음"

    # ── Gate 종합 판정 ──────────────────────────────────────────────────────
    confidence = round(min(1.0, confidence), 3)

    if confidence < 0.35:
        gate_status = "BLOCK"
    elif confidence < 0.55:
        gate_status = "WARNING"
    else:
        gate_status = "PASS"

    weight_adjustment = f"{round((1 - confidence) * -100)}%" if confidence < 1.0 else "0%"

    return {
        "data_point": data_point_name,
        "source": source_url,
        "source_tier": source_info["tier"],
        "benford_deviation": benford_result["status"],
        "regime_change_flag": regime_result["flag"],
        "issuer_incentive_flag": incentive_result["flag_level"],
        "cross_source_consensus": consensus_result["consensus"],
        "gate_status": gate_status,
        "confidence_score": confidence,
        "confidence_weight_adjustment": weight_adjustment,
        "역용_signal": reverse_signal,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
        "guardrails": [
            "Benford 이탈 ≠ 조작 확정 — 추가 검증 트리거",
            "게이트 통과 = 100% 진실 아님 — 필터일 뿐",
            "역용 시그널 = 가설적 휴리스틱 — 트레이딩 확정신호 아님",
            "이 게이트 우회 금지 — 모든 외부데이터는 예외없이 통과 필수",
            "End-Station=FX 명제로 GATE 0 무력화 금지 — 로데이터는 '버리는 노이즈'가 아니라 '직접 베팅하지 않는 사료'",
            "GATE 0의 존재 이유 = 로데이터 속 의도(발표타이밍/통계조작)를 역검증 — 데이터를 0으로 만들면 이 게이트도 0이 됨",
        ],
    }


if __name__ == "__main__":
    import json
    # 테스트
    test = run_gate0(
        data_point_name="KRW 2026Q2 경상수지",
        source_url="https://www.bok.or.kr/portal/main/main.do",
        data_series=[1.2, 3.4, 5.6, 7.8, 2.3, 4.5, 6.7, 1.1, 3.3, 5.5,
                     7.7, 2.2, 4.4, 6.6, 1.3, 3.5, 5.7, 7.9, 2.1, 4.3,
                     6.5, 1.4, 3.6, 5.8, 7.1],
        cross_source_values=[1500, 1510, 1490, 1505],
        context="한국은행 공식발표",
    )
    print(json.dumps(test, ensure_ascii=False, indent=2))
