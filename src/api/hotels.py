from fastapi import Query, APIRouter, Body

from src.database import async_session_maker, engine
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.repo.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get(
    "/",
    summary="Получить список отелей"
)
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="адрес"),
        title: str | None = Query(None, description="название отеля")
):
    async with async_session_maker() as session:
        per_page = pagination.per_page or 5
        offset = per_page * (pagination.page - 1)
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=offset
        )

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return hotel

@router.delete(
    "/{hotel_id}",
    summary="Удалить отель"
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        repo = HotelsRepository(session)
        await repo.delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.post(
    "",
    summary="Создание отеля"
)
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1" : {
                "summary": "Сочи",
                "description": "",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря, 1"
                }
            },
            "2" : {
                "summary": "Дубай",
                "description": "",
                "value": {
                    "title": "Отель Дубай у фонтана",
                    "location": "ул. Шейха, 2"
                }
            }
        })
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}

@router.put(
    "/{hotel_id}",
    summary="Полное изменение данных отеля"
)
async def put_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное изменение данных отеля"
)
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}