import re
from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException, APIRouter, Query

from ..models import Prompt, New, SheetEntry
from ..services.driver.news_crud import create_new, get_news, get_new_by_id, update_new, delete_new, get_news_sheets, \
    delete_date
from ..utils import serialize_new, is_search_in_text

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

@router.post("/news-sheet-filter/")
def read_all_saved(search_word: str = None, filters_sheet: SheetEntry = None, date_start: str = None,
                   date_end: str = None):
    if filters_sheet is not None:
        filters_sheet = filters_sheet.dict()
    enable_search = False
    for it in filters_sheet["indicators"]:
        if it["response"] != "":
            enable_search = True
    date_regex = r"^.{4}-.{2}-.{2}$"
    #list_saved_news = get_news_sheets()
    list_saved_news = get_news_sheets()
    if search_word is not None:
        list_saved_news = [new for new in list_saved_news if is_search_in_text(search_word, new["text"])]
    if filters_sheet is not None and enable_search:
        filtered_news = []
        for new in list_saved_news:
            if new["sheet"] is not None:
                filters = filters_sheet
                saved = new["sheet"]
                for filter_ in filters["indicators"]:
                    found = False
                    indicator_to_find = filter_["indicator_name"]
                    response_to_find = filter_["response"]
                    for it in saved["indicators"]:
                        if indicator_to_find == it["indicator_name"] and response_to_find in it["response"] and response_to_find != "":
                            filtered_news.append(new)
                            found = True
                            break
                    if found:
                        break
        list_saved_news = filtered_news
    date_start_obj = datetime.strptime(date_start, '%Y-%m-%d').date() if date_start else None
    date_end_obj = datetime.strptime(date_end, '%Y-%m-%d').date() if date_end else None
    if (date_start is not None and date_start != "") and (date_end is None or date_end == ""):
        list_saved_news = [news for news in list_saved_news if
                           re.match(date_regex, news["date"]) and datetime.strptime(news["date"], '%Y-%m-%d').date() >= date_start_obj]
    if (date_end is not None and date_end != "") and (date_start is None or date_start == ""):
        list_saved_news = [news for news in list_saved_news if
                           re.match(date_regex, news["date"]) and datetime.strptime(news["date"], '%Y-%m-%d').date() <= date_end_obj]
    if (date_end is not None and date_start is not None) and (date_end != "" and date_start != ""):
        ans = []
        for new in list_saved_news:
            if re.match(date_regex, new["date"]) and datetime.strptime(new["date"], '%Y-%m-%d').date() >= date_start_obj and datetime.strptime(
                    new["date"], '%Y-%m-%d').date() <= date_end_obj:
                ans.append(new)
        list_saved_news = ans

    return list_saved_news


@router.get("/new/")
def read(new_id: str = Query(None)):
    new = get_new_by_id(new_id)
    if new is not None:
        serialized_new = serialize_new(new)
        return serialized_new
    raise HTTPException(status_code=404, detail="new not found")


@router.put("/news/")
def update(new_id: str = Query(None), new: New = None):
    result = update_new(new_id, new)
    if result.modified_count > 0:
        new = new.dict()
        return {"status": "updated", "id": new["url"]}
    else:
        raise HTTPException(status_code=404, detail="sheet not found")


@router.delete("/news/{new_id}")
def delete(new_id: str):
    delete_new(new_id)
    return {"message": "new deleted successfully."}
