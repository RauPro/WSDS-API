from app.models import Prompt, New
from app.services.db_service import DatabaseService

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

def get_new_by_id(new_id: str):
    return collection.find_one({"url": new_id}, {'_url': 0})

def update_new(new_id: str, new_data: New):
    collection.update_one({"url": new_id}, {"$set": new_data.dict()})

def delete_new(new_id: str):
    collection.delete_one({"url": new_id})
