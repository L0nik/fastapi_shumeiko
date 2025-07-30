from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repo.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Получение номеров отеля")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(hotel_id=hotel_id)
    return {"status": "OK", "data": rooms}

@router.post("/{hotel_id}/rooms", summary="Создание номера отеля")
async def create_room(
        hotel_id: int,
        room_data: RoomAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Премиум номер",
                    "description": "",
                    "value": {
                        "hotel_id": 1,
                        "title": "Премиум номер",
                        "description": "Просторный номер с видом на море",
                        "price": 10000,
                        "quantity": 10,
                    }
                }
            }
        )
):
    async with async_session_maker() as session:
        new_room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": new_room}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение данных номера")
async def put_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAdd = Body(openapi_examples={
            "1": {
                "summary": "Эконом номер",
                "description": "",
                "value": {
                    "hotel_id": 1,
                    "title": "Эконом номер",
                    "description": "Компактный номер с видом на море",
                    "price": 3000,
                    "quantity": 50,
                }
            }
        })
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPatch):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}