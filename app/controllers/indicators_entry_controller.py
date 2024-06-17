from fastapi import HTTPException, APIRouter
from ..models import PromptEntry
from ..services.driver.global_setting_crud import generate_new_global
from ..services.driver.prompt_entry_crud import create_prompt_entry, get_prompts_entry, get_prompt_entry_by_id, \
    update_prompt_entry, delete_prompt_entry
from fastapi import HTTPException, APIRouter

from ..models import PromptEntry
from ..services.driver.global_setting_crud import generate_new_global
from ..services.driver.prompt_entry_crud import create_prompt_entry, get_prompts_entry, get_prompt_entry_by_id, \
    update_prompt_entry, delete_prompt_entry

router = APIRouter()


@router.post("/promptsEntry/")
def create(prompt: PromptEntry) -> dict:
    """
    Create a new prompt entry.

    Args:
        prompt (PromptEntry): The prompt entry data to create.

    Returns:
        dict: A dictionary containing a success message and the created prompt entry data.
    """
    created = create_prompt_entry(prompt)
    return {"message": "Prompt created successfully", "data": prompt.dict()}


@router.get("/promptsEntry/")
def read_all() -> list:
    """
    Get all prompt entries.

    Returns:
        list: A list of all prompt entries.
    """
    return get_prompts_entry()


@router.get("/promptsEntry/{prompt_id}")
def read(prompt_id: str) -> dict:
    """
    Get a prompt entry by ID.

    Args:
        prompt_id (str): The ID of the prompt entry to retrieve.

    Returns:
        dict: The prompt entry data.

    Raises:
        HTTPException: If the prompt entry is not found (status code 404).
    """
    prompt = get_prompt_entry_by_id(prompt_id)
    if prompt is not None:
        return prompt
    raise HTTPException(status_code=404, detail="Prompt not found")


@router.put("/promptsEntry/{prompt_id}")
def update(prompt_id: str, prompt: PromptEntry) -> dict:
    """
    Update a prompt entry by ID.

    Args:
        prompt_id (str): The ID of the prompt entry to update.
        prompt (PromptEntry): The updated prompt entry data.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the prompt entry is not found (status code 404).
    """
    updated = update_prompt_entry(prompt_id, prompt.dict())
    if updated.modified_count > 0:
        return {"message": "Prompt Entry updated successfully."}
    else:
        raise HTTPException(status_code=404, detail="Setting not found")


@router.delete("/promptsEntry/{prompt_id}")
def delete(prompt_id: str) -> dict:
    """
    Delete a prompt entry by ID.

    Args:
        prompt_id (str): The ID of the prompt entry to delete.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the prompt entry is not found (status code 404).
    """
    deleted = delete_prompt_entry(prompt_id)
    if deleted:
        generate_new_global()
        return {"message": "Prompt deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Setting not found")
