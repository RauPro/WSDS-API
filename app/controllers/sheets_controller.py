from uuid import uuid4

from fastapi import FastAPI, HTTPException, APIRouter

from ..models import Prompt, SheetEntry
from ..services.driver.sheets_crud import create_sheet, get_sheets, get_sheet_by_id, update_sheet, delete_sheet, create_or_update_sheet

router = APIRouter()
@router.post("/sheets/")
def create(sheet: SheetEntry):
    existing_sheet = get_sheet_by_id(sheet.id)
    
    if sheet.priority == 1:
        create_or_update_sheet(sheet, existing_sheet)
        return {"message": "Sheet created/updated successfully with priority 1", "data": sheet.dict()}
    
    elif sheet.priority == 2:
        if existing_sheet is None or existing_sheet.get('priority', 999) < 2:
            create_or_update_sheet(sheet, existing_sheet)
            return {"message": "Sheet created/updated successfully with priority 2", "data": sheet.dict()}
        else:
            return {"message": "Cannot overwrite existing sheet with higher priority"}

    elif sheet.priority == 3:
        if existing_sheet is not None and existing_sheet.get('priority', 999) == 4:
            create_or_update_sheet(sheet, existing_sheet)
            return {"message": "Sheet updated successfully with priority 3", "data": sheet.dict()}
        else:
            return {"message": "Cannot overwrite existing sheet unless priority is 4"}

    elif sheet.priority > 3:
        create_or_update_sheet(sheet, existing_sheet)
        return {"message": "Sheet created/updated successfully", "data": sheet.dict()}
    
    else:
        return {"message": "Sorry, we can't save this sheet due to priority rules"}

    

@router.get("/sheets/")
def read_all():
    return get_sheets()

@router.get("/sheets/{sheet_id}")
def read(sheet_id: str):
    sheet = get_sheet_by_id(sheet_id)
    if sheet is not None:
        return sheet
    raise HTTPException(status_code=404, detail="sheet not found")

@router.put("/sheets/{sheet_id}")
def update(sheet_id: str, sheet: SheetEntry):
    update_sheet(sheet_id, sheet)
    return {"message": "sheet updated successfully."}

@router.delete("/sheets/{sheet_id}")
def delete(sheet_id: str):
    delete_sheet(sheet_id)
    return {"message": "sheet deleted successfully."}
