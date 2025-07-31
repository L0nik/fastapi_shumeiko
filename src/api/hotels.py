from fastapi import Query, APIRouter, Body

from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get(
    "/",
    summary="Получить список отелей"
)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="адрес"),
        title: str | None = Query(None, description="название отеля")
):
    per_page = pagination.per_page or 5
    offset = per_page * (pagination.page - 1)
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=offset
    )

@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    return hotel

@router.delete(
    "/{hotel_id}",
    summary="Удалить отель"
)
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.post(
    "",
    summary="Создание отеля"
)
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}

@router.put(
    "/{hotel_id}",
    summary="Полное изменение данных отеля"
)
async def put_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelAdd
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное изменение данных отеля"
)
async def patch_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPATCH
):
    await db.hotels.edit(hotel_data, True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}