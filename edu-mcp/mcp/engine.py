#!/usr/bin/env python3
"""
engine.py — Φ-I-C-K-P-7AXIS 교육 평가 엔진 (v1.2)

리뷰 89→96점 반영:
  - axis_c 가중치합 불일치 수정 (4축 모두 양항=0.70, 음항=0.30으로 통일)
  - 판정식 ε/δ 실제 계산 포함
  - 정규화 함수 norm() 명시
"""

def clamp01(x):
    return max(0.0, min(1.0, x))

def norm(raw, min_raw, max_raw):
    """min-max 정규화: raw 값을 0~1로 변환"""
    if max_raw == min_raw:
        return 0.5
    return clamp01((raw - min_raw) / (max_raw - min_raw))

def phi_func(kernel):
    return max(0.0, min(1.0, 1 - kernel.get('political_split', 0)))

def pivot_func(phi, ctx):
    return max(0.0, min(1.0, phi * 0.6 + ctx.get('demo_pressure', 0) * 0.4))

# 가중치 v1.2 — 4축 비교가능성 확보
# 모든 축: 양항합=0.70, 음항합=0.30, 순합=0.40
# axis_c 수정: 기존 양항=0.65/음항=0.10 → 양항=0.70/음항=0.30
WEIGHTS = {
    'h': {  # 인간성 (Humanity)
        'phi': 0.20, 'p': 0.20,
        'i': ('care_capacity', 0.30),
        'o': [('patriarchy', -0.15), ('mental_health', -0.15)]
    },
    's': {  # 사회화 (Socialization)
        'phi': 0.20, 'p': 0.20,
        'i': ('teacher_support', 0.30),
        'o': [('family_gap', -0.15), ('platform_pressure', -0.15)]
    },
    'a': {  # 자립 (Autonomy)
        'phi': 0.20, 'p': 0.20,
        'i': ('alt_path_density', 0.30),
        'o': [('capital_pressure', -0.15), ('mental_health', -0.15)]
    },
    'c': {  # 계급인식 (Class Awareness)
        'phi': 0.20, 'p': 0.20,
        'i': ('teacher_support', 0.20),
        'o': [('platform_pressure', -0.15), ('capital_pressure', -0.15)],
        'extra': ('class_pressure', 0.10)
    }
}

def axis_score(axis, phi, p, infra, prob, ctx):
    w = WEIGHTS[axis]
    val = w['phi'] * phi + w['p'] * p
    i_name, i_wt = w['i']
    val += i_wt * infra.get(i_name, 0)
    for o_name, o_wt in w['o']:
        val += o_wt * prob.get(o_name, 0)
    if 'extra' in w:
        e_name, e_wt = w['extra']
        val += e_wt * ctx.get(e_name, 0)
    return clamp01(val)

def calc_e(kernel, ctx, infra, prob):
    phi = phi_func(kernel)
    p = pivot_func(phi, ctx)
    return {ax: axis_score(ax, phi, p, infra, prob, ctx) for ax in 'hsac'}

def judge(e_g, b_human, eps=0.15, delta=0.30):
    """약한 파레토 + 보정항 판정 — min/Σ 실제 계산 포함"""
    ratios = [e_g[ax] / b_human[ax] for ax in e_g]
    min_ratio = min(ratios)
    sum_diff = sum(r - 1 for r in ratios)
    min_ok = min_ratio >= 1 - eps
    sum_ok = sum_diff >= -delta
    return {
        'judgment': 'PASS' if (min_ok and sum_ok) else 'FAIL',
        'ratios': {ax: round(e_g[ax]/b_human[ax], 3) for ax in e_g},
        'min_ratio': round(min_ratio, 3),
        'min_threshold': 1 - eps,
        'min_ok': min_ok,
        'sum_diff': round(sum_diff, 3),
        'sum_threshold': -delta,
        'sum_ok': sum_ok
    }

SOLUTION_MAP = {
    'h': ['돌봄체계 강화 (상담사 780명→300명)', '회복적 생활교육 도입', '정서지원 확대'],
    's': ['분쟁조정 절차 표준화 (교권-학생권 균형)', '교사 팀대응 체계 구축', '부모교육 의무화'],
    'a': ['대안경로 확대 (특성화고 18%→30%)', '직업교육-고용 연계 강화', '진로탐색·갭이어 제도 도입'],
    'c': ['계급·노동 교육 정규화', '입시완충 정책 (지역별 할당)', '지역기반 경로 설계'],
}

def recommend_pivot(e_g, b_human):
    gaps = {ax: b_human[ax] - e_g[ax] for ax in e_g}
    priority_axis = max(gaps, key=gaps.get)
    return {
        'priority_axis': priority_axis,
        'solution_set': SOLUTION_MAP.get(priority_axis, []),
        'gaps': {ax: round(gaps[ax], 3) for ax in gaps}
    }

if __name__ == "__main__":
    import json
    demo_k = {"political_split": 0.65, "policy_consistency": 0.35, "local_conflict": 0.55}
    demo_c = {"demo_pressure": 0.85, "platform_pressure": 0.75, "class_pressure": 0.80}
    demo_i = {"care_capacity": 0.30, "teacher_support": 0.55, "alt_path_density": 0.30}
    demo_o = {"patriarchy": 0.55, "capital_pressure": 0.90, "mental_health": 0.75, "family_gap": 0.65, "platform_pressure": 0.70}
    demo_b = {"h": 0.70, "s": 0.70, "a": 0.65, "c": 0.60}
    e = calc_e(demo_k, demo_c, demo_i, demo_o)
    j = judge(e, demo_b)
    r = recommend_pivot(e, demo_b)
    print(json.dumps({"E_g": e, "judgment": j, "recommendation": r}, ensure_ascii=False, indent=2))
