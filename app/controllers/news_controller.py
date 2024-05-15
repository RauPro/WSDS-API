from uuid import uuid4

from fastapi import FastAPI, HTTPException, APIRouter

from ..models import Prompt, New
from ..services.driver.news_crud import create_new, get_news, get_new_by_id, update_new, delete_new, get_news_sheets

router = APIRouter()
@router.post("/news/")
def create(new: New):
    new_ = create_new(new)
    return {"message": "new created successfully", "data": new.dict(), "returned": new_}

@router.get("/news/")
def read_all():
    return get_news()
@router.get("/news-sheet/")
def read_all():
    return get_news_sheets()

@router.get("/news/{new_id}")
def read(new_id: str):
    new = get_new_by_id(new_id)
    if new is not None:
        return new
    raise HTTPException(status_code=404, detail="new not found")

@router.put("/news/{new_id}")
def update(new_id: str, new: New):
    update_new(new_id, new)
    return {"message": "new updated successfully."}

@router.delete("/news/{new_id}")
def delete(new_id: str):
    delete_new(new_id)
    return {"message": "new deleted successfully."}
