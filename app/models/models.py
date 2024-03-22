# app/models.py
from pydantic import BaseModel
from typing import List, Optional


class NoticeRequest(BaseModel):
    model: str
    prompt: str
    stream: Optional[bool] = False


class NoticeResponse(BaseModel):
    model: str
    created_at: str
    response: str
    done: bool
    context: List[int]
    total_duration: int
    load_duration: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int
