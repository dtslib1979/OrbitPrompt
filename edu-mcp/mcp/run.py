#!/usr/bin/env python3
"""실행 진입점 — python3 run.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from server import handle

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        r = handle(json.loads(line))
        print(json.dumps(r, ensure_ascii=False))
        sys.stdout.flush()
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.stdout.flush()
