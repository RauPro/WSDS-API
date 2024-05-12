from app.models import Prompt, SheetEntry
from app.services.db_service import DatabaseService

DatabaseService()
collection = DatabaseService.get_sheets_collection()


def create_sheet(sheet_data: SheetEntry):
    try:
        collection.insert_one(sheet_data)
    except Exception as e:
        # Log the exception or handle it accordingly
        print(f"Failed to create sheet: {e}")
        raise


def get_sheets():
    lv = collection.find({}, {'_id': 0})
    return list(lv)


def get_sheet_by_id(sheet_id: str):
    return collection.find_one({"id": sheet_id}, {'_id': 0})


def update_sheet(sheet_id: str, sheet_data: SheetEntry):
    collection.update_one({"id": sheet_id}, {"$set": sheet_data})


def delete_sheet(sheet_id: str):
    collection.delete_one({"id": sheet_id})


def create_or_update_sheet(sheet: SheetEntry, existing_sheet):
    if existing_sheet is None:
        create_sheet(sheet)
    else:
        update_sheet(sheet["id"], sheet)


def create_sheet_priority(sheet: SheetEntry):
    existing_sheet = get_sheet_by_id(sheet["id"])
    if sheet["priority"] == 1:
        create_or_update_sheet(sheet, existing_sheet)
        return({"message": "Sheet created/updated successfully with priority 1", "data": sheet})

    elif sheet["priority"] == 2:
        if existing_sheet is None or existing_sheet.get('priority', 999) < 2:
            create_or_update_sheet(sheet, existing_sheet)
            return({"message": "Sheet created/updated successfully with priority 2", "data": sheet})
        else:
            return({"message": "Cannot overwrite existing sheet with higher priority"})

    elif sheet["priority"] == 3:
        if (existing_sheet is not None and existing_sheet.get('priority', 999) == 4) or existing_sheet is None:
            create_or_update_sheet(sheet, existing_sheet)
            return({"message": "Sheet updated successfully with priority 3", "data": sheet})
        else:
            return({"message": "Cannot overwrite existing sheet unless priority is 4"})

    elif sheet["priority"] > 3:
        create_or_update_sheet(sheet, existing_sheet)
        return({"message": "Sheet created/updated successfully", "data": sheet})

    else:
        return({"message": "Sorry, we can't save this sheet due to priority rules"})
