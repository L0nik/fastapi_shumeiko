from fastapi import Query, Body, APIRouter

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]

@router.get(
    "/",
    summary="Получить список отелей"
)
def get_hotels(
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
    return result

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
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1, "title": title}
    )
    return {"status": "OK"}

@router.put(
    "/{hotel_id}",
    summary="Полное изменение данных отеля"
)
def put_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True)
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное изменение данных отеля"
)
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None, embed=True),
        name: str | None = Body(None, embed=True)
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}