from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class CategorizationResult(BaseModel):
    category: str
    amount: int = Field(ge=0)
    type: Literal["expense", "income"]
    comment: str


class DebtParseResult(BaseModel):
    name: str
    item: str
    amount: int = Field(ge=0)
    date: date
