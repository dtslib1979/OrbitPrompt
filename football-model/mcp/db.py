#!/usr/bin/env python3
"""
db.py — SQLite 누적 저장소
시뮬레이션 돌릴수록 쌓이고, 예측 정확도 올라가는 구조
"""
import sqlite3, json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "football.db"

def conn():
    return sqlite3.connect(DB_PATH)

def init():
    c = conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS teams (
        name        TEXT PRIMARY KEY,
        fifa_rank   INTEGER,
        fifa_points REAL,
        elo         REAL,
        wins        INTEGER DEFAULT 0,
        draws       INTEGER DEFAULT 0,
        losses      INTEGER DEFAULT 0,
        goals_for   INTEGER DEFAULT 0,
        goals_against INTEGER DEFAULT 0,
        matches_played INTEGER DEFAULT 0,
        updated     TEXT
    );

    CREATE TABLE IF NOT EXISTS matches (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date        TEXT,
        home_team   TEXT,
        away_team   TEXT,
        home_score  INTEGER,
        away_score  INTEGER,
        tournament  TEXT,
        neutral     INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS simulation_runs (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        run_time    TEXT,
        n           INTEGER,
        results     TEXT
    );

    CREATE TABLE IF NOT EXISTS predictions (
        team        TEXT PRIMARY KEY,
        win_pct     REAL DEFAULT 0,
        final_pct   REAL DEFAULT 0,
        sf_pct      REAL DEFAULT 0,
        qf_pct      REAL DEFAULT 0,
        r32_pct     REAL DEFAULT 0,
        total_runs  INTEGER DEFAULT 0,
        updated     TEXT
    );
    """)
    c.commit()
    c.close()

def upsert_team(name, fifa_rank, fifa_points, elo):
    c = conn()
    c.execute("""
        INSERT INTO teams (name, fifa_rank, fifa_points, elo, updated)
        VALUES (?,?,?,?,?)
        ON CONFLICT(name) DO UPDATE SET
            fifa_rank=excluded.fifa_rank,
            fifa_points=excluded.fifa_points,
            elo=excluded.elo,
            updated=excluded.updated
    """, (name, fifa_rank, fifa_points, elo, datetime.now().isoformat()))
    c.commit(); c.close()

def bulk_upsert_match_stats(stats: dict):
    """stats: {team: {wins, draws, losses, gf, ga, played}}"""
    c = conn()
    for name, s in stats.items():
        c.execute("""
            UPDATE teams SET wins=?, draws=?, losses=?, goals_for=?,
                goals_against=?, matches_played=?, updated=?
            WHERE name=?
        """, (s['wins'], s['draws'], s['losses'], s['gf'], s['ga'],
              s['played'], datetime.now().isoformat(), name))
    c.commit(); c.close()

def insert_matches(rows: list):
    """rows: list of (date, home, away, hs, as, tournament, neutral)"""
    c = conn()
    c.execute("DELETE FROM matches")
    c.executemany("""
        INSERT OR IGNORE INTO matches
        (date, home_team, away_team, home_score, away_score, tournament, neutral)
        VALUES (?,?,?,?,?,?,?)
    """, rows)
    c.commit(); c.close()

def save_simulation(n: int, results: dict):
    c = conn()
    c.execute("INSERT INTO simulation_runs (run_time, n, results) VALUES (?,?,?)",
              (datetime.now().isoformat(), n, json.dumps(results, ensure_ascii=False)))
    # 누적 예측 업데이트
    for team, s in results.items():
        c.execute("""
            INSERT INTO predictions (team, win_pct, final_pct, sf_pct, qf_pct, r32_pct, total_runs, updated)
            VALUES (?,?,?,?,?,?,?,?)
            ON CONFLICT(team) DO UPDATE SET
                win_pct   = (win_pct   * total_runs + excluded.win_pct   * excluded.total_runs) / (total_runs + excluded.total_runs),
                final_pct = (final_pct * total_runs + excluded.final_pct * excluded.total_runs) / (total_runs + excluded.total_runs),
                sf_pct    = (sf_pct    * total_runs + excluded.sf_pct    * excluded.total_runs) / (total_runs + excluded.total_runs),
                qf_pct    = (qf_pct    * total_runs + excluded.qf_pct    * excluded.total_runs) / (total_runs + excluded.total_runs),
                r32_pct   = (r32_pct   * total_runs + excluded.r32_pct   * excluded.total_runs) / (total_runs + excluded.total_runs),
                total_runs = total_runs + excluded.total_runs,
                updated   = excluded.updated
        """, (team, s.get('win',0), s.get('final',0), s.get('sf',0),
              s.get('qf',0), s.get('r32',0), n, datetime.now().isoformat()))
    c.commit(); c.close()

def get_predictions(top=20):
    c = conn()
    rows = c.execute("""
        SELECT team, win_pct, final_pct, sf_pct, qf_pct, r32_pct, total_runs, updated
        FROM predictions ORDER BY win_pct DESC LIMIT ?
    """, (top,)).fetchall()
    c.close()
    return [{"team":r[0],"win":r[1],"final":r[2],"sf":r[3],"qf":r[4],"r32":r[5],
             "total_runs":r[6],"updated":r[7]} for r in rows]

def get_team(name):
    c = conn()
    row = c.execute("SELECT * FROM teams WHERE name=?", (name,)).fetchone()
    c.close()
    if not row: return None
    cols = ["name","fifa_rank","fifa_points","elo","wins","draws","losses",
            "goals_for","goals_against","matches_played","updated"]
    return dict(zip(cols, row))

def get_all_teams():
    c = conn()
    rows = c.execute("SELECT name, fifa_rank, fifa_points, elo, wins, draws, losses, goals_for, goals_against, matches_played FROM teams").fetchall()
    c.close()
    return {r[0]: {"fifa_rank":r[1],"fifa_points":r[2],"elo":r[3],
                   "wins":r[4],"draws":r[5],"losses":r[6],
                   "gf":r[7],"ga":r[8],"played":r[9]} for r in rows}

def get_run_count():
    c = conn()
    row = c.execute("SELECT COALESCE(SUM(n),0) FROM simulation_runs").fetchone()
    c.close()
    return row[0]

if __name__ == "__main__":
    init()
    print("✅ DB 초기화 완료:", DB_PATH)
