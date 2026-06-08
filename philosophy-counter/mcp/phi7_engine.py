#!/usr/bin/env python3
"""
phi7_engine.py — Φ7 동적 비교 엔진 v2

변경: 수동 점수 제거. 특징 기반 동적 유사도 계산.
      공통점 / 차이점을 실제로 발견함 (선언이 아님).
"""
import sys, json, os, math
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from philosopher_data import PHILOSOPHERS, PHI7_DIMENSIONS, PARKSY_FEATURES, get_philosopher, list_philosophers

def calc_similarity(features_a, features_b):
    """두 특징 집합의 자카드 유사도"""
    set_a = set(features_a)
    set_b = set(features_b)
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return round(len(intersection) / len(union) * 100, 1)

def calc_phi7_scores(features, dim_name):
    """특징 기반 Φ7 차원 점수 계산"""
    all_feats = PHI7_DIMENSIONS[dim_name]["features"]
    total = len(all_feats)
    matched = sum(1 for f in all_feats if f in features)
    return round(matched / total * 100, 1)

def analyze_philosopher(key):
    """철학자 1명 전체 분석 (완전 동적)"""
    p = get_philosopher(key)
    if not p:
        return {"error": f"'{key}' 없음. 목록: {list_philosophers()}"}
    
    p_feats = p["features"]
    
    # 각 차원별 점수 계산
    scores = {}
    for dim in PHI7_DIMENSIONS:
        scores[dim] = calc_phi7_scores(p_feats.get(dim, []), dim)
    
    parksy_scores = {}
    for dim in PHI7_DIMENSIONS:
        parksy_scores[dim] = calc_phi7_scores(PARKSY_FEATURES.get(dim, []), dim)
    
    # 차원별 비교
    comparisons = {}
    similarities = []
    differences = []
    discoveries = []
    
    for dim_key, dim_data in PHI7_DIMENSIONS.items():
        p_score = scores[dim_key]
        m_score = parksy_scores[dim_key]
        diff = round(p_score - m_score, 1)
        
        p_feat_set = set(p_feats.get(dim_key, []))
        m_feat_set = set(PARKSY_FEATURES.get(dim_key, []))
        
        common = p_feat_set & m_feat_set
        only_p = p_feat_set - m_feat_set
        only_m = m_feat_set - p_feat_set
        
        bar_p = "█" * max(1, int(p_score / 10)) + "░" * max(0, 10 - int(p_score / 10))
        bar_m = "█" * max(1, int(m_score / 10)) + "░" * max(0, 10 - int(m_score / 10))
        
        if abs(diff) <= 15:
            verdict = "유사한 축"
            similarities.append({
                "dimension": dim_data["name"],
                "common_features": list(common),
                "score_diff": diff
            })
        elif diff < -15:
            verdict = f"박씨가 더 강함 (차이: {abs(diff):.0f}점)"
            differences.append({
                "dimension": dim_data["name"],
                "reason": f"박씨만 가진 특징: {list(only_m)}",
                "score_diff": diff
            })
            if only_m:
                discoveries.append(f"[발견] {dim_data['name']} — 박씨만의 특징 {list(only_m)}이 {p['name']}에는 없음")
        else:
            verdict = f"{p['name']}이 더 강함 (차이: {diff:.0f}점)"
            differences.append({
                "dimension": dim_data["name"],
                "reason": f"{p['name']}만 가진 특징: {list(only_p)}",
                "score_diff": diff
            })
            if only_p:
                discoveries.append(f"[발견] {dim_data['name']} — {p['name']}만의 특징 {list(only_p)}이 박씨에는 없음")
        
        comparisons[dim_key] = {
            "axis_name": dim_data["name"],
            "philosopher_score": p_score,
            "parksy_score": m_score,
            "diff": diff,
            "philosopher_bar": bar_p,
            "parksy_bar": bar_m,
            "common_features": list(common),
            "only_philosopher": list(only_p),
            "only_parksy": list(only_m),
            "verdict": verdict
        }
    
    # 종합 점수
    avg_p = round(sum(scores.values()) / len(scores), 1)
    avg_m = round(sum(parksy_scores.values()) / len(parksy_scores), 1)
    overall_similarity = round(100 - abs(avg_p - avg_m) * 1.5, 1)
    
    # 발견 요약
    summary_verdict = ""
    if overall_similarity >= 80:
        summary_verdict = f"{p['name']}과 박씨는 철학적 프로필이 **매우 유사**합니다."
    elif overall_similarity >= 60:
        summary_verdict = f"{p['name']}과 박씨는 일부 축에서 유사하나, 결정적 차이가 있습니다."
    elif overall_similarity >= 40:
        summary_verdict = f"{p['name']}과 박씨는 **기본 전제가 다릅니다**."
    else:
        summary_verdict = f"{p['name']}과 박씨는 **거의 반대편에 위치**합니다."
    
    # 결정적 차이 TOP 3
    decisive = sorted(comparisons.values(), key=lambda x: abs(x["diff"]), reverse=True)[:3]
    
    return {
        "philosopher": p["name"],
        "era": p["era"],
        "eco_volume": p["eco_volume"],
        "key_concepts": p["key_concepts"],
        "phi7_scores": scores,
        "phi7_comparison": comparisons,
        "summary": {
            "avg_philosopher": avg_p,
            "avg_parksy": avg_m,
            "overall_similarity": overall_similarity,
            "similar_axes": len(similarities),
            "different_axes": len(differences),
            "total_features_shared": sum(len(c["common_features"]) for c in comparisons.values()),
            "verdict": summary_verdict
        },
        "similarities": similarities,
        "differences": differences,
        "discoveries": discoveries,
        "decisive_differences": [
            {"axis": d["axis_name"], "diff": d["diff"]} for d in decisive
        ],
        "raw_verdict": (
            f"{p['name']} vs 박씨: "
            f"공유 특징 {sum(len(c['common_features']) for c in comparisons.values())}개, "
            f"유사도 {overall_similarity}%. "
            f"결정적 차이: {decisive[0]['axis_name']}({decisive[0]['diff']:+.0f})" if decisive else ""
        )
    }

def rank_by_similarity():
    """전체 철학자 유사도 순위"""
    results = []
    for key in PHILOSOPHERS:
        r = analyze_philosopher(key)
        if "error" not in r:
            results.append({
                "key": key,
                "name": r["philosopher"],
                "similarity": r["summary"]["overall_similarity"],
                "shared_features": r["summary"]["total_features_shared"],
                "verdict": r["summary"]["verdict"][:30],
                "decisive_diff": r["decisive_differences"][0]["axis"] if r["decisive_differences"] else "",
                "decisive_diff_score": r["decisive_differences"][0]["diff"] if r["decisive_differences"] else 0
            })
    results.sort(key=lambda x: -x["similarity"])
    return results

def get_identity_update(philosopher_key):
    """비교 결과 → ID-MANIFEST 업데이트 제안 생성"""
    r = analyze_philosopher(philosopher_key)
    if "error" in r:
        return r
    
    lines = []
    lines.append(f"## ID 반영: {r['philosopher']} 비교 ({datetime.now().strftime('%Y-%m-%d')})")
    lines.append("")
    lines.append(f"종합 유사도: {r['summary']['overall_similarity']}%")
    lines.append(f"공유 특징: {r['summary']['total_features_shared']}개")
    lines.append("")
    
    if r["discoveries"]:
        lines.append("### 발견된 차이점")
        for d in r["discoveries"]:
            lines.append(f"- {d}")
    
    lines.append("")
    decisive = r["decisive_differences"]
    if decisive:
        lines.append("### 결정적 다른 점")
        for d in decisive[:3]:
            lines.append(f"- {d['axis']}: 차이 {d['diff']:+.0f}")
    
    lines.append("")
    lines.append("### ID 반영 제안")
    if r["similarities"]:
        sim_axes = [s["dimension"] for s in r["similarities"]]
        lines.append(f"- [유지/강화] {', '.join(sim_axes)}에서 박씨와 {r['philosopher']}의 접점 확인됨")
    if r["differences"]:
        diff_axes = [d["dimension"] for d in r["differences"]]
        lines.append(f"- [차별화] {', '.join(diff_axes)}는 박씨만의 고유 영역")
    
    return {
        "philosopher": r["philosopher"],
        "id_update": "\n".join(lines),
        "discoveries": r["discoveries"]
    }

def generate_counter_md(philosopher_key):
    """카운터 마크다운 생성"""
    r = analyze_philosopher(philosopher_key)
    if "error" in r:
        return r
    
    lines = []
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## {r['philosopher']} — Φ7 동적 분석")
    lines.append(f"")
    lines.append(f"### {r['summary']['verdict']}")
    lines.append(f"")
    lines.append(f"| 차원 | {r['philosopher']} | 박씨 | 차이 | 판정 |")
    lines.append(f"|------|:-:|:-:|:-:|------|")
    
    for c in r["phi7_comparison"].values():
        diff_str = f"{c['diff']:+.0f}"
        lines.append(f"| {c['axis_name']} | {c['philosopher_score']} | {c['parksy_score']} | {diff_str} | {c['verdict']} |")
    
    lines.append(f"")
    lines.append(f"**종합:** {r['raw_verdict']}")
    lines.append(f"")
    
    if r["discoveries"]:
        lines.append(f"**발견:**")
        for d in r["discoveries"]:
            lines.append(f"- {d}")
    
    return {
        "philosopher": r["philosopher"],
        "markdown": "\n".join(lines),
        "ready_to_commit": True
    }

if __name__ == "__main__":
    if "--analyze" in sys.argv and len(sys.argv) >= 3:
        i = sys.argv.index("--analyze")
        print(json.dumps(analyze_philosopher(sys.argv[i+1]), ensure_ascii=False, indent=2))
    elif "--rank" in sys.argv:
        results = rank_by_similarity()
        print(f"\n{'순위':<4} {'철학자':<16} {'유사도':<8} {'공유특징':<8} {'결정적 차이':<20}")
        print("-" * 60)
        for r in results:
            print(f"{r['key']:<4} {r['name']:<16} {r['similarity']:<8} {r['shared_features']:<8} {r['decisive_diff']}")
    elif "--id" in sys.argv and len(sys.argv) >= 3:
        i = sys.argv.index("--id")
        r = get_identity_update(sys.argv[i+1])
        print(r["id_update"])
    elif "--discover" in sys.argv:
        results = rank_by_similarity()
        print("=== Φ7 철학적 발견 ===")
        for r in results[:5]:
            rr = analyze_philosopher(r["key"])
            if rr["discoveries"]:
                print(f"\n[{r['name']}]")
                for d in rr["discoveries"]:
                    print(f"  {d}")
    else:
        print("--analyze <philosopher> | --rank | --id <philosopher> | --discover")
        print(f"철학자: {list_philosophers()}")
