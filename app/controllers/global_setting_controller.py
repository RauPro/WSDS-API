import re
from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException, APIRouter, Query

from ..models import Prompt, New, SheetEntry
from ..services.driver.global_setting_crud import init_global, update_id_global, get_setting
from ..services.driver.news_crud import create_new, get_news, get_new_by_id, update_new, delete_new, get_news_sheets, \
    delete_date
from ..utils import serialize_new, is_search_in_text

router = APIRouter()


@router.post("/init_global/")
def create():
    return "Init"


@router.put("/update_global/{setting_id}")
def update(setting_id: str):
    updated = update_id_global(setting_id)
    if updated:
        return {"message": "Setting set successfully."}

    else:
        raise HTTPException(status_code=404, detail="Setting not found")


@router.get("/global_id/")
def get_setting_global():
    return get_setting()
