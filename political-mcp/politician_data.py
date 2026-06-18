#!/usr/bin/env python3
"""
politician_data.py — 정치인 기초 데이터
Φ드라이버 7축 계산용 베이스라인
"""

# 정치인 기초 데이터 (당선횟수 / 지지율 / 재임 지역구 / 소속)
POLITICIANS = {
    "박찬대": {
        "party": "더불어민주당",
        "region": "인천 연수구을",
        "terms": 4,
        "base_approval": 52.0,
        "age": 58,
        "role": "원내대표"
    },
    "이재명": {
        "party": "더불어민주당",
        "region": "인천 계양구을",
        "terms": 5,
        "base_approval": 48.0,
        "age": 60,
        "role": "대표"
    },
    "한동훈": {
        "party": "국민의힘",
        "region": "비례대표",
        "terms": 1,
        "base_approval": 38.0,
        "age": 51,
        "role": "대표"
    },
    "조국": {
        "party": "조국혁신당",
        "region": "비례대표",
        "terms": 2,
        "base_approval": 42.0,
        "age": 60,
        "role": "대표"
    },
}

# Φ드라이버 7축 정치 버전 가중치
AXIS_WEIGHTS = {
    "meta":     1.2,  # 발언 일관성 — 공약 vs 실제 행동
    "reverse":  1.1,  # 위기 대응 — 역풍 맞았을 때 회복력
    "modular":  1.0,  # 정책 패턴 — 반복 가능한 정책 공식
    "language": 1.0,  # 수사 — 프레이밍, 언어 장악력
    "zoom":     1.2,  # 의제 집중도 — 핵심 이슈 관통력
    "spiral":   1.3,  # 성장 궤적 — 선수를 거듭할수록 강해지나
    "quantum":  1.5,  # 이변 가능성 — 판세 뒤집는 변수 보유
}

PHI5_WEIGHT = 0.3  # 기초 데이터 비중

def calc_base_strength(name: str) -> float:
    """기초 Φ5 점수: 당선횟수 + 지지율 + 역할 가중치"""
    p = POLITICIANS.get(name)
    if not p:
        return 50.0
    role_bonus = {"대표": 10, "원내대표": 8, "장관": 7, "의원": 0}.get(p["role"], 0)
    score = (p["terms"] * 8) + (p["base_approval"] * 0.6) + role_bonus
    return round(min(100, max(20, score)), 1)
