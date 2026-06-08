#!/usr/bin/env python3
"""달러 시스템 MCP v2.0 — 환율/구조/권력/역사 분석 + 예측 모델"""
import sys, json, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dollar_engine import analyze_rate, structure_critique, phi7_map, timeline, compare_rates, drivers, predict, calc_dsi

VERSION = "2.1.0"
TOOLS = ["analyze", "structure", "phi7_map", "timeline", "compare", "drivers", "predict", "calc_dsi", "version"]

def handle(req):
    tool = req.get("tool", "")
    p = req.get("params", {})

    if tool == "analyze":
        return {"tool": "analyze", "result": analyze_rate(float(p.get("rate", 1400)))}
    elif tool == "structure":
        return {"tool": "structure", "result": structure_critique()}
    elif tool == "phi7_map":
        return {"tool": "phi7_map", "result": phi7_map()}
    elif tool == "timeline":
        return {"tool": "timeline", "result": timeline()}
    elif tool == "compare":
        r1 = float(p.get("rate1", 1200))
        r2 = float(p.get("rate2", 1400))
        return {"tool": "compare", "result": compare_rates(r1, r2)}
    elif tool == "drivers":
        return {"tool": "drivers", "result": drivers()}
    elif tool == "predict":
        days = int(p.get("days", 30))
        return {"tool": "predict", "result": predict(days)}
    elif tool == "calc_dsi":
        return {"tool": "calc_dsi", "result": calc_dsi()}
    elif tool == "version":
        return {
            "name": "달러 시스템 MCP",
            "version": VERSION,
            "tools": TOOLS,
            "desc": "달러 패권 구조를 Φ7 7축으로 해석 + yfinance 실시간 예측 + DSI 스트레스 지수"
        }
    else:
        return {
            "error": f"unknown tool '{tool}'",
            "tools": TOOLS
        }

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            r = handle(req)
            r["_meta"] = {"version": VERSION}
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"JSON parse error: {e}"}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
