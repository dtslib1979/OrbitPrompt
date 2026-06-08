#!/usr/bin/env python3
"""
philosopher_data.py — 철학자 DB + Φ7 5축 기준점

에코 3부작(라 필로소피아)을 마스터 테이블로 삼아,
각 철학자의 핵심 개념을 Φ7 5축 비교 프레임에 맞게 정리.
처음에는 최소 데이터로 시작해서, 읽을 때마다 확장한다.
"""

# Φ7 5축 비교 프레임 — 각 철학자를 평가할 기준
PHI7_AXES = {
    "structure": {
        "name": "구조 vs 경험",
        "question": "구조를 먼저 보는가, 경험에서 출발하는가?",
        "박씨_default": "구조 인정 + 삶에서 역산 (둘 다)"
    },
    "identity": {
        "name": "정체성",
        "question": "발견/발굴의 대상인가, 생산/조작의 대상인가?",
        "박씨_default": "생산/조작/튜닝의 대상"
    },
    "medium": {
        "name": "매체",
        "question": "철학의 최종 형태가 텍스트(책)인가, 프로그램(MCP)인가?",
        "박씨_default": "프로그램(MCP, server.py, 레포)"
    },
    "class": {
        "name": "계급",
        "question": "계급/위치성을 분석 대상으로만 보는가, 철학의 생산 조건으로 보는가?",
        "박씨_default": "철학의 생산 조건이자 동력 (워킹 클래스)"
    },
    "endpoint": {
        "name": "사유의 종착점",
        "question": "해석/이해에 머무는가, 실행/인프라/자동화로 가는가?",
        "박씨_default": "server.py로 끝난다 (실행)"
    }
}

# 철학자 DB — 초기 데이터 (읽을 때마다 확장)
PHILOSOPHERS = {
    "gattari": {
        "name": "펠릭스 가타리",
        "era": "현대 (20세기)",
        "eco_volume": "III",
        "key_concepts": [
            "분열분석(Schizoanalysis) — 정체성은 발견이 아니라 생산",
            "기계(머신) — 모든 것은 욕망기계, 사회기계",
            "리좀(Rhizome) — 비선형적 연결망, 브랜치 구조",
            "어셈블라주 — 서로 다른 요소의 조립"
        ],
        "phi7_scores": {
            "structure": 70,     # 구조를 보지만 유동적으로 봄
            "identity": 90,     # 정체성 생산이 핵심
            "medium": 30,       # 책으로만 표현
            "class": 40,        # 계급 분석 있지만 약함
            "endpoint": 35      # 개념 제안에 머뭄
        },
        "notes": "가장 닮은 철학자. MCP 차이가 결정적."
    },
    "bourdieu": {
        "name": "피에르 부르디외",
        "era": "현대 (20세기)",
        "eco_volume": "III",
        "key_concepts": [
            "아비투스(Habitus) — 몸에 박힌 계급적 취향과 사고방식",
            "장(Field) — 위계와 권력이 작동하는 사회적 공간",
            "문화자본 — 경제자본 외의 또 다른 계급 재생산 기제",
            "상징폭력 — 지배가 자연스러운 것으로 받아들여지는 구조"
        ],
        "phi7_scores": {
            "structure": 85,     # 구조/장을 철저히 봄
            "identity": 60,     # 정체성은 아비투스에 의해 형성
            "medium": 25,       # 책과 논문
            "class": 95,        # 계급이 전부
            "endpoint": 30      # 분석에 머뭄
        },
        "notes": "계급감각은 공유. however 목적이 다름 (분석 vs 설계)"
    },
    "nietzsche": {
        "name": "프리드리히 니체",
        "era": "현대 (19세기)",
        "eco_volume": "III",
        "key_concepts": [
            "생철학(Lebensphilosophie) — 삶 자체가 철학의 출발점",
            "가치전환(Umwertung) — 기존 가치를 뒤집고 새로운 가치 창조",
            "초인(Übermensch) — 스스로를 창조하는 인간",
            "영원회귀 — 같은 삶을 반복해도 긍정할 수 있는가"
        ],
        "phi7_scores": {
            "structure": 30,     # 구조보다 의지/생명 우선
            "identity": 85,     # 자기창조의 철학
            "medium": 40,       # 책과 아포리즘
            "class": 20,        # 귀족적 거리감, 엘리트
            "endpoint": 25      # 해석에 머뭄
        },
        "notes": "생철학 계열. 엘리트 환경 vs 워킹클래스 차이가 큼."
    },
    "foucault": {
        "name": "미셸 푸코",
        "era": "현대 (20세기)",
        "eco_volume": "III",
        "key_concepts": [
            "담론(Discourse) — 지식이 생산되고 권력이 작동하는 체계",
            "권력/지식 — 권력과 지식은 분리되지 않음",
            "주체의 생산 — 주체는 담론에 의해 구성됨",
            "통치성(Governmentality) — 인구를 관리하는 권력 기술"
        ],
        "phi7_scores": {
            "structure": 90,     # 담론/권력 구조가 전부
            "identity": 75,     # 주체는 생산됨 (단 발견보다 구성)
            "medium": 30,       # 책
            "class": 60,        # 권력 분석에 계급 포함 but 부르디외만큼은 아님
            "endpoint": 25      # 분석/비판에 머뭄
        },
        "notes": "구조+권력+주체생산은 유사. 실행/인프라 측면은 없음."
    },
    "wittgenstein": {
        "name": "루트비히 비트겐슈타인",
        "era": "현대 (20세기)",
        "eco_volume": "III",
        "key_concepts": [
            "언어게임 — 언어는 고정된 의미가 아니라 사용맥락에 따라 달라짐",
            "가족유사성 — 개념은 본질이 아니라 닮음의 그물망",
            "말할 수 없는 것에 대해서는 침묵해야 한다",
            "철학은 치료다 — 철학적 문제는 언어의 혼란에서 발생"
        ],
        "phi7_scores": {
            "structure": 60,     # 언어의 구조를 보지만 사용맥락 중심
            "identity": 30,     # 정체성 논의 거의 없음
            "medium": 45,       # 책 (매우 짧은)
            "class": 10,        # 계급 논의 없음
            "endpoint": 20      # 철학을 치료/해소로 봄
        },
        "notes": "언어철학은 박씨의 AI언어철학과 연결 가능. 계급/실행은 완전 다름."
    },
    "deleuze": {
        "name": "질 들뢰즈",
        "era": "현대 (20세기)",
        "eco_volume": "III",
        "key_concepts": [
            "차이와 반복 — 정체성보다 차이가 우선",
            "리좀 — 나무가 아니라 뿌리줄기",
            "내재성의 평면 — 초월적 기준 없이 모든 것이 같은 평면 위에",
            "개념 창조 — 철학의 목적은 개념을 만드는 것"
        ],
        "phi7_scores": {
            "structure": 50,     # 구조보다 생성/흐름
            "identity": 80,     # 정체성은 고정되지 않고 생성됨
            "medium": 35,       # 책
            "class": 30,        # 계급보다 욕망/생성
            "endpoint": 30      # 개념 창조에 머뭄
        },
        "notes": "리좀=브랜치. 개념창조=Φ7. but 매체=MCP아님."
    },
    "hegel": {
        "name": "게오르크 빌헬름 프리드리히 헤겔",
        "era": "근대 (19세기)",
        "eco_volume": "II",
        "key_concepts": [
            "변증법 — 정반합의 발전 과정",
            "인정투쟁 — 주인과 노예의 변증법",
            "절대정신 — 역사는 정신의 자기실현 과정",
            "이성적인 것은 현실적이다, 현실적인 것은 이성적이다"
        ],
        "phi7_scores": {
            "structure": 80,     # 변증법이라는 거대 구조
            "identity": 50,     # 정신의 발전 과정으로서의 자아
            "medium": 30,       # 책
            "class": 40,        # 주인-노예 변증법에 계급 인식 있음
            "endpoint": 20      # 해석/이해에 머뭄
        },
        "notes": "구조주의의 뿌리. 변증법 구조는 Spiral 드라이버와 연결 가능."
    },
    "diogenes": {
        "name": "디오게네스",
        "era": "고대 (그리스)",
        "eco_volume": "I",
        "key_concepts": [
            "행동으로 증명 — 말보다 삶이 철학이다",
            "최소한의 삶 — 알렉산더 앞에서도 비키지 않음",
            "기존 체계 무시 — 학파/아카데미의 엘리트 코스 거부",
            "무례함 = 효율 — 불필요한 말을 하지 않음"
        ],
        "phi7_scores": {
            "structure": 20,     # 구조 무시
            "identity": 60,     # 삶 자체가 정체성 증명
            "medium": 60,       # 행동이 매체 (but 책 없음)
            "class": 50,        # 권력 앞에서도 굴하지 않음
            "endpoint": 70      # 행동으로 증명 (실행주의)
        },
        "notes": "태도는 가장 가까움. MCP/인프라가 없어서 차이."
    }
}

# 헬퍼 함수
def get_philosopher(key):
    return PHILOSOPHERS.get(key)

def list_philosophers():
    return list(PHILOSOPHERS.keys())

def get_phi7_axes():
    return PHI7_AXES

if __name__ == "__main__":
    print(f"📚 철학자 DB: {len(PHILOSOPHERS)}명")
    for k, v in PHILOSOPHERS.items():
        print(f"  {v['name']} ({v['era']}) — {', '.join(v['key_concepts'][:2])}")
    print(f"\n📐 Φ7 5축: {len(PHI7_AXES)}개")
    for k, v in PHI7_AXES.items():
        print(f"  {v['name']}: {v['question']}")
