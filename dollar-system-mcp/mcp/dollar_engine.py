#!/usr/bin/env python3
"""달러 시스템 분석 엔진 — 환율/구조/권력 해석"""
import sys, json, math

# Φ7 7축
PHI7 = {
    "zoom": {"name": "🔍 Zoom", "desc": "개인→국가→글로벌 스케일 전환"},
    "reverse": {"name": "🔄 Reverse", "desc": "가격이 먼저, 정당화는 나중"},
    "language": {"name": "💬 Language", "desc": "금융 언어의 해석권 독점"},
    "meta": {"name": "🧠 Meta", "desc": "시스템 전체를 보는 눈"},
    "modular": {"name": "🧩 Modular", "desc": "땜빵과 패치의 누적"},
    "spiral": {"name": "📈 Spiral", "desc": "반복되는 위기와 구조 재생산"},
    "quantum": {"name": "⚡ Quantum", "desc": "체제 이탈과 대안의 등장"}
}

def analyze_rate(rate):
    """환율 입력 → 구조 분석 리포트"""
    rate = float(rate)
    burden = "높음" if rate > 1350 else "중간" if rate > 1250 else "낮음"
    return {
        "rate": rate,
        "burden_level": burden,
        "interpretation": f"원·달러 {rate}원 = 한국에 적용된 현재 요율",
        "structural_view": "판은 기울어져 있고, 한국의 내부 약점은 그 기울기 위에서 미끄러지는 속도를 더 빠르게 만든다",
        "phi7_mapping": {
            "zoom": f"개인(환전) → 기업(수입물가) → 국가(외채)로 이어지는 {rate}원의 스케일",
            "reverse": f"{rate}원은 실력이 아니라 구조적 전가의 결과",
            "language": f"{rate}원을 설명하는 언어는 누가 해석권을 쥐고 있느냐에 따라 달라진다"
        }
    }

def structure_critique():
    """시스템 진단"""
    return {
        "thesis": "달러 시스템은 설계가 아니라 누적된 땜빵이다",
        "history": [
            {"event": "브레턴우즈 (1944)", "type": "설계"},
            {"event": "닉슨쇼크 (1971)", "type": "버그"},
            {"event": "페트로달러 (1970s)", "type": "워크어라운드"},
            {"event": "QE × n (2008-2020)", "type": "패치"},
            {"event": "제재 무기화 (2022-)", "type": "추가 패치"}
        ],
        "conclusion": "버그가 스펙이 된 상태. '이게 원래 스펙입니다' 문서화."
    }

def handle(req):
    tool = req.get("tool", "")
    p = req.get("params", {})
    if tool == "analyze":
        return {"tool": "analyze", "result": analyze_rate(p.get("rate", 1400))}
    elif tool == "structure":
        return {"tool": "structure", "result": structure_critique()}
    elif tool == "phi7_map":
        return {"tool": "phi7_map", "phi7": PHI7,
                "mapping": {
                    "zoom": "백서 전체 = 개인→국가→글로벌 스케일",
                    "reverse": "사후 정당화 기계 해부",
                    "language": "금융 언어 독점과 해석권",
                    "meta": "달러 체제 전체 구조",
                    "modular": "땜빵과 패치의 역사",
                    "spiral": "위기→패치→재생산 반복",
                    "quantum": "탈달러·블록경제·코인 체제"
                }}
    else:
        return {"tools": ["analyze", "structure", "phi7_map"],
                "rate_example": '{"tool":"analyze","params":{"rate":"1400"}}'}

for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            r = handle(json.loads(line))
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
