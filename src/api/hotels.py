from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.database import async_session_maker, engine
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

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
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        limit = per_page
        offset = per_page * (pagination.page - 1)
        query = select(HotelsModel)
        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(location.lower()))
        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(title.lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

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