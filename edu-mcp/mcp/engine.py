#!/usr/bin/env python3
"""
engine.py — Φ-I-C-K-P-7AXIS 교육 평가 엔진

축구 MCP(Φ5+Φ7)의 교육 포팅.
K,C,I,O_t 입력 → E_g 4축 추정 → B_human 기준선 판정 → 솔루션 추천.

리뷰 97점 반영:
  - clamp01() 구현
  - axis_* 4개 함수 → WEIGHTS 사전 + axis_score() 통합
  - 변수명 충돌 제거 (k→kernel, for k→for ax)
"""

def clamp01(x):
    """0~1 클램프"""
    return max(0.0, min(1.0, x))

def phi_func(kernel):
    """K 상태 → 철학 일관성 점수 (0~1)"""
    return max(0.0, min(1.0, 1 - kernel.get('political_split', 0)))

def pivot_func(phi, ctx):
    """Φ, C → Pivot 방향성 (0=입시중심, 1=돌봄중심)"""
    return max(0.0, min(1.0, phi * 0.6 + ctx.get('demo_pressure', 0) * 0.4))

# 가중치 사전 — 4개 축 통합 (리뷰 97점 반영)
# axis_h/s/a/c 4개 함수 중복을 WEIGHTS + axis_score()로 단일화
WEIGHTS = {
    'h': {
        'phi': 0.35, 'p': 0.30,
        'i': ('care_capacity', 0.20),
        'o': [('patriarchy', -0.25), ('mental_health', -0.20)]
    },
    's': {
        'phi': 0.30, 'p': 0.25,
        'i': ('teacher_support', 0.25),
        'o': [('family_gap', -0.25), ('platform_pressure', -0.20)]
    },
    'a': {
        'phi': 0.20, 'p': 0.25,
        'i': ('alt_path_density', 0.30),
        'o': [('capital_pressure', -0.20), ('mental_health', -0.15)]
    },
    'c': {
        'phi': 0.15, 'p': 0.15,
        'i': ('teacher_support', 0.20),
        'o': [('platform_pressure', -0.20)],
        'extra': ('class_pressure', 0.20)
    }
}

def axis_score(axis, phi, p, infra, prob, ctx):
    """단일 축 점수 계산 (WEIGHTS 기반)"""
    w = WEIGHTS[axis]
    val = w['phi'] * phi + w['p'] * p
    # 인프라 항목
    i_name, i_wt = w['i']
    val += i_wt * infra.get(i_name, 0)
    # 문제 항목들
    for o_name, o_wt in w['o']:
        val += o_wt * prob.get(o_name, 0)
    # 추가 항목 (axis_c 전용: class_pressure)
    if 'extra' in w:
        e_name, e_wt = w['extra']
        val += e_wt * ctx.get(e_name, 0)
    return clamp01(val)

def calc_e(kernel, ctx, infra, prob):
    """K,C,I,O_t → E_g 4축 추정"""
    phi = phi_func(kernel)
    p = pivot_func(phi, ctx)
    return {ax: axis_score(ax, phi, p, infra, prob, ctx) for ax in 'hsac'}

def judge(e_g, b_human, eps=0.15, delta=0.3):
    """
    약한 파레토 + 보정항 판정
    
    조건 1: 모든 축이 기준선의 (1-eps) 이상  (한 축 포기 금지)
    조건 2: 전체 결손 합이 -delta 이상      (제한적 보정 허용)
    """
    ratios = [e_g[ax] / b_human[ax] for ax in e_g]
    min_ok = min(ratios) >= 1 - eps
    sum_ok = sum(r - 1 for r in ratios) >= -delta
    return 'PASS' if (min_ok and sum_ok) else 'FAIL'

SOLUTION_MAP = {
    'h': ['돌봄체계 강화', '회복적 생활교육', '정서지원 확대'],
    's': ['분쟁조정 절차 표준화', '교사 팀대응 체계', '부모교육 강화'],
    'a': ['대안경로 확대', '직업교육 강화', '진로탐색/갭이어 제도'],
    'c': ['계급·노동 교육', '입시완충 정책', '지역기반 경로 설계'],
}

def recommend_pivot(e_g, b_human):
    """E_g와 B_human 비교 → 우선 보강 축 + 솔루션 세트"""
    gaps = {ax: b_human[ax] - e_g[ax] for ax in e_g}
    priority_axis = max(gaps, key=gaps.get)
    return {
        'priority_axis': priority_axis,
        'solution_set': SOLUTION_MAP.get(priority_axis, []),
        'gaps': {ax: round(gaps[ax], 3) for ax in gaps}
    }

if __name__ == "__main__":
    import json, sys
    # 데모 실행
    demo_k = {"political_split": 0.45, "policy_consistency": 0.40, "local_conflict": 0.50}
    demo_c = {"demo_pressure": 0.70, "platform_pressure": 0.80, "class_pressure": 0.75}
    demo_i = {"care_capacity": 0.45, "teacher_support": 0.50, "alt_path_density": 0.35}
    demo_o = {"patriarchy": 0.50, "capital_pressure": 0.85, "mental_health": 0.75, "family_gap": 0.65, "platform_pressure": 0.80}
    demo_b = {"h": 0.70, "s": 0.70, "a": 0.65, "c": 0.60}
    
    e = calc_e(demo_k, demo_c, demo_i, demo_o)
    j = judge(e, demo_b)
    r = recommend_pivot(e, demo_b)
    
    print(json.dumps({
        "E_g": e,
        "judgment": j,
        "recommendation": r
    }, ensure_ascii=False, indent=2))
