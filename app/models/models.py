# app/models.py

from pydantic import BaseModel
from typing import List, Optional

from app.services.driver.id_generator import ObjectId


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


class Prompt(BaseModel):
    indicator_name: str
    prompt: str
    id: Optional[str] = ObjectId()
