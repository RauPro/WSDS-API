from app.models import Prompt
from app.services.db_service import DatabaseService
from app.services.driver.global_setting_crud import get_setting
from app.services.driver.id_generator import ObjectId
from app.services.driver.prompt_entry_crud import get_prompt_entry_by_id

DatabaseService()
collection = DatabaseService.get_prompts_collection()


def create_prompt(prompt_data: Prompt):
    """
    Creates a new prompt in the 'prompts' collection.

    Args:
        prompt_data (Prompt): The data for the new prompt.

    Returns:
        None
    """
    prompt_data.id = ObjectId()
    collection.insert_one(prompt_data.dict())


def get_prompts():
    """
    Retrieves the indicators of the current prompt entry.

    Returns:
        dict: The indicators of the current prompt entry if found.
        bool: False if the current prompt entry is not found.
    """
    current_setting = get_setting()
    prompt = get_prompt_entry_by_id(current_setting.get("value"))
    if prompt is not None:
        return prompt.get("indicators")
    return False


def get_prompt_by_id(prompt_id: str):
    """
    Retrieves a single prompt from the 'prompts' collection by its ID.

    Args:
        prompt_id (str): The ID of the prompt to retrieve.

    Returns:
        dict: The prompt matching the provided ID, excluding the '_id' field, or None if not found.
    """
    return collection.find_one({"id": prompt_id}, {'_id': 0})


def update_prompt(prompt_id: str, prompt_data: Prompt):
    """
    Updates a prompt in the 'prompts' collection by its ID.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (Prompt): The updated data for the prompt.

    Returns:
        None
    """
    collection.update_one({"id": prompt_id}, {"$set": prompt_data.dict()})


def delete_prompt(prompt_id: str):
    """
    Deletes a prompt from the 'prompts' collection by its ID.

    Args:
        prompt_id (str): The ID of the prompt to delete.

    Returns:
        None
    """
    collection.delete_one({"id": prompt_id})
