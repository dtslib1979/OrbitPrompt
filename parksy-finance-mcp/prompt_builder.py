"""LLM 프롬프트 조립 — 60갑자 서사 생성"""

from ratio_map import RATIOS, PERSPECTIVES, SMART_CLAND_AXES

SYSTEM_PROMPT = """당신은 재무비율 분석 전문가이자 60갑자 서사 해석가입니다.
입력된 좌표(시·분)를 재무 구조로 해석하고,
가장 유사한 60갑자 국면 2~3개를 추론해 한 줄 서사로 제시합니다.

출력은 반드시 JSON 형식으로만 응답하십시오. 다른 텍스트 없이.

JSON 형식:
{
  "raw_ratio_block": "해당 좌표의 재무 구조 설명 (2~3문장)",
  "story_blocks": ["갑자명: 서사 한 줄", "갑자명: 서사 한 줄"],
  "prompt_suggestions": ["분석가용 질문1", "분석가용 질문2", "분석가용 질문3"]
}"""


def build(
    h: int, m: int, ctx: str | None = None, axis: str | None = None
) -> tuple[str, str]:
    """시/분/컨텍스트 → (system_prompt, user_prompt)"""
    r_ko, r_en = RATIOS[h]
    p_code, p_en, p_desc = PERSPECTIVES[m]

    user = f"좌표: {h}시 {m}분 ({r_ko} × {p_code} — {p_desc})\n"
    user += f"컨텍스트: {ctx or '없음'}\n"

    if axis and axis in SMART_CLAND_AXES:
        a_en, a_ko = SMART_CLAND_AXES[axis]
        user += f"해석 축: {axis}({a_en} — {a_ko})\n"

    user += (
        "\n출력 JSON 형식:\n"
        "{\n"
        '  "raw_ratio_block": "string",\n'
        '  "story_blocks": ["갑자명: 서사", ...],\n'
        '  "prompt_suggestions": ["질문1", ...]\n'
        "}"
    )

    return SYSTEM_PROMPT, user
