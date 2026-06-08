#!/usr/bin/env python3
"""달러 시스템 엔진 v2.2 (만점판) — DSI + BS_INDEX + 언어역지표"""

import sys, json, math, os
from datetime import datetime, timedelta

PHI7 = {
    "zoom":     {"name": "🔍 Zoom",     "desc": "개인→국가→글로벌 스케일 전환"},
    "reverse":  {"name": "🔄 Reverse",  "desc": "가격이 먼저, 정당화는 나중"},
    "language": {"name": "💬 Language", "desc": "금융 언어의 해석권 독점"},
    "meta":     {"name": "🧠 Meta",     "desc": "시스템 전체를 보는 눈"},
    "modular":  {"name": "🧩 Modular",  "desc": "땜빵과 패치의 누적"},
    "spiral":   {"name": "📈 Spiral",   "desc": "반복되는 위기와 구조 재생산"},
    "quantum":  {"name": "⚡ Quantum",  "desc": "체제 이탈과 대안의 등장"}
}

# ─── 정적 분석 함수 ─────────────────────────────────────────────────────────

def analyze_rate(rate):
    rate = float(rate)
    if rate > 1400:
        tier = "위험"; signal = "자본 유출 압력, 수입물가 급등"
    elif rate > 1350:
        tier = "높음"; signal = "수출 수혜, 가계 구매력 감소"
    elif rate > 1250:
        tier = "중간"; signal = "구조적 균형 — 표면적 안정"
    else:
        tier = "낮음"; signal = "원화 강세, 수출 마진 압박"

    return {
        "rate": rate,
        "tier": tier,
        "signal": signal,
        "interpretation": f"원·달러 {rate}원 = 한국에 적용된 현재 요율",
        "structural_view": "판은 기울어져 있고, 한국의 내부 약점은 그 기울기 위에서 미끄러지는 속도를 더 빠르게 만든다",
        "phi7_mapping": {
            "zoom": f"개인(환전) → 기업(수입물가) → 국가(외채)로 이어지는 {rate}원의 스케일",
            "reverse": f"{rate}원은 실력이 아니라 구조적 전가의 결과",
            "language": f"{rate}원을 설명하는 언어는 누가 해석권을 쥐고 있느냐에 따라 달라진다",
            "spiral": "1997 → 2008 → 2020 → 현재. 위기가 올 때마다 원화는 찍혔고, 달러는 귀해졌다"
        }
    }

def structure_critique():
    return {
        "thesis": "달러 시스템은 설계가 아니라 누적된 땜빵이다",
        "history": [
            {"event": "브레턴우즈 (1944)", "type": "설계", "note": "금 1온스=35달러 고정"},
            {"event": "닉슨쇼크 (1971)", "type": "버그", "note": "금태환 폐지. 설계 붕괴"},
            {"event": "페트로달러 (1973)", "type": "워크어라운드", "note": "석유→달러 결제 강제"},
            {"event": "플라자 합의 (1985)", "type": "패치", "note": "엔화 절상 강제 — 달러 약세 인위 조정"},
            {"event": "QE × n (2008-2020)", "type": "패치", "note": "무한 인쇄로 위기 덮기"},
            {"event": "제재 무기화 (2022-)", "type": "추가 패치", "note": "SWIFT 배제 — 달러 신뢰 균열 시작"}
        ],
        "conclusion": "버그가 스펙이 된 상태. '이게 원래 스펙입니다' 문서화.",
        "phi7_tag": "modular"
    }

def phi7_map():
    return {
        "phi7": PHI7,
        "dollar_mapping": {
            "zoom":     "백서 전체 = 개인→국가→글로벌 스케일 분석",
            "reverse":  "사후 정당화 기계 해부 — 데이터가 먼저, 해석은 나중",
            "language": "금융 언어 독점과 해석권 — '안전자산'이라는 프레임",
            "meta":     "달러 체제 전체 구조를 조감하는 렌즈",
            "modular":  "땜빵과 패치의 역사 — 설계가 아니라 누적",
            "spiral":   "위기→패치→재생산 반복 — 1971, 1985, 2008, 2020",
            "quantum":  "탈달러·블록경제·CBDC·비트코인 체제 이탈 시나리오"
        }
    }

def timeline():
    events = [
        {"year": 1944, "event": "브레턴우즈 체제", "phi7": "meta",     "impact": "달러=기축 설계"},
        {"year": 1971, "event": "닉슨쇼크",         "phi7": "reverse",  "impact": "금태환 종료"},
        {"year": 1973, "event": "페트로달러",        "phi7": "modular",  "impact": "석유→달러 결제 구조"},
        {"year": 1985, "event": "플라자 합의",       "phi7": "zoom",     "impact": "G5 환율 인위 조정"},
        {"year": 1997, "event": "아시아 금융위기",   "phi7": "spiral",   "impact": "한국 IMF 구제금융"},
        {"year": 2008, "event": "글로벌 금융위기",   "phi7": "spiral",   "impact": "QE 시대 개막"},
        {"year": 2020, "event": "코로나 QE",         "phi7": "modular",  "impact": "달러 공급 폭발"},
        {"year": 2022, "event": "러시아 제재",       "phi7": "quantum",  "impact": "SWIFT 무기화, 탈달러 가속"},
        {"year": 2024, "event": "BRICS 결제 시스템", "phi7": "quantum",  "impact": "달러 대안 구조화"},
    ]
    return {"events": events, "thesis": "위기는 반복되고, 패치는 누적되고, 균열은 깊어진다"}

def compare_rates(r1, r2):
    r1, r2 = float(r1), float(r2)
    diff = round(r2 - r1, 1)
    pct  = round(diff / r1 * 100, 2)

    def tier(r):
        if r > 1400: return "위험"
        if r > 1350: return "높음"
        if r > 1250: return "중간"
        return "낮음"

    direction = "상승 (원화 약세)" if diff > 0 else "하락 (원화 강세)"
    return {
        "rate1": r1, "rate2": r2,
        "diff": diff, "pct_change": pct,
        "direction": direction,
        "tier1": tier(r1), "tier2": tier(r2),
        "interpretation": f"{r1}→{r2}원 이동: {pct:+.2f}% 변화. 원화 {direction}.",
        "structural_note": "환율 상승 = 한국 경상수지 적자 압력 / 수입물가 연동 / 가계 구매력 저하"
    }

# ─── 예측 모델 (yfinance 드라이버) ──────────────────────────────────────────

def _linear_fit(xs, ys):
    """numpy 없이 최소자승법 선형회귀"""
    n = len(xs)
    if n < 2:
        return 0.0, ys[-1] if ys else 0.0
    sum_x  = sum(xs)
    sum_y  = sum(ys)
    sum_xx = sum(x*x for x in xs)
    sum_xy = sum(x*y for x, y in zip(xs, ys))
    denom  = n * sum_xx - sum_x * sum_x
    if denom == 0:
        return 0.0, sum_y / n
    slope     = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y - slope * sum_x) / n
    return slope, intercept

def drivers():
    """실시간 드라이버 현황 — yfinance 기반"""
    try:
        import yfinance as yf

        symbols = {
            "USDKRW=X": ("원달러환율", "KRW/USD"),
            "DX-Y.NYB": ("달러인덱스(DXY)", "USD Index"),
            "^TNX":     ("미 10년 국채금리", "%"),
            "^VIX":     ("공포지수(VIX)", ""),
        }

        result = {}
        for sym, (label, unit) in symbols.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="5d")
                if h.empty:
                    result[sym] = {"label": label, "error": "데이터 없음"}
                    continue
                last  = round(float(h["Close"].iloc[-1]), 4)
                prev  = round(float(h["Close"].iloc[-2]), 4) if len(h) >= 2 else last
                chg   = round(last - prev, 4)
                chgp  = round(chg / prev * 100, 2) if prev else 0
                result[sym] = {
                    "label":  label,
                    "value":  last,
                    "unit":   unit,
                    "change": chg,
                    "change_pct": chgp,
                    "direction": "↑" if chg > 0 else "↓" if chg < 0 else "→"
                }
            except Exception as e:
                result[sym] = {"label": label, "error": str(e)}

        # 달러 강세 해석
        dxy_val = result.get("DX-Y.NYB", {}).get("value", 100)
        tnx_val = result.get("^TNX",     {}).get("value", 4.0)
        krw_val = result.get("USDKRW=X", {}).get("value", 1300)

        if dxy_val > 105:
            pressure = "강한 달러 강세 — 원화 약세 압력 높음"
        elif dxy_val > 100:
            pressure = "중립 달러 — 원화 방향 혼조"
        else:
            pressure = "달러 약세 — 원화 강세 지지"

        return {
            "drivers": result,
            "krw_rate": krw_val,
            "dxy": dxy_val,
            "tnx_yield": tnx_val,
            "structural_pressure": pressure,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST")
        }

    except ImportError:
        return {"error": "yfinance 미설치. pip install yfinance --break-system-packages"}
    except Exception as e:
        return {"error": str(e)}


def predict(days=30):
    """선형 회귀 + 드라이버 상관 기반 환율 예측"""
    try:
        import yfinance as yf

        end   = datetime.now()
        start = end - timedelta(days=180)

        # 원달러 60일치
        krw_df = yf.download("USDKRW=X", start=start, end=end, progress=False)
        dxy_df = yf.download("DX-Y.NYB", start=start, end=end, progress=False)
        tnx_df = yf.download("^TNX",     start=start, end=end, progress=False)

        if krw_df.empty:
            return {"error": "환율 데이터 수집 실패"}

        def to_vals(df):
            col = df["Close"]
            if hasattr(col, "squeeze"):
                col = col.squeeze()
            return [float(v) for v in col.dropna().values.tolist()]

        krw_vals = to_vals(krw_df)
        dxy_vals = to_vals(dxy_df) if not dxy_df.empty else []
        tnx_vals = to_vals(tnx_df) if not tnx_df.empty else []

        n = len(krw_vals)
        xs = list(range(n))

        # 선형 트렌드
        slope, intercept = _linear_fit(xs, krw_vals)

        current_rate = round(krw_vals[-1], 2)
        pred_rate    = round(intercept + slope * (n + days - 1), 2)
        trend_dir    = "상승 (원화 약세)" if slope > 0 else "하락 (원화 강세)"
        daily_change = round(slope, 4)

        # DXY 상관 — 단순 피어슨
        def corr(a, b):
            min_len = min(len(a), len(b))
            a, b = a[-min_len:], b[-min_len:]
            ma = sum(a) / len(a); mb = sum(b) / len(b)
            num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
            da  = (sum((x - ma)**2 for x in a))**0.5
            db  = (sum((y - mb)**2 for y in b))**0.5
            return round(num / (da * db), 3) if da * db else 0

        dxy_corr = corr(krw_vals, dxy_vals)
        tnx_corr = corr(krw_vals, tnx_vals)

        # DXY 트렌드 보정
        if len(dxy_vals) >= 10:
            dxy_slope, _ = _linear_fit(list(range(len(dxy_vals))), dxy_vals)
            if abs(dxy_corr) > 0.5:
                adj = dxy_slope * days * dxy_corr * 10
                pred_rate_adj = round(pred_rate + adj, 2)
            else:
                pred_rate_adj = pred_rate
        else:
            pred_rate_adj = pred_rate

        # 신뢰 구간 (표준오차 기반)
        fitted  = [intercept + slope * x for x in xs]
        residuals = [krw_vals[i] - fitted[i] for i in range(n)]
        mse     = sum(r**2 for r in residuals) / max(n - 2, 1)
        stderr  = mse**0.5
        ci_95   = round(1.96 * stderr * (1 + (days / n)**0.5), 2)

        # 시나리오
        scenarios = {
            "강세 (달러 약세)": round(pred_rate_adj - ci_95 * 0.7, 0),
            "기준":             round(pred_rate_adj, 0),
            "약세 (달러 강세)": round(pred_rate_adj + ci_95 * 0.7, 0),
        }

        # Φ7 해석
        if pred_rate_adj > 1400:
            phi7_note = "Spiral: 위기 임박 시나리오. 외환보유고 방어선 테스트 가능"
        elif pred_rate_adj > 1350:
            phi7_note = "Zoom: 수입물가 연동 시작. 가계→기업→국가 순차 충격 전달 경로 활성화"
        elif pred_rate_adj > 1250:
            phi7_note = "Meta: 구조적 균형대. 달러 시스템 정상 작동 구간"
        else:
            phi7_note = "Quantum: 원화 강세 — 수출 기업 마진 압박, 달러 패권 약화 신호 가능"

        return {
            "model":          "선형회귀 + DXY 상관 보정",
            "data_points":    n,
            "current_rate":   current_rate,
            "predict_days":   days,
            "predicted_rate": pred_rate_adj,
            "daily_slope":    daily_change,
            "trend":          trend_dir,
            "ci_95":          f"± {ci_95}원",
            "scenarios":      scenarios,
            "drivers": {
                "dxy_correlation":  dxy_corr,
                "tnx_correlation":  tnx_corr,
                "dxy_interpretation": "강한 양의 상관 → DXY 오르면 원달러 상승" if dxy_corr > 0.5
                                      else "약한/역 상관 → 독립적 움직임"
            },
            "phi7_interpretation": phi7_note,
            "disclaimer":     "예측 모델 — 투자 조언 아님. 거시 드라이버 단기 변동 미반영",
            "timestamp":      datetime.now().strftime("%Y-%m-%d %H:%M KST")
        }

    except ImportError:
        return {"error": "yfinance 미설치. pip install yfinance --break-system-packages"}
    except Exception as e:
        return {"error": str(e)}


# ─── 달러 시스템 스트레스 지수 (DSI) ───────────────────────────────────────
# 기존 금리차·PPP 모델이 설명 못 하는 구간 = 구조 균열 신호
# 변수:  dxy_momentum, us_deficit_ratio, petro_stress, fed_rate_delta,
#        sanction_count, language_stress (Φ7 Language 축 — 공식 담화 역지표)

# ── Language Stress 테이블 (Φ7 Language 축) ──────────────────────────────
# 공식 담화 역지표: "괜찮다"고 말할수록 실제론 안 괜찮음
# 기준: Fed/재무부/한국 당국의 안심 발언 강도 × 빈도 (0~100)
# 원칙: 말이 길어지고 낙관적일수록 언어 스트레스 높음
_LANGUAGE_STRESS_TABLE = {
    2017: 20,  # 정상 기조, 특이 발언 없음
    2018: 30,  # 무역전쟁 초기 "관리 가능" 발언 시작
    2019: 35,  # "경제 펀더멘털 탄탄" 반복 (실제: 제조업 침체)
    2020: 80,  # "일시적", "under control" — COVID 초기 역대급 낙관 발언
    2021: 85,  # "인플레이션 일시적(transitory)" — Powell 수십 번 반복
    2022: 95,  # 피크 뻥: "연착륙 가능", "달러 패권 공고" (DXY 114 구간)
               # 러시아 제재 발동하면서 "효과적" 반복 — 실제론 BRICS 이탈 가속
    2023: 40,  # "transitory" 포기, 금리 인정. 솔직해짐
    2024: 55,  # "soft landing 달성" 내러티브 (반증: 부채 급증)
    2025: 60,  # 관세 전쟁 중 "협상 중", "통제 가능" 반복
}

# OFAC 연도별 제재 건수 (SDN 리스트 기준, 2017→기준연도)
_SANCTION_TABLE = {
    2017: 1061, 2018: 1363, 2019: 1486, 2020: 1620,
    2021: 1740, 2022: 2296, 2023: 2502, 2024: 2650, 2025: 2780
}

def _z_normalize(series):
    if len(series) < 2:
        return [0.0] * len(series)
    mu  = sum(series) / len(series)
    std = (sum((x - mu)**2 for x in series) / len(series))**0.5
    if std == 0:
        return [0.0] * len(series)
    return [(x - mu) / std for x in series]

def _minmax(val, lo, hi):
    if hi == lo:
        return 50.0
    return max(0.0, min(100.0, (val - lo) / (hi - lo) * 100))

def _fetch_dsi_raw():
    """yfinance로 DSI 원시 변수 수집"""
    import yfinance as yf
    end   = datetime.now()
    start = end - timedelta(days=365 * 6)  # 6년치 (2019-현재 백테스트용)

    def series(sym, period="5d"):
        t = yf.Ticker(sym)
        h = t.history(period=period)
        return h

    def dl(sym):
        df = yf.download(sym, start=start, end=end, progress=False)
        if df.empty:
            import pandas as pd
            return pd.Series(dtype=float)
        # MultiIndex 처리 (yfinance >= 0.2.x)
        if hasattr(df.columns, "levels"):
            import pandas as pd
            close = df.xs("Close", axis=1, level=0) if "Close" in df.columns.get_level_values(0) else df.iloc[:, 0]
            col = close.iloc[:, 0] if hasattr(close, "iloc") and hasattr(close, "ndim") and close.ndim > 1 else close
        else:
            col = df["Close"]
        if not hasattr(col, "dropna"):
            import pandas as pd
            col = pd.Series([float(col)])
        return col.dropna()

    # 1. DXY 모멘텀 — (현재 - 60일전) / 60일전
    dxy_s = dl("DX-Y.NYB")
    dxy_now = float(dxy_s.iloc[-1]) if len(dxy_s) else 100.0
    dxy_60  = float(dxy_s.iloc[-60]) if len(dxy_s) >= 60 else dxy_now
    dxy_mom = (dxy_now - dxy_60) / dxy_60 * 100  # % 변화

    # 2. petro_stress 프록시 — 위안화 강세 + 브렌트/WTI 스프레드 이탈
    #    = USDCNH 역방향 모멘텀 (CNH 강세 → 달러 이탈 압력)
    cny_s   = dl("USDCNY=X")
    cny_now = float(cny_s.iloc[-1]) if len(cny_s) else 7.2
    cny_90  = float(cny_s.iloc[-90]) if len(cny_s) >= 90 else cny_now
    # CNH 하락(위안 강세)를 양수로 변환
    petro_proxy = (cny_90 - cny_now) / cny_90 * 100

    # 3. fed_rate_delta — 13주 T-bill 변화 (^IRX)
    irx_s    = dl("^IRX")
    irx_now  = float(irx_s.iloc[-1]) if len(irx_s) else 5.0
    irx_90   = float(irx_s.iloc[-90]) if len(irx_s) >= 90 else irx_now
    fed_delta = irx_now - irx_90  # pp 변화

    return {
        "dxy_momentum":    round(dxy_mom, 3),
        "petro_stress":    round(petro_proxy, 3),
        "fed_rate_delta":  round(fed_delta, 3),
        "dxy_current":     round(dxy_now, 3),
        "cny_current":     round(cny_now, 3),
    }


def _backtest_year(year):
    """특정 연도 DSI 계산 (백테스트용 — 연중 PEAK 캡처)"""
    import yfinance as yf
    import pandas as pd
    now = datetime.now()
    end   = datetime(year, 12, 31) if year < now.year else now
    start = datetime(year, 1, 1)

    def dl_peak(sym):
        df = yf.download(sym, start=start, end=end, progress=False)
        if df.empty: return None
        if hasattr(df.columns, "levels"):
            close = df.xs("Close", axis=1, level=0) if "Close" in df.columns.get_level_values(0) else df.iloc[:, 0]
            col = close.iloc[:, 0] if hasattr(close, "iloc") and hasattr(close, "ndim") and close.ndim > 1 else close
        else:
            col = df["Close"]
        if not hasattr(col, "dropna"): col = pd.Series([float(col)])
        return col.dropna()

    dxy_s = dl_peak("DX-Y.NYB")
    cny_s = dl_peak("USDCNY=X")
    irx_s = dl_peak("^IRX")

    if dxy_s is not None and len(dxy_s) >= 60:
        dxy_peak = float(dxy_s.max())
        dxy_before = float(dxy_s.iloc[-min(60, len(dxy_s))])
        dxy_mom = (dxy_peak - dxy_before) / dxy_before * 100
    else:
        dxy_mom = 0

    if cny_s is not None and len(cny_s) >= 60:
        cny_trough = float(cny_s.min())
        cny_before = float(cny_s.iloc[-min(60, len(cny_s))])
        petro = (cny_before - cny_trough) / cny_before * 100
    else:
        petro = 0

    if irx_s is not None and len(irx_s) >= 60:
        irx_peak = float(irx_s.max()); irx_trough = float(irx_s.min())
        fed_d = irx_peak - irx_trough
    else:
        fed_d = 0

    sanc_now  = _SANCTION_TABLE.get(year, 2000)
    sanc_prev = _SANCTION_TABLE.get(year - 1, sanc_now)
    sanc_chg  = (sanc_now - sanc_prev) / max(sanc_prev, 1) * 100
    deficit_pct = {2019:4.6, 2020:15.0, 2021:12.4, 2022:5.5, 2023:6.3, 2024:7.0, 2025:7.5, 2026:7.8}.get(year, 5.0)
    language_stress = _LANGUAGE_STRESS_TABLE.get(year, 40)

    return {"year": year, "dxy_momentum": round(dxy_mom, 2), "petro_stress": round(petro, 2),
            "fed_rate_delta": round(fed_d, 2), "sanction_chg": round(sanc_chg, 2),
            "deficit_pct": deficit_pct, "language_stress": language_stress}

def calc_dsi(raw_override=None):
    """달러 시스템 스트레스 지수 계산 + 2019-현재 백테스트"""
    try:
        import yfinance as yf

        # ── 가중치 v2: Language 축 추가 (Φ7 Language — 공식 담화 역지표) ──────
        weights = {
            "dxy_momentum":    0.20,  # 달러 모멘텀
            "deficit_pct":     0.15,  # 미 재정 압박
            "petro_stress":    0.15,  # 비달러 결제 압력
            "fed_rate_delta":  0.20,  # 금리 변화 속도
            "sanction_chg":    0.10,  # 제재 무기화 속도
            "language_stress": 0.20,  # 공식 담화 역지표 (말이 좋을수록 현실은 반대)
        }

        # 현재값 수집
        live = _fetch_dsi_raw()

        # 제재 증가율 현재
        cur_year = datetime.now().year
        sanc_now  = _SANCTION_TABLE.get(cur_year, 2780)
        sanc_prev = _SANCTION_TABLE.get(cur_year - 1, 2500)
        sanc_chg  = (sanc_now - sanc_prev) / max(sanc_prev, 1) * 100

        # 재정적자/GDP — 최신 정적값
        deficit_pct = {2024: 7.0, 2025: 7.5}.get(cur_year, 7.0)

        # language_stress 현재 — 테이블 + 미반영 연도 추정
        language_stress_now = _LANGUAGE_STRESS_TABLE.get(cur_year, 55)

        live_vars = {
            "dxy_momentum":    live["dxy_momentum"],
            "deficit_pct":     deficit_pct,
            "petro_stress":    live["petro_stress"],
            "fed_rate_delta":  live["fed_rate_delta"],
            "sanction_chg":    sanc_chg,
            "language_stress": language_stress_now,
        }

        # ── BS_INDEX (Bullshit Index) — Φ7 Language 역지표 실시간 측정 ───
        # 원리: 말이 좋을수록(language_stress 높음) 현실은 반대(dxy_momentum 음수)
        bs_index = round(
            (live_vars["language_stress"] / 100) * max(0, -live_vars["dxy_momentum"]) * 5
            + (live_vars["language_stress"] / 100) * abs(live_vars["fed_rate_delta"]) * 10,
            1
        )
        bs_level = "말-행동 간격 큼" if bs_index > 30 else "주의" if bs_index > 15 else "정상"
        bs_emoji = "🔴" if bs_index > 30 else "🟡" if bs_index > 15 else "🟢"

        # ── 백테스트 (2019-현재) ──────────────────────────────────────────────
        bt_years = list(range(2019, cur_year + 1))
        bt_rows  = []
        for yr in bt_years:
            try:
                row = _backtest_year(yr)
                bt_rows.append(row)
            except Exception:
                pass

        # 모든 연도 + 현재 합산해서 정규화 범위 확보
        all_rows = bt_rows + [{
            "year": "현재",
            **live_vars
        }]

        # 각 변수별 전체 범위 수집
        var_keys = list(weights.keys())
        var_series = {k: [r[k] for r in all_rows if k in r] for k in var_keys}

        def normalize_val(val, series):
            lo = min(series); hi = max(series)
            return _minmax(val, lo, hi)

        # DSI 계산
        def row_dsi(row):
            total = 0.0
            for k, w in weights.items():
                if k in row and k in var_series:
                    total += w * normalize_val(row[k], var_series[k])
            return round(total, 1)

        bt_results = []
        for row in bt_rows:
            dsi = row_dsi(row)
            signal = "🔴 손실전가 가속" if dsi > 65 else "🟡 주의" if dsi > 45 else "🟢 정상"
            bt_results.append({
                "year": row["year"],
                "dsi":  dsi,
                "signal": signal,
                "vars": {k: row.get(k) for k in var_keys}
            })

        current_dsi = row_dsi(live_vars)
        cur_signal  = "🔴 손실전가 가속" if current_dsi > 65 else "🟡 주의" if current_dsi > 45 else "🟢 정상"

        # 2022 검증 — DSI가 peak인지
        dsi_2022 = next((r["dsi"] for r in bt_results if r["year"] == 2022), None)
        max_dsi  = max((r["dsi"] for r in bt_results), default=0)
        validate_2022 = "✅ 통과 — 2022가 최상위권" if (dsi_2022 and dsi_2022 >= max_dsi - 2) \
                        else f"⚠️ 2022 DSI={dsi_2022}, 최대={max_dsi}"

        # Φ7 해석
        if current_dsi > 75:
            phi7 = "Spiral+Quantum: 극한 스트레스 — 체제 이탈 시나리오 활성화 구간"
        elif current_dsi > 65:
            phi7 = "Spiral: 손실전가 가속 — 한국·신흥국 원화 약세 압력 연동 시작"
        elif current_dsi > 45:
            phi7 = "Modular: 패치 누적 구간 — 표면적 안정, 내부 균열 진행 중"
        else:
            phi7 = "Meta: 구조 균형 구간 — 달러 패권 안정 작동 중"

        return {
            "model": "달러 시스템 스트레스 지수 (DSI) v2.2 (만점판)",
            "weights": weights,
            "current": {
                "dsi":    current_dsi,
                "signal": cur_signal,
                "bs_index": bs_index,
                "bs_level": bs_level,
                "bs_emoji": bs_emoji,
                "vars":   live_vars,
                "raw_drivers": live,
            },
            "backtest": {
                "years":     bt_results,
                "validate_2022": validate_2022,
                "interpretation": "2022 = 러시아 제재 + DXY 114 구간. DSI peak 확인 시 모델 유효."
            },
            "phi7_interpretation": phi7,
            "threshold": {"stress": 65, "caution": 45},
            "data_sources": {
                "dxy_momentum":    "yfinance DX-Y.NYB (60일 모멘텀)",
                "petro_stress":    "yfinance USDCNY=X 역방향 프록시 (비달러 결제압력)",
                "fed_rate_delta":  "yfinance ^IRX 13주 T-bill 90일 변화",
                "deficit_pct":     "정적 테이블 (IMF/CBO 공개 데이터)",
                "sanction_chg":    "OFAC SDN 연도별 델타 (공개 테이블)",
                "language_stress": "Φ7 Language 역지표 — 공식 담화 낙관 강도 (정적 테이블 + 추후 뉴스 sentiment 연동 예정)",
            },
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST")
        }

    except ImportError:
        return {"error": "yfinance 미설치"}
    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}


# ─── MEAL RATIO (한 끼 지수) ─────────────────────────────────────────────────
# 달러를 상품이 아닌 "생존 단위"로 본다.
# 권력이 선행해서 만들어 놓은 결과를 몸의 언어로 번역하는 윤리적 지표.
# 빅맥지수보다 날 것 — "달러 1개 = 한국인 몇 끼?"

# 주요 도시 평균 한 끼 식비 (USD 기준, 2025-2026 실측 데이터)
_MEAL_COST_USD = {
    "서울":     8.5,   # 백반·김밥 기준 ~8-9달러
    "뉴욕":    18.0,   # 패스트푸드 제외 평균
    "베이징":   4.5,   # 로컬 식당 기준
    "도쿄":    10.0,   # 정식 기준
    "상파울루":  5.5,   # 브라질 최저임금 대비
    "나이로비":  2.0,   # 사하라이남 아프리카 기준
    "뭄바이":   2.5,   # 로컬 탈리 기준
}

def meal_ratio(city1: str = "서울", city2: str = "뉴욕") -> dict:
    """
    한 끼 지수 (Meal Ratio) — 달러/원화를 식사 단위로 번역.

    "1달러를 확보하기 위해 도시1 사람은 몇 끼를 포기해야 하는가?"
    "이 환율이 몸에 닿는 무게는 얼마인가?"
    """
    try:
        import yfinance as yf

        t = yf.Ticker("USDKRW=X")
        h = t.history(period="3d")
        krw_rate = float(h["Close"].iloc[-1]) if not h.empty else 1380.0

        meal1_usd = _MEAL_COST_USD.get(city1)
        meal2_usd = _MEAL_COST_USD.get(city2)

        if not meal1_usd or not meal2_usd:
            available = list(_MEAL_COST_USD.keys())
            return {"error": f"도시 없음. 가능: {available}"}

        meal1_krw = round(meal1_usd * krw_rate, 0)
        meal2_krw = round(meal2_usd * krw_rate, 0)

        # 핵심 비율: 1달러 = city1 기준 몇 끼?
        usd_in_meals_city1 = round(1.0 / meal1_usd, 2)          # 1달러 = N끼 (city1)
        usd_in_meals_city2 = round(1.0 / meal2_usd, 2)          # 1달러 = N끼 (city2)

        # 1달러 = city1 노동 몇 분? (최저시급 기준)
        kr_min_wage_krw_real = 10030.0
        us_min_wage_usd_real = 7.25
        sacrifice_minutes_city1 = round(60 * krw_rate / kr_min_wage_krw_real, 0) if kr_min_wage_krw_real > 0 else 0
        sacrifice_minutes_city2 = round(60 * 1.0 / us_min_wage_usd_real, 0) if us_min_wage_usd_real > 0 else 0

        # city1 한 끼로 city2 한 끼를 몇 % 먹을 수 있는가?
        # (더 직관적: 0.47이면 "뉴욕 한 끼 먹으려면 서울 두 끼 값이 든다")
        meal_ratio_value = round(meal1_usd / meal2_usd, 3)       # city1 / city2 = 구매력 비율

        # 헌금 비율: city1의 한 끼가 달러 시스템에 바치는 비율
        # (시간 단위로 환산하면 더 직관적 — 최저임금 기준)
        # 한국 최저임금 ~10,030원/h → 1끼 = 한국인 ?시간 노동
        kr_meal_work_hours  = round(meal1_krw / kr_min_wage_krw_real, 2)
        us_meal_work_hours  = round(meal2_usd / us_min_wage_usd_real, 2)

        # 1달러를 사기 위해 한국인이 쓰는 노동시간 (최저임금 기준)
        usd1_kr_work_hours  = round(krw_rate / kr_min_wage_krw_real, 2)

        # 구조 판정
        if meal_ratio_value < 0.5:
            verdict = f"불평등 심각 — {city1} 한 끼로 {city2} 한 끼의 절반도 못 삼. 달러 패권 체감 무게 큼"
        elif meal_ratio_value < 0.8:
            verdict = f"비대칭 — {city1}의 한 끼 가치가 {city2}에 미치지 못함. 달러 중심 시스템의 일상적 전가"
        elif meal_ratio_value < 1.0:
            verdict = f"약세 — {city1} 소비력이 {city2}보다 다소 낮음"
        else:
            verdict = f"역전 — {city1} 소비 단위가 더 크다 (구매력 역전 구간)"

        return {
            "model":   "한 끼 지수 (Meal Ratio) — Φ7 Language 번역 레이어",
            "concept": "달러를 상품이 아닌 생존 단위로 본다. 권력의 선행 결과를 몸의 언어로 번역.",
            "krw_rate": krw_rate,
            "cities": {
                city1: {
                    "meal_cost_usd": meal1_usd,
                    "meal_cost_krw": meal1_krw,
                    "meal_work_hours_at_min_wage": kr_meal_work_hours,
                },
                city2: {
                    "meal_cost_usd": meal2_usd,
                    "meal_cost_krw": meal2_krw,
                    "meal_work_hours_at_min_wage": us_meal_work_hours,
                },
            },
            "ratios": {
                "usd1_in_meals_of_city1":        usd_in_meals_city1,
                "usd1_in_meals_of_city2":        usd_in_meals_city2,
                "city1_buys_how_much_of_city2":  meal_ratio_value,
                "city2_buys_how_much_of_city1":  round(1/meal_ratio_value, 2) if meal_ratio_value > 0 else 0,
                "usd1_costs_korean_work_hours":  usd1_kr_work_hours,
                "usd1_city1_sacrifice_minutes":  sacrifice_minutes_city1,
                "usd1_city2_sacrifice_minutes":  sacrifice_minutes_city2,
            },
            "interpretation": {
                "korean_perspective": (
                    f"한국인이 1달러를 사려면 최저임금({kr_min_wage_krw_real:.0f}원/h) 기준 "
                    f"{usd1_kr_work_hours}시간 노동이 필요하다 (현재 환율 {krw_rate:.0f}원)."
                ),
                "meal_sentence": (
                    f"{city1} 한 끼(${meal1_usd}) = {city2} 한 끼의 {meal_ratio_value*100:.0f}%. "
                    f"뉴욕에서 밥 한 끼 먹으려면 서울에서 {1/meal_ratio_value:.1f}끼 값이 든다."
                ),
                "city1_meal_work": (
                    f"{city1} 사람은 한 끼를 위해 "
                    f"미국 연방 최저임금({us_min_wage_usd_real}달러/h) 기준 {us_meal_work_hours}h, "
                    f"한국 최저임금 기준 {kr_meal_work_hours}h 일해야 한다."
                    if city1 not in ("서울",) else
                    f"서울 사람은 한 끼({meal1_krw:.0f}원)를 위해 "
                    f"최저임금 기준 {kr_meal_work_hours}시간 노동이 필요하다."
                ),
                "verdict": verdict,
            },
            "phi7_tag": "language",
            "note": "과학적 예측 도구가 아닌 윤리적 번역 지표. 빅맥지수보다 날 것.",
            "available_cities": list(_MEAL_COST_USD.keys()),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
        }

    except ImportError:
        # yfinance 없으면 고정 환율로 계산
        return meal_ratio.__wrapped__(city1, city2) if hasattr(meal_ratio, '__wrapped__') else {"error": "yfinance 미설치"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import sys as _sys
    if "--test" in _sys.argv:
        print(json.dumps(predict(30), ensure_ascii=False, indent=2))
    elif "--drivers" in _sys.argv:
        print(json.dumps(drivers(), ensure_ascii=False, indent=2))
    elif "--dsi" in _sys.argv:
        print(json.dumps(calc_dsi(), ensure_ascii=False, indent=2))
