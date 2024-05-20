from app.models import Prompt
from app.models import PromptEntry
from app.services.db_service import DatabaseService
from app.services.driver.global_setting_crud import get_setting
from app.services.driver.id_generator import ObjectId
from app.services.driver.promptEntry_crud import get_promptEntry_by_id

DatabaseService()
collection = DatabaseService.get_prompts_collection()
def create_prompt(prompt_data: Prompt):
    prompt_data.id =  ObjectId()
    collection.insert_one(prompt_data.dict())

def get_prompts():
    current_setting = get_setting()
    prompt = get_promptEntry_by_id(current_setting.get("value"))
    if prompt is not None:
        return prompt.get("indicators")
    return False

def get_prompt_by_id(prompt_id: str):
    return collection.find_one({"id": prompt_id}, {'_id': 0})

def update_prompt(prompt_id: str, prompt_data: Prompt):
    collection.update_one({"id": prompt_id}, {"$set": prompt_data.dict()})

def delete_prompt(prompt_id: str):
    collection.delete_one({"id": prompt_id})
