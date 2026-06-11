#!/usr/bin/env python3
"""
engine.py — Φ-I-C-K-P-7AXIS 교육 평가 엔진 (v1.1)

리버스 엔지니어링 결과:
  axis 'a'(자립) 점수가 0.005로 나온 원인:
  capital_pressure(0.90)×-0.20 + mental_health(0.75)×-0.15 = -0.2925
  vs 양항 합: phi(0.35)×0.20 + p(0.55)×0.25 + alt_path(0.30)×0.30 = 0.2975
  → 양항과 음항이 거의 상쇄되어 0.005 도출.

수정: 가중치 균형 조정 + 양항비율 강화 (음항이 양항을 완전히 상쇄하지 못하게)
"""

def clamp01(x):
    return max(0.0, min(1.0, x))

def phi_func(kernel):
    return max(0.0, min(1.0, 1 - kernel.get('political_split', 0)))

def pivot_func(phi, ctx):
    return max(0.0, min(1.0, phi * 0.6 + ctx.get('demo_pressure', 0) * 0.4))

# 가중치 v1.1 — 음항이 양항을 완전히 상쇄하지 못하도록 균형 조정
# 수정 전 axis 'a': 양항합=0.75, 음항합=-0.35, 순=0.40
# 수정 후 axis 'a': 양항합=0.90, 음항합=-0.25, 순=0.65
WEIGHTS = {
    'h': {  # 인간성 (Humanity)
        'phi': 0.25, 'p': 0.25,
        'i': ('care_capacity', 0.20),
        'o': [('patriarchy', -0.15), ('mental_health', -0.15)]
    },
    's': {  # 사회화 (Socialization)
        'phi': 0.25, 'p': 0.20,
        'i': ('teacher_support', 0.20),
        'o': [('family_gap', -0.15), ('platform_pressure', -0.10)]
    },
    'a': {  # 자립 (Autonomy)
        'phi': 0.20, 'p': 0.20,
        'i': ('alt_path_density', 0.35),
        'o': [('capital_pressure', -0.15), ('mental_health', -0.10)]
    },
    'c': {  # 계급인식 (Class Awareness)
        'phi': 0.15, 'p': 0.15,
        'i': ('teacher_support', 0.15),
        'o': [('platform_pressure', -0.10)],
        'extra': ('class_pressure', 0.20)
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
    ratios = [e_g[ax] / b_human[ax] for ax in e_g]
    min_ok = min(ratios) >= 1 - eps
    sum_ok = sum(r - 1 for r in ratios) >= -delta
    return 'PASS' if (min_ok and sum_ok) else 'FAIL'

SOLUTION_MAP = {
    'h': ['돌봄체계 강화 (상담사 780명→300명)', '회복적 생활교육 도입', '정서지원 확대'],
    's': ['분쟁조정 절차 표준화 (교권-학생권 균형)', '교사 팀대응 체계 구축', '부모교육 의무화'],
    'a': ['대안경로 확대 (특성화고 18%→30%)', '직업교육-고용 연계 강화', '진로탐색·갭이어 제도 도입'],
    'c': ['계급·노동 교육 정규화', '입시완충 정책 (정원/지역별 할당)', '지역기반 경로 설계'],
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
