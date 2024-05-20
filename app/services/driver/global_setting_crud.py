from app.models import PromptEntry
from app.services.db_service import DatabaseService
from app.services.driver.id_generator import ObjectId
from app.services.driver.promptEntry_crud import get_promptsEntry

DatabaseService()
collection = DatabaseService.get_global_collection()


def init_global():
    initial_id_global = {"_id": "id_global", "value": "1"}
    return collection.update_one({"_id": "id_global"}, {"$setOnInsert": initial_id_global}, upsert=True)


def update_id_global(new_value: str):
    result = collection.update_one(
        {"_id": "id_global"},
        {"$set": {"value": new_value}}
    )
    return result.modified_count == 1


def get_setting():
    return collection.find_one({"_id": "id_global"})


def generate_new_global():
    list_ids = get_promptsEntry()
    update_id_global(list_ids[0]["id"])
