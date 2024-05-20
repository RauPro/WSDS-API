from uuid import uuid4

from fastapi import FastAPI, HTTPException, APIRouter

from ..models import Prompt
from ..services.driver.prompts_crud import create_prompt, get_prompts, get_prompt_by_id, update_prompt, delete_prompt
router = APIRouter()
@router.post("/prompts/")
def create(prompt: Prompt):
    create_prompt(prompt)
    return {"message": "Prompt created successfully", "data": prompt.dict()}

@router.get("/prompts/")
def read_all():
    result = get_prompts()
    if result is not None:
        return result
    raise HTTPException(status_code=404, detail="Prompt not found")

@router.get("/prompts/{prompt_id}")
def read(prompt_id: str):
    prompt = get_prompt_by_id(prompt_id)
    if prompt is not None:
        return prompt
    raise HTTPException(status_code=404, detail="Prompt not found")

@router.put("/prompts/{prompt_id}")
def update(prompt_id: str, prompt: Prompt):
    update_prompt(prompt_id, prompt)
    return {"message": "Prompt updated successfully."}

@router.delete("/prompts/{prompt_id}")
def delete(prompt_id: str):
    delete_prompt(prompt_id)
    return {"message": "Prompt deleted successfully."}
