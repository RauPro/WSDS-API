from app.services.db_service import DatabaseService
from app.services.driver.prompt_entry_crud import get_prompts_entry

DatabaseService()
collection = DatabaseService.get_global_collection()


def init_global() -> None:
    """
    Initializes the global settings in the database.

    This function creates an initial document in the 'global' collection with the '_id' set to 'id_global'
    and the 'value' set to '1'. If the document already exists, it will not be modified.

    Returns:
        None
    """
    initial_id_global = {"_id": "id_global", "value": "1"}
    return collection.update_one({"_id": "id_global"}, {"$setOnInsert": initial_id_global}, upsert=True)


def update_id_global(new_value: str) -> bool:
    """
    Updates the 'value' field of the 'id_global' document in the 'global' collection.

    Args:
        new_value (str): The new value to set for the 'value' field.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    result = collection.update_one(
        {"_id": "id_global"},
        {"$set": {"value": new_value}}
    )
    return result.modified_count == 1


def get_setting() -> dict:
    """
    Retrieves the 'id_global' document from the 'global' collection.

    Returns:
        dict: The 'id_global' document, or None if it doesn't exist.
    """
    return collection.find_one({"_id": "id_global"})


def generate_new_global() -> None:
    """
    Generates a new global ID based on the first promptEntry ID.

    This function retrieves the list of promptEntry documents using the `get_promptsEntry` function,
    and updates the 'value' field of the 'id_global' document with the ID of the first promptEntry.

    Returns:
        None
    """
    list_ids = get_prompts_entry()
    update_id_global(list_ids[0]["id"])
