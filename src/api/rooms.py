from fastapi import APIRouter, Body, Query
from datetime import date

from src.database import async_session_maker
from src.repo.rooms import RoomsRepository
from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest, RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Получение номеров отеля")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-07-01"),
        date_to: date = Query(example="2025-07-10")
):
    rooms = await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return {"status": "OK", "data": rooms}

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение данных конкретного номера")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    return {"status": "OK", "data": room}

@router.post("/{hotel_id}/rooms", summary="Создание номера отеля")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Премиум номер",
                "description": "",
                "value": {
                    "title": "Премиум номер",
                    "description": "Просторный номер с видом на море",
                    "price": 10000,
                    "quantity": 10,
                    "facilities_ids": []
                }
            }
        }
    )
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    new_room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomFacilityAdd(room_id=new_room.id, facility_id=facility_id) for facility_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": new_room}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение данных номера")
async def put_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest = Body(openapi_examples={
        "1": {
            "summary": "Эконом номер",
            "description": "",
            "value": {
                "title": "Эконом номер",
                "description": "Компактный номер с видом на море",
                "price": 3000,
                "quantity": 50,
                "facilities_ids": []
            }
        }
    })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id)
    await update_room_facilities(db, room_id, room_data)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных номера")
async def patch_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await update_room_facilities(db, room_id, room_data)
    await db.commit()
    return {"status": "OK"}

async def update_room_facilities(db: DBDep, room_id: int, room_data: RoomAddRequest | RoomPatchRequest):
    current_rooms_facilities = await db.rooms_facilities.get_filtered(room_id=room_id)
    current_facilities_ids = [room_facility.facility_id for room_facility in current_rooms_facilities]
    facilities_to_delete = [facility_id for facility_id in current_facilities_ids if
                            facility_id not in room_data.facilities_ids]
    facilities_to_add = [
        RoomFacilityAdd(facility_id=facility_id, room_id=room_id) for facility_id in room_data.facilities_ids
        if facility_id not in current_facilities_ids
    ]
    if len(facilities_to_add):
        await db.rooms_facilities.add_bulk(facilities_to_add)
    if len(facilities_to_delete):
        await db.rooms_facilities.delete(room_id=room_id, facilities_ids=facilities_to_delete)