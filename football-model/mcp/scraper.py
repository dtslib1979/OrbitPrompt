#!/usr/bin/env python3
"""
scraper.py — 실제 raw 데이터 수집
소스 1: Wikipedia → FIFA 랭킹 + 포인트 (월별 업데이트)
소스 2: github.com/martj42/international_results → 1872-현재 전체 국제경기 결과 CSV
"""
import requests, csv, io, re, sys
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path

# WC2026 본선 진출 48팀 (확정 + 예상)
WC26_TEAMS = {
    # UEFA (16)
    "Germany", "France", "Spain", "England", "Portugal", "Netherlands",
    "Belgium", "Croatia", "Switzerland", "Austria", "Serbia", "Scotland",
    "Turkey", "Hungary", "Denmark", "Czech Republic",
    # CONMEBOL (6)
    "Argentina", "Brazil", "Uruguay", "Colombia", "Ecuador", "Bolivia",
    # CONCACAF (6)
    "USA", "Mexico", "Canada", "Panama", "Jamaica", "Honduras",
    # CAF (9)
    "Morocco", "Senegal", "Egypt", "Nigeria", "Cameroon",
    "Ivory Coast", "South Africa", "DR Congo", "Tunisia",
    # AFC (8)
    "Japan", "South Korea", "Iran", "Saudi Arabia",
    "Australia", "Uzbekistan", "Qatar", "Jordan",
    # OFC (1)
    "New Zealand",
    # 플레이오프 예상
    "Ukraine", "Greece",
}

# Wikipedia 팀명 → WC26 팀명 매핑
WIKI_NAME_MAP = {
    "United States": "USA",
    "Republic of Korea": "South Korea",
    "Korea Republic": "South Korea",
    "Türkiye": "Turkey",
    "Côte d'Ivoire": "Ivory Coast",
    "Republic of Ireland": "Ireland",
    "Czech Republic": "Czech Republic",
    "Bosnia and Herzegovina": "Bosnia",
    "Democratic Republic of the Congo": "DR Congo",
    "Congo DR": "DR Congo",
}

# martj42 데이터셋 팀명 → WC26 팀명 매핑
CSV_NAME_MAP = {
    "United States": "USA",
    "South Korea": "South Korea",
    "Republic of Korea": "South Korea",
    "Korea Republic": "South Korea",
    "Ivory Coast": "Ivory Coast",
    "Cote d'Ivoire": "Ivory Coast",
    "DR Congo": "DR Congo",
    "Congo DR": "DR Congo",
    "Democratic Republic of the Congo": "DR Congo",
    "Turkey": "Turkey",
    "Türkiye": "Turkey",
    "Czech Republic": "Czech Republic",
}

def normalize(name: str) -> str:
    return WIKI_NAME_MAP.get(name, CSV_NAME_MAP.get(name, name))


def fetch_fifa_rankings() -> dict:
    """Wikipedia에서 FIFA 랭킹 + 포인트 스크래핑 (실시간)"""
    print("  📡 FIFA 랭킹 수집 중 (Wikipedia)...", file=sys.stderr)
    url = "https://en.wikipedia.org/wiki/FIFA_World_Rankings"
    r = requests.get(url, timeout=15,
                     headers={"User-Agent": "Mozilla/5.0 (football-model research)"})
    soup = BeautifulSoup(r.text, "html.parser")

    rankings = {}
    for table in soup.find_all("table", class_="wikitable"):
        rows = table.find_all("tr")
        for row in rows[2:]:  # skip 2 header rows
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cells) < 4:
                continue
            rank_str  = re.sub(r'\D', '', cells[0])
            team_name = cells[2] if len(cells) > 2 else cells[1]
            pts_str   = re.sub(r'[^\d.]', '', cells[-1])
            if not rank_str or not pts_str:
                continue
            try:
                rank   = int(rank_str)
                points = float(pts_str)
                name   = normalize(team_name)
                rankings[name] = {"rank": rank, "points": points}
            except ValueError:
                continue
        if rankings:
            break  # 첫 유효 테이블만

    print(f"  ✅ FIFA 랭킹 {len(rankings)}개국 수집", file=sys.stderr)
    return rankings


def fetch_match_results(years: int = 5) -> list:
    """
    GitHub martj42/international_results에서 최근 N년 국제경기 결과 CSV 다운로드
    반환: list of (date, home, away, home_score, away_score, tournament, neutral)
    """
    print(f"  📡 국제경기 결과 {years}년치 수집 중 (GitHub)...", file=sys.stderr)
    url = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
    r = requests.get(url, timeout=30,
                     headers={"User-Agent": "Mozilla/5.0 (football-model research)"})
    cutoff = (datetime.now() - timedelta(days=365 * years)).strftime("%Y-%m-%d")

    rows = []
    reader = csv.DictReader(io.StringIO(r.text))
    for row in reader:
        if row["date"] < cutoff:
            continue
        home = normalize(row["home_team"])
        away = normalize(row["away_team"])
        try:
            hs = int(row["home_score"])
            as_ = int(row["away_score"])
        except (ValueError, KeyError):
            continue
        neutral = 1 if row.get("neutral", "FALSE").upper() == "TRUE" else 0
        rows.append((row["date"], home, away, hs, as_, row.get("tournament",""), neutral))

    print(f"  ✅ 경기 결과 {len(rows)}건 수집 (최근 {years}년)", file=sys.stderr)
    return rows


def calc_team_stats(match_rows: list, teams: set) -> dict:
    """
    경기 결과로 팀별 W/D/L/GF/GA 집계
    WC26 팀만 필터
    """
    stats = {t: {"wins":0,"draws":0,"losses":0,"gf":0,"ga":0,"played":0} for t in teams}

    for (date, home, away, hs, as_, tourn, neutral) in match_rows:
        for team, opp, gs, gc in [(home, away, hs, as_), (away, home, as_, hs)]:
            if team not in stats:
                continue
            stats[team]["played"] += 1
            stats[team]["gf"] += gs
            stats[team]["ga"] += gc
            if gs > gc:
                stats[team]["wins"] += 1
            elif gs == gc:
                stats[team]["draws"] += 1
            else:
                stats[team]["losses"] += 1

    return stats


def calc_elo_from_results(match_rows: list, teams: set, base_elo: float = 1500) -> dict:
    """
    실제 경기 결과로 ELO 레이팅 계산 (K=32)
    초기값 1500에서 시작, 경기마다 업데이트
    """
    elo = {t: base_elo for t in teams}
    K = 32

    for (date, home, away, hs, as_, tourn, neutral) in sorted(match_rows, key=lambda x: x[0]):
        if home not in elo or away not in elo:
            continue
        e_h = 1.0 / (1.0 + 10 ** ((elo[away] - elo[home]) / 400))
        e_a = 1.0 - e_h
        if hs > as_:
            s_h, s_a = 1.0, 0.0
        elif hs == as_:
            s_h, s_a = 0.5, 0.5
        else:
            s_h, s_a = 0.0, 1.0
        elo[home] += K * (s_h - e_h)
        elo[away] += K * (s_a - e_a)

    return {t: round(elo[t], 1) for t in elo}


def fetch_all(years: int = 5) -> dict:
    """
    전체 수집 파이프라인
    반환: {
        "rankings": {team: {rank, points}},
        "matches":  [(date, home, away, hs, as, tourn, neutral), ...],
        "stats":    {team: {wins, draws, losses, gf, ga, played}},
        "elo":      {team: elo_rating},
        "fetched":  ISO timestamp
    }
    """
    rankings = fetch_fifa_rankings()
    matches  = fetch_match_results(years)
    stats    = calc_team_stats(matches, WC26_TEAMS)
    elo      = calc_elo_from_results(matches, WC26_TEAMS)

    return {
        "rankings": rankings,
        "matches":  matches,
        "stats":    stats,
        "elo":      elo,
        "fetched":  datetime.now().isoformat(),
    }


if __name__ == "__main__":
    data = fetch_all(years=3)
    print(f"\n📊 수집 완료")
    print(f"  FIFA 랭킹: {len(data['rankings'])}개국")
    print(f"  경기 결과: {len(data['matches'])}건")
    print(f"\n상위 10개국 ELO:")
    for t, e in sorted(data['elo'].items(), key=lambda x:-x[1])[:10]:
        r = data['rankings'].get(t, {}).get('rank', '?')
        s = data['stats'].get(t, {})
        print(f"  {t:20s} ELO:{e:6.0f}  FIFA:{r:3}  "
              f"W{s.get('wins',0)}-D{s.get('draws',0)}-L{s.get('losses',0)}")
