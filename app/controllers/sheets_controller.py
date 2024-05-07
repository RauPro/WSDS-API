from uuid import uuid4

from fastapi import FastAPI, HTTPException, APIRouter

from ..models import Prompt, SheetEntry
from ..services.driver.sheets_crud import create_sheet, get_sheets, get_sheet_by_id, update_sheet, delete_sheet

router = APIRouter()
@router.post("/sheets/")
def create(sheet: SheetEntry):
    if sheet.priority > 3:
        create_sheet(sheet);
        return {"message": "sheet created successfully", "data": sheet.dict()}
    else:    
     return {"message": "sorry we can't save this sheet"}
    

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
