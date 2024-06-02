from app.models import PromptEntry
from app.services.db_service import DatabaseService
from app.services.driver.id_generator import ObjectId

DatabaseService()
collection = DatabaseService.get_prompt_entry_collection()


def create_prompt_entry(prompt_data: PromptEntry):
    """
    Creates a new prompt entry in the 'promptsEntry' collection.

    Args:
        prompt_data (PromptEntry): The data for the new prompt entry.

    Returns:
        pymongo.results.InsertOneResult: The result of the insert operation.
    """
    return collection.insert_one(prompt_data.dict())


def get_prompts_entry():
    """
    Retrieves all prompt entries from the 'promptsEntry' collection.

    Returns:
        list: A list of dictionaries representing the prompt entries, excluding the '_id' field.
    """
    lv = collection.find({}, {'_id': 0})
    return list(lv)


def get_prompt_entry_by_id(prompt_id: str):
    """
    Retrieves a single prompt entry from the 'promptsEntry' collection by its ID.

    Args:
        prompt_id (str): The ID of the prompt entry to retrieve.

    Returns:
        dict: The prompt entry matching the provided ID, excluding the '_id' field, or None if not found.
    """
    return collection.find_one({"id": prompt_id}, {'_id': 0})


def update_prompt_entry(prompt_id: str, prompt_data: PromptEntry):
    """
    Updates a prompt entry in the 'promptsEntry' collection by its ID.

    Args:
        prompt_id (str): The ID of the prompt entry to update.
        prompt_data (PromptEntry): The updated data for the prompt entry.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation.
    """
    return collection.update_one({"id": prompt_id}, {"$set": prompt_data})


def delete_prompt_entry(prompt_id: str):
    """
    Deletes a prompt entry from the 'promptsEntry' collection by its ID.

    Args:
        prompt_id (str): The ID of the prompt entry to delete.

    Returns:
        bool: True if the prompt entry was successfully deleted, False otherwise.
    """
    result = collection.delete_one({"id": prompt_id})
    return result.deleted_count == 1
