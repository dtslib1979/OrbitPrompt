#!/usr/bin/env python3
"""달러 시스템 MCP — 환율/구조/권력 분석"""
import sys, json
sys.path.insert(0, __file__)
from dollar_engine import handle

VERSION = "0.1.0"
WELCOME = "달러 시스템 MCP — 환율 넣으면 구조 분석 리포트 출력"

for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            req = json.loads(line)
            r = handle(req)
            r["_meta"] = {"version": VERSION}
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
