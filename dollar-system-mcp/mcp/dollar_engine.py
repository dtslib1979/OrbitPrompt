#!/usr/bin/env python3
"""달러 시스템 엔진 v2.0 — 상태분석 + 예측 모델 (yfinance 드라이버)"""

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


if __name__ == "__main__":
    import sys as _sys
    if "--test" in _sys.argv:
        print(json.dumps(predict(30), ensure_ascii=False, indent=2))
    elif "--drivers" in _sys.argv:
        print(json.dumps(drivers(), ensure_ascii=False, indent=2))
