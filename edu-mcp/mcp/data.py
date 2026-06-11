#!/usr/bin/env python3
"""
data.py — Φ-I-C-K-P-7AXIS 교육 MCP 기본 파라미터

기준선(B_human) 기본값, WEIGHTS 고정 사본, 샘플 입력 데이터.
"""

# 기본 인간 기준선 (B_human) — 한국 교육 시스템 기준
DEFAULT_B_HUMAN = {
    'h': 0.70,  # 인간성 최소선
    's': 0.70,  # 사회화 최소선
    'a': 0.65,  # 자립 최소선
    'c': 0.60,  # 계급 인식 최소선
}

# 기본 판정 파라미터
DEFAULT_EPS = 0.15   # 개별 축 허용 결손폭
DEFAULT_DELTA = 0.30 # 전체 결손 허용총량

# 샘플 입력 — 한국 교육 시스템 현황 (2026 추정)
SAMPLE_KOREA = {
    "K": {
        "political_split": 0.45,
        "policy_consistency": 0.40,
        "local_conflict": 0.50
    },
    "C": {
        "demo_pressure": 0.70,
        "platform_pressure": 0.80,
        "class_pressure": 0.75
    },
    "I": {
        "care_capacity": 0.45,
        "teacher_support": 0.50,
        "alt_path_density": 0.35
    },
    "O_t": {
        "patriarchy": 0.50,
        "capital_pressure": 0.85,
        "mental_health": 0.75,
        "family_gap": 0.65,
        "platform_pressure": 0.80
    }
}

# 샘플 입력 — 이상적 교육 시스템 (비교용)
SAMPLE_IDEAL = {
    "K": {"political_split": 0.15, "policy_consistency": 0.85, "local_conflict": 0.15},
    "C": {"demo_pressure": 0.40, "platform_pressure": 0.35, "class_pressure": 0.30},
    "I": {"care_capacity": 0.85, "teacher_support": 0.80, "alt_path_density": 0.75},
    "O_t": {"patriarchy": 0.15, "capital_pressure": 0.30, "mental_health": 0.25, "family_gap": 0.20, "platform_pressure": 0.30}
}
