#!/usr/bin/env python3
"""
philosopher_data.py — Φ7 7축 철학자 DB (형 리뷰 3순위 반영)

변경: 5축(structure/identity/medium/class/endpoint) → Φ7 7축
"""
PHI7_DIMENSIONS = {
    "meta": {
        "name": "🧠 Meta",
        "desc": "전체를 보는 눈 — 방법론, 자기인식, 체계 설계",
        "features": ["체계_설계", "방법론_중시", "자기인식", "메타분석", "구조_중시", "관계_중시"]
    },
    "reverse": {
        "name": "🔄 Reverse",
        "desc": "거꾸로 읽기 — 역방향 설계, 실패분석",
        "features": ["역방향_설계", "실패분석", "케이스스터디", "비판_중심", "해체_중심"]
    },
    "modular": {
        "name": "🧩 Modular",
        "desc": "조립하기 — 재사용 가능한 도구, 시스템 설계",
        "features": ["도구_제작", "시스템_설계", "재사용_중시", "실행_중심", "모듈화"]
    },
    "language": {
        "name": "💬 Language",
        "desc": "언어로 마감 — 프레이밍, 내러티브",
        "features": ["언어게임", "프레이밍", "개념_제안", "책_중심", "담론_분석"]
    },
    "zoom": {
        "name": "🔍 Zoom",
        "desc": "스케일 조절 — 개인→도시→국가",
        "features": ["계급_분석", "권력_분석", "사회구조", "위계_인정", "스케일_전환"]
    },
    "spiral": {
        "name": "📈 Spiral",
        "desc": "반복 상승 — 성장 궤적, 발전",
        "features": ["변증법", "발전_중시", "반복_상승", "역사_중시", "자기극복"]
    },
    "quantum": {
        "name": "⚡ Quantum",
        "desc": "도약 — 예측, 시뮬레이션, 이변",
        "features": ["도약_중심", "예측_중시", "자동화_중심", "인프라_중심", "구축_중심"]
    }
}

PARKSY_FEATURES = {
    "meta":     ["체계_설계", "방법론_중시", "자기인식", "구조_중시"],
    "reverse":  ["역방향_설계", "실패분석", "케이스스터디"],
    "modular":  ["도구_제작", "시스템_설계", "재사용_중시", "실행_중심"],
    "language": ["프레이밍", "개념_제안"],
    "zoom":     ["계급_분석", "권력_분석", "스케일_전환"],
    "spiral":   ["반복_상승", "자기극복"],
    "quantum":  ["자동화_중심", "인프라_중심", "구축_중심", "도약_중심"]
}

PHILOSOPHERS = {
    "gattari": {
        "name": "펠릭스 가타리", "era": "현대 20세기", "eco_volume": "III",
        "key_concepts": ["분열분석 — 정체성은 발견이 아니라 생산", "기계철학 — 모든 것은 어셈블라주", "리좀 — 비선형적 연결망"],
        "features": {
            "meta": ["방법론_중시", "관계_중시", "구조_중시"],
            "reverse": ["비판_중심", "해체_중심", "케이스스터디"],
            "modular": ["시스템_설계", "실행_중심"],
            "language": ["개념_제안", "책_중심", "담론_분석"],
            "zoom": ["권력_분석", "사회구조"],
            "spiral": ["반복_상승", "자기극복"],
            "quantum": ["도약_중심", "구축_중심"]
        }
    },
    "bourdieu": {
        "name": "피에르 부르디외", "era": "현대 20세기", "eco_volume": "III",
        "key_concepts": ["아비투스 — 몸에 박힌 계급적 취향", "장(Field) — 위계와 권력의 공간", "문화자본 — 계급 재생산 기제"],
        "features": {
            "meta": ["체계_설계", "구조_중시", "관계_중시", "메타분석"],
            "reverse": ["비판_중심"],
            "modular": ["시스템_설계"],
            "language": ["책_중심", "담론_분석"],
            "zoom": ["계급_분석", "권력_분석", "사회구조", "위계_인정", "스케일_전환"],
            "spiral": ["반복_상승"],
            "quantum": []
        }
    },
    "nietzsche": {
        "name": "프리드리히 니체", "era": "현대 19세기", "eco_volume": "III",
        "key_concepts": ["생철학 — 삶이 철학의 출발점", "가치전환 — 기존 가치를 뒤집음", "초인 — 스스로 창조하는 인간"],
        "features": {
            "meta": ["자기인식", "방법론_중시"],
            "reverse": ["역방향_설계", "해체_중심", "비판_중심"],
            "modular": [],
            "language": ["개념_제안", "책_중심"],
            "zoom": ["사회구조"],
            "spiral": ["반복_상승", "자기극복", "발전_중시"],
            "quantum": ["도약_중심"]
        }
    },
    "foucault": {
        "name": "미셸 푸코", "era": "현대 20세기", "eco_volume": "III",
        "key_concepts": ["담론 — 지식과 권력의 체계", "권력/지식 — 불가분의 관계", "주체의 생산 — 담론에 의해 구성"],
        "features": {
            "meta": ["체계_설계", "구조_중시", "관계_중시", "메타분석"],
            "reverse": ["비판_중심", "해체_중심"],
            "modular": [],
            "language": ["담론_분석", "책_중심", "프레이밍"],
            "zoom": ["권력_분석", "계급_분석", "사회구조", "위계_인정"],
            "spiral": ["반복_상승"],
            "quantum": []
        }
    },
    "wittgenstein": {
        "name": "루트비히 비트겐슈타인", "era": "현대 20세기", "eco_volume": "III",
        "key_concepts": ["언어게임 — 의미는 사용맥락에 따라 결정", "가족유사성 — 개념은 닮음의 그물망", "철학은 치료"],
        "features": {
            "meta": ["방법론_중시", "메타분석"],
            "reverse": ["해체_중심"],
            "modular": [],
            "language": ["언어게임", "개념_제안", "책_중심", "프레이밍"],
            "zoom": [],
            "spiral": [],
            "quantum": []
        }
    },
    "deleuze": {
        "name": "질 들뢰즈", "era": "현대 20세기", "eco_volume": "III",
        "key_concepts": ["차이와 반복 — 정체성보다 차이", "리좀 — 탈중심적 연결망", "개념 창조 — 철학의 임무"],
        "features": {
            "meta": ["방법론_중시", "관계_중시"],
            "reverse": ["해체_중심", "비판_중심"],
            "modular": ["시스템_설계", "모듈화"],
            "language": ["개념_제안", "책_중심", "담론_분석"],
            "zoom": ["사회구조", "권력_분석"],
            "spiral": ["반복_상승", "자기극복"],
            "quantum": ["도약_중심"]
        }
    },
    "hegel": {
        "name": "게오르크 헤겔", "era": "근대 19세기", "eco_volume": "II",
        "key_concepts": ["변증법 — 정반합 발전", "인정투쟁 — 주인과 노예", "절대정신 — 역사의 자기실현"],
        "features": {
            "meta": ["체계_설계", "구조_중시", "메타분석"],
            "reverse": ["비판_중심"],
            "modular": ["시스템_설계"],
            "language": ["개념_제안", "책_중심"],
            "zoom": ["사회구조", "위계_인정"],
            "spiral": ["변증법", "발전_중시", "반복_상승", "역사_중시"],
            "quantum": []
        }
    },
    "diogenes": {
        "name": "디오게네스", "era": "고대 그리스", "eco_volume": "I",
        "key_concepts": ["행동으로 증명 — 말보다 삶", "최소한의 삶 — 권력 앞에서도 비키지 않음", "체계 거부"],
        "features": {
            "meta": ["자기인식"],
            "reverse": ["역방향_설계", "해체_중심", "비판_중심"],
            "modular": ["도구_제작", "실행_중심"],
            "language": [],
            "zoom": [],
            "spiral": ["자기극복"],
            "quantum": ["도약_중심"]
        }
    },
    "kierkegaard": {
        "name": "쇠렌 키르케고르", "era": "현대 19세기", "eco_volume": "III",
        "key_concepts": ["실존은 선택 — 진리는 주관성", "단독자 — 군중에 속하지 않음", "불안과 절망 — 진정한 자아"],
        "features": {
            "meta": ["자기인식", "방법론_중시"],
            "reverse": ["비판_중심", "해체_중심"],
            "modular": [],
            "language": ["개념_제안", "책_중심"],
            "zoom": [],
            "spiral": ["자기극복", "반복_상승"],
            "quantum": ["도약_중심"]
        }
    },
    "arendt": {
        "name": "한나 아렌트", "era": "현대 20세기", "eco_volume": "III",
        "key_concepts": ["악의 평범성 — 평범한 사람이 만드는 악", "행위적 삶 — 행위를 통한 자유", "공적 영역 — 정치의 상실"],
        "features": {
            "meta": ["방법론_중시"],
            "reverse": ["비판_중심", "케이스스터디"],
            "modular": [],
            "language": ["담론_분석", "책_중심", "프레이밍"],
            "zoom": ["권력_분석", "계급_분석", "사회구조", "위계_인정"],
            "spiral": ["발전_중시"],
            "quantum": []
        }
    },
    "marx": {
        "name": "카를 마르크스", "era": "현대 19세기", "eco_volume": "III",
        "key_concepts": ["유물사관 — 토대가 상부구조 결정", "계급투쟁 — 모든 역사는 계급투쟁", "철학은 세계를 변화시켜야 한다"],
        "features": {
            "meta": ["체계_설계", "구조_중시", "관계_중시", "메타분석"],
            "reverse": ["비판_중심", "역방향_설계"],
            "modular": ["시스템_설계", "실행_중심"],
            "language": ["개념_제안", "책_중심", "담론_분석"],
            "zoom": ["계급_분석", "권력_분석", "사회구조", "위계_인정", "스케일_전환"],
            "spiral": ["변증법", "발전_중시", "역사_중시"],
            "quantum": ["도약_중심", "구축_중심"]
        }
    }
}

def list_philosophers():
    return list(PHILOSOPHERS.keys())

def get_philosopher(key):
    return PHILOSOPHERS.get(key)

def get_all_features():
    return {dim: data["features"] for dim, data in PHI7_DIMENSIONS.items()}
