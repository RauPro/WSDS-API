from fastapi import HTTPException, APIRouter

from ..services.driver.global_setting_crud import update_id_global, get_setting

router = APIRouter()


@router.post("/init_global/")
def create():
    """
    Initialize the global settings.

    Returns:
        str: A message indicating the initialization status.
    """
    return "Init"


@router.put("/update_global/{setting_id}")
def update(setting_id: str):
    """
    Update the global setting with the provided setting ID.

    Args:
        setting_id (str): The ID of the setting to update.

    Returns:
        dict: A dictionary containing a success message if the setting is updated.

    Raises:
        HTTPException: If the setting is not found (status code 404).
    """
    updated = update_id_global(setting_id)
    if updated:
        return {"message": "Setting set successfully."}

    else:
        raise HTTPException(status_code=404, detail="Setting not found")


@router.get("/global_id/")
def get_setting_global():
    """
    Get the current global setting.

    Returns:
        dict: The current global setting.
    """
    return get_setting()
