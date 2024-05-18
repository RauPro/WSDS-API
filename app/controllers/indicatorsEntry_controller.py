from uuid import uuid4
from fastapi import FastAPI, HTTPException, APIRouter

from ..models import PromptEntry
from ..services.driver.promptEntry_crud import create_promptEntry, get_promptsEntry, get_promptEntry_by_id, update_promptEntry, delete_promptEntry
router = APIRouter()
@router.post("/promptsEntry/")
def create(prompt: PromptEntry):
    create_promptEntry(prompt)
    return {"message": "Prompt created successfully", "data": prompt.dict()}

@router.get("/promptsEntry/")
def read_all():
    return get_promptsEntry()

@router.get("/promptsEntry/{prompt_id}")
def read(prompt_id: str):
    prompt = get_promptEntry_by_id(prompt_id)
    if prompt is not None:
        return prompt
    raise HTTPException(status_code=404, detail="Prompt not found")

@router.put("/promptsEntry/{prompt_id}")
def update(prompt_id: str, prompt: PromptEntry):
    update_promptEntry(prompt_id, prompt)
    return {"message": "Prompt updated successfully."}

@router.delete("/promptsEntry/{prompt_id}")
def delete(prompt_id: str):
    delete_promptEntry(prompt_id)
    return {"message": "Prompt deleted successfully."}
