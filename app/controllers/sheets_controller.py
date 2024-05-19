from uuid import uuid4

from fastapi import FastAPI, HTTPException, APIRouter, Query

from . import generate_answer
from ..models import Prompt, SheetEntry, New
from ..services.driver.sheets_crud import create_sheet, get_sheets, get_sheet_by_id, update_sheet, delete_sheet, \
    create_or_update_sheet, create_sheet_priority

router = APIRouter()
@router.post("/sheets/")
def create(sheet: SheetEntry):
    try:
        create_sheet_priority(sheet.dict())
    except Exception as e:
        print(f"Failed to create sheet: {e}")
        raise

    

@router.get("/sheets/")
def read_all():
    return get_sheets()

@router.get("/sheet/")
def read(sheet_id: str = Query(None)):
    sheet = get_sheet_by_id(sheet_id)
    if sheet is not None:
        return sheet
    raise HTTPException(status_code=404, detail="sheet not found")

@router.put("/sheets/")
def update(sheet_id: str = Query(None), sheet: SheetEntry = None):
    result = update_sheet(sheet_id, sheet.dict())
    if result.modified_count > 0:
        sheet = sheet.dict()
        return {"status": "updated", "id": sheet["id"]}
    else:
        raise HTTPException(status_code=404, detail="sheet not found")

@router.delete("/sheets/{sheet_id}")
def delete(sheet_id: str):
    delete_sheet(sheet_id)
    return {"message": "sheet deleted successfully."}


@router.post("/generate_sheet/")
def geneate_sheet(new: New = None):
    try:
        return generate_answer(new)

    except Exception as e:
        print(f"Failed to create sheet: {e}")
    raise


