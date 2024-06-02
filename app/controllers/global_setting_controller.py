from fastapi import FastAPI, HTTPException, APIRouter, Query
from ..services.driver.global_setting_crud import init_global, update_id_global, get_setting

router = APIRouter()


@router.post("/init_global/")
def create():
    return "Init"


@router.put("/update_global/{setting_id}")
def update(setting_id: str):
    updated = update_id_global(setting_id)
    if updated:
        return {"message": "Setting set successfully."}

    else:
        raise HTTPException(status_code=404, detail="Setting not found")


@router.get("/global_id/")
def get_setting_global():
    return get_setting()
