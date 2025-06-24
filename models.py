from typing import Literal
from pydantic import BaseModel


class EvaluationResult(BaseModel):
    reasoning: str
    status: Literal["pass", "fail"]
