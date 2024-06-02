from app.models import Prompt, New
from app.services.db_service import DatabaseService
from app.services.driver.sheets_crud import get_sheet_by_id

DatabaseService()
collection = DatabaseService.get_news_collection()
def create_new(new_data: New):
    """
    Creates a new document in the 'news' collection or updates an existing one.

    Args:
        new_data (New): The data for the new document.

    Returns:
        dict: A dictionary indicating the status of the operation and the ID of the document.
            - If a new document was inserted, returns {"status": "inserted", "id": <document_id>}.
            - If an existing document was updated, returns {"status": "updated", "id": <document_id>}.
            - If no action was taken, returns {"status": "no action", "id": <document_id>}.
    """
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
    """
    Retrieves all documents from the 'news' collection.

    Returns:
        list: A list of dictionaries representing the news documents, excluding the '_id' field.
    """
    lv = collection.find({}, {'_id': 0})
    return list(lv)


def get_news_sheets():
    """
    Retrieves all documents from the 'news' collection along with their associated sheets.

    Returns:
        list: A list of dictionaries representing the news documents, including the associated sheet data.
    """
    lv = collection.find({}, {'_id': 0})
    lv = list(lv)
    for it in lv:
        it["sheet"] = get_sheet_by_id(it["url"])
    return lv

def get_new_by_id(new_id: str):
    """
    Retrieves a single document from the 'news' collection by its ID.

    Args:
        new_id (str): The ID of the document to retrieve.

    Returns:
        dict: The document matching the provided ID, excluding the '_url' field, or None if not found.
    """
    return collection.find_one({"url": new_id}, {'_url': 0})

def update_new(new_id: str, new_data: New):
    """
    Updates a document in the 'news' collection by its ID.

    Args:
        new_id (str): The ID of the document to update.
        new_data (New): The updated data for the document.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation.
    """
    return collection.update_one({"url": new_id}, {"$set": new_data.dict()})

def delete_new(new_id: str):
    """
    Deletes a document from the 'news' collection by its ID.

    Args:
        new_id (str): The ID of the document to delete.
    """
    collection.delete_one({"url": new_id})

def delete_date(document_id, field_name):
    """
    Deletes a specific field from a document in the 'news' collection.

    Args:
        document_id (str): The ID of the document.
        field_name (str): The name of the field to delete.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation.
    """
    result = collection.update_one(
        {'url': document_id},  # The filter to find the document
        {'$unset': {field_name: ""}}  # The $unset operator to remove the field
    )
    return result