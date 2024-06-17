from fastapi import HTTPException, APIRouter

from ..models import Prompt
from ..services.driver.prompts_crud import create_prompt, get_prompts, get_prompt_by_id, update_prompt, delete_prompt

router = APIRouter()


@router.post("/prompts/")
def create(prompt: Prompt):
    """
    Create a new prompt.

    Args:
        prompt (Prompt): The prompt data to create.

    Returns:
        dict: A dictionary containing a success message and the created prompt data.
    """
    create_prompt(prompt)
    return {"message": "Prompt created successfully", "data": prompt.dict()}


@router.get("/prompts/")
def read_all():
    """
    Get all prompts.

    Returns:
        list: A list of all prompts.

    Raises:
        HTTPException: If no prompts are found (status code 404).
    """
    result = get_prompts()
    if result is not None:
        return result
    raise HTTPException(status_code=404, detail="Prompt not found")


@router.get("/prompts/{prompt_id}")
def read(prompt_id: str):
    """
    Get a prompt by ID.

    Args:
        prompt_id (str): The ID of the prompt to retrieve.

    Returns:
        dict: The prompt data.

    Raises:
        HTTPException: If the prompt is not found (status code 404).
    """
    prompt = get_prompt_by_id(prompt_id)
    if prompt is not None:
        return prompt
    raise HTTPException(status_code=404, detail="Prompt not found")


@router.put("/prompts/{prompt_id}")
def update(prompt_id: str, prompt: Prompt):
    """
    Update a prompt by ID.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt (Prompt): The updated prompt data.

    Returns:
        dict: A dictionary containing a success message.
    """
    update_prompt(prompt_id, prompt)
    return {"message": "Prompt updated successfully."}


@router.delete("/prompts/{prompt_id}")
def delete(prompt_id: str):
    """
    Delete a prompt by ID.

    Args:
        prompt_id (str): The ID of the prompt to delete.

    Returns:
        dict: A dictionary containing a success message.
    """
    delete_prompt(prompt_id)
    return {"message": "Prompt deleted successfully."}
