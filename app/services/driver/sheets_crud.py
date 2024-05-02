from app.models import Prompt, SheetEntry
from app.services.db_service import DatabaseService

DatabaseService()
collection = DatabaseService.get_sheets_collection()


def create_sheet(sheet_data: SheetEntry):
    collection.insert_one(sheet_data.dict())


def get_sheets():
    lv = collection.find({}, {'_id': 0})
    return list(lv)


def get_sheet_by_id(sheet_id: str):
    return collection.find_one({"id": sheet_id}, {'_id': 0})


def update_sheet(sheet_id: str, sheet_data: SheetEntry):
    collection.update_one({"id": sheet_id}, {"$set": sheet_data.dict()})


def delete_sheet(sheet_id: str):
    collection.delete_one({"id": sheet_id})
