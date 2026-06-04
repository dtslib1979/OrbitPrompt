"""LLM 프롬프트 조립 — 60갑자 서사 생성 (갑자 컨텍스트 포함)"""

from gapja_master import PHASE_MEANINGS, get_gapja
from ratio_map import RATIOS, PERSPECTIVES, SMART_CLAND_AXES

SYSTEM_PROMPT = """당신은 재무비율 분석가이자 60갑자 서사 해석가입니다.

이 모델의 철학: **비율은 공식이 아니라 관계, 질문, 국면, 선택의 기준이다.**
재무비율 분석은 정답을 내는 것이 아니라, 특정 비율이 무엇을 묻고 어떤 관계를 드러내는지
반복적으로 해석하는 습관을 만드는 데 목적이 있다.

입력: 시·분 좌표, 해당 갑자 국면, 기업 컨텍스트 (선택)
출력: 갑자 서사를 바탕으로 한 재무 국면 해석

반드시 JSON 형식으로만 응답하십시오. 다른 텍스트 없이.

JSON 형식:
{
  "raw_ratio_block": "해당 좌표의 재무 구조 설명 (2~3문장, 구체적)",
  "story_blocks": [
    "갑자명(한자): 서사 한 줄 — 재무적 의미",
    "갑자명(한자): 서사 한 줄 — 재무적 의미"
  ],
  "prompt_suggestions": [
    "분석가용 심층 질문1",
    "분석가용 심층 질문2",
    "분석가용 심층 질문3"
  ]
}"""


def build(
    h: int, m: int, ctx: str | None = None, axis: str | None = None
) -> tuple[str, str]:
    """시/분/컨텍스트 → (system_prompt, user_prompt)"""
    r_ko, r_en = RATIOS[h]
    p_code, p_en, p_desc = PERSPECTIVES[m]
    gj = get_gapja(h, m)
    pm = PHASE_MEANINGS.get(gj["phase_code"], {})

    user = (
        f"좌표: {h}시 {m}분\n"
        f"비율: {r_ko} ({r_en})\n"
        f"관점: {p_code} — {p_desc}\n"
        f"갑자: {gj['hanja']} ({gj['hangul']}) / 오행: {gj['ohaeng']}\n"
        f"국면: {pm.get('ko', gj['phase_code'])} — {gj['story']}\n"
        f"시그널: {pm.get('signal', '')}\n"
        f"컨텍스트: {ctx or '없음'}\n"
    )

    if axis and axis in SMART_CLAND_AXES:
        a_en, a_ko = SMART_CLAND_AXES[axis]
        user += f"해석 축: {axis}({a_en} — {a_ko})\n"

    user += (
        "\n위 좌표의 재무 국면을 갑자 서사로 해석해주세요.\n"
        "raw_ratio_block에는 이 비율이 이 관점에서 어떤 구조적 의미를 갖는지 설명하세요.\n"
        "story_blocks에는 이 갑자와 연관된 재무 서사 2개를 제시하세요.\n"
        "prompt_suggestions에는 분석가가 다음에 물어봐야 할 핵심 질문 3개를 제시하세요."
    )

    return SYSTEM_PROMPT, user
