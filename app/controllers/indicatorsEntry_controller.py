from uuid import uuid4
from fastapi import FastAPI, HTTPException, APIRouter

from ..models import PromptEntry
from ..services.driver.global_setting_crud import generate_new_global
from ..services.driver.prompt_entry_crud import create_prompt_entry, get_prompts_entry, get_prompt_entry_by_id, update_prompt_entry, delete_prompt_entry
router = APIRouter()
@router.post("/promptsEntry/")
def create(prompt: PromptEntry):
    created = create_prompt_entry(prompt)
    return {"message": "Prompt created successfully", "data": prompt.dict()}

@router.get("/promptsEntry/")
def read_all():
    return get_prompts_entry()

@router.get("/promptsEntry/{prompt_id}")
def read(prompt_id: str):
    prompt = get_prompt_entry_by_id(prompt_id)
    if prompt is not None:
        return prompt
    raise HTTPException(status_code=404, detail="Prompt not found")

@router.put("/promptsEntry/{prompt_id}")
def update(prompt_id: str, prompt: PromptEntry):
    updated = update_prompt_entry(prompt_id, prompt.dict())
    if updated.modified_count > 0:
        return {"message": "Prompt Entry updated successfully."}
    else:
        raise HTTPException(status_code=404, detail="Setting not found")


@router.delete("/promptsEntry/{prompt_id}")
def delete(prompt_id: str):
    deleted = delete_prompt_entry(prompt_id)
    if deleted:
        generate_new_global()
        return {"message": "Prompt deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Setting not found")
