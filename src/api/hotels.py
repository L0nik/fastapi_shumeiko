from fastapi import Query, APIRouter, Body

from sqlalchemy import insert

from src.database import async_session_maker, engine
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get(
    "/",
    summary="Получить список отелей"
)
def get_hotels(
        pagination: PaginationDep,
        hotel_id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="название отеля")
):
    result = []
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        result.append(hotel)

    last_index = pagination.page * pagination.per_page
    first_index = last_index - pagination.per_page

    return result[first_index:last_index]

@router.delete(
    "/{hotel_id}",
    summary="Удалить отель"
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
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
        add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}

@router.put(
    "/{hotel_id}",
    summary="Полное изменение данных отеля"
)
def put_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное изменение данных отеля"
)
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}