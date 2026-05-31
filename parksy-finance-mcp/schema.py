"""입출력 타입 정의"""

from pydantic import BaseModel, Field
from typing import Optional


class AnalyzeInput(BaseModel):
    hour: int = Field(..., ge=1, le=12, description="재무비율 시계 위치 (1~12)")
    minute: int = Field(..., ge=1, le=5, description="하위 관점 인덱스 (1~5)")
    context: Optional[str] = Field(None, description="기업명 / 추가 데이터 / 키워드")
    axis: Optional[str] = Field(
        None,
        pattern=r"^(S|M|A|R|T|C|L|A2|N|D)$",
        description="SMART/CLAND 해석 축 (선택)",
    )


class AnalyzeOutput(BaseModel):
    slot_id: str
    ratio_name_ko: str
    ratio_name_en: str
    perspective_code: str
    perspective_desc: str
    raw_ratio_block: str
    story_blocks: list[str]
    prompt_suggestions: list[str]
    axis_analysis: Optional[dict] = None
