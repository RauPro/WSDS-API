from app.models import Prompt
from app.services.db_service import DatabaseService

DatabaseService()
collection = DatabaseService.get_prompts_collection()
def create_prompt(prompt_data: Prompt):
    collection.insert_one(prompt_data.dict())

def get_prompts():
    lv = collection.find({}, {'_id': 0})
    return list(lv)

def get_prompt_by_id(prompt_id: str):
    return collection.find_one({"id": prompt_id}, {'_id': 0})

def update_prompt(prompt_id: str, prompt_data: Prompt):
    collection.update_one({"id": prompt_id}, {"$set": prompt_data.dict()})

def delete_prompt(prompt_id: str):
    collection.delete_one({"id": prompt_id})
