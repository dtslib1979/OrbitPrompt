"""12개 재무비율 × 5개 관점 매핑 테이블"""

RATIOS = {
    1: ("매출 성장률", "Revenue Growth Rate"),
    2: ("매출 규모", "Revenue Scale"),
    3: ("매출총이익률", "Gross Margin"),
    4: ("영업이익률", "Operating Margin"),
    5: ("순이익률", "Net Margin"),
    6: ("ROE", "Return on Equity"),
    7: ("ROIC", "Return on Invested Capital"),
    8: ("자산회전율", "Asset Turnover"),
    9: ("재고회전율", "Inventory Turnover"),
    10: ("부채비율", "Debt-to-Equity"),
    11: ("이자보상배율", "Interest Coverage"),
    12: ("PSR/PER", "Price-to-Sales / Price-to-Earnings"),
}

PERSPECTIVES = {
    1: ("Form", "Form", "구조와 형태 — 현재 상태의 구조적 윤곽"),
    2: ("Flow", "Flow", "돈의 흐름과 수익 모델 — 현금이 어떻게 순환하는가"),
    3: ("Frag", "Frag", "취약성과 리스크 — 어디서 붕괴가 시작되는가"),
    4: ("Field", "Field", "현장 운영과 공급망 — 실제 땅 위에서 무슨 일이 벌어지는가"),
    5: ("Fit", "Fit", "삶과 장기 정렬성 — 이 구조가 인간 가치와 맞닿는가"),
}

SMART_CLAND_AXES = {
    "S": ("Structure", "구조 — 비즈니스 골격"),
    "M": ("Model", "수익모델 — 돈 버는 방식"),
    "A": ("Adoption", "사용·채택 — 실제 사용 깊이"),
    "R": ("Risk", "리스크 — 위험 요인"),
    "T": ("Trajectory", "성장 경로 — 방향과 속도"),
    "C": ("Community", "커뮤니티 — 팬덤·생태계"),
    "L": ("Lifestyle", "라이프스타일 — 정체성과의 정합성"),
    "A2": ("Anchor", "의존·락인 — 전환 비용"),
    "N": ("Norm", "규범·문화 — 사회적 정합성"),
    "D": ("Daywork", "현장·노동 — 사람의 시간과 몸"),
}


def slot_id(h: int, m: int) -> str:
    """좌표 → 슬롯 ID (예: 4시 3분 → '04h3m')"""
    return f"{h:02d}h{m}m"


def get_names(h: int, m: int) -> tuple[str, str, str, str]:
    """시/분 → (비율_한글, 비율_영문, 관점코드, 관점설명)"""
    r_ko, r_en = RATIOS[h]
    p_code, p_en, p_desc = PERSPECTIVES[m]
    return r_ko, r_en, p_code, p_desc


def describe_slot(h: int, m: int) -> dict:
    """슬롯 전체 메타데이터"""
    r_ko, r_en, p_code, p_desc = get_names(h, m)
    return {
        "slot_id": slot_id(h, m),
        "hour": h,
        "minute": m,
        "ratio_ko": r_ko,
        "ratio_en": r_en,
        "perspective_code": p_code,
        "perspective_desc": p_desc,
    }


def all_slots() -> list[dict]:
    """60개 슬롯 전체 목록"""
    return [describe_slot(h, m) for h in range(1, 13) for m in range(1, 6)]
