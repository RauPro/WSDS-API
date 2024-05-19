from app.models import Prompt, New
from app.services.db_service import DatabaseService
from app.services.driver.sheets_crud import get_sheet_by_id

DatabaseService()
collection = DatabaseService.get_news_collection()
def create_new(new_data: New):
    result = collection.update_one(
        {"url": new_data.get("url")},
        {"$setOnInsert": new_data},
        upsert=True
    )
    if result.upserted_id is not None:
        return {"status": "inserted", "id": str(result.upserted_id)}
    else:
        if result.modified_count > 0:
            return {"status": "updated", "id": new_data.get("url")}
        else:
            return {"status": "no action", "id": new_data.get("url")}

def get_news():
    lv = collection.find({}, {'_id': 0})
    return list(lv)


def get_news_sheets():
    lv = collection.find({}, {'_id': 0})
    lv = list(lv)
    for it in lv:
        it["sheet"] = get_sheet_by_id(it["url"])
    return lv

def get_new_by_id(new_id: str):
    return collection.find_one({"url": new_id}, {'_url': 0})

def update_new(new_id: str, new_data: New):
    return collection.update_one({"url": new_id}, {"$set": new_data.dict()})

def delete_new(new_id: str):
    collection.delete_one({"url": new_id})

def delete_date(document_id, field_name):
    """Delete a specific field from a MongoDB document."""
    result = collection.update_one(
        {'url': document_id},  # The filter to find the document
        {'$unset': {field_name: ""}}  # The $unset operator to remove the field
    )
    return result