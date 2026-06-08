#!/usr/bin/env python3
"""
server.py — Φ7 철학 카운터 MCP

에코 3부작(라 필로소피아)을 마스터 테이블로 삼아,
철학자 1명과 박씨 철학을 Φ7 5축으로 비교해서 리포트를 뽑는다.

툴:
  1. phi7_compare   — 철학자 1명 Φ7 5축 비교
  2. identity_diff  — 비교 결과 → ID-MANIFEST 반영안
  3. counter_md     — 전체 결과 → counter.md 자동 생성
  4. rank           — 가장 비슷한 철학자 순위
"""
import sys, json, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from phi7_engine import compare_phi7, batch_compare, find_most_similar, PARKSY_PHI7
from philosopher_data import PHILOSOPHERS, PHI7_AXES, list_philosophers

VERSION = "0.1.0"
MCP_NAME = "phi7_philosophy_counter"

# --- 툴 4개 ---

def tool_phi7_compare(philosopher_key):
    """툴 1: 철학자 1명 Φ7 5축 비교"""
    result = compare_phi7(philosopher_key)
    if "error" in result:
        return result
    return {
        "tool": "phi7_compare",
        "version": VERSION,
        "result": result
    }

def tool_identity_diff(philosopher_key):
    """툴 2: 비교 결과 → ID-MANIFEST 업데이트 제안"""
    result = compare_phi7(philosopher_key)
    if "error" in result:
        return result
    
    p_name = result["philosopher"]
    diffs = result["differences"]
    sims = result["similarities"]
    
    id_updates = []
    id_updates.append(f"### {p_name} 비교 — ID 반영안\n")
    id_updates.append(f"**날짜:** {datetime.now().strftime('%Y-%m-%d')}\n")
    
    if sims:
        id_updates.append("\n[확인/강화]")
        for s in sims[:3]:
            id_updates.append(f"- {s.strip()}")
    
    if diffs:
        id_updates.append("\n[차이 인지]")
        for d in diffs[:3]:
            id_updates.append(f"- {d.strip()}")
    
    id_updates.append(f"\n[메모]\n{result.get('notes', '')}")
    
    return {
        "tool": "identity_diff",
        "version": VERSION,
        "philosopher": p_name,
        "id_update_suggestion": "\n".join(id_updates),
        "current_id_lines": [
            f"비교 대상: {p_name}",
            f"닮은 축: {len(sims)}개",
            f"다른 축: {len(diffs)}개",
            f"반영 우선순위: {'높음' if len(diffs) > 2 else '중간' if len(diffs) > 0 else '낮음'}"
        ]
    }

def tool_counter_md(philosopher_key):
    """툴 3: 카운터 마크다운 생성 (chan-dae-counter.md 포맷)"""
    result = compare_phi7(philosopher_key)
    if "error" in result:
        return result
    
    p = result["philosopher"]
    comp = result["phi7_comparison"]
    
    lines = []
    lines.append(f"\n---\n")
    lines.append(f"## 2026-06-08 #{'0' + str(len(PHILOSOPHERS))[:2]} — {p} Φ7 비교")
    lines.append(f"\n### Φ7 5축 비교: 박씨 vs {p}\n")
    
    for ax_key, ax_data in comp.items():
        lines.append(f"**[{ax_data['axis_name']}]**")
        lines.append(f"- {p}: {ax_data['philosopher_score']}/100")
        lines.append(f"- 박씨: {ax_data['parksy_score']}/100")
        lines.append(f"- 차이: {ax_data['diff']:+.1f}")
        lines.append(f"- 판정: {ax_data['verdict']}")
        lines.append("")
    
    lines.append("### 종합\n")
    lines.append(f"- 닮은 축: {result['summary']['total_similar_axes']}개")
    lines.append(f"- 다른 축: {result['summary']['total_different_axes']}개")
    lines.append(f"- 메모: {result['notes']}")
    lines.append("")
    
    return {
        "tool": "counter_md",
        "version": VERSION,
        "philosopher": p,
        "markdown": "\n".join(lines),
        "ready_to_commit": True,
        "target_file": "dtslib-branch/비즈니스-소설/chan-dae-counter.md"
    }

def tool_rank():
    """툴 4: 유사도 순위"""
    rankings = find_most_similar()
    result = []
    for i, (diff, key, name) in enumerate(rankings, 1):
        result.append({
            "rank": i,
            "philosopher": name,
            "similarity_score": round(100 - diff, 1),
            "assessment": "매우 유사" if diff < 10 else "유사" if diff < 20 else "차이 있음" if diff < 35 else "매우 다름"
        })
    return {
        "tool": "rank",
        "version": VERSION,
        "ranking": result,
        "note": "점수가 높을수록 박씨 철학과 비슷함"
    }

# --- MCP 서버 ---

WELCOME = f"""
╔══════════════════════════════════════════════╗
║  {MCP_NAME} v{VERSION}                       ║
║  Φ7 철학 카운터 — ID 엔진 튜닝 시리즈      ║
║  에코 3부작을 마스터 테이블로              ║
╚══════════════════════════════════════════════╝

툴:
  phi7_compare — 철학자 1명 Φ7 5축 비교
  identity_diff — ID-MANIFEST 반영안 생성
  counter_md   — chan-dae-counter.md 포맷 출력
  rank         — 가장 비슷한 철학자 순위

사용법:
  echo '{{"tool":"phi7_compare","params":{{"philosopher":"gattari"}}}}' | python3 server.py

철학자 목록:
  {', '.join(list_philosophers())}
"""

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(WELCOME)
        return
    
    req = json.loads(raw)
    tool = req.get("tool", "")
    params = req.get("params", {})
    
    if tool == "phi7_compare":
        r = tool_phi7_compare(params.get("philosopher", ""))
        print(json.dumps(r, ensure_ascii=False, indent=2))
    
    elif tool == "identity_diff":
        r = tool_identity_diff(params.get("philosopher", ""))
        print(json.dumps(r, ensure_ascii=False, indent=2))
    
    elif tool == "counter_md":
        r = tool_counter_md(params.get("philosopher", ""))
        print(json.dumps(r, ensure_ascii=False, indent=2))
    
    elif tool == "rank":
        r = tool_rank()
        print(json.dumps(r, ensure_ascii=False, indent=2))
    
    else:
        print(json.dumps({
            "tools": ["phi7_compare", "identity_diff", "counter_md", "rank"],
            "available_philosophers": list_philosophers(),
            "version": VERSION
        }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
