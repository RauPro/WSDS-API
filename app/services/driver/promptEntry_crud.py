from app.models import PromptEntry
from app.services.db_service import DatabaseService


    
DatabaseService()
collection = DatabaseService.get_promptEntry_collection()
def create_promptEntry(prompt_data: PromptEntry):
    collection.insert_one(prompt_data.dict())

def get_promptsEntry():
    lv = collection.find({}, {'_id': 0})
    return list(lv)

def get_promptEntry_by_id(prompt_id: str):
    return collection.find_one({"id": prompt_id}, {'_id': 0})

def update_promptEntry(prompt_id: str, prompt_data: PromptEntry):
    collection.update_one({"id": prompt_id}, {"$set": prompt_data.dict()})

def delete_promptEntry(prompt_id: str):
    collection.delete_one({"id": prompt_id})
