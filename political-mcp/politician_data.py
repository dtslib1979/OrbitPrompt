#!/usr/bin/env python3
"""
politician_data.py — 정치인 기초 데이터 + 7축 자동 계산 (v1.0 통합)

형 설계:   정치인 DB 4명 + 깔끔한 구조
DeepSeek:  데이터 기반 7축 자동 계산 엔진
"""

# 정치인 기초 데이터
POLITICIANS = {
    "박찬대": {
        "party": "더불어민주당",
        "region": "인천 연수구을",
        "terms": 4,
        "base_approval": 52.0,
        "age": 58,
        "role": "원내대표",
        "education": "인하대 경영학과",
        "career_years": 8,
        "committees": ["정무위원회", "AI특별위원회"],
        "keywords": ["AI", "인천", "물류", "돌봄", "경영"],
        "policies": ["AI 도시 인천", "노인 AI 리터러시", "인천 물류 허브"],
        "speeches": 120, "bills": 18, "media": 45
    },
    "이재명": {
        "party": "더불어민주당",
        "region": "인천 계양구을",
        "terms": 5,
        "base_approval": 48.0,
        "age": 60,
        "role": "대표",
        "education": "중앙대 법학과",
        "career_years": 15,
        "committees": ["예산결산특별위원회"],
        "keywords": ["기본소득", "복지", "재정", "개혁", "성장"],
        "policies": ["기본소득", "재정 확장", "보편 복지"],
        "speeches": 350, "bills": 45, "media": 280
    },
    "한동훈": {
        "party": "국민의힘",
        "region": "비례대표",
        "terms": 1,
        "base_approval": 38.0,
        "age": 51,
        "role": "대표",
        "education": "서울대 법학과",
        "career_years": 3,
        "committees": ["법제사법위원회"],
        "keywords": ["검찰", "개혁", "법치", "반부패"],
        "policies": ["검찰 개혁", "법치주의", "반부패"],
        "speeches": 180, "bills": 12, "media": 200
    },
    "조국": {
        "party": "조국혁신당",
        "region": "비례대표",
        "terms": 2,
        "base_approval": 42.0,
        "age": 60,
        "role": "대표",
        "education": "서울대 법학과",
        "career_years": 4,
        "committees": ["법제사법위원회", "교육위원회"],
        "keywords": ["혁신", "교육", "검찰개혁", "진보"],
        "policies": ["검찰개혁", "교육 혁신", "사법 개혁"],
        "speeches": 150, "bills": 20, "media": 190
    },
}

# Φ드라이버 7축 가중치
AXIS_WEIGHTS = {
    "meta":     1.2,  # 발언 일관성
    "reverse":  1.1,  # 위기 대응
    "modular":  1.0,  # 정책 패턴
    "language": 1.0,  # 수사력
    "zoom":     1.2,  # 의제 집중
    "spiral":   1.3,  # 성장 궤적
    "quantum":  1.5,  # 이변 가능성
}

PHI5_WEIGHT = 0.3

# Φ7 LABELS
PHI7_LABELS = {
    "meta":     "발언 일관성 — 과거 입장과 현재의 정합성",
    "reverse":  "위기 대응 — 스캔들·역풍·반대파 대응력",
    "modular":  "정책 조합 — 공약·법안·사업의 패키지 설계력",
    "language": "프레이밍 — 메시지 구조화·수사·내러티브",
    "zoom":     "스케일링 — 중앙정치↔지역구 연결 능력",
    "spiral":   "모멘텀 — 이슈 증폭·타이밍·사이클 이해",
    "quantum":  "변수 중첩 — 예측불가·다중이해관계 해석"
}

def calc_base_strength(name: str) -> float:
    """기초 Φ5 점수: 데이터 기반"""
    p = POLITICIANS.get(name)
    if not p: return 50.0
    role_bonus = {"대표": 10, "원내대표": 8, "장관": 7, "의원": 0}.get(p["role"], 0)
    score = (p["terms"] * 8) + (p["base_approval"] * 0.6) + role_bonus + min(10, len(p["keywords"]) * 2)
    return round(min(100, max(20, score)), 1)

def calc_phi7_scores(name: str) -> dict:
    """데이터 기반 7축 자동 계산 (DeepSeek 엔진)"""
    p = POLITICIANS.get(name)
    if not p: return {k: 50 for k in AXIS_WEIGHTS}
    
    meta = min(95, 50 + min(p["speeches"], 200) * 0.12 + p["bills"] * 1.5)
    reverse = min(95, 40 + p["career_years"] * 3 + len(p["committees"]) * 8)
    modular = min(95, 45 + len(p["policies"]) * 8 + len(p["keywords"]) * 4)
    language = min(95, 40 + min(p["media"], 200) * 0.2 + (10 if p["education"] else 0))
    zoom = min(95, 50 + len(p["committees"]) * 10 + p["career_years"] * 2)
    spiral = min(95, 45 + p["bills"] * 1.2 + min(p["speeches"], 150) * 0.1)
    quantum = min(95, 40 + len(p["keywords"]) * 5 + len(p["committees"]) * 6)
    
    return {
        "meta": round(meta, 1), "reverse": round(reverse, 1),
        "modular": round(modular, 1), "language": round(language, 1),
        "zoom": round(zoom, 1), "spiral": round(spiral, 1),
        "quantum": round(quantum, 1)
    }
