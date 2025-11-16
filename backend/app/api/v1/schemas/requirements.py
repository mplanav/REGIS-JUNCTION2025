from pydantic import BaseModel
from typing import Optional


class RequirementBase(BaseModel):
    id: int
    text: str
    risk_type: Optional[str]
    jurisdiction: str
    page: Optional[int]
    line: Optional[int]
    short_description: Optional[str]


class RequirementListResponse(BaseModel):
    count: int
    items: list[RequirementBase]


class RequirementDetailResponse(BaseModel):
    id: int
    text: str
    risk_type: Optional[str]
    jurisdiction: str
    page: Optional[int]
    line: Optional[int]
    description: str
