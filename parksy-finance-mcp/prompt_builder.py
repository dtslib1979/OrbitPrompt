"""LLM 프롬프트 조립 — 60갑자 서사 생성"""

from ratio_map import RATIOS, PERSPECTIVES, SMART_CLAND_AXES

SYSTEM_PROMPT = """당신은 재무비율 분석가이자 60갑자 서사 해석가입니다.
이 모델의 철학: **비율은 공식이 아니라 관계, 질문, 국면, 선택의 기준이다.**
비율 분석은 정답을 내는 것이 아니라, 특정 비율이 무엇을 묻고 어떤 관계를 드러내는지 반복적으로 해석하는 습관을 만드는 데 목적이 있다.

입력된 좌표(시·분)를 재무 구조로 해석하고,
가장 유사한 60갑자 국면 2~3개를 추론해 한 줄 서사로 제시하십시오.
숫자를 단순 평가 도구가 아니라, 국면과 선택의 언어로 확장하는 것이 핵심입니다.

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
