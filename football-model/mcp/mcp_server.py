#!/usr/bin/env python3
"""
football-mcp-server.py — Φ-I-C-K-P 축구 예측 MCP 서버
API: /predict, /strength, /montecarlo, /matchup
"""
import sys, json, os, asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from simulation import win_prob, predict_match, monte_carlo
from team_data import TEAMS, all_strengths, calc_strength

try:
    from mcp import Server, Tool
    from mcp.server.stdio import stdio_server
    MCP_MODE = True
except:
    MCP_MODE = False

async def main():
    if not MCP_MODE:
        # FastAPI 모드
        print("⚽ Φ-I-C-K-P 축구 예측 MCP 서버")
        import uvicorn
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(title="Football MCP")
        app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
        
        @app.get("/predict")
        async def api_predict(t1: str = "Brazil", t2: str = "France"):
            return predict_match(t1, t2)
        
        @app.get("/strength")
        async def api_strength():
            s = all_strengths()
            ranked = sorted(s.items(), key=lambda x: -x[1])
            return {"teams": [{"name": n, "strength": v} for n, v in ranked]}
        
        @app.get("/team")
        async def api_team(name: str = "Brazil"):
            if name in TEAMS:
                return {"name": name, **TEAMS[name], "strength": calc_strength(name)}
            return {"error": "team not found"}
        
        @app.get("/montecarlo")
        async def api_mc(n: int = 1000):
            result = monte_carlo(n)
            return result
        
        port = int(os.environ.get("PORT", "8100"))
        print(f"  포트: {port}")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    else:
        print("⚽ MCP stdio 모드")
        server = Server("football-mcp")
        # (MCP tools would go here)
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
