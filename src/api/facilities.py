from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAddRequest

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("", summary="Получить список всех удобств")
async def get_facilities(db: DBDep):
    facilities = await db.facilities.get_all()
    return {"status": "OK", "data": facilities}

@router.post("", summary="Добавить новое удобство")
async def get_facilities(db: DBDep, facility_data: FacilityAddRequest):
    new_facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": new_facility}