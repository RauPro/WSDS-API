from fastapi import HTTPException, APIRouter, Query
from . import generate_answer
from ..models import SheetEntry, New
from ..services.driver.sheets_crud import get_sheets, get_sheet_by_id, update_sheet, delete_sheet, \
    create_sheet_priority
from fastapi import HTTPException, APIRouter, Query

from . import generate_answer
from ..models import SheetEntry, New
from ..services.driver.sheets_crud import get_sheets, get_sheet_by_id, update_sheet, delete_sheet, \
    create_sheet_priority

router = APIRouter()


@router.post("/sheets/")
def create(sheet: SheetEntry) -> None:
    """
    Create a new sheet.

    Args:
        sheet (SheetEntry): The sheet data to create.

    Raises:
        Exception: If there is an error while creating the sheet.
    """
    try:
        create_sheet_priority(sheet.dict())
    except Exception as e:
        print(f"Failed to create sheet: {e}")
        raise


@router.get("/sheets/")
def read_all() -> list:
    """
    Get all sheets.

    Returns:
        list: A list of all sheets.
    """
    return get_sheets()


@router.get("/sheet/")
def read(sheet_id: str = Query(None)) -> dict:
    """
    Get a sheet by ID.

    Args:
        sheet_id (str): The ID of the sheet to retrieve.

    Returns:
        dict: The sheet data.

    Raises:
        HTTPException: If the sheet is not found (status code 404).
    """
    sheet = get_sheet_by_id(sheet_id)
    if sheet is not None:
        return sheet
    raise HTTPException(status_code=404, detail="sheet not found")


@router.put("/sheets/")
def update(sheet_id: str = Query(None), sheet: SheetEntry = None) -> dict:
    """
    Update a sheet by ID.

    Args:
        sheet_id (str): The ID of the sheet to update.
        sheet (SheetEntry): The updated sheet data.

    Returns:
        dict: A dictionary containing the update status and the ID of the updated sheet.

    Raises:
        HTTPException: If the sheet is not found (status code 404).
    """
    result = update_sheet(sheet_id, sheet.dict())
    if result.modified_count > 0:
        sheet = sheet.dict()
        return {"status": "updated", "id": sheet["id"]}
    else:
        raise HTTPException(status_code=404, detail="sheet not found")


@router.delete("/sheets/{sheet_id}")
def delete(sheet_id: str) -> dict:
    """
    Delete a sheet by ID.

    Args:
        sheet_id (str): The ID of the sheet to delete.

    Returns:
        dict: A dictionary containing a success message.
    """
    delete_sheet(sheet_id)
    return {"message": "sheet deleted successfully."}


@router.post("/generate_sheet/")
def generate_sheet(new: New = None):
    """
    Generate a sheet based on the provided news data.

    Args:
        new (New): The news data to generate the sheet from.

    Returns:
        dict: The generated sheet data.

    Raises:
        Exception: If there is an error while generating the sheet.
    """
    try:
        return generate_answer(new.dict())
    except Exception as e:
        print(f"Failed to create sheet: {e}")
        raise
